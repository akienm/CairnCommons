# I-learns-its-gates — the system learns which calls are its own

*Proposed 2026-07-16 by CC; cast via /intent → /sorted, then reframed under
/challenge (Akien): the founding intention is gate-learning, not Akien-removal.
**State: RATIFIED by Akien 2026-07-16** (signature gate passed), with one amendment
folded in — build now, not someday (see Approach). Peer of [[I-cairn-claude-md]] in
the intention layer. Migrates into the intention envelope when that schema lands
(MAP.md Q6).*

The system learns its own gates. For every gate — every point where a choice could
be made without Akien — it holds a **confidence** that acting alone is safe, and it
moves that confidence with evidence from two engines:

- **Derivation** — the call follows from the standing intentions (the graph-tree
  reasoner's answer);
- **Experience** — accumulated observation of acting, and of being corrected (the
  learned-memory answer).

Confidence crosses a gate's threshold → the gate opens; counter-evidence → it closes
again. **Every gate is a hypothesis under Law 3, including the founding ones.** Each
core principle is held at ~90%, not as the one true and only answer — so even what
Akien said at the beginning can be overwritten by overwhelming evidence to the
contrary. A system that learns *and* improves itself is a system that can learn its
gates.

**Why (the reframe that sets the trace):** Cairn *is* an inference-automation system
— it compiles inference into code and knowledge into graph trees. So the system
learning which calls are its own is not a convenience; it is that compilation
happening on the system's own decision-authority. "Akien out of operating" is what
this looks like from his side as it works — the **lead falsifier**, not the aim.

**Not Akien-specific.** Gate-learning supports every mind-type Cairn hosts, not only
the graph-tree reasoners. The friction-reduction a given mind-type accumulates is
*that mind-type's* — **CC preferences** for a Claude Code mind — meaning not
settings, but choices it learned reduce friction, recorded for its own later use.
Home: that mind's **shim** (future: devices + shims + a bus; Law 6 — the shim owns
its preferences). **Interim home: the Claude Code harness auto-memory (`~/.claude`),
carried as an IOU that migrates into the CC shim when shims exist.** (Corollary:
Cairn's own knowledge parked in instance-space is on-loan, not at rest.)

**Approach — build now, not someday (ratified amendment, 2026-07-16).** The learning
is not deferred to when the shim/bus architecture matures; it starts today, in
primitive form, and grows. From now on **"how does this component learn?" is asked of
every component we build** — it will not fit everywhere, but we ask how it fits
*before* discarding it, never the reverse. The learning-injection is a **pattern**: a
common process where only the endpoints change (what the component is, what its gates
are, what counts as evidence for it). This is a standing practice, not a phase — it
is what we do. All of our chat logs feed the learning; most of it migrates into graph
trees later, once more of the system is built.

**Traces to:** Telos 1 (demonstrate inference compilation — the release *is* the
demonstration), Telos 4 (thinks the way Akien does — it must make his calls),
Telos 5 (self-improving — learning gates is self-improvement). Mechanism: Law 4
(physics over policy), Law 3 (gates as hypotheses), Law 6 (the shim owns its
preferences).

**Design constraints (from the challenge — load-bearing, not optional):**
- A gate carries **confidence + provenance**, never a boolean. The two engines
  cross-check; when derivation and experience disagree, that disagreement is itself
  a high-value signal to surface to Akien.
- **Asymmetric update, ceilings on the dangerous gates.** Counter-evidence lowers
  confidence faster than confirming evidence raises it. Irreversible / outward gates
  carry a confidence **ceiling below** the autonomy threshold — they never auto-open,
  no matter how much experience accumulates. This is how gate-learning coexists with
  "confirm before irreversible" instead of eating it.
- **Silence ≠ approval.** The feedback signal is sparse and negatively biased (Akien
  mostly speaks when something is wrong). Absence of a negative is weak evidence; an
  explicit positive is strong. The update math must treat them differently or drift
  to overconfidence.
- **~90% is a per-gate default prior, not a universal constant.** Thresholds are
  per-gate; a Telos aim and a formatting choice do not share a meaning at the same
  number.
- **The feedback record is richer than CC++/CC--:** the decision, its context, the
  outcome, Akien's correction if any, and *which gate it is evidence about* — so each
  datum moves a specific gate rather than logging a mood.

**Distinctions recorded (not collisions):**
- vs **Telos 1** — Telos 1 is the capability (inference compiles); this aims that
  capability at the system's own decision-authority and binds falsifiers to it.
- vs **the confirm-before-irreversible/outward discipline** — preserved by the
  confidence ceiling on dangerous gates; autonomy covers the settled, never the
  novel, risky, or outward.

**Falsifier:**
- *Done (asymptotic):* the system runs a full cycle — intent → build → prove →
  commit → recover-from-restart — with Akien touching it only at genuine signature
  gates; operational-touches-per-cycle trends to zero while intent-touches persist;
  **and** gate-confidences visibly move on evidence rather than sitting frozen at
  their priors.
- *Wrong-intent, three ways:* (a) it removes Akien from a steering call that was
  genuinely his — mis-scoped, it is out of operating, not out of steering; (b) it
  lowers a dangerous gate from "experience" and acts past his authority — the ceiling
  failed; (c) confidences never move — then it is not *learning* gates, only
  executing fixed ones, and the founding claim is false.

**Horizon:** re-checked when a new gate-dependency on Akien is discovered (each a
candidate child node); when a wrong-intent signal fires; and when the shim/bus
architecture lands (the CC-preferences home migrates then).

**Open question (recorded, not yet resolved):** is CC-preference data
commons-shared (a fresh CC on another device inherits the accumulated wisdom) or
instance-local (this device's CC only)? The shim owns it either way (Law 6); its
shareability is a distinct call for the shim's charter.

**Spawned / related work:**
- *akien-out-of-operating* — the lead falsifier, ongoing.
- *default-superclaude-to-200k* — validated 2026-07-16; the first gate turned to
  physics (a paging-dependency removed).
- *cc-learning-store* (ticket, code-seam) — the concrete first mechanism: a feedback
  record richer than CC++/CC--, capturing today. The first endpoint of the pattern.
- *learning-as-a-pattern* (ticket, code-seam) — "how does this component learn?" as a
  contract question asked of every component; the shared process with pluggable
  endpoints, crystallizing once cc-learning-store + a second endpoint exist.
