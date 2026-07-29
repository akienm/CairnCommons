# BUILD PACKET — ticket `skills-ride-the-chokepoint` (tier: sonnet)

You are the builder for one Cairn stone. You have minimal context BY DESIGN —
everything you need is in the files below; the gates judge your work by
instrument. Do not improvise beyond the berths.

## Read first, in this order
1. `/home/akien/dev/src/cairn/CLAUDE.md` (the Laws)
2. `/home/akien/dev/src/CairnCommons/tickets/skills-ride-the-chokepoint.json` (your ticket)
3. `/home/akien/dev/src/cairn/skills/sail/SKILL.md` (the build liturgy — follow ALL its steps)
4. The seven chart berths that claim your ticket (build ONLY inside them):
   - `~/.cairn/devices/chart/0/packets/orient-20260729T113711-3d1c16b2d28f.json`
   - `~/.cairn/devices/chart/0/packets/constrain-20260729T113807-279e91bf8194.json`
   - `~/.cairn/devices/chart/0/packets/survey-20260729T113841-dff3aebc809a.json`
   - `~/.cairn/devices/chart/0/packets/decompose-20260729T113912-98b6f57144d0.json`
   - `~/.cairn/devices/chart/0/packets/triage-20260729T113930-eacedd4488a0.json`
   - `~/.cairn/devices/chart/0/packets/hypothesize-20260729T113957-70a60faa6a2f.json`
   - `~/.cairn/devices/chart/0/packets/validate-20260729T114021-166e2a9d70fc.json`

## Environment
- Code repo: `/home/akien/dev/src/cairn` — run from here with `PYTHONPATH=$PWD`.
  Knowledge repo: `/home/akien/dev/src/CairnCommons`. `git pull` both first
  (two sibling stones landed at the chokepoint before you: every forward
  BUILDME/PROVED crossing must name its cast ticket, and an exit-gate-clean
  PROVED crossing auto-enqueues its verdict for tree deposit). Work on main.
- Your voyage journals at the parent component `cairn/base/` (history.json +
  state.json), carrying your ticket:
  ```
  PYTHONPATH=$PWD python3 -c "
  from cairn.base.transitions import emit
  import json
  cur = json.load(open('cairn/base/state.json'))['workflow']
  print(emit(cur, 'BUILDME', history_path='cairn/base/history.json',
             state_path='cairn/base/state.json',
             ticket='skills-ride-the-chokepoint', note='<why this crossing>'))"
  ```
  (Same for PROVEME, LEARNME, PROVED. NEVER hand-edit history/state. If
  cairn/base has no state.json yet, report that instead of inventing one.)
- Seal proofs twice + persist_validation — same pattern as every stone
  (TesterDevice().run_proof(path, caller='ticket skills-ride-the-chokepoint',
  isolation='netns'); assert green+sealed; persist_validation last).

## What you build (the berths hold the full design; summary only)
In triage's order:
1. **The registration** — add `workflow_versions.v1` to
   `/home/akien/dev/src/CairnCommons/node_classes/skill.json`, mirroring the
   structure of code-seam.json's entry: path = the six summonses (THINKME,
   TICKETME, BUILDME, PROVEME, LEARNME, PROVED), skippable_summons =
   ["TICKETME"], and a `why` carrying the settled design (prove_gate maps to
   PROVEME; /challenge is a kick-back to PROVEME, not a seventh stage; cairnmap
   stays a labeled IOU). Change NOTHING else in that file (invariant,
   prove_gate, members_so_far intact). ZERO changes to transitions.py — if any
   code edit seems needed, STOP and report (the registry-is-the-door claim
   would be false; that's a finding).
2. **The teeth** — extend `cairn/base/proofs/test_transitions.py`: a skill@v1
   string validates and journals a crossing at a fixture skill address; a
   drifted skill path refuses; an unknown class still refuses; the entry gate
   fires identically on a skill-class voyage naming a cast ticket; every
   existing tooth untouched and green. Prove twice, seal, persist.
3. **The first history** — live fire: journal the sail NODE's first real
   crossing at `skills/sail/` (history.json + state.json created by the
   projector's append door via emit). The workflow string starts fresh:
   `skill@v1: [THINKME] -> TICKETME -> BUILDME -> PROVEME -> LEARNME -> PROVED`
   crossing THINKME→BUILDME (TICKETME skippable), naming ticket
   `skills-ride-the-chokepoint` and a note that the RECORD starts mid-life
   (the skill itself proved out in prose 2026-07-28; this is its record's
   birth, not its own). The entry gate will judge the claim — your chart
   claims this ticket, so it stands.
4. **Records settle** — retire sail charter edge (d) in
   `skills/sail/intention+why.json`; both charter deltas (node_classes/skill.json
   + sail charter) poke `cairn/intentions_model_compiler/recompile_gate.sh` in
   the same act; ticket cursor → [PROVED] with distinctions; sail step 6
   (answer the chart: run the validate berth's two criteria by their named
   instruments, `cairn.chart.verdict.write_verdict`); cross PROVED; step-8
   deposits (`python3 -m cairn.chart.live learn <berth>` per berth); commit +
   push both repos.

## Rules that override any habit you have
- Bounds `out` is OUT (no other class registered, no cairnmap build, no
  retro-migration of other skills). Bounds questions → report, not widening.
- Report reds with output; skipped steps as skipped. Run proofs twice.
- No CI/workflows/Actions. Nothing in `~/.cairn` goes into git.
- Corrections/doubts → final report only; touch no tickets/charters/memory
  beyond those the berths name.
- Commit often. End every commit with exactly:
  ```
  Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Dsdby9vruqwUkmTroRtqk8
  ```
- Verify done by instrument: `PYTHONPATH=$PWD python3 -m cairn.orient.orient git`
  → 0 dirty / 0 ahead both repos.

## Your final report must carry
1. What stands. 2. Proof evidence verbatim (runs + seals + the sail history's
first record verbatim). 3. Verdict artifact path + what it answered. 4. Files
touched + commit hashes. 5. Any finding/doubt — especially anything the berths
got wrong.
