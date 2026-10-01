# Code Organization

## Polymorphism Over Conditionals

When all cases call the same method with the same parameters, use the base interface directly:

```dart
// Bad: redundant switch with casting
IParam _updateParam(IParam param, IParamValue newValue, String changedBy) {
  switch (param.paramType) {
    case ParamType.text:
      final p = param as TextParam;
      return p.copyWith(changeHistory: p.changeHistory.addChange(newValue as TextParamValue, changedBy));
    // ... same for every type
  }
}

// Good: polymorphic
IParam _updateParam(IParam param, IParamValue newValue, String changedBy) =>
    param.copyWith(changeHistory: param.changeHistory.addChange(newValue, changedBy));
```

## Coordination vs Implementation

Main classes coordinate (orchestrate calls, pass data, handle flow). Implementation details (actual logic, transformations) belong in smaller dedicated classes/methods. Extract complex branches into factories or dedicated classes.
