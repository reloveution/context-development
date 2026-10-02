---
name: flutter-networking
description: Owns Flutter HTTP and WebSocket calls — client choice, timeouts, cancellation, and retry. Use when sending or debugging requests. Parsing, token storage, and failure types belong to their owners.
---

# Flutter networking

Use the HTTP client the app already depends on. Do not add a second client
beside it. A request has a connect timeout and a receive timeout; a call with
neither can hang its owner.

## Cancellation and status

Pass a cancel token into the call and cancel it when the owner ends.
`dart-resource-management` owns that lifetime. A socket reconnect closes the
previous socket before opening the next one.

If the client is configured to accept every status code, HTTP errors arrive
on the response, not as exceptions. Handle the status there. Do not also wait
for an error interceptor to see those codes.

## Retry

Retry a safe, idempotent request after a transport failure or a 408 or 5xx
response. A 429 waits for the delay the server indicates instead of an
immediate repeat. Do not retry a non-idempotent write unless the server
contract makes that retry safe. A 401 refresh is single-flight: parallel
callers wait for one refresh instead of each starting one.

## Boundaries

`dart-error-handling` owns converting a transport failure into a domain
result. `dart-data-patterns` owns JSON mapping. `flutter-performance` owns
moving a large parse off the UI isolate. `flutter-security` owns token
storage, certificate checks, and what must not be logged. A logger that
prints request or response bodies is off unless the payload is known not to
carry credentials.

## Sources

Idempotent methods: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods>.
Dio cancel tokens and `validateStatus`: <https://pub.dev/packages/dio>.
