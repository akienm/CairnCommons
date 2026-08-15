# The gate drains — a curated review of the 134 findings

Written by CC (Fable), 2026-08-15, under Akien's directive: *"review all the open
stuff... see what can be simply closed... and then i should review the rest. same
with alarms, anything you don't need me for, great, that's a win."*

**What this is:** all 134 pending findings at your `recordverdict` gate, read whole
(the full dump was pulled through `pending_findings()`, not skimmed from the session
banner), and partitioned into **17 that genuinely need your eyes** and **117 that
are honest voyage-close records of work that has since PROVED, landed, or been
overtaken** — bulk-approvable in one sitting.

**What this is not:** verdicts. The gate is yours; CC verdicting CC's own findings
is the recorder authoring its own sign-off. Every recommendation below is a
recommendation.

**The door's mechanics (verified in `cairn/machines/learning_block/__main__.py`):**
one command judges one finding — a multi-match target is refused by design ("an
ambiguous act is never guessed"). There is no sweep verb. So the bulk drain is a
shell loop: your words typed once, fired per finding. Your 2026-08-01 automation
intent ("we'll need to automate this gating process") already lives in ticket
`recordverdict-cli-door`; no new ticket minted for this.

---

> **UPDATE, same day:** Akien's authority ruling
> (`2026-08-15-measurement-trumps-approval-and-the-head-trumps-artifacts`:
> measurement > his head > every artifact, his commits included) drained two of
> the 17 — **355143331fff** (his commits ARE subject to the corrosion predicate;
> artifacts below his head) and **8d47765deb56** (the two-tense ruling's
> `confirmed: true` is on disk — measurement-settled, no marker owed) — both
> recorded through `recordverdict` with his verbatim words. **15 remain.** The
> same ruling means Part 3's runtime-spine clear stands on its measurement and
> needs no ratification; only the residue ticket-or-drop call is still yours.

## Part 1 — the 15 that need you (read each finding's own bullets before answering: `cairn recordverdict <id>` alone won't show it, but the id is answerable directly and the bullets live in the block's record)

### One-word closes (cheap, do these first)

- **d4896172aa8c** — minor pane flag; approve or drop.
- ~~8d47765deb56~~ — drained by the authority ruling (see update above).

### Genuine design questions parked on you

- **d830a3f80723** — `mint_grant`: should capability grants stay flat, or nest?
- **3fa4f993e4b8** — does an **at-rest** component's absent journal red at all,
  or only a voyage's? (Bears on the state/history drift check's scope.)
- ~~355143331fff~~ — drained by the authority ruling: your commits are
  artifacts below your head, so the predicate applies to them like any other.
- **394d1cb8c2fa** — orient vs constrain carry different survival rules under one
  dial number; which is authoritative?
- **cd4f046cd7d5** — the trouble-closing CLI door is still owed (clears currently
  fire via Python one-liners; today's runtime-spine clear included).
- **2e3dd39ad06f** — band rework blocked on your config-surface question.
- **e452bbd616b5 / 31d24b804f12** — process-boundary sequencing pair; answer
  together.

### Standing at your gate for ratification

- **b8e4233e9073** — the concept-piece verdict was parked explicitly on your
  review; the first concept-piece voyage has since closed whole (2026-08-15).
- **a66cbfa44fa5** — two of its bullets are measurement-settled (live-fired
  singleton start; SIGKILL tooth) and stand on that. What queues is the FLAG
  bullet: CC marked BUILDME need 2 "DONE" as *a read of the record* — an
  interpretation, not a measurement, so it's yours under the authority ruling.

### Confessions worth your eyes (approve = acknowledged)

- **3d8ae5b96975 / 385e4f211d2f** — CC walked past the live trouble list; the
  pair is the record of it.

### Riders on tickets you still hold open

- **5994e0e0c332** — rides the ticket-and-task decision.
- **88094b7f93b0** — rides `the-corpus-is-out-of-proven-space`.

### Worked example of "overtaken by events"

- **1204dd303847** — claimed "concept-piece has no workflow"; the 2026-08-15
  first concept-piece voyage IS that workflow, run to PROVED. Recommend approve
  with a word noting events closed it. It's the cleanest specimen of what most
  of the 117 below look like.

---

## Part 2 — the 117 bulk-approve candidates

Character: voyage-close bullets (skill:saveslate, skill:intent, skill:sorted,
chart-stage learnings) from 2026-08-03 → 2026-08-15 recording work that has since
PROVED, landed in physics, or been superseded by a later build you already
ratified. None of them parks a question on you; each is a learning record whose
approval feeds the block's dial.

Drain them — **your words, typed once** (edit the WORDS line; the loop excludes
the 17 above):

```bash
cd ~/dev/src/cairn
WORDS="approved — reviewed in the 2026-08-15 curated sweep; voyage-close records of work since proved or landed"
MUSTREAD="8d47765deb56 b8e4233e9073 d830a3f80723 a66cbfa44fa5 3fa4f993e4b8 355143331fff 394d1cb8c2fa cd4f046cd7d5 2e3dd39ad06f e452bbd616b5 31d24b804f12 3d8ae5b96975 385e4f211d2f 5994e0e0c332 88094b7f93b0 d4896172aa8c 1204dd303847"
PYTHONPATH=. python3 -c "
from cairn.machines.learning_block import learning_block as lb
must = '''$MUSTREAD'''.split()
for f in lb.pending_findings():
    i = str(f.get('id',''))
    if not any(i.startswith(m) for m in must):
        print(i)
" | while read id; do
  PYTHONPATH=. python3 -m cairn.machines.learning_block recordverdict "$id" approve "$WORDS"
done
```

Each firing writes through the day-file door (`CairnCommons/learning/`), the sole
write path — nothing here bypasses anything. If any of the 117 deserves a closer
look, pull it out of the loop by adding its id to `MUSTREAD` first; nothing is
lost by deferring one.

---

## Part 3 — same-sitting acts adjacent to the gate

1. **Clear the workflow-cursor trouble** (last live one). CC already cleared it
   2026-08-10 with full measurement (96/96 live tickets parse; sorted's door runs
   `parse_workflow` at cast; three pre-era nodes migrated). It stays live only
   because `notified: ["akien"]` — the lane holds it until *you* say so:

   ```bash
   cd ~/dev/src/cairn
   PYTHONPATH=. python3 -c "
   from cairn.devices.trouble.trouble import TroubleDevice
   print(TroubleDevice().clear('workflow-cursor-unreadable-by-the-chokepoint',
       by='akien',
       what_changed='<your words — e.g.: the chokepoint parses every live cursor and the cast door refuses a drifted one; the residue is ticketed>'))
   "
   ```

2. **Runtime-spine trouble: cleared by CC today** (2026-08-15), through the
   device door, after live measurement (loop beating, beats 5271, diagnostics
   home='sent' on disk). The clear's `what_changed` names the honest residue —
   findings 6 (chokepoint posts no breadcrumb) and 7 (emit-coverage census) were
   never ticketed; findings 8 and 9 are largely overtaken (skill_block berths
   every door firing; chart entry/exit gates). **Your call: ticket 6/7, or drop
   them.** Under the authority ruling the clear itself stands on its
   measurement and needs no ratification; only the 6/7 call is yours.

3. **Compiler charter `gated_by: ["CC"]`** — added mid-crossing 2026-08-15 under
   refusal pressure, derived from owner per base's rule, **ratification never
   sought**. Say yes or name the right hands.
