---
name: dart-mocktail
description: Mocktail testing guidelines for Dart/Flutter. Use when creating mocks, fakes, stubbing async/sync, verifying interactions, registerFallbackValue, or avoiding MissingStub errors.
---

# Dart Mocktail

## Fake vs Mock

- **Fake:** lightweight custom behavior subset; use when asserting on outcomes (result values, state).
- **Mock:** use when verifying interactions (specific methods called, args, call count).
- Prefer real collaborators or fakes over mocks -- outcome-based tests are more robust.

## Mock Creation

- Extend `Mock` -- never add manual overrides or concrete implementations.

```dart
class MockIRepository extends Mock implements IRepository {}
```

## Fallback Values

- Register fallback values for every non-nullable custom type used in matchers (`any()`, `captureAny()`, `captureThat()`).
- Must run before stubbing or verifying -- typically in `setUpAll()`.

```dart
setUpAll(() {
  registerFallbackValue(MyDomainType());
  registerFallbackValue(Result.success(dummy));
});
```

## Stubbing

- Sync: `when(() => mock.method()).thenReturn(value)` for fixed return.
- Sync dynamic: `thenAnswer((invocation) => value)` for computed response.
- Async: `thenAnswer((_) async => result)` -- preferred over `thenReturn(Future.value(...))`.
- Failure: `thenThrow(error)` for error branches.
- Stub every dependency method the test expects to execute -- unstubbed calls cause `MissingStubError`.

## Verification

- `verify(() => mock.method())` -- method was called.
- `verifyNever(() => mock.method())` -- method was not called.
- `verify(() => mock.method()).called(n)` -- assert exact call count.

## Parameters and Matchers

- Supply all named parameters in both stubs and verifies; use `any(named: 'param')` when the exact value is irrelevant.
- `any()` -- match any positional value.
- `captureAny()` -- capture argument for later assertion.
- `captureThat(matcher)` -- capture when matcher matches.

## Best Practices

- Custom types used in matchers should have consistent `==` and `toString` for deterministic assertions.
