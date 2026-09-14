"""The instruments behind ticket 30531f6e1c5d's verdict artifact — the artifact door.

One subcommand per validate criterion (berth validate-20260913T171818-ee1f0ab66a43),
each exiting 0 only when the criterion holds against the LIVE world: the two proofs are
RUN (not their seals read) and the named teeth must print PASS; the commit questions
and chain verifies are fired at the live roots; the WATCHME crossing is read from the
door's own history.json.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat.

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

Subcommands: jurisdiction door cli hooks gate writers genesis beside
"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
COMMONS = Path("/home/akien/dev/src/CairnCommons")
sys.path.insert(0, str(ROOT))
TICKET = "30531f6e1c5d"
DOOR_PROOF = ROOT / "cairn/tools/artifact/proofs/test_artifact_door.py"
GATE_PROOF = ROOT / "bin/proofs/test_artifact_gate.py"
_RUNS = {}


def _proof(path):
    """Run a proof once per process; return (rc, the set of PASS tooth names)."""
    if path not in _RUNS:
        r = subprocess.run([sys.executable, str(path)], cwd=ROOT, capture_output=True, text=True,
                           timeout=300, env=dict(os.environ, PYTHONPATH=str(ROOT)))
        passed = set()
        for line in r.stdout.splitlines():
            s = line.strip()
            if s.startswith("PASS"):
                passed.add(s[4:].strip().split("  — ")[0].strip())
        _RUNS[path] = (r.returncode, passed, r.stdout[-2500:] + r.stderr[-1500:])
    return _RUNS[path]


def _teeth(path, *names):
    rc, passed, tail = _proof(path)
    missing = [n for n in names if n not in passed]
    print(f"{path.relative_to(ROOT)}: rc={rc}, {len(passed)} PASS")
    for n in names:
        print("  ", "PASS" if n in passed else "MISSING", n)
    assert rc == 0, f"{path} exited {rc}:\n{tail}"
    assert not missing, f"teeth not seen PASS: {missing}"


def _cairn(*args, timeout=600):
    r = subprocess.run([str(ROOT / "bin/cairn"), *args], cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    print(f"$ cairn {' '.join(args)} -> {r.returncode}: {(r.stdout + r.stderr).strip()[-400:]}")
    return r


def jurisdiction():
    _teeth(DOOR_PROOF,
           "test_a_record_edited_around_the_door_is_refused_at_the_commit_question",
           "a write outside the jurisdiction is plain and says journaled: False",
           "a derived surface (intentions-congruency-lab) is not a record")
    _teeth(GATE_PROOF, *[f"Write to CairnCommons/{d}/x.json is refused" for d in
                         ("tickets", "troubles", "decisions", "slates", "ideas", "questions", "adjudications")])
    juris = json.loads((ROOT / "cairn/tools/artifact/jurisdiction.json").read_text())
    print("jurisdiction.json keys:", sorted(juris))


def door():
    _teeth(DOOR_PROOF,
           "test_the_three_caller_classes_measure_gate_cc_akien",
           "test_a_chain_break_is_detected_by_replay",
           "test_hand_edit_parks_and_the_record_stays_at_its_journaled_bytes",
           "test_a_scratch_world_never_reaches_the_live_journal")
    from cairn.tools.base.validation import latest_seal
    from cairn.tools.proof_coverage.proof_coverage import _fingerprint_stale
    seal = latest_seal(DOOR_PROOF)
    assert seal and seal["verdict"] == "green", seal and seal.get("verdict")
    stale = _fingerprint_stale(DOOR_PROOF, seal)
    print("seal:", {k: seal[k] for k in seal if k in ("verdict", "sealed", "timestamp", "isolation", "seal")}, "stale:", stale)
    assert not stale, stale


def cli():
    _teeth(DOOR_PROOF,
           "test_the_cli_front_door_answers_caller_with_a_measured_class",
           "install-hook writes .git/hooks/pre-commit")
    r = _cairn("artifact", "caller")
    assert r.returncode == 0, r.returncode
    out = r.stdout + r.stderr
    assert any(c in out for c in ("cc", "akien", "gate")), out
    assert "unknown" not in out, out


def hooks():
    _teeth(DOOR_PROOF,
           "test_the_hook_blocks_a_commit_made_around_the_door",
           "git commit of a journaled tree passes the hook",
           "test_the_tester_hook_asks_the_commit_question_before_the_reseal_ladder")
    hook = COMMONS / ".git/hooks/pre-commit"
    assert hook.exists() and os.access(hook, os.X_OK), hook
    assert "cairn-artifact-door" in hook.read_text(), "the CairnCommons hook is not the door's"
    r = subprocess.run(["git", "-C", str(COMMONS), "log", "-1", "--format=%h %s", "6e40224"],
                       capture_output=True, text=True)
    print("first commit under the hook:", r.stdout.strip())
    assert r.returncode == 0 and r.stdout.startswith("6e40224"), r.stderr
    cairn_hook = (ROOT / ".git/hooks/pre-commit").read_text()
    assert "artifact check" in cairn_hook, "the tester's hook does not ask the commit question"


def gate():
    _teeth(GATE_PROOF,
           "test_the_pretooluse_gate_refuses_a_write_to_a_record",
           "test_the_gate_is_wired_at_pretooluse_for_every_writing_tool",
           "the refusal carries the way through",
           "unreadable stdin allows and says so")
    rc, passed, _ = _proof(GATE_PROOF)
    allowed = [n for n in passed if n.startswith("allowed:")]
    refused = [n for n in passed if n.startswith("refused:")]
    print(f"table rows PASS: allowed={len(allowed)} refused={len(refused)} (measured 10/9 on 2026-09-13)")
    assert len(allowed) >= 10 and len(refused) >= 9, (allowed, refused)


def writers():
    _teeth(DOOR_PROOF,
           "test_the_seal_store_writes_its_validation_through_the_door",
           "test_the_projector_writes_history_and_state_through_the_door",
           "test_the_phase_writer_moves_a_ticket_through_the_door")
    for root in ("cairn", "CairnCommons"):
        r = _cairn("artifact", "check", root)
        assert r.returncode == 0, root


def genesis():
    for root in ("cairn", "CairnCommons"):
        r = _cairn("artifact", "verify", root)
        assert r.returncode == 0, root
        r = _cairn("artifact", "check", root)
        assert r.returncode == 0, root
    _teeth(DOOR_PROOF, "test_the_live_cairn_journal_verifies_from_genesis")


def beside():
    _teeth(DOOR_PROOF,
           "test_the_charter_stands_beside_the_code_and_names_this_proof",
           "test_the_probe_is_armed_with_carry_and_enough")
    hist = json.loads((ROOT / "cairn/tools/artifact/history.json").read_text())
    crossings = [(e.get("from"), e.get("to")) for e in hist]
    print("crossings in history.json:", crossings)
    watch = [e for e in hist if e.get("to") == "WATCHME"]
    assert watch, "no WATCHME crossing recorded in cairn/tools/artifact/history.json"
    proved = [p["identity"] for p in watch[-1].get("proved", [])]
    print("WATCHME crossing proved:", proved)
    assert "WATCHME" in watch[-1].get("workflow", ""), watch[-1].get("workflow")


if __name__ == "__main__":
    fn = globals()[sys.argv[1]]
    fn()
    print("OK", sys.argv[1])
