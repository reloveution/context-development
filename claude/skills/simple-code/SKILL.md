---
name: simple-code
description: Anti-overengineering and cognitive-load minimization. Use proactively when writing, modifying, designing, or reviewing code, and from the /review flow. Goal — short files, predictable shape, no premature abstractions, no compatibility shims, one source of truth, polymorphism instead of switching on type at the call site. Keeps code "diagonally readable" so a human reviewer can keep up with agent-generated volume.
---

# simple-code

Cognitive load is the budget. Every line, layer, and abstraction spends from it.
The reviewer is the bottleneck, not the writer. Optimize for reading, not for hypothetical "future flexibility".

This skill is the content stance for the answer (what to write) and the lens for review (what to flag). Pair with `critical-thinking` (how to reason) and `dart-code-review` (Dart-specific checklist).

## Mission

- Each file: short, predictable, "diagonally readable" — eyes can scan the shape on one screen.
- Same logic exists in one place; differences only at explicit extension points.
- New abstractions appear only when current, named pain demands them.
- Surprise budget per change: zero.

## Core principles

1. **Direct first.** Solve with the shortest code that works *now*. Optimize only if a real signal forces it.
2. **No abstractions "for the future".** No interface, factory, adapter, wrapper, or generic parameter without concrete pain it removes today.
3. **Concrete types beat generic ones.** Do not widen to `Object`, `dynamic`, `Map<String, Object?>` if a domain type fits.
4. **One responsibility, one level.** Do not split a function into helpers unless the split improves reading. Do not collapse two responsibilities into one function.
5. **No compatibility shims.** No aliases, typedef bridges, dual old/new paths "just to keep it compiling". Prefer an explicit compile error to hidden temporary compatibility.
6. **Explicit over magic.** Direct code beats clever code. If a reader must mentally simulate the framework to understand a line, rewrite it.
7. **Local change, local effect.** Touch the minimal scope needed; do not piggy-back unrelated refactors onto a feature change.
8. **Layer discipline.** UI rules in UI; domain rules in domain; data shape in data. Crossing layers needs an explicit reason.
9. **Callbacks only when there is action.** Read-only / disabled paths must not pass mutation handlers.
10. **One source of truth.** Same fact, same rule, same default — exactly one place. Recompute or reference; never duplicate state.
11. **Duplication beats wrong abstraction.** Two similar blocks are fine until a stable shape emerges. Rule of three before extracting.
12. **Delete over "just in case".** Dead code, old branches, commented-out blocks, defensive checks for impossible states — remove them.
13. **Verifiability is non-optional.** After a change: format, analyzer, the relevant tests. Untested logic is unfinished logic.
14. **Errors over silence.** Empty `catch`, swallowed futures, default fallbacks that hide bugs are forbidden. Handle explicitly or rethrow.
15. **Each line earns its place.** If you cannot say what a line does *for the current task*, it should not be there.
16. **Single writer for shared state.** One owner per cache / file / queue. Reads from cache by default; disk hydration is a separate, named operation.
17. **Locality of behavior.** Keep logic next to where it is used; extract only on real reuse or a new responsibility.

## Build polymorphic; do not switch at the call site

Heterogeneous inputs → homogeneous output through one polymorphic call with an explicit generic upper bound. Do not unfold variants with a `switch` plus casts at the assembly site.

```dart
// Bad — assembly site knows every variant
IParam buildFromTemplate(IParamTemplate t, String creator) {
  final id = const Uuid().v7();
  switch (t.type) {
    case ParamType.text:
      return TextParam.fromTemplate(
        id: id, template: t as TextParamTemplate, creator: creator);
    case ParamType.bool:
      return BoolParam.fromTemplate(
        id: id, template: t as BoolParamTemplate, creator: creator);
    // ... 5+ more branches with casts
  }
}

// Good — variants live in implementations; assembly is one call
final params = templates
    .map((IParamTemplate<IParam> t) => t.createParam(const Uuid().v7(), creator))
    .toList();
```

Variants in implementations. Assembly in one call. The generic upper bound is explicit at the seam. The call site does not learn a new type when a new variant is added.

When behavior **truly** varies by type (different operation, different parameters), pattern matching is correct — exhaustively, on a `sealed` hierarchy.

## Do not over-generalize types or structure

Keep concrete domain types and a direct data flow. No intermediate wrappers, mapping layers, or transformations unless they remove real, repeated pain.

