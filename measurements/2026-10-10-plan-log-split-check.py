"""The instrument for 29569fca68a3 — every ticket is split into its plan and its log.

Run from cairn/ with PYTHONPATH=. (it imports cairn.tools.base.ticket_log for reconstruct and
plan_fields). Three verbs, one per falsifier clause; each prints its counts as one JSON line and
exits 0 on pass, 1 on fail, 2 when it cannot measure (no split commit yet):

  reconstruct  for EVERY commit whose message starts '29569fca68a3: split' (the split, then the
               rename of D26/D27 — oldest first), every tickets/*.json (not '_') at its parent is
               reconstructed from the plan at that commit plus ONLY the log lines it added, and
               compared to the parent's doc; no plan at a split commit carries a key outside
               plan_fields; and no plan at HEAD (the plans as they stand) has a blank or missing
               'intention' (the tooth Akien's rename ruling added, via the peer 2026-10-11).
  reds         measurements/2026-10-10-plan-log-split-reds.json: the inspector finding identities
               and the red proofs after the split are each a subset of those before.
  rehearsals   every ticket whose cursor at the snapshot is open (not PROVED, SUPERSEDED, RETIRED,
               KILLED, ABSORBED, DROPPED) has a rehearsals/<id>-*.json record stamped after the split
               commit; prints the total log_reach_count and the tickets carrying reaches.

The snapshot is git itself (D3), so this re-runs at any later commit and reads the same answer.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CC = Path(__file__).resolve().parents[1]
TERMINAL = {"PROVED", "SUPERSEDED", "RETIRED", "KILLED", "ABSORBED", "DROPPED"}
REDS = CC / "measurements" / "2026-10-10-plan-log-split-reds.json"


def git(*a: str) -> str:
    return subprocess.run(["git", "-C", str(CC), *a], capture_output=True, text=True, check=True).stdout


def split_commits() -> list[str]:
    """Every '29569fca68a3: split' commit, oldest first."""
    out = git("log", "--format=%H%x09%s", "HEAD").splitlines()
    return [h for h, s in (x.split("\t", 1) for x in out) if s.startswith("29569fca68a3: split")][::-1]


def split_commit() -> str | None:
    hits = split_commits()
    return hits[0] if hits else None           # the first: the snapshot is its parent


def plans_at(sha: str) -> list[str]:
    names = git("ls-tree", "--name-only", f"{sha}:tickets").splitlines()
    return sorted(n for n in names if n.endswith(".json") and not n.startswith("_"))


def blob(sha: str, rel: str) -> str | None:
    r = subprocess.run(["git", "-C", str(CC), "show", f"{sha}:{rel}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def log_lines(sha: str, plan: str) -> list[dict]:
    raw = blob(sha, "tickets/" + plan[:-5] + ".log.jsonl")
    return [json.loads(x) for x in (raw or "").splitlines() if x.strip()]


def cursor(doc: dict) -> str:
    m = re.search(r"\[([A-Z]+)", str(doc.get("workflow_and_state", "")))
    return m.group(1) if m else "?"


def _blank(v) -> bool:
    return not (isinstance(v, str) and v.strip())


def reconstruct() -> int:
    from cairn.tools.base import ticket_log as L
    sps = split_commits()
    if not sps:
        print(json.dumps({"error": "no commit whose message starts '29569fca68a3: split'"}))
        return 2
    runs = [_one(L, sp) for sp in sps]
    no_intention = [p[:12] for p in plans_at("HEAD")       # the plans as they stand
                    if _blank(json.loads(blob("HEAD", "tickets/" + p)).get("intention"))]
    print(json.dumps({"commits": runs, "no_intention": no_intention}))
    bad = any(r["mismatches"] or r["extra_keys"] or r["missing"] or not r["tickets"] for r in runs)
    return 0 if not (bad or no_intention) else 1


def _one(L, sp: str) -> dict:
    pre = sp + "^"
    keep = set(json.loads(blob(sp, "tickets/_charter+why.json"))["plan_fields"])
    before, after = plans_at(pre), plans_at(sp)
    mismatch, extra, missing, kinds = [], [], [], {}
    for p in before:
        if p not in after:
            missing.append(p)
            continue
        snap = json.loads(blob(pre, "tickets/" + p))
        plan = json.loads(blob(sp, "tickets/" + p))
        added = log_lines(sp, p)[len(log_lines(pre, p)):]
        for x in added:
            kinds[x.get("kind")] = kinds.get(x.get("kind"), 0) + 1
        if L.reconstruct(plan, added) != snap:
            mismatch.append(p)
        if set(plan) - keep:
            extra.append([p, sorted(set(plan) - keep)])
    split_n = sum(1 for p in before if len(log_lines(sp, p)) > len(log_lines(pre, p)))
    return {"split_commit": sp, "tickets": len(before), "split": split_n,
            "already_clean": len(before) - split_n - len(missing),
            "lines_by_kind": kinds, "mismatches": mismatch, "extra_keys": extra, "missing": missing}


def reds() -> int:
    if not REDS.exists():
        print(json.dumps({"error": f"{REDS.name} absent"}))
        return 2
    d = json.loads(REDS.read_text(encoding="utf-8"))
    if "after" not in d:
        print(json.dumps({"error": "no after run recorded"}))
        return 2
    out, ok = {"cairn_commit": d.get("cairn_commit")}, True
    for k in ("inspector", "test"):
        b, a = set(d["before"][k]), set(d["after"][k])
        out[k] = {"before": len(b), "after": len(a), "new": sorted(a - b), "gone": sorted(b - a)}
        ok = ok and a <= b
    print(json.dumps(out))
    return 0 if ok else 1


def rehearsals() -> int:
    sp = split_commit()
    if not sp:
        print(json.dumps({"error": "no split commit"}))
        return 2
    t0 = datetime.fromtimestamp(int(git("show", "-s", "--format=%ct", sp).strip()), timezone.utc)
    stamp0 = t0.strftime("%Y%m%dT%H%M%S")
    open_ids = [p[:12] for p in plans_at(sp + "^")
                if cursor(json.loads(blob(sp + "^", "tickets/" + p))) not in TERMINAL]
    unrehearsed, total, carrying, clean = [], 0, {}, 0
    for tid in open_ids:
        recs = sorted(r for r in (CC / "rehearsals").glob(f"{tid}-*.json")
                      if (m := re.search(r"\d{8}T\d{6}", r.stem[12:])) and m.group(0) >= stamp0)
        if not recs:
            unrehearsed.append(tid)
            continue
        rec = json.loads(recs[-1].read_text(encoding="utf-8"))
        n = rec.get("log_reach_count")
        if n is None:
            unrehearsed.append(tid)
            continue
        clean += bool(rec.get("clean"))
        total += n
        if n:
            carrying[tid] = n
    print(json.dumps({"open": len(open_ids), "rehearsed": len(open_ids) - len(unrehearsed),
                      "clean": clean, "unrehearsed": unrehearsed, "log_reach_total": total,
                      "tickets_carrying_reaches": carrying}))
    return 0 if open_ids and not unrehearsed else 1


if __name__ == "__main__":
    verbs = {"reconstruct": reconstruct, "reds": reds, "rehearsals": rehearsals}
    if len(sys.argv) != 2 or sys.argv[1] not in verbs:
        print("usage: 2026-10-10-plan-log-split-check.py reconstruct|reds|rehearsals", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(verbs[sys.argv[1]]())
