# Async Design

Write all methods in controllers, use cases, repositories, and datasources as `Future` from the start. Adding `async` later forces all callers to change.

Keep synchronous only for: pure computation, in-memory transformations, getters returning already-loaded data, validation without external calls.

```dart
// Good: Future from the start
abstract class ITodoRepo {
  Future<Result<List<Todo>>> getTodos();
  Future<Result<void>> addTodo(Todo todo);
}

// Avoid: sync initially, forced rewrite when adding network
abstract class ITodoRepo {
  List<Todo> getTodos();
}
```
