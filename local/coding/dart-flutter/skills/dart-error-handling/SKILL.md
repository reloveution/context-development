---
name: dart-error-handling
description: Defines Result-based failure boundaries for Dart and Flutter. Use when classifying failures, catching external exceptions, or converting them into domain results.
---

# Dart Error Boundaries

Use `Result<T>` for an expected failure that the caller can handle as data. Keep
programming faults visible: a `StateError`, assertion failure, or violated
invariant is not an ordinary user-facing result.

## Convert at the boundary

- Catch expected exceptions at the external boundary that understands them:
  network, database, file, platform, or parser code. Convert them once to a
  domain failure with the operation and safe context.
- Do not wrap pure domain code in a broad `try/catch` just to return `Result`.
  Let an unexpected programming error preserve its stack and reach the error
  boundary that can diagnose it.
- Catch a specific expected type when recovery differs. Do not catch `Error` as
  a normal failure path, and do not replace an unknown failure with a successful
  default.
- Keep the diagnostic cause and stack trace available to logs or reporting, but
  expose a separate safe message or recovery action to the user.

## Make failure actionable

- Validate untrusted input at its boundary and return the field, operation, or
  next step that the caller can use to recover.
- Model absence, permission denial, conflict, and invalid input separately when
  callers need different behavior; do not collapse them into an undifferentiated
  string.
- Preserve a `Result` returned by a dependency unless this layer can add context
  or translate it into the contract it owns.

`flutter-networking` owns retry and transport-specific exceptions;
`dart-resource-management` owns cleanup; `flutter-security` owns sensitive-data
rules for logging and reporting.
