---
title: Stream Controllers
description: Close in dispose
---

# Stream Controllers

## Close Properly

- Use proper stream controllers and close them in dispose methods.
- Call `controller.close()` when the controller is no longer needed.
- Prevents lingering subscriptions and memory leaks.

## When

- StatefulWidget dispose
- Service/repository close methods
- When the stream's lifetime is tied to a scope
