# Stance

Read when splitting a stance or adding instructions meant for every task.
Which file each harness loads, and how — `harness-layout`.

## Homes

- Global stance: every project, every task. Only what the model will not
  infer and every project needs. A file several harnesses read stays
  harness-neutral and names no package skill: a project of another language
  lacks it.
- Package skills: a language's rules — style, naming, tooling habits, review
  checklists. They matter only where that language is worked on, so they
  load on demand like any skill. A rule that must hold every time goes to a
  linter or a hook: those act whatever the model decides.
- Project stance: what is true of that project only — its commands,
  toolchain, paths, limits — and the names of the package skills its work
  needs. A pointer in a stance made a harness read a skill it had skipped
  (`harness-layout`).
- A shared project's committed stance works without links into this repo
  (`harness-layout`): what teammates need is written into it as that
  project's own text, not as a synced copy of a package block.

## Anti-patterns

- One language block copied into several project stances: a fix lands in one
  copy, the others keep the old rule.
- One language block included into every project from outside it: no
  include works in every harness, some ask for approval per project, and an
  include cuts no cost — its text loads at start like the rest.
- A rule stated in a stance and in a skill: paid twice once the skill loads.
- A language rule in the global stance: projects of every language pay for
  it.
- Splitting a stance to raise compliance: file size, contradicting files and
  file architecture showed no detectable effect on adherence, while it fell
  as a session went on (arXiv 2605.10039; Claude Code, Sonnet 4.6 and Opus
  4.6). Split for cost and ownership.
