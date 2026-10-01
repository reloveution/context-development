---
name: flutter-bloc
description: BLoC/Cubit state management for Flutter — naming, state modeling, widgets, testing, architecture rules.
---

# Flutter Bloc

## Naming

- **Events**: past tense, `BlocSubject + noun + verb` — `LoginButtonPressed`, `UserProfileLoaded`
- **Initial load event**: `BlocSubjectStarted`
- **Base event class**: `BlocSubjectEvent`
- **States**: nouns (snapshot in time)
- **State subclasses**: `BlocSubject + Initial | Success | Failure | InProgress`
- **Single-class state**: `BlocSubjectState` + `BlocSubjectStatus` enum
- **Base state class**: `BlocSubjectState`

## State Modeling

- Extend `Equatable`; annotate `@immutable`; implement `copyWith`; use `const` constructors
- **Single class + status enum**: simple states, many shared properties
- **Sealed class + subclasses**: exclusive states, type safety, exhaustiveness (preferred)
- Shared properties in sealed base class; state-specific in subclasses
- Pass all relevant properties to `props`; copy `List`/`Map` with `List.of`/`Map.of`
- Emit a new state instance every time; never reuse same instance

## Cubit vs Bloc

| Cubit | Bloc |
|---|---|
| Simple state, no events, less boilerplate | Complex event-driven logic, traceability |
| Public methods return `void`/`Future<void>` | Trigger via `add()`; no custom public methods |

Start with Cubit; refactor to Bloc if needed.

## Core Rules

- Do **not** wrap `emit()` in try-catch
- Only `emit` inside Cubit/Bloc; never externally
- Duplicate states (`state == nextState`) are ignored
- Internal bloc events must be private (only for real-time repo updates)
- No Flutter imports in blocs, cubits, repositories
- Do not expose public fields on Bloc/Cubit; access state via getter
- Initialize `BlocObserver` in `main.dart`

## Flutter Widgets

| Widget | Purpose |
|---|---|
| `BlocBuilder` | Rebuild on state changes (builder must be pure) |
| `BlocListener` | Side effects only (navigation, dialogs) |
| `BlocConsumer` | Builder + listener combined |
| `BlocSelector` | Rebuild only on selected state slice |
| `BlocProvider` / `MultiBlocProvider` | Provide blocs to subtree |
| `RepositoryProvider` / `MultiRepositoryProvider` | Provide repos to subtree |

**Context access:**
- `context.read<T>()` — one-off, no rebuild (callbacks)
- `context.watch<T>()` — subscribe and rebuild (inside `build`)
- `context.select<T, R>()` — rebuild on specific slice

Prefer `BlocBuilder`/`BlocSelector` over `context.watch`/`context.select` for explicit scoping. Handle all states in UI: empty, loading, error, populated.

## Architecture

- Inject repositories/use cases into blocs via constructors
- No direct bloc-to-bloc communication — use `BlocListener` to listen to one and `add` events to another
- Shared data: inject same repository into multiple blocs

## Testing

```dart
blocTest<CounterCubit, CounterState>(
  'emits [1] when increment is called',
  build: () => CounterCubit(),
  act: (cubit) => cubit.increment(),
  expect: () => [const CounterState(1)],
);
```

- Test initial state first, then transitions
- Mock cubits/blocs in widget tests for all possible states
- `bloc_test` for state transitions; `bloc_lint` in CI

## Ecosystem

- **bloc_concurrency** — event transformers: sequential, concurrent, droppable, restartable
- **hydrated_bloc** — state persistence across sessions
- **replay_bloc** — undo/redo
- **bloc_lint** / **bloc_tools** — linting and CLI scaffolding
