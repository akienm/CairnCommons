import json, glob, sys
T = "201a37bf1613 0853294fe972 48519f4789b1 4d9115eb04cd aa4463bbd067 b41b0c0fff0e d6eb399ab6ad".split()
hits = {t: [] for t in T}
gated = {t: False for t in T}
for p in glob.glob("/home/akien/dev/src/cairn/**/history.json", recursive=True) + glob.glob("/home/akien/dev/src/CairnCommons/**/history.json", recursive=True):
    try: h = json.load(open(p))
    except Exception: continue
    rows = h if isinstance(h, list) else h.get("entries", h.get("history", []))
    for r in rows if isinstance(rows, list) else []:
        if not isinstance(r, dict): continue
        t = r.get("ticket")
        if t in hits and r.get("to") == "BUILDME" and r.get("direction") == "forward" and str(r.get("at", "")).startswith("2026-09-07"):
            hits[t].append(p.split("/src/")[1] + "@" + r["at"])
            if "a berthed chart chain claims ticket '%s'" % t in str(r.get("entry_gate", "")):
                gated[t] = True
print(f"{sum(1 for t in T if gated[t])} of 7 crossed through an entry gate that read a berthed chart chain claiming the ticket")
n = sum(1 for t in T if hits[t] and gated[t])
for t in T: print(t, sorted(set(hits[t]))[:2])
print(f"{n} of 7 carry a BUILDME crossing journaled 2026-09-07")
sys.exit(0 if n == 7 else 1)
