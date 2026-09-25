---
name: flutter-animations
description: "Comprehensive guide for implementing animations in Flutter. Use when adding motion and visual effects to Flutter apps: implicit animations (AnimatedContainer, AnimatedOpacity, TweenAnimationBuilder), explicit animations (AnimationController, Tween, AnimatedWidget/AnimatedBuilder), hero animations (shared element transitions), staggered animations (sequential/overlapping), and physics-based animations. Includes workflow for choosing the right animation type, implementation patterns, and best practices for performance and user experience."
---

# Flutter Animations

## Decision Tree

| Use When | Type |
|----------|------|
| Single property, state-driven, no fine control | **Implicit** |
| Full lifecycle control, multiple properties, custom transitions | **Explicit** |
| Shared element between screens | **Hero** |
| Sequential/overlapping multiple animations | **Staggered** |
| Natural motion (spring, drag, momentum) | **Physics** |

## Implicit Animations

No controller needed. Change property -> widget animates automatically.

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  width: _expanded ? 200 : 100,
  height: _expanded ? 200 : 100,
  color: _expanded ? Colors.blue : Colors.red,
  child: const FlutterLogo(),
)
```

**Widgets:** `AnimatedOpacity`, `AnimatedPadding`, `AnimatedPositioned` (Stack), `AnimatedAlign`, `AnimatedSwitcher` (cross-fade), `AnimatedDefaultTextStyle`, `AnimatedPhysicalModel`, `AnimatedTheme`

**TweenAnimationBuilder** — custom tween without controller:

```dart
TweenAnimationBuilder<double>(
  tween: Tween<double>(begin: 0, end: 1),
  duration: const Duration(seconds: 1),
  builder: (context, value, child) => Opacity(
    opacity: value,
    child: Transform.scale(scale: value, child: child),
  ),
  child: const FlutterLogo(),
)
```

Common parameters: `duration` (required), `curve`, `onEnd`

Template: [implicit_animation.dart](assets/templates/implicit_animation.dart)

## Explicit Animations

### AnimationController + Tween

```dart
late AnimationController _controller;

@override
void initState() {
  super.initState();
  _controller = AnimationController(
    duration: const Duration(seconds: 2),
    vsync: this,  // SingleTickerProviderStateMixin
  );
}

@override
void dispose() {
  _controller.dispose();  // ALWAYS dispose
  super.dispose();
}
```

Controller methods: `forward()`, `reverse()`, `stop()`, `repeat()`, `animateTo(0.5)`, `reset()`, `fling(velocity:)`, `animateWith(Simulation)`

### Tween + CurvedAnimation

```dart
animation = Tween<double>(begin: 0, end: 300).animate(_controller);

// With curve
animation = CurvedAnimation(parent: _controller, curve: Curves.easeInOut);

// With interval (for staggered)
animation = CurvedAnimation(
  parent: _controller,
  curve: const Interval(0.25, 0.75, curve: Curves.easeInOut),
);
```

**Common Tweens:** `Tween<T>`, `ColorTween`, `RectTween`, `IntTween`, `SizeTween`, `OffsetTween`, `BorderRadiusTween`

### Patterns

**AnimatedWidget** — reusable animated widget, auto-rebuilds:

```dart
class AnimatedLogo extends AnimatedWidget {
  const AnimatedLogo({super.key, required Animation<double> animation})
    : super(listenable: animation);

  @override
  Widget build(BuildContext context) {
    final animation = listenable as Animation<double>;
    return SizedBox(
      height: animation.value,
      width: animation.value,
      child: const FlutterLogo(),
    );
  }
}
```

**AnimatedBuilder** — separates animation from widget (child built once, reused):

```dart
AnimatedBuilder(
  animation: animation,
  builder: (context, child) => SizedBox(
    height: animation.value,
    width: animation.value,
    child: child,  // not rebuilt every frame
  ),
  child: const FlutterLogo(),
)
```

**Multiple properties from single controller:**

```dart
static final _opacityTween = Tween<double>(begin: 0.1, end: 1);
static final _sizeTween = Tween<double>(begin: 0, end: 300);

// In build: _opacityTween.evaluate(animation), _sizeTween.evaluate(animation)
```

### Status Monitoring

```dart
animation.addStatusListener((status) {
  if (status == AnimationStatus.completed) _controller.reverse();
  if (status == AnimationStatus.dismissed) _controller.forward();
});
```

### Built-in Transitions

`FadeTransition`, `ScaleTransition`, `SlideTransition`, `SizeTransition`, `RotationTransition`, `PositionedTransition`, `DecoratedBoxTransition`

```dart
FadeTransition(opacity: _animation, child: const FlutterLogo())
SlideTransition(position: Tween<Offset>(begin: Offset(0, 1), end: Offset.zero).animate(_animation), child: ...)
```

Template: [explicit_animation.dart](assets/templates/explicit_animation.dart)

## Hero Animations

Match `Hero` tags between routes — Flutter animates the transition automatically.

```dart
// Source route
Hero(tag: 'hero-image', child: Image.asset('images/logo.png'))

// Destination route (SAME tag)
Hero(tag: 'hero-image', child: Image.asset('images/logo.png'))
```

### Tags
- Use unique identifiers (data object ID, not index)
- If using object as tag, implement `==` and `hashCode`

### Custom Flight Path

```dart
Hero(
  tag: 'hero-image',
  createRectTween: (begin, end) => MaterialRectCenterArcTween(begin: begin, end: end),
  flightShuttleBuilder: (flightContext, animation, direction, fromContext, toContext) {
    return FadeTransition(opacity: animation, child: child);
  },
  child: Image.asset('image.png'),
)
```

### Radial Hero (circle -> rectangle)

```dart
class RadialExpansion extends StatelessWidget {
  const RadialExpansion({super.key, required this.maxRadius, this.child})
    : clipRectSize = 2.0 * (maxRadius / math.sqrt2);

