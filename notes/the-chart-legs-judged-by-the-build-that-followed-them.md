# The chart legs, judged by the build that followed them

**Voyage:** `constrain-discovers-and-runs-the-instruments-that-will-judge-the-build`
(chart chain 2026-08-14 17:00–17:12, build closed PROVED 17:37).
**Written at:** /sail step 9, by hand — nothing counts tool calls or observes them yet
(ticket `the-builds-tool-calls-are-evidence-about-the-chart`), so this file is what a hand
can do without any of it.

Akien, 2026-08-14: /sail *"runs in sail, gets feedback about tool calls that happen inside
the build. and we add that feedback into our mechanisms."* The chain said where the work
lives, what bounds it, and what already existed. **The tool calls are the only place those
claims met the world.** What follows is each claim that met the world and lost, with the
call that beat it.

---

## 0. THE COUNT COMES FIRST, BECAUSE IT NEEDS NO JUDGEMENT

**141 tool calls between the validate berth and done** (Bash 107, Edit 18, Read 9,
Write 6, Skill 1). Measured, not estimated: counted out of this session's own transcript
jsonl on disk, `tool_use` blocks in assistant records stamped at or after the validate
berth's 17:11:57, the transcript's UTC stamps shifted to local to compare against the
berth's.

Read downward, per the ruling: *"you can score the quality of the information downward
just by doing more tool calls before the build is done."* 141 is a large number and this
file does not soften it.

**AND THE RAW COUNT CANNOT SEPARATE THE TWO THINGS IT IS MADE OF**, which is a finding
about the measure rather than an excuse for the number. A tool call in this window is
either (a) work the build genuinely required — writing the module, planting fixtures,
running the tester four times under mutation, crossing four gates — or (b) a lookup the
packet should have saved, which is the only half the score is about. The count merges
them. Both readings are consistent with 141, and nothing on disk distinguishes them
today. That is precisely the gap ticket `the-builds-tool-calls-are-evidence-about-the-chart`
names: the instrument must OBSERVE the calls, not tally them. Until it exists, the number
is a coarse measurement to sharpen (Law 10), not a verdict — and it is recorded rather
than narrated so a sharper instrument has something to disagree with.

---

## 1. SURVEY RECORDED AN ABSENCE THAT WAS NOT ABSENT

**The claim it falsifies** — survey berth `survey-20260814T170720-476c08ebe757`, an
absence whose `measure` reported the tester's collector as not reachable for composition.

**The call that beat it** — `from cairn.devices.tester.cli import discover` in the build's
first minute. It imported. It had been importable the whole time.

**Why it matters beyond the instance.** The absence's measure was an import attempt that
failed for a *different reason than the one it was read as*. An absence is a claim (the
survey door enforces that much — it refuses a measureless absence), but the door cannot
check that the measure measured the thing its author thought. **A failing probe and an
absent thing produce the same red**, and the survey stage has no way to tell them apart.
This is the same shape as `barren_refs` in this build's own probe, where it was
anticipated and handled — and the anticipation lived in the probe, not in the stage.

**What it cost, and what saved it.** It nearly cost the whole point: the decompose leg had
already begun to treat DISCOVERY as something to *write*. What saved it was checking the
holding before building it, which is `borrow-patterns-cite-dont-graft` and
`build-minimal-grow-against-need` doing their job — the survey was wrong, and the habit
downstream of it was right.

---

## 2. DECOMPOSE GAVE A PIECE THE WRONG KIND, AND THE WRONG KIND WAS THE EXPENSIVE ONE

**The claim it falsifies** — decompose berth `decompose-20260814T170847-6d21fdd1405d`,
the DISCOVERY piece declared `kind: "build"` against a measured absence.

**The call that beat it** — the same import. Once `discover` was reachable, DISCOVERY was
a **compose** piece using an existing holding, not a build piece filling an absence.

**Why it matters.** The kinds are not labels; they are the physics of build-minimal. A
`build` piece licenses new code, a `compose` piece does not. **A wrong kind licenses
exactly the duplication the survey exists to prevent** — and it inherits its wrongness
from finding 1 without any door in between able to catch it, because decompose's judges
check that a build piece names a *measured* absence, never that the absence is *true*.
The chain carries an error forward with full formal validity: every door passed.

The shipped code is right — `discovered_instruments` composes `discover` — so this cost
nothing in the end. It cost nothing because a human-shaped check caught it, which is the
part that does not scale.

---

## 3. NOTHING IN SEVEN STAGES ASKED WHAT THE ARTIFACT DOES WHEN IT RUNS INSIDE ITSELF

