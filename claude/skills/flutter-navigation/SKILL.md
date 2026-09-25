---
name: flutter-navigation
description: Flutter navigation and routing: go_router, auto_route, Navigator 2.0, deep linking, data passing, web URL strategies. Use when implementing screen transitions, routing, deep links, or browser history.
---

# Flutter Navigation

## Approach Selection

**go_router (declarative)** — production default:
- Deep linking (iOS, Android, Web), browser history, URL-based navigation
- Multiple Navigator widgets, shell routes

**auto_route (code-gen declarative)** — alternative for large apps:
- Type-safe arguments generated from annotations, zero string-based parsing
- Built-in per-route DI via `AutoRouteWrapper`, class-based route guards

**Navigator API (imperative)** — limited use:
- Short-lived overlays only: dialogs, bottom sheets, temporary views
- No deep linking, no browser forward button on web

**Named routes** — NOT recommended by Flutter team:
- Can't customize deep link behavior, no browser forward button, always pushes new routes

## Navigation Methods

| go_router | auto_route | Navigator | Purpose |
|---|---|---|---|
| `context.go('/path')` | `context.router.replace(Route())` | — | Replace current route |
| `context.push('/path')` | `context.router.push(Route())` | `Navigator.push()` | Add to stack |
| `context.pop()` | `context.router.maybePop()` | `Navigator.pop()` | Go back |

## Data Between Screens

**go_router — path/query params:**
```dart
// Route: GoRoute(path: '/details/:id', builder: ...)
context.push('/details/123?tab=info');
// Extract: state.pathParameters['id'], state.uri.queryParameters['tab']
```

**go_router — extra data (not in URL, lost on web refresh):**
```dart
context.push('/details', extra: {'key': 'value'});
// Extract: state.extra as Map<String, dynamic>
```

**Navigator — constructor params:**
```dart
Navigator.push(context, MaterialPageRoute(builder: (_) => DetailScreen(item: myItem)));
```

**Return data:**
```dart
final result = await Navigator.push(context, MaterialPageRoute<String>(builder: (_) => SelectionScreen()));
if (!context.mounted) return;
```

## Deep Linking Behavior by Platform

| Platform | Navigator | go_router |
|---|---|---|
| iOS (cold start) | initialRoute "/" then pushRoute | initialRoute "/" then RouteInformationParser |
| Android (cold start) | initialRoute with route | initialRoute with route path |
| iOS/Android (running) | pushRoute called | Route parsed, Navigator configured |
| Web | No browser forward button | Full browser History API |

Platform setup: [deep-linking.md](references/deep-linking.md)

## Web URL Strategy

- **Hash (default):** `example.com/#/path` — no server config
- **Path:** `example.com/path` — call `usePathUrlStrategy()` before `runApp()`, requires SPA rewrite

Server configs and non-root hosting: [web-navigation.md](references/web-navigation.md)

## Navigator 2.0 (Router API)

Underlying declarative API that go_router and auto_route wrap. Direct use rarely justified.

- `RouterDelegate` — builds Navigator based on app state
- `RouteInformationParser` — converts URL to/from app state
- `PopScope` — intercept back navigation (replaced `WillPopScope` in Flutter 3.16+)

Use raw Router API only when routing packages can't express your custom page stack logic.

## References

- [go_router-guide.md](references/go_router-guide.md) — setup, named routes, shell routes, guards, error handling
- [auto_route-guide.md](references/auto_route-guide.md) — setup, type-safe args, route guards, per-route DI, tab navigation
