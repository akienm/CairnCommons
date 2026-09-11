"""The instruments behind ticket 548dd13fb4db's verdict artifact — one subcommand per
validate criterion, each exiting 0 only when the criterion holds against the live world.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat, which is the narration the door exists to refuse.

Fire one at a time:

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

`live_two_turn` dials hex.local for real and costs inference; the other seven are offline.
"""
import sys, json, subprocess, tempfile, os, importlib.util
sys.path.insert(0, "/home/akien/dev/src/cairn")
ROOT = "/home/akien/dev/src/cairn"

TOOLS = [{"type": "function", "function": {
    "name": "terminal", "description": "Run a shell command",
    "parameters": {"type": "object", "properties": {"command": {"type": "string"}},
                   "required": ["command"]}}}]
ASK = [{"role": "user", "content": "What is the hostname of this machine? Use the terminal tool."}]
AGENT_TURNS = ASK + [
    {"role": "assistant", "content": "",
     "tool_calls": [{"id": "c1", "function": {"name": "terminal",
                                              "arguments": {"command": "hostname"}}}]},
    {"role": "tool", "tool_call_id": "c1", "content": "akiendelllinux"}]


def live_two_turn():
    """(a) A real tool-using conversation to hex.local and back, through domain.resolve."""
    from cairn.devices.inference_domain import domain, host
    r = host.ollama_resolver(model="qwen2.5:7b", endpoint="http://hex.local:11434",
                             horizon=host.EXPIRED)
    out1 = domain.resolve({"kind": "chat", "tools": TOOLS, "messages": ASK}, resolver=r)
    calls = out1["answer"].get("tool_calls")
    assert calls, "turn 1 returned no tool_calls on the answer"
    cid = calls[0].get("id") or "c1"
    t2 = {"kind": "chat", "tools": TOOLS, "messages": ASK + [
        {"role": "assistant", "content": "", "tool_calls": [{"id": cid, "function": calls[0]["function"]}]},
        {"role": "tool", "tool_call_id": cid, "content": "akiendelllinux"}]}
    out2 = domain.resolve(t2, resolver=r)
    assert out2["answer"]["text"].strip(), "turn 2 returned an empty answer"
    # and the ROUTED production door carries the agent turns too
    routed = host.ollama_resolver(model="qwen3-coder:30b", horizon=host.EXPIRED)
    outb = domain.resolve({"kind": "chat", "tools": TOOLS, "messages": AGENT_TURNS}, resolver=routed)
    assert outb["answer"]["text"].strip(), "the routed door emptied the second turn"
    print(f"turn1 tool_calls={calls[0]['function']['name']!r}; "
          f"turn2={out2['answer']['text'][:60]!r}; routed={outb['answer']['text'][:60]!r}")


def canonical_toolset():
    """(b) The toolset participates in the canonical digest."""
    from cairn.devices.inference_domain.domain import canonicalize, canonical_digest
    base = {"kind": "chat", "messages": ASK}
    a = dict(base, tools=[{"type": "function", "function": {"name": "alpha"}}])
    b = dict(base, tools=[{"type": "function", "function": {"name": "beta"}}])
    assert canonicalize(a) != canonicalize(b), "differing toolsets collapsed to one canonical"
    assert canonical_digest(canonicalize(a)) != canonical_digest(canonicalize(b)), "digests collided"
    assert canonicalize(base) != canonicalize(a), "a toolset did not change the question"
    # An inequality test that can never be equal proves nothing. `domain` is the ONE key
    # canonicalize strips, so it is the control: if this comparison came back unequal too,
    # the tooth above would be reading "two dicts differ", not "the toolset is part of the
    # question".
    assert canonicalize(dict(base, domain="x")) == canonicalize(dict(base, domain="y")), \
        "even the stripped key changes the canonical — the comparison discriminates nothing"
    print("differing toolsets -> differing canonical AND differing digest; "
          "the stripped `domain` key changes neither (the control)")


