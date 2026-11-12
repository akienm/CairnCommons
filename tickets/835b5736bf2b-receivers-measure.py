"""835b5736bf2b — every probe has a receiver, the parent falsifier measured.

    python3 tickets/835b5736bf2b-receivers-measure.py            # from CairnCommons; exit 0 = green

  1. RECEIVER CENSUS. Over every tickets/*.state.json, every WATCHME spec that names a probe
     whose file is on disk, on a ticket not standing at FIXME, carries a `receiver` dict. A
     spec whose probe file is gone from the repo cannot fire, so it has no data to receive.
     It is counted and printed, never green-washed (each such spec sits on a dead ticket).
  2. CHILDREN. Every child of 835b5736bf2b (by state.json `parent`) has crossed PROVED: it
     stands at PROVED, or its workflow string shows a PROVED step passed before a later
     terminal (a DROPPED after PROVED, by Akien's ruling, keeps its crossing).
  3. NO RECEIVER WRITTEN TO SATISFY THE FIELD. Each distinct receiver's `in` is a directory
     on disk holding code that serves the verb the probes post to, and every armed probe
     with a receiver posts there: its source names `to="codemother"` and
     `verb="machines/watchme/watch"`, and the receiver's code registers `watch`.

`--control` adds one armed spec without a receiver, forces one child to BUILDME, and points
one receiver at a directory that does not exist. It must exit 1 with all three red.
"""
from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

HOME = Path.home()
CAIRN = HOME / "dev/src/cairn"
COMMONS = HOME / "dev/src/CairnCommons"
PARENT = "835b5736bf2b"
VERB = "machines/watchme/watch"


def states():
    for p in sorted(glob.glob(str(COMMONS / "tickets/*.state.json"))):
        s = json.loads(Path(p).read_text())
        if isinstance(s, dict):
            yield Path(p).name[:12], s


def here(wf: str) -> str:
    m = re.search(r"\[([A-Z]+)", wf or "")
    return m.group(1) if m else "?"


def specs(s: dict) -> list[dict]:
    w = s.get("watchme")
    return [x for x in (w if isinstance(w, list) else [w]) if isinstance(x, dict) and x.get("probe")]


def main() -> int:
    control = "--control" in sys.argv
    rows = [(tid, s, sp) for tid, s in states() for sp in specs(s)]
    if control:
        rows.append(("control00000", {"workflow_and_state": "x: [BUILDME]"},
                     {"probe": "cairn/devices/aider_shim/probes/edit_survival_probe.py"}))
    armed = [(t, s, sp) for t, s, sp in rows if (CAIRN / sp["probe"]).is_file()]
    gone = [(t, here(s["workflow_and_state"])) for t, s, sp in rows if not (CAIRN / sp["probe"]).is_file()]
    lacking = [(t, sp["probe"]) for t, s, sp in armed
               if here(s.get("workflow_and_state")) != "FIXME" and not isinstance(sp.get("receiver"), dict)]
    ok1 = not lacking
    gone_states = sorted({st for _, st in gone})
    print(f"clause 1: {'GREEN' if ok1 else 'RED'} — {len(rows)} probe-naming specs; {len(armed)} armed "
          f"(probe on disk), {len(lacking)} armed outside FIXME lacking a receiver {lacking[:10] or ''}; "
          f"{len(gone)} name a probe no longer on disk, on tickets at {gone_states}")

    kids = {t: s["workflow_and_state"] for t, s in states() if s.get("parent") == PARENT}
    if control and kids:
        kids[sorted(kids)[0]] = "code-seam@v2: THINKME -> [BUILDME]"
    def crossed(wf):
        return here(wf) == "PROVED" or "PROVED -> [" in wf
    unproved = [t for t, wf in kids.items() if not crossed(wf)]
    counts = {}
    for wf in kids.values():
        counts[here(wf)] = counts.get(here(wf), 0) + 1
    ok2 = bool(kids) and not unproved
    print(f"clause 2: {'GREEN' if ok2 else 'RED'} — children {len(kids)}: {counts}; never crossed PROVED: "
          f"{unproved or 'none'}")

    receivers = {}
    for t, s, sp in armed:
        r = sp.get("receiver")
        if isinstance(r, dict):
            receivers.setdefault(r.get("in"), []).append((t, sp["probe"]))
    if control:
        receivers["cairn/devices/nowhere/machines/none"] = [("control00000", "x")]
    bad = []
    for where, probes in receivers.items():
        d = CAIRN / (where or "")
        code = " ".join(p.read_text() for p in d.glob("*.py")) if where and d.is_dir() else ""
        if not re.search(r"""["']watch["']""", code):
            bad.append(f"{where}: no code registering 'watch'")
        for t, probe in probes:
            src = (CAIRN / probe).read_text() if (CAIRN / probe).is_file() else ""
            if not (re.search(r"""to=["']codemother["']""", src) and VERB in src):
                bad.append(f"{t} {probe}: does not post to codemother {VERB}")
    ok3 = bool(receivers) and not bad
    print(f"clause 3: {'GREEN' if ok3 else 'RED'} — {len(receivers)} distinct receiver(s) "
          f"{sorted(receivers)}, {sum(len(v) for v in receivers.values())} armed probes routed; "
          f"findings {bad[:10] or 'none'}")
    reds = 3 - ok1 - ok2 - ok3
    print(f"{3 - reds}/3 green{' (control)' if control else ''}")
    return 1 if reds else 0


if __name__ == "__main__":
    raise SystemExit(main())
