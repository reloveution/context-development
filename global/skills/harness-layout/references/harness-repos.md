# Harness repos

`~/.claude`, `~/.codex`, `~/.cursor` are private git repos (branch `main`), one
per harness. They hold settings, hooks, private skills and the symlinks into
the public repo. Symlinks are committed: git stores only the target path, so
the history shows what was connected where, and a symlink replaced by a plain
file shows up as a typechange (`T`). Replacing a copied dir with a symlink is
one commit of the deletions and the symlink; the old copy stays in history.

## Current connections

| Harness | Stance | Core skills | Package skills | Hooks |
|---|---|---|---|---|
| Codex | symlink | symlinks | none globally; projects link them | `git_guard` symlink; retrust in `/hooks` after an entry edit |
| Claude Code | symlink | symlinks | none globally; projects link them | `git_guard`, `dart_format.sh` symlinks |
| Cursor CLI | `~/AGENTS.md` symlink; no rules | Claude's symlinks | none globally; projects link them | `git_guard`, `dart_format.sh` symlinks |

## `.gitignore` as a whitelist (Claude, Codex)

- `/*`, then `!/<name>` per tracked entry — not `*`, or nested content stays
  ignored. `!/.gitignore` is required. `.DS_Store` and `__pycache__/` are
  ignored at any depth.
- A new entry in the harness root stays untracked until its line is added.
- Not tracked: Claude — `skills/synced/` (claude.ai account skills),
  `settings.local.json` (one-off permissions), `plugins/`, `backups/` (copies
  of `~/.claude.json`); Codex — `skills/.system/` (Codex's own skills),
  `auth.json`.

## Cursor

- `~/.cursor/.gitignore` is a block managed by the CLI, and the CLI's ripgrep
  runs with `--no-require-git`: that file decides what the agent sees in
  `~/.cursor` (transcripts, terminals, MCP descriptors). Do not touch it.
- Hence `status.showUntrackedFiles no`: add new files by name (`git add -f` in
  the root and in `hooks/`), changes with `git add -u`. A pre-commit hook in
  `.git/hooks/` rejects added paths outside `cli-config.json`, `hooks.json`,
  `sandbox.json`, `mcp.json`, `hooks/`, `rules/`, `skills/`, `commands/`, and
  any `.DS_Store`.
- `cli-config.json` is tracked for `permissions`, though runs rewrite its cache
  marks and it holds the account email.

## Secrets

Never in git, never read whole by an agent: `~/.cursor/mcp.env`,
`~/.codex/auth.json`, `~/.claude.json` (query single fields with `jq`). A
secret lives in a local 0600 file; configs reference it by variable name.
