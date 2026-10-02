# Claude Code

Checked on 2.1.282–2.1.283 (the CLI updates itself).

## Contents

- Paths
- Behavior
- Hooks
- Sandbox
- Probes

## Paths

- Skills `~/.claude/skills/<name>/SKILL.md`; project `.claude/skills/`.
  Symlinked skills work; Claude sees the symlink path (probe 2026-09-25).
- Stance `~/.claude/CLAUDE.md` — a symlink to
  `global/stance/claude-stance.md`; a target with another name is read (probe
  2026-09-28). Project `CLAUDE.md`; with no `CLAUDE.md`, `.claude/CLAUDE.md`
  or `CLAUDE.local.md` in cwd or above (the user's `~/.claude/CLAUDE.md`
  does not count), every `AGENTS.md` there instead — from 2.1.277, switch
  Project instructions in `/config` (docs). A VS Code session in
  context-development had `~/AGENTS.md` as project instructions (2026-10-02),
  so such a project pays for both stances.
- Rules `~/.claude/rules/*.md` are always in context (dir not created).
- Project memory (docs, code.claude.com/docs/en/memory): an `@path` in
  `CLAUDE.md` or a read `AGENTS.md` is expanded at launch, relative to that
  file; an import cuts no cost — its text loads at launch too. An import
  that resolves outside the working directory is external: the first time,
  a dialog asks to approve it for the project; declined, it stays off.
  `.claude/rules/*.md` is more of this memory, not Cursor's `.cursor/rules/`:
  without `paths` it loads at launch like `.claude/CLAUDE.md`, with `paths`
  when Claude reads a matching file. A rules symlink pointing outside is an
  external import too, and the dialog appears only for an `@` import, never
  for a symlink alone. `~/.claude/CLAUDE.md` and `~/.claude/rules/` import
  with no dialog.
  Probe 2026-10-02, 2.1.286, `-p`, empty dir in `~`: a relative `@` and a
  rules file or symlink inside the project loaded; an absolute `@` outside
  and a rules symlink pointing outside did not, with no dialog and no denial
  in the result — interactive approval not run. A rule with
  `paths: ["**/*.dart"]` was absent from the initial context; loading on a
  `.dart` read not checked.
- Commands `~/.claude/commands/*.md` — not used, the dir is gone (2026-09-28).
- Settings `~/.claude/settings.json`; hook scripts in `~/.claude/hooks/`.
- `~/.claude/skills/synced/` — skills synced from the claude.ai account; not
  ours, untracked. The model lists them as `anthropic-skills:<name>` (probe
  2026-09-28).

## Behavior (probes 2026-09-26 unless marked)

- Command and skill are one mechanism: `commands/<name>.md` and
  `skills/<name>/SKILL.md` both give `/name`; on a name clash the skill wins
  (docs).
- One skill name in `~/.claude/skills/` and the project's `.claude/skills/`:
  the personal one runs (docs; probe 2026-09-27).
- A personal command named like a bundled alias wins: `/review` ran
  `~/.claude/commands/review.md`, not `/code-review` (probe 2026-09-27). The
  docs only say a skill does not take over a bundled command's aliases.
- Without `disable-model-invocation` the model sees the description and
  invokes the skill itself; with `disable-model-invocation: true` the
  description is not in context and `/name` still works in the CLI. The
  model's skill list then lacks the skill: in a VS Code extension session
  `gogogo` joined the list the moment the flag was removed (2026-09-27). A
  `/name` that reaches the model as text then fails — upstream issues #78523
  (open), #77740, #26251.
- `$ARGUMENTS` is substituted (`$0` is the first argument, docs); without a
  placeholder the arguments still arrive.
- A nested `CLAUDE.md` is loaded when Claude reads a file in its dir, not at
  startup (2.1.282).
- A changed skill description is picked up through a symlink without
  restarting the session (2026-09-27).

## Hooks (`settings.json`)

- PreToolUse `Bash`: `hooks/git_guard.py` — a symlink into `global/hooks/`,
  whose script holds the whitelist and its test — behind
  `|| { rc=$?; … exit 2; }`: exit 1 (a SyntaxError) and 127 (no `python3`)
  would let the command run; the guard's own exit 2 keeps its reason with no
  extra line. Shell history lives only in the transcripts,
  `~/.claude/projects/<path>/<session>.jsonl`, kept 30 days by default
  (`cleanupPeriodDays`, docs); there is no separate audit log.
- PostToolUse `Write|Edit`, `timeout` 30: `hooks/dart_format.sh` — a
  symlink into `local/coding/dart-flutter/hooks/`, shared with Cursor. It
  formats a `.dart` file with the SDK its nearest `.fvmrc` pins, taken from
  the fvm cache (`dart` from `PATH` when unpinned), and never installs:
  `fvm dart` installs a missing SDK by itself, with no prompt even under
  `--fvm-skip-input` (probe 2026-10-02, fvm 4.0.5). A missing SDK or a
  format error exits 2, so Claude gets stderr (probe 2026-10-02). Stop,
  Notification, PermissionRequest: macOS notification and sound.
