"""dda0e72b9c67 clause (4): the spellings bin/cmd/proofgate's segment judgement does not see.

For every proof on disk in cairn (git ls-files, proofs/test_*.py) and three spellings —
``ls <proof> | xargs python3``, a heredoc fed to ``bash`` that runs ``python3 <proof>``, and a
script FILE that runs it — this hands the command to the gate exactly as the hook would
(``proofgate.judge``: refused, rewritten, or passed), runs what the gate hands back under
``strace -f``, and records every write-shaped syscall aimed under the live ~/.cairn.

THE HARM BOUND. The 2026-10-06 census ran raw and its 2705 paths landed in the operator's world.
This one runs each command inside ``bwrap`` with ~/.cairn as a throwaway overlay (``--tmp-overlay``:
the lower layer is the live tree, every write lands in a tmpfs that dies with the run), the
network unshared (no live 5432, no inference host), and the live bus socket whited out inside
the sandbox, so a proof cannot reach a live device either. strace still sees the path the proof
aimed at, which is the measurement: a write under ~/.cairn *would have* landed live.

A connect() to a socket under ~/.cairn is recorded separately as ``reached``.

    python3 tickets/dda0e72b9c67-spelling-census.py OUT_DIR [--jobs N] [--only SUBSTR]
    python3 tickets/dda0e72b9c67-spelling-census.py OUT_DIR --summary

Resumable: a (proof, spelling) row already in OUT_DIR/rows.jsonl is not re-run.
"""

from __future__ import annotations

import concurrent.futures as cf
import importlib.machinery
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

REPO = Path.home() / "dev" / "src" / "cairn"
CAIRN_HOME = Path.home() / ".cairn"
BUS_SOCK = CAIRN_HOME / "devices" / "cairn" / "machines" / "bus" / "0" / "bus.sock"
TIMEOUT_S = 300
PROOF = re.compile(r"(^|/)proofs/(.+/)?test_[^/]*\.py$")
TRACE = "openat,open,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,unlinkat,link,linkat,symlink,symlinkat,truncate,connect"
WRITE_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")
_LOCK = threading.Lock()


def _gate():
    spec = importlib.util.spec_from_loader(
        "proofgate", importlib.machinery.SourceFileLoader("proofgate", str(REPO / "bin" / "cmd" / "proofgate")))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def proofs() -> list[str]:
    out = subprocess.run(["git", "-C", str(REPO), "ls-files"], capture_output=True, text=True, check=True)
    return sorted(p for p in out.stdout.splitlines() if PROOF.search(p))


def spellings(proof: str, scratch: Path) -> dict[str, str]:
    script = scratch / "runs_the_proof.sh"
    script.write_text(f"#!/bin/bash\npython3 {proof}\n")
    return {
        "xargs": f"ls {proof} | xargs python3",
        "heredoc": f"bash <<'EOF'\npython3 {proof}\nEOF",
        "script": f"bash {script}",
    }


def writes_in(log: Path) -> tuple[list[str], list[str]]:
    """(paths written under ~/.cairn, sockets under ~/.cairn connected to) from an strace -f log."""
    home = str(CAIRN_HOME)
    wrote, reached = set(), set()
    for line in log.read_text(errors="replace").splitlines():
        if home not in line:
            continue
        call = line.split("(", 1)[0].split()[-1] if "(" in line else ""
        quoted = re.findall(r'"([^"]*)"', line)
        if call.startswith(("symlink", "link")):
            # the TARGET of a link is not written (the seal links its pristine copy at live
            # records, read-only); only the new link's own path is
            quoted = quoted[-1:]
        elif not call.startswith("rename"):
            quoted = quoted[:1]
        for path in (q for q in quoted if q == home or q.startswith(home + "/")):
            if call == "connect":
                reached.add(path)
            elif call in ("openat", "open"):
                if any(f in line for f in WRITE_FLAGS):
                    wrote.add(path)
            elif call:
                wrote.add(path)
    return sorted(wrote), sorted(reached)


