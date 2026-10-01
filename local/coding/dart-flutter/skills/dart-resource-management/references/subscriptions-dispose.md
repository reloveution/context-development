---
title: Subscriptions and Dispose
description: Cancel, nullify
---

# Subscriptions and Dispose

## Always Dispose

- Always dispose resources properly.
- Cancel subscriptions, close streams, free memory in dispose methods.

## After Cancelling

- After cancelling subscriptions, always nullify the variable.
- Prevents errors with non-null variables that reference disposed/cancelled subscriptions.
- Example: `_subscription?.cancel(); _subscription = null;`
