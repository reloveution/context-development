---
name: flutter-adaptive-ui
description: Guides adaptive Flutter layout from available window or parent space. Use when choosing responsive layout variants, breakpoints, NavigationBar versus NavigationRail, large-screen width, SafeArea, foldables, or separating layout from platform behavior.
---

# Flutter Adaptive UI

Adaptive layout responds to the space a widget actually receives. A device type,
screen orientation, or platform name is not a reliable proxy for that space.

## Measure the right space

- Use `MediaQuery.sizeOf(context)` for a decision about the whole app window.
  Do not cache that size outside `build`; the widget must rebuild when it
  changes.
- Use `LayoutBuilder` for a decision inside a constrained subtree. Its
  `BoxConstraints` describe the space that parent gives that subtree, which can
  differ from the app window.

## Change layout shape, not device identity

- Share the content, destinations, and actions before branching their layout.
  For example, one list of destinations can feed either a `NavigationBar` or a
  `NavigationRail`.
- Choose a breakpoint from the layout's content and available space, not from
  phone/tablet/desktop labels. Material's 600 logical-pixel navigation change
  is a useful starting point, not a universal desktop threshold.
- Do not use `Platform.is...` or portrait locking to select an app layout. Near
  the top of the widget tree, do not use `OrientationBuilder` to switch app
  layouts either. Window size can change through resizing, multi-window,
  picture-in-picture, and folding.
- On wide layouts, set a readable maximum content or item width rather than
  stretching every control across the window.

## Display features and platform behavior

- Wrap content that must not be obscured by a notch, rounded corner, or system
  UI in `SafeArea`; place it around the relevant content rather than assuming
  the whole `Scaffold` needs the same inset.
- A platform or hardware check may select an implementation only when an
  external capability or product policy actually differs. Express that decision
  by intent at its boundary; it does not decide the layout.

## Boundaries

`flutter-widget-patterns` owns ordinary composition, constraint debugging,
accessibility, input controls, and assets. `flutter-navigation` owns routes
and deep links; `flutter-performance` owns rebuild and rendering cost. Use
`flutter-testing` for widget tests of each supported layout variant.

## Sources

Flutter adaptive guidance: <https://docs.flutter.dev/ui/adaptive-responsive/general>,
<https://docs.flutter.dev/ui/adaptive-responsive/best-practices>, and
<https://docs.flutter.dev/ui/adaptive-responsive/safearea-mediaquery>.
