# The heartbeat, the probe, and the bus

*Ratified in conversation with Akien, 2026-07-18 (evening). This is the converged
runtime architecture for how Cairn devices are driven and how they talk. It sharpens
and partly supersedes the earlier "operational-driver primitive" + "host/rack" +
"peers fire in two modes" sketches in `MAP.md` and `tickets/state-machine-physics.json`.
The code shipped 2026-07-18 morning (`ground_loop` `584aa74`, `system_rackmount` `5cb593a`)
was built to the OLD shape (a generic `run_driver` executor + a central scheduler) — that
shape was the goof this document corrects. The rework SHIPPED the same evening (commits
`d27ce1d` bus, `ae2d372` base probe+shim, `a535de0` heartbeat, `faafb70` system device),
each piece proven under the tester — see "What this changes in code — DONE" at the bottom.*

## The two universal substrates

Everything runtime hangs on exactly two things:

- **The heartbeat** — one daemon that provides a pulse, and nothing more. This is the
  `ground_loop`. It does not execute, resolve, schedule, or route. It beats.
- **The bus** — one common messaging substrate for everything. Inspectable, logged,
  and the *sole* path for inter-device communication.

The symmetry that makes them load-bearing:

| Substrate | Sole path to… | Owner-gated | Inspectable/logged by construction |
|---|---|---|---|
| `db_domain` | durable **state** | yes (Law 6) | yes |
| **the bus** | inter-device **communication** | yes (Law 6) | yes |
| the heartbeat | — (it only beats) | — | the beat is trivially observable |

Because the bus is the *only* door for communication (devices never hold references
to each other, never call each other directly), "inspectable + logged + common" are
not features added per surface — they are automatic. Physics, not policy (Law 4).

## Devices, shims, and processes

- **Each device is its own process.** Isolated, independently crash/restartable, and
  it does **not** run continuously — it sleeps when idle and is woken on demand.
- **The shim** (`BaseShim`) is always-on, lightweight, one per device. It:
  1. fires the device's due probes on each heartbeat pulse,
  2. **receives** incoming bus messages for its device,
  3. **starts the device** (the heavier process) on demand when a message arrives and
     the device isn't running.
  So the shim is the device's persistent front and process-manager; the device is the
  heavier process the shim wakes. This is the sleep/wake peer model made physical: a
  device is a process that *wakes to a poke*, not a daemon that spins.

### Why event, not poll — the shrinking-footprint aim (Akien, 2026-07-22)

**Polling costs CPU; events don't.** A process that wakes on a schedule to check
whether something happened burns cycles on every tick where the answer is *no* — and
the answer is *no* almost every tick, by construction. An event-driven wake burns cycles
only when the thing actually happened. So the choice between "scan periodically" and
"subscribe to the gate that produces the change" is not a style preference — it is the
difference between a cost that grows with the *clock* and a cost that grows with *real
events*, and real events are rare relative to the clock.

This traces to a standing aim Akien named explicitly: **an ever-decreasing computational
footprint.** Cairn should cost *less* to run as it matures, not more — the opposite of a
system that accretes background daemons and cron ticks until the machine is busy doing
nothing. Every "poll" we can convert to an "event" moves a cost off the clock and onto
the events that justify it.

**Where it traces (Akien, 2026-07-22): telos aims 1 and 5.** It is a *derived
consequence*, not a seventh aim and not a core value. Aim **1 (demonstrate inference
compilation)** is the load-bearing parent, because **Law 1 is this same principle stated
at the inference level** — "the resolver is spent on the novel, not on re-deriving the
settled" is *don't spend compute twice*. Inference compilation turns re-derivation into
structure, which *is* reduced compute; event-not-poll is that principle one layer down, at
runtime instead of at inference. Improving along that axis as the system matures is aim
**5 (self-improving).** So shrinking-footprint is compilation generalized from inference
to the running machine — not, primarily, an altruism (aim 6) thing.

