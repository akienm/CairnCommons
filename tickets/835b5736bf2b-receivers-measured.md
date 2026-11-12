# 835b5736bf2b — every probe has a receiver, the parent falsifier measured

This is the piece the parent's PROVED crossing is sealed over. It is a separate file from the ticket,
because a seal over the ticket expires when the crossing writes the cursor back (CairnCommons 891fb63).

## The claim

Every WATCHME probe that can fire names a receiver, and that receiver is real code that the probe
posts to. Every child crossed PROVED.

## What was measured, 2026-11-12

`python3 tickets/835b5736bf2b-receivers-measure.py` (beside this file, run from CairnCommons) exits 0:

- **Clause 1, green.** The tickets hold 132 WATCHME specs that name a probe. 102 of those probes are
  on disk (armed). None of the armed probes outside FIXME lacks a `receiver` dict.
  - 30 specs name a probe file that is not in the repo.
  - 20 of the 30 have no receiver. All 20 are on dead tickets (SUPERSEDED, KILLED or RETIRED), and
    their probe files are deleted, so nothing is left to fire.
  - The other 10 carry the receiver already. Seven are probes not yet built, on tickets at TICKETME,
    BUILDME or WATCHME:waiting.
  - One is 7aed0fd0ba29 (PROVED). Its probe left the repo with the cairnmap tool, which
    d547b4859f9a retired (cairn 3882dac1).
- **Clause 2, green.** The ticket has 44 children by state.json `parent`: 43 PROVED and 1 DROPPED.
  The dropped one, e24386e75704, crossed PROVED first. It was then dropped because Akien ruled its
  only probe deleted on 2026-10-04 ("yes, delete it the schema watching probe.").
- **Clause 3, green.** All 101 armed probes that carry a receiver name the same one,
  `cairn/devices/codemother/machines/watchme`. Its code registers `watch`, and each of those probes'
  source posts `to="codemother"`, `verb="machines/watchme/watch"`. No receiver was written only to
  fill the field.

**Negative control.** `--control` adds three falsifying inputs: one armed spec without a receiver,
one child forced to BUILDME, and one receiver pointing at a directory that does not exist. It reads
0/3 and exits 1.

## How the letter was read

The falsifier says "zero probe-bearing WATCHME specs that lack a receiver ... on a ticket not
standing at FIXME". This measure reads "probe-bearing" as **a probe file on disk**. A spec on a
retired ticket whose probe file is deleted posts nothing, so it has nothing to receive. Those
specs are counted above, not hidden.
