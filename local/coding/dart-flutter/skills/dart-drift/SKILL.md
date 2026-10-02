---
name: dart-drift
description: Guides Drift for non-Flutter Dart services, CLI tools, and PostgreSQL or native SQLite deployments. Use when implementing or migrating Drift outside a Flutter app.
---

# Drift for Non-Flutter Dart

Use this skill for a CLI, server, or other non-Flutter Dart process. A Flutter
application uses `flutter-drift` instead. Choose the database platform before
writing schema code: native SQLite and PostgreSQL differ in generated SQL,
migration support, lifecycle, and deployment assumptions.

## Database boundary

- Keep credentials, endpoints, pool limits, and timeouts in deployment
  configuration, never in source or a skill.
- Register one database owner for the process and close it during shutdown.
  Share that owner with DAOs; do not open a connection per query.
- Use Drift tables, DAOs, and generated row or companion types as the persistence
  boundary. Map them to domain values outside that boundary.
- Use a companion for partial writes: absent means leave a column unchanged,
  while a present null means write SQL `NULL`.

## Queries and transactions

- Use `getSingle()` only when absence and duplicates are violations; use
  `getSingleOrNull()` when absence is an expected result.
- Put a logically atomic group of writes in one transaction. Do not report
  success, publish an event, or update a cache before that transaction commits.
- Add indexes only for an observed query shape, then verify the query plan or
  measured effect. A broad index or a watch stream is not a default optimization.

## Schema change

- Change a persisted schema with a versioned migration, not by modifying a table
  and assuming existing databases will update themselves.
- Generate schema snapshots and migration tests before shipping a schema change;
  test upgrade from representative prior data and the data transformation, not
  just opening an empty database.
- SQLite migrations can use Drift's migrator APIs. Turn on SQLite foreign keys
  in `beforeOpen` with `PRAGMA foreign_keys = ON`, as the migrations guide
  shows; that pragma is not a PostgreSQL step. For PostgreSQL deployments with
  multiple application servers, manage schema changes with a dedicated
  migration process; do not assume SQLite-oriented migration operations apply.

## Scope

- Generated Drift files are outputs: edit the schema or DAO source, regenerate,
  and review the generated diff instead of hand-editing outputs.
- Streams and subscriptions need an explicit owner and cancellation path; use
  `dart-resource-management` for lifecycle details.
- Use `flutter-performance` for N+1, batching, and data-flow cost rather than
  changing query structure solely because it appears complex.
