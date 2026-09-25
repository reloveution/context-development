# Architecture Layers (Clean Architecture + BLoC/Cubit)

```
Presentation:  Pages/Screens (widgets) + Controllers (Cubit/BLoC)
Domain:        Use-cases, Entities, Repository interfaces, Services
Data:          Repository implementations + Datasources
```

## Presentation Layer

### Pages/Screens
- Compose widgets for UI; contain no business logic
- Dispatch events to BLoC / call Cubit methods
- Rebuild via `BlocBuilder`/`BlocListener`/`BlocConsumer`
- Allowed logic: conditional rendering, animations, layout, routing

### Controllers (Cubit/BLoC)
- Transform use-case results into UI state
- Manage UI state via `emit()`
- Depend on Use Cases via constructor injection
- No Flutter imports, no direct data access

## Domain Layer

### Use Cases (`Usc` suffix)
- Single business operation per use case
- Depend on Repository interfaces (many-to-many)
- Can depend on other Use Cases
- Return `Result<T>`

### Entities
- Pure domain models, no DB/API knowledge
- Immutable with `copyWith`

### Repository Interfaces (`I` prefix)
- Abstract contracts defined in domain layer
- Implementations live in data layer

### Services
- Domain-level services for cross-cutting business logic (permissions, checklists)

## Data Layer

### Repository Implementations (`Impl` suffix)
- SSOT for data types; one repo per data type
- Implement domain interfaces
- Aggregate data from Datasources, parse raw data into domain models
- Handle caching, error handling, retry logic
- Expose data as Streams or Futures

### Datasources (`Dts` suffix)
- Wrap external data sources (APIs, databases, platform plugins)
- Stateless; one datasource per data source
- Return raw data; parsing happens in repositories

## Layer Communication

1. Adjacent layers only: Presentation → Domain → Data
2. State flows: Data → Domain → Presentation; Events flow: Presentation → Domain → Data
3. Presentation never reaches Data directly
4. Lower layers don't depend on upper layers

## Testing

- **Widgets**: widget tests
- **Cubit/BLoC**: unit tests with `bloc_test`, mock Use Cases
- **Use Cases**: unit tests, mock Repositories
- **Repositories**: unit tests, mock Datasources
- **Datasources**: integration tests