- Every hook command but the guard starts with guards: exit when
  `CURSOR_VERSION` is set (Cursor CLI), and when `CURSOR_TRACE_ID` is set
  unless the parent is the Anthropic extension (Cursor IDE). The guard has
  none: Claude Code started from a shell that inherited `CURSOR_*` would run
  without it; if Cursor runs it too, it is the same script.
- Edits to hooks in `settings.json` are picked up by a file watcher (docs):
  a running session blocked with the new guard command, no restart (probe
  2026-09-29, 2.1.283).
- Protocol (probe 2026-09-28, 2.1.283): exit 2 blocks, and the model gets
  stderr as `PreToolUse:Bash hook error: [<command>]: <stderr>`; exit 1 lets
  the command run (`hook_non_blocking_error` in the transcript); exit 0 lets it
  run with empty stdout and with Cursor's `{"permission":"allow"}`
  (`hook_success`). Input: `hook_event_name` `PreToolUse`, `tool_name` `Bash`,
  `tool_input.command` a string. By the docs a timed-out hook does not block
  (default 600 s); top-level `{"decision": "block"}` is no longer documented.

## Sandbox

- Boundary (14.4.4): `sandbox` in `settings.json` — Bash writes only in cwd,
  `additionalDirectories`, `$TMPDIR` (`/tmp/claude-501`) and `allowWrite`
  (`~/fvm`, `~/.pub-cache`), with no prompt inside
  (`autoAllowBashIfSandboxed`). A write outside gets "Operation not
  permitted"; the change reached this running session with no restart.
- Leaving it takes `dangerouslyDisableSandbox`; the ask rule
  `Bash(dangerouslyDisableSandbox:true)` sends it to the user. In `-p` auto
  mode it stopped at "needs approval"; without the rule the auto classifier
  decided on its own ("[Auto-Mode Bypass]"). In the VS Code auto mode
  session every escape prompted the user.
- Without the sandbox only critical paths — `/`, top-level dirs, `~`, cwd and
  its parents — always prompt for `rm` (docs); the rest outside the project
  went to the auto classifier, which let `sed -i`, `rm` and `find -delete`
  through once the prompt claimed the user's consent.
- Dart and Flutter: `flutter test` needs `network.allowLocalBinding`, else
  "Failed to create server socket … Operation not permitted" on 127.0.0.1;
  `pub` needs `enableWeakerNetworkIsolation`, else "Got TLS error trying to
  find package" — the docs name it only for `gh`, `gcloud`, `terraform`.
  `network.allowedDomains: ["*"]` opens every host (`curl` got 200 in Manual
  mode, which has no per-command hosts). With these, `pub add`,
  `flutter test`, `dart test` and JE's drift and widget tests pass.
- Protected paths stay read-only for Bash inside writable dirs: most of
  `~/.claude`, and the target of a protected symlink —
  `global/stance/claude-stance.md` behind `~/.claude/CLAUDE.md`. Edit and
  Write are not sandboxed.
- Web tools: `WebSearch` and a bare `WebFetch` in `permissions.allow` — search
  and page reads never ask, Manual mode included (`-p`, no denials).

## Probes

- Non-interactive: `claude -p "<prompt>"`; to let a skill run a script, add
  `--allowedTools "Bash(bash:*)"`.
- From inside Claude Code:
  `env -i HOME=$HOME PATH=$PATH USER=$USER LOGNAME=$LOGNAME claude -p …` —
  without `USER` and `LOGNAME` it reports "Not logged in".
- `--setting-sources=project` leaves the personal skills out — probes a
  project skill that has a same-named copy in `~/.claude/skills/`
  (2026-09-27).
- Sandbox probe: `--settings <file>` merges the file into the personal
  settings; try a sandbox change that way before `settings.json`, since this
  session's own Bash is sandboxed from then on and cannot write
  `~/.claude/projects` or `~/.codex` for a child harness.
- Hook probe: `--settings <file> --setting-sources project` runs the file's
  hooks without the personal ones — the user audit hook logged nothing
  (2026-09-28).
- Run from an empty dir in `~`, not inside a repo; the expected answer must
  exist only in the file under test.
- Traces: `~/.claude/projects/<path>/`.
- The model's skill list: in the trace `<session>.jsonl`, the entry with
  `attachment.type: skill_listing` — its `content` holds one
  `- name: description` line per entry, commands included. Every description
  came whole on 2.1.286 (`-p`, 2026-10-02): context-development 27 entries,
  14.9k chars, of them ours 5 — 2.4k, built-ins and claude.ai account skills
  22 — 12.5k; JE 66 entries, 23.6k, ours 40 — 10.6k. By the docs the
  listing gets 1% of the window, `description` plus `when_to_use` is cut at
  1,536 chars, and past the budget the least-invoked skills lose their
  descriptions first (not probed). The `stream-json` init `skills` is another set: no commands,
  plus built-ins the model is not shown.
