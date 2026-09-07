# Opus queue, 2026-09-06 — clear the waitings

*Written by CC (Fable) at Akien's word: "write that up as the opus queue and saveslate."
Measured 2026-09-06 evening against CairnCommons 79ce803 / cairn 35a915b. Every count
below is a pointer to re-measure (Law 3), not a promise. "Waiting" means a summons is
out and nobody has picked it up (`transitions.pickup`): clearing one is picking it up
and crossing, through the doors named here — never by editing the cursor.*

| Cursor | Count | Who clears |
|---|---|---|
| PROVEME:waiting | 19 | Opus (17), Akien (2 quorum seals) |
| TICKETME:waiting | 8 | Opus |

Work in this order. Each item is independent of the ones after it.

## 1. Thirteen tickets at PROVEME with a sealed proof and a berthed chart — answer the chart, cross PROVED

Twelve crossed TICKETME→BUILDME→PROVEME this morning (cairn 963a1df) through
`harbor_master.clearance.clear`, journaled in the owning component's history; one legacy
ticket (4ddc9df3369e) has the same standing without the journal. Each carries a
`chart_claim` naming a validate berth under `~/.cairn/devices/chart/0/packets/` whose
`criteria[]` list `claim` + `instrument` (a shell line). What is left per ticket, in the
/sail skill's own steps 6–8:

1. Run every criterion's `instrument` verbatim; record outcome + evidence.
2. Write the verdict artifact through
   `cairn.devices.codemother.machines.verdict.verdict.write_verdict` — every criterion a
   run verdict (claim verbatim, instrument, outcome, evidence), every hypothesis in the
   chain `confirmed`|`killed`. A failed criterion is a kick-back, not a crossing.
3. Deposit: `PYTHONPATH=~/dev/src/cairn python3 -m skills.chart.live learn <verdict-berth>`
   (if the tree hangs on the bus, `timeout 15` and proceed — the crossing enqueues the
   deposit on `verdict-deposits.jsonl` anyway).
4. Tickets carrying `WATCHME(<object>)` in the string: arm the probe FIRST — a module at
   the berth the ticket's `watchme.probe` names, declaring a frozen `PROBE` with `carry`
   and `enough`. The emission gate refuses an unarmed one.
5. Cross PROVED through `harbor_master.clearance.clear(workflow_str, "PROVED", actor=,
   boat_id=<ticket id>, proven_by=<proof path>, history_path=, state_path=)` — the exit
   gate reads the verdict off disk. Then set the ticket cursor to `[PROVED]` with a note
   worth reading in a year, and commit.

The thirteen, with the proof the crossing named:

| Ticket | Proof | WATCHME |
|---|---|---|
| 15d6a0ef9c11 valid-verbs-standard-cli-vocabulary | tools/base/proofs/test_address_rule.py | — |
| 4de7baf7e255 sleep-cycle-token | devices/cairn/proofs/test_trouble_panel.py | yes |
| 50ad391f4e95 aider-shim-reaches-into-inference-domain | devices/aider_shim/proofs/test_driver.py | — |
| 61416fbb8013 the-builds-tool-calls-are-evidence-about-the-chart | devices/codemother/proofs/test_codemother.py | — |
| 65b34c57ab71 charter-placed-under-codemother | devices/codemother/proofs/test_codemother.py | yes |
| 68f563403c8f post-build-reflection-feeds-codemother | devices/codemother/proofs/test_codemother.py | — |
| 87a7f1c7ae21 everybody-should-be-talking-to-the-inference-domain | devices/cairn/machines/bus/proofs/test_announce_menu.py | — |
| 9b6b392ebcfe idle-detection-trigger | devices/cairn/proofs/test_trouble_panel.py | — |
| a705346aa75c operator-show-reaches-all-inbox-items | tools/operator_inbox/proofs/test_operator_inbox.py | — |
| bf146e9e3967 token-rotation-mechanism | devices/cairn/proofs/test_trouble_panel.py | — |
| ea4a6151300f inference-call-comprehensive-task-ticket | devices/inference_domain/proofs/test_an_inference_call_logs_that_it_started.py | yes |
| f53cbc262023 the-verbatim-is-checked-against-the-transcript | machines/ruling/proofs/test_ruling.py | — |
| 4ddc9df3369e trouble-tickets-location-is-liveness | devices/trouble/proofs/test_trouble.py (no journaled crossing — journal PROVEME first, then PROVED) | — |

