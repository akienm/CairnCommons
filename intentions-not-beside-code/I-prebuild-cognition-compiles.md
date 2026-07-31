# I-prebuild-cognition-compiles — the pre-build steps migrate to deterministic code, one at a time

*Proposed 2026-07-19 by CC, drafted from Akien's stated intention ("eventually we'll
move every bit of this we can into python") and reconstructed from its origin (the
2026-07-02 claude.ai web chat where the sequence was named, and the Delta Dental
Copilot work where the first steps were compiled). **State: PROPOSED — awaiting
Akien's ratification (signature gate).** Peer of [[I-learns-its-gates]] and
[[I-cairn-claude-md]] in the intention layer. Corrects the stale 4-step compression
in MAP.md:484–505 (orient/constrain/deconstruct/plan), which this supersedes on
ratification.*

Before any code is written, a builder runs a fixed sequence of cognitive passes. Today
the resolver (an LLM) occupies that whole sequence as a single oracle slot. **The
intention is that each pass migrates out of the model into deterministic Python as we
learn it well enough to compile** — the role-replacement staircase applied to the
pre-build nexus. Each compiled step becomes independently inspectable (one module per
step), memoizable at its seam, and *provable* rather than merely plausible. Only the
genuinely-novel core — **hypothesize** — stays model-side the longest; everything
around it starves. Delta measured this at ~89% whole-build token reduction doing
exactly this compilation.

**The sequence (a loop, not a line):**

1. **Orient** — parse the request, ground it in what's actually being asked, place it
   in its domain/context.
2. **Constrain** — the bounds: what's required, what's forbidden, what shape the
   answer must take.
3. **Survey** — look at what already exists (files, patterns, prior art in the
   codebase) *before* touching the problem. Easy to skip, expensive when skipped —
   it's the pass whose absence makes a weak model read-wander.
4. **Decompose / disassemble** — break the ask into its constituent sub-problems.
5. **Triage** — sort those parts into *already-known/answerable* vs. *genuinely
   novel*. Named "framing / decomposition-into-subquestions" in the origin chat; the
   **starvation gate itself** — it decides what needs real reasoning (cold-path,
   model) vs. what's just retrieval (warm-path, cached). Where the economic win is
   measured.
6. **Hypothesize** — for the genuinely-novel parts only, form a candidate approach.
7. **Validate** — test the hypothesis against the constraints from step 2 *before*
   committing. **On failure it returns to one of two altitudes** (Akien, 2026-07-19):
   back to **hypothesize** for a local miss (this candidate violates a constraint), or
   up to **design** for a structural miss (no hypothesis can satisfy these
   constraints — the design is wrong). This is the return-for-learning vs.
   return-for-higher distinction landing on the step whose job is to catch it before
   Build.
8. **Build** — only now does code get written. **Build spawns children:** a change
   can reveal hidden sub-problems, which re-enter as new nodes at step 4
   (MAP.md:44 — "build → deconstruct is the universal shape").

**Why:** Cairn is an inference-automation system — it compiles inference into code.
The pre-build cognition is the densest, most repeated inference in the whole build
loop, so it is the highest-yield place to compile. Moving a step from "the model does
it" to "code does it" does three things at once: it cuts tokens (the measured 89%), it
makes the step's *output* an inspectable artifact handed to the next pass (so a wrong
orientation is caught before it becomes a passing-but-hollow build), and it turns the
step from a discipline the model must remember into physics it cannot skip (Law 4).
The staircase is the mechanism; this intention names the specific steps and their
order so each migration is a discrete, provable graft rather than a vague ambition.

**Traces to:** Telos 1 (demonstrate inference compilation — this *is* that
compilation, aimed at the build loop's own cognition) and Telos 5 (self-improving —
each compiled step is a faculty the system now owns rather than rents). Mechanism:
Law 4 (a compiled step is physics, not a remembered ritual), Law 3 (a step's
readiness-to-compile is a hypothesis — measured, not assumed), Law 5 (intent + impl
share an address — each step's module co-locates its why), Law 1 (a settled step
becomes structure, so the resolver stops re-deriving it).

**Design constraints (load-bearing):**
- **The back-edges are part of the shape, not an afterthought.** Step 7 returns to
  hypothesize *or* design; Build returns to Decompose. A version of this drawn as a
  straight line has dropped the thing that makes it a build *loop* — and Cairn holds
  that nothing is terminal.
- **Triage is a distinct step, not folded into Decompose.** Disassemble takes the
  problem apart; triage sorts the parts by novelty. Collapsing them loses the
  starvation gate — the exact pass where the token win is decided.
- **Survey is a distinct step, not folded into Orient.** Orient grounds the *request*;
  Survey grounds it in the *existing code*. The second is the one that gets skipped.
- **One module per step.** Each compiled pass is independently inspectable and
  improvable; the seam between passes is a typed artifact (an "X-JSON handed down"),
  which is both where memoization lives and where intent can quietly deform — so the
  bottom proof must trace back to the top intent, not just to the prior seam's output.
- **Migrate on evidence, not on eagerness.** A step moves to Python when it's
  understood well enough that the deterministic version passes a proof a hollow one
  couldn't (Law 8) — not because it's next in line.

**Falsifier:**
- *Done (asymptotic):* a build runs the full sequence with the model reached only for
  the genuinely-novel *hypothesize* pass — orient, constrain, survey, decompose,
  triage, and validate all served by deterministic Python emitting inspectable
  artifacts — and the measured token cost of a defined-ticket build trends toward the
  Delta ~89%-reduced floor while builds stay non-hollow.
- *Wrong, two ways:* (a) a step is compiled that shouldn't be — the deterministic
  version passes its tests but produces builds that answer the wrong question (the
  seam deformed and the bottom proof didn't catch it), meaning triage/validate were
  compiled past their real understanding; (b) the steps never move — the resolver
  keeps occupying the whole slot and the token cost doesn't fall, meaning this is a
  description of cognition, not a compilation of it.

**Horizon:** re-checked each time a step is proposed for migration (each migration is a
child ticket with its own proof), and when the graph-tree substrate lands (the origin
framing had these passes destined for trees, not only Python — the two are the
cold-path and warm-path of the same compilation).

**Provenance / the trail that found this:** the sequence was named in the 2026-07-02
claude.ai web chat (`~/.unseen_university/akien/20260702.ClaudeWeb...txt`), where
Akien was reaching for a forgotten step's word and it was named *decomposition*; the
same reach recurred 2026-07-19 and resolved to the same word. This file exists so it
does not have to be re-derived a third time (Law 1 — the resolver is spent on the
novel, not on re-deriving the settled). First steps already partly compiled in the
UU/Delta work: orient+survey (`pre_inference_assemble.py`, the packet's
`context_shortlist`), constrain (the constraint normalizer/decorator), and the packet
chain `intent → hard_constraints → success_definition → sufficiency_gate → proof_plan
→ consequence_check`.

**Related work:**
- [[I-learns-its-gates]] — the same compilation aimed at decision-authority; *which*
  step is ready to migrate is itself a learned gate.
- MAP.md:484–505 — the pre-build passage this replaces; update it to point here on
  ratification.
