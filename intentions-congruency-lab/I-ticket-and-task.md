# ticket-and-task

*concept-piece · ticket 6a657e22db6f · owning intention: intentions-not-beside-code/_charter+why.json*

## Intention

Every workflow instance is flagged, at /intent, as a TICKET or a TASK. A ticket's intention joins the FABRIC — the set of records that say what the system IS — at cast, before any work is done. A task is work the system needs done that does not define it. Both are workflows: same machinery, same mutable string, different relationship to the fabric.

## Why

Akien, 2026-07-22, from 'yank the UU debris out of ~/bin': 'that right there is work that doesn't result in code, has an intention, but that intention is really complete when it's done.' Until now every ticket answered the same way — FREEZE into the component's history as provenance — so the question never had to be asked. The debris yank is the first member that answers differently, and it exposed that the disposition was never actually decided, only defaulted.

The distinction earns its cost by DERIVING what used to be chosen. Because a ticket moves the definition at cast, its voyage MUST freeze beside the code — the fabric changed, so provenance is owed (Law 5). Because a task can be cast, run, and completed with the definition never moving, there is no component whose charter its story is provenance OF — so depot-and-forget is not a policy call, it is what remains. One flag, two dispositions, no judgment at resolve time.

## Settled at cast

- **the_test**: THE SEED TEST — does replaying this intention on a BARE MACHINE contribute to regrowing the system? Ticket if yes, task if no. Install the usage-widget hook: essential, TICKET. Yank the UU debris from ~/bin: a no-op on a fresh box, TASK.
- **where_the_flag_is_set**: At /intent, not /sorted (Akien, 2026-07-22: 'flag at intent, agreed'). The seed test is answerable from the WHAT alone — no approach, no typing, no gate-set needed — so it belongs at the cheapest gate in the system. It also sharpens /intent's trace step: a task still traces up to a Law, but it traces to SERVING the system rather than DEFINING it.
- **the_default**: TICKET is the fall-through; TASK is the branch that must justify itself by passing the seed test. Rationale is the recoverable-error principle: wrongly ticketing costs one spare record; wrongly tasking loses the fabric's provenance permanently.
- **recurrence**: Akien's 'really done' and 'recurrent' cases are ONE mechanism. The standing regime is fabric and is a ticket, cast once; each firing is a task; a one-shot is the same shape with a trigger that will never fire again. No intention closes — the disposable thing was always the instance. This is why the distinction does NOT collide with nothing-is-terminal. SHARPENED 2026-09-04: ad-hoc tasks are 'prototyped' development tickets — when a human-typed task recurs, the recurrence is the signal that this work should be automated, and the development ticket to automate it is cast. The ad-hoc task prototyped the ticket.
- **graduation**: A task that discovers a rule SPAWNS a ticket. The yank is a task; 'no dead-predecessor debris on PATH' is fabric. Without this the boundary is a trap door and knowledge found during maintenance leaves with the receipt.
- **not_a_node_class**: Ticket-vs-task cuts ACROSS the node classes — it splits host-seam work down the middle (install the hook = ticket, yank the debris = task) — which a class by definition cannot do. It sits on the workflow, not on the node. Confirms the earlier axis read; supersedes notes/maintenance-is-an-axis-not-a-class.
- **term_check**: MEASURED before coining: `task` is free. Sole prior occurrence anywhere in cairn/ or CairnCommons/ is `resolver-calls-per-solved-task` (MAP.md:190, 500) — a unit of work in the demo metric, different sense, no collision.

## Explicitly out of scope

WHERE A TASK BERTHS. Ruled once this session (recurrent+shareable -> repo, otherwise ~/.cairn), then destabilized within the hour when the roots-as-stations question opened. Scoped out to child (a) rather than carried as a settled field, because casting a rule we are actively re-deriving is the defect this gate exists to stop. The distinction itself does not depend on the answer; only the disposition's address does.

## Why this class

The distinction yields no single component. Its implementation is two skill edits (/intent asks the question, /sorted carries the disposition) plus prose that governs every future cast — plenty of code addresses, no ONE code address, which is the homeless test. Proved by human judgment, not by a tester run.

## Falsifier

- **proves_green**: quorum signature gate — N human readers read and restate it back; recorded as a VALIDATION with method = 'review by N readers', caller = the reviewers, evidence = their restatement. Verdict (reviewers) and seal (notary) are different hands here; do not collapse them.
- **proves_red**: The distinction is WRONG if the seed test is soft — if, across the first ten nodes cast through the flagged /intent, two readers place any node differently. A test that needs adjudication is not a test, and this one has to be answerable from the WHAT alone or it does not belong at /intent.

It is INCOMPLETE if the empty cell fills: TRANSIENT BUT SHAREABLE — a one-shot every Cairn user needs (a corrective for a bad release, say). Judged genuinely empty today, because the migrations we have (charter -> state+history) change the fabric and are therefore tickets. A real member is the signal to revisit, not a reason to pre-build.

Wrong-INTENT signal (the one to watch hardest): if TASK becomes the cheap escape hatch and the fabric quietly stops recording itself, the flag has become a loophole and is doing the opposite of its job — the UU disease in a new costume.
- **horizon**: The first ten nodes cast through a flagged /intent. Measure: disagreement rate on the flag (target zero), and the ticket:task ratio (a collapse toward task is the wrong-intent signal firing).