Forbidden signals:
- "for the future", "just in case", "for universality";
- worse readability traded for nominal flexibility;
- simple logic hidden behind extra interfaces / adapters / factories.

Acceptance test: if removing the abstraction makes the code shorter, clearer, and no worse for testing or change — it should not exist.

## Migration purity

- No aliases, typedefs, temporary adapters, no parallel old/new branches "for compatibility".
- Default: no stubs or placeholders. An explicit compile error is preferred over a hidden compatibility layer.
- If the right step is too large for one iteration, leave a visible compile error and a `TODO` marking the unfinished migration point. Visible breakage on plan > silent compatibility that confuses the architecture.

## Anti-patterns to flag in review

- Switch-by-type at the call site when the base interface already exposes the operation.
- Wrapper / adapter / factory created for a single caller.
- Generic `<T>` parameters whose body never branches on `T`.
- Interfaces with one implementation and no real test substitution.
- `dynamic` / `Object?` where a domain type exists.
- Helpers that exist only to give a name to two lines of inline code.
- Defensive null-checks or `try/catch` around values the type system already proves non-null.
- Empty `catch`, swallowed `Future`s, ignored returned `Result<T>`.
- `// removed`, `// kept for compatibility`, commented-out alternative branches.
- Files past ~300 lines, functions past 25 lines, cyclomatic complexity past 10 — split.
- Two similar blocks already extracted into an "abstraction" used by exactly one of them.
- Read-only / disabled UI passing live mutation callbacks.
- Diff that touches files unrelated to the stated task.

## Decision rules

Before adding an abstraction, answer concretely:
1. What pain — observed today, in this codebase — does it remove?
2. What does the code look like without it? Is it really worse, or just less symmetric?
3. Will it be used by ≥2 real callers now, or only "eventually"?
4. Does it improve reading speed for someone unfamiliar with the change?

If you cannot answer 1 and 3 with concrete evidence — do not add it.

Before keeping a line, answer:
1. What breaks if I delete it today?
2. Is the answer covered by a test? If not, why is the line load-bearing?

If both answers are "nothing visible" — delete.

## Reviewer checklist (use during /review)

For every changed file:
- [ ] Reads top-to-bottom on a single screen; no scroll-jumping to follow control flow.
- [ ] One clear responsibility; no embedded second concern.
- [ ] No new abstraction without a today-pain justification.
- [ ] No widening to `dynamic` / `Object?` / overly-generic types.
- [ ] No compatibility aliases / dual paths / "removed" comments.
- [ ] Same logic exists in exactly one place across the diff.
- [ ] Type-switch at call site replaced by polymorphism where the base interface allows.
- [ ] Errors handled explicitly; no silent `catch`, no ignored `Future`.
- [ ] No code that has no current job (dead args, unused fields, extra parameters).
- [ ] Diff scope matches the task — no unrelated edits.

For the change set:
- [ ] Layer boundaries respected (UI / domain / data).
- [ ] Single source of truth preserved or restored.
- [ ] Migration steps are honest — explicit compile errors instead of shims.
- [ ] Tests added or updated for the new behavior; mutation-killable, not just executed.

## Hard rules

- Do not introduce an abstraction whose only justification is "future use".
- Do not create temporary compatibility layers to keep two API generations alive.
- Do not switch on a runtime type in a place where the base interface already exposes the needed operation.
- Do not leave commented-out code or "removed" markers — delete or restore.
- Do not duplicate the same fact in two places; pick one owner.
- Do not silently expand the diff scope beyond the requested task.

## Performance is not over-engineering — but only with evidence

Optimize only against observed pain (profiler, frame drops, scanner, user-visible latency). Behavior understood and preserved first — test before semantics change. Small proven fix > broad rewrite. Big-O catalog/safety: `flutter-performance`. N+1: `dart-data-patterns`. Cyclomatic: `dart-crap-metric`.

## Relation to other skills

- `critical-thinking` — how to reason; this skill — what to write.
- `dart-simplicity`, `dart-design-principles` — Dart-specific narrower views.
- `dart-code-review`, `/review` — checklists; this skill is one of their lenses.
- `dart-crap-metric`, `flutter-coverage-gate`, `dart-mutation-testing` — verifiability backstop.
- `flutter-performance`, `dart-data-patterns` — Big-O audit / N+1.
