# 6bc43453ca64 — a waiting label with no blocker is cleared: review record

**Intention.** A `:waiting` phase stands only while something real is waited on; a waiting
label with no blocker is cleared.

**What holds it today (measured 2026-10-14).** The phase is no longer a label a hand writes.
`transitions.advance` renders `waiting` onto the cursor only when the stage it lands on is a
summons (`is_summons`: the stage ends in `ME`, a stage that demands a peer) —
`cairn/tools/base/transitions.py:2050`. A crossing therefore sets the phase from the stage, and
the departed stage loses any phase it carried. A `:waiting` with nothing summoned has no writer.

**Census (the repaired instrument).** Every ticket under `CairnCommons/tickets/` whose cursor
carries `:waiting` was parsed with `transitions.parse_workflow`, and its stage tested with
`transitions.is_summons`:

    54 waiting labels; 0 stand on a non-summons stage []   (rc=0)

The 2026-09-07 chart named `harbor_master show map` as its instrument; that surface no longer
renders this question, so the instrument was repaired to current names and measures the same
claim (every remaining `:waiting` stands on a real summons; none is stale).

**Hypotheses.** (1) Every `:waiting` ticket is classified genuine or stale — confirmed, all 54
classified, all genuine. (2) Stale labels are removed and genuine ones remain — confirmed, zero
stale survive, and none of the 54 was cleared.

**Falsifier.** A ticket whose cursor reads `:waiting` on a stage that is not a summons.