**The claim it falsifies** — no single field; the gap is in the chain's *question set*.
Orient grounded it, constrain bounded it, survey inventoried it, decompose split it,
triage ordered it, hypothesize predicted it, validate said what done means. **None asked:
this build makes a floor that RUNS PROOFS, and this component's own proofs CALL THAT
FLOOR — seventeen times.**

**The call that beat it** — the first full run of `test_chart_constrain.py` after the run
half landed, which would have forked the tester recursively without bound. The hazard was
found *while building*, by a builder who happened to look, and was answered with
`CAIRN_CONSTRAIN_FLOOR_RUNNING` inherited across the subprocess boundary — depth capped at
one by physics rather than by an exclusion roster someone maintains.

**Why it matters.** This is the one finding here that no existing door would have caught,
and the only one that could have been *dangerous* rather than merely wrong. The general
shape, offered without a mechanism attached because inventing one here would be the
reification failure this corpus keeps recording: **when the artifact under construction is
of the same kind as the tooling that judges it, the chain has a self-reference question to
ask and currently asks none.** Named at its measured size; whether it earns a stage field,
a floor check, or nothing at all is a question, not a design.

---

## 4. THE DEPOSIT FACE RE-VALIDATES A HISTORICAL PACKET AGAINST A FLOOR THAT HAS MOVED

**The call that produced it** —
`python3 -m skills.chart.live learn .../constrain-20260814T170159-7ff139d9c0eb.json`,
run at step 9 over this voyage's own seven berths. Six deposited (idempotent,
`duplicate: true`). The constrain one **refused**:

```
ConstrainRefused: constrain refuses a packet that declares its own provenance for
constraints — ... Declared vs measured: constraints declared 'floor', measured 'claude'.
```

**What actually happened.** `deposit_constrain` calls `validate_constrain`, which
re-derives provenance by re-running the floor over the packet's own `intent_ref` and
comparing. The packet was authored at 17:01 when the floor emitted 6 charter constraints;
the floor now emits 6 charter constraints **and 9 check constraints**, so the reproduction
fails and the packet — which was honestly `floor` when written and is a correct record of
what happened — can never be deposited again.

**Nothing was lost here**, and that was measured rather than assumed: `live counsel …
constrain` returns node `b796cc0b74188748` sourced from that exact berth, created
2026-08-14 17:02:05. The chart-time deposit had already landed.

**Why it is still a finding.** Provenance is a claim about **who authored a field, at the
time it was authored**. The door tests it as a claim about **now**. That is the
snapshot-versus-invariant failure this corpus already records, running in the other
direction: instead of a check that goes green because a snapshot happened to match, a check
that goes red because the world moved on from a record that was true. Two consequences,
both structural rather than hypothetical:

- **every constrain packet berthed before today is now permanently undepositable** — the
  same measurement will fail on all 43;
- **a voyage that skipped the chart-time deposit and shipped first would strand its own
  packet**, and would find out only at close.

**Disposition: recorded, NOT fixed.** The provenance door is not in this ticket's `in`
bounds (`constrain.py` is in scope only for the discovery half, the run half, and their
emission), and widening bounds mid-build is Akien's gate, never a silent act. It goes to
the carried backlog for `/sorted` under the name
**`the-deposit-re-judges-a-historical-packet-against-a-floor-that-moved`**.

---

## 5. WHAT THE CHAIN GOT RIGHT, RECORDED BECAUSE A LEDGER OF ONLY FAILURES IS NOT A MEASUREMENT

- **The mechanical collision was found before building** — the `crowding_out` probe, armed
  hours earlier, would have read the floor's own bulk as evidence the ceiling was healthy
  the moment a new kind appeared. The chart caught the instrument flattering the thing it
  measures, before it flattered anything.
- **The hypothesize leg predicted its own most valuable kill in advance**, verbatim: *"a
  source that resolves but does not identify is the laundered-provenance failure in a new
  place."* It happened. Seven hypotheses confirmed, one killed, and the killed one is the
  only one that changed the code.
- **The bounds held.** `out` named the four follow-on categories, the dial, the judging
  components, and hex.local. Nothing outside them was touched — including the shared judge,
  where the fix would have been easier and would have been a silent widening.

---

## The shape of all four findings together

Three of the four (1, 2, 4) are the same failure wearing different clothes: **a record that
was true when written, read later as though it were a claim about the present.** The
survey's absence was true of the author's knowledge; the decompose kind was true given the
survey; the provenance was true of the floor that day. Every door passed on every one of
them, because the doors check *shape and internal consistency* and the error is *temporal*.

Finding 3 is not that. It is a question the chain does not ask.

Nothing here is proposed as a mechanism. Each is a measurement with the call that took it,
which is the state a thing has to reach before it can honestly be designed for.
