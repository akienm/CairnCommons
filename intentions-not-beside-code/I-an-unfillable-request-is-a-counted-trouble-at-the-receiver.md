# an-unfillable-request-is-a-counted-trouble-at-the-receiver

*concept-piece · ticket a75ec82aa1f2 · owning intention: intentions-not-beside-code/_charter+why.json*

## Intention

A component that receives a request it cannot fill raises the trouble **at its own address**,
under an identity naming what was asked, counted on every repeat, and tells the caller which
trouble it raised. A sender that is blocked by the refusal **adds** to that same trouble; it
does not write one of its own. The test before raising is the outline's (3.4.3.5): *can only
CC or Akien fix this? If not, it is a log line, not a trouble. One problem, one trouble.*

## Why

Ruling 8h, 2026-10-05, Akien verbatim: *"Any component that gets a request that it can't fill,
that's a trouble ticket. We will eventually class certain classes of trouble is not requiring a
ticket. Because like if we throw a trouble ticket because I mistype something on the Cairn
command line, that might not be a trouble that I actually need to go look at. But every
requester that gets something they can't do should throw a ticket. Because we need to stop
people throwing things at them that they can't do."*

The lived symptom: codemother asked inference_domain for a `codemother` domain row that does
not exist about 1,000 times a day, every ask was refused in silence, and nobody could see the
broken caller.

Which end raises, Akien's answer (CairnCommons/questions/open-b9037ca75019.json), verbatim:
*"if i request something from inference, and it fails inside of inference, inference issues a
trouble ticket. it reports what it reports to the caller, perhaps including the trouble ticket
in question. the sender can then choose to add to that ticket if the sender is blocked by the
result. how's that? — actually the codemother, lets say, just appends new data to the
inference's trouble. writing is not safe, but appending is. and this way if this mechanisms
inside of the initial reporter are not working correctly, the adding of codemother's
information can still happen."*

The outline carries the same shape at 3.4.3.4: *a device that errs while servicing another
device's request can return a pointer to the trouble ticket, and the receiver can add details.*

## How it is, measured

- **The counter is the trouble lane's fold.** A raise goes through `raise_trouble`
  (`cairn/tools/base/diagnostic.py:332`), and the trouble device folds on the slugged identity
  (`cairn/devices/trouble/trouble.py`, `self._slug(identity)`), so a repeat of the same ask is
  a count on one trouble and a different ask is a different trouble.
- **Each receiver raises at its own boundary (RULE 1).** inference_domain raises
  `inference-unfilled-domain-<asked>` when a domain row does not exist, naming the caller
  (`cairn/devices/inference_domain/domain.py:555`; ticket e9a2d8ae7d43, PROVED). The caller's
  refusal is unchanged.
- **Every device's undeliverable mail is raised where it failed.** `BaseShim._bounce_to_sender`
  (`cairn/tools/base/shim.py:967`) raises the trouble at the receiving shim under the identity
  the bounce already carries in `body.trouble`: `mail-<device>-has-no-verb-<verb>`,
  `mail-<device>-verb-<verb>-raised`, `mail-<device>-has-no-receive`. The raise is guarded, so
  a trouble lane that is down never stops the bounce, and the failure goes to stderr (ticket
  eff2fb9810de, PROVED).
- **The sender's raise is the append.** `BaseShim.handle_bounce` (`shim.py:1013`) raises
  under the bounce's identity, so it folds into the receiver's trouble rather than standing
  beside it, and it still lands when the receiver's own raise failed: the case Akien named.
- **Mail born of a test raises nothing at either end.** A testing-marked envelope's bounce
  carries the mark, and both shims emit `test_bounce_disposed` instead of raising (ticket
  b3386f431ae3's ruling, carried to the shim by eff2fb9810de).

## What would falsify this

RED on any of: (1) a receiver refuses a request it cannot fill and raises nothing; (2) the
trouble replaces the refusal or the bounce, or a failed raise stops it; (3) the receiver's
trouble and the sender's addition land as two troubles instead of one; (4) a fillable request
raises; (5) a failure only its typist can fix (a cairn CLI typo) becomes a trouble rather than
a log line. Each is checkable against the files named above and their proofs.

## What is built and what is red

Built and proved: the inference_domain domain-row raise (e9a2d8ae7d43) and the base shim's
receiver raise with the sender's append (eff2fb9810de). Red: a device whose verb handler
*returns* a refusal (rather than raising, or having no verb) raises nothing unless that device
raises it itself, as inference_domain does; there is no declared refusal shape the shim reads.
That is a hypothesis about need (Law 3) until a measured silent refuser pulls for it. No
no-ticket seam is built: the outline's test runs before raising, so a typo is a log line at its
own surface (open-7d7bcae62287).

## Provenance

ticket `a75ec82aa1f2` · ruling 8h (2026-10-05) · question `open-b9037ca75019` (which end
raises) · question `open-7d7bcae62287` (the outline's test before raising) · tickets
`e9a2d8ae7d43`, `eff2fb9810de`, `7cb1989e7825`, `b3386f431ae3` · outline 3.4.3.4, 3.4.3.5 ·
traces to Law 7 and CP4.
