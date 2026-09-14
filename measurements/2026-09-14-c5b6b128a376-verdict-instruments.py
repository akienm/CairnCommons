"""The instruments behind ticket c5b6b128a376's verdict artifact — a proof that binds a
build-added name at import is red at PROVEME, not UNRAN at hollow.

One subcommand per validate criterion (berth validate-20260914T152501-ec8f830b1a0b), each
exiting 0 only when the criterion holds against the LIVE world: the proofs are RUN (never
their seals read) and the named teeth must print green; the sieve is run over the live
corpus and every lack it reports is checked against `git show <pre>:<file>`; the hollow
reading is READ from the sealed evidence the tester landed (a fresh 5-minute run is the
tester's instrument, not this script's — the seal is what PROVED reads); the charters are
read from the artifact door's journal and the compiled lab.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: sieve_proof live_corpus hollow charters sail probe
"""
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
COMMONS = Path("/home/akien/dev/src/CairnCommons")
sys.path.insert(0, str(ROOT))
TICKET = "c5b6b128a376"
PROOF = ROOT / "cairn/tools/proof_coverage/proofs/test_call_time_binding.py"
COVERAGE_PROOF = ROOT / "cairn/tools/proof_coverage/proofs/test_proof_coverage.py"
SAIL_PROOF = ROOT / "skills/sail/proofs/test_sail_pins_its_refusals.py"
PC_CHARTER = "cairn/tools/proof_coverage/intention+why.json"
TESTER_CHARTER = "cairn/devices/tester/intention+why.json"
SIEVE = "proof_binds_its_subject_at_call_time"
_RUNS = {}


def _proof(path, timeout=900):
    """Run a proof once per process; return (rc, teeth green, teeth red, a tail)."""
    if path not in _RUNS:
        from cairn.tools.proof_coverage.proof_coverage import teeth_printed
        r = subprocess.run([sys.executable, str(path)], cwd=ROOT, capture_output=True, text=True,
                           timeout=timeout, env=dict(os.environ, PYTHONPATH=str(ROOT)))
        printed = teeth_printed(r.stdout)
        _RUNS[path] = (r.returncode, set(printed["green"]), set(printed["red"]),
                       r.stdout[-2500:] + r.stderr[-1500:])
    return _RUNS[path]


def _teeth(path, *names):
    rc, green, red, tail = _proof(path)
    missing = [n for n in names if n not in green]
    print(f"{path.relative_to(ROOT)}: rc={rc}, {len(green)} green, {len(red)} red")
    for n in names:
        print("  ", "green" if n in green else "MISSING", n)
    assert rc == 0, f"{path} exited {rc}:\n{tail}"
    assert not missing, f"teeth not seen green: {missing}"


def _ticket():
    return json.loads(next(COMMONS.glob("tickets/" + TICKET + "-*.json")).read_text())


def sieve_proof():
    """(1) the sieve's proof runs green twice with the five clause teeth; lacks() over the ticket is []."""
    from cairn.tools.proof_coverage import proof_coverage as pcm
    declared = pcm.declared(PROOF)[TICKET]
    assert set(declared) == {"1", "2", "3", "4", "5"}, declared
    _teeth(PROOF, *declared.values())
    first = _proof(PROOF)[1]
    _RUNS.pop(PROOF)
    _teeth(PROOF, *declared.values())
    assert _proof(PROOF)[1] == first, "the two runs printed different green sets"
    print("run twice: identical green sets")
    # the criterion names `python3 -m cairn.tools.proof_coverage <id>`; that CLI does not exist
    # (no __main__ in the package) — the same question is asked of lacks() directly.
    found = pcm.lacks(_ticket(), repo_root=ROOT)
    print("proof_coverage.lacks over the ticket:", json.dumps(found, indent=1)[:1500])
    assert found == [], "the ticket is not covered"


def live_corpus():
    """(2) the sieve over every ticket with a crossing: each lack is a module-level import on every hop,
    of a file or name truly absent at the pre-build commit — never a false positive."""
    from cairn.tools.base.crossings import buildme_crossing
    from cairn.tools.proof_coverage import proof_coverage as pcm
    sieve = getattr(pcm, SIEVE)
    tickets, lacks_by, checked = pcm.load_tickets(COMMONS), {}, 0
    for t in tickets:
        cr = buildme_crossing(t["id"])
        if not cr:
            continue
        checked += 1
        found = sieve(t, repo_root=ROOT)
        if not found:
            continue
        pre = pcm._prebuild_commit(cr["at"], repo_root=ROOT)
        for lack in found:
            v = lack["values"]
            for hop in v["chain"]:
                rel, line = hop.rsplit(":", 1)
                stmts = [n for n in ast.parse((ROOT / rel).read_text()).body
                         if isinstance(n, (ast.Import, ast.ImportFrom)) and n.lineno == int(line)]
                assert stmts, (t["id"], hop)
            if "file" in v:
                assert pcm._git(ROOT, "show", f"{pre}:{v['file']}") is None, (t["id"], v["file"], pre)
            else:
                shown = pcm._git(ROOT, "show", f"{pre}:{v['in']}")
                assert shown is not None and v["name"] not in pcm._top_level_names(shown), (t["id"], v)
            lacks_by.setdefault(t["id"], []).append(f"{v['proof']} -> {' -> '.join(v['chain'])}")
    print(f"tickets with a BUILDME crossing: {checked}; tickets with binding lacks: {len(lacks_by)}; "
          f"lacks: {sum(len(v) for v in lacks_by.values())}, every one anchored on module-level imports "
          f"of something absent at pre (checked by git show)")
    for tid, rows in sorted(lacks_by.items()):
        print(" ", tid, "\n    " + "\n    ".join(rows))
    assert TICKET not in lacks_by, "this ticket's own proofs bind an added name at import"


