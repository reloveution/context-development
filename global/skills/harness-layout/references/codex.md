# Codex

Checked on CLI 0.156.1. Install: Homebrew cask `codex` →
`/opt/homebrew/bin/codex` (the `codex-app` cask is the desktop app, a different
product). Codex is to be dropped later — keep Codex-only files separate.

## Contents

- Paths
- Cost per model call
- Measure
- Skills and commands
- Sandbox
- Hooks
- Probes

## Paths

- Global skills: `~/.codex/skills/` works (probe 2026-09-27), though the docs
  list only `~/.agents/skills/` as the user location. `~/.codex/skills/.system/`
  holds Codex's own skills. Project skills: `.agents/skills/` in cwd and its
  parents up to the repo root (docs), gitignored or not (probe 2026-09-27);
  `.codex/skills/` also works (probe 2026-09-25). Symlinked skill dirs are
  followed (docs, probes). The catalog lists the symlink path (`r0` =
  `~/.codex/skills`) and implicit use reads through it; an explicit `$name`
  injects the body with the real path (rollouts 2026-09-27).
- Stance `~/.codex/AGENTS.md` — a symlink to
  `global/stance/agents-stance.md`; a target with another name is read (probe
  2026-09-27). Project `AGENTS.md` from the git root down to cwd; never above
  the git root, and outside git never above cwd. `CLAUDE.md` is not read
  unless `project_doc_fallback_filenames` names it.
- Project instructions, per the AGENTS.md guide
  (developers.openai.com/codex/guides/agents-md). From the project root down
  to cwd, each directory contributes at most one file: `AGENTS.override.md`,
  then `AGENTS.md`, then `project_doc_fallback_filenames`. The guide
  documents no import syntax. Fallback names apply when `AGENTS.md` is
  missing.
  Probe 2026-10-02, 0.156.1, `codex debug prompt-input`, empty dir in `~`,
  not a git repo; user `config.toml` not edited. It matches the guide: the
  `AGENTS.md` body is in the prompt, `@chunks/….md` stays literal, and with
  `-c 'project_doc_fallback_filenames=["STANCE_CHUNK.md"]'` that file is read
  only when `AGENTS.md` is absent. `CLAUDE.md` and the rules directories are
  absent. A symlink that is itself `AGENTS.md` is followed, including a
  target outside the directory — the guide does not discuss that case.
  `sub/AGENTS.md` was absent; outside git the guide checks only cwd. The
  git-root-to-cwd walk was not probed.
- Settings `~/.codex/config.toml`; annotated key reference
  `~/.codex/CONFIG-REFERENCE.md`. The macOS desktop app ignores `config.toml`
  (open upstream bug); the CLI honors it.
- `~/.codex/rules/` — command approval policy (`prefix_rule`), not
  instructions (docs).

## Cost per model call

Codex bills per call; base instructions, stance, skills catalog and tool
schemas ride in every call of every iteration.

| Change | Per call | Version |
|---|---|---|
| Full stance as `AGENTS.md` (144 lines) | +2 340 tokens | 0.153.4 |
| Minimal `AGENTS.md` (~20 lines) | +237 | 0.153.4 |
| Disable `browser_use`, `browser_use_external`, `browser_use_full_cdp_access`, `computer_use`, `multi_agent`, `image_generation` | −2 895 | 0.153.4 |
| Skills catalog 42 → 9 entries (14 275 → 5 045 chars) | −2 038: 13 566 → 11 528 in an empty dir, 15 720 → 13 682 in a Flutter project | 0.156.1 |
| 32 project skills linked, catalog 9 → 41 entries (4 924 → 13 535 chars) | +1 900: 13 774 → 15 674 in the Flutter project | 0.156.1 |
| Invariants: `developer_instructions` → stance (−355 / +675 chars) | ≈ +80, by chars/4 | 0.156.1 |

