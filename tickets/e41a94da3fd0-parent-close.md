# e41a94da3fd0 — parent close: "The inspector finds, the gate certifies"

The parent's falsifier, measured over its four children. **The parent wrote no code;
its build is PROVES declarations** — a second key `"e41a94da3fd0"` beside each child's
own in three proofs, and the falsifier's clauses marked (1)-(6) with no word changed.

## Children

| Child | Ticket | Cursor (read 2026-10-29) | Proof it crossed PROVED on |
|---|---|---|---|
| 1 | 5dc4d8a0b4d2 | `[PROVED]` | cairn/tools/base/proofs/test_only_the_gate_writes_a_certificate.py |
| 2 | 66ee1ffc1ec7 | `[PROVED]` | cairn/tools/base/proofs/test_the_crossing_compares_what_the_inspector_found.py |
| 3 | 632edb992aa3 | `[PROVED]` | cairn/tools/base/proofs/test_light_modules_keep_the_crossing_off_the_inspector_path.py |
| 4 | 7c41e2b09d5a | `[PROVED]` | cairn/tools/base/proofs/test_the_crossing_stands_on_a_certificate.py |

## The falsifier, clause by clause

| Clause | Tooth | Proof | Reading |
|---|---|---|---|
| (1) every gate's output is a certificate the base gate class writes and verifies | test_certify_writes_what_verify_accepts | test_only_the_gate_writes_a_certificate.py | green |
| (2) a certificate written or edited by hand fails verification | test_a_certificate_around_the_door_fails_both_checks | test_only_the_gate_writes_a_certificate.py | green |
| (3) the only checks are inspector sieves | test_each_lane_asks_its_inspector_function | test_the_crossing_compares_what_the_inspector_found.py | green |
| (4) an entry gate does nothing but compare findings and kick back | test_the_gate_reads_nothing_of_the_world | test_the_crossing_compares_what_the_inspector_found.py | green |
| (5) the inspector imports nothing that can post, record a crossing, or reach a host, and test_inspector_nexus is green | test_the_inspector_never_reaches_the_crossing; test_inspector_nexus whole | test_the_crossing_compares_what_the_inspector_found.py; cairn/machines/build_inspector/proofs/test_inspector_nexus.py | green; green |
| (6) every crossing past an entry gate names the certificate it stands on | test_a_gated_crossing_names_a_certificate_that_verifies | test_the_crossing_stands_on_a_certificate.py | green |

## Readings

- Each of the five proofs above (the four children's plus test_inspector_nexus), run
  singly twice with `bin/cairn test <proof>`: exit 0 on all ten runs.
- The five together, after the PROVES keys were added:
  `5 proofs · 5 green · 0 red`.
- `proof_coverage.declared` over the three keyed proofs gives e41a94da3fd0 keys
  `['1','2']`, `['3','4','5']`, `['6']`, which equals the falsifier's clauses `['1'..'6']`.
- Every live certificate under `CairnCommons/certificates/`, through
  `gate_class.verify_certificate`, read after this parent's PROVEME: all eight VERIFY
  (7c41e2b09d5a BUILDME 20261028T234242Z, PROVEME 20261028T231650Z, PROVEME
  20261029T000935Z, PROVED 20261029T001330Z; 7a31059daa23 BUILDME 20261029T163915Z,
  PROVEME 20261029T164259Z; this parent's own BUILDME 20261029T165449Z and PROVEME
  20261029T171058Z).
- The hollow reading for this parent: the three proofs are its instrument and are skipped;
  the one file measured is this ticket's own JSON, which no tooth pins, so `--seal`
  notified the operator (n-f2bb692445a5) instead of covering it.

## What the live record shows, and what it doesn't

Clause (6) is measured in a fixture by tooth 1 and on the live record by child 4's own
crossings: each one past an entry gate names a certificate that verifies. Children 1–3
crossed PROVED **before** child 4 built certification, so their crossings name none.
That is the order the work happened in, not a gap in the clause. Every crossing from
child 4 onward stands on a certificate.

## What the voyage found

Certifying exposed the demo seat's no-flag row as a failing row in 57 of 58 PROVED records,
which blocked PROVED for every ticket without a demo flag. Fixed under child 4 (D14,
cairn e1f9c58c). The `test_encapsulation_holds` red that child 2's off-interface import
introduced was fixed at cairn 124b00f2.
