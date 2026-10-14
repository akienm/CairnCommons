# 471aa05ba639 — the parent's falsifier, measured over its children

The piece this ticket's PROVED crossing is sealed over. It is not the ticket file: a seal over the
ticket expires when the crossing writes the cursor back.

## What was measured, 2026-10-14

- `bin/cairn test cairn/tools/charter/proofs/test_append_door_instrument.py
  cairn/tools/artifact/proofs/test_a_history_row_without_standing_is_refused.py` reads
  **2 proofs · 2 green · 0 red**. The tooth `test_every_real_history_on_disk_would_pass_the_gate`
  is unchanged and green over every class-space history, and `artifact.write` refuses a history
  row lacking `standing` and writes nothing.
- Child **62a57b781efc** (the artifact door refuses a history row without standing) reads
  `[PROVED]`; child **ba8c62b8203e** (the two bypass rows carry their predecessor's standing) reads
  `[PROVED]`. diagnostic_inspector seq 4 is left as written, per Akien's answer
  (open-a13486d0510d).
- Chart chain: `validate-20261014T042027-004908b2b44c.json`; verdict
  `verdict-20261014T045830-d50713c6f200.json` (both criteria passed, the one hypothesis confirmed).
- The parent wrote no code: its falsifier is measured over what its two children built.
