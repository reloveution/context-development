#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

KNOWN_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "background",
    "hooks",
    "paths",
    "shell",
}
NAME_MAX = 64
DESCRIPTION_MAX = 1024
DESCRIPTION_BUDGET = 400
BODY_MAX_LINES = 500
NAME_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
KEY_LINE = re.compile(r"([A-Za-z0-9_-]+):(?: (.*))?")
BLOCK_SCALAR = re.compile(r"[>|][-+]?")
DOUBLE_QUOTED = re.compile(r'"(?:[^"\\]|\\.)*"')
SINGLE_QUOTED = re.compile(r"'(?:[^']|'')*'")
FRONTMATTER = re.compile(r"---\n(.*?)\n---(?:\n|$)", re.DOTALL)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
PLAIN_FORBIDDEN_START = set("{},#&*!|>%@`")
INSTRUCTION_FILES = {"claude.md", "agents.md"}


def plain_problem(value):
    if value[0] in PLAIN_FORBIDDEN_START or value[:2] in ("- ", "? ", ": "):
        return f"plain value cannot start with {value[0]!r}: quote it"
    if ": " in value or value.endswith(":"):
        return "plain value holds ': ' — quote it or write '—'"
    if " #" in value:
        return "plain value holds ' #', a YAML comment — quote it"
    return None


def flow_problem(value):
    if not value.endswith("]"):
        return "unclosed '[' list"
    for item in value[1:-1].split(","):
        item = item.strip()
        if any(char in item for char in "[]{}"):
            return "nested brackets in a '[...]' list"
        problem = item and scalar_problem(item)
        if problem:
            return problem
    return None


def scalar_problem(value):
    if value[0] == '"':
        return None if DOUBLE_QUOTED.fullmatch(value) else "broken '\"' quoting"
    if value[0] == "'":
        return None if SINGLE_QUOTED.fullmatch(value) else "broken \"'\" quoting"
    if value[0] == "[":
        return flow_problem(value)
    return plain_problem(value)


def nested_problem(text):
    if text.startswith("- "):
        return scalar_problem(text[2:].strip())
    match = KEY_LINE.fullmatch(text)
    if not match:
        return f"nested line {text!r} is neither 'key: value' nor '- item'"
    value = (match.group(2) or "").strip()
    return value and scalar_problem(value)


def unquote(value):
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_entry(number, head, rest):
    match = KEY_LINE.fullmatch(head)
    if not match:
        return None, "", [f"frontmatter line {number}: expected 'key: value'"]
    key, value = match.group(1), (match.group(2) or "").strip()
    texts = [line.strip() for line in rest if line.strip()]
    if BLOCK_SCALAR.fullmatch(value):
        return key, " ".join(texts), []
    texts = [text for text in texts if not text.startswith("#")]
    if not value:
        problems = [nested_problem(text) for text in texts]
        return key, "", [f"'{key}': {p}" for p in problems if p]
    problems = [scalar_problem(value)] + [plain_problem(t) for t in texts]
    joined = " ".join([unquote(value)] + texts)
    return key, joined, [f"'{key}': {p}" for p in problems if p]


def entries(lines):
    groups = []
    for number, line in enumerate(lines, 2):
        if line[:1] not in ("", " ") and not line.startswith("#"):
            groups.append((number, line, []))
        elif groups:
            groups[-1][2].append(line)
    return groups


def parse_frontmatter(text):
    if "\t" in text:
        return {}, ["frontmatter holds a tab — YAML forbids tabs in indentation"]
    fields, problems = {}, []
    for number, head, rest in entries(text.split("\n")):
        key, value, entry_problems = read_entry(number, head, rest)
        problems += entry_problems
        if key in fields:
            problems.append(f"duplicate key '{key}'")
        if key:
            fields[key] = value
    return fields, problems


