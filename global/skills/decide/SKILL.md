---
name: decide
description: Decides an open choice the user hands back — by evidence, consistency with the repo and project goals — and resumes the interrupted work. Use only when the user delegates the choice — «реши сам», «решай», «на твоё усмотрение», «используй decide», "decide yourself", "your call" — or declines to pick between offered options. Not for questions the user has not handed back.
argument-hint: [which question / extra constraint — optional]
---

# decide — the call is yours

The user cannot or will not choose. **Decide yourself and carry on.**
Handing the question back is allowed only in the extreme; it is close to a
failure of this skill.

**Scope:** the open question(s) put to the user. Text the user adds when
invoking narrows to one of them, or adds a constraint or a comment.

**No live question in the conversation** → say so in one line and decide the
nearest fork in the work in progress; no fork there either → the skill does
not apply, say that and stop. Naming an empty input is not handing the question
back. Inventing a fork so there is something to decide is the worst outcome of
this skill.

## Procedure

1. **Restate** the question in one line, and every live option in one line.
   Drop options already rejected.
   - Both options solve the wrong problem → say it in one line and decide the
     real fork. That is fixing the question, not returning it.
   - Several questions → decide first the one the others depend on. Mark
     dependent decisions explicitly, so you don't ship an incompatible pair.

2. **Classify the question and the cost of being wrong** — they set the depth
   and the source set.
   - *Convention, style, naming* → this repo and its project docs. Somebody
     else's convention is not an argument here.
   - *Behavior of an external system* → official documentation and the sources
     of the installed version.
   - *Architectural fork* → repo + third-party production code + pre-mortem.
   - *Measurable effect* (speed, memory, size, complexity) → a measurement;
     prose is secondary.

3. **Gather evidence. Budget first:** local and reversible → levels 1–3 only,
   no web. Irreversible, contract-changing or spanning a layer → the full
   ladder plus pre-mortem. The cost of deciding never exceeds the cost of being
   wrong.

   1. *Experiment* — run the variants yourself: a micro-test, a twenty-line
      prototype, a benchmark, a static analyzer on two versions of the code,
      a call to the real API. A five-minute check closes the question → run the
      check instead of hunting for text: a run on the installed version does not
      lie, unlike an article about the neighbouring one. Strongest evidence on
      this list.
   2. *Repository* — how the nearest problem is already solved here. Look at the
      project's **reference features**: the newest ones, test-covered, matching
      the current project rules. Not legacy areas, however much of them there
      is. Several modules of one layer, not one file. A convention in force
      beats a theoretical one.
   3. *Project* — the project's instruction files and rules, plans and specs,
      the stated goal of the task the question grew out of.
   4. *Official documentation and primary sources* — specifications, changelogs,
      the source of the library/framework itself. Mandatory for any claim about
      an external system (API, package, tool, version): memory is not a source.
      Access order:
      - Official site or documentation repo via the web tool.
      - Sources of the installed version locally — when the docs disagree with
        the behavior; the truth is in the code of the version this project pins.
   5. *Production code and practice* — for a non-trivial implementation or
      architectural choice, search the web for both established practice and
      documented failure modes; then inspect how mature open-source GitHub
      projects solved the same problem. Start with projects from the adjacent
      domain; if none are close enough, use projects with comparable constraints.
      Prefer maintained, widely used, tested and licensed projects, but treat
      popularity as a discovery signal, not proof. Read the implementation,
      tests, issues, PRs and ADRs — not the README — and distinguish a pattern
      that survived production use from an anti-pattern, workaround or a
      project-specific compromise. Do not transplant their structure unchanged:
      their context is evidence, not our architecture.
   6. *Peer-reviewed publications* — confirmed work in reputable journals and at
      conferences (ICSE, FSE, TSE, EMSE and the like). Apt when the question is
      a measurable engineering effect: complexity, defect density, performance,
      maintenance cost.
   7. *Articles* — strong Medium and Habr material. Lowest weight: good as a
      pointer to a primary source and as confirmation of what you already have,
      never as proof. Take only those with an author, a date and a reproducible
      example; a contradiction with levels 1–6 is resolved against them.

   **After gathering:** put all the material side by side. Evidence carries
   weight by its substance — verifiability, freshness, closeness to our version
   and context — not by its position in this list. Analyse without prejudice.
   Sources contradict each other → that is a line of its own in the output, not
   a side silently chosen.

4. **Skills.** Load `critical-thinking` and apply it; do not restate it here.
   The tie-break this skill adds: on equal evidence the simpler, more local,
   more deletable option wins. Load any other skill the question calls for.

5. **Rank against the goal**, in this order: correctness/safety → consistency
   with the existing code and code style → simplicity → reversibility → effort.
   Breaking an established architectural pattern of the project needs an
   explicit reason; "this is how the reference features do it" is a sufficient
   reason on its own, until something outweighs it.
   - Implement the selected option as a continuation of this project's existing
     design: respect its layer boundaries, public API shape, naming, error and
     state handling, test style and local conventions. An externally validated
     pattern is adapted to these constraints; it does not license an isolated
     second style or architecture.
   - The user named specific features, files or areas as the reference for
     implementation, code style or architecture → that is the priority
     benchmark, it outweighs your own pick of reference features.
   - Work already written in one of the variants is not an argument by itself.
     It enters as effort only, and as an explicit line at that.

6. **Commit to one option.** Weak evidence is not a reason to hand the question
   back: take the cheapest reversible option, say exactly that, and name the
   condition for rolling it back.
   - A valid outcome is a third option, "not now": both branches close doors and
     the second case does not exist yet (YAGNI). Then pick the step that leaves
     both doors open, and name the event that reopens the question.

7. **Return to the interrupted work** and do it per the decision — implement,
   don't re-litigate out loud. Scope grows only if the decision cannot stand
   otherwise; an expensive expansion is stated in chat plainly, not dragged in
   silently as drive-by refactoring.
   - Irreversible or architectural decision → one line next to the task in the
     plan/spec that owns it, so it is not re-decided next session. A local
     reversible decision stays in the chat.

## Hard rules

- A menu of options and "which do you prefer" is the last resort: only when the
  choice rests on an unverifiable personal preference, or on access you do not
  have. The default is one decision.
- No half-measures ("A rather than B, but B would do too"). One option, flat.
- A compromise taken is spoken, not hidden; the price the user pays later is
  named now.
- If the decision contradicts something the user said earlier — say so in one
  line and decide anyway: they delegated.
- Irreversible and outward-facing actions (data loss, push/publish/send): you
  decide the technical question yourself, you still confirm the action itself.
- A source you did not open is not cited. What you read is kept apart from what
  you recalled.

## Output format — before returning to work

```
Decision: <option>
Why: <the single fact that settled it — evidence, not taste>
Source: <source type + the concrete link/path/run> (only what you actually opened)
Conflict: <source against source, and how it was resolved> (line only if there was one)
Rejected: <option> — <one line> (the two strongest at most)
Compromise: <what gets worse>
Roll back if: <the observation that would flip the decision>
```

Then carry on with the work. Five to eight lines; the plan is not retold.

Write the answer in the language of the conversation.
