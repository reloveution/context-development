---
name: dart-dependency-injection
description: Defines composition-root, lifetime, and test-isolation decisions for get_it in Dart and Flutter. Use when registering, resolving, scoping, or replacing dependencies.
---

# Dart Dependency Injection

Treat `get_it` as composition infrastructure, not a service locator available
throughout application code. Resolve dependencies while wiring an object, then
pass them through its constructor. A class that calls `getIt` hides its contract
and makes its dependencies harder to test and replace.

## Composition root

- Keep registration and resolution in startup or feature composition modules.
  A factory may resolve its direct dependencies there; business, data, and UI
  classes receive them as constructor arguments.
- Register against the contract the caller needs when implementations may vary.
  The registration must still expose the concrete lifetime and disposal owner.
- A cycle in the registration graph is a design problem. Separate the shared
  responsibility or introduce an explicit mediator; an interface alone does not
  break a runtime dependency cycle.

## Choose a lifetime

- `registerFactory`: each resolution needs a new, short-lived instance.
- `registerSingleton`: one already-created app-lifetime instance is required.
- `registerLazySingleton`: one shared instance is needed, but creation can wait
  until first use.
- For a session, account, or feature lifetime, use a scope rather than silently
  promoting its state to an app singleton. Define how that scope is left.
- A registration that owns a database, controller, subscription, or other
  resource must have a disposal path. Follow `dart-resource-management` for the
  resource itself; `get_it` can invoke a disposal callback or `Disposable` when
  a registration, scope, or container is reset.

## Test isolation

- Prefer constructing the unit under test with fakes or mocks directly.
- If a test exercises the composition root, register only its test dependencies
  and `await getIt.reset()` in teardown so disposal completes before the next
  test.
- Do not use global reassignment as ordinary test setup; it conceals the
  dependency graph and lets registrations leak between tests.
