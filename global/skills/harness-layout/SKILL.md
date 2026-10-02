---
name: harness-layout
description: Locates AI-harness config and safely changes shared skills, stances, hooks and symlinks. Use when adding, editing, moving or connecting them; asking where a harness reads them; or checking symlinks and explicit-only skills.
---

# harness-layout

## Architecture

**One source: `~/Work/context-development`** (public repo). Harness dirs and
projects hold **symlinks** into it, never copies.

| Layer | In the repo | Symlinked into |
|---|---|---|
| Core | `global/stance/`, `global/skills/<name>/`, `global/hooks/` | the global dirs of every harness |
| Package | `local/coding/<pkg>/skills/<name>/` — `dart-flutter`, `rust`, `common` | projects, one skill at a time, by the project's own list |
| Project | nothing: the project's own stance (`CLAUDE.md` / `AGENTS.md`) lives only in the project; its skills are symlinks from the repo, and a skill the project owns stays in it — `gogogo`, its own in every project | — |

- Core skills are `critical-thinking`, `recheck`, `decide`, `harness-layout`
  and `make-skill`; everything else is a package skill. Projects link only
  the package skills they need, never a whole package; migration removes old
  global package links at once.
- Cursor gets core skills from `~/.claude/skills/`. Do not alter another
  harness or isolate Cursor's `HOME` merely to hide duplicates from Cursor.
- Project stances hold only project facts and name the package skills needed;
  language rules stay in the package skill. `make-skill` owns that split.
  Do not put a `CLAUDE.md` or `AGENTS.md` (any case) inside this repo: Claude
  and Cursor may load it as nested instructions.
- `claude-stance.md` links to `~/.claude/CLAUDE.md`; `agents-stance.md` links
  to `~/.codex/AGENTS.md` and `~/AGENTS.md`. The latter is Cursor CLI's global
  stance and is outside the harness repos.
- The private harness repos hold settings, hooks, private skills and the
  tracked symlinks. Nothing personal goes into the public repo. Their current
  connections and tracking rules are in
  [references/harness-repos.md](references/harness-repos.md).
- A core hook is one tested script in `global/hooks/`; a package hook is in
  `local/coding/<pkg>/hooks/`. Each is symlinked into the harnesses, while its
  hook entry stays harness-local.
- A command is a skill the user calls by name; do not create `commands/*.md`
  or Cursor `.mdc` rules. Use explicit-only flags only after a demonstrated
  harm from implicit invocation; their harness-specific limits are below.
- The stances own global invariants. The hook enforces the git whitelist and
  the OS sandbox enforces the write boundary; an allow rule can bypass that
  boundary, so it is only for commands that cannot run inside it.
- Keep Codex-only config separate. A project links only needed skills because
  every listed description costs context; measurements are in the references.

Exact paths, limits, probe recipes and harness-specific exceptions are live
facts only where marked in these references:
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
4. In a shared project, keep symlinks into this repo in `.gitignore` and track
   skills it owns (`/.agents/skills/*`, then `!/.agents/skills/gogogo/`; a
   pattern with a trailing `/` skips a symlink, probe 2026-09-27). Its
   committed stance must work without the links.

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
