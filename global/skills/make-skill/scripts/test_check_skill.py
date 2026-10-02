#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
from pathlib import Path

CHECK = Path(__file__).with_name("check_skill.py")
GOOD = "name: demo\ndescription: Does a thing. Use when testing."


def skill(front, body="Body.\n"):
    return f"---\n{front}\n---\n{body}"


def only(front):
    return {"SKILL.md": skill(front)}


def described(text):
    return only(f"name: demo\ndescription: {text}")


def named(name):
    return only(f"name: {name}\ndescription: D."), name


OK = [
    only(GOOD),
    described('"Topic: list. Use when x."'),
    described("'It''s fine: yes'"),
    described(">\n  Topic: list.\n  Use when x."),
    described("|-\n  a: b"),
    described("Does a thing\n  across two lines."),
    described("a" * 400),
    described("Use C# or F# here."),
    described("Use when returning Result<T>."),
    only("name: demo\ndescription: D.\nargument-hint: [item number]"),
    only("name: demo\ndescription: D.\nargument-hint: []"),
    only(
        'name: demo\ndescription: D.\nlicense: MIT\nmetadata:\n  author: x\n'
        '  version: "1.0"\n  sources:\n    - A, B\n    - C'
    ),
    only("# note\nname: demo\ndescription: D."),
    {"SKILL.md": skill(GOOD, "x\n" * 500)},
    named("a" * 64),
    {
        "SKILL.md": skill(
            GOOD,
            "See [a](references/a.md), [w](https://x.y/z), [t](#top).\n"
            "Code `[m](Self::method)` is not a link.\n"
            "```\n[x](missing.md)\n```\n",
        ),
        "references/a.md": "A.\n",
    },
    {
        "SKILL.md": skill(GOOD, "Read `references/b.md` when needed.\n"),
        "references/b.md": "B.\n",
    },
]

ERROR = [
    ("SKILL.md not found", {"README.md": "x"}),
    ("frontmatter block", {"SKILL.md": "name: demo\n"}),
    ("': '", described("Topic: list.")),
    ("': '", described("Use when:")),
    ("': '", described("Does a thing\n  then: breaks.")),
    ("' #'", described("Use when #1 fails.")),
    ("cannot start with '`'", described("`x` does y.")),
    ("cannot start with '*'", described("*bold* text")),
    ("cannot start with '{'", described("{a: b}")),
    ("quoting", described('"unclosed')),
    ("quoting", described("'a'b'")),
    ("unclosed '['", only("name: demo\ndescription: D.\nargument-hint: [a")),
    (
        "nested brackets",
        only("name: demo\ndescription: D.\nargument-hint: [a, [b]]"),
    ),
    ("expected 'key: value'", only(GOOD + "\njust text")),
    ("expected 'key: value'", only(GOOD + "\nlicense:MIT")),
    ("neither", only(GOOD + "\nmetadata:\n  just text")),
    ("': '", only(GOOD + "\nmetadata:\n  note: a: b")),
    ("': '", only(GOOD + "\nmetadata:\n  - a: b")),
    ("tab", only(GOOD + "\nmetadata:\n\tauthor: x")),
    ("duplicate key 'name'", only("name: demo\n" + GOOD)),
    ("unknown frontmatter key 'desciption'", only("name: demo\ndesciption: D.")),
    ("'description' is missing", only("name: demo")),
    ("'description' is missing", only("name: demo\ndescription:")),
    ("'name' is missing", only("description: D.")),
    ("differs from the folder", only("name: other\ndescription: D.")),
    ("must be 1-64", *named("Demo")),
    ("must be 1-64", *named("de--mo")),
    ("must be 1-64", *named("-demo")),
    ("must be 1-64", *named("a" * 65)),
    ("limit is 1024", described("a" * 1025)),
    ("broken link", {"SKILL.md": skill(GOOD, "[a](references/no.md)\n")}),
    (
        "leaves the skill folder",
        {"SKILL.md": skill(GOOD, "[a](../other/SKILL.md)\n")},
    ),
    (
        "broken link",
        {
            "SKILL.md": skill(GOOD, "Read [a](references/a.md).\n"),
            "references/a.md": "See [b](b.md#part).\n",
        },
    ),
    (
        "broken symlink",
        {
            "SKILL.md": skill(GOOD, "Read `references/x.md`.\n"),
            "references/x.md": ("symlink", "/nonexistent/check-skill-target"),
        },
    ),
    (
        "nested instructions",
        {
            "SKILL.md": skill(GOOD, "Read `references/claude.md`.\n"),
            "references/claude.md": "x\n",
        },
    ),
    ("nested instructions", {"SKILL.md": skill(GOOD), "AGENTS.md": "x\n"}),
]

WARNING = [
    ("over 400", described("a" * 401)),
    ("over 500", {"SKILL.md": skill(GOOD, "x\n" * 501)}),
    (
        "never read",
        {"SKILL.md": skill(GOOD), "references/c.md": "C.\n"},
    ),
]


def build(base, files, folder):
    root = Path(base) / folder
    root.mkdir()
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, tuple):
            os.symlink(content[1], path)
        else:
            path.write_text(content, encoding="utf-8")
    return root


def outcome(files, folder="demo"):
    with tempfile.TemporaryDirectory() as base:
        root = build(base, files, folder)
        out = subprocess.run(
            [sys.executable, str(CHECK), str(root)],
            capture_output=True,
            text=True,
        )
    return out.returncode, out.stdout


def verdict(expected, needle, code, stdout):
    lines = stdout.splitlines()
    if expected == "ok":
        return code == 0 and lines[-1].endswith("0 errors, 0 warnings")
    marker = f": {expected}: "
    hit = any(marker in line and needle in line for line in lines)
    return hit and code == (1 if expected == "error" else 0)


def main():
    cases = [
        ("ok", "", *(entry if isinstance(entry, tuple) else (entry, "demo")))
        for entry in OK
    ]
    for expected, table in (("error", ERROR), ("warning", WARNING)):
        for needle, files, *folder in table:
            cases.append((expected, needle, files, (folder or ["demo"])[0]))
    failures = []
    for expected, needle, files, folder in cases:
        code, stdout = outcome(files, folder)
        if not verdict(expected, needle, code, stdout):
            failures.append(f"{expected} {needle!r} {files}: {stdout!r}")
    for line in failures:
        print(line)
    print(f"{len(cases) - len(failures)}/{len(cases)} cases correct")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
