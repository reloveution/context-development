---
name: flutter-coverage-gate
description: Layered test-coverage thresholds for Flutter projects (domain/data/bloc/widgets) and how to enforce them. Use when the user asks to "raise coverage", "set a coverage gate", "what's covered and what's not", "coverage threshold", or wants to verify a feature is properly tested before merge.
---

# Flutter Coverage Gate

Coverage by itself is not a quality signal — but **layered targets** are
useful: they encode where tests bring value (pure logic) versus where
they bring noise (UI). This skill defines the thresholds and the workflow
to reach and verify them.

Always pair coverage with mutation testing
(skill `dart-mutation-testing`): a clean coverage gate without mutation
is theater.

## Targets per layer

| Layer | Path pattern | Line coverage | Branch coverage |
|---|---|---|---|
| Domain (entities, value objects, use cases) | `lib/features/**/domain/**` | ≥ 95% | ≥ 90% |
| Data (repositories, datasources, mappers) | `lib/features/**/data/**` | ≥ 80% | ≥ 70% |
| BLoC / Cubit | `lib/features/**/presentation/bloc/**`, `**/cubit/**` | ≥ 80% | ≥ 70% |
| Widgets / pages | `lib/features/**/presentation/widgets/**`, `**/pages/**` | best-effort | — |
| DI assembly, generated, `main.dart` | `lib/di/**`, `*.g.dart`, `*.freezed.dart`, `lib/main.dart` | excluded | excluded |

Rationale:
- Domain has no I/O, no framework — testing it is cheap and high-value.
- Data layer interacts with external systems; some error branches need
  integration tests rather than unit ones, hence lower bar.
- BLoCs are state machines — testing transitions is feasible and worthwhile.
- Widgets rarely benefit from line coverage; favor golden tests and
  widget tests for behavior, not lines.

## Workflow

1. **Run tests with coverage**:
   ```bash
   flutter test --coverage
   ```
   Output: `coverage/lcov.info`.

2. **Filter excluded files** before measuring (avoid `main.dart`,
   generated, DI):
   ```bash
   lcov --remove coverage/lcov.info \
     'lib/main.dart' \
     'lib/di/**' \
     '**/*.g.dart' \
     '**/*.freezed.dart' \
     -o coverage/lcov.cleaned.info
   ```

3. **Per-layer report**: split `lcov.cleaned.info` by path prefix and
   compute coverage per layer. A small Dart script in
   `tool/coverage_gate.dart` is the right home — checked in, runnable
   via `dart run tool/coverage_gate.dart`.

4. **Fail the gate** if any layer is below its threshold. Report:
   - layer, target, actual, gap;
   - top-5 lowest-covered files in that layer (for prioritization).

5. **Add tests** in priority order: domain → data → bloc → widgets.

6. **Verify honesty** with `dart-mutation-testing` on the changed files.

## What to test, by layer

### Domain
- Every public method of every use case (`Usc` suffix).
- Every non-trivial getter / computed property of entities.
- Every constructor validation path that returns a `Result.err`.
- Boundary cases: empty, single, max, min, zero, negative.

### Data
- Mappers in both directions (DTO → entity, entity → DTO), including
  null/optional fields.
- Repository: success path, each `Result.err` branch, cache fallback.
- Datasource: response parsing for success and failure shapes.
  Network errors covered by an injected fake `IHttpClient`.

### BLoC / Cubit
- Each event/method emits the expected sequence of states.
- Idempotency: emitting the same event twice is safe.
- Error states are emitted (not silently swallowed).
- Use `bloc_test` from `flutter-bloc` skill.

### Widgets
- Rendering with required props.
- Tap/long-press/scroll → callback invoked.
- Error state UI present when state is `error`.
- Skip pixel-level assertions unless the widget is a design-system
  primitive — use golden tests there.

## Anti-patterns

- Hitting the threshold by adding tests that import the file but
  do not assert anything meaningful. Mutation testing exposes this.
- Excluding inconvenient files from the lcov filter to "fix" the gate.
  Excluded files must match the table above; document any addition.
- One giant test that exercises an entire flow and pads coverage —
  prefer many small focused tests; failures point to the cause faster.
- Treating widget coverage as equally important as domain coverage.
  It is not. Time spent on widget line coverage usually yields less
  than the same time on domain mutation score.

## Enforcement options

- **Local pre-push**: `tool/coverage_gate.dart` invoked from a git
  pre-push hook (skill `update-config` for harness hooks).
- **CI**: same script invoked as a step; fails the build on gap.
- **Reporting**: emit a Markdown summary checked in to PR description
  (layer / target / actual table).
