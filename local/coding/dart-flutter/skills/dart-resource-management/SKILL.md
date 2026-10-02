---
name: dart-resource-management
description: Owns Timer, StreamSubscription, StreamController, and Flutter State lifecycles. Use when a Dart resource needs cancellation or closing, a widget subscribes to a changing source, or cleanup is missing or unsafe.
---

# Dart Resource Management

An object that creates a resource owns its terminal path. Release it when that
object's lifetime ends; do not discard the only handle and assume garbage
collection will stop the work.

## Flutter State

- `State.dispose` is terminal. Release resources retained by the state there,
  then call `super.dispose()` last.
- For a source a widget subscribes to, subscribe in `initState`, replace that
  subscription in `didUpdateWidget` when the source changes, and unsubscribe
  in `dispose`.
- `dispose` is not an app-shutdown hook. Use an app-lifecycle owner when a
  resource must react to backgrounding or termination.

## Timers

- Use `Timer` rather than `Future.delayed` only when the delayed action may
  become irrelevant and needs cancellation.
- A debounced or replaced timer must cancel the previous timer before creating
  the next one, and cancel the final timer when its owner ends.

## Streams

- The owner of `stream.listen` retains its `StreamSubscription` and cancels it
  at the lifetime boundary. `cancel()` can perform asynchronous source cleanup;
  wait for it when the next operation depends on that cleanup.
- The owner of a `StreamController` closes it when it will emit no more events.
  Closing prevents further `add` calls and sends `done`; a paused listener can
  delay the returned `Future`, so do not make unrelated teardown wait on it.

## Boundaries

`flutter-networking` owns request and socket cancellation;
`flutter-animations` owns ticker and animation-controller disposal; database
lifecycle belongs to `dart-drift` or `flutter-drift`; `flutter-performance`
owns memory profiling and cache policy. `dart-error-handling` owns error-path
cleanup semantics.

## Sources

Dart API: <https://api.dart.dev/dart-async/StreamSubscription/cancel.html> and
<https://api.dart.dev/dart-async/StreamController/close.html>. Flutter API:
<https://api.flutter.dev/flutter/widgets/State/dispose.html>.
