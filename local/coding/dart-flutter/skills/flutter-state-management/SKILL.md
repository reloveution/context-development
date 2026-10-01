---
name: flutter-state-management
description: State management for Flutter. Use when choosing patterns, implementing BLoC/Cubit, built-in (Streams, Futures, ValueNotifier), ChangeNotifier, or Provider.
---

# Flutter State Management

## General Rules
- Separate ephemeral (local) and app state
- Keep state immutable; use `copyWith` for updates
- No global variables for state
- Single state management approach per widget
- Serialize state for app lifecycle / restoration

## BLoC
- Trigger changes via events from UI callbacks: `() => bloc.add(FormSubmitted(user))`
- Don't wrap `emit()` in try-catch
- Don't use `setState` inside BLoC
- Don't mix `BlocBuilder` with `setState`

## Cubit
- Interact via public methods: `cubit.loadData()`
- Business logic inside cubit methods; each method emits correct state
- No bloc-style events in cubits

## Built-in (only when explicitly requested)
- `ValueNotifier` + `ValueListenableBuilder` — simple local single-value state
- `StreamBuilder` — async event sequence
- `FutureBuilder` — single async result

## ChangeNotifier (only when explicitly requested)
- Scope `ChangeNotifierProvider` to narrowest consuming subtree
- Private mutable fields, expose getters or unmodifiable views
- `notifyListeners()` after each mutation
- `Consumer<T>` around smallest dependent subtree; unrelated children in `Consumer.child`
- `Provider.of<T>(context, listen: false)` for imperative actions without rebuilds
- `ListenableBuilder` for listening to any `Listenable`
