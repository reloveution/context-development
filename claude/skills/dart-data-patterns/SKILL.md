---
name: dart-data-patterns
description: Data handling patterns for Dart/Flutter. Use when implementing serialization, caching, layer separation, DTOs, repositories, offline-first, or data validation.
---

# Data Patterns

## Data Flow

- Repositories = single source of truth; reconcile local cache + remote; expose immutable data
- Abstract data sources (API, DB) via repository/service interfaces
- Consumers depend on abstractions, not implementations

## Layer Boundaries

- Domain entities: no JSON, no SQL, no platform APIs
- DTOs encapsulate all mapping and JSON conversion; tables reference DTOs, not converters
- Data layer owns serialization/persistence; domain layer owns business rules

## Serialization

- DTOs for data transfer between layers; separate from domain entities
- `fromJson`/`toJson` with explicit nullability and type handling
- Code generation (json_serializable, freezed) when appropriate
- `copyWith` for immutable updates; validate at boundaries before use

## Streaming

- `Stream<T>` from repositories for reactive data (WebSocket, DB watch, polling)
- Broadcast streams when multiple listeners; handle errors and completion

## Caching & Performance

- TTL-based caching with invalidation rules (on write, time, demand)
- Cursor-based or offset-based pagination for large datasets
- Isolates (`compute()`) for large payload parsing; minimize serialization in hot paths

## N+1 Avoidance

Repo/HTTP/Drift call in a loop = N+1. Fix: bulk fetch by id + in-memory join · joined Drift (`leftOuterJoin`/`innerJoin`) · preload / `Future.wait` · DataLoader.

Preserve when batching: auth/tenancy/soft-delete · missing-record (don't invent rows) · `ORDER BY`/`LIMIT` · rate-limit/retry. `Future.wait` reports only the first error — wrap each future in `.catchError(...)` for partial success.

Catalog/scanner (Dart-aware): `flutter-performance` (flags `io-or-query-in-loop`).

## Synchronization

- Sync strategy: last-write-wins, merge, or conflict resolution
- Optimistic updates: apply locally → reconcile with backend; roll back on failure
- Offline-first: serve from local cache, queue writes offline, flush when connected

## Data Management

- Version schema; support upgrade paths; test migrations on real data
- Normalize where appropriate; denormalize for read performance
- Compress large payloads when beneficial (balance CPU vs bandwidth)

## Security

- Encrypt at rest (`flutter_secure_storage` for credentials); HTTPS for network
- Support export/import for user data; handle corrupt data gracefully
