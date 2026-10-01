# Tool Output Economy

This file is re-sent on every model call of every task. Keep it short.

Cost = number of model calls × context carried into each. The second multiplier
compounds: an untruncated output is re-sent on **every** later iteration of the
same task, not once.

- Truncate at the call site: `2>&1 | tail -3` for a green test run,
  `grep -A 14 '<test name>'` for a red one, `| head -40` for analyze. Full logs
  only when the summary is genuinely insufficient.
- Batch independent read-only calls into one turn — reads, greps, finds,
  `git status`/`diff`. N calls in one turn cost one model call; N turns cost N,
  each carrying everything before it. Batching within one turn only.
- Read the line range you need, not the whole file. Never re-read a file you
  just edited.
- Never run a full test suite unless the user explicitly asks. Run the file or
  the directory covering the change.

# Invariants

- Git: only `status`, `diff`, `log`, `show`, `blame`, `ls-files`, `ls-tree`,
  `check-ignore`, `rev-parse`, `mv`. Commits, pushes, resets, checkouts and
  every other git command belong to the user.
- No sub-agents, no background shells: their token spend is unobservable from
  the calling session. One test process at a time.
- Edit files with the file-edit tool, never through the shell (`sed -i`,
  heredoc, inline scripts): hooks and diff review see only that tool.
- Memory is off: never write to a harness memory store. Something worth
  keeping across sessions — propose it to the user in plain text.
- Replies: concise and direct, no filler, no emojis. Describe edits at a high
  level; no large code dumps in chat.

# Critical Thinking

Apply skill `critical-thinking` on every non-trivial task — design, debugging,
review, recommendations, claims about external systems; skip mechanical edits.
