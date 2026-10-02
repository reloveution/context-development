---
name: flutter-bloc
description: BLoC and Cubit with flutter_bloc — state shape, emit rules, provider widgets, context lookup, bloc_test, and official add-ons. Use when implementing or reviewing Bloc/Cubit logic and UI wiring, not when choosing Provider vs bloc for the whole app.
---

# Flutter Bloc

## Cubit vs Bloc

| Cubit | Bloc |
| --- | --- |
| State changes via public methods | State changes via `add`; no extra public methods on the Bloc class |
| No event types | Past-tense events for anything that already happened from the bloc's view |

Prefer Cubit until event traces, concurrency transformers, or a large event surface
justify a Bloc. Event and state naming follows
[bloclibrary.dev naming conventions](https://bloclibrary.dev/naming-conventions/)
(optional but documented for multi-developer projects).

## State modeling

- Emit a new state instance on each change; `emit` skips when the next state equals
  the current one.
- Use a sealed class hierarchy when phases are mutually exclusive; use one state
  class plus a status enum when most fields are shared across phases.
- When using `Equatable`, list every compared field in `props` and copy mutable
  collections with `List.of` / `Map.of`.

Immutable-state habits shared with other approaches live in
`flutter-state-management`; DTO and boundary conversion live in
`dart-data-patterns` and `dart-error-handling`.

## Cubit/Bloc invariants

- Call `emit` only inside the Cubit or Bloc. Do not wrap `emit` in `try/catch`;
  handle expected failures before emitting (for example after a `Result` from a
  repository) or surface unexpected errors with `addError` / `onError`.
- No `package:flutter` imports in bloc files (`bloc_lint` `avoid_flutter_imports`).
- No public fields on Cubit/Bloc (`bloc_lint` `avoid_public_fields`). Cubit
  methods return `void` or `Future<void>` (`prefer_void_public_cubit_methods`).
- On Bloc, handle work in `on<Event>` handlers; do not add public methods that
  bypass events (`avoid_public_bloc_methods`).

## Widget tree

| Widget | Role |
| --- | --- |
| `BlocProvider` / `MultiBlocProvider` | Create or provide a Cubit/Bloc for descendants |
| `RepositoryProvider` / `MultiRepositoryProvider` | Provide repositories to descendants |
| `BlocBuilder` | Rebuild when state changes (`buildWhen` optional) |
| `BlocSelector` | Rebuild only when a selected slice changes |
| `BlocListener` | Side effects (navigation, dialogs) — not layout |
| `BlocConsumer` | `BlocListener` + `BlocBuilder` when both are needed |

`BlocProvider` creates and closes the instance; `BlocProvider.value` only passes
an existing instance into a new subtree (for example a route) and does not close it.

## Context lookup

A Cubit/Bloc is visible only to **descendants** of the provider's `child`. The
`BuildContext` passed to `create`, or the same `build` that wraps
`BlocProvider`, is **above** the provider — `BlocProvider.of`, `context.read`,
and `context.watch` throw there. Read from the `child` subtree (use `Builder` when
the provider and consumer share one widget).

`flutter_bloc` exports `context.read`, `context.watch`, and `context.select`
(Provider-style extensions). Same names as **flutter-provider**, different
ancestor widgets (`BlocProvider` vs `Provider`).

| Situation | Mechanism |
| --- | --- |
| Callback or event handler, no rebuild | `context.read` |
| Rebuild on full state, with `buildWhen` | `BlocBuilder` |
| Rebuild on a derived slice | `BlocSelector` or `context.select` |
| Rebuild on full state, no `buildWhen` | `context.watch` or `BlocBuilder` |

When `bloc_lint` `prefer_build_context_extensions` is enabled, prefer
`context.watch` / `context.select` over `BlocBuilder` / `BlocSelector` if the
wrapper adds no `buildWhen` or selector logic beyond `select`.

Composition-root registration and test doubles belong to `dart-dependency-injection`.

## Coordinating blocs

Do not invoke one Cubit/Bloc from another. React in `BlocListener` (or similar)
and dispatch events, or share data through a repository injected into both.

## Testing

Use `bloc_test` for Cubit/Bloc transition sequences:

```dart
blocTest<CounterCubit, int>(
  'emits [1] when increment is called',
  build: () => CounterCubit(),
  act: (cubit) => cubit.increment(),
  expect: () => [1],
);
```

Assert the initial state, then each transition. Widget pumping, finders, and
general test design belong to `flutter-testing`; Mocktail mechanics belong to
`dart-mocktail`.

## Official add-ons

| Package | Purpose |
| --- | --- |
| `bloc_concurrency` | Event transformers: `sequential`, `concurrent`, `droppable`, `restartable` |
| `hydrated_bloc` | Persist and restore state across sessions |
| `replay_bloc` | Undo / redo over state history |
| `bloc_lint` | Analysis rules for bloc projects |
| `bloc_tools` | CLI (`bloc lint`, scaffolding) used with `bloc_lint` |

Register a `BlocObserver` at application startup when global bloc logging or
error reporting is required.

## Boundaries

- **flutter-state-management** — choosing and mixing approaches (Provider, built-in,
  local vs app state); not flutter_bloc API detail.
- **flutter-architecture** — layer and feature layout (deferred in this repo's
  plan); not resumed here.

## Sources

[bloclibrary.dev](https://bloclibrary.dev/) — Flutter bloc concepts, naming,
`bloc_lint` rules; `package:bloc` / `package:flutter_bloc` API docs on pub.dev.
