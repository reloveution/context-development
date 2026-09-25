---
name: flutter-widget-patterns
description: Flutter widget patterns. Use when building UI, fixing layout errors, theming, composing widgets, GoRouter, accessibility, or assets.
---

# Flutter Widget Patterns

## Composition & Build

- Create separate widget classes, not widget-returning methods
- Compose smaller widgets; don't extend existing ones
- Extract complex logic from build/onPressed into separate methods
- Pass callbacks (events/controller methods) to reusable widgets, not state managers
- In dialogs/context changes: pass controller methods, not controllers
- Controllers: inject via providers at composition root; access from context in widget tree

## Context & Keys

- Check `context.mounted` before context-dependent operations after async gaps
- `addPostFrameCallback` — extremely rarely, only where truly necessary
- Use keys for widgets that need to maintain state across rebuilds

## Container Replacement

- Empty: `SizedBox.shrink()` / `SizedBox.expand()`
- Color only: `ColoredBox`
- Decoration only: `DecoratedBox`
- Multiple properties: combine specific widgets

## Layout Errors

- **RenderFlex overflowed:** wrap unbounded Row/Column children in Flexible/Expanded
- **Vertical viewport unbounded:** ListView in Column — wrap in Expanded/SizedBox
- **InputDecorator unbounded width:** TextField — wrap in Expanded/SizedBox
- **ScrollController multiple:** one per scroll view; detach before reuse
- **RenderBox not laid out:** add size constraints or wrap in constraint-passing widgets
- Don't call setState/showDialog in build; use callbacks
- Flutter Inspector for constraint chain analysis

## Row/Column & Layout

- **Expanded:** fills remaining main axis space
- **Flexible:** shrinks to fit; don't combine with Expanded in same parent
- **Wrap:** overflow moves to next line
- **SingleChildScrollView:** fixed content larger than viewport
- **ListView/GridView:** always use builder constructor for long lists
- **FittedBox:** scale/fit child within parent
- **LayoutBuilder:** responsive decisions based on available space
- **Stack + Positioned/Align:** precise placement by anchoring to edges
- **OverlayPortal:** dropdowns, tooltips on top of everything

## GoRouter Navigation

- `go_router` for declarative navigation, deep linking, web support
- Configure `redirect` for authentication flows
- Navigator only for short-lived overlays (dialogs, temporary views)
- Setup: `GoRouter(routes: [...])` with `MaterialApp.router(routerConfig: router)`
- Path parameters: `state.pathParameters['id']`

## Theming

- Centralized `ThemeData`; define theme + darkTheme; themeMode for toggle
- `ColorScheme.fromSeed()` for harmonious palettes
- Full 8-digit hex for Flutter colors (AARRGGBB)
- No hardcoded colors — use `Theme.of(context)`

### ThemeExtension

- For custom tokens not in ThemeData
- Extend `ThemeExtension<T>`; implement `copyWith` and `lerp`
- Register in `ThemeData.extensions`; access via `Theme.of(context).extension<T>()!`

### WidgetStateProperty

- `resolveWith` for state-dependent values (pressed, hovered, etc.)
- `WidgetStateProperty.all` when same for all states

### Fonts

- `google_fonts` package; one or two font families
- Use typographic scale: displayLarge, titleLarge, bodyMedium, labelSmall

## Performance

- `ListView.builder` / `SliverList` for long lists (lazy loading)
- `compute()` for CPU-intensive operations to avoid blocking UI thread
- `RepaintBoundary` for expensive custom painters

## Accessibility

- Color contrast >= 4.5:1 for text
- Dynamic text scaling: test with increased system font size
- `Semantics` widget for descriptive labels
- Test with TalkBack (Android) / VoiceOver (iOS)

## Network Images

- `cached_network_image` for network images
- Always include `loadingBuilder` and `errorBuilder`
