---
name: flutter-internationalization
description: Localizes Flutter UI with slang — JSON source, generated t, and locale rebuilds. Use when adding or changing user-facing strings. gen-l10n and ARB are not this package's localization.
---

# Flutter internationalization

User-facing copy lives in slang JSON and is read through the generated
translations. Do not add gen-l10n, ARB files, or `AppLocalizations`.

## Source and generation

Edit the locale JSON the project stance names. Do not edit `strings.g.dart`
or `strings_*.g.dart`; they are generator output. Regenerate with
`dart run slang`. A project stance may prefix that command with its SDK
runner. A new string is a JSON entry, then a regeneration, then a use of the
generated member.

## Reading strings

The global `t` reads the current locale and does not rebuild widgets when
the locale changes. Use it when the locale stays fixed for the process.
When the user can change locale at runtime, wrap the app in
`TranslationProvider` and read `Translations.of(context)` or `context.t`.
Pass `AppLocaleUtils.supportedLocales` to `MaterialApp.supportedLocales`.

Write the whole sentence in JSON, with slang parameters when a value is
inserted. Do not concatenate translated fragments in Dart.

## Boundaries

The project stance owns the JSON path, which locales exist, and any SDK
prefix on the slang command. `dart-data-patterns` owns mapping external
payloads. This skill owns UI copy only.

## Sources

Slang 4 generated contract (`t`, `TranslationProvider`, `dart run slang`):
the header of `strings.g.dart` in an app that runs slang.
Package: <https://pub.dev/packages/slang>.
