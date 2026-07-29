# BUILD PACKET — ticket `a-voyage-names-its-ticket` (tier: sonnet)

You are the builder for one Cairn stone. You have minimal context BY DESIGN —
everything you need is in the files below; the gates judge your work by
instrument. Do not improvise beyond the berths.

## Read first, in this order
1. `/home/akien/dev/src/cairn/CLAUDE.md` (the Laws — they bind everything)
2. `/home/akien/dev/src/CairnCommons/tickets/a-voyage-names-its-ticket.json` (your ticket)
3. `/home/akien/dev/src/cairn/skills/sail/SKILL.md` (the build liturgy — follow its steps)
4. The seven chart berths that claim your ticket (build ONLY inside them —
   constrain's bounds are hard edges, survey's holdings are what you compose,
   absences are what you build, triage's order is your order, validate's
   criteria are what your close must answer):
   - `~/.cairn/devices/chart/0/packets/orient-20260729T113259-c4afa3b858f0.json`
   - `~/.cairn/devices/chart/0/packets/constrain-20260729T113345-5d90eec55fd9.json`
   - `~/.cairn/devices/chart/0/packets/survey-20260729T113436-3b002faf174c.json`
   - `~/.cairn/devices/chart/0/packets/decompose-20260729T113500-a89acafe28b8.json`
   - `~/.cairn/devices/chart/0/packets/triage-20260729T113526-4bd219d309e1.json`
   - `~/.cairn/devices/chart/0/packets/hypothesize-20260729T113555-5adb2ac48b1e.json`
   - `~/.cairn/devices/chart/0/packets/validate-20260729T113613-7d10f924d35c.json`

## Environment
- Code repo: `/home/akien/dev/src/cairn` — run everything from here with
  `PYTHONPATH=$PWD`. Knowledge repo: `/home/akien/dev/src/CairnCommons`.
- `git pull` both repos before starting. Work on main. Push when done.
- Your voyage journals at the parent component `cairn/build_inspector/`
  (history.json + state.json there), carrying your ticket:
  ```
  PYTHONPATH=$PWD python3 -c "
  from cairn.base.transitions import emit
  import json
  cur = json.load(open('cairn/build_inspector/state.json'))['workflow']
  print(emit(cur, 'BUILDME', history_path='cairn/build_inspector/history.json',
             state_path='cairn/build_inspector/state.json',
             ticket='a-voyage-names-its-ticket', note='<why this crossing>'))"
  ```
  (Same idiom for PROVEME, LEARNME. NEVER hand-edit history.json/state.json.)
- Seal proofs:
  ```
  PYTHONPATH=$PWD python3 -c "
  from cairn.tester.device import TesterDevice
  from cairn.tester.validation_store import persist_validation
  t = TesterDevice()
  for i in range(2):
      rec = t.run_proof('cairn/base/proofs/test_transitions.py',
                        caller='ticket a-voyage-names-its-ticket', isolation='netns')
      print(rec['verdict'], rec['evidence']['seal']['verdict'])
      assert rec['verdict']=='green' and rec['evidence']['seal']['verdict']=='sealed'
  persist_validation(rec, proof_path='cairn/base/proofs/test_transitions.py')"
  ```

## IMPORTANT — this stone HOLDS ITS CLOSE
Run sail steps 0–5 plus commits, then STOP and report. Do **not** write the
verdict artifact, do **not** cross PROVED, do **not** run deposits or touch
charters. Rationale: your validate criterion 2 needs "the next sibling
voyage's journaled BUILDME crossing" through your tightened door — that
sibling runs after you. The orchestrator (Fable session) will close your stone.
Your report is the handoff.

## What you build (the berths hold the full design; summary only)
One helper in `cairn/base/transitions.py` replacing the two opt-in
`isinstance(_ticket, str) and (_TICKETS / ...).exists()` checks (entry ~411-415,
exit ~421-425): a forward crossing into BUILDME or PROVED must name a cast
ticket or raise a FOURTH sibling refusal exception (distinct wording: unnamed →
route to /sorted; named-but-uncast → its own message), refusing BEFORE anything
is written. Beside it: an explicit exempt-roster constant, EMPTY in v0 (the
survey measured zero ticketless call sites), with journaling machinery so any
future roster entry passes gated-and-clean, never silently. Then the teeth
(triage piece 3 — including REWRITING the existing jurisdiction tooth that
currently asserts unnamed-passes; every OTHER pre-existing tooth must stay
green untouched), prove twice, seal, and one live dry-fire: an unnamed forward
crossing at a fixture address refused in anger with history sha256 identical
before/after.

## Rules that override any habit you have
- Bounds `out` is OUT. Wanting something out is a question for the report, not
  a silent widening.
- Report reds with their output. A skipped step is reported as skipped.
- No CI/workflows/Actions. No daemons, clocks, or polling. Nothing in `~/.cairn`
  goes in git.
- Mid-build corrections or design doubts: put them in your final report — do
  NOT deposit anything into the chart trees; do NOT edit charters, tickets, or
  memory files.
- Commit often with honest messages. End every commit with exactly:
  ```
  Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Dsdby9vruqwUkmTroRtqk8
  ```
- Verify "done" by instrument: `PYTHONPATH=$PWD python3 -m cairn.orient.orient git`
  (expect only your intended dirt before commit; 0 dirty / 0 ahead after push).

## Your final report must carry
1. What stands (one paragraph). 2. Proof evidence verbatim (both unsealed runs'
verdicts + both seal lines + the dry-fire refusal output + the sha256 pair).
3. Files touched + commit hashes. 4. Any finding/doubt/kick-back, however small.
5. The exact state you left the voyage in (expected: cursor at LEARNME, close held).
