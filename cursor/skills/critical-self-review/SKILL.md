---
name: critical-self-review
description: Deep critical self-review of the previous assistant answer. Activates when the user signals doubt about the prior answer or explicitly asks to recheck. Triggers (RU/EN, case/punctuation insensitive) — "перепроверь себя", "перепроверь", "ты уверен?", "уверен?", "проанализируй глубже", "точно?", "ты точно прав?", "а если ты ошибся?", "проверь ещё раз", "ещё раз проверь", "critical review", "self-review", "double-check", "double check", "are you sure?", "recheck", "check yourself". Do NOT activate on ordinary clarifying questions about content — only on signals of distrust toward the answer's correctness.
---

# critical-self-review

Honest, multi-layer audit of the **previous assistant answer** in this session. Goal: catch errors, hasty conclusions, unverified assumptions — not a cosmetic reread.

**Proactive counterpart:** `critical-thinking` — applied *during* reasoning, not after. If `critical-thinking` was in force, this audit should rarely flip the verdict; if it does, the prior answer skipped the discipline. Apply the `critical-thinking` stance (evidence vs inference, ≥2 hypotheses, pre-mortem, no sycophancy) inside each phase below.

## When to apply
Activate automatically on user-doubt phrases (see triggers in `description`). If doubt targets a specific fragment — focus on it; otherwise take the whole last assistant answer.

Do not apply to ordinary clarifying questions ("how does X work?", "tell me more") — no distrust signal there.

## Protocol (strict order)

### Phase 1. Reconstruct your reasoning
- List **factual claims** in the original answer.
- List **conclusions**.
- List **implicit assumptions** (taken for granted, unverified).
- Name the step where a hidden logical jump could sit.

### Phase 2. Red-team yourself
For each key claim:
- How do I know — training memory or verified now?
- What's the opposite interpretation of the context? What if it's right?
- What source/context did I skip though I could check?
- What would an expert wince at?
- Alternative hypothesis explaining the same facts differently?
- Am I conflating **syntax/form** with **semantics/effect**?
- Am I conflating the author's **intent** with a **side effect** under misuse?

**Mandatory: at least two alternative hypotheses**, even if the first seems obvious.

### Phase 3. Verification (mandatory)
- Factual claims about the external world (products, APIs, commands, system behavior) → **WebSearch/WebFetch required**. Memory is not a source.
- Code/script → read in full, dry-run mentally, execute safely if possible (`--dry-run`, isolated).
- File/repo/library → find the **primary source**, not retellings.
- Numbers, versions, dates → direct reference.

### Phase 4. Context that changes interpretation
- Who authored the artifact? Does that change anything?
- What environment runs it? Does environment alter behavior?
- Adjacent files, README, comments — what was ignored?
- Can the same artifact produce different effects in different contexts?

### Phase 5. Honest verdict (no softening)
1. **CONFIRMED** — correct; list **what** was checked and with **which** sources/actions.
2. **REFINED** — broadly correct, but inaccuracies / missing context. List them.
3. **PARTIALLY WRONG** — some conclusions wrong. Specify which and why.
4. **WRONG** — main conclusion wrong. Explain the reasoning error, give a new answer.

## Hard rules

- No defending the original answer out of inertia. Found an error → admit it plainly, no "technically I was right, but...".
- No surface rereads. At least one web search if the answer made factual claims about the external world.
- No CONFIRMED verdict without explicit list of checks and sources.
- At least one alternative hypothesis always; two in Phase 2.
- Distinguish "I verified" from "this seems plausible".
- If context contains a source artifact (code, script, link) — locate its primary source and creation context.
- Tone: dry, technical, ruthless toward own errors. No emoji, no flourishes.

## Output format (strict)

```
## Self-review

### Phase 1: What I claimed
- Claim 1: ...
- Claim 2: ...
- Hidden assumption: ...

### Phase 2: Attack
- Alternative hypothesis 1: ...
- Alternative hypothesis 2: ...
- What I did NOT check: ...
- Where the logical jump could be: ...

### Phase 3: What I verified now
- [tool] → [finding]
- [tool] → [finding]

### Phase 4: Context I missed (or confirmed)
- ...

### Verdict: [CONFIRMED / REFINED / PARTIALLY WRONG / WRONG]
[If not CONFIRMED — corrected answer]
```
