---
name: simple-code
description: Guides code toward readable ownership, direct flow, and only current complexity. Use when writing, modifying, designing, or reviewing code for simplicity.
---

# Simple Code

Cognitive load is limited. Prefer code whose purpose, owner, and effect a
reviewer can follow top to bottom without reconstructing a hypothetical design.

## Build for the current problem

- Start with the shortest direct implementation that satisfies the current
  behavior. Add performance complexity only for an observed constraint, after a
  relevant check preserves behavior.
- Add an abstraction only for a concrete, current pain. Compare it with the
  direct alternative; reject it when that alternative is no harder to read,
  change, or test.
- Two similar blocks are acceptable. Extract a shared shape only after current,
  repeatable use establishes it; symmetry or possible future reuse is not enough.
- Preserve known domain information. Do not weaken a type, contract, or boundary
  merely to make an API look reusable.
- Prefer explicit data flow to hidden framework behavior, implicit fallbacks, or
  layers that obscure a simple operation.

## Keep ownership visible

- Give a function one responsibility and keep behavior near its use. Extract a
  helper only when it names a real step, a new responsibility, or stable reuse.
- Keep UI concerns, domain rules, and data representation in their own layers.
  Crossing a boundary needs a named reason.
- Give every fact, default, cache, file, queue, and mutable state one owner.
  Reference or recompute it elsewhere; do not duplicate it or create two writers.
- Do not expose a mutation action on a read-only or disabled path.
- When variants share an operation, put that operation behind their shared
  contract instead of central type-switches and casts. Use an exhaustive type
  branch when the operation itself truly differs; do not invent a hierarchy just
  to remove a small switch.

## Do not hide incomplete or failing work

- Replace an old path instead of keeping aliases, adapters, stubs, or parallel
  behavior solely for compatibility. If a migration cannot finish, split it at
  a coherent working boundary and record the remaining work with a named TODO.
- Delete dead code, obsolete branches, and commented-out alternatives. Each line
  needs a current job.
- Handle errors explicitly: never silently catch, discard asynchronous failure,
  or substitute a default that hides a fault.
- Verify changed behavior with the relevant formatter, analysis, and tests.

## Decide and review

Before adding complexity, answer: what current pain does it remove; what does
the direct alternative look like; and why is the new form easier to change or
test now? Before retaining a line, answer what breaks if it disappears today.

Flag: speculative interfaces, wrappers, factories, layers, or generic parameters;
weakened domain boundaries; helpers that conceal rather than name a step; two
sources of truth; compatibility paths; swallowed failures; dead code; and
unrelated refactoring in the requested change.

Treat file size and complexity scores as leads for inspection, never universal
gates. A split that adds indirection without a new responsibility is not a
simplification.
