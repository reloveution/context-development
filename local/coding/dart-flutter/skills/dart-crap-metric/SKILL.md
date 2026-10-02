---
name: dart-crap-metric
description: Prioritizes risky Dart functions with CRAP when matching function-level complexity and coverage exist. Use when auditing CRAP or prioritizing complexity and test work.
---

# CRAP Metric

CRAP ranks functions that combine complex control flow with weak test coverage:

```
CRAP(m) = comp(m)^2 * (1 - cov(m))^3 + comp(m)
```

`comp(m)` is cyclomatic complexity and `cov(m)` is coverage for the same
function in `[0, 1]`. Fully covered code scores its plain complexity. A high
score is a review priority, not a defect or a release gate.

## Preconditions

Compute CRAP only when both inputs identify the same callable unit:

- the complexity report names functions or methods and their cyclomatic score;
- the coverage report maps executed and missed code to those same functions;
- generated code, UI without logic, and DI assembly are excluded deliberately.

Line coverage alone, a file-level percentage, or a heuristic scanner cannot
produce a reliable function CRAP score. Such tools may identify a lead, but the
report must say that CRAP was not computed.

## Use the ranking

1. Sort the measured functions by CRAP and inspect the highest results in their
   callers and tests.
2. Decide whether the risk is primarily untested behavior, unclear control flow,
   or both. Add focused tests before changing behavior; use
   `dart-mutation-testing` when test strength matters.
3. Simplify only a real responsibility or control-flow problem. Do not split a
   cohesive function, delete a branch, or add an abstraction merely to lower a
   score; use `simple-code` for that decision.
4. Re-measure the same units and explain any score change.

`flutter-coverage-gate` owns coverage policy and thresholds. `flutter-performance`
owns data-flow cost, including Big-O and N+1; cyclomatic complexity does not
measure either.

## Report

For each measured candidate, report `file:line`, complexity, coverage, CRAP,
the behavior at risk, and the chosen next step. Distinguish measured scores from
heuristic leads. Do not auto-refactor or claim that a score proves a bug.
