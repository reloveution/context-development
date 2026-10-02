---
name: review-diff
description: Reviews all changes since the last commit — critical-thinking, simple-code and Dart Big-O lenses plus a per-file checklist — then summarizes them by feature. Use when the user calls it by name or asks to review the current changes.
---

Run `git diff HEAD` and `git status` to see all changes since the last commit: staged, unstaged and untracked files.

Apply skill `critical-thinking` as the meta-stance for the entire review: separate evidence from inference, force ≥2 hypotheses on every flagged issue (real bug vs. unfamiliar style? root cause vs. symptom?), pre-mortem the recommendations, resist sycophancy toward the diff author, calibrate confidence on each finding (verified vs. likely vs. assumption).

Apply skill `simple-code` as the cognitive-load and anti-overengineering lens: flag premature abstractions, compatibility shims, call-site type-switches that should be polymorphic, widened types, duplicated facts, silenced errors, and diff scope creep.

Apply the Big-O lens from skill `dart-code-review` (catalog/safety in `flutter-performance`). Optional first-pass scan: the scanner from skill `flutter-performance`.

Perform a thorough code review of these changes following the checklist below:

**Per File:**
- Correct directory and naming conventions
- Clear single responsibility
- Readable names (variables, functions, classes)
- Correct logic, no missing edge cases
- Modular, no unnecessary duplication
- Errors/exceptions handled appropriately
- No security concerns
- No obvious performance issues
- Matches project style guide

**Overall:**
- Change set is focused and scoped
- Layer boundaries respected

If issues are found — list them with file paths, line numbers, and concrete suggestions for fixing.

After the review, provide a concise human-readable summary of all changes: what was changed, why (based on context), and what areas of the app are affected. Group changes by feature/module, not by file. Write the summary in the same language the user has been using in this conversation.
