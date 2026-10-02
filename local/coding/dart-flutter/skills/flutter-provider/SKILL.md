---
name: flutter-provider
description: Provider API for Flutter — Provider, ChangeNotifierProvider, watch, read, and select. Use when wiring or reading a Provider ancestor. Choosing Provider versus Bloc is flutter-state-management.
---

# Flutter Provider

`context.watch`, `context.read`, and `context.select` here look up a
`Provider` ancestor. The same names on a `BlocProvider` are `flutter-bloc`.

## Which provider

| Type | Use |
| --- | --- |
| `Provider` | Expose a value that does not notify |
| `ChangeNotifierProvider` | Create a `ChangeNotifier` and dispose it with the provider |
| `Provider.value` / `ChangeNotifierProvider.value` | Pass an instance owned elsewhere; `.value` does not dispose it |
| `FutureProvider` / `StreamProvider` | Expose the latest result of a future or stream |
| `ProxyProvider` / `ChangeNotifierProxyProvider` | Rebuild this value when an upstream provider changes |

Scope the provider to the narrowest subtree that reads it. Pass an explicit
type. Since provider 6.0, `watch<T>()` and `watch<T?>()` resolve to the same
deepest provider; the nullable form returns null when that provider is
absent instead of throwing.

`ValueListenableProvider`'s default constructor was removed in
5.0.0-nullsafety.0. `.value` came back in 5.0.0-nullsafety.1 and is still
there in 6.1.5. Release 6.1.5 did not change that class. A
`ValueListenableBuilder` remains the local way to read a `ValueNotifier`
without a provider.

## Where to read

| Call | Where |
| --- | --- |
| `context.watch<T>()` | `build`, rebuilds on notification |
| `context.select<T, R>(selector)` | `build`, rebuilds when the selector result changes |
| `context.read<T>()` | Callbacks and `didChangeDependencies`, no subscription |

Do not call these in `initState` or a constructor. The inherited lookup is
not available there yet.

## Boundaries

Choosing this over Bloc or `setState` is `flutter-state-management`.
Test doubles and where they are registered are `dart-mocktail` and
`dart-dependency-injection`. Pump the widget under the provider you mean;
`flutter-testing` owns the rest of the test.

## Sources

<https://pub.dev/packages/provider/changelog>: nullable lookup in 6.0.0;
`ValueListenableProvider.value` restored in 5.0.0-nullsafety.1. `select`
takes a selector: `context.select((Person p) => p.name)`.
