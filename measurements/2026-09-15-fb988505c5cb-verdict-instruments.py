"""The instruments behind ticket fb988505c5cb's verdict artifact — measurement drains the
review lane.

One subcommand per validate criterion (berth validate-20260915T105708-6bc98b60e90f), each
exiting 0 only when the criterion holds against the LIVE world: the proofs are RUN (never
their seals read) and the named teeth must print green; the troubles corpus is censused;
the emission gate is READ off the live ticket and the berthed probe; the charter and its
journal entry are read from the artifact door; the lane is diffed live against its own
full census.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: proof renderers probe charter live_fire
"""
import glob
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
COMMONS = Path("/home/akien/dev/src/CairnCommons")
sys.path.insert(0, str(ROOT))
TICKET = "fb988505c5cb"
SB_PROOF = "cairn/machines/skill_block/proofs/test_review_lane_drains_by_measurement.py"
INBOX_PROOF = "cairn/tools/operator_inbox/proofs/test_operator_inbox.py"
SLATE_PROOF = "bin/proofs/test_slate.py"
CHARTER = "cairn/tools/operator_inbox/intention+why.json"
LAB = COMMONS / "intentions-congruency-lab" / "cairn-tools-operator_inbox--intention+why.json"
PRE_BUILD_LANE = 64   # pending_reviews() at HEAD ceb3578 before the predicate, measured 2026-09-15
NAMED = {"bc7b64626405", "c5b6b128a376", "9adc6fddf185"}


def _pytest(path, k=None):
    cmd = [sys.executable, "-m", "pytest", path, "-q", "-p", "no:cacheprovider"]
    if k:
        cmd += ["-k", k]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=600,
                       env={**__import__("os").environ, "PYTHONPATH": str(ROOT)})
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    print(f"  {path}{' -k ' + k if k else ''}: rc={r.returncode} {tail}")
    return r.returncode, tail


def _sealed(validation_path):
    v = json.loads(Path(validation_path).read_text())[-1]
    seal = (v.get("evidence") or {}).get("seal") or {}
    return v.get("verdict"), seal.get("verdict")


def proof():
    ok = True
    for i in (1, 2):
        rc, tail = _pytest(SB_PROOF)
        ok &= rc == 0 and "16 passed" in tail
    for k in ("map", "any_terminal", "drain", "reviewed", "terminal_vocabulary", "idea"):
        rc, tail = _pytest(SB_PROOF, k)
        ok &= rc == 0 and "passed" in tail
    verdict, seal = _sealed(ROOT / "cairn/machines/skill_block/validations/test_review_lane_drains_by_measurement.json")
    print(f"  standing validation: verdict={verdict} seal={seal}")
    ok &= verdict == "green" and seal == "sealed"
    text = (ROOT / SB_PROOF).read_text()
    ok &= "ideas/<id>.json" in text and "TERMINAL_STATES" in text
    ok &= "/home/akien/dev/src/CairnCommons" not in text
    print("  proof names the idea-file join and TERMINAL_STATES; no live-commons path in the proof:", ok)
    return 0 if ok else 1


def renderers():
    ok = True
    rc, tail = _pytest(INBOX_PROOF)
    ok &= rc == 0 and " passed" in tail and "failed" not in tail
    rc, tail = _pytest(INBOX_PROOF, "trouble or section_order")
    ok &= rc == 0
    r = subprocess.run([sys.executable, str(ROOT / SLATE_PROOF)], cwd=ROOT, capture_output=True,
                       text=True, timeout=600, env={**__import__("os").environ, "PYTHONPATH": str(ROOT)})
    print(f"  {SLATE_PROOF}: rc={r.returncode}")
    ok &= r.returncode == 0
    files = sorted(glob.glob(str(COMMONS / "troubles" / "*.json")))
    withq = []
    for f in files:
        try:
            d = json.loads(Path(f).read_text())
        except Exception:
            continue
        if isinstance(d, dict) and ("question" in d or "questions" in d):
            withq.append(f)
    print(f"  troubles census: {len(files)} records, {len(withq)} with a question key")
    ok &= len(files) > 0 and not withq
    return 0 if ok else 1


