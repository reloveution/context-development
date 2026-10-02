---
name: flutter-state-management
description: State management choices for Flutter. Use when comparing or combining approaches (local vs app state, Provider, built-in, BLoC/Cubit), not for flutter_bloc or Provider API detail.
---

# Flutter state management

Pick one update path per widget. An app may use more than one library; a
widget does not mix them for the same value.

| Situation | Owner |
| --- | --- |
| Ephemeral state of one widget | That widget's `State`, or a `ValueNotifier` beside it |
| A value several widgets read, with no event stream | `flutter-provider` |
| Feature state driven by events or async transitions | `flutter-bloc` |
| An existing `Future`, `Stream`, or `ValueNotifier` and no library was requested | `FutureBuilder`, `StreamBuilder`, or `ValueListenableBuilder` |

Do not put feature state in a global variable. `flutter-bloc` owns Cubit/Bloc
mechanics. `flutter-provider` owns Provider types and `context.watch` /
`read` / `select` on a Provider ancestor. Immutable updates and DTO mapping
belong to `dart-data-patterns`.
