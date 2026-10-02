---
name: flutter-security
description: Flutter security for credentials, TLS, and logs. Use when storing a secret, checking certificates, or deciding what may be logged.
---

# Flutter security

Put API keys, tokens, and credentials in `flutter_secure_storage`. Do not put
them in `SharedPreferences`, source, or a skill.

Send traffic over HTTPS. Do not install a certificate callback that accepts
every certificate. Certificate pinning is a separate product decision with a
rotation plan, not the default.

`Text` does not interpret HTML. Do not HTML-escape ordinary widget strings.
Sanitize only a source that a web view or an HTML widget will interpret.

Do not log passwords, tokens, session cookies, or raw authorization payloads.
`flutter-networking` owns request retry and single-flight token refresh.
`dart-error-handling` owns how a failure is represented.

## Sources

<https://pub.dev/packages/flutter_secure_storage>.
`HttpClient.badCertificateCallback`: <https://api.dart.dev/dart-io/HttpClient/badCertificateCallback.html>.