def hollow():
    """(3) the sealed hollow reading over this ticket: every writes_to file measured, 0 hollow, 0 UNRAN."""
    from cairn.devices.tester import hollow as H
    from cairn.tools.base.crossings import proven_by_since_buildme
    writes = H.writes_to(_ticket())
    proofs = proven_by_since_buildme(TICKET)
    print("proofs since BUILDME:", proofs)
    readings = {}
    for rel in proofs:
        vpath = ROOT / rel
        vpath = vpath.parent.parent / "validations" / (vpath.stem + ".json")
        docs = json.loads(vpath.read_text())
        rec = docs[-1] if isinstance(docs, list) else docs
        ev = rec.get("evidence") or {}
        assert rec.get("verdict") == "green", (rel, rec.get("verdict"))
        reading = (ev.get("hollow") or {}).get(TICKET)
        if reading:
            readings[rel] = reading
    assert readings, "no proof carries a sealed hollow reading for this ticket"
    unran, hollow_files, measured = [], [], set()
    for rel, reading in readings.items():
        for f, val in reading.items():
            measured.add(f)
            if isinstance(val, dict) and "unreadable" in val:
                unran.append((rel, f, val))
            elif val == [] or val == "hollow" or (isinstance(val, dict) and val.get("hollow")):
                hollow_files.append((rel, f, val))  # the sealed shape: {file: [teeth redded]}; [] is hollow
    print(f"measured files: {len(measured)}; hollow: {len(hollow_files)}; UNRAN: {len(unran)}")
    for f in sorted(measured):
        print("  ", f, {rel: reading[f] for rel, reading in readings.items() if f in reading})
    assert not unran and not hollow_files, (unran, hollow_files)
    if writes:
        py = [w for w in writes if w.endswith(".py") and "/proofs/" not in w and "/probes/" not in w]
        missing = [w for w in py if w not in measured]
        print("writes_to .py files hollow reverts:", py, "not measured:", missing)
        assert not missing, missing


def charters():
    """(4) both charters name the sieve, written through the door with verb charter; the lab copies carry it."""
    for rel in (PC_CHARTER, TESTER_CHARTER):
        doc = json.loads((ROOT / rel).read_text())
        text = json.dumps(doc)
        assert SIEVE in text, rel
        edges = "\n".join(doc["filed_edges"])
        assert SIEVE in edges and ("importlib" in edges or "front door" in edges.lower()), rel
        entries = [json.loads(l) for l in (ROOT / ".artifact-journal.jsonl").read_text().splitlines() if l.strip()]
        mine = [e for e in entries if e.get("path", "").endswith(rel) and e.get("verb") == "charter"
                and TICKET in json.dumps(e)]
        print(f"{rel}: charter-verb journal entries naming {TICKET}: {len(mine)}; sieve in filed_edges: yes")
        assert mine, f"no charter-verb journal entry for {rel}"
    lab = COMMONS / "intentions-congruency-lab"
    hits = subprocess.run(["grep", "-rl", SIEVE, str(lab)], capture_output=True, text=True).stdout.split()
    names = [Path(h).name for h in hits]
    print("lab copies naming the sieve:", names)
    assert any("proof_coverage" in n for n in names) and any("tester" in n for n in names), names


def sail():
    """(5) /sail step 3 carries the sentence; skills/sail's proof reads it and runs green; the skill link resolves."""
    skill = (ROOT / "skills/sail/SKILL.md").read_text()
    step3 = skill.split("## 3. Prove")[1].split("\n## ")[0]
    assert "at call time" in step3 and SIEVE in step3, step3
    print("step 3 names the rule and the sieve")
    _teeth(SAIL_PROOF, "test_step_3_names_the_call_time_binding_rule", "test_the_named_sieve_resolves")
    link = os.path.realpath(os.path.expanduser("~/.claude/skills/sail"))
    print("~/.claude/skills/sail ->", link)
    assert link == str(ROOT / "skills/sail"), link


def probe():
    """(6) the WATCHME probe loads, is frozen with carry and enough, measures live instance-space; the
    WATCHME crossing stands in the journal."""
    import importlib
    mod = importlib.import_module("cairn.tools.proof_coverage.probes.sieve_predicts_unran")
    p = mod.PROBE
    assert callable(p.carry) and callable(p.enough) and p.to == "harbor_master"
    try:
        p.why = "x"
        raise AssertionError("PROBE is not frozen")
    except (AttributeError, TypeError):
        pass
    carried = p.carry({})
    print(json.dumps(carried, indent=1)[:1200])
    assert "finding" in carried and isinstance(carried["unpredicted"], list)
    _teeth(PROOF, "test_the_watchme_probe_is_armed_with_carry_and_enough")
    hist = json.loads((ROOT / "cairn/tools/proof_coverage/history.json").read_text())
    entries = hist["entries"] if isinstance(hist, dict) else hist
    mine = [e for e in entries if e.get("ticket") == TICKET]
    targets = [str(e.get("to") or e.get("target") or "") for e in mine]
    print("crossings for the ticket:", targets)
    assert any("WATCHME" in t.upper() for t in targets), "no WATCHME crossing journaled yet"


if __name__ == "__main__":
    globals()[sys.argv[1]]()
    print("OK", sys.argv[1])
