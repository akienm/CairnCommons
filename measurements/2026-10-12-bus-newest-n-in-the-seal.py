"""Criterion 2 of ticket f8a97b570073, measured inside the sealed exec.

The live bus socket is not visible inside `cairn test --exec` (the seal snapshots
~/.cairn without bus.sock), and a seal that saw the live bus would let live state decide
a verdict. So this starts its OWN bus over a scratch table, seeds it to today's live size,
and asserts what the criterion means:
  (i)  read(limit=5) returns exactly the newest 5, oldest first, in under 2 s;
  (ii) count() returns the seeded total.

The bus is a direct child of this process (not a systemd unit), so it sits in the test
run's own process tree and the run's kill reaches it; it is also stopped in `finally`.
The scratch HOME is short because AF_UNIX paths are bounded at 108 bytes.

Run:  cd ~/dev/src/cairn && PYTHONPATH=. python3 ~/dev/src/CairnCommons/measurements/2026-10-12-bus-newest-n-in-the-seal.py
Exit 0 when both hold, 1 when either fails.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SEEDED = 4500          # live cairn/personal measured 4487 on 2026-10-12
BOUND_S = 2.0
TO, CHANNEL = "cairn", "personal"


def main() -> int:
    from cairn.tools.bus_client.remote import RemoteBus, _BUS_MODULE
    home = Path(tempfile.mkdtemp(prefix="bn", dir="/tmp"))
    proc = subprocess.Popen([sys.executable, "-m", _BUS_MODULE, "serve", "--home", str(home), "--scratch"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=dict(os.environ))
    try:
        deadline = time.monotonic() + 60
        while not (home / "bus.sock").exists():
            if proc.poll() is not None:
                print(f"scratch bus exited {proc.returncode}: {proc.stderr.read().decode()[-600:]}")
                return 1
            if time.monotonic() > deadline:
                print("scratch bus never opened its socket in 60 s")
                return 1
            time.sleep(0.1)
        bus = RemoteBus(home=home, scratch=True)
        t0 = time.monotonic()
        for i in range(SEEDED):
            bus.post(sender="measure", to=TO, channel=CHANNEL, why="f8a9 criterion 2 seed",
                     body={"n": i})
        seed_s = time.monotonic() - t0
        t = time.monotonic()
        rows = bus.read(to=TO, channel=CHANNEL, limit=5)
        read_s = time.monotonic() - t
        t = time.monotonic()
        total = bus.count(to=TO, channel=CHANNEL)
        count_s = time.monotonic() - t
        got = [((r.get("body") or {}).get("n")) for r in rows]
        want = list(range(SEEDED - 5, SEEDED))
        ok_read = got == want and read_s < BOUND_S
        ok_count = total == SEEDED
        print(f"seeded {SEEDED} in {seed_s:.2f} s")
        print(f"  {'PASS' if ok_read else 'FAIL'}  read(limit=5) -> {got} in {read_s:.3f} s (want {want}, < {BOUND_S} s)")
        print(f"  {'PASS' if ok_count else 'FAIL'}  count() -> {total} in {count_s:.3f} s (want {SEEDED})")
        return 0 if ok_read and ok_count else 1
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=20)
        shutil.rmtree(home, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
