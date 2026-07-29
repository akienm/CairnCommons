# BUILD PACKET — ticket `the-deposit-rides-the-read` (tier: opus)

You are the builder for one Cairn stone. You have minimal context BY DESIGN —
everything you need is in the files below; the gates judge your work by
instrument. Do not improvise beyond the berths.

## Read first, in this order
1. `/home/akien/dev/src/cairn/CLAUDE.md` (the Laws)
2. `/home/akien/dev/src/CairnCommons/tickets/the-deposit-rides-the-read.json` (your ticket)
3. `/home/akien/dev/src/cairn/skills/sail/SKILL.md` (the build liturgy — follow ALL its steps)
4. The seven chart berths that claim your ticket (build ONLY inside them):
   - `~/.cairn/devices/chart/0/packets/orient-20260729T112638-5c169aa538ff.json`
   - `~/.cairn/devices/chart/0/packets/constrain-20260729T112807-896865355314.json`
   - `~/.cairn/devices/chart/0/packets/survey-20260729T112908-70ca2b913f8e.json`
   - `~/.cairn/devices/chart/0/packets/decompose-20260729T113016-7724772bdec1.json`
   - `~/.cairn/devices/chart/0/packets/triage-20260729T113048-2212ed29ee9b.json`
   - `~/.cairn/devices/chart/0/packets/hypothesize-20260729T113143-e2ca1dfb9193.json`
   - `~/.cairn/devices/chart/0/packets/validate-20260729T113215-c0e3211648d2.json`

## Environment
- Code repo: `/home/akien/dev/src/cairn` — run everything from here with
  `PYTHONPATH=$PWD`. Knowledge repo: `/home/akien/dev/src/CairnCommons`.
- `git pull` both repos before starting (a sibling stone landed a jurisdiction
  tightening at the chokepoint just before you — every forward BUILDME/PROVED
  crossing must name its cast ticket; yours does). Work on main. Push when done.
- Your voyage journals at the parent component `cairn/chart/` (history.json +
  state.json), carrying your ticket:
  ```
  PYTHONPATH=$PWD python3 -c "
  from cairn.base.transitions import emit
  import json
  cur = json.load(open('cairn/chart/state.json'))['workflow']
  print(emit(cur, 'BUILDME', history_path='cairn/chart/history.json',
             state_path='cairn/chart/state.json',
             ticket='the-deposit-rides-the-read', note='<why this crossing>'))"
  ```
  (Same idiom for PROVEME, LEARNME, PROVED. NEVER hand-edit history/state.)
- Seal proofs (each of the four files, twice, then persist):
  ```
  PYTHONPATH=$PWD python3 -c "
  from cairn.tester.device import TesterDevice
  from cairn.tester.validation_store import persist_validation
  t = TesterDevice()
  for p in ['cairn/base/proofs/test_transitions.py',
            'cairn/chart/proofs/test_chart_verdict.py',
            'cairn/build_inspector/proofs/test_inspector_nexus.py']:
      for i in range(2):
          rec = t.run_proof(p, caller='ticket the-deposit-rides-the-read', isolation='netns')
          print(rec['verdict'], rec['evidence']['seal']['verdict'], p)
          assert rec['verdict']=='green' and rec['evidence']['seal']['verdict']=='sealed'
      persist_validation(rec, proof_path=p)"
  ```

## What you build (the berths hold the full design; summary only)
Deposit-as-physics, in triage's order:
1. **Ledger section in `cairn/chart/verdict.py`** (stays tree-free: stdlib +
   cairn.chart.orient ONLY): `enqueue_verdict(ticket)` appends an enqueued
   record to an append-only JSONL ledger in `~/.cairn/devices/chart/0/`
   (berth path + ticket + stamp) after locating the latest claiming verdict
   artifact via a `claiming_artifacts`-style locator FACTORED HERE — then
   refactor `cairn/build_inspector/inspector.py`'s exit check to compose that
   locator by import (ONE latest-claimer rule; kill its private twin glob).
   `pending()` derives enqueued-minus-deposited by read. `mark_deposited(berth,
   node_id)` appends the second record kind. NOTHING mutates existing lines.
2. **Enqueue seam in `cairn/base/transitions.py`**: the exit-gate-clean
   forward-into-PROVED branch lazy-imports and calls the enqueue. Key on the
   ARTIFACT existing, never on the clean note (an unclaimed gated-and-clean
   crossing has a clean note but NO artifact and must enqueue nothing).
   Refusals and back-edges enqueue nothing. File-only writes (netns-safe).
3. **Drain in `cairn/chart/live.py`**: both door verbs (counsel + learn) drain
   pending entries through the existing `deposit_verdict` before serving;
   failed deposit → entry stands pending + named loudly in output, verb still
   serves; deposited berths skip (idempotence via the deposited record).
4. **Teeth**: extend `cairn/base/proofs/test_transitions.py` (its `_exit_world`
   fixture) and `cairn/chart/proofs/test_chart_verdict.py` (its scratch-nexus-
   table pattern — the LIVE hypothesize tree is never a fixture) per the
   hypothesize berth; re-verify the nexus pin covers the grown verdict.py.
5. **Live fire + records**: your own stone's close IS the live fire — your
   PROVED crossing must enqueue your real verdict artifact, and your step-8
   deposits (`python3 -m cairn.chart.live learn <berth>`) drain it. Verify the
   ledger shows it enqueued-then-deposited. Then: ticket cursor → [PROVED] with
   distinctions; charter deltas (`cairn/chart/intention+why.json` + retire edge
   (l) in `cairn/build_inspector/intention+why.json`) and in the SAME act run
   `cairn/intentions_model_compiler/recompile_gate.sh`; commit + push.

Sail step 6 (answer the chart): run the validate berth's three criteria by
their named instruments, then write the verdict artifact with
`cairn.chart.verdict.write_verdict` (claims verbatim from the berths, evidence
from real runs — narration refuses at the gate), then cross PROVED.

## Rules that override any habit you have
- Bounds `out` is OUT (no berth deposits on the ledger, no clocks/daemons, no
  db-backed ledger, no compaction). A bounds question goes in your report.
- Report reds with their output; skipped steps reported as skipped.
- No CI/workflows/Actions. Nothing in `~/.cairn` goes into git.
- Mid-build corrections/doubts → final report only; do NOT edit tickets you
  don't own, other charters, or memory files.
- Run proofs twice always; never trust the first green.
- Commit often. End every commit with exactly:
  ```
  Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Dsdby9vruqwUkmTroRtqk8
  ```
- Verify done by instrument: `PYTHONPATH=$PWD python3 -m cairn.orient.orient git`
  → 0 dirty / 0 ahead in both repos at your close.

## Your final report must carry
1. What stands. 2. Proof evidence verbatim (all runs + seals + the ledger's
real lines at close). 3. The verdict artifact path + what it answered.
4. Files touched + commit hashes. 5. Any finding/doubt/kick-back — especially
anything the berths got wrong (that is signal, not failure).
