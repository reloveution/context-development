---
name: gogogo
description: Starts or resumes work on this repo's plan.md — reads the plan work rules, the plan and the harness map, reports state, proposes the next item. Use when the user calls it by name or asks to start or resume work on the plan.
argument-hint: [item number]
---

Read and internalize the plan work rules and the referenced documents:

1. **Rules**: read `plan-work-rules.md` — memorize all principles, plan rules, execution standards and the post-item audit.
2. **Plan**: read `plan.md` — the full item list, order, dependencies («вход для п.N»), current progress.
3. **Harness map**: read `global/skills/harness-layout/SKILL.md` — where config lives in the harnesses, how to connect and edit it; open its `references/` as the item needs.

After reading all three documents:

1. **Confirm understanding** — briefly list the key rules you will follow (2-3 sentences).
2. **Report current state** — which items are done, which are in progress (open subitems), and which were moved after their blocker.
3. **Propose starting point** — find the first uncompleted item (`[ ]`) in `plan.md` in file order (a blocked item is moved right after its blocker and keeps its number), for an item with subitems take its first open subitem in file order, state its number and description, and propose to begin work from there. If the user added an item number after the skill name, start from it instead.

The «Исполнение» and «Аудит после пункта» sections of `plan-work-rules.md` bind every item taken from the plan.

Write the response in the same language the user has been using in this conversation.