It is also **a why for the ground loop itself**, though the ground loop's charter does
not phrase it this way: the ground loop is the *one* permitted periodic pulse, and it
exists precisely so that nothing else has to be. One heartbeat, shared, replaces every
component's private timer — N polling loops collapse to one, and the one does nothing but
beat. Concretely, this is why the pre-Cairn cron jobs were deleted (2026-07-22) rather
than ported: a cron entry is a private polling loop with a private schedule and no owner
(see `notes/held-inspectors-janitors-filters.json` — the unowned-default that governs a
record's survival). Functionality like `cleanupPeriodDays` may well be rebuilt — but it
will hang on a probe fired by a gate, not on a clock that wakes to ask "anything?".

## Probes vs tickets — two species, named for what they are

- **Probe** — *immutable, no workflow.* "Call X when this trigger is true." It
  carries no state of its own. Because it is *declaration*, it lives with the device's
  **code** (class-space — git, greppable, shareable). A probe firing = **kick off a
  separate, short-lived Python process** in its own space that sends a message to the
  target's shim, then **terminates.** That statelessness is why it can be a fire-and-die
  process. The heartbeat fires probes (via the shim). Every recurring wake-up —
  interval, time, data-accumulated, resource-threshold — is a probe.
- **Ticket** — *a workflow node: mutable, carries a state machine* (a voyage, e.g.
  `PROVEME → WATCHME(<object>) → PROVED`). A different species. Its state is mutable,
  so it lives where workflow-state lives (instance-space / the node store), not
  class-space.
- **A ticket CREATES a probe and carries it; the probe fires when the ticket
  crosses a gate.** (RESHAPED 2026-07-30, ticket `watchme-emits-a-probe`;
  CORRECTED 2026-08-03 by Akien's ruling, which fixed two words at once. The
  clause first read "`LEARNING` is a state; a probe is the worker" — that state
  is dissolved. It then read "a node EMITS a probe at a crossing", and **both of
  those words were wrong**: *node* is ambiguous (this system has several kinds,
  and the workflow one is a **ticket**), and *emission* is not what happens —
  **the probe is CREATED**.) The two-species point SURVIVES INTACT and is in fact
  strengthened: "this ticket has created a probe" and "this ticket rests at
  `PROVED`" are two separate facts about two different species — do not mush them
  into "a mutable ticket."

  **The mechanism, in Akien's own words (2026-08-03).** The `WATCHME` state
  causes the **creation** of a probe — aimed *wherever one needs to be*: a
  gateway, a time, a future event, whatever it takes to send back feedback about
  the intention. **Once that probe is created, the state is complete.** A ticket
  then crosses a gate with its probe attached; the probe fires there, and emits a
  call back to **the thing that put it there, or to some other thing designated
  at creation time**.

  So the ticket does not sit in a state waiting for its own watcher — a proved
  intention's efficacy data can only accumulate after it rests. The probe
  outlives the crossing that created it, which is what makes it a different
  species rather than a phase of the ticket.

  **And the probe carries no authority.** When its `enough` condition clears, or its
  finding lands, it **deposits and pokes** — it never moves the node's state. The
  back-edge that re-opens a node whose intention did not work is the **owner's act**
  at the register (Law 6). A worker that could move what it watches would be exactly
  the ambient authority the ownership law exists to refuse.

Probes are general, not scheduler-specific: even the question-nexus template's loop
is a probe. One primitive for "call this again / on this trigger," used everywhere.

## Triggers — anything that evaluates to true

**A trigger is anything that can evaluate to true.** A predicate. There is **no closed
enum** of trigger kinds (the shipped `interval/date/quantity/state` set was a
reification — see the reify-vs-flow catches below). Open examples, not a taxonomy:

- an interval elapsed, or a specific wall-clock time arrived (the "cron" subset)
- an amount of data accumulated past a threshold (queue depth — this is also how
  **backpressure** works: a filling channel fires a probe on its reader)
- a resource crossing a line — CPU pegged, memory, disk
- a state or event entered
- **a proof going green** — a proof is *precisely* a claim evaluated to true (a green
  VALIDATION), so proof is the exemplar quality-trigger; `PROVEME → PROVED` is a
  proof-trigger. The tester (Law 8) and the probe system are the same substrate.

New signal → new predicate, **not a schema change.**

## Where a probe is evaluated — at the shim of the device that cares

*CORRECTED 2026-08-04 by the shim-routes-everything ruling. This section used to read
"a probe is evaluated wherever its trigger's **data** is owned," and that is what put
one device's predicate inside another device.*

**A probe is evaluated at the shim of the device whose predicate it is** — the device
that chose the line and has the reason for caring. A probe reads what it needs to read;
the reading's owner is a *source*, not a host for the predicate.

- **Global** probes read genuinely shared data (the passage of time / the beat).
  Evaluated at the heartbeat level.
- **Everything else** is somebody's probe, and it fires at that somebody's shim.

Consequence: **one** firing path in the whole system. A device never has to ask whether
its watch runs here or over there — it runs here, always, because its shim is the thing
that fires its probes.

## The shim is the device's router — for everything, not just messages

*RULED 2026-08-04 by Akien (`CairnCommons/decisions/2026-08-04-the-shim-routes-everything.json`),
replacing the advertise → subscribe → poke protocol this section used to describe.*

**Each device owns its own everything as far as possible — that is encapsulation.** And
the piece that already stands between a device and the world is its **shim**: it fronts
the bus for the one device it knows. So the shim is not a message pipe that happens to
also fire probes. **The shim is the device's router, for everything it has to route** —
mail, predicates, and whatever else turns out to need routing. It can sort on a
predicate precisely because it is the one thing that knows both the bus and the device.

What this **deletes**: a device does **not** register its predicate inside a foreign
device. There is no menu to advertise, no subscription table to hold, no
resolve-my-own-method indirection. A device that cares about a line declares a `Probe`
with that line in its trigger, and **its own shim fires it** — the mechanism every shim
already has (`probes()` → `on_pulse` → poke). One mechanism, not two.

Worked example, restated: *"alert me at 80% CPU."* The device that wants the alert owns
that predicate — it is **its** line, chosen for **its** reason, and it belongs where the
reason is. It declares the probe; its shim evaluates it on the beat. The **host** is
still one thing with one owner, so `system_rackmount` still owns the *reading* (it is
the one that makes the host calls, and the OS-specific backing swaps behind it). But
owning the reading is all it owns: it is a **sampler**, not a broker for other devices'
predicates.

**What died with the protocol, said plainly.** The old shape claimed Law 6 for "the raw
reading never leaves the device." That was never Law 6 — Law 6 gates **writes**. The
reading-never-leaves clause was an extra invention wearing the law's name, and it bought
a registration protocol, a subscription table, and a second firing path, all to avoid a
number crossing a function call. The encapsulation it was reaching for is real; the
place to get it is the device's own shim.

## The bus in detail

- **Protocol at the edge.** The bus's semantics (channels, owned envelopes, retention,
  causality) are Cairn's; the wire protocol is a *swappable adapter*. MCP is the current
  lingua franca for agentic communication, so it is the adapter today — swap it when the
  ecosystem moves, the way `system_rackmount` abstracts an OS service behind a
  device-independent face. The protocol must not hold the design hostage.
