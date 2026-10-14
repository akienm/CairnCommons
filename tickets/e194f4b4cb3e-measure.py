"""Re-measure e194f4b4cb3e's falsifier clauses against the live box (marked testing).

Run from ~/dev/src/cairn with PYTHONPATH=. — exits 0 only if every clause reads as the
measurement record (e194f4b4cb3e-measured-satisfied.md) states. ``--control`` swaps clause 2's
model for one no rung carries, so the same instrument must read red (exit 1).
"""
import glob, json, os, sys, time

control = "--control" in sys.argv[1:]
ok = True

# (1) listed: the rack's device list names inference_domain, and its status view answers over the bus.
from cairn.tools.bus_client.bus_client import reach
bus = reach("inference_domain")
t0 = time.monotonic()
st = bus.request(sender="cc", to="inference_domain", verb="get", why="e194 clause 1 measure (testing)",
                 body={"what": "yield"})
s1 = round(time.monotonic() - t0, 2)
import subprocess
listed = "inference_domain" in subprocess.run(["bin/cairn", "list"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.split()
c1 = listed and isinstance(st, dict) and "spent" in json.dumps(st.get("body", st))
print(f"(1) listed in `cairn list`: {listed}; yield view answered over the bus in {s1}s: {c1}")
ok &= c1 and s1 < 10

# (2) a bus infer naming a model returns hex.local's answer under 10s.
model = "no-such-model:0b" if control else "qwen2.5:7b"
t0 = time.monotonic()
r = bus.request(sender="cc", to="inference_domain", verb="infer", why="e194 clause 2 measure (testing)",
                body={"prompt": f"Reply with the single word: ok (e194 measure nonce {time.time_ns()})", "model": model})
s2 = round(time.monotonic() - t0, 2)
b = (r or {}).get("body") or {}
host = ((b.get("provenance") or {}).get("host") or "")
c2 = b.get("answer") is not None and "hex.local" in host and s2 < 10
print(f"(2) infer model={model} answered in {s2}s from {host or b.get('refused')}: {c2}")
ok &= c2

# (3) with the host unreachable the resolver refuses, naming the host, inside 10s.
from cairn.devices.inference_domain import host as h
dead = "http://127.0.0.1:9"
t0 = time.monotonic()
try:
    h.ollama_resolver(model="qwen2.5:7b", endpoint=dead, timeout=10.0)({"kind": "generate", "prompt": "ok"})
    c3, why = False, "answered"
except h.HostUnreachable as e:
    why = str(e)
    c3 = "127.0.0.1:9" in why
s3 = round(time.monotonic() - t0, 2)
print(f"(3) unreachable host refused in {s3}s naming it: {c3} ({why[:120]})")
ok &= c3 and s3 < 10

# (4) no chart packet berthed after 2026-09-07 carries 'tree stratum unavailable'.
P = os.path.expanduser("~/.cairn/devices/chart/0/packets")
late = [p for p in glob.glob(f"{P}/orient-*.json") if os.path.basename(p)[7:15] > "20260907"]
bad = [p for p in late if "tree stratum unavailable" in open(p).read()]
c4 = len(late) > 0 and not bad
print(f"(4) {len(late)} orient packets after 2026-09-07, {len(bad)} carry 'tree stratum unavailable': {c4}")
ok &= c4

sys.exit(0 if ok else 1)
