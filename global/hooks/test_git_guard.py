#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).with_name("git_guard.py")
ALLOW_LINE = json.dumps({"permission": "allow"})

BLOCK = [
    "git commit -m x",
    "git push origin main",
    "git -C . commit -m x",
    "sudo git push",
    "env FOO=1 git reset --hard",
    "cd x && git reset --hard",
    "fvm flutter test; git checkout -- .",
    "echo a | git apply",
    "git add .",
    "git clean -fd",
    "git restore .",
    "git switch main",
    "git worktree add ../w",
    "git cherry-pick abc",
    "git -c user.name=x commit -m y",
    "git --git-dir=/tmp/.git rm f",
    "python3 - <<'PY'\nprint(1)\nPY\ngit checkout -- /dev/null",
    "git\tcommit -m x",
    'echo "$(git commit -m x)"',
    'echo "`git commit -m x`"',
    "echo `git stash`",
    "sh -c 'git commit -m x'",
    'bash -lc "cd x && git push"',
    "sudo zsh -c 'git push'",
    "/usr/bin/git commit -m x",
    "GIT commit -m x",
    "command git commit -m x",
    "xargs git add",
    "find . -name x -exec git rm {} +",
    "(cd x && git commit -m y)",
    "echo x\ngit commit -m y",
    "git status \\\n&& git commit -m y",
    "git reflog expire --all",
    "git grep -O x",
    "git branch -D x",
    "git stash",
    "git history reword HEAD",
    'git commit -m "unbalanced',
]

ALLOW = [
    "git status",
    "git status --short",
    "git diff",
    "git diff --stat HEAD~1",
    "git -C /tmp diff",
    "git --no-pager diff",
    "git mv a.dart b.dart",
    "git mv -f a b",
    "fvm flutter test",
    "grep -rn 'git commit' docs/",
    "ls -la hooks/",
    "echo 'digital gitlab legit'",
    "cat lib/main.dart",
    "git",
    "git --version",
    "python3 - <<'PY'\nfrom pathlib import Path\n"
    "print('git commit inside string')\nPY",
    "git --no-pager log",
    "git log --oneline -5",
    "git log | head -5",
    "git show HEAD",
    "git blame lib/main.dart",
    "git ls-files",
    "git ls-tree -r --name-only HEAD docs/",
    "git check-ignore -v x",
    "git rev-parse --show-toplevel",
    "$(git rev-parse HEAD)",
    'echo "$(git log -1 --format=%H)"',
    "sh -c 'git status'",
    "grep -rn git docs/",
    "rg -n git lib",
    "echo git commit",
    "$(xcrun --find git)",
    "which git; echo ok",
    "cd git && ls",
    "git diff > /tmp/x.patch",
]

SHAPES = {
    "claude-codex": lambda command: {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    },
    "cursor": lambda command: {
        "hook_event_name": "beforeShellExecution",
        "command": command,
    },
    "cursor-claude": lambda command: {
        "hook_event_name": "preToolUse",
        "tool_name": "Shell",
        "tool_input": {"command": command},
    },
}

RAW = [
    ("block", "not json"),
    ("block", "[]"),
    (
        "block",
        json.dumps(
            {"tool_name": "Bash", "tool_input": {"command": ["git", "push"]}}
        ),
    ),
    (
        "allow",
        json.dumps(
            {
                "tool_name": "apply_patch",
                "tool_input": {
                    "command": "*** Begin Patch\n*** Update File: a.sh\n@@\n"
                    " git commit -m x\n*** End Patch"
                },
            }
        ),
    ),
    ("allow", json.dumps({"tool_name": "Bash", "tool_input": {}})),
]


def decision(raw, allow_output=""):
    out = subprocess.run(
        [sys.executable, str(GUARD)],
        input=raw,
        capture_output=True,
        text=True,
    )
    if out.returncode == 2 and out.stderr.strip():
        return "block"
    if out.returncode == 0 and out.stdout.strip() == allow_output:
        return "allow"
    return (
        f"broken: exit={out.returncode} out={out.stdout!r} "
        f"err={out.stderr!r}"
    )


def main():
    failures = []
    for expected, commands in (("block", BLOCK), ("allow", ALLOW)):
        for command in commands:
            for shape, build in SHAPES.items():
                allow_output = ALLOW_LINE if shape == "cursor" else ""
                got = decision(json.dumps(build(command)), allow_output)
                if got != expected:
                    failures.append(f"{shape} {command!r}: {got}")
    for expected, raw in RAW:
        got = decision(raw)
        if got != expected:
            failures.append(f"raw {raw!r}: {got}")
    total = (len(BLOCK) + len(ALLOW)) * len(SHAPES) + len(RAW)
    for line in failures:
        print(line)
    print(f"{total - len(failures)}/{total} cases correct")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
