---
name: flutter-testing
description: Flutter testing guidance covering unit tests, widget tests, integration tests, mocktail mocking, and plugin testing. Use when writing tests, mocking dependencies, debugging test errors, or running tests.
---

# Flutter Testing

## Test Types

| | Unit | Widget | Integration |
|---|---|---|---|
| Confidence | Low | Higher | Highest |
| Speed | Fast | Fast | Slow |
| Dependencies | Few | More | Most |

Many unit + widget tests for coverage, enough integration tests for critical flows.

## Mocktail (Project Standard)

Project uses **Mocktail**, NOT Mockito.

- `Fake` for asserting outcomes; `Mock` for verifying interactions
- Extend `Mock`, no manual overrides in subclass
- `registerFallbackValue` for every non-nullable custom type before stubbing
- Sync: `when(() => mock.method()).thenReturn(value)`
- Async: `when(() => mock.method()).thenAnswer((_) async => result)`
- Failure: `when(() => mock.method()).thenThrow(error)`
- Verify: `verify(() => ...)`, `verifyNever(() => ...)`, `.called(n)`
- Supply all named params; `any(named: 'param')` when value irrelevant
- Stub every dependency method expected in test — avoid MissingStub
- Prefer real collaborators or fakes when asserting outcomes

```dart
class MockRepo extends Mock implements IRepository {}

void main() {
  late MockRepo mockRepo;
  setUpAll(() => registerFallbackValue(SomeType()));
  setUp(() => mockRepo = MockRepo());

  test('should fetch data', () async {
    when(() => mockRepo.getData()).thenAnswer((_) async => Result.success(data));
    final result = await useCase.execute();
    verify(() => mockRepo.getData()).called(1);
  });
}
```

## Unit Tests

- `package:test/test.dart`, Arrange-Act-Assert pattern
- `group('ClassName', () { ... })` — wrap every suite
- Name tests: "should ..." phrasing
- Test behavior (output/state), not implementation (private methods)
- `package:checks` for assertions

For matchers, exception testing, streams, fake clock: [unit-testing.md](references/unit-testing.md)

## Widget Tests

- Wrap in `MaterialApp(home: ...)` when widget requires theme/navigation context

**Finders:**

| Finder | Usage |
|---|---|
| `find.text('Hello')` | By exact text |
| `find.textContaining('ello')` | By partial text |
| `find.byType(ElevatedButton)` | By widget type |
| `find.byKey(ValueKey('id'))` | By key |
| `find.byIcon(Icons.add)` | By icon |
| `find.ancestor(of: ..., matching: ...)` | By ancestor |

**Matchers:** `findsOneWidget`, `findsNothing`, `findsWidgets`, `findsNWidgets(n)`

**Interactions:**
```dart
await tester.tap(finder);
await tester.drag(finder, Offset(0, -300));
await tester.enterText(finder, 'text');
await tester.fling(finder, Offset(0, -500), 10000);
await tester.longPress(finder);
await tester.scrollUntilVisible(finder, 500.0);
await tester.pump();           // single frame
await tester.pumpAndSettle();  // all animations complete
```

For orientation, forms, accessibility, animations: [widget-testing.md](references/widget-testing.md)

## Integration Tests

Setup: `integration_test` SDK dependency + test driver.

```dart
IntegrationTestWidgetsFlutterBinding.ensureInitialized();
testWidgets('user flow', (tester) async {
  await tester.pumpWidget(const MyApp());
  // interact and verify
});
```

For performance profiling, CI/CD config: [integration-testing.md](references/integration-testing.md)

## Platform Channel Mocking

```dart
setUp(() {
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
      .setMockMethodCallHandler(
    const MethodChannel('your.plugin.channel'),
    (MethodCall methodCall) async {
      if (methodCall.method == 'getVersion') return '1.0';
      return null;
    },
  );
});
tearDown(() {
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
      .setMockMethodCallHandler(
    const MethodChannel('your.plugin.channel'), null,
  );
});
```

For plugin project testing: [plugin-testing.md](references/plugin-testing.md)

## Common Test Errors

- **MissingPluginException** — mock the method channel (see above)
- **TimeoutException / pumpAndSettle hangs** — use `pump()` if animation loops; increase timeout for long ops
- **Widget not found** — call `pumpAndSettle()` for async; verify correct finder type/text
- **No MaterialApp** — wrap widget in `MaterialApp(home: ...)` in test

## CLI

```bash
flutter test                           # all tests
flutter test test/my_test.dart         # specific file
flutter test --name "should fetch"     # specific test
flutter test integration_test/         # integration
flutter test --coverage                # with coverage
```
