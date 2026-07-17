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
- `ceiling` — `true` if this gate must **never auto-open** (irreversible / outward /
  steering), however much evidence accrues. A structured guardrail read by the fold,
  not a prose match (rung 3): a never-auto-open gate is physics, not a substring the
  projection might miss (Law 4).
- `confidence_move` — direction + rough magnitude on that gate's *autonomy* (may this
  gate open for CC?); the prose rationale for the move (the `ceiling` field carries the
  guardrail structurally).
- `note` — the why, in one line.
- `provenance` — where in the record this came from (session/turn).

## Guardrails (from I-learns-its-gates — not optional)

- **Asymmetric:** counter-evidence lowers faster than confirmation raises.
- **Ceilinged:** irreversible / outward gates carry a confidence ceiling *below* the
  autonomy threshold — they never auto-open, however much evidence piles up.
- **Silence ≠ approval:** absence of a CC-- is weak evidence, never a confirmation.
- **~90% is a per-gate default prior**, not a universal truth-level.

## The retrieval architecture (design horizon — future-physics)

Why this store is more than an append-only log: **a memory that only accumulates
cannot be recalled from.** As records pile up, retrieval either scans forever
(unbounded — it eats the very context it was meant to protect) or times out before
the relevant record returns (there, but unreached). Growth guarantees one failure or
the other. This is the *horizon-of-awareness* problem: CC's context window is finite,
so recall is bounded, and the store must be built to keep the horizon reachable as it
grows. Three constraints follow — none built yet at n=5 (future-physics, like the
tester), but the v0 shape must not preclude them:

1. **Sparse, on-demand retrieval.** Recall surfaces the *one relevant record* at the
   matching gate — never the whole scroll. A store you must load entire to use is
   spending context to save it, backwards.
2. **Fold the settled (Law 1).** The settled compiles up; the raw recedes. Per-gate
   **confidence** is the compiled/hot layer (bounded — one entry per gate, this is
   what recall hits); raw records are the cold/episodic layer, kept for audit and the
   graph-tree migration, *not* the retrieval surface. Because every record is
   **gate-attributed**, the compiled view is a **pure projection** (a fold over each
   gate's records) — zero-inference, the same shape as cairnmap over charters. Lazy
   projection now → materialized + recompile-gated later.
3. **Importance-weighted consolidation ("sleep").** A periodic (nightly/weekly)
   background pass, run in the *unstressed, long-horizon* state, summarizes out the
   least salient records and keeps the decisive ones in detail. **Guardrail (load-
   bearing):** importance ≠ frequency. Rare-but-decisive records — counter-evidence,
   ceiling-gate records — score **high by rule** and are never summarized out, or
   sleep amplifies the very bias the store exists to fight. (`evidence: correction` +
   a lowering `confidence_move` already *is* the surprise signal.) Our advantage over
   biology: "summarized out" = dropped from the hot layer, still recoverable from cold
   storage (git, commons, graph trees) — our forgetting is *reversible*.

**Multi-layer recall** (the system's memory hierarchy, checked cheapest-first —
escalate only on a miss or ambiguity):

- **L1 / fast — the slate.** Already built. Most-important-things-present; the
  `/loadslate` read.
- **L2 / warm — a rolling short-term summary,** kept current over ~a week. The *one
  new tier*, and precisely what the sleep pass **produces**: consolidation
  materializes as L2.
- **L3 / cold — deep dive** into raw records / commons / graph trees. Paid for only
  when L1/L2 come up short.

This hierarchy is self-similar with the whole system (CLAUDE.md/slate = L1, cairnmap =
the compiled L2 view, charters+proofs+records = L3) and its escalate-cheapest-first
protocol is the same move as `/sorted`'s escalation ladder — a `learning-as-a-pattern`
sighting.

Records live in `records/`. This is v0: flat JSON, hand-authored. It migrates to
graph trees once more of the system is built.
