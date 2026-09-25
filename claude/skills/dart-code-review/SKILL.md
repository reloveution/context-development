---
name: dart-code-review
description: Code review checklist for PRs/MRs. Use when reviewing pull requests, examining code changes, or when the user asks for a code review.
---

# Code Review

## Mindset

- No assumptions — investigate implementation details before judging correctness
- Be objective; devil's advocate approach, not automatic praise
- Fetch documentation when unsure about package best practices
- If a change remains unclear after investigation, flag it in the report

## Pre-Review

- Branch is feature/bugfix — not main/develop
- Branch is up-to-date with target (main)
- List all changed/added/deleted files
- For every change: review commit title and connected components

## Per File

- Correct directory and naming conventions
- Clear single responsibility; reason for change is understandable
- Readable names; correct logic; no missing edge cases
- Modular, no unnecessary duplication
- Errors/exceptions handled; no security concerns (input validation, no secrets)
- No obvious performance issues
- Public APIs and complex logic documented
- Sufficient test coverage for new/changed logic
- Matches project style guide
- Generated files up-to-date and not manually edited

## PR-Level

- Change set focused and scoped to stated purpose
- PR description accurately reflects changes
- Tests cover new/changed logic; evaluate if tests can actually fail (not just mock checks)
- CI passes

## Big-O Lens

Diff scan: nested loops · `.contains`/`.indexOf`/`.firstWhere` in loop · sort-in-loop · repo/HTTP/Drift call in loop (N+1) · `.where()`/`.map()`/`.sort()` in `build()`.

Safety before proposing fix (full list in `flutter-performance`): size matters · ordering preserved · cache invalidation valid · batching preserves auth/tenant/order/page.

On "analyze/audit/scan/report" — produce report, no file edits unless implement requested. Format: scope · findings (`file:line`, current pattern, complexity before→after, risk, tests) · `files modified: yes/no`.

Scanner: `python3 ~/.claude/skills/flutter-performance/scripts/analyze_complexity.py . --format markdown` — Dart-aware; leads, not proof.

## Output

Conclusions and recommendations per file. Constructive feedback with suggestions.
