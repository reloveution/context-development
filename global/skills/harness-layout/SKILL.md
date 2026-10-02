---
name: harness-layout
description: Where AI-harness config lives and how to change it safely — one public repo (~/Work/context-development) is the single source, symlinked into Claude Code, Codex, Cursor CLI and projects. Use when adding, editing, moving or connecting a skill, stance (CLAUDE.md, AGENTS.md), rule or hook; when making a command — a skill the user calls by name — that works across harnesses, or weighing user-only flags (disable-model-invocation, allow_implicit_invocation); when asked where a harness reads its config from; or when checking symlinks.
---

# harness-layout

Solo user, mostly Dart/Flutter. Harnesses: Claude Code, Codex (to be dropped
later), Cursor CLI.

## Architecture

**One source: `~/Work/context-development`** (public repo). Harness dirs and
projects hold **symlinks** into it, never copies.

| Layer | In the repo | Symlinked into |
|---|---|---|
| Core | `global/stance/`, `global/skills/<name>/`, `global/hooks/` | the global dirs of every harness |
| Package | `local/coding/<pkg>/skills/<name>/` — `dart-flutter`, `rust`, `common` | projects, one skill at a time, by the project's own list |
| Project | nothing: the project's own stance (`CLAUDE.md` / `AGENTS.md`) lives only in the project; its skills are symlinks from the repo, and a skill the project owns stays in it — `gogogo`, its own in every project | — |

- Core skills: `critical-thinking`, `recheck`, `decide`, `harness-layout`.
  Everything else is a package skill; a project links only the skills it
  needs, never a whole package, once work in it starts. No transition period:
  a harness switched to the repo drops package skills from its global dir at
  once.
- Cursor gets the core skills from `~/.claude/skills/`: its CLI always reads
  Claude's and Codex's skill dirs, so `~/.cursor/skills/` holds no core. Other
  harnesses are never changed just to hide something from Cursor, nor is it
  run in an isolated `HOME`; duplicates in its catalog are tolerated (user
  decision 2026-09-27).
- A project's own `CLAUDE.md` / `AGENTS.md` holds only project-specific bits
  — naming suffixes, scanner paths, project commands, token limits — and
  names the package skills its work needs. A language's rules live in those
  skills, never in a block each project imports or copies: Claude loads an
  `@` import from outside the project only after a per-project approval, and
  Codex has no import (references). What goes where — `make-skill`.
- No file in the repo is named `CLAUDE.md` or `AGENTS.md`, in any letter
  case: the disk is case-insensitive APFS, and Claude and Cursor load nested
  ones (Codex unverified). Claude loaded `references/claude.md` and a
  `CLAUDE.md` symlink in a skill dir on reading a file in their dir
  (2026-09-27). Hence the stance
  names: `global/stance/claude-stance.md` → `~/.claude/CLAUDE.md`,
  `global/stance/agents-stance.md` → `~/.codex/AGENTS.md` and `~/AGENTS.md`
  (Cursor; pi by docs). `~/AGENTS.md` lies outside every repo — no harness
  repo records it — yet it is the only file Cursor CLI takes as a global
  stance: `~/.cursor/rules/` and `~/.cursor/AGENTS.md` are not read (probes
  2026-09-29). Codex started in `~` itself would read it on top of
  `~/.codex/AGENTS.md` (unverified).
- `~/.claude`, `~/.codex`, `~/.cursor` are private git repos — the harness
  repos. They hold settings, hooks, private skills and the symlinks
  themselves: a committed symlink records what is connected where. Nothing
  personal goes into the public repo. See
  [references/harness-repos.md](references/harness-repos.md).
- Exception: a hook script that holds a core invariant is one copy in
  `global/hooks/` (its test beside it), symlinked into each harness's
  `hooks/`; the hook entry that runs it stays in the harness repo.
- A package's hook script lives in `local/coding/<pkg>/hooks/`, its test
  beside it. Hooks have no per-project connection, so it is symlinked into
  each harness's `hooks/` the same way and acts only on its own files
  (`dart_format.sh`: `.dart` only).
- A command is an ordinary skill the user calls by name (`/name`, `$name`) —
  all three harnesses fold commands into skills (docs); its description ends
  with "use when the user calls it by name or asks
  to …". The text after the name arrives as is — no placeholders. No
  `commands/*.md`, no Cursor `.mdc` rules. Its name avoids every harness's
  built-in commands: `review` is a Claude alias of `/code-review` and a Codex
  command (docs), hence `review-diff`.
