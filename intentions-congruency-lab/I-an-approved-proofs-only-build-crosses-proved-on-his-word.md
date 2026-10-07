# An approved proofs-only build crosses PROVED on his word

*Concept-piece, spanning: implemented at two component boundaries, so no one directory can
hold it. Cast 2026-10-06 as ticket `3fef5a02da2d`, from Akien's ruling 8p on the
`45c168cc1ff1` refusal.*

## The intention

When a ticket's build wrote only its own proofs, the hollow has nothing it may revert, so it
measures nothing. For that build, **Akien's answered approval of the proof change is the
measurement** (Law 10: "Akien said X" is one). The tester records his approval as the
hollow reading, and asks him once when no answer exists. Clearance accepts that recorded
approval at PROVED only after reading the question again.

Every other empty hollow stays red (`hollow_nothing_measured`). A recorded approval that does
not read again as resolved, bound to this ticket and answered by Akien is red too
(`hollow_approval_unresolved`).

## Why (his words, verbatim)

> yeah and then i say it's approved and it then is proved. at that point the tester records
> that proving. and it's the tester that's asking me for a ruling. what do you think? good
> approach?

— Akien, 2026-10-06, ruling 8p on the `45c168cc1ff1` refusal (relayed verbatim by peer
`akiendelllinux_cc_0`; he then said "agreed" to its two refinements: the question belongs at
ticketing, and `open-728473f9b70d` is 45c1's yes)

What the user lives with: `45c168cc1ff1`'s build wrote only its two proofs. Its hollow
skipped both as the instrument and sealed `{}`, and clearance refused
`hollow_nothing_measured`. No repair of the code could ever give it anything to revert. He had
already said yes to that proof change, and the ticket still could not cross. The only ways
past were faking `writes_to` or weakening the gate. Now his yes is the reading, recorded
where clearance can check it again.

## Where it is implemented (RULE 1: one child per boundary)

| Child | Address | What it does |
|---|---|---|
| `f5bba1daa72a` the-tester-records-an-approved-proofs-only-build | `cairn/devices/tester` | When a hollow measured nothing and every skip is an instrument skip, the tester reads the questions bound to the ticket. If one answered by Akien names a skipped file, it seals each such file `{"approved": <qid>}` and the run is green. With none, the run stays red and `cairn test --hollow --seal` opens one question to Akien naming the files, once. |
| `ec4ca415f43d` clearance-accepts-a-recorded-approval | `cairn/devices/cairn/machines/harbor_master` | The PROVED rung reads `{"approved": <qid>}` as covered only when that question resolves, is bound to this ticket and was answered by Akien. Anything else is the new lack `hollow_approval_unresolved`. An empty reading stays `hollow_nothing_measured`. |

## Where it is going

The question belongs at ticketing: "Does the operator allow this" is asked at `/sorted` when
a ticket will change proofs (his answer to `open-728473f9b70d`). The tester asks at
measurement time only when no such answer stands.

## How we would know it is wrong

- **RED** if an approved proofs-only build still reads red at clearance. RED too if an
  approval answered by someone else, unresolved, bound to another ticket, or naming none of
  the files reads green. And RED if an empty reading, or one whose skips are not all
  instrument skips, reads green.
- **WRONG INTENT** if Akien reads an approval recorded this way as one he did not give.

First fire: `45c168cc1ff1` crossed PROVED through harbor `clear()` on 2026-10-06, with
`open-728473f9b70d` recorded as its proving (commit `31507f9b`).
