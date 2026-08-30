# Review: CC Patterns for Cognition Gates

**Ticket:** review-cc-patterns-for-cognition-gates
**Source:** github.com/miloudbelarebia/claude-code-prompt-engineering-patterns
**Source provenance:** Third-party reverse-engineering of leaked npm package. NOT ground truth.

## Pattern-to-Cairn Mapping

| CC Pattern | What It Does | Cairn Analog | Gap / Design Surface |
|---|---|---|---|
| Coordinator has no tools | Forces delegation to specialized agents; coordinator thinks, doesn't execute | **No analog.** The cocoon (memory: cocoon-settle-stages-around-cc) wraps CC with cheaper stages, but those stages both think AND execute. The coordinator's constraint is architectural: a component stripped of its own tools must decompose before acting. | gap: a decompose-before-act gate — a component that must split work before touching it |
| Verifier spawned fresh | Adversarial check from a clean context, no prior-bias leakage | **Partial analog:** build_inspector (26 sieves) verifies deterministically, but from the same context the builder used. /challenge runs in-context. The tester runs in netns (isolated network) but shares the same codebase state. | gap: nothing spawns a verifier with zero prior context; the closest is tester's netns isolation, which is network-level, not cognitive-level |
| Anti-hallucination 5 rules (don't over-claim AND don't over-hedge) | Bidirectional constraint: both false positives and false negatives are defects | **Direct analog:** skill_block door (refuse-with-every-lack-named-in-one-pass). The door rejects under-specified AND over-specified inputs. The build_inspector's own tooth-1 check ("a healthy component draws a finding — a gate that always fires gets unwired") is the anti-hallucination shape: gates that never fire are as suspect as gates that always fire. | analog exists — the pattern is already implemented, just not named as anti-hallucination |
| Numeric anchors outperform qualitative | Measurable constraints beat directional guidance | **Direct analog:** Law 4 ("a rule that matters is enforced by physics, not policy") + the sieve architecture (deterministic Python, not LLM judgment). Every sieve returns numeric findings; the gate opens on an equality compare, never an oracle assessment. | analog exists — this IS the Cairn design principle; the CC pattern validates it from a different codebase |
| Static/dynamic prompt split | Cache boundary: static content (identity, rules, tools) above the boundary; dynamic content (memory, per-session state) below | **Partial analog:** the three-root separation (class-space, commons, instance-space) achieves the same cache-like boundary at the file level. CLAUDE.md is static; session context is dynamic. | analog exists at a different level — file-level, not prompt-level; no actionable gate here |
| 4-phase workflow (Research → Synthesis → Implementation → Verification) | Mandatory phase ordering; each phase has its own agent type | **Direct analog:** the chart chain (orient → constrain → survey → decompose → triage → hypothesize → validate) is the same pattern with 7 phases instead of 4, each schema-gated. The chart chain is MORE constrained than CC's phases (gates refuse structurally, not by agent-type assignment). | analog exists and is more mature; no gap |

## Gate Designs

### Gate 1: `intention_fidelity` — does the charter faithfully translate the ticket's intention?

**What it measures:** The cognitive quality of intention extraction — whether the component's charter (`intention+why.json`) accurately represents the ticket that spawned it, not just whether the charter exists (which `charter_on_disk` already checks).

**CC pattern origin:** Anti-hallucination rules (don't over-claim AND don't over-hedge). A charter that claims more than the ticket intended is over-claiming; one that claims less is over-hedging. Both are defects the current `charter_on_disk` sieve cannot see — it checks existence, not fidelity.

**Predicate (deterministic):**
1. Read the component's `intention+why.json` → extract `what`, `falsifier`
2. Read the ticket named by the component's `owning_intention` or `history.json` → extract `intention`, `falsifier`
3. Compare: every keyword in the ticket's falsifier must appear in the charter's falsifier (coverage check). Every keyword in the charter's falsifier must trace to the ticket (no invented scope).
4. Finding if: charter falsifier covers < 80% of ticket falsifier keywords, OR charter falsifier contains > 20% keywords absent from the ticket (scope creep).

