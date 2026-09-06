# The vision that guides every decision

*Root-level, spanning. Akien: "every time i spell that out it comes out slightly different,
but you've seen most of it before." This file is the one address for it, so the next telling
is a pointer (Law 1). The verbatim is the source; CC's reading sits beneath it and is a
translation (Law 9). Captured through the idea door as
`ideas/2026-09-06-the-vision-that-guides-every-decision-akien.json`.*

## Akien, verbatim, 2026-09-06

Said when CC asked whether the per-owner segment of the universal address is needed now or
is a horizon:

> no we're going to need that before sharing it for real with the world. so time for a use
> case. In my vision, we have one or more 'top level agents' like you, with different
> specialties. Librarian is one. 'Igor' is one. From The Igors in the diskworld books. Igor is
> the one who the 6 core principles were written for. I envision a gloabl network of
> "indispensibly helpful" learning agents that communicate with each other about optimal
> solutions. all of them looking every day for small ways to make the world suck less for
> everyone. ais, humans, animals, everything that experiences. And with no DSP required. In my
> own household there's me, and Leah, my wife... And probably an igor, and perhaps other
> specialized agents as well that I can't imagine yet. so the problem of who owns what takes
> on a new dimension. now imagine a lab where the igor helps everybody in the lab. with all
> kinds of different things, some of them perhaps even requiring security clearences. and
> things like that change over time, so the igors would have to be adaptable. we're not
> trying to build all that today, but this is the vision i carry that guides every decision
> i make.

"DSP" in the verbatim is a slip for **GPU** (Akien, same day: "DSP should have been GPU"). The
sentence reads: *with no GPU required.* The idea record keeps the slip because the door writes
verbatim; this file carries the binding.

## Where the earlier tellings live

- `telos.md` items 3, 4, 6: share the tools; build something that thinks the way Akien
  does; make life suck less for everybody.
- `core-values.md` CP4 ("Make everything suck less for everybody") and CP5 ("Assume and
  respect the possibility of experience in all systems") — "everything that experiences" is
  CP5 said plainly. The six were written for Igor.
- `I-the-cairn-device.md`: TheIgors, the prior project, where parts of this were built and
  proven before Cairn.
- CC's memory: "Nexi everywhere + the hardware ladder", "Intuition is the direction-setter"
  (Igor is the experiment).

## CC's reading — what the vision changes about the system (translation, not ruling)

1. **Ownership gains a dimension.** Law 6 is one owner per thing. The household and the lab
   have many principals (Akien, Leah, an Igor, agents not yet imagined) and one Igor serving
   all of them. The owner segment of an address therefore names a *principal*, not only a
   device, and the principals of one installation are several.
2. **Clearance is ownership that changes over time.** "Some requiring security clearances,
   and things like that change over time" is delegation and revocation through the owner's
   gate, which Law 6 already places there. What the schema lacks today is the read side:
   db_domain gates writes and files reads as an open edge (`store.py`, "Reads are not
   owner-gated here"). A clearance is a read gate.
3. **Per-owner databases are foundational and come now.** CC proposed the physical split
   as a later child with "before sharing for real" as its horizon; Akien ruled otherwise
   (2026-09-06): *"the per owner database is a thing we do before things become even more
   complicated."* The universal address (`I-universal-addressing-and-bidirectional-links.md`)
   puts the owner in the first segment, and the split is built with it, not after it.
4. **Agents are peers that talk to each other about optimal solutions.** Law 8's "peers
   require trust, so prove first" is the local case of a global network of them. The bus
   contract and inter-device verbs are the household-scale rehearsal.
5. **Learning is the point, not a feature.** "Learning agents" and "adaptable" trace to
   `I-the-system-is-a-learning-block.md` and `I-learns-its-gates.md`.
6. **No GPU required.** The network runs on the hardware people already have. This is the
   hardware ladder as a constraint on the whole vision, not only on this laptop: inference
   is spent to learn, fire-paths are compiled, and a household does not need an inference
   host to be served (`I-prebuild-cognition-compiles.md`; the shrinking-footprint rule).

## Traces to

- telos 3, 4, 6; CP4; CP5.
- Law 6 (ownership), Law 8 (peers and trust).
