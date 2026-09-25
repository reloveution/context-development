# Plugin Testing Reference

## Plugin Project Structure

```
my_plugin/
├── lib/                    # Dart code
├── android/src/test/       # Android unit tests
├── ios/                    # iOS native code
├── example/
│   ├── integration_test/   # Integration tests
│   └── ios/RunnerTests/    # iOS tests
├── test/                   # Dart unit tests
└── pubspec.yaml
```

## Error Simulation via Platform Channel

```dart
(MethodCall methodCall) async {
  if (methodCall.method == 'failingMethod') {
    throw PlatformException(code: 'ERROR', message: 'Native error');
  }
  return null;
}
```

## Native Test Commands

**Android:**
```bash
cd example/android
./gradlew testDebugUnitTest
```

**iOS:**
```bash
cd example/ios
xcodebuild test -workspace Runner.xcworkspace -scheme Runner -configuration Debug
```
