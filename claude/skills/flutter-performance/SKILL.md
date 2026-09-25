---
name: flutter-performance
description: Performance optimization for Flutter apps. Use when optimizing lists, build methods, const/keys, images, RepaintBoundary, isolates, or profiling with DevTools.
---

# Flutter Performance

## Lists
- `ListView.builder` / `GridView.builder` / `SliverList` for large lists — never `Column`/`Row` with many children
- `const` constructors for list item widgets
- Pagination: load in chunks, combine with builder
- Lazy loading: load on demand (scroll/visibility)

## Build Methods
- No expensive work in `build()` — move to `initState`, `didChangeDependencies`, or cached values
- Scope rebuilds: `Builder`, `ValueListenableBuilder`, `StreamBuilder`, `BlocBuilder`
- Extract frequently rebuilt subtrees into separate widget classes

## Const & Keys
- `const` constructors for static widgets — reused across rebuilds
- Keys for widgets that maintain identity across reorders: `ValueKey`, `ObjectKey`, `UniqueKey`

## Images
- `Image.asset` — cached automatically
- Network images: `cached_network_image` package
- Don't reload same image on every rebuild

## RepaintBoundary
- Wrap complex custom painters — isolates repaint region from siblings/parent
- Adds a compositing layer; profile before/after to validate benefit

## Isolates
- `compute()` for CPU-intensive work: JSON parsing, image processing, batch transforms
- Function and argument must be top-level or static (isolate can't share references)

## Data Structures
- Right structure for the job: List vs Set vs Map, growable vs fixed
- Prefer O(1)/O(log n) over O(n) at scale
- Cache expensive computations when inputs don't change

## Profiling
- Flutter DevTools: Timeline, CPU profiler, memory view
- Identify: build time, layout, paint, rasterize bottlenecks
- Profile before/after optimizations and periodically during development

## Big-O Audit

Data-flow hot spots; separate from cyclomatic (skill `dart-crap-metric`).

**Rule.** Optimize only when behavior is understood and preserved. Small proven fix > broad rewrite. Tests before semantics change.

**On "analyze/audit/scan/report"** — structured report, no file edits unless user asks to implement/fix/refactor. Read the flagged function before listing it; estimate before→after from code, not the raw match. Report = scope · stack · findings (`file:line`, current pattern, complexity before→after, why-equivalent, risk, tests) · patch status: proposed/implemented/blocked · `files modified: yes/no`.

**Transformations:**
- Nested lookup loops: `O(a·b) → O(a+b)` — Map/Set index of B once; on dup keys keep first/last/all-match
- Membership in loop (`.contains`/`.indexOf`/`.firstWhere`): `O(n·m) → O(n+m)` — `Set` once before loop
- Sort in loop: `O(n²·log n) → O(n·log n)` — sort once outside · heap · binary; only if comparator has no loop-local state
- Pairwise: `O(n²) → O(n·log n)` — sort+two pointers · sweep line · spatial hash · union-find
- Derivation in `build()`: per-rebuild → once — Bloc state · memo selector · `ListView.builder`; memo deps = every semantic input, no hidden in-place mutation
- N+1 I/O (call in loop): N → 1 — bulk · joined Drift · preload — preserve auth/tenant/order/page/retry

**Safety before:** size matters · ordering preserved · identity not public · cache invalidation valid · dedup keeps distinct · batching preserves auth/tenant/soft-delete/page/sort.

**Safety after:** narrow test → analyzer/build · micro-bench on hot path · localized patch.

**Don't:** complex for tiny input · cache w/o invalidation · JSON-as-key · break public ordering · `O(n) → O(n·log n)` without removing larger bottleneck.

**Scanner:** `python3 ~/.claude/skills/flutter-performance/scripts/analyze_complexity.py . --format markdown` — Dart-aware first pass; leads, not proof. Reports nothing → inspect hot paths, `build()`, repo/Drift/HTTP loops by hand.
