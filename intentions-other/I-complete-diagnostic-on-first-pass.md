# I-complete-diagnostic-on-first-pass — the report resolves it on the first pass

*Cast 2026-07-23 by CC via /intent → /sorted, from Akien's decades-proven method (his
2007 test-automation framework, the UU model, Trouble Tickets). **State: CAST,
awaiting Akien's signature gate** (concept-piece quorum gate — the why goes to the
commons the moment it is written; the seal is his ratify). Node-class:
concept-piece (the prose IS the implementation; a code-seam — the diagnostic
interpreter — instantiates it). Migrates into the intention envelope when that schema
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
  what the *interpreter* assembles from the breadcrumbs and logs. The emission is
  dumb so the report can be smart.

**Spawned / related work.**
- *diagnostic-interpreter* (ticket, code-seam) — the concrete build that instantiates
  this: the crawler that assembles the complete first-pass report from the emission
  breadcrumbs + timestamp-indexed logs, **plus** the learning-loop that folds a forced
  second-run's miss into the next report's completeness for that transition-class. The
  "report + learning-loop" Akien scoped.
- *`cairn/base/diagnostic.py`* (built) — `DiagnosticBase.emit`, the transition-grade
  breadcrumb every device inherits; the interpreter crawls on its pointer + microsecond
  stamp. The docstring already named this interpreter as "the next build."
- Kin: `[[diagnostic-logging-method]]` (the how — instrument → interpret → review →
  fix) is the operating procedure this principle is the why for.
