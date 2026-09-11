"""SPIKE — NOT A COMPONENT. Lives in the scratchpad deliberately (Law 9: nothing
green until built, running and inspected; this is none of those). Its ONE job is
to MEASURE what an unmodified OpenAI-shaped agent actually puts on the wire, so
ticket 548dd13fb4db is built from a measurement instead of from my memory of the
chat-completions schema.

Every inbound request is written verbatim to CAPTURE before anything is attempted.
"""
import json, os, sys, time, uuid, traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, "/home/akien/dev/src/cairn")
from cairn.devices.inference_domain import domain, host

CAPTURE = os.environ.get("SPIKE_CAPTURE", "/tmp/spike_capture.jsonl")
ENDPOINT = os.environ.get("SPIKE_ENDPOINT", "http://hex.local:11434")
MODEL = os.environ.get("SPIKE_MODEL", "qwen3-coder:30b")
PORT = int(os.environ.get("SPIKE_PORT", "8899"))


def capture(kind, payload):
    with open(CAPTURE, "a") as fh:
        fh.write(json.dumps({"at": time.time(), "kind": kind, "payload": payload},
                            default=str) + "\n")


def _ollama_messages(messages):
    """OpenAI carries tool-call arguments as a JSON STRING; ollama's /api/chat wants an
    OBJECT and refuses the string with "Value looks like object, but can't find closing
    '}' symbol" (measured 2026-09-11, hex.local, qwen3-coder:30b, second turn of a
    tool-using conversation). This is the translation the door owes on the way IN."""
    out = []
    for m in messages:
        m = dict(m)
        calls = m.get("tool_calls")
        if calls:
            fixed = []
            for c in calls:
                c = dict(c)
                fn = dict(c.get("function") or {})
                args = fn.get("arguments")
                if isinstance(args, str):
                    try:
                        fn["arguments"] = json.loads(args) if args.strip() else {}
                    except Exception:
                        fn["arguments"] = {"_unparsed": args}
                c["function"] = fn
                fixed.append(c)
            m["tool_calls"] = fixed
        if m.get("content") is None:
            m["content"] = ""
        out.append(m)
    return out


def _openai_message(answer):
    """ollama returns tool calls as {"function": {"name", "arguments": <dict>}}; the
    OpenAI shape needs an id, a type, and arguments as a JSON STRING."""
    msg = {"role": answer.get("role", "assistant"), "content": answer.get("text", "") or None}
    calls = answer.get("tool_calls") or []
    if calls:
        msg["tool_calls"] = [{
            "id": "call_" + uuid.uuid4().hex[:20],
            "type": "function",
            "function": {"name": c.get("function", {}).get("name", ""),
                         "arguments": json.dumps(c.get("function", {}).get("arguments", {}))
                                      if isinstance(c.get("function", {}).get("arguments"), (dict, list))
                                      else str(c.get("function", {}).get("arguments", ""))},
        } for c in calls]
    return msg


class Door(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):  # keep stderr for real errors only
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        capture("GET", {"path": self.path, "headers": dict(self.headers)})
        if self.path.rstrip("/").endswith("/models"):
            try:
                models = host.installed_models(endpoint=ENDPOINT)
            except Exception as exc:
                capture("models_error", {"error": repr(exc)})
                models = {MODEL: ""}
            self._send(200, {"object": "list", "data": [
                {"id": name, "object": "model", "owned_by": "cairn"} for name in models]})
        else:
            self._send(404, {"error": {"message": f"no route {self.path}"}})

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        try:
            req = json.loads(raw or b"{}")
        except Exception:
            capture("unparseable", {"path": self.path, "raw": raw[:4000].decode("utf8", "replace")})
            self._send(400, {"error": {"message": "unparseable body"}})
            return

        # THE MEASUREMENT — verbatim, before any attempt to serve it.
        capture("POST", {"path": self.path, "headers": dict(self.headers), "body": req})

        if not self.path.rstrip("/").endswith("/chat/completions"):
            self._send(404, {"error": {"message": f"no route {self.path}"}})
            return

        # What this spike CANNOT serve through the one door today — named, not faked.
        unserved = []
        if req.get("stream"):
            unserved.append("stream=true (ollama /api/chat is sent stream:False here)")
        if unserved:
            capture("unserved", {"reasons": unserved})
            self._send(400, {"error": {
                "message": "SPIKE cannot serve this through inference_domain yet: "
                           + "; ".join(unserved),
                "type": "cairn_spike_gap"}})
            return

        model = req.get("model") or MODEL
        tools = req.get("tools") or None

        def agent_resolver(request):
            """ollama_resolver's chat branch PLUS `tools` — the one thing it does not
            send today. Uses host's own _post, so the transport, the endpoint facts and
            the meter are inference_domain's, not this spike's."""
            payload = {"model": model, "messages": _ollama_messages(request["messages"]), "stream": False,
                       "options": {"temperature": request.get("temperature", 0.0)}}
            if request.get("tools"):
                payload["tools"] = request["tools"]
            body = host._post("/api/chat", payload, endpoint=ENDPOINT,
                              timeout=600.0, transport=host._urllib_transport)
            message = body.get("message")
            if not isinstance(message, dict):
                raise host.HostRefused(f"/api/chat returned {type(message).__name__} for 'message'")
            return {
                "answer": {"text": message.get("content", "") or "",
                           "role": message.get("role", "assistant"),
                           "tool_calls": message.get("tool_calls") or [],
                           "body": body},
                "cost": host.metered_cost(body),
                "falsifier": f"model {model}",
                "horizon": "",
                "provenance": {"host": ENDPOINT, "path": "/api/chat", "model": model,
                               "tools": [t.get("function", {}).get("name") for t in (tools or [])]},
            }

        resolve_req = {"kind": "chat", "messages": req["messages"], "model": model}
        if tools:
            resolve_req["tools"] = tools   # part of the question: same turns, different
                                           # toolset is a different call, so it must
                                           # canonicalize differently
        try:
            result = domain.resolve(resolve_req, resolver=agent_resolver)
        except Exception as exc:
            capture("resolve_error", {"error": repr(exc), "tb": traceback.format_exc()[-3000:]})
            self._send(502, {"error": {"message": f"{type(exc).__name__}: {exc}",
                                       "type": "cairn_resolve_error"}})
            return

        answer = result.get("answer") or {}
        body = answer.get("body") or {}
        out = {
            "id": "chatcmpl-" + uuid.uuid4().hex[:24],
            "object": "chat.completion",
            "created": int(time.time()),
            "model": req.get("model") or MODEL,
            "choices": [{"index": 0,
                         "finish_reason": "tool_calls" if answer.get("tool_calls") else "stop",
                         "message": _openai_message(answer)}],
            "usage": {"prompt_tokens": body.get("prompt_eval_count", 0),
                      "completion_tokens": body.get("eval_count", 0),
                      "total_tokens": body.get("prompt_eval_count", 0) + body.get("eval_count", 0)},
            "x_cairn": {"hit": result.get("hit"), "canonical": result.get("canonical")},
        }
        capture("served", {"hit": result.get("hit"), "chars": len(answer.get("text", ""))})
        self._send(200, out)


if __name__ == "__main__":
    print(f"spike door on :{PORT} -> {ENDPOINT} ({MODEL}); capture {CAPTURE}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Door).serve_forever()
