# The heartbeat, the probe, and the bus

*Concept-piece. Converged with Akien 2026-07-18; restated 2026-09-30. The component
detail lives in the charters — `cairn/devices/cairn/machines/bus/intention+why.json`,
`cairn/devices/cairn/machines/ground_loop/intention+why.json`,
`cairn/devices/cairn/machines/sleep_cycle/intention+why.json`,
`cairn/tools/base/probe.py`. The long form this replaced is in git history.*

## This is an event-driven system

Akien, 2026-09-30: *"this is ENTIERLY an event driven system EXCEPT: Akien can say he'll
be away from x to y times. and sleep."* Things happen because something happened — a
message, a write, a crossing. A clock is used only where no event can exist: a time
Akien named, and an idle stretch (*"a '3 hours without a human' screensaver like
trigger"*, 2026-08-06).

**Why:** polling costs CPU on every tick where the answer is *no*, and that is almost
every tick. An event costs only when the thing happened. Cairn should cost less to run
as it matures (telos aim 1 — Law 1 one layer down: don't spend compute twice).

## The bus — the heart

Akien, 2026-09-30: *"The bus is the heart of the thing. it's intention is to be an
inspectable messaging pipe between each component that is the only path between
components (originally intended to be MCP). unlike conventional MCP, this can do both
sync and async. the shims are part of the bus (same process). a device is a shim + it's
component(s)."*

- **A device = its shim + its component(s) or external thing.** The librarian is a
  separate process; its shim, in the bus process, wakes it and hands it the message.
  Calibre is all shim — it talks to the Calibre db itself.
- **One pipe for everybody, except the db** (2026-09-06): *"if everything goes thru one
  pipe, we learn faster. and this is how everybody should communicate with everybody...
  except the db."* — *"the db gets a pass only because i expect a LOT of db traffic."*
- **Delivery is instant from an in-memory ring** (2026-09-06): *"if a new message came
  in, and a device came for that message, it was just there instantly no db access. if
  the reciver wasn't that fast, that ring buffer would go to the db when the ground loop
  pulse came by."* That flush is the bus's act, and it is persistence, not delivery.
- Every message carries its why and its causality, so the traffic is a readable record.

## The heartbeat — the ground loop

*"NOTHING IN THE GROUND LOOP EXCEPT THE PULSE, THE GROUND LOOP CONTROL FLAGS, AND THE
DEVICES FOUND LIST. EVER."* (2026-09-06). It exists because CC once made daemons for
everything and could not shut them down, so it is as simple as possible. Each beat it
spawns the pulse as separate processes and does not wait on them. Three things listen:
the bus's ring flush (*"NOTHING in the system that should fire on the heartbeat execpt
the messaging"*, 2026-09-30), Akien's away windows, and sleep (maintenance, handed round
the devices one at a time by the sleep-cycle token).

## The probe

*"all probes respond to events"* and *"if it's not consumed, it's trash"* (2026-09-30).
A probe is "when this event happens, send this to that consumer": immutable, no state,
no authority. It fires where the thing happens — a door, a crossing — never on the beat.
It exists only because a consumer needs its data and uses it; the receiver is built
first, then the sender. A trigger is any predicate; it is evaluated where its data is
owned, so only the poke crosses the bus (Law 6).

A **ticket** is a different species — a mutable workflow node. A ticket's WATCHME
creates a probe; the probe never moves the ticket.
