---
title: Timer Usage
description: Timer vs Future.delayed, cancellation
---

# Timer Usage

## Prefer Timer Over Future.delayed

- Use `Timer` instead of `Future.delayed` when cancellation is needed.
- `Future.delayed` cannot be cancelled; Timer can via `timer.cancel()`.
- Critical for delayed work that may become irrelevant when widget is disposed.

## Cancellation Requirements

- Timer must be nullable.
- Cancel before creating new instances (avoid duplicate timers).
- Cancel in cleanup methods (dispose, close).
- Nullify the variable after cancelling to satisfy non-null analysis.