Don't: cross on a proof that is a stand-in for the ticket's falsifier (three tickets
above share `test_trouble_panel.py`, three share `test_codemother.py` — the verdict must
show the criterion's own instrument ran, not that the shared proof is green). Don't
write a verdict for an instrument you did not run. Don't touch `WATCHME` tickets'
cursors past WATCHME — they dwell there until the probe says `enough`.

## 2. Four legacy tickets at PROVEME:waiting that name no proof — find it or send them back

| Ticket | Owning component | Standing |
|---|---|---|
| 2f0a6ea8c966 a-beat-costs-what-changed | devices/cairn/machines/ground_loop (9 proofs, 11 seals) | no ticket id in history; WATCHME(a_beat_costs_what_changed) |
| 7cb1989e7825 mail-arrives-and-what-cannot-marks-itself | devices/cairn/machines/bus (12 proofs, 11 seals) | BUILDME entry journaled in bus/history.json; WATCHME(does-the-mail-lane-get-worked) |
| b48ebc9b9e48 the-questions-are-the-sieve | machines/build_inspector (9 proofs, 9 seals) | no ticket id in history; WATCHME(engine-branchless-under-a-second-block) |
| d6cacb63868b learning-block-engine-track | machines/learning_block (1 proof, 1 seal) | BUILDME entry journaled in learning_block/history.json |

For each: read the ticket's `falsifier.proves_green`, find the proof beside the
component that asserts it, and run it. If one exists and is green → item 1's path
(journal the PROVEME crossing with that `proven_by`, then answer whatever chart claims
the ticket, then PROVED). If none asserts the falsifier → the cursor is a claim nobody
verified: set it back to `[BUILDME]` through the door with the finding in the journal,
and the ticket rejoins item 4's build queue. Red is the honest default (Law 9). Don't
pick the nearest green proof to make the cursor true.

## 3. Two concept-pieces at PROVEME — Akien's hand, not Opus's

| Ticket | Piece |
|---|---|
| 728d393d70ed cognition-domains-general-coding-research | (no owning_intention on the ticket — locate the prose by title) |
| 907f456a6136 the-method-transfers-across-substrates | press_office (1 proof, 1 seal already beside it) |

Their gate is the quorum signature: Akien reads and signs through
`cairn.devices.tester.quorum.seal(artifact_path, claim=, signatures=[...], notary=,
falsifier=, horizon=)`; the PROVEME crossing then names that validation
(`emit(..., validation=<path>)`, the `_quorum_gate` seat, cairn 7374626). Opus's part:
put the two pieces in front of him with the seal command filled in, and nothing else.
The same-hand seal under a ruling is the ruled exception for CODE, not prose.

## 4. Eight tickets at TICKETME — cross BUILDME, then build

Seven cast today with a builder_check on the ticket (files, lines to copy, don'ts); one
older. Akien delegated the order to CC ("you get to specify the order", 2026-09-06 evening);
this is it, and the reason for each seat is written so a builder can disagree with it:

1. 48519f4789b1 one-bus-per-instance-hosts-every-shim — and 2. d6eb399ab6ad
   the-first-shim-starts-the-ground-loop, in one voyage (2's call site is decided by 1).
   First because everything below either rides the bus or moves its tables.
3. 0853294fe972 cairn-checks-the-floor-before-it-resolves. Shim-side, touches no tables;
   goes before the store is opened up so the launch chain is green when it is.
4. b41b0c0fff0e hot-and-the-root-verbs-resolve-in-the-shim (child of 15d6a0ef9c11 —
   item 1 above lands the parent's PROVED first, or the child's proof asserts against a
   parent still at PROVEME; either is legal, the first is cleaner). Same reason as 3.
5. **201a37bf1613 a-scratch-table-cannot-outlive-its-process** — measured 2026-09-06:
   9,087 tables in `cairn`, 12 live; 8,270 carry a dead pid, 2,424 are `_delivery`
   companions the bus mints at bus.py:287 that no proof's `finally` drops. The ticket: a
   `scratch()` door in the store (pid-registered, dropped on exit, companions registered,
   swept by the tester before each seal), the 17 minting proofs moved onto it, and a
   one-time sweep by hand. Seated here so the per-owner migration copies from a clean
   database; the emptied old database is then dropped by the next item, not this one.
6. **aa4463bbd067 the-owner-is-a-database-and-every-link-is-a-tuple** — the per-owner
   database, the universal address, the link tuple, the migration of the twelve live
   tables. RULED to come "before things become even more complicated"
   (`decisions/2026-09-06-the-per-owner-database-comes-before-more-complexity`, confirmed).
   After 1–4 because the bus's `create_owned_table` moves onto `connect(owner)` here, so
   the bus must be one and settled; before 5dbc03e007c5 because that sieve reads the
   store and should be born on the new address. The ticket carries the builder-level how
   (address.py, `cairn_<owner>` databases, registry per database, links as two owned
   half-rows, void-and-reuse lists, `migrate_to_per_owner.py`, seven proof teeth) and two
   rulings it must not exceed: no read gate is invented here, and **the librarian is
   allowed access to everything until the hardening step** (Akien, same evening). The
   credential vault (idea `2026-09-06-each-user-me-you-igor-etc-has`) is NOT in this
   ticket; it is not yet cast. Drops the emptied old `cairn` database after its counts
   assert (amended: item 5 sweeps, this item drops).
7. 5dbc03e007c5 cognition-gate-intention-extraction (2026-08-30; an `intention_fidelity`
   sieve in build_inspector; no chart chain yet).
8. 4d9115eb04cd a-seal-that-cannot-be-reproven-rides-the-ruled-ladder — LAST, and only
   after its dependency is cast and landed: the import-closure fingerprint, idea
   7bdf2d19671d (`ideas/2026-09-06-fingerprint-what-the-proof-exercises-not-the.json`),
   not yet cast. Cast it (/intent → /sorted) before touching this one.

The credential vault (ideas `2026-09-06-each-user-me-you-igor-etc-has` and its parent) is
NOT in this queue: Akien 2026-09-06, "we build the first one during the predecessor to UU.
originally it's own device. but cairn is the right place for it for now." The predecessor to UU
is UtilityCloset, later renamed AgentDatacenter, one project (his lineage: TheIgors →
UtilityCloset/AgentDatacenter → UnseenUniversity → Cairn; the old code is under
~/TheIgorsProject/utility_closet); UU's `unseen_university/devices/vault/` is the prior art to cite when it is cast. Not cast.

Each BUILDME crossing runs the chart chain at the entry gate; constrain now trusts a
standing seal (963a1df), so the bus-touching hang recorded in the 2026-09-05 slate no
longer blocks. Then /sail.

## What is NOT in this queue

- The 12 tickets at WATCHME are dwelling, not waiting — a probe decides when they move.
- The 11 live `inspector-new-finding-*` troubles: item 1's reseals will clear some
  `component_color` ones as a side effect; the two `device_isolation_holds` (cairn and
  web_server importing trouble) are a design question for Akien, not a build.
- The review delegation (CC relays "reviewed and approved" from chat, record gains
  reviewed_by/recorded_by, Stop-hook detector for review markers) — Akien said "get it
  now" and has not ruled; it waits at his gate.
