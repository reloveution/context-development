---
name: dart-code-quality
description: Core code quality rules for Dart/Flutter. Use when formatting, handling async/null safety, organizing classes, or following Dart best practices.
---

# Dart Code Quality

## Logging

- No `print`/`debugPrint` in production; preserve existing `log()` calls
- Use `dart:developer` `log()` for structured logging
- No new comments — only `TODO` in English; no trailing comments
- Document reasons when ignoring linter rules

## Async/Await

- Always `async/await`, never `.then()`
- Pass-through without async: `Future<T> method() => other();`
- No unnecessary `await` in return: `return future;` not `return await future;`
- `unawaited()` for fire-and-forget; never silently discard futures
- `Future<void>` for async methods without return value

## Null Safety

- Avoid `!` — extract nullable to local variable, then use it
- Prefer `?.`, `??`, `??=` over explicit null checks
- `bool?`: use `== true` to distinguish from null

## Style

- **Naming:** PascalCase classes, camelCase members, snake_case files
- **Line length:** 80 chars max
- **Strings:** single quotes; interpolation `$var` over `+`; alt quotes to avoid escapes
- **Formatting:** trailing commas in multi-line; newline at end of file
- Write as short as possible while staying clear

## Control Flow

- Guard clauses: `if (state is! Loaded) return;` to reduce nesting
- No `== true`/`== false` on booleans (exception: `bool?`)
- No empty else/statements; `.isEven` not `% 2 == 0`
- `return value = compute();` — join return with assignment

## Functions

- Arrow functions for single-expression; max ~20 lines per function
- Named params for >2 parameters; required before optional
- No positional boolean params; no redundant argument values
- Extension methods over static methods for utilities
- `typedef F<T> = R Function(T);` for complex signatures

## Variables

- `final` for immutable values; `final` in for-in loops
- Do NOT use `final` for function parameters (`avoid_final_parameters: true`)
- Ternary over mutable if-else: `final val = cond ? y : x;`
- `Type? v;` not `Type? v = null;`

## Types

- No `dynamic` — explicit type annotations; always declare return types
- Class modifiers: `sealed`, `base`, `final`, `interface`, `abstract`, `mixin`
- Pattern matching over `.runtimeType.toString()`
- `void` not `Null`; avoid type names as parameter names

## Collections

- Literals `[]`, `{}` not constructors
- `.isEmpty`/`.isNotEmpty` over `.length == 0`
- `.whereType<T>()` for type filtering; `.contains()` over `.indexOf() != -1`
- Inline in literals; `StringBuffer` for loops
- Cascades `..` when appropriate; `enum.values.byName()` for string-to-enum

## Organization

- Extract methods when nesting >3 levels; no duplication
- No unnecessary overrides, parentheses, raw strings
- No returning null from void; no returning `this` (except builder)
- No setters without getters; no self-assignments

### Class Member Order

1. Static constants → 2. Fields (final → regular) → 3. Constructor → 4. Getters/Setters → 5. Lifecycle → 6. @override → 7. Public methods → 8. Private methods

## Constructors

- `this.field` over body assignments; `super.field` for super params
- `late` for non-null vars initialized after construction
- Asserts in initializer list with messages
- No field initializers in const classes; no unused constructor params

## Constants and Imports

- No magic numbers — use `AppConstants`
- Relative imports for same directory; no imports from package `src`

## Error Handling

- User-friendly messages; never expose technical details
- Specific `on SpecificException catch (e)` — never generic catch
- Never catch `Error`; use `rethrow` not `throw e`
- No control flow in `finally`

## Documentation

- `///` doc comments; first sentence = concise summary; blank line after
- Document public APIs, private when helpful; include code samples
- Explain why, not what; no useless docs restating the obvious

## Tools

- `dart format`, `dart fix`, `build_runner build --delete-conflicting-outputs`

## Testing

- Arrange-Act-Assert; `group()` per class; "should ..." naming
- `package:checks` for assertions; fakes/stubs over mocks
- See **flutter-testing** and **dart-mocktail** skills for details
