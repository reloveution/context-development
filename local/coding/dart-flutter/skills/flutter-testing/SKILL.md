---
name: flutter-testing
description: Chooses and writes Flutter unit, widget, and integration tests. Use when deciding the test type, pumping a widget, or fixing a hanging pump or MissingPluginException. Mocktail is dart-mocktail; coverage is flutter-coverage-gate.
---

# Flutter testing

Use the cheapest test that can fail when the behavior changes. A pure
decision is a unit test. A widget contract is a widget test. A flow that
needs the real app binding is an integration test. Run the file or directory
that covers the change. The project stance owns whether a full suite is
allowed.

Assert the observable result. Do not assert a private method.

## Widget tests

Pump a `MaterialApp` when the widget needs a theme, direction, or
localization. After a tap, text entry, or drag, pump a frame. Use
`pumpAndSettle` only when every animation ends. A looping ticker makes
`pumpAndSettle` time out; pump frames instead.

## Platform channels

`MissingPluginException` means the test reached a platform channel. Mock that
channel for the test and clear the handler afterwards, or inject a fake so
the channel is never called. `flutter-drift` owns the in-memory database used
when the channel would have been `path_provider`.

## Integration tests

Call `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` before the
test. On a device or desktop, run that file with `flutter test`. A web
target still uses `flutter drive` with `test_driver/integration_test.dart`.
A project stance may prefix the command with its SDK runner.

## Boundaries

`dart-mocktail` owns mocks, fallbacks, and `when` / `verify`.
`flutter-coverage-gate` owns `flutter test --coverage` and gates.
`dart-mutation-testing` owns checking that a test can fail.
`flutter-bloc` owns `bloc_test`. `flutter-provider` owns pumping under a
provider.

## Sources

Widget binding and `pumpAndSettle`: <https://api.flutter.dev/flutter/flutter_test/WidgetTester-class.html>.
Channel mocks: <https://api.flutter.dev/flutter/flutter_test/TestDefaultBinaryMessenger/setMockMethodCallHandler.html>.
Integration binding: <https://api.flutter.dev/flutter/integration_test/IntegrationTestWidgetsFlutterBinding-class.html>.