- Hence `AGENTS.md` stays short; durable behavior goes into skills.
- `config.toml` → `developer_instructions` holds only hints for Codex's own
  tools (`max_output_tokens`; never propose a `prefix_rule`, see Sandbox).
  The core invariants moved to
  the shared stance (2026-09-27), one text for Codex, Cursor and pi. The
  price: `developer_instructions` sit at the top of the developer message and
  outrank every `AGENTS.md`, while the stance can be overridden by a project
  `AGENTS.md`. Git is held by the `git_guard` hook (see Hooks), the write
  boundary by the sandbox (see Sandbox). The trimmed base instructions (`model-instructions/terra.md:48`) let formatters
  and bulk mechanical rewrites skip `apply_patch`; they outrank the stance,
  so there the stance's file-edit rule likely yields (not probed).
- Base model instructions (~17.7K chars) are replaced wholesale by
  `model_instructions_file` (replacement, not append). Trimmed copy and
  pristine original: `~/.codex/model-instructions/`. After an upgrade re-dump
  the original and re-apply the edits by diff.
- The skills catalog is budgeted by `skills.max_context_tokens`: by the docs
  at most 2% of the window, 8,000 chars when the window is unknown; past it
  descriptions are shortened first, then skills left out with a warning —
  front-load the trigger words. Whole so far: 41 entries at a 555K window
  (2026-09-27); JE 45 entries, 14.8k chars, context-development 10, 5.2k
  (`debug prompt-input`, 2026-10-02).
- `<plugins_instructions>` (~208 tokens) is not injected in every run.
- Feature flags: `codex features list|enable|disable <name>` (writes
  `[features]`); install health: `codex doctor`.

## Measure

- Context composition without a model call: `~/.codex/prompt-breakdown.sh`
  (`codex debug prompt-input`). Its "base instructions" line is the built-in
  template, not `model_instructions_file`.
- The skills catalog: the `<skills_instructions>` block of
  `codex debug prompt-input <text>` run from the project dir — roots `rN`,
  then one `- name: description (file: rN/…)` line per skill. `exec` sends
  the same plus remote plugins' skills
  (`~/.codex/plugins/cache/openai-curated-remote`), which renumbers the roots
  (rollout 2026-09-28).
