---
name: flutter-navigation
description: Routes Flutter screens with go_router or auto_route — deep links and web URLs. Use when adding screens, links, or browser history.
---

# Flutter navigation

Keep the declarative router the app already depends on. Do not add
`go_router` beside `auto_route`, or the reverse. The screen stack, deep
links, and the browser URL belong to that router. `Navigator` is for a
short-lived overlay such as a dialog or sheet.

## URL contract

Put data the URL must restore into path or query parameters. An object
passed beside the URL is gone after a web refresh or a cold link.

Intercept system back with `PopScope`. `WillPopScope` is the retired API.
After an awaited pop, `context.mounted` belongs to `flutter-widget-patterns`.

Generated route files are outputs. Change the router source, regenerate, and
do not hand-edit the generated file. Since auto_route 9 the `Router` class
is not generated: you extend `RootStackRouter`. Version 11 still works that
way.

## Web

Hash URLs need no server rewrite. Path URLs need `usePathUrlStrategy()`
before `runApp` and a host that serves the app for every path.

## Boundaries

`flutter-widget-patterns` owns layout, theming, and `context.mounted`.
`flutter-adaptive-ui` owns wide-layout structure. `dart-dependency-injection`
owns app-wide injection. A route guard stays part of the router.

## Sources

auto_route : <https://pub.dev/packages/auto_route>
go_router: <https://pub.dev/packages/go_router>.
Deep links: <https://docs.flutter.dev/ui/navigation/deep-linking>.
`PopScope`: <https://api.flutter.dev/flutter/widgets/PopScope-class.html>.
