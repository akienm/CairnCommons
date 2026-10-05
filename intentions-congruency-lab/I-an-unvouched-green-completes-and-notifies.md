# An unvouched green completes and notifies

*Concept-piece, spanning: implemented at four component boundaries, so no one directory can
hold it. Cast 2026-10-04 as ticket `df05d93da4c0`, from Akien's answer to `open-ed0a56ce6357`.*

## The intention

A green that measurement cannot vouch for **completes its crossing and notifies the
operator**: one line naming the file, with the diff, and the rate of those notices measured
from the first one. There is no skip rule and no red for it.

"Cannot vouch for" has two faces today:

1. **A revert the proofs cannot see.** The hollow reverts a file the build changed, and no
   declared tooth reds.
2. **A green whose conditions moved.** A proof sealed red, then sealed green, but its proof
   bytes, fixtures, interpreter, isolation, timeout or CAIRN_* environment differ between the
   two runs. So the green may answer the changed measurement instead of the change.

## Why (his words, verbatim)

> oooooo... this is a good one. it exposes some important things... docstrings is only the
> start. consider something a week from now, something we can't imagine specifically yet...
> something where the system works... but it doesn't match the model in my head. so it passes
> the before test before, and the after test after, but only because the conditions of
> measurment have changed. and i'd assert that's probably an item to check with operator.
> [...] i think it is the shape and we'll try it out. if i get inundated, we'll change it. but
> we let it complete AND notify me. because the repo has the whole history anyway, we can
> back out a part if needed.

— Akien, 2026-10-04, answering `CairnCommons/questions/open-ed0a56ce6357.json`

What the user lives with: a skip rule covers today's case (a docstring edit) and misses next
week's, which nobody can imagine yet. A red holds a ticket hostage to a judgement only he can
make. Completing and notifying puts the one-line diff in front of the one reader who holds the
spec (Law 9). Git keeps every part reversible.

## Where it is implemented (RULE 1: one child per boundary)

| Child | Address | What it does |
|---|---|---|
| `0069ce6b8681` clearance-reads-a-notified-file-as-covered | `cairn/devices/cairn/machines/harbor_master` | The PROVED rung reads a hollow value `{"notified": <id>}` as covered, so `hollow_file` no longer refuses a file already sent to the operator. |
| `b5871526384a` tester-hollow-sends-the-unseen-to-the-operator | `cairn/devices/tester` | A file whose revert reds no declared tooth becomes one notice (file + the diff between the pre-build blob and HEAD) and is sealed `{"notified": id}`. Notices live under the tester's instance address. The `notices` verb answers the unseen list plus the rate; `notice-seen` marks one seen. |
| `81c41e528d6f` operator-inbox-shows-the-tester-notices | `cairn/tools/operator_inbox` | A NOTICES lane asks the tester's `notices` verb and shows each line, its diff head and the per-day rate. It is loud when the tester cannot be asked. |
| `f0aad0cd0f56` a-proof-run-records-its-conditions | `cairn/devices/tester` | Every proof run record carries its conditions. A green seal that replaces a red recorded under other conditions posts a notice naming each changed condition. |

## How we would know it is wrong

- **RED** if an unvouched green is refused at PROVED, passes silently, or is skipped by a
  rule. A rule that classifies a file by AST or docstring shape inside hollow is the skip
  rule this intention forbids.
- **WRONG INTENT** if he is inundated. The tester's per-day rate, shown in his inbox, is the
  instrument that says so; when it chafes, this intention is reviewed, not plastered.

First fire: `e0f318650123` crossed PROVED on 2026-10-04 with three notices
(`n-2e36a33c528c`, `n-2f83b3d8dccc`, `n-454e651f5057`) for two docstring-only reverts and the
post_commit charter.