- User-only flags (`disable-model-invocation: true`; for Codex
  `agents/openai.yaml` with `policy.allow_implicit_invocation: false`) only
  when self-invocation does harm — none now. They save a catalog entry but
  break explicit calls: Claude drops the skill from the model's list, Cursor
  never injects one symlinked into a project (see the references).
- Core invariants — git limited to the whitelist of
  `global/hooks/git_guard.py`; no sub-agents or background shells; one test
  process at a time; edits only through the file-edit tool; memory off; reply
  style — live in the stances: `claude-stance.md` (plus the artifact ban),
  `agents-stance.md` for Codex, Cursor and pi. The git whitelist is also
  enforced by that script as a hook in all three harnesses; it stops habitual
  forms and retries after a block, while only the sandbox stops a deliberate
  bypass, so git flags stay allowed (decision 2026-09-28). Codex
  `developer_instructions` hold only hints for its own tools.
- Write boundary: every harness runs shell commands in its OS sandbox —
  writes only in the project, the temp dir and named caches (`~/fvm`,
  `~/.pub-cache`); leaving it asks the user. An allow rule takes a command
  out of the sandbox with no prompt (Codex, Cursor), so the rules hold only
  what cannot run inside: `pkill -f frontend_server_aot`. Web search and
  page reads never ask. Keys and probes — in the references.
- Codex-only files (`agents/openai.yaml`) stay separate, so Codex can be
  dropped in one step.
- A skill is a short `SKILL.md` plus `references/` read on demand; scripts live
  inside the skill dir and are referenced relative to it — such a script runs
  in all three harnesses (probe 2026-09-25).
- Every listed skill's description rides in every model call. Claude and
  Codex list descriptions whole; Cursor fits its catalog into ≈ 20k chars and
  caps every description at one length that falls as entries grow — 480
  chars at 42 entries, 125 at 77 (2026-10-02). In a Flutter project with 35
  package skills linked, its 40 entries — core and its own skill included —
  take 10.6k chars of every Claude call and 12.2k of every Codex call (≈ 2.7k
  and 3k tokens). Hence a project links only the skills it needs; numbers and
  probes — in the references.
- Skill text and the shared stance `agents-stance.md` are harness-neutral,
  since several harnesses read the same file: an action, not a tool name ("search the web", not `WebSearch`);
  no harness paths, invocation syntax (`/name`, `$name`), placeholders
  (`$ARGUMENTS`, `${CLAUDE_SKILL_DIR}`) or harness built-in skills; MCP tools
  as `server:tool`. A hint for one harness's own tools goes to that harness's
  config. Exceptions: this skill, and vendored upstream text.

## Current state (2026-10-02 — update on every migration)

| Harness | Stance | Core skills | Package skills | Hooks |
|---|---|---|---|---|
| Codex | symlink | symlinks | none globally; projects link them | `git_guard` symlink; trusted in `/hooks` — again after any edit of its entry |
| Claude Code | symlink | symlinks | none globally; projects link them | `git_guard`, `dart_format.sh` symlinks |
| Cursor CLI | symlink `~/AGENTS.md`; no rules; account User Rules until cleared | Claude's symlinks | none globally; projects link them | `git_guard`, `dart_format.sh` symlinks |

## Where each harness reads config

| | Global skills | Global stance | Project skills | Project stance | Invoke |
|---|---|---|---|---|---|
| Claude Code | `~/.claude/skills/` | `~/.claude/CLAUDE.md` | `.claude/skills/` | `CLAUDE.md`; `AGENTS.md` only with no `CLAUDE.md` | `/name` |
| Codex | `~/.codex/skills/`, `~/.agents/skills/` | `~/.codex/AGENTS.md` | `.agents/skills/` | `AGENTS.md`, git root → cwd | `$name` |
| Cursor CLI | `~/.cursor/skills/`, plus `~/.claude/skills/`, `~/.codex/skills/` | `~/AGENTS.md` only, plus account User Rules | `.cursor/skills/`, `.agents/skills/`, plus `.claude/`, `.codex/` | `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/` in every dir up to `/` | `/name` |

Verified live unless the harness reference marks a path as docs or bundle.
Details, quirks and probe recipes per harness:
[references/claude-code.md](references/claude-code.md),
[references/codex.md](references/codex.md),
[references/cursor.md](references/cursor.md).