**Non-hollow discriminator:** A charter that copies its ticket's `intention` verbatim but rewrites the falsifier to something unrelated (e.g., replaces "messages reach the shim" with "the file exists") would pass `charter_on_disk` but fail `intention_fidelity`.

**Limitations:** Keyword overlap is a coarse proxy for semantic fidelity. It catches gross drift (wrong falsifier, missing clauses) but misses subtle rewording that preserves words while changing meaning. The memory "words kept, meanings replaced" (n=9) is precisely this failure mode — the gate catches the easy cases but not the hard ones. A future version could use structural comparison (AST of the falsifier's clauses) rather than keyword overlap.

### Gate 2: `gate_retry_instrumented` — is the fail→fix→retry loop measured?

**What it measures:** Whether the builder's retry loop is instrumented, not just exhibited. The pattern exists (gates refuse, CC fixes, CC retries), but nowhere measured — no count of retries per gate, no error-type classification.

**CC pattern origin:** The 4-phase Verification phase. CC's internal architecture doesn't just verify — it counts and classifies verification failures. Cairn's gates refuse but don't record what they refused or how many times.

**Predicate (deterministic):**
1. Read the component's `history.json` → count entries where a gate refused (EntryGateRed, BuildGateRed, ExitGateRed)
2. For each gate refusal, check whether a subsequent successful crossing exists for the same ticket
3. Finding if: gate refusals exist in history but no retry count is recorded in the component's `state.json`

**Status:** Deferred — this gate requires history.json to reliably record gate refusals, which is not yet guaranteed (the history door catches in-place edits but does not enforce recording of gate events). Ticketed separately would be premature until the history door is more mature.

## Transferability Assessment

| Gate Design | CC Origin | Analogy Type | Confidence | Thin Spots |
|---|---|---|---|---|
| `intention_fidelity` | Anti-hallucination 5 rules | **Structural** — both systems need bidirectional fidelity checking; the direction (over-claim vs. over-hedge) is the same in both | 0.7 | The CC "5 rules" are summarized in one line in the reverse-engineered source; we know the direction (bidirectional) but not the specific predicates CC uses. The keyword-overlap approach is our design, not CC's — we're borrowing the principle, not the implementation. |
| `gate_retry_instrumented` | 4-phase Verification + internal metrics | **Surface-level** — CC's verification is agent-level (spawn a fresh verifier); Cairn's is gate-level (structural refusal). The instrumentation need is real but the implementation would look nothing like CC's. | 0.5 | The reverse-engineered source says CC counts and classifies but doesn't show how. We'd be designing instrumentation from the principle alone, not from a studied implementation. Too thin to design a specific predicate. |
| (verifier-spawned-fresh) | Multi-agent Verifier role | **Surface-level** — CC spawns a separate agent with no tools and fresh context. Cairn's tester runs in netns (network isolation) but shares codebase state. The gap is real but the solution would be Cairn-native (perhaps a second tester pass with a shuffled component order), not a CC port. | 0.4 | The CC Verifier is adversarial by role assignment, not by a gate predicate. Porting this would mean designing what "adversarial" means deterministically — CC doesn't have to because the LLM IS the adversary. Too thin for a gate. |

## Conclusion

One actionable gate design emerges: `intention_fidelity`. It measures cognitive quality (fidelity of intention extraction), has a deterministic predicate (keyword overlap), and is non-hollow (a charter with a rewritten falsifier fails it while passing `charter_on_disk`). Ticketed for build at `CairnCommons/tickets/cognition-gate-intention-extraction.json`.

The fail→fix→retry instrumentation is a real need but requires the history door to mature first. The verifier-spawned-fresh pattern is a real gap but cannot be designed as a deterministic gate from the available source material.

**Provenance:** This review cites patterns from a reverse-engineered source (Belarebia, 2026). No code was copied. No CC internal was treated as ground truth. Where the source was too thin to design from, this is stated. The gate design (`intention_fidelity`) borrows the bidirectional-fidelity principle; the predicate (keyword overlap) is Cairn-native.