  final double maxRadius;
  final double clipRectSize;
  final Widget? child;

  @override
  Widget build(BuildContext context) => ClipOval(
    child: Center(child: SizedBox(
      width: clipRectSize, height: clipRectSize,
      child: ClipRect(child: child),
    )),
  );
}
```

### HeroMode

```dart
HeroMode(enabled: false, child: Hero(...))  // disable hero animations
```

### Hero Rules
- Keep widget trees similar between routes
- Wrap images in `Material(color: Colors.transparent)` for ink splash
- No duplicate tags on same route

Template: [hero_transition.dart](assets/templates/hero_transition.dart)

## Staggered Animations

All animations share one `AnimationController`. Each uses `Interval` for timing.

```dart
// Opacity: 0% - 10% of controller duration
opacity = Tween<double>(begin: 0, end: 1).animate(
  CurvedAnimation(parent: controller, curve: const Interval(0.0, 0.1, curve: Curves.ease)),
);

// Width: 12.5% - 25%
width = Tween<double>(begin: 50, end: 150).animate(
  CurvedAnimation(parent: controller, curve: const Interval(0.125, 0.25, curve: Curves.ease)),
);

// Build all with single AnimatedBuilder
AnimatedBuilder(animation: controller, builder: (context, child) {
  return Opacity(opacity: opacity.value, child: Container(width: width.value, ...));
});
```

### Interval Timing

`Interval(0.25, 0.75)` with 2000ms controller = starts at 500ms, ends at 1500ms

### Duration Calculation

```dart
const itemDelay = Duration(milliseconds: 50);
const itemAnimationTime = Duration(milliseconds: 250);
final totalDuration = itemAnimationTime + (itemDelay * (itemCount - 1));
```

### Staggered List (ripple effect)

```dart
for (int i = 0; i < itemCount; i++) {
  animations[i] = Tween<double>(begin: 0, end: 1).animate(
    CurvedAnimation(
      parent: controller,
      curve: Interval(i * 0.1, (i * 0.1) + 0.4, curve: Curves.easeOut),
    ),
  );
}
```

### Repeating

```dart
// Loop
if (status == AnimationStatus.completed) { _controller.reset(); _controller.forward(); }
// Ping-pong
if (status == AnimationStatus.completed) _controller.reverse();
if (status == AnimationStatus.dismissed) _controller.forward();
```

Template: [staggered_animation.dart](assets/templates/staggered_animation.dart)

## Physics-Based Animations

### Fling

```dart
_controller.fling(velocity: 2.0);

// From gesture
void _handlePanEnd(DragEndDetails details) {
  _controller.fling(velocity: details.velocity.pixelsPerSecond.dx / 1000);
}
```

Use `AnimationController.unbounded(vsync: this)` for physics that exceed 0-1 range.

### Spring

```dart
_controller.animateWith(SpringSimulation(
  spring: const SpringDescription(mass: 1, stiffness: 200, damping: 10),
  start: 0.0, end: 1.0, velocity: 0.0,
));
```

**SpringDescription parameters:**
- `mass` (0.5-5.0): higher = more inertia, slower response
- `stiffness` (100-500): higher = faster oscillation
- `damping` (5-20): higher = less bounce; critical ~15-18

**Presets:**
- Bouncy: mass 0.5, stiffness 300, damping 8
- Snappy: mass 1.0, stiffness 400, damping 18
- Gentle: mass 2.0, stiffness 150, damping 20

### Gravity

```dart
_controller.animateWith(GravitySimulation(acceleration: 980, distance: 500, startDistance: 0));
```

### Custom Simulation

```dart
class CustomSimulation extends Simulation {
  @override
  double x(double time) => target * (1 - math.exp(-time / 0.5));
  @override
  double dx(double time) => target * math.exp(-time / 0.5) / 0.5;
  @override
  bool isDone(double time) => dx(time).abs() < 0.01;
}
```

## Curves Reference

| Animation Type | Recommended Curve |
|---------------|-------------------|
| Fade in/out | `easeInOut` |
| Size change | `easeOut` |
| Position slide | `easeInOut` |
| Color change | `linear` |
| Scale (playful) | `elasticOut` |
| Reveal | `backOut` |
| Loading spinner | `linear` |
| Success | `elasticOut` |

**Families:** ease (easeIn/Out/InOut), cubic (easeInCubic/OutCubic/InOutCubic), elastic (elasticIn/Out/InOut), bounce (bounceIn/Out/InOut), back (backIn/Out/InOut), decelerate, fastOutSlowIn

**Custom curve:**

```dart
class ShakeCurve extends Curve {
  @override
  double transform(double t) => sin(t * pi * 2);
}
```

## Best Practices

- Always dispose `AnimationController` in `dispose()`
- Use `AnimatedBuilder`/`AnimatedWidget` instead of `setState()` in listeners
- Use `timeDilation = 10.0` to debug animations (slow 10x)
- Respect `MediaQuery.disableAnimations` for accessibility
- Typical duration: 200-500ms; avoid > 1s without reason
- Prefer implicit for simple cases, explicit for complex
- Use `RepaintBoundary` around animated children to isolate repaints
- Avoid heavy widget trees inside animation builders
- Support reverse animations for intuitive feel
- Use static Tweens to avoid recreation per frame
