# Deep review, 2026-08-15 morning — post-remodel, post-Fable-switch

Asked for by Akien with 17 minutes on the clock: "our own rules aren't really
changing fast enough to keep up" with the rulings; "check the deterministic
inspectors and gates first." Every claim below is a measurement taken this
morning, with the instrument named.

## Verdict: NOT lgtm — the deterministic core IS solid; the mess is in the seams between records and their readers.

## What measured solid (where he pointed first)

- **Build inspectors**: `inspect(component=...)` on constrain, orient (both
  rungs — it correctly inspected 2 components for the ambiguous name), verdict:
  all `clean: true`. And handed a wrong component path it REFUSED loudly with
  the census list ("a gate that silently inspects nothing passes everything,
  Law 8") — the refusal shape works.
- **Repos**: orient git — both repos 0 ahead, 0 behind, 0 dirty.
- **The staleness detector built 2026-08-14 works**: the ground loop measured
  ITSELF older than the code and named itself instead of benching constrain.

## Finding 1 — the ground loop knows it is stale and stays stale (biggest)

Pid 897888, started Aug 14, measured itself REWRITTEN-under (constrain.py,
9 occurrences at 23:14 on 08-14). The trouble record's disposition says
"Restart the loop." Nine-plus hours later: same pid, still stale, **65% CPU /
616 CPU-minutes** (the known 2500ms-beat-vs-1s-cadence defect compounding).
The voyage built the *naming* half; **nobody owns the restart** — a detector
with no actuator, so the watch layer has been dark-while-looking-alive since
yesterday evening. Discuss: does the loop restart itself (exec) when it
measures its own staleness, or does the trouble fire a restart at a holder?

## Finding 2 — a cleared trouble still shouts, because my hand-clear wrote prose into an enum

`ground-loop-device-constrain` standing is `"CLEARED — the folder imports and
…"` (my hand-clear, 08-14). The session-open banner still lists it LIVE — the
deterministic reader wants the bare word and gets a paragraph. This is the
missing trouble-closing door biting for the second time: the door would have
written the value the reader parses. Records-go-through-their-door, n+1.

## Finding 3 — the ruling lag, MEASURED (his actual question)

Rulings live in `CairnCommons/decisions/` (not rulings/). Census: for each of
the 22 rulings dated 08-10→08-14, grep cairn (code+charters+skills+CLAUDE.md)
for its id. **8 of 22 have ZERO citations anywhere.** Three kinds of zero:

- **Absorbed without trace** (content in CLAUDE.md, id cited nowhere):
  `a-device-is-its-own-process` (×2 near-duplicate files),
  `tools-machines-devices-instances` (the complexity axis). Untraceable but
  not un-kept.
- **Genuinely unabsorbed**: `one-mechanism-per-meaning` (both halves, 0 cites,
  nothing enforces or even restates it);
  `open-questions-land-with-cc-and-surface-at-the-hook` — and this one is
  live: a `questions/` store EXISTS with 8 open questions, but **the four
  questions standing at Akien's gate from yesterday's constrain voyage are in
  NONE of them** (grep: 0 hits). They ride slate prose only — exactly what the
  ruling ruled against. Rules didn't keep up, measured.
- **Tracked as IOU only**: `corrosion-is-drift-with-no-ruling-behind-it` —
  in CLAUDE.md's rules-awaiting-physics via ticket name; concept-piece uncast.
- Also: `decisions/` carries near-duplicate pairs (two device-is-its-own-process,
  two corrosion incl. -baselined, two chart-is-a-skill variants) — intake is
  accreting variants rather than superseding.

## Finding 4 — the session-open banner costs ~200KB every session

28 captured SessionStart injections, 186–207KB each. The harness truncates to
a 2KB preview; the full compile is paid every session and mostly unread —
"context nothing reads is paid forever" (the slate door's own charter), parked
at the system's front door. Worth finding what the compiler is inlining.

## Not findings, still open (unchanged)

`the-runtime-spine-has-never-run` (off-template standing "?");
`workflow-cursor-unreadable-by-the-chokepoint` (open on Akien's two design
questions, code halves fixed).
