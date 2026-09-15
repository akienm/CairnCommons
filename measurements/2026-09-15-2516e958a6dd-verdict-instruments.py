"""The instruments behind ticket 2516e958a6dd's verdict artifact — a probe resolves its
owning ticket through the one locator.

One subcommand per validate criterion (berth validate-20260915T121526-c6a28d16c2eb), each
exiting 0 only when the criterion holds against the LIVE world: the proofs are RUN, the
locators are CALLED, the census is re-taken over probes/*.py, the seals are read from the
validation store, the diff is read from git. Berthed in the commons because the verdict door
RE-RUNS what it is handed.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: grammar probe census seal
"""
import glob
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
sys.path.insert(0, str(ROOT))
ENV = {**os.environ, "PYTHONPATH": str(ROOT)}
G_PROOF = "cairn/tools/chain/proofs/test_chain_grammar.py"
P_PROOF = "cairn/tools/base/proofs/test_probe.py"
BUILD_COMMIT = "16e1577"   # the build's commit, 2026-09-15 12:18 local
LIVE_STEM = "2516e958a6dd-a-probe-resolves-its-owning-ticket-through-the-one-locator"


def _run(cmd, timeout=600):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout, env=ENV)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"  {' '.join(cmd[-3:])}: rc={r.returncode} {tail[:120]}")
    return r.returncode, r.stdout


def grammar():
    from cairn.tools.chain.grammar import ticket_path
    ok = True
    for _ in (1, 2):
        rc, out = _run([sys.executable, "-m", "pytest", G_PROOF, "-q", "-p", "no:cacheprovider"])
        ok &= rc == 0 and "10 passed" in out
    live = ticket_path(LIVE_STEM)
    print(f"  live stem -> {live}")
    ok &= bool(live) and live.endswith(LIVE_STEM + ".json")
    with tempfile.TemporaryDirectory(prefix="verdict-2516e958a6dd-") as d:
        Path(d, "abcdef012345-a-thing-that-ends-in-it.json").write_text("{}")
        tail = ticket_path("it", tickets_dir=d)
        print(f"  'it' under a synthetic dir -> {tail}")
        ok &= tail is None
    text = (ROOT / G_PROOF).read_text()
    ok &= "test_a_full_stem_resolves_before_the_regex_gates_and_a_tail_still_does_not" in text
    return 0 if ok else 1


def probe():
    ok = True
    for _ in (1, 2):
        rc, out = _run([sys.executable, P_PROOF])
        ok &= rc == 0 and "census: names=" in out and "hex-holes=0 disagree=0" in out
    r = subprocess.run([sys.executable, "-c", "import sys, cairn.tools.base.probe; "
                        "print(sorted(m for m in sys.modules if m.startswith('cairn.tools.chain')))"],
                       cwd=ROOT, capture_output=True, text=True, env=ENV)
    print(f"  chain modules loaded by importing probe: {r.stdout.strip()}")
    ok &= r.returncode == 0 and r.stdout.strip() == "[]"
    text = (ROOT / P_PROOF).read_text()
    ok &= "test_owning_ticket_answers_to_every_spelling_and_holes_with_the_path" in text
    ok &= "test_owning_ticket_agrees_with_the_one_locator_over_every_probe" in text
    return 0 if ok else 1


def census():
    from cairn.tools.base.probe import owning_ticket
    from cairn.tools.chain.grammar import ticket_path
    names = {}
    for f in ROOT.glob("**/probes/*.py"):
        src = f.read_text(encoding="utf-8")
        for m in re.finditer(r'owning_ticket\(\s*"([^"]+)"', src):
            names.setdefault(m.group(1), []).append(str(f))
        if "owning_ticket(" in src:
            for m in re.finditer(r'_(?:OWNING_)?TICKET\s*=\s*"([^"]+)"', src):
                names.setdefault(m.group(1), []).append(str(f))
    holes = disagree = hex_holes = 0
    for n in sorted(names):
        o = owning_ticket(n)
        h = o.startswith("{unresolvable")
        holes += h
        t = ticket_path(n)
        if (None if h else o) != t:
            disagree += 1
            print(f"  DIFF {n}: owning={'HOLE' if h else o} ticket_path={t}")
        if h and re.fullmatch(r"[0-9a-f]{12}", n):
            hex_holes += 1
    print(f"  names={len(names)} holes={holes} hex-holes={hex_holes} disagree={disagree}")
    return 0 if names and len(names) >= 84 and disagree == 0 and hex_holes == 0 else 1


def seal():
    from cairn.devices.tester.validation_store import standing
    ok = True
    for p in (G_PROOF, P_PROOF):
        s = standing(p)
        seal = s.get("seal") or {}
        print(f"  {p}: proven={s.get('proven')} verdict={seal.get('verdict')} date={seal.get('date')} caller={seal.get('caller')}")
        ok &= bool(s.get("proven")) and seal.get("verdict") == "green" and "2516e958a6dd" in str(seal.get("caller"))
    out = subprocess.run(["git", "show", "--stat", "--format=", BUILD_COMMIT], cwd=ROOT,
                         capture_output=True, text=True).stdout
    files = [l.split("|")[0].strip() for l in out.strip().splitlines()[:-1]]
    code = sorted(f for f in files if f.endswith(".py"))
    print(f"  .py files in the build commit: {code}")
    ok &= code == sorted(["cairn/tools/base/probe.py", "cairn/tools/chain/grammar.py", G_PROOF, P_PROOF])
    return 0 if ok else 1


if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"grammar": grammar, "probe": probe, "census": census, "seal": seal}.get(sub)
    if fn is None:
        print(__doc__)
        sys.exit(2)
    rc = fn()
    print(f"{sub}: {'PASS' if rc == 0 else 'FAIL'}")
    sys.exit(rc)
