"""measure_reds.py before|after — record 29569fca68a3's red sets (D6): the inspector's finding
identities (inspect() called directly, so nothing is filed) and the proofs `cairn test` reports
RED or UNRUNNABLE, into CairnCommons/measurements/2026-10-10-plan-log-split-reds.json."""
import json, re, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

phase = sys.argv[1]
assert phase in ("before", "after", "after_rename")  # after_rename: D26/D27, cairn moved with it
OUT = Path("/home/akien/dev/src/CairnCommons/measurements/2026-10-10-plan-log-split-reds.json")
S = Path(tempfile.gettempdir())
cairn_sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                           check=True).stdout.strip()
cc_sha = subprocess.run(["git", "-C", "/home/akien/dev/src/CairnCommons", "rev-parse", "HEAD"],
                        capture_output=True, text=True, check=True).stdout.strip()
t0 = time.time()
from cairn.machines.build_inspector.inspector import inspect
rep = inspect()
ins = sorted({f"{f.get('method')}|{f.get('at')}" for f in rep.get("findings", [])})
t1 = time.time()
log = S / f"plan-log-split-suite_{phase}.txt"
with open(log, "w") as fh:
    rc = subprocess.run(["bin/cairn", "test", "-q"], stdout=fh, stderr=subprocess.STDOUT).returncode
reds = sorted({m.group(2) for m in re.finditer(r"^\s+(RED|UNRUNNABLE)\s+(\S+)", log.read_text(), re.M)})
d = json.loads(OUT.read_text()) if OUT.exists() else {}
if "cairn_commit" in d and d["cairn_commit"] != cairn_sha:
    print(f"!! cairn moved: before {d['cairn_commit']} now {cairn_sha}", file=sys.stderr)
d.setdefault("cairn_commit", cairn_sha)       # the before/after commit; each phase carries its own
d.setdefault("what", "29569fca68a3 red sets before and after the plan/log split (D6)")
d[phase] = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "commons_commit": cc_sha,
            "cairn_commit": cairn_sha,
            "inspector": ins, "test": reds, "suite_exit": rc,
            "inspector_secs": round(t1 - t0), "suite_secs": round(time.time() - t1)}
OUT.write_text(json.dumps(d, indent=2) + "\n")
print(json.dumps({phase: {"inspector": len(ins), "test": len(reds), "suite_exit": rc,
                          "secs": round(time.time() - t0)}}))
