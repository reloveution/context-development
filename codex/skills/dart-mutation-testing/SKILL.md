---
name: dart-mutation-testing
description: Manual mutation testing for Dart/Flutter logic. Use when validating test quality for business logic changes. Enforces batch execution, per-test mutation loop, and immediate test strengthening on survived mutants.
---

# dart-mutation-testing

Manual mutation testing workflow for Dart/Flutter projects.

## Core Principle

A test is considered trustworthy only when it kills realistic mutants in the
covered production code.

## Required Execution Mode

- Work in batches (portions), not over the entire suite in one pass.
- Recommended batch size: 5-10 target tests per portion.
- Before each portion: run baseline tests for the portion scope.
- After each portion: run full project test suite.

## Per-Test Mutation Loop (strict)

1. Read target test and locate exact production code it covers.
2. Apply one focused mutant in production code.
3. Run only the target test file.
4. Interpret result:
   - `KILL` (test fails on mutant): revert mutant, move to next mutant/test.
   - `SURVIVED` (test still passes on mutant):
     - revert mutant,
     - immediately strengthen the test,
     - rerun target test,
     - confirm new assertion kills the same mutant.
5. Do not accumulate survived mutants for later; fix test quality immediately.

## Important Clarification

- If the test fails after mutation (`KILL`), this is expected and good. Do not
  strengthen for that mutant; just revert and continue.
- Strengthening is mandatory when mutant survives (`SURVIVED`).

## Mutation Patterns (examples)

- Nullify payload fields (`value -> null`).
- Drop required fields from `toJson()`.
- Drop payload keys from hash input.
- Change boundary operators (`>= -> >`, `<= -> <`).
- Replace targeted collection/index operations with wrong ones.

## Test Strengthening Patterns

- Add missing assertions for changed fields.
- Add golden hash assertions for canonical edge cases.
- Assert full payload/JSON shape, not only one field.
- Assert branch-specific behavior (op/lifecycle/state transitions).

## Reporting Format Per Portion

- Table: `# | test | mutant | result (KILL/SURVIVED) | action`.
- For each survived mutant: include exact test enhancement that fixed it.
- End each portion with full-suite status.
