---
name: dart-3-patterns
description: Applies Dart 3 patterns and records safely — exhaustiveness, guards, destructuring, and record shape. Use when matching values, validating shapes, or returning multiple values.
---

# Dart 3 Patterns

Use patterns to match a value's shape and bind its parts in one operation. They
require language version 3.0 or later. Prefer them when matching, validation, or
a destructured result is clearer than casts and temporary variables.

## Exhaustive control flow

- Use a switch expression for one produced value and a switch statement for
  effects or multiple statements.
- A `when` guard runs after a pattern matches; a false guard continues to the
  next case. Put a condition in a guard when the following case must handle its
  false path.
- For a sealed hierarchy or enum, cover every known variant. Do not add `_` or
  `default` merely to silence exhaustiveness when a new variant should force a
  compiler error.
- In `p1 || p2`, every alternative must bind the same variables with compatible
  types. Use `&&` only when both constraints must match.

```dart
final label = switch (shape) {
  Square(size: final size) || Circle(size: final size) when size > 0 => 'valid',
  Square() || Circle() => 'empty',
};
```

## Destructure deliberately

- Use `if (value case pattern)` for a single refutable match; variables it binds
  exist only in the matching branch.
- List and map patterns validate shape while destructuring external data. Match
  untrusted input before treating its fields as domain values.
- Object patterns read the getters they name. Match only properties that belong
  to the object's stable public contract.
- Use `?` when a subvalue must be non-null to match; use `!` only when failure
  is the intended result of a null value.

```dart
if (data case {'user': [String name, int age]}) {
  saveUser(name, age);
}
```

## Records

- Records are anonymous, immutable, fixed-size, heterogeneous typed values.
- Named field names are part of record shape and type; positional field labels
  are documentation only. Access positional fields with `$1`, `$2`, and named
  fields by name.
- Use a record for a small value group or multiple return values. Use a class
  when the value needs behavior, invariants, identity, or an extensible API.

```dart
final (:name, :age) = getUserInfo();
```
