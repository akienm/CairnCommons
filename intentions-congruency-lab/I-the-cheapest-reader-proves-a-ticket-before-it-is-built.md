# The cheapest reader proves a ticket before it is built

*Spanning intention (the rehearsal touches /sorted, /sail, the chart, the BUILDME entry gate and a new
machine, so no one directory holds it). Born 2026-09-15 from idea `2026-09-15-1-so-we-re-getting-buried-in`. Cast as ticket `cf80bdb57205`;
the machine's charter is `cairn/machines/rehearsal/intention+why.json`. Ruled the same day: "agreed on all
counts. RULED APPROVED CAST INTO STONE LETS GO".*

## Akien, verbatim, 2026-09-15

> if i say 'i want tickets so well written that haiku can reliably build them' is not going to be as effective
> as 'reading the ticket as haiku, point out every unanswered question so we can take another pass at getting
> them answered before the build' is it? how can i do it even better?

(Haiku's answer, which he carried in whole: show the proof skeleton, not a critique; comparative reading —
three cold reads that never see each other, every divergence a gap; interactive narrowing — answer one gap,
re-read, the next gap appears.)

> OMG. This is how to train a learning block to produce effective tickets. it means there's a loop inside of
> the ticketing skill or script. We run an agent with the ticket, ask for it's proof tree, simplify or get
> questions answered, then try again until it passes that gate. All on the cheapest model. and after the
> prebuild. which we can also keep learning at the same time.

> we're not talking about a building step, but a ticketing step, learning from a haiku agent, we hand the
> agent the prebuild which we can run without llm. this will make ticketing a testable artifact in a whole
> new way. we're not measuring 'yes it has field a' but we're measuing if it can be built as written.

> tell haiku that it's job is to build out it's tree, not to produce code. so 'not possible' is not a fail
> but another right answer.

> and then the build simulation ticketing process. because that gives us almost a hard gate on ticket
> quality equal to me. and then we run all our tickets thru it, and i don't have to approve them because we
> know they'll build as we meant. that leaves me ideas and intentions only.

## What it is (CC's reading, accepted "agreed on all counts")

A **rehearsal** is a build performed without the build. The cheapest model (Haiku 4.5) reads the ticket
plus its prebuild — the chart chain's berths — three times cold, and returns a **typed build tree**: every
step with a state in `builds_as_written | builds_under_assumption | cannot_proceed`, the assumption, what
would settle it, and a confidence. The three trees are diffed **by code**; every divergence and every
non-`builds_as_written` node is a gap. CC disposes each gap: derivable from an intention, charter or prior
ticket → a one-line decision on the ticket with its provenance; not derivable → `cairn question open
--ticket`. Then re-read. A clean rehearsal (three reads, zero gaps) is a record in `CairnCommons/rehearsals/`
the ticket points at, and the BUILDME entry lane `the_ticket_rehearses_clean` refuses the crossing without
one whose ticket hash still matches.

**The gate reads "no reader has to assume", never "Haiku's build is the build."** Akien's own check
(2026-09-15): anything Haiku can build, Opus almost certainly can; the exception is Opus building differently
because it noticed a conflict Haiku walked past. So after PROVED the built proof is diffed against the
converged tree and the divergence is written onto the rehearsal record — that is the WATCHME, and the
gate's own greens are measured by it (Law 8: a hollow green is worse than a red).

## Why

- **Law 3.** A ticket's buildability was a self-report by its author (/sorted's `builder_check`: the same
  mind writes and judges). The rehearsal is the measurement that replaces the self-report.
- **Law 9 / ruling 2026-08-15.** Measurement outranks his approval. A ticket that rehearses clean needs no
  approval from him, and his inbox holds only what only his head can settle — the questions the rehearsal
  could not derive.
- **The lived symptom.** "so we're getting buried in 'things akien has to look at' again, and i can't keep
  up. My day job isn't doing well ... since we have no funding other than my day job, continuing to fall
  behind is a problem."
- **It measures the chart for free.** The reader gets the ticket and the chart, never the repo; a
  `cannot_proceed` that names a file the survey did not list is a finding against the survey leg.
- **It is how the learning block learns.** Every gap kind, every decision kind, every post-PROVED divergence
  is a labeled example from the real world; the tree that asks the recurring questions before the first
  read is a child cast after ten records exist.

## Pointers

- Ticket: `CairnCommons/tickets/cf80bdb57205-the-cheapest-reader-rehearses-a-ticket-before-buildme.json`
- Siblings from the same idea: `fb988505c5cb` (measurement drains the review lane), `d421051bc1f7`
  (a ticket is a list of decisions, not prose — see `I-a-ticket-is-decisions-not-prose.md`)
- Machine charter: `cairn/machines/rehearsal/intention+why.json`
- Records: `CairnCommons/rehearsals/` (artifact door, verb `rehearse`)
- The reader, measured 2026-09-15: `claude -p --model claude-haiku-4-5-20251001 --output-format json`, 3.3s, $0.04
