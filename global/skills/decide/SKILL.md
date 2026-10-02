---
name: decide
description: Decides a choice the user hands back — «реши сам», «на твоё усмотрение», "your call", or a refusal to pick — and resumes the interrupted work; not for requests for advice. Use when the user calls it by name or delegates a choice.
argument-hint: [which question / extra constraint — optional]
---

# decide — the call is yours

The user handed the choice over: **decide and carry on.** A menu or "which do
you prefer" only when the choice rests on a personal preference nothing can
verify, or on access you lack.

**Scope:** the question(s) put to the user; text added on the call narrows to
one of them or adds a constraint. Delegated ahead («дальше решай сам») → the
forks of the current task; a new task needs a new delegation. A request for
advice ("what is better?") is not delegation: recommend and wait. No open
question → say so in one line, decide the pending fork of the current task if
there is one, otherwise stop. Never invent a fork to have something to decide.

## Procedure

1. **Restate** the question and each live option in one line; drop rejected
   ones. Both options solve the wrong problem → decide the real fork: fixing
   the question is not returning it. Several questions → first the one the
   others depend on; mark the dependent decisions.
2. **Classify — it picks the sources:** convention, style or naming → this
   repo, never someone else's convention; external system → its docs and the
   installed version's source; architectural fork → repo, production code and
   a pre-mortem; measurable effect → a measurement.
3. **Budget by the cost of being wrong:** local and reversible → levels 1–3,
   no web; irreversible, contract-changing or cross-layer → every level plus a
   pre-mortem. Deciding never costs more than being wrong.
   1. *Experiment* — a micro-test, prototype, benchmark, analyzer run on both
      versions or a real call, on the installed version. The strongest: when a
      short check settles it, run it instead of reading.
   2. *Repository* — the project's reference features: newest, tested, under
      the current rules, several modules of a layer, not legacy.
   3. *Project* — instruction files, plans, specs, the goal of the task.
   4. *Primary sources* — specs, changelogs, the library's source; the
      installed version's code wins when the docs disagree.
   5. *Production code* — practice and its documented failure modes, then
      mature projects solving the same problem: code, tests, issues, PRs, not
      the README. Popularity finds, it does not prove; tell a pattern that
      survived production from a workaround. Their context is evidence, not
      our architecture.
   6. *Peer-reviewed work* — for measurable engineering effects.
   7. *Articles* — only with an author, a date and a reproducible example; a
      pointer to a primary source, never proof, and they lose to levels 1–6.

   Weigh evidence by substance — verifiability, freshness, closeness to our
   version — not by level. Sources that disagree get their own output line.
4. **Rank:** correctness/safety → consistency with the project → simplicity →
   reversibility → effort. Equal evidence → the simpler, more local, more
   deletable option. Breaking a project pattern needs a stated reason;
   references the user named outrank your own pick. Work already written
   counts only as effort, on its own line.
5. **Commit to one option**, without "B would do too". Weak evidence → the
   cheapest reversible option, said so, with the condition for rolling it
   back. Both branches close doors and the second case does not exist yet →
   "not now": the step that keeps both open, and the event that reopens it.
6. **Return to the work** and implement — no re-litigating. Scope grows only
   when the decision cannot stand otherwise, and that is said in chat.
   Irreversible or architectural decision → one line next to the task in the
   plan or spec that owns it.

## Limits

- An earlier user constraint still binds; an earlier lean on this very
  question does not — name the contradiction in one line.
- Choosing is delegated, acting is not: irreversible and outward-facing steps
  (data loss, push, publish, send) are still confirmed.

## Output — before returning to work

```
Decision: <option>
Why: <the single fact that settled it — evidence, not taste>
Source: <source type + the concrete link/path/run> (only what you actually opened)
Conflict: <source against source, and how it was resolved> (line only if there was one)
Rejected: <option> — <one line> (the two strongest at most)
Compromise: <what gets worse>
Roll back if: <the observation that would flip the decision>
```

Five to eight lines, the plan not retold; then carry on. Write in the language
of the conversation.
