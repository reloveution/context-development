#!/usr/bin/env python3
import json
import shlex
import sys

ALLOWED = {
    "blame",
    "check-ignore",
    "diff",
    "log",
    "ls-files",
    "ls-tree",
    "mv",
    "rev-parse",
    "show",
    "status",
}
VALUE_OPTS = {
    "-C",
    "-c",
    "--git-dir",
    "--work-tree",
    "--namespace",
    "--exec-path",
    "--super-prefix",
    "--config-env",
}
TEXT_COMMANDS = {"grep", "rg", "echo", "printf", "cat"}
SHELLS = {"sh", "bash", "zsh", "dash", "eval"}
SHELL_TOOLS = {"Bash", "Shell"}
PUNCTUATION = "();<>|&`\n"
ASK = "Do not retry it in another form; ask the user."
REASON = (
    "git mutations are manual only. Allowed: "
    + ", ".join("git " + name for name in sorted(ALLOWED))
    + ". "
    + ASK
)
ALLOW = json.dumps({"permission": "allow"})
CURSOR_EVENT = "beforeShellExecution"


def tokenize(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=PUNCTUATION)
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def segments(tokens):
    current = []
    for token in tokens:
        if token and all(char in PUNCTUATION for char in token):
            yield current
            current = []
        else:
            current.append(token)
    yield current


def name_of(token):
    return token.rsplit("/", 1)[-1].lower()


def exempt(first):
    return first.startswith("#") or name_of(first) in TEXT_COMMANDS


def subcommand_after(segment, index):
    rest = iter(segment[index + 1:])
    for token in rest:
        if token in VALUE_OPTS:
            next(rest, None)
        elif not token.startswith("-"):
            return token
    return None


def invoked(segment):
    found = []
    after_shell = False
    for index, token in enumerate(segment):
        if after_shell and not token.startswith("-"):
            found += violations(token)
        name = name_of(token)
        if name in SHELLS:
            after_shell = True
        elif name == "git":
            sub = subcommand_after(segment, index)
            if sub is not None and sub not in ALLOWED:
                found.append(sub)
    return found


def violations(command):
    found = []
    for segment in segments(tokenize(command)):
        for token in segment:
            if "$(" in token or "`" in token:
                found += violations(token)
        if segment and not exempt(segment[0]):
            found += invoked(segment)
    return found


def command_of(payload):
    if payload.get("tool_name", "Bash") not in SHELL_TOOLS:
        return None
    if "command" in payload:
        return payload["command"]
    return payload.get("tool_input", {}).get("command")


def verdict(payload):
    command = command_of(payload)
    if command is None:
        return None
    if not isinstance(command, str):
        return "git_guard: the command is not a string. " + ASK
    if "git" not in command.lower():
        return None
    found = violations(command.replace("\\\n", ""))
    return "git " + found[0] + ": " + REASON if found else None


def main():
    try:
        payload = json.loads(sys.stdin.read())
        reason = verdict(payload)
    except Exception as error:
        reason = "git_guard failed (" + repr(error) + "). " + ASK
    if reason:
        sys.stderr.write(reason + "\n")
        return 2
    if payload.get("hook_event_name") == CURSOR_EVENT:
        print(ALLOW)
    return 0


if __name__ == "__main__":
    sys.exit(main())
