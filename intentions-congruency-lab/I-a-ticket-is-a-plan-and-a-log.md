# A ticket is a plan and a log

*Spanning intention. Every reader and writer of a ticket moves, and the census counts 171 files across
components, so no single directory can hold it. Born 2026-10-09 from idea
`2026-10-09-idea-intention-ticket-and-chart-are-planning`, intent berth
`~/.cairn/devices/skill_block/0/berths/intent/intent-20261009T134421-7d72ff02192c.json`. Agreed the same
day ("agreed on all counts"), and ordered ahead of every other queue item ("the split goes FIRST").
Not yet cast: the format tickets and the migration are cast after the weekly usage reset.*

## Akien, verbatim, 2026-10-09

> IDEA INTENTION TICKET and CHART --- ARE PLANNING. we need to stop looking at tickets like most of
> software does. and start looking at them as the plan for that idea. we don't need to be pushing
> questions in as much as the end decisions and how they line up.

> the ticket becomes the history, and at the same time, the plan is spawned. from here, when we say
> ticket we mean the plan artifact and the history artifact, two related files. to build something, you
> only need the plan. if something is unclear, then you need the history.

> the plan is always the 'current what to do' all questions answered, all intentions clear. the
> questions and the answering of them is in the ticket log. maybe it's ticket log and ticket plan?

Long-term context, from the same conversation: Cairn is a pipeline (the harbor), with every ticket in
flight at once. Building one at a time is a usage limit, not the design.

## What it is (agreed shape)

- **"Ticket" means the pair.**
- **`tickets/<id>/plan.json`**: the current what-to-do. It is rewritten in place and carries no
  superseded lines. The chart folds into it, and the cursor (`workflow_and_state`) lives here, so there is
  still exactly one copy of where the work stands.
- **`tickets/<id>/log.json`**: append-only. It holds the questions and their answers, retired decisions,
  and the trail of how the plan got this way.
- **A one-time, deterministic migration** converts every existing flat `tickets/<id>-<slug>.json` file.
- **The rehearsal reader is handed the plan only.** Every reach into the log is counted as a measurement
  of a decision the plan is missing.
- **The tester asks nothing the plan already settles** (F50, ticket `bf1cd5d79805`): a proof file the
  plan names is approved by the plan. That ticket rides with the format work, because "the plan names it"
  needs a plan to exist.

## The measured scope

`CairnCommons/measurements/2026-10-09-ticket-json-census.json` (measured 2026-10-09T10:05-06:00):
**639 sites over 171 files read or write a ticket file: 87 writers and 557 readers.** Its
`path_assumptions` list names every place that assumes the flat `tickets/` layout, such as
`transitions.py:866` (`_TICKETS`), `cross.py:40`, `cast.py:81`, `chain/grammar.py:282-348`,
`question.py:105`, `clearance.py:539-544` and the build inspector. Line numbers are hand-verified for code
sites. The `kind` of each proof and probe site is heuristic, and the census says so. This is the scope
the migration has to move, and the list the format tickets work from.

## Why

- **Law 5.** The address carries what a mind needs now: the key points, not the trail. The plan is the
  now; the log is the trail. Both are kept, and they are two artifacts so that one reader never has to
  load the other.
- **Law 1.** A builder that has to dig the standing answer out of a ticket's trail is re-deriving
  something already settled.
- **The lived symptom:** questions get pushed into tickets when what a builder needs is the end decisions
  and how they line up.
- **The pipeline aim:** with every ticket in flight at once, each plan has to build without its history.

## Relations

- **`I-a-ticket-is-decisions-not-prose.md` / `d421051bc1f7`** (TICKETME:waiting) is the direct ancestor:
  the plan is its decision list with the trail moved out. The why is the same, so this is not a
  collision. Whether d421 folds into the plan format ticket is decided at `/sorted`.
- **`I-the-briefing-surface-is-charter-plus-state-never-history.md`** makes the same cut one level up:
  charter plus state at the briefing surface, history elsewhere.
- **`I-the-cheapest-reader-proves-a-ticket-before-it-is-built.md`** describes the rehearsal, which is
  the reader the plan serves and the instrument that measures the cut.
- **`tickets/_charter+why.json`** (schema v1) is the store charter that changes.

## Falsifier

- **Done** when every ticket is the pair: no flat ticket files remain under `tickets/`, the census's 639
  sites read the new paths, the build_inspector is green, and a plan-only rehearsal has run over every
  open ticket with its log-reaches counted.
- **Wrong intent** in either of two cases. The first is if plan-only rehearsals raise gaps that only
  history can settle, rather than a decision; that would mean the trail was load-bearing and the cut is
  in the wrong place. The second is if a plan cannot stay free of superseded lines without losing what a
  builder needs.
