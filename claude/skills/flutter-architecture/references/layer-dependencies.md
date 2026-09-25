# Layer Dependencies

## Dependency Chain

```
Controllers → Use Cases → Repositories → DataSources
     ↑            ↑            ↑              ↑
  (via DI)    (via DI)     (via DI)      (raw data)
```

All dependencies flow through **constructor interfaces** (abstract classes).

- **DataSources** return raw data (JSON, bytes, platform primitives)
- **Repositories** parse raw data into domain models — parsing happens only here
- **Use Cases** can depend on other Use Cases
- Communication only between adjacent layers; Presentation never reaches Data directly

## Example

```dart
abstract class IApiTodoDts {
  Future<Map<String, dynamic>> fetchRaw();
}

abstract class ITodoRepo {
  Future<Result<List<Todo>>> getTodos();
}

class TodoRepoImpl implements ITodoRepo {
  TodoRepoImpl(this._dts);
  final IApiTodoDts _dts;

  @override
  Future<Result<List<Todo>>> getTodos() async {
    final raw = await _dts.fetchRaw();
    return Result.success((raw['items'] as List)
        .map((e) => Todo.fromJson(e as Map<String, dynamic>))
        .toList());
  }
}

class GetTodosUcs {
  GetTodosUcs(this._repo, this._authUcs);
  final ITodoRepo _repo;
  final GetAuthUserUcs _authUcs;
}
```
