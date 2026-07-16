# learning/ — where chat logs compile into gate-learning (v0)

The CC-preference store (ticket cc-learning-store, under intention
[[I-learns-its-gates]]). Born here in commons because losing it loses knowledge;
destined to migrate into the CC **shim** when the shim/bus architecture lands
(Law 6 — the shim owns its preferences).

**How this component learns** (dogfood — the question we now ask of every
component): it accumulates *records*, each attributing one decision-and-response to
a specific **gate**, and each carrying a **confidence-move** on that gate's
autonomy. Enough records move a gate across its threshold → the gate opens (CC acts
alone); counter-evidence moves it back. The store learns by being appended to and
re-read at like decisions.

## Record format (v0 — will change; sparse-but-real beats rich-but-empty)

One record = one datum of evidence about one gate. Fields:

- `id`, `date`, `session`
- `gate` — the decision-class this bears on (e.g. `repo-visibility`, `ci-on-github`,
  `build-now-vs-defer`). Gates are discovered as demanded, like node-classes.
- `decision` — what CC did or proposed.
- `signal` — Akien's response (a correction, a CC++, a CC--, or silence).
- `evidence` — `correction` | `confirmation` | `weak` (silence ≠ approval: silence is
  `weak` at most, an explicit positive is `confirmation`).
- `confidence_move` — direction + rough magnitude on that gate's *autonomy* (may this
  gate open for CC?), with a `ceiling` note if it is an irreversible/outward gate that
  must never auto-open.
- `note` — the why, in one line.
- `provenance` — where in the record this came from (session/turn).

## Guardrails (from I-learns-its-gates — not optional)

- **Asymmetric:** counter-evidence lowers faster than confirmation raises.
- **Ceilinged:** irreversible / outward gates carry a confidence ceiling *below* the
  autonomy threshold — they never auto-open, however much evidence piles up.
- **Silence ≠ approval:** absence of a CC-- is weak evidence, never a confirmation.
- **~90% is a per-gate default prior**, not a universal truth-level.

Records live in `records/`. This is v0: flat JSON, hand-authored. It migrates to
graph trees once more of the system is built.
