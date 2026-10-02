---
name: dart-mocktail
description: Mocktail-specific Dart test-double mechanics. Use when declaring a Mocktail mock or fallback fake, stubbing or verifying a Mocktail call, matching arguments, registering fallback values, or fixing an unstubbed-call type error.
---

# Dart Mocktail

## Declare doubles

Use a bare `Mock` subclass for a dependency whose calls need stubbing or
verification; Mocktail supplies the implementation.

```dart
class MockIRepository extends Mock implements IRepository {}
```

Use a `Fake` as a fallback value for an argument matcher:

```dart
class FakeRequest extends Fake implements Request {}
```

## Fallback Values

- Before using `any()` or `captureAny()` for a non-nullable custom parameter,
  register a fallback value. Primitive types are already registered.
- Register each type once, before the matcher is used; `setUpAll()` keeps that
  global registration out of individual tests.

```dart
setUpAll(() {
  registerFallbackValue(FakeRequest());
});
```

## Stubbing

- Use `thenReturn(value)` for a fixed synchronous response and `thenAnswer(...)`
  for a computed or asynchronous response.
- Use `thenThrow(error)` to make a call fail.
- Stub every invoked member with a non-nullable return type. An unstubbed
  Mocktail member returns `null`, which causes a type error at that call site.

## Verification

- `verify(() => mock.method())` records a matching call; append `.called(n)`
  for its count.
- `verifyNever(() => mock.method())` asserts that no matching call occurred.

## Parameters and Matchers

- Include named arguments in the stub or verification closure; use
  `any(named: 'param')` when their value is irrelevant.
- `any()` matches a positional argument; `captureAny()` records one for a
  later assertion; `captureAny(that: matcher)` records only a matching argument.

## Boundary

Choose a real collaborator, fake, or mock by test intent; structure assertions;
and handle unit, widget, integration, and plugin tests with **flutter-testing**.

## Source

Mocktail package documentation: <https://pub.dev/packages/mocktail>
