# Widget Testing Reference

## Orientation Testing

```dart
testWidgets('landscape layout', (tester) async {
  await tester.binding.setSurfaceSize(const Size(800, 400));
  await tester.pumpWidget(const MyApp());
  expect(find.byType(Row), findsOneWidget);
  addTearDown(tester.binding.setSurfaceSize(null));
});
```

## Form Validation

```dart
testWidgets('validates email', (tester) async {
  await tester.pumpWidget(MaterialApp(home: Scaffold(body: Form(
    child: TextFormField(
      key: const Key('email'),
      validator: (v) => v != null && v.contains('@') ? null : 'Invalid email',
    ),
  ))));

  await tester.enterText(find.byKey(const Key('email')), 'invalid');
  await tester.pump();
  expect(find.text('Invalid email'), findsOneWidget);

  await tester.enterText(find.byKey(const Key('email')), 'test@example.com');
  await tester.pump();
  expect(find.text('Invalid email'), findsNothing);
});
```

## Accessibility

```dart
final semantics = tester.getSemantics(find.byType(ElevatedButton));
expect(semantics.label, 'Submit button');
expect(semantics.hasAction(SemanticsAction.tap), true);
```

## Animation Testing

```dart
await tester.tap(finder);
await tester.pump();                               // start
await tester.pump(const Duration(milliseconds: 100)); // mid-frame
await tester.pumpAndSettle();                       // complete

final opacity = tester.widget<Opacity>(find.byType(Opacity));
expect(opacity.opacity, 0.0);
```

## Debugging

```dart
debugDumpApp(); // print full widget tree
```
