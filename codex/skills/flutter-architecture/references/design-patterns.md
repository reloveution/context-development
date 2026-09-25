# Design Patterns

## Result\<T\>

Project implementation: `lib/shared/domain/entities/result.dart`

Single class with `isSuccess` flag, `data`, `errorMessage`, `stackTrace`, `timestamp`. Not a sealed class.

```dart
// Creating
Result.success(data)
Result.error(message: 'Failed', stackTrace: stackTrace, fallbackData: cached)

// Consuming — side effects (e.g. emit states in Cubit)
result.when(
  onSuccess: (data) => emit(SuccessState(data)),
  onError: (error, stack) => emit(FailureState(error)),
);

// Consuming — return a value
final state = result.map(
  onSuccess: (data) => SuccessState(data),
  onError: (error, stack) => FailureState(error),
);

// Direct access
if (result.isSuccess) {
  final data = result.data;
}
```

## Repository Pattern

SSOT over datasources with caching and error handling.

```dart
class TodoRepoImpl implements ITodoRepo {
  final IApiTodoDts _api;
  final ILocalTodoDts _local;

  @override
  Future<Result<List<Todo>>> getTodos() async {
    try {
      final raw = await _api.fetchRaw();
      final todos = raw.map(Todo.fromJson).toList();
      return Result.success(todos);
    } catch (e, s) {
      return Result.error(message: 'Failed to load todos', stackTrace: s);
    }
  }
}
```

## Optimistic UI

Update UI immediately, rollback on error. Handled in Cubit/BLoC:

```dart
Future<void> addTodo(Todo todo) async {
  final previous = state.todos;
  emit(state.copyWith(todos: [...previous, todo])); // optimistic

  final result = await _addTodoUcs(todo);
  result.when(
    onSuccess: (_) {},
    onError: (error, _) {
      emit(state.copyWith(todos: previous)); // rollback
    },
  );
}
```

## Offline-First

Local cache as primary source, background sync when online.

```dart
class TodoRepoImpl implements ITodoRepo {
  final IApiTodoDts _api;
  final ILocalTodoDts _local;

  Stream<List<Todo>> get todos => _local.todosStream;

  @override
  Future<Result<void>> addTodo(Todo todo) async {
    try {
      await _local.saveTodo(todo);
      if (await _hasConnection()) {
        await _api.createTodo(todo);
      }
      return Result.success(null);
    } catch (e, s) {
      return Result.error(message: 'Failed to add todo', stackTrace: s);
    }
  }
}
```

## Pattern Selection

| Pattern | Use When |
|---|---|
| Result\<T\> | All business operations across all layers |
| Repository | Abstracting datasources, caching, SSOT |
| Optimistic UI | Instant UI response, network latency |
| Offline-First | Poor connectivity, offline support |
