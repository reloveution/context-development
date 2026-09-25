# Architecture Error Handling

All services, repositories, use cases, and controllers communicate through `Result<T>`. Never throw in business logic. See **dart-error-handling** skill for details.

## Multi-Level Protection (critical operations)

1. **Result\<T\>** — primary error wrapper (`Result.success(data)` / `Result.error(message:, stackTrace:)`)
2. **runZonedGuarded** — wrap critical measurement/calculation zones
3. **try/catch** — within zones for transient failures

```dart
runZonedGuarded(() async {
  try {
    final result = await repo.getData();
    return result;
  } on TimeoutException catch (e, s) {
    return Result.error(message: 'Timeout', stackTrace: s);
  }
}, (e, s) => log('Zone error', error: e, stackTrace: s));
```

## Layer Responsibilities

- **Repositories**: Convert exceptions to `Result.error(message:, stackTrace:)`
- **Use Cases**: Propagate and compose `Result<T>`
- **Controllers (Cubit/BLoC)**: Handle `Result<T>` via `.when()` for UI state emission
