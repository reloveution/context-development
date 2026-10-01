# Unit Testing Reference

## Matchers

```dart
// Equality
expect(actual, equals(expected));
expect(actual, isNot(equals(expected)));

// Null
expect(value, isNull);
expect(value, isNotNull);

// Numeric
expect(5, greaterThan(3));
expect(5, lessThan(10));
expect(5, greaterThanOrEqualTo(5));

// Type
expect(obj, isA<String>());

// String
expect(text, contains('sub'));
expect(text, startsWith('pre'));
expect(text, endsWith('suf'));
expect(text, matches(RegExp(r'\d+')));

// Collections
expect(list, isEmpty);
expect(list, isNotEmpty);
expect(list, hasLength(3));
expect(list, contains(item));
expect(list, orderedEquals([1, 2, 3]));
```

## Exception Testing

```dart
expect(() => calculator.divide(10, 0), throwsArgumentError);

// With specific message
expect(
  () => calculator.divide(10, 0),
  throwsA(isA<ArgumentError>()
    .having((e) => e.message, 'message', contains('zero'))),
);
```

## Stream Testing

```dart
expectLater(stream, emitsInOrder([1, 2, 3]));
expectLater(stream, emitsDone);
expectLater(stream, emitsError(isA<Exception>()));
```

## Fake Clock

```dart
import 'package:clock/clock.dart';

withClock(Clock(() => DateTime(2024, 1, 1)), () {
  expect(DateTime.now().year, 2024);
});
```

## Pitfalls

- Test behavior (output/state), not implementation (private methods)
- Don't depend on exact timing — test completion, not duration
- Each test must be independent — use setUp/tearDown
- Don't over-mock — only mock external boundaries
