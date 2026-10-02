---
name: flutter-widget-patterns
description: Fixes Flutter layout, theming, and accessibility. Use when a constraint overflows, a theme token is missing, or a widget needs semantics. Routing is flutter-navigation; wide layouts are flutter-adaptive-ui.
---

# Flutter widget patterns

Screen routes belong to `flutter-navigation`. Window and parent-space layout
belong to `flutter-adaptive-ui`. Long lists, rebuild scope, and `compute()`
belong to `flutter-performance`.

## Composition

Make a widget class when the piece has its own identity. Pass callbacks into
a reusable widget. After an async gap, check `context.mounted` before using
that context. Do not call `setState` or `showDialog` during `build`.

## Constraints

| Failure | Fix |
| --- | --- |
| RenderFlex overflow | Give the loose child a `Flexible` or `Expanded` |
| Vertical viewport unbounded | Give the scroll view a bounded height (`Expanded` or a sized box) |
| InputDecorator unbounded width | Bound the `TextField` the same way |
| RenderBox not laid out | Pass constraints down; do not read size before layout |

One `ScrollController` per scroll view. Detach it before attaching it to
another. An empty gap is a `SizedBox`. A color alone is a `ColoredBox`. A
decoration alone is a `DecoratedBox`.

## Theme

Read colors and type from `Theme.of(context)`. A `Color` literal is
`0xAARRGGBB`; a six-digit web hex is transparent. A custom token is a
`ThemeExtension` with `copyWith` and `lerp`, registered on `ThemeData.extensions`.
State-dependent theme values use `WidgetStateProperty`. Declare a font in
the project and reference that family. Do not add `google_fonts` unless the
project already uses it.

## Accessibility and images

Ordinary text aims at a 4.5:1 contrast ratio. Check the screen with a larger
text scale and with TalkBack or VoiceOver. A control that is not already
described by its text gets a `Semantics` label.

A network image has an error builder so a failed load is visible. Declare
every bundled asset in the pubspec and use that path.

## Sources

Constraints: <https://docs.flutter.dev/ui/layout>.
`ThemeExtension`: <https://api.flutter.dev/flutter/material/ThemeExtension-class.html>.
Contrast: <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>.
