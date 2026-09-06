# The command lazy-inits the system — who starts what

*Spanning intention. Akien has walked CC through this twice (the second time 2026-09-06:
"This is my second time going over this with you"). This file exists so there is no third.
Nothing here is RULED-marked; it is his description, verbatim, with CC's reading beneath it and
the two readings named where his words admit two.*

## Akien, verbatim, 2026-09-06

> now lets talk about cairn and who starts the ground loop, databas, shims, etc. This is my
> second time going over this with you: lets say i type 'cairn librarian show status hot' now
> before we go any farther 'hot' isn't in there yet. I added that just now. hot would mean
> don't show cached values, get the real values. so, to keep this easy: the cairn command sees
> that the venv exists, and the db, and that it's all set up. it also sees that the librarian
> is a device (there's a resolver in cairn) and so goes to cairn/cairn/librarian/bin/librarian
> and passes in 'show status hot'. this launches the librarian's shim (if it's already running,
> this new shim passes the command to the running shim and returns the reply and exits). all
> shims, on start, check to see if the ground loop is running. if it' not, the shim launches
> the ground loop. the shims are the same process as the bus (the librarian like all devices is
> a different process communicating to the shim via ipc or whatever the device requires (eg a
> calibre device shim is just a calibre database interface). the shim's resolver says 'show
> status = get json status and format for humans' or something similar. but then it also sees
> 'hot' which means the device has to be running. so it starts the librarian. everythign
> automatically lazy inits. the librarian replies to the shim with the updated status, which is
> then returned to me in the console.

Same day, on the pipe every one of these hops rides (recorded in full in
`I-heartbeat-probes-and-bus.md`): device → IPC → its own shim → bus → the addressee's shim →
IPC → the addressee; everybody, except the db, which gets a pass only because of expected
volume. And: nobody has their own ground loop; there is one for everybody. And: nothing in the
ground loop except the pulse, the ground loop control flags, and the devices-found list. Ever.

## The chain, step by step (CC's reading)

`cairn librarian show status hot`

1. **`cairn`** (the one entry point, `bin/cairn`) checks the box is set up: the venv exists, the
   db is there, "it's all set up." Then it resolves `librarian` as a device — there is a
   resolver in cairn — and execs the device's launcher, `devices/librarian/bin/librarian`,
   passing `show status hot` through verbatim.
2. **The launcher starts the librarian's shim.** If a shim for this device is already running,
   the new one hands the command to the running one, prints the reply, and exits. The shim is
   the device's always-on front; a second copy is a courier, not a second front.
3. **Every shim, on start, checks the ground loop.** Not running → the shim launches it. This is
   the only way the ground loop ever gets started: as a side effect of the first shim that
   needs a pulse. No service unit, no boot script, no superclaude special case — lazy init.
4. **The shim IS the bus process.** "The shims are the same process as the bus." The device is
   a different process and talks to its shim over IPC — "or whatever the device requires": a
   calibre device's shim is just a calibre database interface, because that is the IPC that
   device has.
5. **The shim's resolver parses the verbs.** `show status` = get the JSON status and format it
   for humans (the standard vocabulary, ticket 15d6a0ef9c11). `hot` = do not answer from what
   the shim holds; get the real values — which means the device has to be running, so the shim
   starts the librarian.
6. **The librarian answers its shim** with the updated status; the shim formats it; the console
   prints it. Everything along the way lazy-inited, and none of it is torn down: the shim, the
   ground loop and the device stay up for the next command.

## Where his words admit two readings — named, not resolved

**"The shims are the same process as the bus."** Two shapes fit the sentence:

- (a) **One bus process hosting every shim.** The first `cairn <device>` on the box starts it;
  every later shim is a registration inside it; a device's process reaches its shim by IPC into
  that one process. One pipe in physics: one ring, one flush, one log.
- (b) **One process per device's shim, each holding the bus.** Then N shims are N rings, and the
  only place their messages meet is the db after the flush — which is the shape the same day's
  "one pipe, we learn faster" was stated against.

CC reads (a), because (b) contradicts the one-pipe rule stated in the same conversation and
reproduces the nine private buses measured that morning. (a) also matches step 2 exactly: "if
it's already running, this new shim passes the command to the running shim" — the running one
is the bus process, with this device's shim registered in it.

**Resolved by Akien, 2026-09-06 — (a), and wider than a box:**

> one bus per cairn instance. this is actually not limited to a single computer, but we
> haven't gotten that far yet. we have 4 laptops i7s 9th, 10th, 10th, and 12th gen. 16gb. and
> an 8th gen asus laptop i7 20gb and a rpi400. at one point, during the very first iteration of
> this work, we had them all running as a swarm, reading the training corpus overnight with NO
> GPUs on local hardware with 10 MINUTE timeouts. All on one bus. One master db, and each laptop
> had a live backup cross syncing in real time.

So the unit the bus belongs to is the **cairn instance**, not the host. Today an instance is
one laptop and the bus is one process on it; the design already intends an instance that spans
six machines (the four i7 laptops, the Asus, the rpi400) on one bus with one master db and a
live cross-synced backup per box. That was built and ran once, in the first iteration, with no
GPUs and 10-minute timeouts. What follows for the chain above:

- Step 4's "one bus process" is one bus **per instance**; when the instance spans hosts, the
  bus spans them and the shims on each host register into the same bus, not a local one.
- Step 3's ground loop is per instance for the same reason (one for everybody), so a shim on a
  second host checks for *the instance's* loop, not for a loop on its own host.
- The db's pass on the one-pipe rule (volume) is what the "one master db + live backup per
  laptop" shape was already exercising: db traffic goes direct, everything else rides the bus.
- The ring buffer and the flush-to-db-on-pulse is the piece that lets "instantly, no db access"
  hold on a shared bus across hosts; where the ring physically lives when the bus spans hosts is
  **not designed yet** ("we haven't gotten that far yet").

None of the multi-host part is built or ticketed; it is the horizon the single-box shape must
not foreclose. The measurable now: any design that binds the bus to the host (a per-host
socket path with no instance name in it, a host-local singleton lock for the loop) is a
decision against this paragraph.

## Measured against the code, 2026-09-06 (CC)

- `bin/cairn` resolves `cairn <device> <verb>` through the filesystem to
  `~/.cairn/devices/<device>/0/bin/<verb>` (symlinked to class-space) — the resolver exists. It
  checks nothing about the venv or the db (no such lines in the script).
- `devices/librarian/0/bin/librarian` starts the *web server listener* as a transient systemd
  unit and lets the listener wire the librarian's shim and the ground loop in-process. So today
  the "shim" the launcher starts is the web server, and the bus it uses is that process's
  private one.
- No shim checks for the ground loop on start (`grep claim_singleton|ground_loop` over
  `devices/*/shim.py`: none). `tools/base/shim.py` mentions the loop only in its docstring.
  The ground loop's own record read DEAD, last beat ~2 days old, 32 subscribers.
- Nine modules build a private bus + ground loop in-process via `bus_client.connect_bus()`;
  the private beat costs ~89 s per call (measured), the actual request 0.0 s.
- The device↔shim IPC exists in one primitive form: codemother's shim writes mail to
  `~/.cairn/devices/codemother/0/mail/` and returns no reply.
- `hot` is not parsed anywhere. `show`/`get` resolve through `declared_views()` in the base
  device class; `list`, `start`, `stop`, `settings` (RULED 2026-09-06 as the root set) are not
  built yet.

## What this retires

- Any launcher, listener, or tool that constructs its own `GroundLoopDevice` or `BusDevice`
  (`bus_client._wire()` is the seam; its docstring already calls itself "one seam to change").
- The ring cast's stated assumption "the bus is single-process, in-memory delivery via hooks,
  not IPC" (sorted berth `sorted-20260904T171337-82d43e9e4c65`, awaiting review) — the ring
  stays; where it lives changes.
- The name "ground-loop flush" wherever it appears (the flush is the bus's; the pulse is what it
  listens for).
