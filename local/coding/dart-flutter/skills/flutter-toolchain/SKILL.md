---
name: flutter-toolchain
description: Flutter SDK and pub-dependency workflow. Use when running Flutter/Dart project commands, checking an FVM pin, adding or removing packages, or choosing a dependency.
---

# Flutter Toolchain

Use the SDK and dependency graph selected by the project; do not silently
replace either.

## SDK

- When the project has an FVM selection (`.fvmrc` or its documented equivalent),
  run Flutter and Dart through `fvm flutter` and `fvm dart`.
- Otherwise follow the project's documented toolchain. Do not run `fvm use`,
  initialize FVM, or change an SDK version unless the user requests that change.

## Dependencies

- Before proposing a new package, inspect its pub.dev page and primary
  documentation. If the connected `dart:pub_dev_search` tool is available, use
  it for discovery.
- Add or remove a dependency through connected `dart:pub` when available;
  otherwise use the selected SDK's `flutter pub add` or `flutter pub remove`.
  Use `dev:<package>` only for development dependencies.
- Let pub update `pubspec.yaml` and the lockfile together. Do not hand-edit a
  version merely to force a resolution; inspect compatibility first.
- Adding a platform plugin can require a full restart rather than hot reload.

## Sources

- [FVM project versions](https://fvm.app/documentation/getting-started/faq)
- [dart pub add](https://dart.dev/tools/pub/cmd/pub-add)
- [Flutter packages](https://docs.flutter.dev/packages-and-plugins/using-packages)
