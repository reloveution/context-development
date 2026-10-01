---
name: flutter-provider
description: Provider state management for Flutter. Use when exposing values with Provider, ChangeNotifierProvider, FutureProvider, StreamProvider, scoping with context.watch/read/select, ProxyProvider, or testing provider-based state.
---

# Flutter Provider

## Provider Types
- **Provider** — exposes a value (no change notification)
- **ChangeNotifierProvider** — auto-disposes notifier when removed from tree
- **FutureProvider** — exposes Future result
- **StreamProvider** — exposes Stream values
- **ProxyProvider** — depends on other providers; refreshes when upstream changes
- **Provider.value** — for existing instances managed elsewhere

Scope each provider to the narrowest subtree that consumes it.

## Accessing State

| Method | Where | Purpose |
|---|---|---|
| `context.watch<T>()` | `build()` | Subscribe and rebuild on change |
| `context.read<T>()` | Callbacks, event handlers | One-off access, no subscription |
| `context.select<T, R>()` | `build()` | Subscribe to specific state slice |

- Always specify generic type: `Provider<MyType>`, `context.watch<MyType>()`
- Place `Consumer`/`Selector` as deep in the tree as practical
- Outside `build`: access only at `didChangeDependencies` or in callbacks — not in constructors or `initState`

## Lifecycle
- Use `create`/`update` callbacks — don't instantiate from external mutable variables
- `ChangeNotifierProxyProvider` when notifier depends on other providers
- `MultiProvider` to avoid nested declarations; for very large apps consider incremental mounting during splash

## Diagnostics
- Add `DiagnosticableTreeMixin` to provided objects for DevTools readability

## Migration
- `ValueListenableProvider` is deprecated — use `ValueListenableBuilder` + `Provider.value`

## Testing
- Shallow provider wiring per test; override providers to inject mock/fake dependencies
- Scope to what each test needs, keep setup minimal