## Connect

1. Put the file in the repo: a core skill in `global/skills/<name>/`, a package
   skill in `local/coding/<pkg>/skills/<name>/`. Moving existing config in
   starts with a verbatim copy; changes go on top of it as diffs, and the
   harness's own copy is not edited until a symlink replaces it.
2. Symlink with absolute paths, one symlink per skill dir:

   ```bash
   ln -s ~/Work/context-development/global/skills/<name> ~/.codex/skills/<name>
   ln -s ~/Work/context-development/local/coding/dart-flutter/skills/<name> \
     <project>/.agents/skills/<name>
   ```

   Project dirs: `.agents/skills/` for Codex and Cursor, `.claude/skills/` for
   Claude. Exception: when both ends are in one repo — a skill of the repo
   itself (`gogogo`) in `.agents/skills/<name>`, linked from
   `.claude/skills/<name>` — the link is relative
   (`../../.agents/skills/<name>`), so it survives a clone to another path.
   Claude loads the skill through that link, Codex and Cursor straight from
   `.agents/skills/` (probe 2026-09-27).
3. Check: `find -L <dir> -type l` must print nothing — a broken symlink
   silently disables the skill.
4. Commit the symlink in the harness repo. In a project follow its own rule:
   a project whose remote is shared with others keeps its symlinks into this
   repo in `.gitignore` and tracks the skills it owns (`/.agents/skills/*`,
   then `!/.agents/skills/gogogo/`; a pattern with a trailing `/` skips a
   symlink, probe 2026-09-27), and its committed stance must work without
   them.

Connecting is manual for now; a script is planned.

## Edit

- Edit the file in the repo, never through a symlink path. Atomic saves (temp
  file + rename) replace a symlink with a plain file and silently fork the
  config: resolve with `readlink` and edit the target. A forked symlink shows
  as a typechange (`T`) in the harness repo's `git status`.
- Never `cp -R` into a harness `skills/` dir: through a symlink it overwrites
  the repo copy.
- On macOS `rm -r <symlink>/` (trailing slash) deletes the target — a skill in
  the repo; `ln -s <src> <symlink to a dir>` creates the link inside the
  target. Remove a symlink by its bare path; create one with `ln -sn`, which
  fails on an existing name (probe 2026-09-28).
- A symlinked skill is seen by its symlink path, except Codex on an explicit
  `$name`: it injects the body with the real path (probe 2026-09-27). So `../`
  from a skill dir lands in different places — a skill never references files
  outside its own dir. For another skill's script it names that skill, which
  holds the path (probe 2026-09-27: `dart-code-review` → `flutter-performance`
  in all three).
- Skills name other skills, never their paths, and only down the layers: a
  package skill may name core, `common` and its own package; core and `common`
  never name a package skill — a project of another language lacks it.
- Frontmatter must parse as strict YAML: a plain `description` never holds
  `: `. Claude and Codex forgive it; Cursor lists the skill with an empty
  description (probe 2026-09-28). Write `Topic — list`, like the other skills.
- Vendored skill `rust-skills` (upstream `leonardomso/rust-skills`, MIT, its
  `LICENSE` inside): update by cloning upstream into a scratch dir and copying
  its contents over the repo copy without `.git`, then delete its `AGENTS.md`
  and `CLAUDE.md` — symlinks to `SKILL.md` that harnesses load as nested
  instructions. Upstream text stays verbatim, harness-specific bits included.
  On macOS `cp -R src/ dst/` copies the contents, `cp -R src dst/` the folder.
- A claim about harness behavior is a fact only after a live run (probe recipes
  in the references); docs and bundle code are hypotheses until then.

## Memory policy (hard rule)

Memory is off in every harness — the Claude Code memory store, Cursor tracking,
Codex `features.memories` (default `false`, keep it). When something seems
worth keeping across sessions:

1. Do not write it to any memory store.
2. Propose it to the user in plain text — what, and why it is durable.
3. Only on explicit approval, put it into the repo: a cross-cutting behavior →
   the stance in `global/stance/` (`agents-stance.md` only if it earns its
   per-call cost, otherwise a skill); a reusable procedure → a skill in
   `global/skills/` or `local/coding/<pkg>/skills/`; a project fact → that
   project's `CLAUDE.md` / `AGENTS.md`.
