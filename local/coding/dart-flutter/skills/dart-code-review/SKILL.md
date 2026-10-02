---
name: dart-code-review
description: Reviews Dart and Flutter changes for language-specific correctness, generated sources, tests, and performance leads. Use when reviewing Dart code or applying a Dart review lens to a diff.
---

# Dart Code Review

Review the changed human-written Dart code in its file and feature context. This
is the Dart-specific lens; `review-diff` owns the scope and summary of a current
repository diff.

## Check

- Compare public types, nullability, asynchronous behavior, errors, and resource
  ownership with their callers and the behavior the change promises. Do not infer
  correctness solely from a plausible diff.
- Treat a suppression or local deviation from `analysis_options.yaml` as a
  decision that needs a documented reason, not as a style preference.
- Do not manually edit generated files. When a source or schema change requires
  generation, check that the generated output is included and consistent.
- For changed behavior, ask whether a focused test would fail if that behavior
  regressed. Route test design to `flutter-testing` and mutation strength to
  `dart-mutation-testing`.
- Mark a performance candidate when a changed path adds nested traversal,
  repeated lookup or I/O in a loop, or collection work in `build()`. It is a
  lead, not proof: use `flutter-performance` to establish cost and safety before
  recommending an optimization.
- Route security-sensitive input, credentials, and network handling to
  `flutter-security`; do not reduce that review to a checklist item.

## Report

For an analyze, audit, scan, or report request, do not edit files. Report each
confirmed finding as `file:line` — current behavior, impact, and the missing
test or evidence. Label an unchecked suspicion as a lead and a non-blocking
style suggestion as `Nit`.
