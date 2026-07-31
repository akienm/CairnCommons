# I-complete-diagnostic-on-first-pass — the report resolves it on the first pass

*Cast 2026-07-23 by CC via /intent → /sorted, from Akien's decades-proven method (his
2007 test-automation framework, the UU model, Trouble Tickets). **State: PROVED —
sealed 2026-07-25 through the quorum signature gate.** Reviewer (verdict): akien.
Notary (seal): cc — different hands, refused by physics otherwise. The seal, its
evidence and its falsifier: `intentions-not-beside-code/validations/I-complete-diagnostic-on-first-pass.json`.
It sat unsigned for two days for a purely mechanical reason worth recording: the
VALIDATION write-door derived a seal's address from a PROOF FILE path, and a
concept-piece has no proof file — so the gate was never awaiting a signature, it was
awaiting an ADDRESS (`cairn/tester/quorum.py` closed it, and this is the first
concept-piece VALIDATION in Cairn). Node-class:
concept-piece (the prose IS the implementation; a code-seam — the diagnostic
inspector — instantiates it). Migrates into the intention envelope when that schema
lands (MAP.md Q6).*

A diagnostic surface — a failure report, a system alarm, a trouble ticket — **delivers
all the data required to resolve the issue in its initial emission.** The resolver
never re-runs the thing to gather more. The first report already carries identity,
location, the exact failing code, expected-vs-actual, fatality, source, the full
trace, and every value at every transition and boundary that bears on the fault.

**Why — this is proven, not speculative.** Akien built this into a test-automation
framework in 2007 because he knew errors were coming and he was tired of running
things over and over to gather one more piece of failure data each pass. A report
that arrives complete takes a team from half-a-day-per-issue to ~10 minutes. It is
the **first tool he reaches for in debugging**, validated across decades and across
UU. So `build-minimal / grow-against-need` — the rule for *unproven* ideas — does not
gate it; a proven first-reach tool is infra you build **ahead** of need, the way you
build logging before you need it. (CC mis-filed it as speculative once, 2026-07-23,
and was corrected — the why is what let the rule's boundary be adjudicated: this is
`ask-the-why-to-distinguish` lived.)

**What it sharpens and serves.**
- It **sharpens Law 7**: errors are not merely *loud* at diagnostic surfaces — the
  diagnostic surface is **complete on first emission**. Loud-but-partial still costs a
  second run; loud-and-complete does not.
- It **serves Law 1**: re-running to collect more failure data *is* re-deriving the
  settled — the exact waste a complete-first-report kills. The answered question
  ("what did I need to see?") becomes structure (a field in the report), once.

**The falsifier is a special class — a learning signal, not a terminal kill-switch.**
This is the load-bearing subtlety (Akien, 2026-07-23). A diagnostic that forces a
second run to resolve some *additional* point does **not** falsify the principle — it
is the learning loop firing. The surface has just discovered, empirically, a datum it
should have carried; that miss is **folded into the initial report** so the same gap
never costs a second run again. It is `[[I-learns-its-gates]]` pointed at the
diagnostic surface itself: the report learns its own completeness from the evidence of
what it missed. So the falsifier splits:

- *First miss of a given datum* → **learning signal.** Expected, even welcome — this
  is *how* the report grows toward completeness. Feed-forward, not a defect.
- *The same gap forcing a second run again, after it was already learned* → **the
  real, terminal falsifier.** The surface was told once and failed to consume its own
  evidence — a Law 1 defect (re-deriving the settled).

*Horizon (asymptotic, monotonic):* completeness only rises; no learned gap recurs. The
principle is "held" not when a report is ever perfect, but when every miss is reliably
folded into the next report. Re-checked each time a real mystery-red forces a second
run — did the loop fold the miss, or let it recur?

**Distinctions recorded (not collisions).**
- vs **Law 7** — Law 7 is loudness at the diagnostic surface; this is *completeness*
  of it. Loud is necessary, not sufficient. This adds "and complete on first pass."
- vs the **decision-autonomy learning** (`learning/`, `cc-learning-store`) — that store
  learns *whether CC may act alone* at a gate; this loop learns *what a report must
  carry* for a transition-class. Both are `learns-its-gates` instances with different
  endpoints (what the component is, what its gates are, what counts as evidence). Kin,
  cross-referenced, **not** merged — a distinct store with a distinct key.
- vs **the diagnostic emission** (`cairn/base/diagnostic.py`) — the emission stays a
  dumb, thin breadcrumb (Law 6: only the pointer crosses); this principle is about
  what the *inspector* assembles from the breadcrumbs and logs — the FINDINGS. The
  emission is dumb so the findings can be smart.

**Spawned / related work.**
- *diagnostic-inspector* (ticket, code-seam) — the concrete build that instantiates
  this: the inspector that reacts to a fired probe and FILTERS the emission
  breadcrumbs + timestamp-indexed logs into the complete first-pass FINDINGS, **plus**
  the learning-loop it carries that folds a forced second-run's miss into the next
  findings' completeness for that transition-class. Its explicit remit (Akien): save CC
  tokens exploring an issue as the prebuild step does for coding, and get better over
  time. (Born as *diagnostic-interpreter* / `assemble`; refactored to the
  inspector/filters/findings shape 2026-07-24.)
- *`cairn/base/diagnostic.py`* (built) — `DiagnosticBase.emit`, the transition-grade
  breadcrumb every device inherits; the inspector crawls on its pointer + microsecond
  stamp. The docstring already named this inspector as "the next build."
- Kin: `[[diagnostic-logging-method]]` (the how — instrument → interpret → review →
  fix) is the operating procedure this principle is the why for.
