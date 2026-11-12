# 8e3474a6ae43 — RULE 1 (encapsulation), the parent falsifier measured

This is the piece the parent's PROVED crossing is sealed over. It is a separate file from the ticket,
because a seal over the ticket expires when the crossing writes the cursor back (CairnCommons 891fb63).

## The claim

RULE 1 stands in CLAUDE.md above the Laws, pointing at its intention, and that intention carries
Akien's agreed 2026-10-01 text. No Law was renumbered. Every child is terminal. The live
encapsulation sieve finds no reach into a device from outside it.

## What was measured, 2026-11-12

`python3 tickets/8e3474a6ae43-rule1-measure.py` (beside this file, run from CairnCommons) exits 0:

- **Clause 1, green.**
  - CLAUDE.md has a `## RULE 1` block before `## The Laws`, and the block names
    `I-rule-1-encapsulation.md`.
  - The .md carries all 18 sentences of the FINAL RULE 1 TEXT block from
    `~/.cairn/foreground-decisions.md`, word for word, after markdown and arrows are folded.
  - Each of the 10 Law numbers opens with the same words it did at 925c9086f15f, the last CLAUDE.md
    commit before 2026-10-01T12:00. Nothing was renumbered.
- **Clause 2, green.** The ticket has 28 children by state.json `parent`: 26 PROVED and
  2 SUPERSEDED. None is live.
- **Clause 3, green.** `encapsulation_breaches` over the whole cairn repo returns 0 rows. Its reach
  is the import sieve's: 4,897 import sites in cairn/, 242 in skills/, 37 in bin/ and 16 in
  press_office/. `launchers/`, which the falsifier names, no longer exists. Opaque (computed)
  imports are counted by `encapsulation_opaque` and are never red (outline 17.13.1).

**Negative control.** `--control` swaps in one falsifying input per clause: Laws 1 and 2 swapped,
child 124c0312c2d8 forced to BUILDME, and one synthetic breach row. It reads 0/3 and exits 1, so each
clause can tell a falsifying world from a green one.

## What this does not measure

The sieve is a **device-path check** (outline 17.13.1, Q#77). It does not read `public_interface`.
A reach past a machine's or tool's declared interface *inside one device* is not checked, and the
agreed text's "one check over every component" is narrower in physics than in prose. CLAUDE.md's
RULE 1 block already says so, and the narrowing is Akien's answer, not a lapse.
