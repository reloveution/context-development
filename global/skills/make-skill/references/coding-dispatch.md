# Coding-skill dispatch

Read when creating or revising a skill that guides code with a possible
performance/readability trade-off.

## Contract

- Add a `Dispatch` section only when the skill owns a concrete trade-off. Its
  `normal` branch is the default: choose the smallest clear implementation
  that preserves behaviour and lets a reviewer follow control flow, data flow,
  names and invariants locally.
- A `critical-path` branch needs explicit frequency, volume or frame-budget
  evidence: a stated hot loop, a measured profile/benchmark, or a demonstrated
  heavy data/UI workload. A loop, a folder name or a scanner match is a lead,
  not proof that an optimisation belongs in the patch.
- The critical branch lists only this skill's subject-specific trade-offs and
  their proof: preserve semantics first, state the invariant, then measure or
  test the claimed improvement. Do not move its tactics into `simple-code`, a
  stance or an unrelated coding skill.
- A skill without a specific trade-off has no dispatch section. Do not invent a
  performance branch just for symmetry.

## Boundaries

- A stance may only point to the dispatch; it does not restate either branch.
  Project paths never select one.
- Default code does not inherit a critical-path representation or micro-
  optimisation. Conversely, readability preferences do not veto a proven,
  local critical-path change; the owner states why the added complexity pays.
- One rule has one owner: data access/batching stays with the data skill;
  rendering/rebuild work stays with the UI-performance skill; a type or
  collection micro-optimisation stays with the skill that proves its effect.

## Review

Name the evidence that selected `critical-path`, the behaviour preserved, the
measurement or focused test, and the added review cost. If any is absent, use
`normal` or report the candidate without editing it.

## Sources

- User decision, 2026-10-02: ordinary code optimises reviewability; critical
  loops, heavy data and heavy UI may use owner-specific performance tactics.
- [Flutter performance best practices](https://docs.flutter.dev/perf/best-practices):
  frequent `build()` work, large lazy lists and expensive rendering operations
  need targeted attention and DevTools evidence.
- [Google code-review guidance](https://google.github.io/eng-practices/review/):
  reviewers assess design, correctness, complexity, tests and readability.
