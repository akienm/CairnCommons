# Librarian v3 — Session Notes for Claude Code

Context: v3 exists because Akien finally understood Gates, and the system is
now built around intentions that must be harmonized before ticketing. This
session was design-only (no code reviewed) — working through what the
extraction-first plan actually implies before touching the Librarian's code.

## 1. The observed failure mode (why orientation is first up for extraction)

When an intention's supporting data lives in the same folder as the code,
orientation stops being "figure out what's being asked" and collapses into
"pattern-match to the nearest thing this resembles." Proximity to the answer
changes the shape of the reasoning. Since Opus 5 shipped, this shows up as
the model converging on an answer *faster* — which looks like confusion but
is actually skipped work: constrain and survey get compressed into "I can
already see it," so bounds-checking never runs to completion.

Implication: this is not a prompting problem to patch. It's an argument for
making orientation its own gated question nexus with a typed exit condition,
run *before* the model is allowed to see what's sitting in the folder — or at
minimum, with an explicit decision about what orientation is allowed to see
on its first pass vs. what's revealed only after constrain/survey commit
their outputs.

## 2. The agentic loop vs. the pipeline

The 8-stage pre-build pipeline (orient → constrain → survey → decompose →
triage → hypothesize → validate → build) is not a flat sequence — **each
stage is its own loop** (think → act → observe, repeat until that stage's
local exit condition is met). The pipeline is a loop of loops, not a line
with loops bolted onto it.

This matters for the Librarian directly: chat and deep research are not the
same loop wearing different clothes.

- **Chat loop**: exit condition is conversational (turn ends when the point
  is made or the question is asked). Shallow-orient, usually no
  survey/decompose at all. Mostly "think → respond."
- **Research loop**: exit condition is epistemic (loop until confidence
  crosses a threshold or the question space is exhausted). Walks the full
  eight stages, survey and triage doing the expensive repeated work — every
  new source reopens decomposition.

The Librarian needs a cheap default loop (chat) plus a **detection step**
that decides when to escalate into the expensive nested loop (research).
That escalation-detection step is itself the starvation-gate/triage pattern,
just showing up one level up — at "which loop am I in" rather than "which
stage am I in." The current ambiguity in the Librarian's output (unclear if
it chats back) may be because this top-level dispatcher isn't explicit yet —
everything may still be living inside one undifferentiated loop that
sometimes does deep things with no clean signal for when it switches modes.

## 3. Each pre-build stage is its own reusable question nexus

Escalation-detection, survey, triage, etc. should not be logic embedded in
one agent (e.g. "the Librarian's escalation logic"). Each should be a
standalone, typed question nexus:

- Answers one narrow, checkable question (not "what should I do" but e.g.
  "is this input answerable from cache or does it need a fresh loop").
- Inputs/outputs specified independent of which agent is calling it.
- Has its own exit condition, separate from whatever loop invoked it.
- Accumulates — the mechanism that lets it compile toward deterministic
  over time instead of staying a fresh LLM call forever.

Once built once, generically, every future Cairn agent draws on the same
nexus instead of reinventing it. Building the Librarian (chatbot) before the
builder is, concretely, "build and prove several of these nexuses in one
place first."

## 4. Parsimonious output as the actual target

The goal for each nexus's output isn't just correctness — it's the smallest
form that fully determines what downstream nexuses need. Concretely:

- **Typed/schema output, not prose.** A fixed schema (domain, scope,
  known-constraints-ref, survey-refs, confidence) lets the next stage's
  prompt be built by template-filling, with zero re-reading required.
- **References beat restatement.** Point at files/nodes/tickets rather than
  restating found content; downstream resolves the pointer only if needed.
- **Confidence/provenance travels as data, not as hedging prose.** A
  confidence float costs nothing downstream; hedged prose costs a full read.
- **Test for "parsimonious enough":** could the next nexus's prompt be
  constructed by template-filling from this output with zero LLM re-reading?
  If yes, the interface is actually compiled, not just shortened.

Tension to hold explicitly: parsimony and the premature-convergence problem
(section 1) pull in opposite directions. The *internal* reasoning inside a
nexus's loop should stay wide and exploratory (that's where survey/constrain
earn their keep) — only the *emitted* artifact needs to be narrow. Loose
process, tight output. Keep these as separate concerns inside the nexus's
own loop, or pressure to shrink the output starts squeezing the reasoning
that should stay wide.

## 5. `more_about(ref)` tool — recoverable compression

Resolves the tension in #4: tightness doesn't have to be lossy if it's
reversible on demand.

- A downstream nexus can call `more_about(ref)` to get an expanded view of
  something the upstream nexus compressed.
- Every `more_about` call is a labeled training signal: "this field, at this
  compression level, wasn't enough for this class of intention." That should
  write back into the upstream nexus's graph tree so the parsimony threshold
  adjusts for that class over time — the tree compiling out a recurring
  correction, not just logging a complaint.
- Calls must be **scoped** ("expand the constraint-set," not "tell me more
  about everything") — a vague call teaches the tree nothing; a scoped one
  is a usable training signal.
- Design decision still open: `more_about` should almost certainly be a
  cheap lookup against the upstream nexus's already-computed internal state
  (it did the wide reasoning once; the emitted output was just one view of
  it) — not a fresh LLM re-invocation. Re-running the full pass every time
  compression turns out insufficient would fight the parsimony goal directly.

## 6. Shadow/champion gamification (Claude vs. Hex per nexus)

For every extracted pre-build nexus, run two implementations in parallel and
score them against each other — same pattern as production shadow/champion
testing, extended from the existing CC+/CC- points system:

- **Claude** runs the real pass (production, authoritative output).
- **Hex** (M1 Studio, 32GB) runs the graph-tree version in shadow on the same
  input, simultaneously — its output never touches the live pipeline, only
  gets logged.
- **Score on behavioral match, not text match**: would a downstream nexus
  have made the same call given either output? Compare on the fields that
  matter (scope, constraint-set, confidence), not prose similarity.
- **`more_about` frequency is a free scoring signal** — if Hex's output
  needed more follow-up expansions than Claude's did for a given input
  class, that's a concrete strike against Hex for that class, no separate
  metric needed.
- **Promotion needs a run, not a streak** — flip Hex from shadow to primary
  for a given nexus only after N consecutive matches above threshold. Keep
  Claude running in shadow occasionally even post-promotion (inverted roles)
  to catch drift the moment something like a model upgrade changes what
  "correct" looks like — same proof-of-innocence instinct as the self-test
  gate, applied to model-swap instead of infra failure.
- A scoreboard per nexus (current champion, match-rate trend, last flip
  date) doubles as both the gamification layer and the actual audit trail.

## Sequencing note

Extraction order: **orientation first**, then work down the stack
(constrain, survey, decompose, triage, hypothesize, validate). Orientation is
first specifically because it's where the Opus-5 premature-convergence
failure was observed directly, and because every downstream nexus depends on
however parsimonious/complete its output turns out to be.
