---
name: make-skill
description: Creates, edits, reviews or trims agent skills and distills books, articles or docs into them — SKILL.md, description, references, scripts. Use when writing a new skill, changing or cleaning up one, turning sources into a skill, or finding why a skill misfires or costs too much context.
---

A skill earns its place only with what the model lacks and would get wrong
without it: local facts, decisions, gotchas, procedures verified here. Skills
an agent writes from its own knowledge score below no skill at all, while
curated ones score far above it (SkillsBench 1.1). So every rule traces to a
source — the user, a repo file, a live run, a primary doc — never to training
memory.

Where a skill lives and how it is connected — `harness-layout`. Turning
books, articles, docs or a chat into a skill — read
`references/distill.md` first.

## One home per rule

- Needed on every task and not inferable → the stance; needed on demand → the
  skill that owns the topic; a new skill only on the terms of Structure.
- Before writing, search the stances and neighbouring skills for the rule's
  key terms. Found → name the owner instead of restating the rule.
- A repeated deterministic step → a script in the skill's `scripts/`.

## Frontmatter

- `name`: a-z, 0-9 and single hyphens, at most 64, equal to the folder name;
  never a harness's built-in command (`review` is one).
- `description` is all the model sees before it loads the skill:
  - what the skill does and when to use it, in the third person, with the
    trigger words in the first ~100 chars — harnesses cut long catalogs;
  - no workflow summary: the model may act on it and skip the body;
  - exclusions only against a misroute seen in practice;
  - aim at 400 chars or less (the limit is 1024): every session pays for it;
  - a plain value never holds `: ` or ` #` — write `—`, or quote the value.
- A command is a skill the user calls by name: its description ends with "Use
  when the user calls it by name or asks to …"; the text after the name
  arrives as is, with no placeholders. A flag that hides a skill from the
  model only when self-invocation does harm (`harness-layout`).

## Body

- Lead with the outcome and the constraints; give decision rules, not step
  lists. Fixed steps only where deviation breaks something: order-dependent,
  destructive or fragile operations.
- `always`, `never`, `must` only for true invariants, each with its reason:
  current models over-apply bare absolutes.
- Do not prescribe what current models do unasked — double-check, re-verify,
  think step by step: it only adds cost, and a demand to write out reasoning
  may be refused (ask for a short rationale). A check the task itself needs —
  a test, a validator script — stays.
- Keep requirements apart from defaults and examples: in a mixed list the
  model may take an example for a requirement.
- One term per concept; concrete examples; nothing time-bound ("until
  August"); no tutorials, install guides, changelogs or READMEs.
- Harness-neutral text: an action, not a tool name ("search the web"); no
  harness paths, invocation syntax, placeholders or built-in skills; MCP tools
  as `server:tool`. Exceptions: `harness-layout` and vendored upstream text.
- Name other skills, never their paths, and only down the layers: a package
  skill may name core, `common` and its own package; core and `common` never
  name a package skill — a project of another language lacks it.

## Structure

Split inside a skill before splitting it out: a reference costs nothing until
read, while every skill's description is paid in every session — whole in
some harnesses, in others out of a fixed catalog budget that each new entry
cuts for all (`harness-layout`).

- A part gets its own skill only with its own trigger: a task that needs it
  without the rest, or a project that links it without the rest. A skill with
  no trigger, contract or test of its own folds back into its owner; one file
  serving unrelated triggers splits (SkillSeam).
- Over-splitting misroutes: routing accuracy falls about 3 points per
  doubling of the library, and the misses land on look-alike neighbours
  (Scaling Laws of Skills); a task served by 4+ skills gains about half of
  what 2–3 give (+10.1 against +19.0, SkillsBench 1.1). Skills that answer one
  request or always load together merge, their parts becoming references.
- `SKILL.md` holds what every use needs — decision rules, gotchas, exact
  thresholds, output formats: on-demand files helped least where success hung
  on those (SkillJuror). A reference read on every use belongs in the body.
- `SKILL.md` stays short: a standard-length skill beat a comprehensive one
  (+21.5 against +0.7 points, SkillsBench 1.1). The body ceiling — 500 lines
  or ~5000 tokens — is not a target.
- `references/` hold what only some uses need: a subtopic, long examples, a
  checklist, API detail. Each is named in `SKILL.md` with when to read it — an
  unnamed file is never read; one level from `SKILL.md` — a file reached
  through another may be read only in part; one topic per file; past ~100
  lines, a contents list on top.
- `scripts/`: inside the skill dir and called relative to it, never through
  `../`; for another skill's script, name that skill. Say whether to run a
  script or read it. A script handles its own errors and has a test.
- No file named `CLAUDE.md` or `AGENTS.md`, in any letter case, inside a
  skill: harnesses load it as nested instructions.

## Edit or review a skill

1. Read `SKILL.md`, its references and scripts. Search the repo and the
   stances for the skill's name (callers) and for its key terms (overlaps).
2. Judge every block: would the model err without it, is it stated elsewhere,
   is it verified? Then keep, compress, move, merge, split, rename or delete.
   Advice the model follows anyway goes. A verified fact or a user decision
   is moved to its home, never dropped.
3. Change one source. On a rename or delete, search for the name before and
   after; no compatibility copies.
4. A new or kept rule names the failure it prevents — seen in a transcript or
   a run, not imagined.

## Check

- Run `python3 scripts/check_skill.py <skill-dir>...`, the path relative to
  this skill's dir: zero errors, and read every warning.
- By hand: the first ~100 chars of the description carry the triggers; no
  other skill's description answers the same request; after a rename or
  delete, no hit for the old name.
- A new skill or a changed description: one live run of one trigger phrase in
  a harness that loads the skill, from an empty dir outside any repo (probe
  recipes — `harness-layout`). A claim about harness behavior holds only after
  a live run; docs are a hypothesis.
