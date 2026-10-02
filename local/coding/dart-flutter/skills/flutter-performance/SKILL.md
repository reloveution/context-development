---
name: flutter-performance
description: Guides Flutter performance for a profiled frame, a hot path, or a complexity audit. Use when a frame janks, a list or data loop is expensive, or when reading analyze_complexity findings.
---

# Flutter performance

## Dispatch

**normal** — Leave the smallest clear implementation. A style preference, a folder name, or a scanner hit is not a reason to change it.

**critical-path** — Only with a stated hot loop, a profile, or a demonstrated heavy list or data workload. Preserve behavior, name the evidence, then apply one change and check it. Missing evidence means report the candidate and do not edit.

Already the simple path: do not repeat a costly derivation in `build()`, and a mostly off-screen list uses a builder rather than a column of every child.

## Profiler

Use a profile build. Debug frame times are not release times. Mobile and desktop use the DevTools Performance view. Web timeline events go to Chrome DevTools, not that Flutter view.

Each frame is two bars: UI (Dart, `build`, the layer tree) and raster (GPU). Over about 16 ms at 60 Hz is jank, marked red. Dark red is shader compilation. Select the frame. Frame analysis names the expensive work. A slow UI bar goes to the CPU profiler. A slow raster bar is still caused by the Dart scene (`saveLayer`, overlapping opacity, clips, shadows). Turn on Track widget builds, Track layouts, or Track paints only for the phase you are chasing. Those options slow frames. The memory view answers retained size, not jank.

## Changes

Apply only on the critical path, or when the user asked to act on a scanner finding. Read the function. The scanner line is a lead.

- Rebuild the widget that depends on the change, not its ancestors. `const` and keys only when identity across rebuilds is the measured problem. Mechanical `const` is the linter. `RepaintBoundary` only after a paint profile, then profile again: it adds a layer.
- `compute()` for CPU work whose function and arguments are top-level or static. Do not send a Drift database (`flutter-drift`). Cyclomatic cost is `dart-crap-metric`.
- Nested lookup: one `Map` or `Set`. Duplicate keys keep the existing rule (first, last, or all). Membership in a loop (`.contains`, `.indexOf`, `.firstWhere`): that `Set` is built once before the loop.
- Sort in a loop: once outside, or a heap or binary search, only if the comparator has no loop-local state. Pairwise: sort and two pointers, a sweep, a spatial hash, or union-find.
- A `build()` derivation is computed once. Memo dependencies are every semantic input, with no hidden in-place mutation.
- N+1: one bulk, joined, or preloaded call. Keep auth, tenant, order, page, and retry. Query shape stays with `dart-drift` or `flutter-networking`.

Skip the edit when the input is tiny, public order or identity would change, the cache has no invalidation, dedup would drop distinct items, a batch would drop auth, tenant, soft-delete, page, or sort, JSON would become a map key, or `O(n)` would become `O(n log n)` while a larger bottleneck remains. After an edit: a narrow test, then the analyzer. A micro-benchmark only on the hot path.

## Audit

On "analyze", "audit", "scan", or "report", do not edit unless the user also asks to implement. Report scope, stack, findings (`file:line`, pattern, complexity before and after, why equivalent, risk, tests), status `proposed`, `implemented`, or `blocked`, and `files modified: yes` or `no`.

Run `python3 scripts/analyze_complexity.py . --format markdown` from the project root. The path is relative to this skill. An empty report is not proof: inspect `build()` and repository, Drift, and HTTP loops by hand.

## Sources

Dispatch: coding-skill dispatch, user decision 2026-10-02. <https://docs.flutter.dev/perf/best-practices> and <https://docs.flutter.dev/tools/devtools/performance>.