def name_errors(fields, folder):
    name = fields.get("name", "")
    if not name:
        return ["'name' is missing or empty"]
    errors = []
    if len(name) > NAME_MAX or not NAME_PATTERN.fullmatch(name):
        errors.append(
            f"name {name!r} must be 1-{NAME_MAX} chars of a-z, 0-9 and "
            "single inner hyphens"
        )
    if name != folder:
        errors.append(f"name {name!r} differs from the folder {folder!r}")
    return errors


def description_errors(fields):
    description = fields.get("description", "")
    if not description:
        return ["'description' is missing or empty"]
    if len(description) > DESCRIPTION_MAX:
        return [
            f"description is {len(description)} chars, the limit is "
            f"{DESCRIPTION_MAX}"
        ]
    return []


def field_problems(fields, folder):
    errors = [
        f"unknown frontmatter key '{key}'"
        for key in sorted(set(fields) - KNOWN_KEYS)
    ]
    errors += name_errors(fields, folder) + description_errors(fields)
    warnings = []
    length = len(fields.get("description", ""))
    if length > DESCRIPTION_BUDGET:
        warnings.append(
            f"description is {length} chars — over {DESCRIPTION_BUDGET}, "
            "about the ~100 tokens the Agent Skills spec allots to metadata "
            "loaded in every session"
        )
    return errors, warnings


def prose(text):
    lines, fenced = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced:
            lines.append(INLINE_CODE.sub("", line))
    return "\n".join(lines)


def link_errors(root, markdown):
    errors = []
    folder = os.path.dirname(markdown)
    text = prose(Path(markdown).read_text(encoding="utf-8"))
    for target in LINK.findall(text):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        path = os.path.normpath(os.path.join(folder, target.split("#")[0]))
        shown = os.path.relpath(markdown, root)
        if not path.startswith(root + os.sep):
            errors.append(f"{shown}: link {target!r} leaves the skill folder")
        elif not os.path.exists(path):
            errors.append(f"{shown}: broken link {target!r}")
    return errors


def tree_errors(root):
    errors = []
    for folder, dirs, files in os.walk(root):
        for name in sorted(dirs + files):
            path = os.path.join(folder, name)
            shown = os.path.relpath(path, root)
            if name.lower() in INSTRUCTION_FILES:
                errors.append(
                    f"{shown}: harnesses load it as nested instructions"
                )
            if os.path.islink(path) and not os.path.exists(path):
                errors.append(f"{shown}: broken symlink")
            if name.endswith(".md") and os.path.isfile(path):
                errors += link_errors(root, path)
    return errors


def orphan_warnings(root, skill_text):
    references = os.path.join(root, "references")
    warnings = []
    for folder, _, files in os.walk(references):
        for name in sorted(files):
            shown = os.path.relpath(os.path.join(folder, name), root)
            if shown not in skill_text:
                warnings.append(
                    f"{shown}: not named in SKILL.md — never read"
                )
    return warnings


def check_skill(root):
    skill_md = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill_md):
        return ["SKILL.md not found"], []
    text = Path(skill_md).read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return ["SKILL.md must start with a '---' frontmatter block"], []
    fields, errors = parse_frontmatter(match.group(1))
    field_errors, warnings = field_problems(fields, os.path.basename(root))
    errors += field_errors + tree_errors(root)
    body_lines = text[match.end():].count("\n")
    if body_lines > BODY_MAX_LINES:
        warnings.append(
            f"body is {body_lines} lines, over {BODY_MAX_LINES} — move "
            "detail to references/"
        )
    return errors, warnings + orphan_warnings(root, text)


def main(argv):
    if not argv:
        print("usage: check_skill.py <skill-dir>...")
        return 2
    error_count = warning_count = 0
    for arg in argv:
        root = os.path.normpath(os.path.abspath(arg))
        errors, warnings = check_skill(root)
        for line in errors:
            print(f"{arg}: error: {line}")
        for line in warnings:
            print(f"{arg}: warning: {line}")
        error_count += len(errors)
        warning_count += len(warnings)
    print(f"{len(argv)} skills, {error_count} errors, {warning_count} warnings")
    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
