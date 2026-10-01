# RULE 1 — Encapsulation

*Concept-piece, and a ROOT: implemented by every component boundary in the system, so no one
directory can hold it. Cast 2026-10-01 as ticket `8e3474a6ae43`. The text below was reviewed and
AGREED by Akien the same day; it supersedes his shouted first version wherever they differ. It is
numbered RULE 1 and stands above the Laws without renumbering them — a Law's number is its address.*

## The rule (agreed text, 2026-10-01)

Every component talks to every other component only through that component's public
interface. Devices, machines, tools, and anything else with a boundary are components.
A component's internals are private to it.

- **A device's public interface is the bus**, plus any client tool it publishes for traffic
  the bus can't carry. Nothing outside a device reaches into its code: not another device,
  not a machine or tool held by another device, not a skill. Device A to device B goes
  A → bus → B's shim → B.
- **A machine's or tool's public interface is what it declares.** Inside a device, machines
  and tools call each other freely through those interfaces. A shared tool is used the same
  way by all of its users. Reaching past a declared interface is a violation, wherever the
  caller sits.
- **Why:** it limits a change to the component that made it. Contracts let A change without
  breaking B. This is good practice everywhere, not special to Cairn.
- **What follows:** a ticket's build lives inside its own component, and its proofs and
  hollow check measure only that component. A build touching another component's internals
  reds as a boundary violation. Contracts are proved on both sides.
- **Physics:** one check over every component reds any reach past a public interface, the
  moment it is written.

**Agreed details.** (1) Public interfaces are **declared explicitly** — a component lists its
public surface (`public_interface` in its charter), and anything not listed is internal.
(2) db_domain's 2026-08-31 exception becomes a **published client tool**: everyone imports the
tool, the tool talks straight to the db proxy over its socket (no bus hop, for graph-tree
volume), and db_domain can change everything underneath.

## Akien, verbatim, 2026-10-01

> NO DEVICE MAY IMPORT ANOTHERS DEVICE PERIOD. ONLY OVER THE BUS.

> RULE 1 is this: ENCAPSULATION. ... WHY? BECUASE THAT REDUCES IMPACTS OF CHANGES ACROSS
> BOUNDARIES. THIS APPLIES TO MORE THAN DEVICES, MACHINES AND TOOLS.

> i said something that could be interpreted as: a machine in one device can't communicate with
> another machine in the same device. that's not so. But the machines have public interfaces, as do
> the tools and the devices and everything else. so perhaps the better way to phrase it is this:
> DEVICES, MACHINES, TOOLS, each >>COMPONENT<< may only talk to other components via their public
> interfaces. and the public interface for devices is the bus.

> If we are stricly encapsulating everything LIKE WE SHOULD NOT JUST FOR THIS PROJECT BUT ALWAYS
> because it's good practice... then what files changed elsewhere doesn't matter one whit.

A direction signal, recorded and not acted on: *"a long time ago i asked you if this should be
seperate repos. one for each device. you said no. that was a mistake."*

## The lived symptom

A change in one device breaks another that reached into its code, and the test strategy, unable to
trust any boundary, re-proves everything — *"your testing strategy APPEARS to assume changes anywhere
could bork anything so test everything."*

## Pointers

- Parent ticket: `CairnCommons/tickets/8e3474a6ae43-rule-1-encapsulation.json` (eight children)
- The physics: `encapsulation_holds` in `cairn/machines/build_inspector` (ticket `56d1aff4455e`), over
  `import_sieve.import_sites` (ticket `a907458344ba`)
- Supersedes: ticket `7b5c539cb58c`; the sieves `device_isolation_holds` and `machine_imports_no_device`