- **One substrate; every surface is a view.** UU split logic between the mcp bus and
  "how the web server surfaced things." Cairn: the web server, the MCP inspector, a
  debug pane are all *read-projections* of the one bus. Nothing surfaced by re-deriving
  it elsewhere (Law 1).
- **Durable transit rides `db_domain`, owner-gated.** The bus does not open its own
  Postgres; a message in transit is an owned write through `db_domain`. That buys
  logged + inspectable for free and enforces one-owner.
- **Record-of-truth vs diagnostic surface, as physics (Law 7).** Permanent records
  (errors, announces-of-fact) never collapse and never expire; diagnostic channels
  (debug/info) may collapse in a view and expire on a rolling window (sudo_relay's
  pattern). The substrate always stores the full truth; only views collapse.
- **Channels per device** (Murderbot-feeds model, Martha Wells): **announce** (public
  feed — public conversations), **personal** (chat inbox — others post through the
  owner's gate), **info** + **debug** (logging). A device's `introspect()` surface can
  publish onto its announce feed, so *inspecting a device is reading its feed* —
  observability and messaging stop being two systems.
- **Every envelope carries why + causality** (sender, intention, reply-to), so the bus
  is a *replayable causal record*, not just traffic. A device woken from sleep rebuilds
  its context by reading its own feed history (horizon-of-awareness, made concrete).
- **The human is a native participant.** Akien has channels like any device; the web
  server is a view. Participation on the bus, not operation through a side door
  (get-Akien-out-of-ops at the messaging layer).

## The reify-vs-flow catches this session (specimens of learning-its-gates)

CC (I) froze Cairn-fluid categories three times; Akien caught each at n=1:

1. **rack = scheduler** — inferred from one MAP line; the rack is the *chassis* (bus +
   shims), not a scheduler.
2. **ground_loop = executor** — collapsed the heartbeat, the ticket-firing, and the
   scheduler into one device, losing "the ticket is the same unit no matter what fires
   it." The ground loop is *only* the heartbeat; firing lives in the shim.
3. **triggers = `interval/date/quantity/state` enum** — froze an open list of example
   predicates into a closed typed set and coined "quantity." A trigger is *anything that
   evaluates to true.*

The tell: I turn examples/metaphors into frozen taxonomies. The fix flows them apart.

**A fourth, caught 2026-08-04 — host service = subscription broker.** Different tell,
worth its own entry. From the true premise *"the host has one owner"* I built a
**registration protocol** — advertise, subscribe, resolve-internally — so that other
devices could keep their predicates in `system_rackmount`. Akien's catch: *"each device
should own its own everything as much as possible, that's encapsulation."* The premise
was fine; the leap from *one owner of the reading* to *one holder of everyone's
predicates* was not, and it cost a second firing path parallel to the one every shim
already has. **Tell: when I own a piece of shared data, I reach for a protocol around it
rather than a plain source others can read.** A broker is what a taxonomy looks like when
it is made of runtime instead of types — the same freezing reflex, one layer down.

## What this changes in code — DONE (reworked + proven 2026-07-18 evening)

The rework shipped the night the model converged, each piece proven bare AND under the
tester, each committed separately:

- the **bus** → BUILT (`cairn/bus/`, commit `d27ce1d`). The sole comms path; durable transit
  rides db_domain (owner `bus`); per-device channels (announce/personal records, info/debug
  diagnostic); record channels refuse to collapse, diagnostic views may (Law 7); every
  envelope carries why + causality (Law 5). Filed: MCP wire-adapter; per-device-owned channels.
- the **Probe primitive** → BUILT (`cairn/base/probe.py`, commit `ae2d372`). Immutable;
  a trigger is ANY predicate `(now, context) -> bool`, NOT a named kind (the enum is deleted);
  evaluated where its data is owned (Law 6).
- `BaseShim` → REWORKED (`cairn/base/shim.py`, `ae2d372`). Gains per-pulse probe-firing
  (`on_pulse`, batch-safe), message receipt + on-demand device start (`deliver`/`_start_device`).
  The long-deferred one-loop primitive is resolved: the heartbeat IS the one loop. Filed: each
  device its own OS process (the shape — start-on-demand — is proven; real spawn grows against need).
- `ground_loop` → STRIPPED to the heartbeat (`cairn/ground_loop/loop.py`, commit `a535de0`).
  `beat(now, context)` pulses subscribed shims; no `run_driver`, no resolve, no write. The
  method-registry + collect fixtures + executor proof were RETIRED (the proven-space registry
  returns with the emit-chokepoint when a real consumer pulls it).
- `system_rackmount` → REWORKED to the *system device* (`cairn/system_rackmount/`, commit
  `faafb70`). Owns host-resource predicates; advertise → subscribe → poke; evaluates locally so
  the reading never leaves (Law 6); the central `SchedulerService` + `interval/date/quantity/
  state` enum are DELETED. Its capstone proof composes every piece above end-to-end.
  **SUPERSEDED IN SPEC 2026-08-04 and therefore RED until the code catches up** (Law 9): the
  shim-routes-everything ruling deletes advertise/subscribe/poke and leaves this device owning
  the *reading* only. The predicate goes home to the device that cares, fired by its own shim.
  The code still ships the broker — that is the red, and it is named here rather than left to
  be discovered by the next reader of a charter that no longer describes the design.
- **tickets** → the mutable workflow species stays DISTINCT and DEFERRED — the probe/ticket
  boundary is now clean in code (a probe is the immutable worker; a ticket is the mutable
  node), but the ticket state machine still waits on the emit-chokepoint
  (`CairnCommons/tickets/state-machine-physics.json`). Not built here, by design (not the goof).
