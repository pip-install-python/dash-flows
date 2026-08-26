---
name: report
description: Produce the network-standard end-of-pass report — evidence-first, observed-vs-expected, honest about what was not done. Use when finishing any drop, sync, or fix in this repo.
---

The report is read by an orchestrator who will wire-verify every
claim before acting on it. Write for that reader: evidence beats
narrative, and an accurate "not done" outranks an optimistic "done".

Structure, in order:

1. **What shipped** — commit sha(s) on which branch, pushed or not,
   one line on the shape of the change (files/insertions).

2. **What was verified ON THE WIRE** — paste the artifacts: the
   healthz JSON, status codes per probe, the CI/CD run conclusion
   and what its wait certified, test counts (passed/skipped/failed,
   which environments). Anything you could not reach, say exactly
   why and hand the owner the command that settles it. Never let an
   unverified claim read as verified.

3. **What was deliberately NOT done** — out-of-scope items,
   not-applicable steps (with the evidence they don't apply here),
   and anything you could not perform (PR closures, dashboard or
   env actions) enumerated FOR the owner rather than claimed.

4. **Corrections to the prompt** — where the drop's assumptions
   mismatched this tree, what you did instead, and what the prompt
   should say next time. This section is expected to be non-empty
   sometimes; its absence on a mismatched prompt is a failure of
   this repo's contract, not politeness.

5. **Findings beyond the brief** — defects discovered en route
   (fixed or filed), with enough evidence for independent
   verification. Distinguish template-class findings (every fork
   has this) from this-repo findings; template-class ones are the
   most valuable output a pass can produce.

6. **Open items** — split by who acts: owner (dashboard/env/merge),
   orchestrator (cross-repo), this repo's next pass.

Anti-patterns, all observed in the fleet and all rejected on
receipt: "should work" (test it or mark it unverified); summary
claims without artifacts; green CI presented as deploy proof when
the wait certified a different build; claiming closures you cannot
perform; silently skipping a step instead of reporting why it does
not apply.
