---
name: flutter-coverage-gate
description: Measures Flutter test coverage, layers exclusions and per-area gates when the project defines them, and ties coverage to mutation and CRAP. Use when raising coverage, setting a gate, or reporting what is covered — not for general test design.
---

# Flutter Coverage Gate

Line coverage counts execution, not assertion quality. It is useful only when the
project records **which paths matter**, **what to exclude**, and **numeric targets
per area** in its own CI script, config, or testing policy — not as a universal
bar.

A passing line-coverage gate alone is weak evidence — spot-check changed behavior
with `dart-mutation-testing`. Prioritize complex, weakly covered units with
`dart-crap-metric` when function-level complexity and coverage align on the same
callable; a file percentage alone is not CRAP.

## Measure

1. Run tests with coverage (default output path):
   ```bash
   flutter test --coverage
   ```
   Produces `coverage/lcov.info` (line hits). For branch data, the project's
   Flutter toolchain must support and enable branch collection (for example
   `flutter test --coverage --branch-coverage` when available); do not assume
   branch percentages unless that flag is part of the project's documented
   workflow.

2. Remove files the project deliberately excludes from the gate (typical
   candidates: `main.dart`, DI/bootstrap-only folders, `*.g.dart`,
   `*.freezed.dart`, generated localization). Example filter shape:
   ```bash
   lcov --remove coverage/lcov.info \
     'lib/main.dart' 'lib/di/**' '**/*.g.dart' '**/*.freezed.dart' \
     -o coverage/lcov.filtered.info
   ```
   Keep the exclude list versioned next to the project's thresholds.

3. Split the filtered report by **path prefixes that match this repo's layout**
   (for example `lib/features/**/domain/**`, `**/data/**`,
   `**/presentation/bloc/**`, `**/cubit/**`, widget/page folders). Prefixes
   and targets are project decisions — copy them from the checked-in gate script
   or policy, not from this skill.

4. Compare each area's line (and branch, if collected) percentage to that
   area's recorded target. On failure, report area, target, actual, gap, and the
   lowest-covered files in that area for prioritization.

5. When closing gaps, add tests in typical payoff order: pure domain → data →
   Cubit/Bloc → widgets. What to assert in each layer belongs to
   `flutter-testing`, `dart-data-patterns`, and `flutter-bloc`.

`flutter-testing` owns test types, pumping, and assertions; this skill owns
**coverage measurement and gate policy** once the project defines it.

## Layering rationale (not numeric defaults)

When defining targets, weight areas by test cost and signal:

| Area | Typical signal |
| --- | --- |
| Pure domain logic | High — cheap unit tests, few framework deps |
| Data / IO boundaries | Medium — more branches need fakes or integration tests |
| Cubit/Bloc | Medium — state sequences are testable (`flutter-bloc`) |
| Widgets / pages | Low for line % — favor behavior or golden tests over line padding |

Widgets are often **best-effort** or excluded from numeric gates; that choice
belongs in project policy.

## Anti-patterns

- Empty or assertion-free tests that only import files to raise percentages —
  mutation testing exposes this.
- Expanding the exclude list to pass a gate without updating documented policy.
- One long flow test that pads coverage instead of focused tests that localize
  failures.
- Treating line coverage as proof of correctness or as a substitute for CRAP or
  mutation checks on risky changes.
- Chasing widget line coverage while domain or state-machine gaps remain — the
  same effort usually buys more signal from domain tests and mutation checks.

## Enforcement

How the gate runs (local script, CI job, PR comment) is project-specific. The
skill does not prescribe hook names or paths until they exist in the repository
under review.

## Boundaries

- **dart-mutation-testing** — manual mutant cycle on focused behavior; not a
  coverage percentage.
- **dart-crap-metric** — function-level risk ranking when complexity and
  coverage map to the same unit; not a release gate by itself.
- **flutter-architecture** — folder layout conventions (deferred in this repo's
  plan); gate prefixes must follow the app on disk.

## Sources

Flutter `flutter test --coverage` and optional `--branch-coverage` /
`--coverage-path` (`package:flutter_tools` test command). LCOV filtering and
HTML reports via system `lcov` (for example
`genhtml coverage/lcov.filtered.info -o coverage/html`) or project tooling.
