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

## Where a probe is evaluated — Law 6 for triggers

**A probe is evaluated wherever its trigger's data is owned.** So device-local data
is never exported; only the *wake-up* crosses the bus, never the raw data it tested.

- **Global** probes read genuinely shared data (the passage of time / the beat).
  Evaluated at the heartbeat level.
- **Device-specific** probes read a device's own data (its queue depth, an internal
  metric). Evaluated *inside* the device; the data stays home.

Consequences: minimal data movement (telemetry never crosses the bus just to be
tested), and encapsulation by construction.

## Advertise → subscribe → poke (the registration protocol)

A caller never needs to know a device's internals (`object.object.method`):

1. A device **advertises a menu** of probes it offers — e.g. "I accept a CPU-threshold
   probe (takes a value)" — as one item in a list of its offerings (part of its
   Form v0 #2 surface: inspect a device, see what probes it offers).
2. A caller **subscribes**: *"I'll take one of those, value 80, here's my probe
   address."*
3. The device **resolves its own method internally** and wires it into the probe.
4. When the predicate goes true, the device **pokes the caller's address**. The caller
   gets its wake-up and never saw a CPU number.

Owner-gated throughout (Law 6). Advertise / subscribe / poke are all just bus messages.

Worked example: *"alert me at 80% CPU."* CPU is the **system device's** data (it is the
one that can make the CPU calls). So the CPU-threshold probe lives on the system
device; any device that wants it asks the system device (owner-gated), which evaluates
locally and pokes the requester when true. This is what "abstracts host services
device-independently" cashes out to — **`system_rackmount` = the system device: owner
of host-resource predicates (CPU/memory/disk), serving threshold probes on request.**
NOT a central scheduler. (Settles the earlier open A/B question → A.)

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

## What this changes in code — DONE (reworked + proven 2026-07-18 evening)

The rework shipped the night the model converged, each piece proven bare AND under the
tester, each committed separately:

- the **bus** → BUILT (`cairn/devices/bus/`, commit `d27ce1d`). The sole comms path; durable transit
  rides db_domain (owner `bus`); per-device channels (announce/personal records, info/debug
  diagnostic); record channels refuse to collapse, diagnostic views may (Law 7); every
  envelope carries why + causality (Law 5). Filed: MCP wire-adapter; per-device-owned channels.
- the **Probe primitive** → BUILT (`cairn/tools/base/probe.py`, commit `ae2d372`). Immutable;
  a trigger is ANY predicate `(now, context) -> bool`, NOT a named kind (the enum is deleted);
  evaluated where its data is owned (Law 6).
- `BaseShim` → REWORKED (`cairn/tools/base/shim.py`, `ae2d372`). Gains per-pulse probe-firing
  (`on_pulse`, batch-safe), message receipt + on-demand device start (`deliver`/`_start_device`).
  The long-deferred one-loop primitive is resolved: the heartbeat IS the one loop. Filed: each
  device its own OS process (the shape — start-on-demand — is proven; real spawn grows against need).
- `ground_loop` → STRIPPED to the heartbeat (`cairn/devices/ground_loop/loop.py`, commit `a535de0`).
  `beat(now, context)` pulses subscribed shims; no `run_driver`, no resolve, no write. The
  method-registry + collect fixtures + executor proof were RETIRED (the proven-space registry
  returns with the emit-chokepoint when a real consumer pulls it).
- `system_rackmount` → REWORKED to the *system device* (`cairn/devices/system_rackmount/`, commit
  `faafb70`). Owns host-resource predicates; advertise → subscribe → poke; evaluates locally so
  the reading never leaves (Law 6); the central `SchedulerService` + `interval/date/quantity/
  state` enum are DELETED. Its capstone proof composes every piece above end-to-end.
- **tickets** → the mutable workflow species stays DISTINCT and DEFERRED — the probe/ticket
  boundary is now clean in code (a probe is the immutable worker; a ticket is the mutable
  node), but the ticket state machine still waits on the emit-chokepoint
  (`CairnCommons/tickets/state-machine-physics.json`). Not built here, by design (not the goof).

## One pipe, everybody, except the db (Akien, 2026-09-06 — sharpening, not RULED)

