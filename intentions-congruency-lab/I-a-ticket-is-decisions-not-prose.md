# A ticket is decisions, not prose

*Concept-piece. Born 2026-09-15 from idea `2026-09-15-1-so-we-re-getting-buried-in`. Cast as ticket `d421051bc1f7`, deliberately held
behind its sibling `cf80bdb57205` (the rehearsal): the ticket-v2 schema is compiled from the first ten
rehearsals' decision lines, never authored first. Ruled the same day: "agreed on all counts. RULED APPROVED
CAST INTO STONE LETS GO".*

## Akien, verbatim, 2026-09-15

> as i wrote that, i recall that there's an item 3 as well. i have not specified what should be in a ticket
> for the most part. ive said we have to have a title and intention and so on, and we do have those things.
> but i read many of your tickets and i just get lost in the verbage. to me it's completely amazing that
> works for you. my ADD brain gets lost. i think the role of that verbage is part of what i'm aiming at:
> less prose, more 'decisions made'. You have historically had this big thing about decisions, needing to
> record them and all. yeah, we have some big ones, but they need to be in our intentions. small ones need
> to be in the ticket. if haiku build simulation needs something more spelled out, that's a decision we're
> making even if i'm not making it. many small decisions. then we submit to haiku simulation again.

## What it is (CC's reading, accepted "agreed on all counts")

A ticket is a **list of one-line decisions, each carrying who made it** — `Akien verbatim <date>`,
`derived from <address>`, `CC at cast <date>`, or `CC under rehearsal <record>` — and never a body of
prose. **Big decisions** (anything that changes a charter's what or why) go to the intention in the same
act. **Small decisions** (the mechanism choices a builder needs) go on the ticket. The prose ticket-v1
copies onto the ticket — why, how, cast_checks, challenge_at_birth — stays in the berths it came from and is
pointed at. A reader who cannot infer (Akien; the cheapest model) can scan it, and he can veto **one line**.

The shape is **precipitated, not designed** (Law 1): the three tickets cast 2026-09-15 carry a leading
`decisions[]` as the first instance; the rehearsal's gap-answers are decision lines; after ten rehearsal
records the kinds that recurred become `CairnCommons/tickets/_schema-v2.json`, with the census beside it.
No hand migration — an open v1 ticket becomes v2 by being rehearsed.

## Why

- **Law 5.** The address carries what a mind needs NOW — the key points, not the trail. A ticket's prose
  is the trail.
- **CP4, designing to the tool**, where the tool is now two readers: his "ADD brain" and the cheapest
  model, neither of whom infers from prose.
- **The provenance is the veto.** A line marked `CC at cast` is one he can strike without touching the
  lines that are his own words; a line marked `Akien verbatim` is one CC may not reinterpret.
- **The lived symptom:** "i read many of your tickets and i just get lost in the verbage."

## Pointers

- Ticket: `CairnCommons/tickets/d421051bc1f7-a-ticket-is-a-list-of-decisions-not-prose.json`
- Siblings: `cf80bdb57205` (`I-the-cheapest-reader-proves-a-ticket-before-it-is-built.md`), `fb988505c5cb`
- Filing today is a hand script (`file_tickets2.py`, scratchpad) — moving it into `skills/sorted/door.py`
  is decision D5 of the ticket.