def probe():
    ok = True
    rc, tail = _pytest(INBOX_PROOF, "probe")
    ok &= rc == 0 and "1 passed" in tail
    from cairn.tools.operator_inbox.probes import the_lane_holds_only_his_decisions as m
    armed = callable(m.PROBE.trigger) and callable(m.PROBE.carry) and callable(m.PROBE.enough)
    owner = m.owning_ticket(m._OWNING_TICKET)
    print(f"  PROBE armed={armed} to={m.PROBE.to} owning_ticket={str(owner)[:80]}")
    ok &= armed and TICKET in str(owner)
    from cairn.tools.base.transitions import inspect_emission
    rec = inspect_emission("the_lane_holds_only_his_decisions", TICKET)
    fatal = [l["identity"] for l in rec if l.get("fatality") not in (None, "none")]
    print(f"  emission gate lanes: {[l['identity'] for l in rec]} fatal={fatal}")
    ok &= bool(rec) and not fatal
    return 0 if ok else 1


def charter():
    ok = True
    doc = json.loads((ROOT / CHARTER).read_text())
    fals = doc.get("falsifier", "")
    print(f"  falsifier present: {bool(fals)}; names the drain: {'terminal' in fals and 'pending_reviews' in fals}")
    ok &= bool(fals) and "pending_reviews" in fals and "the_lane_holds_only_his_decisions" in fals
    entries = [json.loads(l) for l in (ROOT / ".artifact-journal.jsonl").read_text().splitlines() if l.strip()]
    hits = [e for e in entries if e.get("path") == CHARTER and e.get("verb") == "charter"
            and TICKET in str(e.get("why", ""))]
    print(f"  journal entries (verb charter, this ticket): {len(hits)}; last at {hits[-1]['at'] if hits else None}")
    ok &= bool(hits)
    same = LAB.exists() and json.loads(LAB.read_text()) == doc
    print(f"  congruency-lab copy matches charter: {same}")
    ok &= same
    return 0 if ok else 1


def live_fire():
    from cairn.machines.skill_block.skill_block import berth_ticket_cursors, pending_reviews
    from cairn.tools.base.transitions import is_terminal
    full = pending_reviews(drain=False)
    lane = pending_reviews()
    lane_ids = {r["berth_id"] for r in lane}
    cursors = berth_ticket_cursors()
    tmap = {}
    for tf in glob.glob(str(COMMONS / "tickets" / "*.json")):
        try:
            t = json.loads(Path(tf).read_text())
        except Exception:
            continue
        if not isinstance(t, dict):
            continue
        for k in ("intent_berth", "sorted_berth"):
            v = t.get(k)
            if isinstance(v, str) and v.startswith("/"):
                tmap.setdefault(str(Path(v).resolve()), set()).add(t.get("id"))
        fi = t.get("from_idea")
        if isinstance(fi, str) and fi and not fi.startswith("/"):
            ip = COMMONS / "ideas" / f"{fi}.json"
            try:
                b = json.loads(ip.read_text()).get("berth")
                if isinstance(b, str) and b.startswith("/"):
                    tmap.setdefault(str(Path(b).resolve()), set()).add(t.get("id"))
            except Exception:
                pass
    drained = [r for r in full if r["berth_id"] not in lane_ids]
    under_named = 0
    for r in drained:
        key = str(Path(r["path"]).resolve())
        tids = tmap.get(key, set())
        if tids & NAMED:
            under_named += 1
        print(f"  drained [{r['skill']}] {r['berth_id']} tickets={sorted(tids)} cursors={cursors.get(key)}")
    bad = [r for r in lane if any(is_terminal(s) for s in cursors.get(str(Path(r['path']).resolve()), []))]
    banner = subprocess.run([str(ROOT / "bin/cmd/slate")], capture_output=True, text=True, timeout=300)
    line = next((l for l in banner.stdout.splitlines() if "ARTIFACTS AWAITING REVIEW" in l), "")
    print(f"  census={len(full)} lane={len(lane)} drained={len(drained)} under the three named tickets={under_named}")
    print(f"  banner: {line.strip()}")
    print(f"  lane berths with a terminal ticket: {len(bad)}")
    ok = (len(lane) <= PRE_BUILD_LANE - under_named and under_named >= 8 and not bad
          and f"{len(lane)} artifact(s)" in line and all(is_terminal(s) for r in drained
                                                          for s in [max(cursors.get(str(Path(r['path']).resolve()), []), key=is_terminal)]))
    return 0 if ok else 1


if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"proof": proof, "renderers": renderers, "probe": probe, "charter": charter,
          "live_fire": live_fire}.get(sub)
    if fn is None:
        print(__doc__)
        sys.exit(2)
    rc = fn()
    print(f"{sub}: {'PASS' if rc == 0 else 'FAIL'}")
    sys.exit(rc)