def run_one(gate, proof: str, spelling: str, out: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="dda0-census-") as tmp:
        t = Path(tmp)
        typed = spellings(proof, t)[spelling]
        judged = gate.judge(typed)
        row = {"proof": proof, "spelling": spelling, "typed": typed,
               "gate": None if judged is None else judged["action"]}
        if judged and judged["action"] == "refuse":
            row.update(ran=False, wrote=[], reached=[])
            return row
        command = judged["command"] if judged else typed
        log, done, left = t / "strace.log", t / "done", t / "left"
        # pid 1 of a fresh pid namespace is this untraced shell: it starts strace on the command,
        # waits for the COMMAND to finish (a marker the traced shell writes), counts what the
        # proof left running (a lazily started daemon keeps strace -f waiting forever, measured
        # on the first trial: the bare proof started a bus server at the live bus home), stops
        # strace with TERM so the log is whole, and exits — which kills every survivor.
        inner = (f"rm -f {BUS_SOCK}; "
                 f"strace -f -qq -o {log} -e trace={TRACE} bash -c "
                 f"'bash -c \"$CENSUS_CMD\" > {t / "out"} 2>&1; echo $? > {done}' & S=$!; "
                 f"for i in $(seq {TIMEOUT_S * 2}); do [ -e {done} ] && break; sleep 0.5; done; "
                 f"sleep 1; ps -e -o pid=,args= | grep -v -E '^ *(1|'$S'|'$$') ' "
                 f"| grep -v -E ' (ps|grep|sleep) ' > {left}; "
                 f"kill -TERM $S 2>/dev/null; sleep 2; exit 0")
        argv = ["bwrap", "--dev-bind", "/", "/", "--proc", "/proc",
                "--overlay-src", str(CAIRN_HOME), "--tmp-overlay", str(CAIRN_HOME),
                "--unshare-net", "--unshare-pid", "--die-with-parent", "--chdir", str(REPO),
                "--", "bash", "-c", inner]
        if judged:
            # A command the gate rewrote runs under the tester's own bwrap seal, which cannot
            # nest inside this one (measured: the seal's probe read INDETERMINATE and
            # `cairn test --exec` refused to run). The seal IS the isolation under test here, so
            # it runs on the live box under strace alone: a write it lets through lands live,
            # and that landing is exactly what this row must be able to read.
            argv = ["bash", "-c",
                    f"strace -f -qq -o {log} -e trace={TRACE} bash -c \"$CENSUS_CMD\" "
                    f"> {t / 'out'} 2>&1; echo $? > {done}; : > {left}"]
        env = {**os.environ, "CENSUS_CMD": command}
        started = time.time()
        try:
            subprocess.run(argv, env=env, capture_output=True, text=True, timeout=TIMEOUT_S + 60,
                           cwd=str(REPO))
        except subprocess.TimeoutExpired:
            pass
        row["exit"] = done.read_text().strip() if done.is_file() else "timeout"
        row["left_running"] = [x.strip() for x in left.read_text().splitlines()] if left.is_file() else []
        wrote, reached = writes_in(log) if log.is_file() else ([], [])
        lines = [x for x in log.read_text(errors="replace").splitlines()
                 if any(f'"{w}"' in x for w in wrote)][:40] if wrote else []
        tail = (t / "out").read_text(errors="replace").splitlines()[-6:] if (t / "out").is_file() else []
        row.update(ran=True, ran_as=command, wrote=wrote, reached=reached, syscalls=lines, tail=tail)
        if judged:
            # inside the tester's seal ~/.cairn IS the swap, mounted at the live address, so a
            # path strace saw is not yet a live write: it is one only if it is on the live disk
            # now, changed since the run began (a live device beating in the same window would
            # read here too, which is why the rows keep the syscalls)
            row["aimed_inside_seal"] = wrote
            row["wrote"] = [w for w in wrote if _landed_since(Path(w), started)]
        return row


def _landed_since(path: Path, t0: float) -> bool:
    try:
        return path.lstat().st_mtime >= t0 - 1
    except OSError:
        return False


def done_keys(rows: Path) -> set[tuple[str, str]]:
    if not rows.is_file():
        return set()
    return {(r["proof"], r["spelling"]) for r in map(json.loads, rows.read_text().splitlines()) if r}


def census(out: Path, jobs: int, only: str | None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    rows = out / "rows.jsonl"
    gate, have = _gate(), done_keys(rows)
    todo = [(p, s) for p in proofs() if not only or only in p
            for s in ("xargs", "heredoc", "script") if (p, s) not in have]
    print(f"{len(todo)} runs to go ({len(have)} already recorded)", flush=True)
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        for n, row in enumerate(ex.map(lambda ps: run_one(gate, *ps, out), todo), 1):
            with _LOCK, rows.open("a") as f:
                f.write(json.dumps(row) + "\n")
            if row["wrote"]:
                print(f"[{n}/{len(todo)}] {row['spelling']:8} {row['proof']}: {len(row['wrote'])} live write(s)", flush=True)
            elif n % 25 == 0:
                print(f"[{n}/{len(todo)}]", flush=True)


def summary(out: Path) -> int:
    rows = [json.loads(x) for x in (out / "rows.jsonl").read_text().splitlines() if x]
    proofs_seen = sorted({r["proof"] for r in rows})
    red = 0
    for s in ("xargs", "heredoc", "script"):
        mine = [r for r in rows if r["spelling"] == s]
        gates = {g: sum(1 for r in mine if r["gate"] == g) for g in (None, "rewrite", "refuse")}
        leaking = [r for r in mine if r["wrote"]]
        paths = sum(len(r["wrote"]) for r in leaking)
        reached = sum(1 for r in mine if r["reached"])
        red += bool(leaking)
        print(f"{s:8} runs={len(mine)} gate: passed={gates[None]} rewritten={gates['rewrite']} "
              f"refused={gates['refuse']} | proofs writing live ~/.cairn={len(leaking)} "
              f"paths={paths} | reached a live socket={reached}")
    print(f"proofs censused: {len(proofs_seen)}")
    return 1 if red else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    out = Path(a[0])
    if "--summary" in a:
        sys.exit(summary(out))
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 3
    only = a[a.index("--only") + 1] if "--only" in a else None
    census(out, jobs, only)
