# Integration Testing Reference

## Setup

```yaml
# pubspec.yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter
```

Test driver `test_driver/integration_test.dart`:
```dart
import 'package:integration_test/integration_test_driver.dart';
Future<void> main() => integrationDriver();
```

## Performance Profiling

```dart
testWidgets('scrolling performance', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  final timeline = await tester.trace(() async {
    await tester.fling(find.byType(ListView), const Offset(0, -1000), 5000);
    await tester.pumpAndSettle();
  });

  final avg = timeline.frames
      .map((f) => f.duration)
      .reduce((a, b) => a + b) ~/
      timeline.frames.length;
  expect(avg.inMilliseconds, lessThan(17)); // 60fps
});
```

## Build Count Tracking

```dart
int buildCount = 0;
await tester.pumpWidget(MaterialApp(home: Builder(
  builder: (context) {
    buildCount++;
    return const MyWidget();
  },
)));
expect(buildCount, 1);

await tester.tap(find.byType(ElevatedButton));
await tester.pumpAndSettle();
expect(buildCount, 1); // should not rebuild
```

## Running

```bash
flutter test integration_test/
flutter test -d <device-id> integration_test/
flutter drive --target=integration_test/my_test.dart
```

## GitHub Actions CI

```yaml
name: Integration Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test integration_test/
```