Akien, verbatim, 2026-09-06, on codemother reaching the inference proxy:

> lets talk about 'talking to the infernece proxy'... that should be an ipc from codemother
> to codemother's shim, then over the bus to the inference proxy's shim and thence over ipc
> to the inference proxy. Why? because if everything goes thru one pipe, we learn faster. and
> this is how everybody should communicate with everybody... except the db.

> and the db gets a pass only because i expect a LOT of db traffic

What this sharpens in the sections above:

- **The device never touches the bus.** The path is device → (IPC) → its own shim → bus →
  the addressee's shim → (IPC) → the addressee. The shim is the only thing that holds a bus
  handle. "Devices never hold references to each other" already stood; this adds that a
  device does not hold a reference to the bus either — its shim is its whole outside.
- **The why is learning rate, not tidiness.** One pipe means every inter-device exchange is
  one recorded observation at one address (Law 10), and whatever learns from traffic
  (codemother, the librarian) reads one log instead of N. Every private side-channel is a
  measurement that did not get taken.
- **The db exception is volume, not privilege.** `db_domain` keeps its direct path only
  because the traffic is expected to be large; it is the one substrate whose per-message cost
  would dominate if it rode the pipe. It is not an exemption from ownership or from logging.

**Measured against the code on the day (2026-09-06, CC):** `cairn/tools/base/bus_client.py`
builds the bus, the ground loop and the addressee's shim *inside the caller's process* —
its own docstring says "Today: in-process construction." So today there is one pipe in
name and zero pipes in physics: nine modules call `connect_bus()` directly
(tools/base/validation.py, intention_extractor/live.py, web_server/listener.py,
aider_shim/interceptor.py, codemother/watch.py, codemother/seed_trees.py,
librarian/live.py, skills/chart/live.py, and the tool itself), each booting a private bus
and a private beat. The week's "inference_domain hangs on the bus" was that private beat
running every discovered probe before the request was even sent (stack captured under
`faulthandler`: the beat sat in `no_component_reaches_proved_with_an_uncharted_build`
globbing the ticket corpus). Timed the same evening, unbuffered: wiring the bus and shims in-process took 0.0s, the private beat took 89.3s (an earlier run of the same script exceeded a 240s cap), and the request itself — embed over the bus to inference_domain to hex.local — took 0.0s and returned a 768-dimension vector. The pipe is instant; the toll booth every caller builds in front of it is the whole cost. The device-to-shim IPC exists in one primitive form: codemother's
shim writes mail to `~/.cairn/devices/codemother/0/mail/` and returns no reply.

Akien, verbatim, 2026-09-06, on the private beats above:

> nobody should have their own ground loop. there's one for everybody. we talked yesterday or
> the day before about using the ground loop pulse to echo the ring buffer to disk.

So the pipe has a shape: **one ground loop process for the box**, holding the one bus; the bus's
hot path is an in-memory ring (cast 2026-09-04, sorted berth
`sorted-20260904T171337-82d43e9e4c65`; its title says "with-ground-loop-flush", which is CC's
naming and WRONG in attribution — see the correction below): a message that a device comes
for is handed over from the ring instantly, no DB; a message whose receiver was not that fast
is written to the DB by THE BUS when the pulse comes by. The durable log is those rows. A caller reaches the bus through its own shim's IPC to that
one loop — never by constructing a loop of its own. Measured 2026-09-06: no ground loop
process was running on the box at all; every "bus" in use was a private one.

**CORRECTION (Akien, 2026-09-06, verbatim — CC had written "ground-loop flush"):**

> NO I DIDN'T SAY GROUND LOOP FLUSH. NOTHING IN THE GROUND LOOP EXCEPT THE PULSE, THE GROUND
> LOOP CONTROL FLAGS, AND THE DEVICES FOUND LIST. EVER. But when we last talked about the bus,
> we talked about having a ring buffer so if a new message came in, and a device came for that
> message, it was just there instantly no db access. if the reciver wasn't that fast, that ring
> buffer would go to the db when the ground loop pulse came by.

The ground loop's contents are closed: pulse, control flags, devices-found list. The flush is
the bus's own act; the pulse is only what it listens for. Any name, docstring or field that
says "ground loop flush" is drift and is to be renamed when touched.
