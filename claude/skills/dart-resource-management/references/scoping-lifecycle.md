---
title: Scoping and Lifecycle
description: Resource scoping, app lifecycle
---

# Scoping

- Use proper scoping for resources to avoid memory leaks.
- Scope resources to the widget or scope that owns them.
- Don't store widget-scoped resources in global or long-lived objects.

# App Lifecycle

- Implement proper cleanup in app lifecycle methods.
- **pause** — release heavy resources when app goes to background.
- **resume** — reacquire if needed.
- **dispose** — full cleanup when appropriate.
- Use `WidgetsBindingObserver` for app-level lifecycle.
