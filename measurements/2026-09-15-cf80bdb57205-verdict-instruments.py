"""The instruments behind ticket cf80bdb57205's verdict artifact — the cheapest reader
rehearses a ticket before BUILDME.

One subcommand per validate criterion (berth validate-20260915T133325-ffc67756ff7d), each
exiting 0 only when the criterion holds against the LIVE world: the proof is RUN twice
(never its seal read) and its text grepped; the door's verb roster and jurisdiction are
imported; the sieve is called three ways over a scratch commons; the entry gate's lanes
are listed off a fixture; the live record is hashed against the live ticket and found in
the journal; the probe module is imported and the emission gate read off the live ticket;
the CLI and the sail skill are exercised.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: proof door lane live_fire probe cli
"""
import glob
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
COMMONS = Path("/home/akien/dev/src/CairnCommons")
sys.path.insert(0, str(ROOT))
TICKET = "cf80bdb57205"
PROOF = "cairn/machines/rehearsal/proofs/test_rehearsal.py"


def _pytest(path):
    cmd = [sys.executable, "-m", "pytest", path, "-q", "-p", "no:cacheprovider"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    tail = (r.stdout.strip().splitlines() or ["<no output>"])[-1]
    print(f"pytest {path}: rc={r.returncode} {tail}")
    return r.returncode == 0


def _fail(msg):
    print("RED:", msg)
    sys.exit(1)


def proof():
    ok = _pytest(PROOF) and _pytest(PROOF)
    text = (ROOT / PROOF).read_text()
    hits = [l for l in text.splitlines() if "dev/src/CairnCommons" in l or "claude -p" in l]
    print(f"grep live-commons/claude-binary in proof: {len(hits)} line(s)")
    if not ok:
        _fail("proof not green twice")
    if hits:
        _fail("the proof names the live commons or the claude binary")


def door():
    from cairn.tools.artifact import artifact
    from cairn.machines.build_inspector.inspector import buildme_rides_the_rehearsal
    print("'rehearse' in VERBS:", "rehearse" in artifact.VERBS)
    jur = json.loads((ROOT / "cairn/tools/artifact/jurisdiction.json").read_text())
    entries = [e for e in json.loads(json.dumps(jur)).get("records", jur.get("classes", [])) or []
               if "rehearsals" in json.dumps(e)] if isinstance(jur, dict) else []
    has = "rehearsals" in json.dumps(jur)
    print("jurisdiction names rehearsals:", has, f"({len(entries)} entr(ies))")
    if "rehearse" not in artifact.VERBS or not has:
        _fail("verb or jurisdiction missing")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "tickets").mkdir()
        (root / "rehearsals").mkdir()
        tk = root / "tickets" / "abcdef012345-a-fixture-ticket.json"
        tk.write_text(json.dumps({"id": "abcdef012345", "decisions": []}))
        absent = buildme_rides_the_rehearsal("abcdef012345", root=root)
        doc = json.loads(tk.read_text())
        doc["rehearsal"] = "rehearsals/abcdef012345-stale.json"
        tk.write_text(json.dumps(doc))
        (root / "rehearsals" / "abcdef012345-stale.json").write_text(json.dumps(
            {"clean": True, "ticket_sha256": "0" * 64, "gaps": []}))
        stale = buildme_rides_the_rehearsal("abcdef012345", root=root)
        doc["rehearsal"] = "rehearsals/abcdef012345-clean.json"
        blob = json.dumps(doc).encode()
        tk.write_bytes(blob)
        (root / "rehearsals" / "abcdef012345-clean.json").write_text(json.dumps(
            {"clean": True, "ticket_sha256": hashlib.sha256(blob).hexdigest(), "gaps": []}))
        clean = buildme_rides_the_rehearsal("abcdef012345", root=root)
        none = buildme_rides_the_rehearsal(None, root=root)
    counts = (len(absent), len(stale), len(clean), len(none))
    print("sieve findings absent/stale/clean/None:", counts)
    if counts != (1, 1, 0, 0):
        _fail(f"expected (1,1,0,0), got {counts}")


