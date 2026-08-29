# Orient is a universal qualified verb

**Orient** is the first-move verb: get your bearings on X before acting on X. The
target qualifies it — **orient build**, **orient session**, **orient debug**,
**orient task**. The verb is the pattern; the qualifier carries the distinction.

## The pattern

    orient <target>

One verb, applied to different scopes. The implementation varies — a formalized
machine, a script, a method — but the act is the same: read the territory, surface
what needs attention, establish where you are before you move.

## The inventory

| Qualified name     | Current implementation                              | Current name          | Status        |
|--------------------|-----------------------------------------------------|-----------------------|---------------|
| **orient build**   | `cairn/devices/builder/machines/orient/`             | orient (stage 1 of chart chain) | formalized machine with floor/tree/ceiling |
| **orient session** | `bin/cmd/slate` (session-open hook)                  | slate                 | already says "Orient from MAP.md" on cold start |
| **orient debug**   | `cairn/machines/diagnostic_inspector/` + diagnostic-logging method | diagnostic / diagnose | formalized machine + method pattern |
| **orient task**    | (none — future slot)                                 | —                     | named by the convention, not yet implemented |

## The instrument

`cairn/tools/orient/` — the prebuild scans (device_census, call_sites, repo_truth,
import_map). These are the **measurements** any orientation act can compose.
The instrument is not itself an orientation act — it is what orientation acts use.

## Disambiguation

**Orient** the verb names the act. **Orient** the machine (`cairn/devices/builder/
machines/orient/`) is one instance of that act — orient build. The tool
(`cairn/tools/orient/`) is the instrument, not the act. The three are:

- the **verb** (this convention)
- the **machine** (orient build — one formalized act)
- the **instrument** (the scans any act can call)

When context is ambiguous, the qualifier resolves it: "orient build" is the machine,
"orient session" is the slate, "orient" alone is the verb pattern.

## Provenance

Akien, 2026-08-29: "session open is EXACTLY session orient. i think we just expanded
the use case is all. i think we used DIAGNOSE or something like that for the debug
orient. so we'd change them all to be orient, but all orients would say what was
being oriented."

The build orient was the first to formalize (machine since 2026-08-13, instrument
since 2026-07-27). This convention recognizes the others as the same verb.

## What this does NOT do

- Rename files or components (follow-on tickets)
- Create new orient machines for session/debug/task
- Change CLI dispatch (belongs to valid-verbs-standard-cli-vocabulary)
- Modify the orient machine's or instrument's code or charter

The convention names what exists. Code follows the name.
