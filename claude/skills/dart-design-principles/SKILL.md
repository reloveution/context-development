---
name: dart-design-principles
description: Core software design principles for maintainable Dart/Flutter code. Use when applying SOLID, composition over inheritance, polymorphism over switch/case, immutability, abstraction layers, and code reusability.
---

# Dart Design Principles

## SOLID

- **Single Responsibility**: one reason to change per class
- **Open/Closed**: extend via new implementations, not by editing existing code
- **Liskov Substitution**: subtypes must honor behavioral contracts of base types
- **Interface Segregation**: small specific interfaces; clients must not depend on unused methods
- **Dependency Inversion**: depend on abstractions; high-level modules never depend on low-level modules directly

## Polymorphism Over Type Checking

Use base interface methods directly when all switch/case branches call the same method with the same parameters. Avoid unnecessary type casting (`as`) when the interface provides needed functionality.

### Bad (Redundant Switch)

```dart
IParam _updateParam(IParam param, IParamValue newValue, String changedBy) {
  switch (param.paramType) {
    case ParamType.text:
      final textParam = param as TextParam;
      return textParam.copyWith(
        changeHistory: textParam.changeHistory.addChange(
          newValue as TextParamValue, changedBy),
      );
    case ParamType.integer:
      final intParam = param as IntegerParam;
      return intParam.copyWith(
        changeHistory: intParam.changeHistory.addChange(
          newValue as IntegerParamValue, changedBy),
      );
    case ParamType.decimal:
      final decParam = param as DecimalParam;
      return decParam.copyWith(
        changeHistory: decParam.changeHistory.addChange(
          newValue as DecimalParamValue, changedBy),
      );
  }
}
```

### Good (Polymorphic)

```dart
IParam _updateParam(IParam param, IParamValue newValue, String changedBy) =>
    param.copyWith(
      changeHistory: param.changeHistory.addChange(newValue, changedBy),
    );
```

When behavior truly varies by type, switch/pattern matching is still appropriate.

## Composition and Abstraction

- Prefer composition over inheritance when it adds flexibility and testability
- Compose behavior from smaller, focused components
- Hide implementation details behind abstractions; expose only what clients need
- Use interfaces for contracts between modules; enables mocking and swapping implementations

## Code Style

- Prefer functional and declarative patterns over verbose imperative style
- Prefer immutable data structures; use `final` fields and `copyWith` for updates
- Implement `hashCode` and `operator==` for custom classes (consider Equatable)

## Reusability

- Share behavior via inheritance ("is-a") or composition ("has-a") based on relationship
- Extract repeated logic into utility functions; prefer extension methods for type-specific utilities
- Centralize validation logic; validate at boundaries (input, API response)
