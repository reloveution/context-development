---
name: recheck
description: Audits the previous answer after user doubt — «перепроверь», «ты уверен?», “recheck”, “are you sure?” — or a required post-work audit. Not for ordinary clarifying questions.
argument-hint: [what to recheck — optional]
---

# recheck

Audit the **previous assistant answer** in this session, or the fragment the
user names. This is a reactive check: apply it after a signal that the answer
may be wrong, an explicit request, or a workflow that requires a post-work
audit. It does not replace `critical-thinking`, which governs the work before
the answer.

Do not invoke it for an ordinary request to explain, expand, or clarify a
subject. A question mark or a named fact alone is not doubt about a previous
answer.

## Audit

1. State the answer or fragment under review, its load-bearing claims and the
   assumptions that could change its conclusion.
2. Reopen only evidence that can change the verdict. Check external factual
   claims against the appropriate primary source — documentation, a record, or
   the installed artifact; check code and repository claims against the source
   and a safe relevant verification.
   Distinguish verified evidence from an inference or an unchecked point.
3. Report one verdict: **CONFIRMED**, **REFINED**, **PARTIALLY WRONG**, or
   **WRONG**. User doubt is a reason to audit, not evidence to reverse the
   answer: name the sources and checks performed, correct every error plainly,
   and retain unresolved uncertainty rather than manufacturing a reversal.

Keep the report proportional: enough evidence for another person to audit the
verdict, without a ritual phase-by-phase transcript.
