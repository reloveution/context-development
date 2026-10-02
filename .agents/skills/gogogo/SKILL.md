---
name: gogogo
description: Continues this repository's plan — reports its state and selects the next open item. Use when the user calls it by name or asks to start or resume plan work.
argument-hint: "[item number]"
---

Choose the next plan item without changing it or beginning its work. Read:

1. `plan-work-rules.md` for the governing rules.
2. `plan.md` for order, dependencies and status.
3. `harness-layout`; read its references only when the selected item needs their
   architecture, connection or harness-specific facts.

Report briefly:

1. Confirm understanding in 2–3 sentences, including the rules that constrain
   this step.
2. Closed items, open work and postponed items relevant to the next choice.
3. The first uncompleted item (`[ ]`) in file order; for a parent with subitems,
   choose its first open subitem. State its number and description. If the user
   supplied an item number, choose it instead.

Stop for the user's manual review. The selected item's work follows the
execution and post-item audit sections of `plan-work-rules.md`.

Write the response in the same language the user has been using in this conversation.