def _old_host():
    """The committed (pre-build) host.py, loaded read-only. No working tree is touched."""
    old = subprocess.run(["git", "show", "HEAD:cairn/devices/inference_domain/host.py"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    fd, path = tempfile.mkstemp(suffix="_oldhost.py"); os.write(fd, old.encode()); os.close(fd)
    spec = importlib.util.spec_from_file_location("_oldhost", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    os.unlink(path)
    return m


def second_turn_tooth():
    """(c) The second turn works NOW and REDDED before the build — a tooth that passes
    both ways asserts nothing, so both directions are measured."""
    from cairn.devices.inference_domain import host
    assert host.validated_messages({"messages": AGENT_TURNS}) == AGENT_TURNS, \
        "the built door does not accept a tool-using conversation"
    old = _old_host()
    try:
        old.validated_messages({"messages": AGENT_TURNS})
    except old.BadRequest as e:
        print(f"built door ACCEPTS the 3-turn conversation; pre-build door REFUSED it: {e}")
        return
    raise AssertionError("the PRE-BUILD door accepted the agent turns — the tooth proves nothing")


def both_records():
    """(d) Every agent call lands a row AND an emission line, joined by canonical digest."""
    from cairn.devices.db_domain import store
    from cairn.devices.inference_domain import domain
    from cairn.devices.inference_domain.domain import canonical_digest
    rows = [r for r in store.read("inference_calls")
            if '"tools":[' in str(r.get("canonical") or "")]
    assert rows, "no tool-carrying rows in inference_calls at all"
    pointers = {str(rec.get("pointer")) for rec in domain.diagnostic_records()}
    digests = {canonical_digest(str(r["canonical"])) for r in rows}
    joined = digests & pointers
    assert joined, "not one tool-carrying row joins the emission trail by digest"
    missing = digests - pointers
    assert not missing, f"{len(missing)} tool-carrying row(s) have no emission line"
    print(f"{len(rows)} tool-carrying rows, {len(digests)} distinct canonicals, all on the trail")


def agent_lane():
    """(e) A byte-identical retry re-resolves, WITHOUT salting the canonical or skipping lookup."""
    from cairn.devices.inference_domain import domain, host
    calls = {"n": 0}
    def fake(request):
        calls["n"] += 1
        return {"answer": {"text": f"a{calls['n']}"}, "cost": 1.0,
                "horizon": host.EXPIRED, "provenance": {}}
    def plain(request):
        calls["n"] += 1
        return {"answer": {"text": f"a{calls['n']}"}, "cost": 1.0, "horizon": "", "provenance": {}}
    import uuid
    req = {"kind": "chat", "tools": TOOLS,
           "messages": [{"role": "user", "content": f"lane_{uuid.uuid4().hex}"}]}
    before = domain.canonicalize(req)
    domain.resolve(dict(req), resolver=fake); n1 = calls["n"]
    domain.resolve(dict(req), resolver=fake); n2 = calls["n"]
    assert n2 == n1 + 1, "the agent lane replayed a cached answer instead of re-resolving"
    after = domain.canonicalize(req)
    assert before == after, "the canonical text was SALTED — the lane forked the cache"

    req2 = {"kind": "chat", "tools": TOOLS,
            "messages": [{"role": "user", "content": f"lane_{uuid.uuid4().hex}"}]}
    domain.resolve(dict(req2), resolver=plain); m1 = calls["n"]
    hit = domain.resolve(dict(req2), resolver=plain)
    assert hit["hit"] is True and calls["n"] == m1, "the DEFAULT lane stopped compiling once"
    print("agent lane re-resolves; default lane still hits; canonical text identical in both")


def refusals():
    """(5) A SECOND CHECKABLE SHAPE, not an exemption: malformed agent turns still refuse."""
    from cairn.devices.inference_domain import host
    bad = [
        ("tool result with no tool_call_id", {"role": "tool", "content": "x"}),
        ("tool result whose role is wrong", {"role": "user", "tool_call_id": "c", "content": "x"}),
        ("assistant turn with neither content nor calls", {"role": "assistant", "content": "",
                                                           "tool_calls": []}),
        ("tool call with no function name", {"role": "assistant", "content": "",
                                             "tool_calls": [{"function": {"arguments": {}}}]}),
        ("arguments as a JSON string", {"role": "assistant", "content": "",
                                        "tool_calls": [{"function": {"name": "t",
                                                                     "arguments": '{"a":1}'}}]}),
    ]
    for why, turn in bad:
        try:
            host.validated_messages({"messages": [turn]})
        except host.BadRequest:
            continue
        raise AssertionError(f"NOT REFUSED: {why} — that is an exemption, not a second shape")
    # and the WELL-FORMED agent shapes still pass: a shape that refuses everything is not a shape
    assert host.validated_messages({"messages": AGENT_TURNS}) == AGENT_TURNS
    print(f"{len(bad)} malformed agent turns refused; the well-formed conversation accepted")


def bounds():
    """(6) No listener, no socket, no second connection; domain.py unedited; sole path holds."""
    diff = subprocess.run(["git", "diff", "--", "cairn/devices/inference_domain"],
                          cwd=ROOT, capture_output=True, text=True).stdout
    added = [l for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
    import re
    bad = [l for l in added if re.search(r"HTTPServer|serve_forever|\.bind\(|\.listen\(|socket\.socket", l)]
    assert not bad, f"a listener/socket entered the device: {bad[:3]}"
    # A grep that has never matched anything is not evidence of absence. Fire the same
    # pattern at a file KNOWN to hold a listener — the hermes door spike — so the zero
    # above is a measurement rather than a regex that quietly never worked.
    spike = "/home/akien/dev/src/CairnCommons/measurements/2026-09-11-hermes-openai-door-spike.py"
    hits = [l for l in open(spike) if re.search(r"HTTPServer|serve_forever|\.bind\(|\.listen\(|socket\.socket", l)]
    assert hits, "the listener pattern matches NOTHING even in a known listener — the tooth is dead"
    stat = subprocess.run(["git", "diff", "--stat", "--", "cairn/devices/inference_domain/domain.py"],
                          cwd=ROOT, capture_output=True, text=True).stdout.strip()
    assert not stat, f"domain.py was edited, and constrain put it out of bounds: {stat}"
    from cairn.tools.import_sieve import sieve
    caught = sieve.catches(sieve.import_graph(ROOT), {
        "kind": "sole_path", "capability": "the inference host",
        "modules": ("urllib.request", "urllib.error", "http.client", "requests", "httpx",
                    "aiohttp", "socket", "ftplib", "telnetlib"),
        "only": "cairn/devices/inference_domain/"})
    assert not caught, f"the sole path to the inference host was breached: {caught}"
    print("no listener/socket added; domain.py untouched; sole-path mesh clean")


def probe_armed():
    """(7) The WATCHME probe is armed at the berth the ticket's spec names, and it BITES."""
    from cairn.devices.inference_domain.probes import an_agent_retry_gets_a_fresh_sample as p
    from cairn.tools.base.probe import Probe
    assert isinstance(p.PROBE, Probe), "PROBE is not a frozen Probe"
    assert p.PROBE.carry and p.PROBE.enough, "a probe needs both a carry and an enough"
    now = "2026-09-11T12:00:00-06:00"
    tc = '{"kind":"chat","tools":[{"a":1}]}'
    replayed = p.judge([{"created": now, "canonical": tc, "verdict": "hit"}])
    clean = p.judge([{"created": now, "canonical": tc + str(i), "verdict": "miss"}
                     for i in range(p._ENOUGH)])
    assert p._trigger(None, {"corpus": replayed}), "the probe does not fire on a replayed agent call"
    assert not p._enough({"corpus": p.judge([])}), "the probe CLEARS AT ZERO — it is vacuous"
    assert p._enough({"corpus": clean}), "the probe never clears even on clean traffic"
    print("probe armed, fires on a replay, is non-vacuous, and clears on clean traffic")


if __name__ == "__main__":
    fn = globals()[sys.argv[1]]
    fn()
    print(f"GREEN {sys.argv[1]}")
