---
name: dart-error-handling
description: Error handling patterns for Dart/Flutter. Use when implementing Result<T>, exception vs Error, try-catch at boundaries, validation, retry, logging, and resource cleanup.
---

# Dart Error Handling

## Result<T>

- All business operations (sync included) return `Result<T>` -- never throw in business logic
- Use as UI feedback wrapper: `failure.message` or `failure.toUserMessage()` for snackbars/dialogs

## Exception vs Error

- **Exception**: expected failures (network, validation, I/O) -- catch with `on SpecificException catch (e) {}`
- **Error**: programming errors (AssertionError, StateError) -- never catch, let propagate
- Only throw `Error` subclasses for programming errors (lint: `only_throw_errors`)
- `rethrow` (not `throw e`) to preserve stack trace (lint: `use_rethrow_when_possible`)

## Try-Catch

- Use only at external boundaries (HTTP, database, file I/O, platform channels) -- convert to `Result.failure` immediately
- Never wrap pure business logic that uses `Result<T>`
- `finally` for cleanup only -- no control flow, no return, no throw (lint: `control_flow_in_finally`, `throw_in_finally`)

## Error Types

- Specific types: `NetworkFailure`, `ValidationError`, `NotFoundError`
- Include context: which field failed, suggested next step
- Map platform exceptions to domain `Result` failures
- User-facing: friendly messages only, never expose technical details

## Validation and Retry

- Validate at boundaries, fail fast -- return `Result.failure` with clear messages
- Network retry: exponential backoff for transient failures only
- Set max retries; return `Result.failure` after exhaustion

## Logging

- `log()` from `dart:developer` -- never `print`/`debugPrint` (lint: `avoid_print`)
- Include: error type, message, stack trace, relevant IDs
- Crash reporting (e.g. Firebase Crashlytics) for production
- Never log sensitive data (passwords, tokens, PII)

## Resource Cleanup

- Close sinks, cancel subscriptions, close connections/file handles in `dispose` (lint: `close_sinks`, `cancel_subscriptions`)
- Ensure cleanup runs on error paths -- use try-finally or `await for` with disposal
- Design for failure paths explicitly -- never fail silently
