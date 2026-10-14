# e194f4b4cb3e — inference_domain answers the bus, measured satisfied

The piece this ticket's PROVED crossing is sealed over. It is not the ticket file, because a seal over
the ticket expires when the crossing writes the cursor back (CairnCommons 891fb63).

## The claim

The ticket's why (measured 2026-09-06): no inference_domain process was running, a bus request to it hung
20s+, and every chart packet that week carried "tree stratum unavailable". The lived symptom is a
device that cannot reach its brain. The falsifier names four clauses and a WRONG INTENT route.

Akien answered open-55b04185f30f: "Lgtm — approving CC's triage of 2026-09-23, whose proposal for this
question was: 'route it the way the ticket's own WRONG INTENT clause says; no standing daemon'". So
e194 closes as measured satisfied on clauses (2) and (4), with no standing daemon. The hang fix goes
to a bus/shim ticket.

## What was measured, 2026-10-14

`PYTHONPATH=. python3 ../CairnCommons/tickets/e194f4b4cb3e-measure.py` from `~/dev/src/cairn` (the script is
beside this file) runs against the live box. Every call is marked testing. Exit 0 only if all four read
as below.

- **(1) listed.** `cairn list` names inference_domain, and `get` / `what=yield` over a `reach` bus
  answers in about 6s. There is **no standing pid, by design**. Since 2026-09-18
  (`bus_client.inference_bus` docstring) the asker's bus pulses inference_domain's shim and the
  device answers in that process. A standing pid is the daemon Akien's answer rules out, and it is
  not built. The status-pid half of the clause is killed, and nothing is owed for it.
- **(2) infer under 10s with hex.local's answer.** `bus.request(..., verb="infer", body={"prompt":
  <nonce'd>, "model": "qwen2.5:7b"})` answers in **0.37–0.46s**. Its provenance host is
  `http://hex.local:11434`, and the answer is not a cache hit (the prompt carries a fresh nonce).
  Codemother's own call (`watch.py:_embed`) names its model the same way.
- **(3) unreachable host refuses inside 10s, naming it.** `host.ollama_resolver(endpoint=
  "http://127.0.0.1:9")` raises `HostUnreachable("inference host unreachable at
  http://127.0.0.1:9/api/generate ...")` in **0.01s**. `host` is in inference_domain's declared
  public_interface.
- **(4) the tree stratum is back.** **325** orient packets have berthed since 2026-09-07, and **0**
  carry "tree stratum unavailable". The last two that did are `orient-20260907T172520` and
  `orient-20260907T172521`.
- **Negative control.** `--control` swaps clause 2's model for `no-such-model:0b`. The same
  instrument reads `RouteRefused` and exits 1, so the script can tell an answer from a refusal.

## Routed, not built here

- **The reply-path hang** (the WRONG INTENT clause, per open-55b0): a verb handler that raises sends no
  reply to its asker (`cairn/tools/base/shim.py:796` → the batch's `refused` list only), so a
  synchronous asker waits out its timeout. Cast as **41f57726a609** ("A verb handler that raises still
  answers its asker").
- **A bare infer defaults to the embedding model.** `InferenceDomainDevice._handle_resolve`
  (`cairn/devices/inference_domain/device.py:113`) reads `body.get("model", "nomic-embed-text")` for
  every kind, so `infer` with no model is refused `RouteRefused ... model='nomic-embed-text'`. That
  refusal is loud and comes back inside 0.04s, so it is not a hang and not this ticket's symptom. It
  is reported to the casting session as its own defect.

## The review record

Akien's standing approval, which open-83ff98f1ef31 extends to concept-pieces: "a) Yes: CC signs and
seals concept-pieces from now on", and "APPROVED THRU PROVED. FASTEST ROUTE TO EVERYTHING PROVED".
