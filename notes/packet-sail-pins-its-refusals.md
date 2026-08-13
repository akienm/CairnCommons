# BUILD PACKET — ticket `sail-pins-its-refusals` (tier: haiku; escalate to sonnet on failure)

You are the builder for one Cairn stone — the smallest in the batch. You have
minimal context BY DESIGN — everything you need is in the files below; the
gates judge your work by instrument. Do not improvise beyond the berths.

## Read first, in this order
1. `/home/akien/dev/src/cairn/CLAUDE.md` (the Laws)
2. `/home/akien/dev/src/CairnCommons/tickets/sail-pins-its-refusals.json` (your ticket)
3. `/home/akien/dev/src/cairn/skills/sail/SKILL.md` (BOTH the liturgy you follow AND the file your proof reads)
4. The seven chart berths that claim your ticket (build ONLY inside them):
   - `~/.cairn/devices/chart/0/packets/orient-20260729T114100-a83a0d698732.json`
   - `~/.cairn/devices/chart/0/packets/constrain-20260729T114130-6b75f7c41004.json`
   - `~/.cairn/devices/chart/0/packets/survey-20260729T114205-5b83b3189844.json`
   - `~/.cairn/devices/chart/0/packets/decompose-20260729T114227-bf99a6bec19e.json`
   - `~/.cairn/devices/chart/0/packets/triage-20260729T114241-df9a32816c10.json`
   - `~/.cairn/devices/chart/0/packets/hypothesize-20260729T114303-3545cf5ba067.json`
   - `~/.cairn/devices/chart/0/packets/validate-20260729T114321-7904c5f6244e.json`

## Environment
- Code repo: `/home/akien/dev/src/cairn` — run from here with `PYTHONPATH=$PWD`.
  Knowledge repo: `/home/akien/dev/src/CairnCommons`. `git pull` both first.
  Work on main. Push when done.
- Your voyage journals at `skills/sail/` (its history.json exists — a sibling
  stone just gave skills their record), carrying your ticket. Your ticket is a
  CODE-SEAM, so your voyage's workflow string is your ticket's own:
  ```
  PYTHONPATH=$PWD python3 -c "
  from cairn.tools.base.transitions import emit
  print(emit('code-seam@v1: [THINKME] -> TICKETME -> BUILDME -> PROVEME -> LEARNME -> PROVED',
             'BUILDME', history_path='skills/sail/history.json',
             state_path='skills/sail/state.json',
             ticket='sail-pins-its-refusals', note='<why this crossing>'))"
  ```
  then use the returned string's successor for each later crossing (PROVEME,
  LEARNME, PROVED). NEVER hand-edit history.json/state.json.

## What you build (the berths hold the full design; summary only)
One proof file: `skills/sail/proofs/test_sail_liturgy.py`, reading the REAL
SKILL.md (path resolved relative to the proof's own `__file__` — a fixture
copy as subject must be structurally impossible). Checker functions applied to
text, plus teeth:
- refusal contract present and imperative: berths-required routing to /chart,
  cast-ticket-required routing to /sorted;
- act ORDER by relative position, never printed step numbers: BUILDME journal
  before build; answer-the-chart act before the PROVED crossing; seal follows
  PROVEME;
- gate names resolve by REAL import from cairn.tools.base.transitions: BuildGateRed,
  EntryGateRed, ExitGateRed;
- mutation teeth: run the same checkers over mutated copies of the TEXT (a
  reordered version, a dropped refusal clause, an orphaned gate name) and
  assert each reds — while the honest current file greens, and an honest
  renumbering of headings would still green (structure, not phrasing).
Then: run it twice (green both), seal twice under
`TesterDevice().run_proof('skills/sail/proofs/test_sail_liturgy.py',
caller='ticket sail-pins-its-refusals', isolation='netns')` +
`persist_validation` (validations land beside the skill). If the tester
refuses the skills/ path: do NOT modify the tester — report it; the
double-green stands as the honest seal state (the constrain berth pre-settled
this disposition).
Records: retire edge (b) in `skills/sail/intention+why.json` (mark it LANDED,
name your ticket) and poke `cairn/tools/intentions_model_compiler/recompile_gate.sh`
in the same act; ticket cursor → [PROVED] with distinctions; sail step 6
(answer the validate berth's two criteria by their named instruments, write
the verdict artifact via `cairn.machines.chart.verdict.write_verdict`); cross PROVED;
step-8 deposits (`python3 -m cairn.machines.chart.live learn <berth>` for each of your
seven berths); commit + push both repos.

## Rules that override any habit you have
- Do NOT rewrite SKILL.md. If a tooth finds a real defect in it, report the
  finding — a kick-back, never a silent fix.
- Bounds `out` is OUT (no /chart twin proof, no step-number or wording pins,
  no tester changes). Run proofs twice; report reds with output.
- No CI/workflows/Actions. Nothing in `~/.cairn` goes into git.
- Corrections/doubts → final report only; touch nothing beyond what the berths
  name.
- Commit often. End every commit with exactly:
  ```
  Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Dsdby9vruqwUkmTroRtqk8
  ```
- Verify done by instrument: `PYTHONPATH=$PWD python3 -m cairn.tools.orient.orient git`
  → 0 dirty / 0 ahead both repos.

## Your final report must carry
1. What stands. 2. Proof evidence verbatim (both runs, both seals or the
tester's refusal). 3. Verdict artifact path + what it answered. 4. Files
touched + commit hashes. 5. Any finding/doubt — especially anything the berths
got wrong.
