# auto_route Guide

## Setup

```yaml
# pubspec.yaml
dependencies:
  auto_route: ^9.0.0
dev_dependencies:
  auto_route_generator: ^9.0.0
  build_runner:
```

```dart
@RoutePage()
class HomePage extends StatelessWidget { ... }

@AutoRouterConfig()
class AppRouter extends RootStackRouter {
  @override
  List<AutoRoute> get routes => [
    AutoRoute(page: HomeRoute.page, initial: true),
    AutoRoute(page: DetailsRoute.page),
  ];
}

void main() {
  final router = AppRouter();
  runApp(MaterialApp.router(routerConfig: router.config()));
}
```

Run `dart run build_runner build` after adding/changing `@RoutePage()` annotations.

## Type-Safe Data Passing

Arguments are generated from page constructor params — no string parsing:
```dart
@RoutePage()
class DetailsPage extends StatelessWidget {
  const DetailsPage({required this.itemId, this.tab});
  final String itemId;
  final String? tab;
}

// Navigation — fully typed, compile-time checked
context.router.push(DetailsRoute(itemId: '123', tab: 'info'));
```

Path/query params for deep linking:
```dart
AutoRoute(
  page: DetailsRoute.page,
  path: '/details/:itemId', // itemId extracted from URL automatically
);
```

## Tab Navigation (AutoTabsRouter)

Cleaner than ShellRoute — manages tab index, preserves state:
```dart
@RoutePage()
class DashboardPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) => AutoTabsRouter(
    routes: const [HomeRoute(), SettingsRoute()],
    builder: (context, child) => Scaffold(
      body: child,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: context.tabsRouter.activeIndex,
        onTap: context.tabsRouter.setActiveIndex,
        items: const [...],
      ),
    ),
  );
}
```

Advanced tab options:
- `lazyLoad: false` — build all tabs immediately
- `keepHistory: true` — preserve navigation stack per tab

## Route Guards

Class-based, composable, support async checks and redirect-with-callback:
```dart
class AuthGuard extends AutoRouteGuard {
  @override
  void onNavigation(NavigationResolver resolver, StackRouter router) {
    if (isAuthenticated) {
      resolver.next();
    } else {
      resolver.redirect(
        LoginRoute(onResult: (success) {
          if (success) resolver.next();
        }),
      );
    }
  }
}

// Register globally
@override
List<AutoRouteGuard> get guards => [AuthGuard()];
```

Per-route guard: `AutoRoute(page: AdminRoute.page, guards: [AdminGuard()])`.

## Per-Route DI (AutoRouteWrapper)

Inject BLoC/providers scoped to a specific route:
```dart
@RoutePage()
class ProfilePage extends StatelessWidget implements AutoRouteWrapper {
  @override
  Widget wrappedRoute(BuildContext context) => BlocProvider(
    create: (_) => getIt<ProfileBloc>(),
    child: this,
  );
}
```

## Custom Transitions

```dart
CustomRoute(
  page: FadeRoute.page,
  transitionsBuilder: TransitionsBuilders.fadeIn,
  durationInMilliseconds: 300,
);
```

Built-in: `fadeIn`, `slideBottom`, `slideLeft`, `slideRight`, `slideTop`, `noTransition`.

## Stack Manipulation

```dart
// Push and remove everything until predicate
context.router.pushAndPopUntil(HomeRoute(), predicate: (r) => false);

// Replace entire stack
context.router.replaceAll([HomeRoute(), DetailsRoute(itemId: '1')]);

// Navigate to nested route preserving parent stack
context.router.navigate(DashboardRoute(children: [SettingsRoute()]));
```

## Deep Linking

Works automatically when routes have `path:` defined. Same platform config as go_router (see [deep-linking.md](deep-linking.md)).

## Pitfalls

1. Run `build_runner` after any `@RoutePage()` change — stale generated code causes runtime errors
2. `maybePop()` over `pop()` — respects `PopScope` and route guards, returns `false` if can't pop
3. Don't mix `Navigator.push/pop` with auto_route for main navigation
4. `context.router` returns nearest `StackRouter`; use `context.tabsRouter` inside tabs
5. Route names are generated as `{PageName}Route` — `HomePage` becomes `HomeRoute`
6. For web: define `path:` on every route, otherwise URLs won't update
