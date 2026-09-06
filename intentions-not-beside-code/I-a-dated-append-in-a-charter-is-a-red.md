# a-dated-append-in-a-charter-is-a-red

*concept-piece · ticket c7477924430e · owning intention: intentions-not-beside-code/_charter+why.json*

## Intention

Define the canonical dated-append shapes — the patterns that mark where someone accreted dated narrative into a present-tense artifact instead of rewriting it whole. A deterministic Python function composable by the parent's probe.

## Why

child of an-artifact-is-present-tense-or-past-tense-never-both: the parent's probe carries v0 patterns (RETIRED, formerly, date-stamped parenthetical) locally. Canonicalizing them into a reusable checker transfers ownership of the pattern list from probe-local to child-owned, and lets the parent's enough count start — the watch cannot clear until the canonical checker exists.

## Definition

- **what**: A dated append is a shape in a present-tense artifact that narrates a change rather than stating the current design. It accretes history into the briefing surface where a reader loads by default, forcing re-derivation of the settled (Law 1) and making the artifact carry two tenses at once.
- **canonical_shapes**: 
  - 
    - **name**: retirement_stamp
    - **pattern**: \bRETIRED\b
    - **example**: RETIRED: this field was replaced by X on 2026-08-01
    - **why_it_signals**: A retirement stamp narrates a succession. The successor IS the artifact now; the predecessor's story belongs in the commons (Law 5). A reader loading the artifact sees a thing that used to be, where they should see only what IS.
  - 
    - **name**: used_to_be_clause
    - **pattern**: \bformerly\b
    - **example**: the orient brick (formerly the orient tool)
    - **why_it_signals**: A 'formerly' clause is provenance wearing a present-tense hat. The old name belongs in the commit that changed it; the current name stands alone. A reader does not need to know what a thing used to be called in order to use it now.
  - 
    - **name**: date_stamped_parenthetical
    - **pattern**: (20\d\d-\d\d-\d\d
    - **example**: (2026-08-01: added the orient brick to the chain)
    - **why_it_signals**: A date-stamped parenthetical is the most common shape: someone changed the design and appended a dated note instead of rewriting the paragraph. The date is the tell — a present-tense statement does not need one, because the current version IS the statement. The date says 'this was added at a specific time', which is history.
- **what_is_NOT_a_dated_append**: 
  - A date in a ruling citation ('Akien, 2026-08-17') — the date is the address of a ruling, not a change narrative. Rulings are present-tense statements of authority; the date locates them.
  - A date in a ticket's date field — that is metadata, not prose narrative.
  - A dated entry in history.json — history IS the past tense, and the file says so in its name. The rule targets present-tense artifacts, not history.
  - A date in a proof or validation — those are records of truth (Law 7), append-only by construction.
- **the_fix**: Rewrite the paragraph to state the current design, period. Move the story of how it got there to the commons or to the commit. A pointer ('ruling 2026-08-17') is not a dated append — it is a citation, and citations are how provenance shrinks to present tense.
- **the_test**: Read the paragraph without the date or the change-narrative clause. Does it still say what the thing IS? If yes, the date was decoration — remove it. If no, rewrite: the thing the date was trying to say is the current design, and the current design should be stated as fact, not as something that happened on a date.
- **composability**: The parent's probe (present_tense_artifacts_carry_no_dated_appends.py) composes these shapes via regex. When a deterministic checker replaces the v0 patterns, it owns the pattern list and the probe imports it — transferring ownership of shape-recognition from probe-local to child-owned, per the ticket's own intention.

## Falsifier

- **proves_green**: 
  - **proof_gate**: quorum signature gate
- **proves_red**: Done when the canonical shape-check function catches every specimen in the corpus and the parent's probe composes it instead of the v0 patterns. Wrong-intent if a legitimate dated-append exists that a present-tense artifact must carry — the answer then is a labeled exception, never a loosened pattern.
