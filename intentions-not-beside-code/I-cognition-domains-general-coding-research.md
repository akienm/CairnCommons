# cognition-domains-general-coding-research

*concept-piece · ticket 728d393d70ed · owning intention: intentions-not-beside-code/_charter+why.json*

## Intention

A **cognition domain** is a machine that sits above `inference_domain` and below the
devices: it carries the *getting* rules for one kind of thinking — what content dresses an
ask, which rungs the escalation walk may dial, which models it prefers — and a device
**composes** one or more of them. Three domains stand today, authored as rows, never as
classes: **general** (the default; adds nothing by design), **coding** (code-shaped asks,
prefers the coder models), **research** (answers grounded in provided material, the
librarian's vertical). A device that needs its own behaviour composes a common domain and
overrides the parts it needs; that is an experiment, and it is allowed.

## Why

A device needs LLM smarts at different levels — the cairn device might use a little
general-domain chat for a support question while the aider shim needs a full coding domain
with its own escalation. Without domains every device reinvents its own escalation strategy.
With them the strategy is composed from a machine, and one device can mix domains (general
for help-desk, custom for core work) without becoming LLM-heavy for the small asks.

Akien's boundary sentence sets the seam: *"the reasoning happens in the calling device, but
getting the inference comes from here."* The domain is the GETTING half. The agentic loop
and the judgement of an answer stay in the device; the domain is where the loop lives BY
DEFAULT, and the device overrides when it must.

## How it is, measured

- **A domain is a row, composed by a call.** The domains stack
  `cairn/devices/inference_domain/machines/route/stacks/domains.json` holds `general`
  (`default: true`), `coding` and `research`; each row carries `why`, `prompts`,
  `escalation` and `prefers`. `domain.resolve()` dresses a request through
  `_domain_dressed` (`cairn/devices/inference_domain/domain.py:374`): the row is looked up
  by name from `route.domain_rows` (`machines/route/route.py:89`), an unknown name refuses
  loudly, a bare request rides the default row. There is no class hierarchy to belong to —
  a device names a domain per ask, so it can name a different one on the next ask.
- **The glue IS the escalation strategy.** `escalation.allow` lists the provider rungs the
  routed walk may dial for that domain — a getting rule, never a judgement on content
  (`domains.json` `escalation_note`); `prefers` orders the models. The models the rows call
  are shared (`stacks/models.json`, `stacks/combos.json`); what differs between domains is
  the walk, which is why two domains over the same host are still two domains.
- **General is the baseline.** The default row has empty prompts, no walk restriction and no
  preference, so a pre-domains caller is byte-for-byte unchanged and a device that never
  specialises pays nothing for the machinery (the row's own `why`).
- **A custom domain overrides the common one's strategy** by authoring a row whose
  `escalation`/`prefers`/`prompts` differ; a caller's own `system` outranks the row's
  prompt (`domain.py:374` docstring), so the device keeps its reasoning and the row supplies
  only what the device left unsaid.
- **Each domain owns its question list** as `(question, owner)` tuples: the question-tree
  embeddings generator (ticket 0b22c0e39c35, PROVED) registers every question with its
  owner, and the librarian's nexus verbs take `owner=` on every call
  (`cairn/devices/librarian/trees.py:183`). A domain's questions are the rows it owns there.
- **Progression** is a device changing the name it composes: the librarian starts on
  `general` and declares `research` from its own seam, never inferred from message content
  (`domains.json`, the research row's `why`).

## What would falsify this

RED on any of: (1) a domain becomes a class hierarchy — inheritance forces a choice, a
device could no longer mix; (2) a device cannot use a domain for a limited ask without
becoming LLM-heavy; (3) `general` stops serving as a baseline a plain device can ride
unchanged; (4) a custom row cannot override the common row's escalation; (5) a domain's
question list is no longer expressible as `(question, owner)` tuples in the embeddings
generator. Each is checkable against the files named above.

## What is built and what is red

Built and proved: the rows and the dressing seam (`inference_domain`, its route machine and
their validations); the embeddings generator's `(question, owner)` registry. Red: no device
yet composes TWO domains in one process, so the mixing claim is a labelled hypothesis (Law 3)
until a device does it and its meter shows the small asks staying small. The children the
ticket foresaw — general, coding and research as separate builds — collapsed into rows, which
is the cheaper shape the design predicted; a domain that needs more than a row (its own loop)
is cast as a machine when a device pulls for it.

**Provenance:** ticket `728d393d70ed` · ruling `2026-08-08-inference-proxy-is-a-rules-stack`
· ticket `2ff6113705be` (the-domain-carries-the-inference-side) · traces to Telos 1, Law 6, and the design
notes cocoon-settle-stages-around-cc and nexi-everywhere-hardware-ladder.