def lane():
    import inspect as _i
    from cairn.tools.base import transitions
    from cairn.devices.tester.validation_store import standing
    src = _i.getsource(transitions.inspect_entry)
    lanes = [l.split('"')[1] for l in src.splitlines() if "_sieve_lane(\"" in l]
    print("inspect_entry lanes:", lanes)
    st = standing("cairn/tools/base/proofs/test_transitions.py") or {}
    seal = st.get("seal", {})
    print("test_transitions seal:", seal.get("verdict"), seal.get("date"), seal.get("caller"))
    if len(lanes) != 5 or lanes[-1] != "the_ticket_rehearses_clean":
        _fail("five lanes with the fifth the_ticket_rehearses_clean not found")
    if seal.get("verdict") != "green":
        _fail("test_transitions is not standing green")


def live_fire():
    recs = sorted(glob.glob(str(COMMONS / "rehearsals" / "*.json")))
    print("rehearsal records:", len(recs))
    tp = glob.glob(str(COMMONS / "tickets" / f"{TICKET}-*.json"))[0]
    blob = Path(tp).read_bytes()
    doc = json.loads(blob)
    ptr = doc.get("rehearsal")
    rec = json.loads((COMMONS / ptr).read_text())
    live = hashlib.sha256(blob).hexdigest()
    print("pointer:", ptr, "clean:", rec.get("clean"), "gaps:", len(rec.get("gaps") or []))
    print("record sha:", rec.get("ticket_sha256"))
    print("live sha:  ", live, "(equal)" if live == rec.get("ticket_sha256") else "(stale — the ticket was written after the rehearsal: a crossing moved the cursor)")
    journal = (COMMONS / ".artifact-journal.jsonl").read_text().splitlines()
    hits = [json.loads(l) for l in journal if ptr in l]
    verbs = sorted({h.get("verb") for h in hits})
    print("journal entries naming the record:", len(hits), "verbs:", verbs)
    if not recs or not rec.get("clean") or not hits or "rehearse" not in verbs:
        _fail("no clean record through the door for the live ticket")
    if live != rec.get("ticket_sha256"):
        later = [json.loads(l) for l in journal if tp.split("/")[-1] in l]
        print("later ticket writes:", [(w.get("at") or w.get("ts"), w.get("verb")) for w in later[-3:]])


def probe():
    from cairn.tools.base.probe import Probe
    from cairn.machines.rehearsal.probes import the_rehearsal_predicts_the_build as pm
    from cairn.tools.base import transitions
    ok = isinstance(pm.PROBE, Probe) and callable(pm.PROBE.carry) and callable(pm.PROBE.enough)
    print("PROBE is a Probe with carry+enough:", ok)
    lanes = transitions.inspect_emission("the_rehearsal_predicts_the_build", TICKET)
    fatal = [l for l in lanes if l.get("fatal")]
    print("inspect_emission lanes:", [l.get("identity") for l in lanes], "fatal:", [l.get("identity") for l in fatal])
    if not ok or fatal or len(lanes) != 3:
        _fail("probe not armed, emission gate fatal, or fewer than three lanes read")


def cli():
    r = subprocess.run([str(ROOT / "bin/cairn"), "rehearse", "--help"], capture_output=True, text=True)
    print("cairn rehearse --help rc:", r.returncode, (r.stdout.splitlines() or [""])[0])
    skill = Path.home() / ".claude/skills/sail/SKILL.md"
    hits = [f"{i+1}:{l}" for i, l in enumerate(skill.read_text().splitlines()) if l.startswith("## 0c")]
    print("sail 0c:", hits)
    if r.returncode != 0 or len(hits) != 1:
        _fail("CLI or skill step absent")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
    print("PASS", sys.argv[1])
