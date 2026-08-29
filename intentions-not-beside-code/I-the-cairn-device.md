# The cairn device

*Ruled by Akien, 2026-08-19. Filed as an intention because the device that IS Cairn
is spanning — it has no single code address, it is the whole project's control surface.*

## What

A singleton device (`cairn`, instance 0) that represents all-of-Cairn as a
running thing. Not the host (that is `system_rackmount`) — the PROJECT: the
software, its components, and their collective state.

## Why

There is no device that means "all of Cairn." Individual devices own their own
state, but nobody owns the system-wide controls:

- **The trouble ticket list** — a runtime thing, currently homeless. The cairn
  device owns it and surfaces it on its pane.
- **Circuit breakers for all devices** — the cairn device's settings pane carries
  the master switches.
- **System-wide state** — `live()` across all trouble lanes, roster health,
  the normal-operating-state of the whole.

## The trouble panel (child a)

A new web pane on the cairn device. Two-sided layout:

- **Left:** the trouble list (all live tickets).
- **Right, top:** a red light — bright red if any live, dull reddish grey if none.
- **Right, below the light:** contents of the currently selected trouble from the list.
- Starts at row 0 on first load.
- Dynamic page — requires client-side interaction (click-to-select, live updates).

## The web server graduates to Starlette (child b)

The current web_server is stdlib `http.server` — synchronous, no WebSocket, no
dynamic pages. The trouble panel needs real-time push (the red light) and
client-side interaction (row selection).

Starlette + uvicorn is the ruled framework (CC's recommendation, February 2026;
Akien confirmed 2026-08-19). Already built and proven in TheIgors
(`lab/claudecode/utility_closet_server.py`). The graft brings:

- Async request handling
- First-class WebSocket (fan-out to all connected browsers)
- Static file serving
- No build step, no npm

This is a graft from Cairn's own sibling project, not a new dependency decision.

## Complexity-axis placement

The cairn device is a **device** — a top-level thing that is its own process
and goes in the rack. Its held machines and tools nest under it at
`devices/cairn/0/` in both roots.

## Held machines

The cairn device holds three machines at `devices/cairn/machines/`:

- **ground_loop** — the heartbeat: a wall-clock-driven loop that beats the roster
  and writes its own liveness record.
- **bus** — the message bus: mail-based inter-device communication.
- **harbor_master** — the clearance gate: ownership verification, grants, and
  voyage lifecycle for the emit chokepoint.

These were absorbed from independent device directories (ticket
`cairn-device-absorbs-foundational-infrastructure`, 2026-08-29). They are
foundational infrastructure — they serve every device but own no independent
process of their own, which is the machine rung, not the device rung.

## What this does NOT own

- Host-level concerns (packages, OS, the laptop) — `system_rackmount`
- Individual device state — each device owns its own (Law 6)
