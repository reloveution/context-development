---
name: dart-resource-management
description: Resource lifecycle and disposal for Dart/Flutter. Use when managing Timer, StreamController, subscriptions, animations, network cancellation, file/DB handles, native resources, or preventing memory leaks.
---

# Dart Resource Management

## Disposal Pattern

All resources must be cleaned up in `dispose()` (widgets) or `close()` (services/repositories). After cancelling or closing any resource, nullify the variable.

```dart
_subscription?.cancel();
_subscription = null;

_timer?.cancel();
_timer = null;

_streamController.close();

_animationController.dispose();
```

## Timer

- Use `Timer` instead of `Future.delayed` -- `Future.delayed` cannot be cancelled.
- Timer must be nullable.
- Cancel existing timer before creating a new instance (avoid duplicates).
- Cancel in `dispose()`; nullify after cancel.

## Subscriptions

- Cancel in `dispose()`; nullify after cancel.
- Example: `_subscription?.cancel(); _subscription = null;`

## StreamController

- Call `controller.close()` when the controller's owner is disposed or closed.
- Close in: `StatefulWidget.dispose()`, service/repository `close()` methods, or when the stream's lifetime scope ends.

## Animations and Tickers

- Call `controller.dispose()` in `dispose()`; never leave them running after widget removal.

## Network

- Cancel in-flight HTTP requests and WebSocket connections on widget disposal.
- Use `CancelToken` (dio) or equivalent.

## Pending Futures

- Check `mounted` before `setState` or context usage after async gaps.
- Avoid completing work for disposed widgets.

## Files and Database

- Close `IOSink`, `RandomAccessFile`, and other file streams; use try-finally for cleanup on error paths.
- Close database connections when no longer needed; don't hold connections across lifecycle boundaries.

## Native Resources

- Release cameras, sensors, etc. when no longer needed.
- Call platform-specific release/dispose methods.
- Don't hold native resources across widget disposal or app backgrounding.

## Scoping

- Scope resources to the widget or object that owns them.
- Don't store widget-scoped resources in global or long-lived objects.

## App Lifecycle

- Use `WidgetsBindingObserver` for app-level lifecycle.
- **pause** -- release heavy resources (cameras, large caches) when app goes to background.
- **resume** -- reacquire if needed.

## Memory

- Ensure disposed objects are not retained by closures or references.
- Set image cache eviction policies; don't hold unlimited image data.
- Profile with DevTools to identify leaks.
