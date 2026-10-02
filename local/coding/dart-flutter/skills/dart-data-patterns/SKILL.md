---
name: dart-data-patterns
description: Defines DTO, serialization, mapping, and validation boundaries for Dart and Flutter data. Use when decoding, encoding, or translating external data into domain values.
---

# Dart Data Boundaries

Keep external representation at the data boundary. A domain entity carries
business meaning; a DTO carries an API, database, or file schema. Neither is a
convenient substitute for the other.

## Map deliberately

- Keep JSON, SQL, platform, and transport details out of domain entities.
- Give each external schema one DTO and keep decoding, encoding, and DTO-to-domain
  mapping together. Do not scatter casts or JSON keys through repositories,
  use cases, or widgets.
- Validate untrusted shape, nullability, ranges, and required fields before a
  value becomes a domain object. Return a boundary-specific failure instead of
  inventing a partially valid entity.
- Map domain values back to DTOs only at an outbound boundary. Do not let a
  persistence format become the public domain contract.
- Use generated serializers only when their generated mapping is reviewed as
  part of the source change; generated output is not a place for hand edits.

## Keep schema changes honest

- Version a persisted schema and write an explicit upgrade path before changing
  stored representation. Test that path against representative existing data.
- For user data, add export, import, backup, or recovery only when the product
  needs that promise. Validate imported and recovered data at the same boundary
  as network or file input, and make corrupt-data handling explicit.

`flutter-architecture` owns repositories, layer flow, caching, synchronization,
and offline-first. `flutter-performance` owns N+1, pagination, isolates, and
data-flow cost; `dart-resource-management` owns stream lifecycle; and
`flutter-security` owns storage and transport security.
