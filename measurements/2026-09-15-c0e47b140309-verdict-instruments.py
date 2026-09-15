"""The instruments behind ticket c0e47b140309's verdict artifact — two proofs a ruled change
staled read green again.

One subcommand per validate criterion (berth validate-20260915T120920-f52466e73d98), each
exiting 0 only when the criterion holds against the LIVE world: the proofs are RUN, the diff
is read from git, the seals are read from the validation store, the clear emissions are
listed from the tester's log tree. Berthed in the commons because the verdict door RE-RUNS
what it is handed.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: transitions design diff seal
"""
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
sys.path.insert(0, str(ROOT))
ENV = {**os.environ, "PYTHONPATH": str(ROOT)}
T_PROOF = "cairn/tools/base/proofs/test_transitions.py"
D_PROOF = "skills/design/proofs/test_design_door.py"
BUILD_COMMIT = "20ef088"   # the build's commit, 2026-09-15 12:07 local
LOGS = Path.home() / ".cairn/logs/tester/0"
FOURTH = "the_ticket_has_every_answer_it_needs"


def _run(cmd, timeout=600):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout, env=ENV)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"  {' '.join(cmd[-3:])}: rc={r.returncode} {tail[:120]}")
    return r.returncode, r.stdout


def transitions():
    ok = True
    for _ in (1, 2):
        rc, out = _run([sys.executable, "-m", "pytest", T_PROOF, "-q", "-p", "no:cacheprovider"])
        ok &= rc == 0 and "87 passed" in out
    text = (ROOT / T_PROOF).read_text()
    n = text.count(FOURTH)
    print(f"  {FOURTH} named {n} times in the proof; 'proved 4 check(s)' present: {'proved 4 check(s)' in text}")
    ok &= n >= 2 and "proved 4 check(s)" in text
    ok &= "len(record) == 4 and sum(transitions.gate.passed(e) for e in record) == 3" in text
    ok &= "test_the_entry_gate_names_every_sieve_so_a_dropped_one_shortens_the_record" in text
    ok &= 'assert [f["method"] for f in raised] == ["buildme_rides_the_chart"]' in text
    diff = subprocess.run(["git", "show", "--stat", "--format=", BUILD_COMMIT, "--", T_PROOF],
                          cwd=ROOT, capture_output=True, text=True).stdout
    print("  build diff on the proof:", diff.strip().splitlines()[-1] if diff.strip() else "none")
    ok &= "test_transitions.py" in diff
    return 0 if ok else 1


def design():
    ok = True
    for _ in (1, 2):
        rc, _ = _run([sys.executable, D_PROOF], timeout=300)
        ok &= rc == 0
    text = (ROOT / D_PROOF).read_text()
    field = '"questions": "none, because skills/design/proofs/test_design_door.py is a proof fixture, not a cast"'
    print("  fixture carries the questions field:", field in text)
    ok &= field in text
    diff = subprocess.run(["git", "show", "--stat", "--format=", BUILD_COMMIT, "--", D_PROOF],
                          cwd=ROOT, capture_output=True, text=True).stdout
    print("  build diff on the proof:", diff.strip().splitlines()[-1] if diff.strip() else "none")
    ok &= "1 +" in diff
    return 0 if ok else 1


def diff():
    out = subprocess.run(["git", "show", "--stat", "--format=", BUILD_COMMIT], cwd=ROOT,
                         capture_output=True, text=True).stdout
    files = [l.split("|")[0].strip() for l in out.strip().splitlines()[:-1]]
    code = [f for f in files if f.endswith(".py")]
    print(f"  files in the build commit: {files}")
    print(f"  .py files: {code}")
    ok = sorted(code) == sorted([T_PROOF, D_PROOF])
    rest = [f for f in files if f not in code]
    # the rest is the crossing's record (history/state/journal) and the two reseals
    ok &= all(f.endswith((".json", ".jsonl")) for f in rest)
    return 0 if ok else 1


def seal():
    from cairn.devices.tester.validation_store import standing
    ok = True
    for p in (T_PROOF, D_PROOF):
        s = standing(p)
        seal = s.get("seal") or {}
        print(f"  {p}: proven={s.get('proven')} verdict={seal.get('verdict')} date={seal.get('date')} caller={seal.get('caller')}")
        ok &= bool(s.get("proven")) and seal.get("verdict") == "green" and "c0e47b140309" in str(seal.get("caller"))
    want = {"validation-verdict-changed-test_transitions", "validation-verdict-changed-test_design_door"}
    seen = {}
    for f in sorted(glob.glob(str(LOGS / "20260915.*.tester.clear_trouble.json"))):
        d = json.loads(Path(f).read_text())
        if d.get("pointer") in want and "c0e47b140309" in json.dumps(d.get("values")):
            seen[d["pointer"]] = f.split("/")[-1]
    print(f"  seal-time clears: {seen}")
    ok &= set(seen) == want
    log = subprocess.run(["git", "log", "-1", "--format=%h %s", BUILD_COMMIT], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    print(f"  build commit: {log[:100]}")
    ok &= log.startswith(BUILD_COMMIT)
    ladder = [f for f in glob.glob(str(LOGS / "20260915.18*.tester.clear_trouble.json"))
              if "seal-red" in Path(f).read_text()]
    print(f"  ladder seal-red clears after the seal: {len(ladder)} (measured: the ladder read both seals as reproducing and emitted nothing)")
    ok &= not ladder
    return 0 if ok else 1


if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"transitions": transitions, "design": design, "diff": diff, "seal": seal}.get(sub)
    if fn is None:
        print(__doc__)
        sys.exit(2)
    rc = fn()
    print(f"{sub}: {'PASS' if rc == 0 else 'FAIL'}")
    sys.exit(rc)
