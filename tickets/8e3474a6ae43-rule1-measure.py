"""8e3474a6ae43 — RULE 1 (encapsulation), the parent falsifier measured.

    python3 tickets/8e3474a6ae43-rule1-measure.py            # from CairnCommons; exit 0 = green

Three clauses, each read off disk, each printed with its count:

  1. CLAUDE.md carries a '## RULE 1' block ABOVE '## The Laws' that points at
     intentions-not-beside-code/I-rule-1-encapsulation.md; that .md carries every sentence of
     Akien's agreed 2026-10-01 text (~/.cairn/foreground-decisions.md, the FINAL RULE 1 TEXT
     block) word for word (markdown and arrows folded); and the Laws' numbers are unchanged:
     each number opens with the same words it did at the last CLAUDE.md commit before RULE 1
     (925c9086f15f, before 2026-10-01T12:00).
  2. every child of 8e3474a6ae43 (by state.json `parent`) stands terminal: PROVED, SUPERSEDED,
     KILLED, RETIRED or DROPPED, and at least one is PROVED.
  3. the live encapsulation sieve (build_inspector.encapsulation_breaches over the whole cairn
     repo — cairn/, skills/, bin/, press_office/; launchers/ no longer exists) returns zero rows.

`--control` swaps one input per clause for a falsifying one (a Laws block with 1 and 2
swapped, a child forced to BUILDME, one synthetic breach row) and must exit 1 with all three red.
"""
from __future__ import annotations

import glob
import json
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
CAIRN = HOME / "dev/src/cairn"
COMMONS = HOME / "dev/src/CairnCommons"
PARENT = "8e3474a6ae43"
BEFORE_RULE1 = "925c9086f15f"
TERMINAL = {"PROVED", "SUPERSEDED", "KILLED", "RETIRED", "DROPPED"}


def words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", s.lower())


def laws(text: str) -> dict[str, str]:
    block = text.split("## The Laws", 1)[1].split("\n## ", 1)[0]
    return {m.group(1): " ".join(words(m.group(2))[:6])
            for m in re.finditer(r"^ ?(\d+)\. (.*)$", block, re.M)}


def clause1(control: bool) -> tuple[bool, str]:
    md = (CAIRN / "CLAUDE.md").read_text()
    i_rule, i_laws = md.find("## RULE 1"), md.find("## The Laws")
    block = md[i_rule:i_laws] if 0 <= i_rule < i_laws else ""
    points = "I-rule-1-encapsulation.md" in block
    src = (HOME / ".cairn/foreground-decisions.md").read_text()
    agreed = src.split("RULE 1 — ENCAPSULATION.", 1)[1].split("Agreed details:", 1)[0]
    sentences = [s for s in re.split(r"(?<=[.:])\s+", agreed.replace("*", " ")) if len(words(s)) >= 3]
    body = " ".join(words((COMMONS / "intentions-not-beside-code/I-rule-1-encapsulation.md").read_text()))
    missing = [s for s in sentences if " ".join(words(s)) not in body]
    then = laws(subprocess.run(["git", "-C", str(CAIRN), "show", f"{BEFORE_RULE1}:CLAUDE.md"],
                               capture_output=True, text=True, check=True).stdout)
    now = laws(md)
    if control:
        now = dict(now); now["1"], now["2"] = now["2"], now["1"]
    moved = [n for n, w in then.items() if now.get(n) != w]
    ok = points and not missing and not moved and len(then) >= 9
    return ok, (f"RULE 1 block above the Laws pointing at the .md: {points}; agreed sentences "
                f"{len(sentences) - len(missing)} of {len(sentences)} verbatim; Laws then {len(then)}, "
                f"renumbered {moved or 'none'}")


def clause2(control: bool) -> tuple[bool, str]:
    kids = {}
    for p in glob.glob(str(COMMONS / "tickets/*.state.json")):
        s = json.loads(Path(p).read_text())
        if isinstance(s, dict) and s.get("parent") == PARENT:
            m = re.search(r"\[([A-Z]+)", s.get("workflow_and_state", ""))
            kids[Path(p).name[:12]] = m.group(1) if m else "?"
    if control and kids:
        kids[sorted(kids)[0]] = "BUILDME"
    live = {k: v for k, v in kids.items() if v not in TERMINAL}
    counts = {v: list(kids.values()).count(v) for v in sorted(set(kids.values()))}
    ok = bool(kids) and not live and counts.get("PROVED", 0) > 0
    return ok, f"children {len(kids)}: {counts}; not terminal: {live or 'none'}"


def clause3(control: bool) -> tuple[bool, str]:
    sys.path.insert(0, str(CAIRN))
    from cairn.machines.build_inspector.inspector import encapsulation_breaches
    rows = encapsulation_breaches(str(CAIRN))
    if control:
        rows = rows + [{"file": "control", "line": 0, "module": "cairn.devices.x.y"}]
    return not rows, f"encapsulation_breaches rows: {len(rows)}" + (
        "" if not rows else " — " + "; ".join(f"{r['file']}:{r['line']} {r['module']}" for r in rows[:10]))


def main() -> int:
    control = "--control" in sys.argv
    reds = 0
    for n, fn in enumerate((clause1, clause2, clause3), 1):
        ok, said = fn(control)
        reds += not ok
        print(f"clause {n}: {'GREEN' if ok else 'RED'} — {said}")
    print(f"{3 - reds}/3 green{' (control)' if control else ''}")
    return 1 if reds else 0


if __name__ == "__main__":
    raise SystemExit(main())
