---
name: dart-dependency-injection
description: Dependency injection patterns for Dart/Flutter applications. Use when configuring get_it, registering dependencies, using constructor injection, setting up composition root, and testing with mocks.
---

# Dart Dependency Injection

## Composition Root

- `get_it` calls (`getIt.get<T>()`) only at app init (`main()` or setup function)
- Never inside class constructors or methods
- Exception: global UI services (e.g. audio player for button click sounds) -- document clearly, keep to absolute minimum
- Resolve dependencies at composition root, pass to constructors when creating instances

```dart
// Composition root (main.dart or setup function)
final service = getIt<IService>();
final repository = getIt<IRepository>(param1: service);
final useCase = getIt<IUseCase>(param1: repository);
final controller = MyController(useCase: useCase);
```

## Constructor Injection

- All dependencies through constructors: `MyClass(this.service, this.repository)`
- Use abstract classes as interfaces, not concrete implementations
- Enables swapping implementations in tests without overriding get_it

## Registration

- Order: datasources -> repositories -> use cases -> controllers (leaf nodes first)
- Factory: stateless services, new instance per resolution
- Singleton: stateful services (repositories, API clients, databases), shared instance
- Prefer instance-based singletons -- avoid static methods and lazy proxy wrappers

## Lifecycle & Scoping

- Dispose singletons that hold resources (database, StreamController)
- Global singletons for app-wide services
- Scoped providers (e.g. `RepositoryProvider`) for feature-specific dependencies in Flutter

## Circular Dependencies

- If A depends on B and B on A: extract shared interface, introduce mediator, or split responsibility
- Circular registration causes runtime errors or infinite loops

## Testing

- Constructor injection enables easy mocking: `MyClass(mockService, mockRepository)`
- No need to override get_it or register mocks globally for unit tests
- Separate setup functions or parameters to switch implementations per environment (dev/staging/prod)

```dart
test('should do something', () {
  final mockRepo = MockIRepository();
  when(() => mockRepo.get()).thenAnswer((_) async => result);
  final useCase = MyUseCase(mockRepo);
  // test useCase
});
```
