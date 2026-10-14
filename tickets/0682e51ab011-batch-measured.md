# 0682e51ab011 — the 2026-09-07 batch, measured from the journal

The piece this ticket's PROVED crossing is sealed over. It is not the ticket file, because a seal over
the ticket expires when the crossing writes the cursor back (CairnCommons 891fb63).

## The claim

"Every ticket whose work needs no cognition crosses to BUILDME in one batch." The validate berth
(`validate-20260907T144539-a02ac721a8e0`) names seven: 201a37bf1613, 0853294fe972, 48519f4789b1,
4d9115eb04cd, aa4463bbd067, b41b0c0fff0e, d6eb399ab6ad (commit CairnCommons 8652628, 2026-09-07).

## What was measured, 2026-10-14

- `python3 tickets/0682e51ab011-batch-measure.py` (beside this file) reads every `history.json` in both
  repos for a row with `ticket` = one of the seven, `to` = BUILDME, `direction` = forward and `at` on
  2026-09-07. It also checks that the row's `entry_gate` reads "a berthed chart chain claims ticket '<id>'".
  Result: **7 of 7** carry the crossing and **7 of 7** passed that gate, all between 14:21:12 and 14:27:35
  on 2026-09-07. That is one batch. Exit 0.
- Negative control: the same script with 201a37bf1613 swapped for 25ee4866642e (not in the batch)
  reads **6 of 7**, exit 1. The script tells a batch member from a non-member.
- The journal is the measure, not today's map. The harbor map on 2026-10-14 reads 0853294fe972 at
  TICKETME. It was retreated that day because its latest BUILDME named the wrong proof (cairn cfb5bfac).
  A later retreat does not undo the 2026-09-07 crossing, and the criterion is that crossing.
  The 2026-09-18 verdict (`verdict-20260918T045535-c67cf0a92974`) read the map and saw 7 of 7 past
  TICKETME at that time.
- The review record is Akien's standing approval, which open-83ff98f1ef31 extends to concept-pieces:
  "a) Yes: CC signs and seals concept-pieces from now on."
