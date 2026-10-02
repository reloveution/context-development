---
name: dart-mutation-testing
description: Manually checks whether focused Dart or Flutter tests detect a realistic behavior change. Use when verifying test strength, checking a surviving mutant, strengthening tests after coverage, or confirming a regression test would fail.
---

# Dart Mutation Testing

Mutation testing checks test strength, not coverage: make one realistic,
behavior-changing edit and confirm the focused test fails. A killed mutant is
evidence that the test detects that change; a surviving mutant needs a test
assertion or an explicitly documented equivalence reason.

## Scope

Use it for changed, human-written behavior with a focused covering test — for
example, a boundary condition, returned value, state transition, mapper, or
error path. It is most useful when high line coverage alone is insufficient
evidence of an observable assertion.

Do not mutate generated code, passive wiring, or a widget with no behavior
under test. `flutter-testing` owns test type, setup, and assertion design;
`flutter-coverage-gate` owns coverage policy and thresholds.

## Manual cycle

1. Select one behavior and the narrowest test that covers it.
2. Make one realistic, reversible mutation in `lib/`; do not combine changes.
3. Run the selected test and expect it to fail.
4. Revert the mutation, then confirm the same test passes.

If the mutation survives, first check that the selected test actually reaches
the changed behavior. Then strengthen an assertion for the observable result,
state, error, or collaborator contract and repeat the same cycle. Do not count
the survivor as an equivalent mutant without a specific semantic reason.

## Boundaries

Use `dart-mocktail` for Mocktail doubles and interaction matchers. Use
`dart-crap-metric` to prioritize complex, weakly tested functions, and report
mutation evidence to `dart-code-review` when reviewing changed behavior.
