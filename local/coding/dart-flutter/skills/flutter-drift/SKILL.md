---
name: flutter-drift
description: Sets up Drift in a Flutter app — drift_flutter, web wasm and worker, isolates, and watch-query limits. Use when adding or debugging local SQLite in Flutter, including web and widget tests. A non-Flutter Dart process, including a CLI, server, or PostgreSQL, uses dart-drift.
---

# Flutter Drift

Use this for a Flutter app's local SQLite database. A CLI, server, or other
non-Flutter Dart process uses `dart-drift`. Open the app database with
`driftDatabase` from `drift_flutter`. From Drift 2.32.0 with `sqlite3` 3.x, a
new app does not need `sqlite3_flutter_libs` or `sqlcipher_flutter_libs`.
`drift_sqflite` has no isolate support and does not work under `flutter test`.

## Open the database

Add packages with the setup guide's command. Do not reuse version pins from an
older snippet:

`dart pub add drift drift_flutter path_provider dev:drift_dev dev:build_runner`

The class needs a `schemaVersion` and an optional `QueryExecutor`, so tests
and `computeWithDatabase` can replace the opener:

```dart
AppDatabase([QueryExecutor? executor]) : super(executor ?? _open());

@override
int get schemaVersion => 1;
```

`driftDatabase(name: ...)` stores `$name.sqlite` in
`getApplicationDocumentsDirectory()`. Set at most one of `databaseDirectory`
and `databasePath`. Pass `databaseDirectory: getApplicationSupportDirectory`
when the file should not sit in the user documents directory — on Windows the
documents directory is the user folder and application support is AppData —
and import `package:path_provider/path_provider.dart` for that function.
`driftDatabase` already runs SQL on a background isolate, including when
`shareAcrossIsolates` is set. Do not open a second `NativeDatabase` on the
same file. A hand-built `NativeDatabase` on Android still has to point sqlite3
at an app temp directory, because `/tmp` is not usable there; `drift_flutter`
does that itself via `getTemporaryDirectory`.

`part 'database.g.dart'` and `_$AppDatabase` stay unresolved until generation.
Run `dart run build_runner build`, or `dart run build_runner watch` while
editing the schema. Treat generated files as outputs (`dart-drift`).

## Web

Ship two files in `web/`, from the same Drift release as the `drift` version
in `pubspec.lock`: `sqlite3.wasm` and `drift_worker.dart.js`. The web guide's
samples use that worker name; the release build command is
`dart compile js -O4 web/drift_worker.dart`. Pass
`sqlite3Wasm: Uri.parse('sqlite3.wasm')` and
`driftWorker: Uri.parse('drift_worker.dart.js')`. The `DriftWebOptions`
dartdoc still shows a `drift_worker.js` sample; the URI has to be the file
that is actually in `web/`. `package:drift/web.dart` (`WebDatabase`) is
deprecated.

Serve `sqlite3.wasm` as `Content-Type: application/wasm`. `flutter run` does.
A static host that does not will make the browser reject the module.
`Cross-Origin-Opener-Policy: same-origin` and
`Cross-Origin-Embedder-Policy: require-corp` turn on the faster file-system
path. Without them Drift uses a slower fallback, and Chrome on Android can
then race across tabs. Those headers also break some popup auth flows, so
turn them on only after that path still works.

## Isolates

Sending a database instance into `Isolate.run` or `compute` throws: the
instance holds streams and futures. For a heavy job on another isolate, call
`computeWithDatabase` from `package:drift/isolate.dart` and construct the
database with the connection it supplies. A hand-rolled
`serializableConnection` closes the isolate-side database when the task ends.

`shareAcrossIsolates` defaults to false. Turn it on when more than one
isolate in the same Flutter engine opens that database: `watch()` stays
aligned across them, and drift avoids "database is locked" from concurrent
transactions. Discovery uses `IsolateNameServer`, so a separate Flutter
engine still gets its own database and its writes do not update the first
engine's streams.

## Watch queries

`watch()` emits the current rows on listen, then again after a write made
through Drift. A write from another SQLite client does not. A custom select
sets `readsFrom`, and a custom update sets `updates`, or the stream has no
tables to follow. Invalidation is per table, not per row, so a watched query
stays small. Subscription cancel belongs to `dart-resource-management`.
Choosing `StreamBuilder` belongs to `flutter-state-management`.

## Tests

Inject `NativeDatabase.memory()` from `package:drift/native.dart`. Do not
call the production `driftDatabase()` opener in a test: it calls
`path_provider`, including `getTemporaryDirectory`, which has no plugin
implementation there.

When a widget test watches a query, wrap the memory database in
`DatabaseConnection` with `closeStreamsSynchronously: true`. Drift keeps a
cancelled query stream open for one event-loop turn so a `StreamBuilder` can
resubscribe, and a widget test fails if that timer is still pending. Close
the database in the test's teardown.

```dart
AppDatabase(
  DatabaseConnection(
    NativeDatabase.memory(),
    closeStreamsSynchronously: true,
  ),
);
```

## Boundaries

`dart-drift` owns platform choice, companions, `getSingle` versus
`getSingleOrNull`, transactions, generated outputs, versioned migrations, and
SQLite `PRAGMA foreign_keys`. `dart-data-patterns` owns mapping a row to a
domain value. `flutter-performance` owns N+1 and batching; its `compute()`
rule is for plain CPU work, not a Drift instance. `flutter-testing` owns
which test type to write. `flutter-widget-patterns` owns `context.mounted`
and widget composition.

## Sources

Setup: <https://drift.simonbinder.eu/setup/>.
Web: <https://drift.simonbinder.eu/platforms/web/>.
Platforms: <https://drift.simonbinder.eu/platforms/>.
Isolates: <https://drift.simonbinder.eu/isolates/>.
Streams: <https://drift.simonbinder.eu/dart_api/streams/>.
Testing: <https://drift.simonbinder.eu/testing/>.
Migrations, including the foreign-key pragma: <https://drift.simonbinder.eu/migrations/>.
`driftDatabase` file location: <https://pub.dev/documentation/drift_flutter/latest/drift_flutter/driftDatabase.html>.
Support-directory override: <https://github.com/simolus3/drift/issues/3139>.
Test opener and `getTemporaryDirectory`: <https://github.com/simolus3/drift/issues/3385>.
