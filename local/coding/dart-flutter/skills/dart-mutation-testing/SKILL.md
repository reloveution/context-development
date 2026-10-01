---
name: dart-mutation-testing
description: Mutation testing for Dart/Flutter. Use when the user asks to "verify test quality", "strengthen tests", "make sure tests actually catch regressions", "mutation test", "kill mutants", or after raising line coverage to confirm tests are meaningful. Activates after `dart test`/`flutter test --coverage` to check that high coverage is not an illusion.
---

# Dart Mutation Testing

Line coverage proves code is **executed**, not that tests **catch regressions**.
Mutation testing changes production code in small, semantics-altering ways
(mutants). A good test suite "kills" the mutant — at least one test fails.
A surviving mutant means a test gap, even if coverage is 100%.

Use this skill to harden tests on critical business logic: domain layer,
use cases, repositories, mappers, validators, calculation-heavy code.

## When to apply

- User asks to verify or strengthen existing tests.
- After significant changes to domain/data layers.
- After a CRAP-metric pass (skill `dart-crap-metric`) lowered complexity
  and added tests — confirm those tests are meaningful.
- Before declaring a feature "fully covered".

Skip on UI widgets without logic, generated code, pure DTO `fromJson`/`toJson`,
and trivial wiring.

## Tooling

Package: [`mutation_test`](https://pub.dev/packages/mutation_test).

```bash
flutter pub add dev:mutation_test
dart run mutation_test --help
```

The package consumes an XML config and patches Dart sources in a sandbox.
It does **not** require Flutter widget bindings — works on pure Dart code
and Flutter business logic equally.

## Standard config

Place at project root: `mutation_test.xml`.

Key sections:
- `<files>` — globs for sources to mutate (typically `lib/features/**/domain/**/*.dart`
  and `lib/features/**/data/**/*.dart`).
- `<exclude>` — generated files (`*.g.dart`, `*.freezed.dart`), DI assembly,
  pure UI, asset bundles.
- `<commands>` — how to run tests: `flutter test` or `dart test` with a tight
  timeout per test invocation.
- `<rules>` — which mutation operators to apply.

Recommended operators (start narrow, expand later):
- arithmetic (`+` ↔ `-`, `*` ↔ `/`)
- comparison (`<` ↔ `<=`, `==` ↔ `!=`, `>` ↔ `>=`)
- boolean (`&&` ↔ `||`)
- conditional negation (replace condition with `true`/`false`)
- return-value mutation (replace return expression with default)
- null-aware: `?.` → `.`, `??` → ignore left side
- increment/decrement direction

Avoid mutating: logging calls, asserts, `// coverage:ignore` blocks.

## Workflow

1. **Baseline**: ensure `flutter test` is green and coverage is collected.
2. **Run**: `dart run mutation_test mutation_test.xml -o report.html`.
3. **Read report**: focus on **surviving mutants** grouped by file.
4. For each surviving mutant:
   - Read the diff the tool applied.
   - Decide: missing test, weak assertion, or equivalent mutant
     (semantically identical — rare; document and exclude in the rules).
   - Add or strengthen a test that fails on the mutant.
5. **Re-run** until mutation score ≥ target.

## Targets

- Domain entities and value objects: ≥ 90% mutation score.
- Use cases (`Usc` suffix): ≥ 85%.
- Repositories / datasources: ≥ 75% (some mutants on error paths
  may need integration tests).
- Mappers / serializers: 100% on round-trip cases.

## Common gaps surfaced by mutation testing

- Asserting only that a `Result` is `Ok`/`Err`, not its payload.
- Using `verify(() => mock.method(any()))` instead of pinning specific args.
- Missing boundary cases: empty list, single element, max size, null.
- Comparing only `length`/`isEmpty` instead of element identity.
- Ignoring sort order in collection assertions.
- Asserting "no exception" rather than the actual side effect.

## Combining with other skills

- After `dart-crap-metric` reduces a function's complexity, run mutation
  testing on the new smaller pieces — they are easier to fully cover.
- Before `dart-code-review`, mutation testing gives objective "tests are
  honest" evidence; the review then focuses on design, not coverage debate.
- Use `dart-mocktail` patterns for fakes that survive mutation runs
  (no over-stubbing).

## Anti-patterns

- Running mutation testing on the whole repo at once on every change —
  too slow. Scope to changed files via `<files>` glob.
- Tweaking tests to pass mutants without understanding the mutation —
  often masks a real bug.
- Excluding mutants instead of fixing tests "to keep the score green".
- Treating "equivalent mutant" as the default explanation — usually
  it is a real test gap.
