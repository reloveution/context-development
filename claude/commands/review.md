Run `git diff` against the last commit to see all current changes.

Apply skill `critical-thinking` as the meta-stance for the entire review: separate evidence from inference, force ≥2 hypotheses on every flagged issue (real bug vs. unfamiliar style? root cause vs. symptom?), pre-mortem the recommendations, resist sycophancy toward the diff author, calibrate confidence on each finding (verified vs. likely vs. assumption).

Apply skill `simple-code` as the cognitive-load and anti-overengineering lens: flag premature abstractions, compatibility shims, call-site type-switches that should be polymorphic, widened types, duplicated facts, silenced errors, and diff scope creep. Use the reviewer checklist from `simple-code` per file and per change set.

Apply the Big-O lens from skill `dart-code-review` (catalog/safety in `flutter-performance`). Optional first-pass scan: `python3 scripts/analyze_complexity.py . --format markdown`.

Perform a thorough code review of these changes following the Code Review Checklist from CLAUDE.md:

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
- SOLID principles followed
- No magic numbers, no `print`/`debugPrint`

If issues are found — list them with file paths, line numbers, and concrete suggestions for fixing.

After the review, provide a concise human-readable summary of all changes: what was changed, why (based on context), and what areas of the app are affected. Group changes by feature/module, not by file. Write the summary in the same language the user has been using in this conversation.
