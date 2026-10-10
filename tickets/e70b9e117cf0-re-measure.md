# e70b9e117cf0 — b577a9f486dd's verdict, re-measured

The piece this ticket's PROVED crossing is sealed over. It is not the ticket file: a seal over the
ticket expires when the crossing writes the cursor back (CairnCommons 891fb63).

## What was measured, 2026-10-10

- b577a9f486dd's three criteria were checked again as commands over the intentions-not-beside-code journal
  and state, read with `git show <sha>:<path>` from CairnCommons:
  at **7e6d9b0** they exit **0, 0, 0**; at **7e6d9b0^** they exit **1, 1, 1**.
- Criteria 2 and 3 name the journal's last entry. At 7e6d9b0, the journal's actual shape puts the BUILDME
  crossing at index 0, and the evidence says so in words (ticket decision 4, commons 4f932d4).
- The new verdict, `~/.cairn/devices/chart/0/packets/verdict-20261010T142050-7e19dee91d34.json`, passes
  `validate_verdict`. `enqueue_verdict('b577a9f486dd')` returned it.
- `mark_superseded` recorded the pre-rule verdict `verdict-20260815T141125-dd35ea1c8f7b.json`
  as superseded by the new one. The learn drain landed 7 parts with 0 failures. `pending() == []`,
  and `skills.chart.live counsel probe` exits 0.
- This task's own verdict is `verdict-20261010T142212-9d2cbca6ab67.json`.
