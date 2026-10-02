---
name: dart-code-quality
description: Preserves Dart's static type and null-safety guarantees in application code. Use when resolving analyzer findings, choosing Dart types, or handling nullable and unawaited values.
---

# Dart Code Quality

Treat the project's formatter, analyzer, and lint configuration as the owner of
mechanical style. Do not add a competing length, naming, member-order, or
comment rule here.

## Preserve static guarantees

- Keep domain APIs, collection elements, and generic arguments specific enough
  for static analysis to find invalid values. `dynamic` is appropriate only at
  a genuinely dynamic boundary; validate and convert it before domain use.
- Let inference express local types when it remains clear. Add an annotation
  when inference would widen the value or obscure the contract.
- Treat `!` as an assertion of an established invariant, not a way to silence a
  nullable value. Establish the invariant or handle the null path first.
- Do not replace a typed collection with a `dynamic` collection or cast it back
  to a more specific element type.

## Make asynchronous ownership explicit

- Await work whose completion, result, or failure belongs to the current
  operation. For deliberately detached work, use `unawaited()` and arrange
  error handling with the owner of that work.
- Use `Future<void>` only when callers have no result to consume. Propagate or
  convert a failure according to `dart-error-handling`.

## Route adjacent concerns

`dart-error-handling` owns failure contracts, `simple-code` owns abstraction
and structure choices, and `flutter-testing` owns test design. Do not duplicate
their rules here.

## Sources

- [Dart type system](https://dart.dev/language/type-system) — sound types,
  inference, dynamic values, and strict casts.
- [Understanding null safety](https://dart.dev/null-safety/understanding-null-safety)
  — nullable types and null assertions.
- [`unawaited`](https://api.dart.dev/dart-async/unawaited.html) — marking an
  intentionally unawaited future.
