---
name: flutter-security
description: Security best practices for Flutter apps. Use when storing credentials, validating input, securing network/API, or preventing XSS.
---

# Flutter Security

## Storage
- Never store sensitive data in `SharedPreferences` or plain text
- `flutter_secure_storage` for API keys, tokens, credentials

## Input & Display
- Validate all user inputs on both client and server
- Sanitize data before displaying (XSS prevention)

## Network
- HTTPS only for all communications
- Certificate pinning for critical APIs
- Proper session management and token refresh

## Logging
- Never log passwords, tokens, personal data
