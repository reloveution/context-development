# Cursor CLI

Checked on 2026.09.23-86fc751; probes of 2026-09-27 on 2026.09.26-dd393fe
(the CLI updates itself). Install: script → `~/.local/bin/cursor-agent`
(+ `agent` symlink) → `~/.local/share/cursor-agent/versions/<ver>/` (bash
wrapper, bundled `node`, minified `index.js` — "bundle" below). Auth is
separate from the IDE: `cursor-agent login`, `--api-key` / `--auth-token`, or
`CURSOR_API_KEY` / `CURSOR_AUTH_TOKEN`; without it every subcommand fails.

## Paths

- Skills `~/.cursor/skills/`; project `.cursor/skills/`, `.agents/skills/`.
  Third-party extensibility adds `~/.claude/skills/`, `~/.codex/skills/`,
  `.claude/skills/`, `.codex/skills/` (probe 2026-09-26), claude.ai account
  skills in `~/.claude/skills/synced/<id>/<name>/` included (8 entries, by the
  model's answer, probe 2026-09-27). The catalog also holds Cursor's built-in
  `~/.cursor/skills-cursor/` and installed plugins' skills
  (`~/.cursor/plugins/cache/<marketplace>/<plugin>/…/skills/`). Plugins are
  installed per account (`GetEffectiveUserPluginsRequest`, bundle
  2026.09.28-64d2043) and bring skills, commands, MCP servers and hooks;
  remove one in the interactive `/plugins` (CLI changelog), not by deleting
  the cache. The `parallel` plugin's `parallel-web-search` took web search
  over from Cursor's own tools and called a missing `parallel-cli`
  (2026-09-29). In the cache (2026-09-29): `figma` 14 skills + MCP, `finance`
  MCP, `orchestrate` 1 skill, `parallel` 4 skills, `superpowers` 14 skills,
  a subagent and a `SessionStart` hook.
  `~/.agents/skills/` — docs only. One skill dir reached by two paths is one
  skill; same-named copies in the global roots show as one entry (by the
  model's answer, tokens not measured). A global and a project copy are both
  listed, identical content included: in JE 32 names had two paths,
  `~/.cursor/skills/` and a gitignored `.agents/skills/` (by the model's
  answer, probe 2026-09-27). A skill dir linked from all three roots was read
  through `~/.cursor/skills/` (probe 2026-09-27, one run). A project skill
  dir linked from both `.agents/skills/` and `.claude/skills/` is one entry,
  listed by the `.claude/skills/` path (JE: 36 dirs, each path once in the
  chat's `store.db`, 2026-09-28). Same-named but
  different copies in `~/.cursor/skills/` and a project's `.claude/skills/`:
  the project one was read (probe 2026-09-27, one run).
- Implicit use: the model reads an auto skill itself (its body lands in
  `store.db`). `harness-layout` was picked by its description;
  `critical-thinking` was not — 0 of 3 runs (a recommendation, a flaky-test
  cause, a Dart fact) until `~/AGENTS.md` pointed to it, then 3 of 3 (probes
  2026-09-27). Its description was empty then (invalid YAML, below); fixed,
  it is cut in JE before "Use on every non-trivial task" (2026-09-28).
- The skills catalog is a fixed budget: its `<agent_skill fullPath="…">`
  elements totalled ≈19.5k chars at 76–110 entries (`store.db`, 10 chats
  2026-09-25…28). Most descriptions are cut to one length plus `...`,
  falling as entries grow — 116 chars at 78 entries, 50 at 110 — and
  absolute paths eat the same budget. Past the budget, more skills cost no
  tokens but shorten every description: trigger words go first.
- Frontmatter that is not strict YAML leaves the description empty
  (`<agent_skill fullPath="…" />`): a plain description holding `: ` did so
  for `critical-thinking` and `flutter-navigation` in all 10 chats, while
  Claude and Codex showed both whole. Quoted, then reworded without `: `,
  both showed (probes 2026-09-28).
- `disable-model-invocation: true` — the skill leaves the catalog, `/name`
  works. Skills get no placeholder substitution; the text after `/name`
  arrives. Unknown frontmatter fields (`argument-hint`) are tolerated (probe
  2026-09-27).
- `/name` injects the body of a project skill only from a real dir: a symlinked
  skill dir in `.cursor/skills/`, `.agents/skills/` or `.claude/skills/` (target
  outside the project or inside it) or a symlinked `SKILL.md` is not injected,
  with or without `disable-model-invocation`. A symlinked dir in
  `~/.cursor/skills/` or `~/.claude/skills/` is injected (`/review-diff`,
  `/decide`; by `store.db`, one run each). A symlinked project auto skill
  still works: the catalog lists its path and the model reads it. So a
  user-only skill symlinked into a project is unreachable in Cursor (probes
  2026-09-27, one run each) — hence no user-only skills.
- Memory: the bundle carries the memory protocol (`KnowledgeBaseParams` with
  `knowledge_to_store`, `PotentiallyGenerateMemoryResponse`); whether the CLI
  agent stores memories — not checked, the stance forbids it. Sub-agents: a
  Task tool with `subagent_type` and `run_in_background` (bundle
  2026.09.26-dd393fe).
- Commands `~/.cursor/commands/*.md` (dir not created), also
  `~/.claude/commands/` and `.claude/commands/` (bundle); commands enter the
  context only on `/name` and substitute `$ARGUMENTS`, `$1`… (bundle). One
  command file with `description` in its frontmatter worked in both Claude and
  Cursor (probe 2026-09-25).
- Stance and rules: from the project dir up to `/`, not stopping at the git
  root; in every dir `.cursor/rules/`, `AGENTS.md`, `.cursorrules`, and with
  third-party on `CLAUDE.md`, `CLAUDE.local.md` plus nested `.claude/**`,
  `.codex/**`, `.grok/**`. `.md` rules always apply, their frontmatter is not
  parsed (bundle). So `~/AGENTS.md` (a symlink with another target name
  works) acts as the global stance, inside git repos too (probe). Not read
  (probes 2026-09-29, 2026.09.28-64d2043): `~/.cursor/rules/*.md` and
  `*.mdc` without frontmatter, `~/.cursor/AGENTS.md` — the walk-up
  (`dirname` from the project to `/`, bundle) loads `AGENTS.md` only from
  those dirs. Undocumented — the docs name only the project root — so
  recheck `~/AGENTS.md` after a CLI update. `~/.claude/CLAUDE.md` (probe) and `~/.codex/AGENTS.md` (bundle)
  are not read; a project `CLAUDE.md` is — a project with both `CLAUDE.md` and
  `AGENTS.md` pays for both.
- An `.mdc` rule with `description` and no `globs` is Apply Intelligently: the
  model pulls it itself (docs).
- The account's User Rules (IDE: Customize → Rules, docs) reach the CLI in
  every request as `<user_rule>` blocks: 7 rules, ~880 chars, seen in a probe
  chat's `store.db` and quoted back by the model (2026-09-27). No local file
  holds them, so removing the IDE keeps them. Keep them empty — the global
  stance is `~/AGENTS.md`.

## Settings

- `~/.cursor/cli-config.json` is CLI-owned: rewritten on runs, unknown keys
  dropped. `approvalMode: "allowlist"` plus
  `sandbox: {mode: "enabled", networkAccess: "allow_all"}`; `permissions.allow`
  entries are command prefixes (`Shell(git status)` also covers
  `git status --short`). Sub-agent model: `subagentModels.explore` /
  `exploreSubagentModel` = `inherit`.
- Sandbox (probes 2026-09-29, `-p`): a `permissions.allow` match runs the
  command outside the sandbox with no prompt ("matched the user's command
  allowlist") — `sed -i` and `find -delete` changed files outside the
  workspace; every other command runs inside with no prompt, and a write
  outside gets "Operation not permitted" plus a hint to re-run with
  `required_permissions: ["all"]`. In `-p` such a re-run is refused
  ("Rejected:"); the interactive CLI asks the user (user's run 2026-09-29).
- Boundary (14.4.4): writes only in the workspace, `$TMPDIR` and
  `sandbox.json` `additionalReadwritePaths` (`~/fvm`, `~/.pub-cache`); so
  `permissions.allow` keeps no `Shell(...)` but `pkill -f
  frontend_server_aot`. `pub add`, `flutter test`, `dart analyze` run inside
  (2026-09-29).
- Web (bundle 2026.09.28-64d2043, 2026-09-29): `autoAcceptWebSearch: true` —
  search never asks (live, `-p`). `WebFetch(*)` in `permissions.allow` — the
  interactive CLI matches the fetched domain against it, and a bare `*`
  matches all — it fetched with no prompt (user's run). `-p` ignores the
  allowlist for fetch and
  approves it only with `--force`: without it "Web fetch rejected: User
  Rejected" (live). No MCP server duplicates these tools: with Firecrawl in
  `mcp.json` the agent searched through it instead of its own tools, so it
  was removed (2026-09-29), and so was Context7.
- Third-party extensibility cannot be turned off in the CLI: its entry point
  hands the rules, skills and subagents loaders a constant `() => true`
  (bundle 2026.09.26-dd393fe). The IDE toggle "Include Third-Party Plugins,
  Skills, and Other Configs" (docs) does not reach the CLI, which has no
  `cli-config.json` key, flag or env var for it (Cursor staff on the forum,
  2026-07-29).

## Hooks (probe 2026-09-28 on 2026.09.26-dd393fe)

`~/.cursor/hooks.json` and a project's `.cursor/hooks.json` both run, deny
wins (docs): `beforeShellExecution`, `afterFileEdit`. Payload keys are
Cursor's own (`.command`, `.file_path`). Configured: `hooks/git_guard.py` —
a symlink into `global/hooks/`, the same script as Claude's and Codex's;
`hooks/dart_format.sh` (Claude's script, `timeout` 30) after an edit.
`afterFileEdit` is fire-and-forget: its exit 2 and stderr reach neither the
agent nor any file under `~/.cursor` (probe 2026-10-02), so a missing SDK
leaves the file unformatted without a trace. Shell history lives only in
the session traces — `projects/<slug>/agent-transcripts/<id>/<id>.jsonl`
and `chats/<hash>/<id>/store.db` (probe 2026-10-02), retention unknown;
there is no separate audit log.

- `beforeShellExecution` with `failClosed: true`: exit 0 with empty stdout
  blocks ("returned no output") — hence `git_guard` prints
  `{"permission":"allow"}` for this event only; that output runs; exit 1 blocks;
  exit 2 blocks and the agent gets stderr ("Hook blocked with message: …").
  Every block message ends with "Agent note: Do not suggest workarounds to
  the blocked tool." Input: `command`, `hook_event_name`
  `beforeShellExecution`, `cwd`, `sandbox`, `workspace_roots`, `user_email`,
  ids.
- Third-party: the CLI runs Claude-format `PreToolUse` hooks from a project's
  `.claude/settings.json` before `beforeShellExecution`, as `hook_event_name`
  `preToolUse`, `tool_name` `Shell` (matcher `Bash` matches it), with
  `tool_input.command`; empty stdout there does not block.
  `.claude/settings.local.json` and `~/.claude/settings.json` load too (docs);
  Cursor staff say permissions from `.claude/settings.json` apply as well
  (forum, 2026-07-29) — neither probed.
- Hook env, Claude-format hooks included: `CURSOR_VERSION`,
  `CURSOR_PROJECT_DIR`, `CURSOR_USER_EMAIL`, `CURSOR_TRANSCRIPT_PATH`,
  `CURSOR_INVOKED_AS`, `CURSOR_RIPGREP_PATH`; `CLAUDE_PROJECT_DIR` (bundle);
  never `CURSOR_TRACE_ID`.

## MCP and secrets

- Server definitions are global (`~/.cursor/mcp.json`); the disabled list is
  per project (`~/.cursor/projects/<path-slug>/mcp-disabled.json`). A new
  project starts with nothing disabled — from its dir:

  ```bash
  for s in snyk Semgrep "Endor Labs" SonarQube Socket \
           hf-mcp-server Figma "Chrome DevTools"; do
    agent mcp disable "$s"
  done
  ```

- Secrets: `~/.cursor/mcp.env` (0600, outside git); `mcp.json` holds only
  `"env": {"<NAME>": "${env:<NAME>}"}`; a function in `~/.zshrc` loads the file
  for `agent` and `cursor-agent`. The CLI does not read `envFile` and passes no
  env of its own to stdio servers; a missing variable sends the literal
  `${env:NAME}` — an error on the tool call, not at start (probe).

## Measure

- Per-call tokens: `agent -p --output-format json` — `usage.inputTokens`
  (also `outputTokens`, `cacheReadTokens`, `cacheWriteTokens`). Once part of
  the prompt is cached, `inputTokens` drops by `cacheReadTokens`: compare
  their sum.
- A new dir is a new project with every MCP server on: compare runs from an
  empty dir of the same name, recreated each time.
- Baseline before the move to the repo (2026-09-27): empty
  `~/cursor-probe-1451`, prompt `Ответь одним словом: ок` — 25 595 input
  tokens, identical in 2 runs; the catalog had 79 entries.
- After (2026-09-27; stance `~/AGENTS.md` before its `critical-thinking`
  pointer, no rules, `~/.cursor/skills/` only `review-diff`): 17 172 (−8 423); the catalog still had 79 entries — the core
  and Claude's legacy copies now listed under `~/.claude/skills/`.
- Invariants added to the stance (2026-09-27, `~/cursor-probe-1466`, sums):
  17 204 → 17 406 (+202), User Rules still on.
- Claude's legacy copies gone (2026-09-28, `~/cursor-probe-1482`): 17 067
  (−339); the catalog 79 → 44 entries, none `dart-*` or `flutter-*` (by the
  model's answer). So many fewer entries saving so little fits the fixed
  catalog budget (Paths) — not checked for that run.

## Probes

- Non-interactive: `agent -p "<prompt>"`; `--force` to run shell (bash is not
  in the allowlist); a new dir also needs `--trust`, git repos included.
- Traces: `~/.cursor/projects/<slug>/`, `~/.cursor/chats/<hash>/<session>/`;
  runs rewrite cache marks in `cli-config.json`. The session's `store.db`
  (SQLite, table `blobs`) holds the prompt as JSON text, skills catalog
  included.
- `/setup-terminal` in interactive `agent` — one-time terminal integration
  (Terminal.app: newline is Option+Enter; Ctrl+J always works).
