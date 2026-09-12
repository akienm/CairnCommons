"""The instruments behind ticket 76639374d9f9's verdict artifact — one subcommand per
validate criterion, each exiting 0 only when the criterion holds against the live world.

BERTHED IN THE COMMONS, NOT THE SCRATCHPAD, because the verdict artifact NAMES these
commands and the verdict door RE-RUNS what it is handed (`write_verdict` observes before
it berths). An instrument that dies with the session turns a verdict into a claim about a
run nobody can repeat.

Fire one at a time:

    PYTHONPATH=$HOME/dev/src/cairn python3 <this file> <subcommand>

`hollow` runs `cairn test --hollow 76639374d9f9 --seal` and must go LAST (resealing wipes
hollow evidence); the others are offline and fast. `live_two_turn` dials hex.local.
"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path("/home/akien/dev/src/cairn")
sys.path.insert(0, str(ROOT))
TICKET = "76639374d9f9"
TICKET_FILE = Path("/home/akien/dev/src/CairnCommons/tickets/"
                   "76639374d9f9-openai-wire-is-a-machine-anybody-can-include.json")
PROOFS = ROOT / "cairn/machines/openai_wire/proofs"


def _run(path, *args, timeout=600):
    r = subprocess.run([sys.executable, str(path), *args], cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    sys.stdout.write(r.stdout[-3000:])
    sys.stderr.write(r.stderr[-1500:])
    return r.returncode


def _seal(proof):
    from cairn.tools.proof_coverage.proof_coverage import _fingerprint_stale
    from cairn.tools.base.validation import latest_seal
    seal = latest_seal(proof)
    assert seal is not None, f"{proof} has no seal"
    assert seal["verdict"] == "green", f"{proof} latest seal is {seal['verdict']}"
    stale = _fingerprint_stale(proof, seal)
    assert not stale, f"{proof} seal is stale: {stale}"
    return seal


def clause_a():
    """(a) the SIEVE says openai_wire imports no device: the sieve's own seeded-failure proof
    is sealed green and current, and inspect() over the live corpus, filtered to the sieve,
    names build_inspector (135a905eac3c) and never openai_wire."""
    proof = ROOT / "cairn/machines/build_inspector/proofs/test_machine_imports_no_device.py"
    seal = _seal(proof)
    greens = set(seal["evidence"]["teeth_green"])
    assert "a_machine_importing_a_device_reds_by_file_and_module" in greens, greens
    from cairn.machines.build_inspector.inspector import inspect
    out = inspect()
    findings = [f for f in _findings(out) if f.get("method") == "machine_imports_no_device"]
    comps = sorted({f.get("component") for f in findings})
    print("machine_imports_no_device live findings:", comps)
    assert "openai_wire" not in comps, comps
    assert comps == ["build_inspector"], f"expected exactly build_inspector (135a905eac3c), got {comps}"


def _findings(out):
    if isinstance(out, dict):
        for k in ("findings", "reds"):
            if isinstance(out.get(k), list):
                return out[k]
        acc = []
        for v in out.values():
            if isinstance(v, dict) and isinstance(v.get("findings"), list):
                acc.extend(v["findings"])
        return acc
    return list(out)


def clause_b():
    """(b) translate.py pure and stdlib-only in both directions."""
    seal = _seal(PROOFS / "test_translate.py")
    assert "inbound_string_arguments_become_objects" in seal["evidence"]["teeth_green"]
    assert "translate_imports_stdlib_only" in seal["evidence"]["teeth_green"]
    assert _run(PROOFS / "test_translate.py") == 0


def clauses_c_d():
    """(c)(d) serve.py from injected callables alone; the c/d teeth never call make_server."""
    import ast
    seal = _seal(PROOFS / "test_serve.py")
    greens = set(seal["evidence"]["teeth_green"])
    for t in ("a_raising_resolve_is_a_named_5xx_not_an_empty_answer",
              "stream_true_is_refused_with_the_reason_on_the_wire",
              "models_lists_what_the_injected_callable_says"):
        assert t in greens, t
    tree = ast.parse((PROOFS / "test_serve.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in (
                "a_raising_resolve_is_a_named_5xx_not_an_empty_answer",
                "stream_true_is_refused_with_the_reason_on_the_wire"):
            assert "make_server" not in ast.unparse(node), f"{node.name} opens a listener"
    assert _run(PROOFS / "test_serve.py") == 0


def watch_armed():
    """The WATCHME probe is armed by the gate's own resolver, counts 0 holders today, and a
    seeded second holder raises the count to 2 (enough)."""
    from cairn.tools.base import watchme_spec
    from cairn.machines.openai_wire.probes import openai_wire_is_included_by_a_second_holder as probe
    t = json.loads(TICKET_FILE.read_text())
    err = watchme_spec.armed_error(t["watchme"])
    assert err is None, err
    assert probe.PROBE.carry and probe.PROBE.enough
    live = probe.survey_the_corpus()
    print("live holders:", live)
    assert live["distinct"] == 0, live
    seeded = probe.judge_graph({
        "devices/hermes_shim/shim.py": {"cairn.machines.openai_wire"},
        "devices/other/door.py": {"cairn.machines.openai_wire.serve"},
        "machines/openai_wire/proofs/test_serve.py": {"cairn.machines.openai_wire"},
    })
    assert seeded["distinct"] == 2, seeded


def coverage():
    """Per-letter coverage: clauses() returns the letters, lacks() is empty."""
    from cairn.tools.proof_coverage.proof_coverage import clauses, lacks
    t = json.loads(TICKET_FILE.read_text())
    got = clauses(t)
    print("clauses:", got)
    assert got == ["a", "b", "c", "d", "e"], got
    L = lacks(t, repo_root=ROOT)
    print("lacks:", L)
    assert L == [], L


def live_two_turn():
    """A real model (hex.local) answers a two-turn tool conversation through openai_wire."""
    from cairn.machines.openai_wire import make_handler, make_server, translate
    from cairn.devices.inference_domain import domain, host
    import threading, urllib.request
    ENDPOINT, MODEL = "http://hex.local:11434", "qwen3-coder:30b"

    def resolve(request):
        def agent_resolver(req):
            payload = {"model": request["model"], "messages": translate.to_provider(req["messages"]),
                       "stream": False, "options": {"temperature": 0.0}}
            if req.get("tools"):
                payload["tools"] = req["tools"]
            body = host._post("/api/chat", payload, endpoint=ENDPOINT, timeout=600.0,
                              transport=host._urllib_transport)
            m = body["message"]
            return {"answer": {"text": m.get("content") or "", "role": "assistant",
                               "tool_calls": m.get("tool_calls") or [],
                               "usage": {"prompt_tokens": body.get("prompt_eval_count", 0),
                                         "completion_tokens": body.get("eval_count", 0)}},
                    "cost": host.metered_cost(body), "falsifier": f"model {MODEL}", "horizon": "",
                    "provenance": {"host": ENDPOINT, "path": "/api/chat", "model": MODEL}}
        rq = {"kind": "chat", "messages": request["messages"], "model": request["model"] or MODEL}
        if request.get("tools"):
            rq["tools"] = request["tools"]
        out = domain.resolve(rq, resolver=agent_resolver)
        ans = dict(out["answer"]); ans["extra"] = {"hit": out.get("hit")}
        return ans

    srv = make_server(make_handler(resolve=resolve, models=lambda: list(host.installed_models(endpoint=ENDPOINT))),
                      "127.0.0.1", 0)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    def post(body):
        r = urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions", data=json.dumps(body).encode(),
                                   headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(r, timeout=600) as h:
            return json.loads(h.read())

    tools = [{"type": "function", "function": {"name": "read_file", "description": "Read a file's text",
              "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}}]
    # A NONCE IN THE PATH so every run of this instrument is a REAL dial and never a cache
    # hit standing in for one — the door re-runs this at write_verdict, and a hit would
    # measure the cache, not the wire.
    import uuid
    target = f"/tmp/answer-{uuid.uuid4().hex[:8]}.txt"
    msgs = [{"role": "user", "content": f"Use the read_file tool to read {target} and then tell me, "
                                        "in one short sentence, what it says. Do not guess."}]
    r1 = post({"model": MODEL, "messages": msgs, "tools": tools, "temperature": 0})
    c = r1["choices"][0]
    print("turn1:", c["finish_reason"], json.dumps(c["message"])[:300], r1["usage"], r1.get("x_cairn"))
    tc = c["message"].get("tool_calls") or []
    assert c["finish_reason"] == "tool_calls" and tc, "the model did not call the tool"
    assert isinstance(tc[0]["function"]["arguments"], str), "arguments not a JSON string on the wire"
    assert json.loads(tc[0]["function"]["arguments"])["path"] == target
    msgs.append(c["message"])
    msgs.append({"role": "tool", "tool_call_id": tc[0]["id"], "content": "the cake is a lie"})
    r2 = post({"model": MODEL, "messages": msgs, "tools": tools, "temperature": 0})
    c2 = r2["choices"][0]
    print("turn2:", c2["finish_reason"], repr(c2["message"]["content"]), r2["usage"], r2.get("x_cairn"))
    assert r1["x_cairn"]["hit"] is False and r2["x_cairn"]["hit"] is False, "a cache hit is not a live fire"
    assert c2["finish_reason"] == "stop" and "cake" in (c2["message"]["content"] or "").lower()


def hollow():
    """`cairn test --hollow 76639374d9f9 --seal` — LAST. Read for 0 hollow AND the skipped/unwrit counts."""
    r = subprocess.run(["bin/cmd/test", "--hollow", TICKET, "--seal", "--timeout", "300"],
                       cwd=ROOT, capture_output=True, text=True, timeout=3000)
    sys.stdout.write(r.stdout[-6000:]); sys.stderr.write(r.stderr[-2000:])
    assert r.returncode == 0, f"hollow exited {r.returncode}"
    line = [l for l in r.stdout.splitlines() if l.startswith(TICKET + ":")]
    assert line and " 0 hollow " in line[-1], line


if __name__ == "__main__":
    globals()[sys.argv[1]]()
    print("OK", sys.argv[1])
