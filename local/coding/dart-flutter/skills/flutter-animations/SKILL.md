---
name: flutter-animations
description: Guides Flutter motion choices and controller-based animation. Use when adding implicit, explicit, Hero, staggered, or physics-based animation; or when managing an AnimationController or ticker.
---

# Flutter Animations

Choose the smallest animation mechanism that expresses the required behavior:

| Need | Use |
| --- | --- |
| A property changes with widget state | An implicitly animated widget |
| A custom state-driven value | `TweenAnimationBuilder` |
| Imperative start, stop, repeat, reversal, or a simulation | `AnimationController` |
| The same element moves between routes | `Hero` with a stable unique tag |
| One timeline drives phased effects | One controller with `Interval`s |

## State-driven motion

Use an implicitly animated widget when the end state is enough; it owns its
controller. `TweenAnimationBuilder` is the equivalent choice when no
pre-packaged widget exposes the property being interpolated.

## Controlled motion

Create an `AnimationController` only when code needs to control the timeline.
Its owner disposes it at the end of that owner's lifetime. For an awaited
controller operation, use `orCancel` and handle `TickerCanceled` when disposal
or a replacement animation is a normal outcome.

Use a `Tween` to map controller progress to a typed value and
`CurvedAnimation` to change timing. For an animation-driven rebuild, prefer
`AnimatedWidget` for a reusable leaf or `AnimatedBuilder` inside a larger
widget; give `AnimatedBuilder.child` the subtree that does not depend on the
animation.

For a gesture- or simulation-driven value, use `fling` or `animateWith` rather
than inventing a frame timer. An unbounded controller is appropriate only when
the simulation's value is not constrained to the usual controller range.

## Route and phased motion

`Hero` requires a matching tag in both routes and no duplicate tag in the same
route. Derive the tag from stable item identity, not a list index. Route
structure and navigation ownership belong to `flutter-navigation`.

For staggered motion, derive each effect from the same controller and an
`Interval`; define timing from the interaction, rather than fixed "ideal"
durations or curve presets.

## Boundaries

For custom non-essential motion, honor `MediaQuery.disableAnimations`; general
accessibility and semantics belong to `flutter-widget-patterns`. Test pumping
and assertions belong to `flutter-testing`; profiling, repaint boundaries, and
broader build optimization belong to `flutter-performance`.

## Sources

Flutter documentation: <https://docs.flutter.dev/ui/animations/overview>,
<https://api.flutter.dev/flutter/widgets/MediaQueryData/disableAnimations.html>,
and <https://docs.flutter.dev/perf/best-practices>.
