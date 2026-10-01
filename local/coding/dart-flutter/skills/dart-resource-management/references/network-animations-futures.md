---
title: Network, Animations, Futures
description: Request cancellation, controllers, pending ops
---

# Network

- Implement proper network request cancellation when widgets are disposed.
- Cancel in-flight HTTP requests, WebSocket connections.
- Use `CancelToken` (dio) or similar when available.

# Animations and Tickers

- Dispose animation controllers and tickers in dispose methods.
- Call `controller.dispose()`; never leave them running after widget removal.

# Pending Futures

- Cancel pending futures and operations when widgets are disposed.
- Check `mounted` before calling `setState` or using context after async gaps.
- Avoid completing work for disposed widgets.