- Per-call tokens: `~/.codex/token-report.sh` — the `token_usage_record` entries
  of `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. The rollout also stores
  the start-context blocks (`response_item` messages) and
  `session_meta.base_instructions`.
- The first call's input is identical run to run; only the cached share varies
  with the provider cache.

## Skills and commands

- Unknown frontmatter fields are tolerated; `disable-model-invocation` is
  ignored — the model still invokes the skill.
- User-only skill: `agents/openai.yaml` with
  `policy.allow_implicit_invocation: false` — the skill leaves the prompt's
  catalog, `$name` still works in `exec`. The TUI resolves a typed `$name`
  against every enabled skill, hidden ones included (source 0.156.1:
  `skills_to_info` in app-server, `find_skill_mentions_with_tool_mentions` in
  the TUI; not run live); bug #23454, filed on 0.131.0, is open.
- No placeholder substitution; the text after `$name` arrives.
- `[[skills.config]]` with `path` and `enabled = false` turns one skill off;
  `path` names the `SKILL.md` itself — a dir path is silently ignored (earlier
  probe, noted in `config.toml` until 2026-09-27).
- Implicit use: the model reads `SKILL.md` itself with a shell command; on
  `$name` Codex injects the body.
- Custom prompts (`~/.codex/prompts/`, `/prompts:name`) are deprecated (docs).

## Sandbox

- Boundary (14.4.4): writes only in cwd, `/tmp`, `$TMPDIR` and
  `writable_roots` (`~/fvm`, `~/.pub-cache`); leaving it takes the user's
  approval per command (`on-request`; `exec` runs with `approval: never`).
- An allow `prefix_rule` runs the command outside the sandbox with no prompt
  (docs): `sed -i` and `find -delete` changed files outside the roots, while
  `rm` got "Operation not permitted" (2026-09-29). So `rules/default.rules`
  keeps only `pkill -f frontend_server_aot`, which cannot run inside.
- Dart and Flutter inside: `pub get`, `pub add`, `flutter test`,
  `dart analyze`, `dart format`, `git status`, `git log` run with no prompt
  (2026-09-29); without `~/.pub-cache` in the roots a new package fails on
  `~/.pub-cache/hosted-hashes` with "Operation not permitted".
- Web: `web_search = "cached"` searches, and `curl` reads pages inside the
  sandbox (`network_access = true`) — neither asks (2026-09-29).
- `codex exec -s workspace-write -C <root> --add-dir <dir>`: shell commands
  (`ln -sn`, `rm -r`, `rm`, `unlink`, `find -delete`) and `apply_patch` write
  inside `<dir>`, its `.claude/` included; a write outside both gets
  "Operation not permitted".
- `rm -rf` is rejected before it runs ("rm -f style commands are not
  permitted"); the text is not in `model_instructions_file`. `rm -r` passes.
- `pgrep` fails in the sandbox: "sysmond service not found", exit 3 — a
  runbook cannot check for running processes (TUI run 2026-09-28).
- The TUI takes `--add-dir` too (`codex --help`); a TUI started without it
  left the other dir read-only, and `ln` there needed an approved escalation
  (2026-09-28).
- `.git`, `.codex`, `.agents` inside a writable root stay read-only (docs;
  upstream issue #24461: `.agents` even through `--add-dir`) — not probed.

## Hooks

- Sources: `hooks.json` or inline `[hooks]` next to each config layer —
  `~/.codex`, `<repo>/.codex` — and all of them run (docs). Inline hooks from
  `-c 'hooks.PreToolUse=[{hooks=[{type="command",command="…"}]}]'` run too.
  A layer with both is merged with a startup warning (docs) — keep one.
- Configured: inline `[[hooks.PreToolUse]]` in `~/.codex/config.toml`, no
  matcher (the guard passes non-shell tools) → `hooks/git_guard.py`, a
  symlink into `global/hooks/`, behind the same `|| { rc=$?; … exit 2; }` as
  Claude's: a crash or a missing `python3` blocks with a reason.
- Not a hook: `notify` in `config.toml` → `~/.codex/notify.sh`, a macOS
  banner when a turn ends.
- Trust: a non-managed hook runs only after `/hooks` in the TUI trusts its
  definition hash (docs). `exec` skips an untrusted hook silently and the
  command runs; `--dangerously-bypass-hook-trust` lifts the gate. `/hooks`
  writes `[hooks.state."<config path>:pre_tool_use:<group>:<hook>"]
  trusted_hash = "sha256:…"` into `config.toml`, and `exec` honors it for a
  user-level hook (probe 2026-09-29; open issue #32491 is about project
  hooks). Any edit of the entry changes the hash — trust again.
- `PreToolUse` fires for `Bash` and `apply_patch`; `tool_input.command` is a
  string — the shell command or the patch text. Input also has
  `hook_event_name` `PreToolUse`, `tool_name`, `cwd`, `turn_id`, ids.
- Exit 2 blocks only with a non-empty stderr, and the model gets "Command
  blocked by PreToolUse hook: <stderr>. Command: <cmd>"; exit 2 with empty
  stderr, exit 1 and exit 0 — empty or `{"permission":"allow"}` — let the
  command run. Only exit 0 with empty stdout shows `Completed`;
  `{"permission":"allow"}` and exit 1 show `Failed` (2026-09-29), so
  `git_guard` prints it for Cursor's `beforeShellExecution` only. The hook
  command goes through a shell (`;` is honored).
- Hooks run outside the sandbox: the probe hook wrote outside the writable
  roots, and its env had no `CODEX_*` vars.

## Probes

- `codex exec "<prompt>"`; outside a git repo add `--skip-git-repo-check`.
  Nothing else is needed for a skill to run its script.
- From a non-interactive shell `exec` waits for stdin to close — pass
  `< /dev/null`; `--ephemeral` leaves no session file (2026-09-28).
- Traces: `sessions/<date>/rollout-*.jsonl` and `threads` rows in
  `state_5.sqlite`; in a git repo `exec` appends
  `[projects."<path>"] trust_level` to `config.toml`.
- Hook probe: the prompt must authorize the blocked command outright — under
  the stance the model refused `git commit` without trying, so the hook never
  fired (2026-09-29).
