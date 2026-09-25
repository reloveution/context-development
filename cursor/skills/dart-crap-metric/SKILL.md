---
name: dart-crap-metric
description: CRAP metric (Change Risk Anti-Patterns) and cyclomatic complexity for Dart/Flutter. Use when the user asks to "lower CRAP", "find risky/dangerous code", "reduce complexity", "find fat functions", "complexity audit", or to prioritize refactoring and test-writing effort. Combines complexity and coverage to surface the most fragile functions.
---

# CRAP Metric for Dart/Flutter

CRAP (Change Risk Anti-Patterns) flags code that is both **complex** and
**poorly tested** — the riskiest combination during change.

Formula:

```
CRAP(m) = comp(m)^2 * (1 - cov(m))^3 + comp(m)
```

where `comp(m)` is cyclomatic complexity of method `m`, and `cov(m)` is
its test coverage in `[0, 1]`.

Interpretation:
- Fully covered code (`cov = 1`) → CRAP equals plain complexity.
- Untested complex code grows cubically in the coverage gap — the term
  dominates and pushes such code to the top of the refactoring queue.

**Project target: CRAP < 5 for `lib/` business logic.**

## When to apply

- User asks to lower CRAP, find dangerous code, or audit complexity.
- Before a large refactor: identify hot spots first.
- After a feature merge: confirm new code stays under the threshold.
- Pairs with `dart-mutation-testing` — first lower CRAP (split + cover),
  then verify the new tests are honest.

Skip on widgets/UI without logic, generated code, DI assembly.

## Tooling

- Cyclomatic complexity: `dart_code_metrics` (or
  `dart_code_metrics_presets` for the maintained fork).
  ```bash
  flutter pub add dev:dart_code_metrics_presets
  dart run dart_code_metrics:metrics analyze lib --reporter=json > metrics.json
  ```
- Coverage: `flutter test --coverage` produces `coverage/lcov.info`.
- Combine: a small Dart script reads both, computes CRAP per function,
  prints sorted top-N.

## Workflow

1. **Measure**:
   - Run tests with coverage: `flutter test --coverage`.
   - Run metrics: `dart run dart_code_metrics:metrics analyze lib`.
2. **Compute CRAP** per function from `metrics.json` + `lcov.info`.
3. **Sort descending**, take top-N (start with N = 10).
4. **For each hot spot**, choose the cheaper fix:
   - **Split** — if `comp ≥ 8`: extract guard clauses, lift each branch
     into a small private method, separate parsing from decision-making.
     Smaller pieces are trivially testable.
   - **Cover** — if `comp ≤ 7` but coverage is low: write tests for each
     branch and boundary. Use mutation testing afterwards
     (skill `dart-mutation-testing`) to prove the tests are real.
5. **Re-measure**, iterate until all functions in scope have CRAP < 5.

## Decomposition heuristics

Apply in order; stop when complexity drops under 10:

1. **Guard clauses**: invert `if`s and return early. Removes nesting,
   often halves complexity without a single new function.
2. **Extract validation**: lift input checks into a separate
   `Result<T>`-returning function or extension method.
3. **Polymorphism over switch**: replace large `switch`/`if-else` chains
   with sealed classes + pattern matching (skill `dart-3-patterns`) or
   strategy objects (skill `dart-design-principles`).
4. **Split parse vs. act**: a function that decodes input *and* mutates
   state is two functions in disguise.
5. **Pure helpers**: pull pure computations into `_` private functions or
   extensions (`X` suffix) — they get unit tests for free.

## Reporting

When presenting CRAP results to the user:
- Show top offenders with file:line, complexity, coverage, CRAP score.
- For each, recommend "split" or "cover" with one-sentence reasoning.
- Do not auto-refactor without confirmation — splits change call graph
  and may affect blocs/use-case wiring.

## Hard limits (mirrors CLAUDE.md)

- Function body ≤ 25 lines (excluding signature/closing brace).
- Cyclomatic complexity ≤ 10.
- CRAP < 5 for `lib/` business logic.
- Tests, generated code, DI assembly are exempt from limits but still
  benefit from low complexity for readability.

## CRAP vs Big-O

CRAP/cyclomatic = control-flow branching, not data flow. A function with `comp = 1, cov = 1.0` can still hide `O(n²)` or N+1. Big-O lives in `flutter-performance` and `dart-data-patterns`; scanner: `flutter-performance` (Dart-aware).

## Anti-patterns

- Lowering CRAP by deleting branches that "look unreachable" without
  proof. Add a test that asserts unreachability instead.
- Splitting one fat function into ten one-liners — readability tanks
  while CRAP looks fine. The goal is cohesion, not method count.
- Boosting coverage with assertion-free tests just to drop CRAP.
  Mutation testing will expose this; do it honestly the first time.
- Treating CRAP as a CI gate without manual review — outliers
  (state machines, parsers) sometimes legitimately exceed thresholds
  and need a documented exception.
