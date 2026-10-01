---
name: flutter-adaptive-ui
description: Build adaptive and responsive Flutter UIs that work beautifully across all platforms and screen sizes. Use when creating Flutter apps that need to adapt layouts based on screen size, support multiple platforms including mobile tablet desktop and web, handle different input devices like touch mouse and keyboard, implement responsive navigation patterns, optimize for large screens and foldables, or use Capability and Policy patterns for platform-specific behavior.
---

# Flutter Adaptive UI

## Core Constraint Rule

**Constraints go down. Sizes go up. Parent sets position.**

- Widget receives constraints from parent, decides its size within those constraints, reports size up
- Widget cannot know or control its own position
- Be specific when defining alignment — if parent lacks info to align, child's size might be ignored

## Constraint Gotchas

- **ConstrainedBox** only adds ADDITIONAL constraints on top of parent's — wrap in `Center` or similar to get loose constraints first
- **UnconstrainedBox** lets child be any size (may cause overflow warning); infinite size throws error
- **OverflowBox** — like UnconstrainedBox but no overflow warnings
- **LimitedBox** only applies limits when given infinite constraints (e.g. inside UnconstrainedBox); ignored inside Center
- **FittedBox** can only scale BOUNDED widgets (non-infinite width/height)
- **Container** without child/size expands to fill constraints; with child, sizes to child
- **Expanded** forces child to fill available space (ignores child's preferred width); **Flexible** allows child to be smaller
- **Loose** constraints: child can be smaller (e.g. Scaffold body); **Tight** constraints: child must match (e.g. SizedBox.expand)

## 3-Step Adaptive Approach

### Step 1: Abstract

Extract shared data from widgets that need adaptability:
- Navigation: shared `Destination` class for both `NavigationBar` and `NavigationRail`
- Dialogs: shared content for fullscreen (mobile) and modal (desktop) variants
- Lists: shared data model for single-column and multi-column layouts

### Step 2: Measure

| Tool | Use When | Returns |
|------|----------|---------|
| `MediaQuery.sizeOf(context)` | App-level layout decisions (top of tree) | App window `Size` in logical pixels |
| `LayoutBuilder` | Widget-specific sizing (local subtree) | Parent's `BoxConstraints` (min/max width/height) |

Use `sizeOf` instead of `MediaQuery.of` — more efficient, only rebuilds on size changes.

### Step 3: Branch

Use window size, never device type:

```dart
final width = MediaQuery.sizeOf(context).width;
if (width >= 840) return DesktopLayout();
if (width >= 600) return TabletLayout();
return MobileLayout();
```

**Breakpoints (Material guidelines):**
- Compact (Mobile): width < 600
- Medium (Tablet): 600 <= width < 840
- Expanded (Desktop): width >= 840

## Design Principles

- **Touch first**: start with touch UI, layer mouse/keyboard as accelerators
- **Platform strengths**: mobile = capture/quick actions; tablet/desktop = organize/manipulate; web = deep linking/sharing
- **Break down widgets**: small `const` widgets improve rebuild performance and testability

## Implementation Rules

- **Never lock orientation** — multi-window, foldables, accessibility all require flexibility
- **Never check device type** (`Platform.isIOS`, `Platform.isAndroid`) for layout — use window size (windows can be resized, split, PiP)
- **Never use OrientationBuilder** for layout — orientation doesn't indicate available space; use `MediaQuery.sizeOf`/`LayoutBuilder` with breakpoints
- **Constrain content width** on large screens — use multi-column layouts with `GridView`/flex, not full-width
- **Support multiple inputs**: keyboard navigation (accessibility), mouse hover (`MouseRegion`), focus management (`FocusNode`), screen readers (`Semantics`)
- **Preserve state** across rotation/resize — use `PageStorageKey` for list scroll position; verify plugins don't lose state on config changes

## Capabilities and Policies

Separate what code *can* do from what it *should* do.

**Capability** (can do) — API existence, OS restrictions, hardware (camera, GPS):
```dart
class Capability {
  bool hasCamera() => Platform.isAndroid || Platform.isIOS;
}
```

**Policy** (should do) — app store guidelines, design preferences, feature flags:
```dart
class Policy {
  // Banned by Apple App Store guidelines
  bool shouldAllowPurchaseClick() => !Platform.isIOS;
}
```

**Why separate:**
- Name methods by intent (`shouldAllowPurchaseClick`), not device (`isIOS`)
- Mock independently in tests — widget tests don't change when policies change
- Easy to update when platforms evolve

**Policy implementation types:**
- **Compile-time**: unlikely to change, high consequence (e.g. payment provider per platform)
- **Runtime**: hardware checks (touch screen, API level)
- **RPC-backed**: incremental feature rollout, decisions that might change

## Examples

### Responsive Navigation

```dart
Widget build(BuildContext context) {
  final width = MediaQuery.sizeOf(context).width;
  return width >= 600
    ? _buildNavigationRailLayout()
    : _buildBottomNavLayout();
}
```

Full example: [responsive_navigation.dart](assets/responsive_navigation.dart)

### Adaptive Grid

```dart
LayoutBuilder(
  builder: (context, constraints) => GridView.extent(
    maxCrossAxisExtent: constraints.maxWidth < 600 ? 150 : 200,
  ),
)
```

### Capability/Policy

Full example: [capability_policy_example.dart](assets/capability_policy_example.dart)
