# Architecture Concepts

## Separation of Concerns

- Split app into UI, Domain (optional), Data layers
- Widgets focused on presentation; business logic in Cubits/BLoCs and Use Cases
- Layers communicate only with adjacent layers

## Single Source of Truth (SSOT)

Each data type has one authoritative source (typically a Repository) that is the only class allowed to modify that data.

- Use getters to derive values from SSOT field
- Use records to group related values instead of parallel lists
- One repository per data type

## Unidirectional Data Flow (UDF)

State flows: Data → Logic → UI. Events flow: UI → Logic → Data.

1. User interaction triggers event handler
2. Logic class calls repository methods
3. Repository updates data and provides new state
4. UI rebuilds with new state

Data can also originate from data layer (e.g., polling). Changes always happen in SSOT.

## UI = f(State)

- Data drives UI, not the other way
- Data should be immutable and persistent
- Views contain minimal logic
