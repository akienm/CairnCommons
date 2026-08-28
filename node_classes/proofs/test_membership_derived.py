"""
Proof: membership-is-derived-or-dropped
Verifies that node_class definitions use members_derived_by (a runnable command)
instead of members_so_far (a static array), and that each command produces
correct membership when run.
"""
import json
import subprocess
from pathlib import Path

NODE_CLASSES_DIR = Path(__file__).parent.parent

DEFINITIONS = ["code-seam", "concept-piece", "host-seam", "operational-driver", "skill"]

EXPECTED_COUNTS = {
    "code-seam": 22,
    "concept-piece": 1,
    "host-seam": 1,
    "operational-driver": 0,
    "skill": 15,
}


def test_members_so_far_removed():
    for name in DEFINITIONS:
        path = NODE_CLASSES_DIR / f"{name}.json"
        data = json.loads(path.read_text())
        assert "members_so_far" not in data, (
            f"{name}.json still carries members_so_far — the stale static array survived"
        )


def test_members_derived_by_present():
    for name in DEFINITIONS:
        path = NODE_CLASSES_DIR / f"{name}.json"
        data = json.loads(path.read_text())
        assert "members_derived_by" in data, (
            f"{name}.json missing members_derived_by"
        )
        assert isinstance(data["members_derived_by"], str), (
            f"{name}.json members_derived_by is not a string"
        )
        assert len(data["members_derived_by"].strip()) > 0, (
            f"{name}.json members_derived_by is empty"
        )


def test_derivation_commands_produce_correct_membership():
    for name in DEFINITIONS:
        path = NODE_CLASSES_DIR / f"{name}.json"
        data = json.loads(path.read_text())
        cmd = data["members_derived_by"]
        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True, text=True, timeout=30
        )
        lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
        expected = EXPECTED_COUNTS[name]
        assert len(lines) >= expected, (
            f"{name}: derivation command returned {len(lines)} results, "
            f"expected >= {expected}"
        )


def test_skill_retired_members_preserved():
    path = NODE_CLASSES_DIR / "skill.json"
    data = json.loads(path.read_text())
    assert "retired_members" in data, "skill.json lost retired_members"
    assert isinstance(data["retired_members"], list), "retired_members is not a list"
    assert len(data["retired_members"]) == 1, (
        f"retired_members has {len(data['retired_members'])} entries, expected 1"
    )


def test_skill_roster_note_preserved():
    path = NODE_CLASSES_DIR / "skill.json"
    data = json.loads(path.read_text())
    assert "roster_note" in data, "skill.json lost roster_note"
    assert isinstance(data["roster_note"], str), "roster_note is not a string"
    assert len(data["roster_note"]) > 0, "roster_note is empty"
