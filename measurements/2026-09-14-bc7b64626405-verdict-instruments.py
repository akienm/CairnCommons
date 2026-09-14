"""The instruments behind ticket bc7b64626405's verdict artifact — a question and its ticket
name each other, and an answer names what it spawned.

One subcommand per validate criterion (berth validate-20260914T163741-6c5d55f60223), each
exiting 0 only when the criterion holds against the LIVE world: the proofs are RUN (never
their seals read) and the named teeth must print green; the sieve is run over the live
commons; the hollow reading is READ from the sealed evidence the tester landed (the
5-minute run is the tester's instrument — the seal is what PROVED reads); the charter and
the ticket are read from the artifact door's journal; the CLI is fired against the live
store and the ticket file read back.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: proofs coverage_hollow live_corpus cli_and_wording renderer probe sorted charter live_fire
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
COMMONS = Path("/home/akien/dev/src/CairnCommons")
sys.path.insert(0, str(ROOT))
TICKET = "bc7b64626405"
LINKS = ROOT / "cairn/tools/question/proofs/test_question_links.py"
STANDING = ROOT / "cairn/tools/question/proofs/test_question.py"
CHARTER = "cairn/tools/question/intention+why.json"
CAIRN = ROOT / "bin" / "cairn"
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


def _ticket_path():
    return next(COMMONS.glob("tickets/" + TICKET + "-*.json"))


def _ticket():
    return json.loads(_ticket_path().read_text())


def _sh(*args, env=None, timeout=300):
    return subprocess.run([str(a) for a in args], cwd=ROOT, capture_output=True, text=True,
                          timeout=timeout, env=dict(os.environ, PYTHONPATH=str(ROOT), **(env or {})))


def _journal(path_suffix):
    from cairn.tools.artifact import artifact as door
    root = ROOT if path_suffix.startswith("cairn/") or path_suffix.startswith("skills/") else COMMONS
    return [e for e in door.read_journal(root) if (e.get("path") or "").endswith(path_suffix)]


def proofs():
    """(1) the links proof runs green twice with a PROVES block for the ticket covering clauses 1-5 + cli +
    probe; the standing 9adc proof runs green re-worded to spawned."""
    from cairn.tools.proof_coverage import proof_coverage as pcm
    declared = pcm.declared(LINKS)[TICKET]
    assert {"1", "2", "3", "4", "5", "cli", "probe"} <= set(declared), declared
    _teeth(LINKS, *declared.values())
    first = _proof(LINKS)[1]
    _RUNS.pop(LINKS)
    _teeth(LINKS, *declared.values())
    assert _proof(LINKS)[1] == first, "the two runs printed different green sets"
    print("links proof run twice: identical green sets")
    lent = pcm.declared(STANDING)[TICKET]
    _teeth(STANDING, *lent.values())
    src = STANDING.read_text()
    assert "spawned=" in src and "--spawned" in src and "follow_ups=" not in src and "--follow-up" not in src
    print("standing proof says spawned=/--spawned and no longer follow_ups=/--follow-up")
    for p in (LINKS, STANDING):
        v = p.parent.parent / "validations" / (p.stem + ".json")
        docs = json.loads(v.read_text())
        rec = docs[-1]
        assert rec.get("verdict") == "green", (p.name, rec.get("verdict"))
        print(f"  standing seal for {p.name}: green, isolation={rec.get('isolation')}, at={rec.get('at')}")


def coverage_hollow():
    """(2) proof_coverage.lacks over the ticket == [] and the sealed hollow reading measured every written
    file: 0 hollow, 0 UNRAN. (The criterion names `python3 -m cairn.tools.proof_coverage`; that CLI does
    not exist — lacks() is asked directly.)"""
    from cairn.tools.proof_coverage import proof_coverage as pcm
    from cairn.tools.base.crossings import proven_by_since_buildme
    t = _ticket()
    found = pcm.lacks(t, repo_root=ROOT)
    print("proof_coverage.lacks over the ticket:", json.dumps(found, indent=1)[:1500])
    assert found == [], "the ticket is not covered"
    writes = [w for w in pcm._writes_to(t) if "/proofs/" not in w]
    proofs_named = proven_by_since_buildme(TICKET)
    print("proofs since BUILDME:", proofs_named)
    readings = {}
    for rel in proofs_named:
        vpath = ROOT / rel
        vpath = vpath.parent.parent / "validations" / (vpath.stem + ".json")
        rec = json.loads(vpath.read_text())[-1]
        assert rec.get("verdict") == "green", (rel, rec.get("verdict"))
        reading = ((rec.get("evidence") or {}).get("hollow") or {}).get(TICKET)
        if reading:
            readings[rel] = reading
    assert readings, "no proof carries a sealed hollow reading for this ticket"
    unran, hollow_files, measured = [], [], set()
    for rel, reading in readings.items():
        for f, val in reading.items():
            measured.add(f)
            if isinstance(val, dict) and "unreadable" in val:
                unran.append((rel, f, val))
            elif not (isinstance(val, list) and val):
                hollow_files.append((rel, f, val))
    print(f"writes_to (non-proof): {len(writes)}; measured: {len(measured)}; hollow: {len(hollow_files)}; "
          f"UNRAN: {len(unran)}")
    for f in sorted(measured):
        print("  ", f, {rel: reading[f] for rel, reading in readings.items() if f in reading})
    unmeasured = [w for w in writes if w not in measured]
    assert not unmeasured, f"written files without a hollow reading: {unmeasured}"
    assert not unran and not hollow_files, (unran, hollow_files)


def live_corpus():
    """(3) the sieve over the live commons returns [] and the inspector over the component reports no
    finding beyond working-tree dirtiness."""
    from cairn.machines.build_inspector import inspector as I
    assert I.SIEVES.get("question_links_agree") is I.question_links_agree, "the sieve is not registered"
    found = I.question_links_agree({"component": "question"}, ROOT / "cairn/tools/question", commons=COMMONS)
    print("question_links_agree over the live commons:", found)
    assert found == [], "the live corpus disagrees at the ends"
    r = _sh(sys.executable, ROOT / "cairn/machines/build_inspector/inspector.py", "question", timeout=900)
    text = r.stdout
    rep = json.loads(text[text.find("{"):])
    findings = rep.get("findings") or []
    kinds = sorted({f.get("method") for f in findings})
    print(f"inspector over question: rc={r.returncode} clean={rep.get('clean')} methods={kinds}")
    assert not [f for f in findings if f.get("method") not in ("history_integrity", "working_tree_clean")], findings


def cli_and_wording():
    """(4) answer without --spawned exits 2; `--spawned none` records []; no --follow-up wording survives
    on the surfaces the ticket wrote (the librarian's own follow-up questions are another word)."""
    import tempfile
    with tempfile.TemporaryDirectory(prefix="bc7b-cli-") as tmp:
        commons = Path(tmp) / "CairnCommons"
        (commons / "questions").mkdir(parents=True)
        (commons / "tickets").mkdir()
        (Path(tmp) / "cairn").mkdir()
        env = {"CAIRN_QUESTIONS_DIR": str(commons / "questions"),
               "CAIRN_ARTIFACT_ROOTS": json.dumps({"CairnCommons": str(commons), "cairn": str(Path(tmp) / "cairn")})}
        r = _sh(CAIRN, "question", "open", "--ticket", "0badc0ffee00", "does the cli refuse a silent answer?",
                "--why", "criterion 4", env=env)
        qid = next(tok for tok in r.stdout.split() if tok.startswith("open-"))
        bad = _sh(CAIRN, "question", "answer", qid, "x", env=env)
        print(f"answer without --spawned: rc={bad.returncode} stderr={bad.stderr.strip()[-160:]}")
        assert bad.returncode == 2 and "spawned" in bad.stderr
        ok = _sh(CAIRN, "question", "answer", qid, "x", "--spawned", "none", env=env)
        rec = json.loads((commons / "questions" / (qid + ".json")).read_text())
        print(f"answer --spawned none: rc={ok.returncode} record spawned={rec.get('spawned')!r}")
        assert ok.returncode == 0 and rec.get("spawned") == [] and rec.get("resolved") is True
    word = re.compile(r"follow[-_]ups?\b", re.IGNORECASE)
    surfaces = [ROOT / "cairn/tools/question", ROOT / "skills/sorted", ROOT / "skills/ruled",
                ROOT / "cairn/machines/ruling/cli.py", ROOT / "cairn/tools/operator_inbox/inbox.py",
                ROOT / "cairn/machines/build_inspector/inspector.py", ROOT / "bin/cmd/question"]
    tellers = []
    for base in surfaces:
        for p in (sorted(base.rglob("*")) if base.is_dir() else [base]):
            if not p.is_file() or "/proofs/" in str(p) or "/validations/" in str(p) \
                    or p.name in ("history.json", "state.json") or p.suffix not in (".py", ".md", ".sh", ".json", ""):
                continue
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if word.search(line) and "pre-build" not in line and "pre-2026-09-14" not in line:
                    tellers.append(f"{p.relative_to(ROOT)}:{n}")
    flag = _sh("grep", "-rn", "--", "--follow-up", "cairn", "skills", "bin")
    lines = flag.stdout.splitlines()
    outside_proofs = [ln for ln in lines if "/proofs/" not in ln]
    print(f"'--follow-up' anywhere in cairn/skills/bin: {len(lines)} line(s), {len(outside_proofs)} outside "
          f"proofs/ (a proof asserting the words are GONE names them); follow-up in any form on the ticket's "
          f"surfaces (pre-build readers allowed): {tellers}")
    for ln in lines:
        print("  ", ln[:160])
    assert not outside_proofs and not tellers


def renderer():
    """(5) `cairn operator show artifact <ticket>` prints one QUESTIONS section; `cairn question list <ticket>`
    prints the tree."""
    r = _sh(CAIRN, "operator", "show", "artifact", TICKET)
    sections = [ln for ln in r.stdout.splitlines() if ln.startswith("QUESTIONS")]
    print(f"operator show artifact: rc={r.returncode} QUESTIONS sections={len(sections)}")
    assert r.returncode == 0 and len(sections) == 1, r.stderr[-300:]
    lst = _sh(CAIRN, "question", "list", TICKET)
    ids = [ln for ln in lst.stdout.splitlines() if "open-" in ln]
    print(f"question list: rc={lst.returncode}\n" + lst.stdout.strip()[:800])
    assert lst.returncode == 0 and ids, lst.stderr[-300:]
    from cairn.tools.question import question as Q
    linked = Q.links_of(_ticket())
    assert all(any(i in ln for ln in ids) for i in linked), (linked, ids)


def probe():
    """(6) the WATCHME probe is armed at the berth the ticket names, frozen with carry and enough, measures
    the live corpus, and the WATCHME crossing stands on the record."""
    from cairn.tools.question.probes import both_ends_agree as P
    from cairn.tools.base.probe import Probe
    assert isinstance(P.PROBE, Probe) and callable(P.PROBE.carry) and callable(P.PROBE.enough)
    assert P.PROBE.to == "harbor_master"
    ctx = P._carry({})
    print("carry over the live corpus:", json.dumps({k: v for k, v in ctx.items() if k != "lacks"})[:600])
    assert ctx["wrong_intent"] == [] and ctx["lacks"] == []
    t = _ticket()
    spec = ((t.get("watchme") or {}) if isinstance(t.get("watchme"), dict) else {})
    berth = spec.get("probe", "")
    print("ticket's probe berth:", berth)
    assert berth and Path(berth).resolve() == Path(P.__file__).resolve(), (berth, P.__file__)
    hist = json.loads((ROOT / "cairn/tools/question/history.json").read_text())
    entries = hist if isinstance(hist, list) else hist.get("entries") or hist.get("crossings") or []
    text = json.dumps(entries)
    assert "WATCHME" in text and TICKET in text, "no WATCHME crossing for the ticket on the record"
    wf = t["workflow_and_state"]
    print("workflow:", wf)
    # the crossing INTO WATCHME leaves the cursor sitting on it (":waiting") until PROVED crosses;
    # the emission gate fired on the way in — the record above is the evidence, the cursor confirms it landed
    assert "[WATCHME(" in wf or "PROVED]" in wf, wf


def sorted_skill():
    """(7) /sorted step 5 names `cairn question rebind <id>` and says --spawned; rebind is a live verb."""
    text = (ROOT / "skills/sorted/SKILL.md").read_text()
    n_rebind = text.count("question rebind")
    n_flag = text.count("--follow-up")
    print(f"skills/sorted/SKILL.md: 'question rebind' x{n_rebind}, '--follow-up' x{n_flag}, "
          f"'--spawned' x{text.count('--spawned')}")
    assert n_rebind >= 1 and n_flag == 0 and "--spawned" in text
    assert Path(os.path.realpath(Path.home() / ".claude/skills/sorted")) == ROOT / "skills/sorted"
    r = _sh(CAIRN, "question", "rebind", TICKET)
    print(f"cairn question rebind {TICKET}: rc={r.returncode} out={r.stdout.strip()[-200:]}")
    assert r.returncode == 0


def charter():
    """(8) the charter names the sieve, the probe, the proof and --spawned, closes edges (a) and (c), was
    written with verb charter, and the recompile gate exits 0."""
    doc = json.loads((ROOT / CHARTER).read_text())
    blob = json.dumps(doc)
    for needle in ("question_links_agree", "both_ends_agree.py", "test_question_links.py", "--spawned", "rebind", TICKET):
        assert needle in blob, needle
    assert "--follow-up" not in blob
    edges = doc["filed_edges"]
    assert edges[0].startswith("(a)") and "CLOSED" in edges[0] and TICKET in edges[0]
    assert edges[2].startswith("(c)") and "CLOSED" in edges[2] and TICKET in edges[2]
    entries = [e for e in _journal(CHARTER) if e.get("verb") == "charter" and TICKET in (e.get("why") or "")]
    print(f"charter-verb journal entries naming the ticket: {len(entries)}; edges (a) and (c) CLOSED")
    assert entries
    r = _sh(ROOT / "cairn/tools/intentions_model_compiler/recompile_gate.sh", timeout=600)
    print(f"recompile_gate.sh rc={r.returncode}")
    assert r.returncode == 0
    lab = COMMONS / "intentions-congruency-lab" / "cairn-tools-question--intention+why.json"
    assert "question_links_agree" in lab.read_text()


def live_fire():
    """(9) the ticket's own live fire wrote both ends: the ticket lists an id whose record names the ticket,
    and the journal shows the cast entry for the ticket path beside the question entry."""
    from cairn.tools.question import question as Q
    t = _ticket()
    linked = Q.links_of(t)
    print("ticket questions:", linked)
    assert linked, "the ticket lists no question"
    for qid in linked:
        rec = Q.read(qid)
        assert rec["ticket"] == TICKET, (qid, rec["ticket"])
        assert "spawned" in rec or not rec.get("resolved"), qid
    casts = [e for e in _journal(_ticket_path().name) if e.get("verb") == "cast" and "opened" in (e.get("why") or "")]
    print(f"cast entries on the ticket path for an opened question: {len(casts)}; "
          f"e.g. {casts[-1]['why'][:120] if casts else None}")
    assert casts
    resolved = [Q.read(q) for q in linked if Q.read(q).get("resolved")]
    print(f"resolved: {len(resolved)}; spawned claims: {[r.get('spawned') for r in resolved]}")
    assert all(isinstance(r.get("spawned"), list) for r in resolved)


SUBS = {"proofs": proofs, "coverage_hollow": coverage_hollow, "live_corpus": live_corpus,
        "cli_and_wording": cli_and_wording, "renderer": renderer, "probe": probe, "sorted": sorted_skill,
        "charter": charter, "live_fire": live_fire}

if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else ""
    if sub not in SUBS:
        print(__doc__)
        raise SystemExit(2)
    SUBS[sub]()
    print("OK", sub)
