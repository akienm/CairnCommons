"""The instruments behind ticket 9adc6fddf185's verdict artifact — a decision is a question.

One subcommand per validate criterion (berth validate-20260914T115829-16ad465de31e), each
exiting 0 only when the criterion holds against the LIVE world: the proofs are RUN (never
their seals read) and the named teeth must print green; the hollow reading is taken fresh
(no seal); the retirement is read from the live CLI, the live Stop hooks, and the live
skill text; the sorted contract is read from the seam's own `contract` verb.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: door_inbox answer_cli lane_hollow retirement sieves intake
"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
COMMONS = Path("/home/akien/dev/src/CairnCommons")
sys.path.insert(0, str(ROOT))
TICKET = "9adc6fddf185"
Q_PROOF = ROOT / "cairn/tools/question/proofs/test_question.py"
RULING_PROOF = ROOT / "cairn/machines/ruling/proofs/test_ruling.py"
EXEMPT_PROOF = ROOT / "cairn/machines/exemptions/proofs/test_exemption_set.py"
SORTED_PROOF = ROOT / "skills/sorted/proofs/test_sorted_door.py"
_RUNS = {}


def _proof(path, timeout=900):
    """Run a proof once per process; return (rc, the teeth that printed green, a tail)."""
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


def _cairn(*args, timeout=600, env=None):
    r = subprocess.run([str(ROOT / "bin/cairn"), *args], cwd=ROOT, capture_output=True, text=True,
                       timeout=timeout, env=env)
    print(f"$ cairn {' '.join(args)} -> {r.returncode}: {(r.stdout + r.stderr).strip()[-400:]}")
    return r


def door_inbox():
    """(1) open rides the artifact door with verb question; the inbox lists it under its ticket."""
    _teeth(Q_PROOF, "test_a_question_opens_through_the_door_and_the_inbox_lists_it_under_its_ticket")
    # the door's verify verb takes the ROOT NAME, not a path (cairn/tools/artifact/__main__.py).
    r = _cairn("artifact", "verify", "CairnCommons")
    assert r.returncode == 0, "the live CairnCommons journal does not verify"
    # the live lane: this ticket's own four questions stand in the store, answered, and every
    # one of them was written through the door (its path is in the journal). They predate the
    # question/answer verbs — they were opened with verb write before this build existed — so the
    # verb itself is measured by the proof's scratch world, not by demanding a fixture question
    # be pushed into the live store.
    from cairn.tools.question import question as Q
    tk = json.loads(next(COMMONS.glob("tickets/" + TICKET + "-*.json")).read_text())
    journal = (COMMONS / ".artifact-journal.jsonl").read_text(encoding="utf-8")
    for qid in tk["questions"]:
        rec = Q.read(qid)
        print(f"  {qid}: resolved={rec.get('resolved')} journaled={qid in journal} answered_by={rec.get('answered_by')}")
        assert rec.get("resolved") and qid in journal, qid


def answer_cli():
    """(2) an answer resolves verbatim, a follow-up is born_of it, a second answer is refused; the CLI is the same door."""
    _teeth(Q_PROOF, "test_an_answer_resolves_it_and_a_follow_up_is_born_of_it",
           "test_the_cli_opens_answers_and_lists")
    r = _cairn("question", "list")
    assert r.returncode == 0


def lane_hollow():
    """(3) the BUILDME lane refuses an open question and passes once answered; the hollow reading is 0."""
    _teeth(Q_PROOF, "test_a_ticket_with_an_open_question_is_refused_at_buildme_and_crosses_once_answered")
    r = subprocess.run([str(ROOT / "bin/cairn"), "test", "--hollow", TICKET, "--timeout", "300"],
                       cwd=ROOT, capture_output=True, text=True, timeout=3000)
    sys.stdout.write(r.stdout[-3000:]); sys.stderr.write(r.stderr[-1500:])
    assert r.returncode == 0, f"hollow exited {r.returncode}"
    line = [l for l in r.stdout.splitlines() if l.startswith(TICKET + ":")]
    assert line and " 0 hollow " in line[-1], line
    assert "UNRAN" not in r.stdout and "unreadable" not in r.stdout, "a reversion could not be read"


def retirement():
    """(4) `cairn ruling open` refuses, the hook is gone, no skill or CLAUDE.md tells CC to open a ruling."""
    _teeth(RULING_PROOF, "test_the_hook_no_longer_fires_on_stop")
    _teeth(Q_PROOF, "test_ruling_open_is_retired_and_no_skill_opens_one")
    r = _cairn("ruling", "open", "/dev/null")
    assert r.returncode != 0 and "cairn question" in (r.stdout + r.stderr)
    # verify takes an id; the newest decision on disk is the one read, so the read-only store still answers.
    newest = sorted(p.stem for p in (COMMONS / "decisions").glob("2026-*.json"))[-1]
    r = _cairn("ruling", "verify", newest)
    assert r.returncode == 0, "cairn ruling verify no longer reads decisions/"
    settings = json.loads((ROOT / ".claude/settings.json").read_text())
    stop = json.dumps(settings.get("hooks", {}).get("Stop", []))
    assert "ruling" not in stop, stop
    tellers = subprocess.run("grep -rln 'cairn ruling open' skills/*/SKILL.md CLAUDE.md", shell=True,
                             cwd=ROOT, capture_output=True, text=True).stdout.split()
    print("files naming `cairn ruling open`:", tellers)
    for f in tellers:
        lines = [l for l in (ROOT / f).read_text().splitlines() if "cairn ruling open" in l]
        assert all(any(w in l.lower() for w in ("retired", "refuse", "never", "not ")) for l in lines), (f, lines)


def sieves():
    """(5) an answered question is same-act evidence; an open one is not; a cite of neither still reds."""
    _teeth(Q_PROOF, "test_an_answered_question_is_same_act_evidence_for_the_sieves")
    _teeth(EXEMPT_PROOF, "test_AN_ANSWERED_QUESTION_IS_EVIDENCE_AND_AN_OPEN_ONE_IS_NOT")


def intake():
    """(intake) the sorted contract carries `questions`, the door refuses a phantom id, the skill opens them; the charter stands."""
    r = subprocess.run([sys.executable, "-m", "cairn.machines.skill_block", "contract", "sorted"], cwd=ROOT,
                       capture_output=True, text=True, timeout=120, env=dict(os.environ, PYTHONPATH=str(ROOT)))
    assert r.returncode == 0 and "questions" in r.stdout, r.stdout[-500:] + r.stderr[-500:]
    print("contract sorted names questions")
    _teeth(SORTED_PROOF, "unresolvable question id refused", "questions exemption without referent refused",
           "the contract names questions", "the skill tells the caster to open a question")
    _teeth(Q_PROOF, "test_the_charter_stands_beside_the_code_and_names_this_proof",
           "test_the_probe_is_armed_with_carry_and_enough")
    r = subprocess.run([str(ROOT / "cairn/tools/intentions_model_compiler/recompile_gate.sh")], cwd=ROOT,
                       capture_output=True, text=True, timeout=300)
    print(f"$ recompile_gate.sh -> {r.returncode}: {(r.stdout + r.stderr).strip()[-300:]}")
    assert r.returncode == 0
    from cairn.devices.cairn.machines.harbor_master.clearance import boat_owner_of
    owner = boat_owner_of(TICKET)
    print("owning intention resolves to:", owner)
    assert owner


if __name__ == "__main__":
    globals()[sys.argv[1]]()
    print("OK", sys.argv[1])
