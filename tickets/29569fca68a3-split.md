# 29569fca68a3 — every ticket is split into its plan and its log

Every ticket is split into its plan and its log: the split reconstructs every pre-split ticket exactly, no plan carries a key outside plan_fields, nothing went redder, and the plan-only rehearsal has read every open ticket.

The piece this ticket's PROVED crossing is sealed over. It is not the ticket file: a seal over the
ticket expires when the crossing writes the cursor back. Every number below is the output of
`CairnCommons/measurements/2026-10-10-plan-log-split-check.py`, run from cairn on 2026-10-11.

## (1) and (2) — `reconstruct` exits 0

```
{"commits": [{"split_commit": "f93d899d813c8a8c22e8f79a1577e0273727289d", "tickets": 535, "split": 377, "already_clean": 158, "lines_by_kind": {"rehearsal": 219, "field": 772, "decision_retired": 25, "phase_write": 39}, "mismatches": [], "extra_keys": [], "missing": []}, {"split_commit": "1716a07f70fb53c559771ea9adc858cdcc7062ee", "tickets": 535, "split": 19, "already_clean": 516, "lines_by_kind": {"renamed": 19}, "mismatches": [], "extra_keys": [], "missing": []}], "no_intention": []}
```

Both split commits: 535 tickets, 0 mismatches between plan + added log lines and the parent's
ticket, 0 keys outside plan_fields, 0 plans with no intention (decisions 26 and 27).

## (3) — `reds` exits 0

The suite and build_inspector were run before the split and after the rename on the same cairn
commit cd84cbb3 (the run took 5951 s; cairn moved to 43c2f48a under it, through 8902708b6212's
voyage and this ticket's own 09d34468). The red set after is a subset of the red set before:

- build_inspector: 115 before, 45 after, **0 new**. The 70 gone are all `working_tree_clean`.
- `cairn test`: 18 before, 15 after, **0 new**.

## (4) — `rehearsals` exits 0

```
{"open": 120, "rehearsed": 120, "clean": 31, "unrehearsed": [], "log_reach_total": 580}
```

Every open ticket has a plan-only rehearsal record. Per-ticket log_reach counts are in the verb's
full output (36 tickets carry reaches).
