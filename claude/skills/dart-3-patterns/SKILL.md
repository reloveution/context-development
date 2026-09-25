---
name: dart-3-patterns
description: Dart 3 patterns including switch/if-case, pattern matching, sealed classes, and records. Use when writing exhaustive switches, destructuring, pattern matching on types, or returning multiple values with records.
---

# Dart 3 Patterns

## Switch

- **Statement:** no `break` needed; matching case runs and exits
- **Expression:** `=>` branches, commas between cases, `_` for default
- **Guards:** `case pattern when condition:` — evaluated after match; false → next case
- **Logical-or:** `case a || b` — share body; same variables in each branch
- **Exhaustiveness:** enforced at compile time via `sealed` classes, enums, or `_`/`default`
- Empty `case` falls through; labeled `continue` for non-sequential fallthrough

## if-case

- Single pattern match: `if (pair case [int x, int y]) { ... }`
- Bound variables scoped to matched branch; `else` when no match

## Pattern Types

- **Logical-or** (`p1 || p2`): left-to-right; same variables in each branch
- **Logical-and** (`p1 && p2`): both must match; variable names must not overlap
- **Relational** (`==`, `<`, `>=`...): compare against constants; combine with `&&` for ranges
- **Cast** (`sub as Type`): assert type; throws on mismatch
- **Null-check** (`sub?`): match non-null, bind as non-nullable
- **Null-assert** (`sub!`): require non-null, throw otherwise
- **Constant**: match equality to constants (const constructors, collections)
- **Variable** (`var name`, `final Type name`): bind new variables
- **Wildcard** (`_`, `Type _`): match without binding
- **List**: match by position; `...` or `...rest` for rest elements; map keys throw `StateError` if missing
- **Record**: match by shape; destructure positional and named
- **Object**: `var Foo(:one, :two) = foo;` — destructure via getters; extra fields ignored

## Where to Use Patterns

- Variable declarations: `var (a, [b, c]) = ('str', [1, 2]);`
- Assignments (swap): `(b, a) = (a, b);`
- Loops: `for (final MapEntry(key: k, value: v) in map.entries)`
- `switch`/`if-case`, collection literals

## Records

- Immutable, fixed-size, heterogeneous, strongly typed, structural equality
- Syntax: `('first', a: 2)` — positional + named fields
- Access: positional via `$1`, `$2`; named via identifier
- Named field names are part of the type shape; order irrelevant for equality
- Destructure: `final (:name, :age) = userInfo(json);`
- `typedef` aliases for readability; extension types can wrap records
- Prefer records for simple immutable grouping; classes when abstraction/behavior needed

## Benefits

- Algebraic data types with `sealed` + exhaustive switches
- Declarative validation/destructuring of complex data (JSON)
