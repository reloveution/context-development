# go_router Guide

## Setup

```yaml
# pubspec.yaml
dependencies:
  go_router: ^17.0.0
```

```dart
final router = GoRouter(
  routes: [
    GoRoute(path: '/', builder: (context, state) => HomeScreen()),
    GoRoute(path: '/details', builder: (context, state) => DetailsScreen()),
  ],
);

void main() => runApp(MaterialApp.router(routerConfig: router));
```

## Named Routes

```dart
GoRoute(
  name: 'details',
  path: '/details/:id',
  builder: (context, state) => DetailsScreen(id: state.pathParameters['id']!),
);

context.goNamed('details', pathParameters: {'id': '123'});
context.goNamed('details',
  pathParameters: {'id': '123'},
  queryParameters: {'tab': 'info'},
);
```

## Data Passing

**Path params** (mandatory):
```dart
GoRoute(path: '/users/:userId', builder: (context, state) =>
  UserDetailScreen(userId: state.pathParameters['userId']!));

context.push('/users/123');
```

**Query params** (optional):
```dart
GoRoute(path: '/search', builder: (context, state) =>
  SearchScreen(
    query: state.uri.queryParameters['q'],
    page: int.tryParse(state.uri.queryParameters['page'] ?? '1'),
  ));

context.push('/search?q=flutter&page=2');
```

**Extra data** (not in URL, lost on web refresh):
```dart
GoRoute(path: '/details', builder: (context, state) =>
  DetailsScreen(data: state.extra as Map<String, dynamic>?));

context.push('/details', extra: {'key': 'value'});
```

## Shell Routes (Nested Navigation)

```dart
ShellRoute(
  builder: (context, state, child) => Scaffold(
    body: child,
    bottomNavigationBar: BottomNavigationBar(
      items: const [
        BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
        BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Settings'),
      ],
      onTap: (index) => context.go(index == 0 ? '/home' : '/settings'),
    ),
  ),
  routes: [
    GoRoute(path: '/home', builder: (context, state) => HomeScreen()),
    GoRoute(path: '/settings', builder: (context, state) => SettingsScreen()),
  ],
);
```

## Route Guards

```dart
GoRouter(
  redirect: (context, state) {
    final isAuthenticated = checkAuth();
    final isLoggingIn = state.matchedLocation == '/login';
    if (!isAuthenticated && !isLoggingIn) return '/login';
    if (isAuthenticated && isLoggingIn) return '/';
    return null;
  },
  routes: [...],
);
```

## Error Handling

```dart
GoRouter(
  errorBuilder: (context, state) => ErrorScreen(error: state.error),
  routes: [...],
);
```

## Pitfalls

1. Don't use `Navigator.push/pop` for main navigation — only for overlays
2. Check `context.mounted` after async operations before navigating
3. `context.go()` replaces route, `context.push()` adds to stack
4. Path params are mandatory, query params are optional
5. API v7.0.0+: `pathParameters`/`uri.queryParameters` (not `params`/`queryParams`), `matchedLocation` (not `subloc`)
6. Use `ShellRoute` for persistent UI, not nested `GoRoute` with `Navigator`
