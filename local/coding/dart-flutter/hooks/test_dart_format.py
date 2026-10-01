#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "dart_format.sh"
STUB = (
    "#!/bin/sh\n"
    "printf '%s\\n' {tag} \"$@\" >> \"$LOG\"\n"
    "[ -z \"$FAIL\" ] || {{ echo \"$FAIL\" >&2; exit 65; }}\n"
)
PROJECTS = {
    "pinned": '{"flutter": "9.9.9"}',
    "with space": '{"flutter": "9.9.9"}',
    "missing": '{"flutter": "8.8.8"}',
    "broken": "not json",
    "nokey": '{"flavors": {}}',
}
CASES = [
    ("pinned/lib/a.dart", 0, "pinned"),
    ("pinned/packages/p/lib/b.dart", 0, "pinned"),
    ("with space/lib/c.dart", 0, "pinned"),
    ("free/lib/d.dart", 0, "global"),
    ("pinned/lib/notes.md", 0, None),
    ("pinned/lib/gone.dart", 0, None),
    ("missing/lib/e.dart", 2, None),
    ("broken/lib/f.dart", 2, None),
    ("nokey/lib/g.dart", 2, None),
]
SHAPES = {
    "claude-edit": lambda p: {"tool_name": "Edit", "tool_input": {"file_path": p}},
    "claude-write": lambda p: {"tool_response": {"filePath": p}},
    "cursor": lambda p: {"hook_event_name": "afterFileEdit", "file_path": p},
}
RAW = [("{}", 0), ("not json", 2)]


def write_stub(path, tag):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(STUB.format(tag=tag))
    path.chmod(0o755)


def build(root):
    write_stub(root / "cache/versions/9.9.9/bin/dart", "pinned")
    write_stub(root / "bin/dart", "global")
    for name, fvmrc in PROJECTS.items():
        (root / name).mkdir()
        (root / name / ".fvmrc").write_text(fvmrc)
    for path, _, _ in CASES:
        if "gone" not in path:
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            (root / path).write_text("void main(){}\n")


def run(bash, root, payload, cwd=None, fail=""):
    log = root / "log"
    if log.exists():
        log.unlink()
    env = dict(
        os.environ,
        PATH=f"{root / 'bin'}:{os.environ['PATH']}",
        FVM_CACHE_PATH=str(root / "cache"),
        LOG=str(log),
        FAIL=fail,
    )
    out = subprocess.run(
        [bash, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        cwd=cwd or root,
        env=env,
    )
    calls = log.read_text().splitlines() if log.exists() else []
    return out.returncode, out.stderr, calls


def check(got, code, calls, hint):
    got_code, err, got_calls = got
    if got_code != code or got_calls != calls:
        return f"exit={got_code} calls={got_calls} err={err.strip()!r}"
    if code == 2 and hint not in err:
        return f"stderr without {hint!r}: {err.strip()!r}"
    return None


def cases(bash, root):
    for path, code, tag in CASES:
        calls = [tag, "format", str(root / path)] if tag else []
        hint = "fvm install" if code == 2 else ""
        for shape, make in SHAPES.items():
            payload = json.dumps(make(str(root / path)))
            got = run(bash, root, payload)
            yield f"{shape} {path}", got, code, calls, hint
    a = str(root / "pinned/lib/a.dart")
    yield "relative path", run(
        bash, root, json.dumps(SHAPES["cursor"]("lib/a.dart")), root / "pinned"
    ), 0, ["pinned", "format", a], ""
    yield "format error", run(
        bash, root, json.dumps(SHAPES["cursor"](a)), fail="parse error"
    ), 2, ["pinned", "format", a], "parse error"
    for raw, code in RAW:
        yield f"raw {raw!r}", run(bash, root, raw), code, [], "jq"


def main():
    failures = []
    total = 0
    for bash in sorted({"/bin/bash", shutil.which("bash")} - {None}):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            build(root)
            for name, got, code, calls, hint in cases(bash, root):
                total += 1
                problem = check(got, code, calls, hint)
                if problem:
                    failures.append(f"{bash} {name}: {problem}")
    for line in failures:
        print(line)
    print(f"{total - len(failures)}/{total} cases correct")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
