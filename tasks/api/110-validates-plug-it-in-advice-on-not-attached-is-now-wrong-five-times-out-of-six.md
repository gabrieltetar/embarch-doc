# 110 — `validate`'s "plug it in" advice on `kind: "not_attached"` is now wrong five times out of six

**State:** claimed — leg 138 unit 2, 2026-09-17, `agent/api/110-not-attached-advice`.

**Supervisor dispatch note — doc-size reserve for `api`.** Two files to plan around rather than
discover: `embarch-api/spec.md` **9,089/10,240 B (1,151 B left)**, in reserve and filed against the
blocked `tasks/api/083-compact-api.md`; and `embarch-api/decisions/client-crate.md`
**10,947/12,288 B (1,341 B left)**, not yet filed. If your work pushes a file into the reserve, or
leaves one there that nothing has filed, file `tasks/api/<NNN>-compact-api.md` in the same commit
(`tasks/README.md` has the shape) — recording the debt, not paying it.

**Second supervisor note — this is a wording question, so say what you chose.** There are at least
three defensible answers and I am not leaning: match Core's `"probe unavailable"` exactly; keep
`embarch-api`'s own voice but drop the "plug it in" imperative and relay `reason`; or keep "not
attached" and qualify it. Pick one on its merits and record the reasoning where an `embarch-api`
decision belongs. I say this explicitly because two units in a row this morning found the
supervisor's dispatch note had leaned one way and the worker was right to go the other.

**Filed by:** leg 137, 2026-09-17, from
`inbox/api-validate-not-attached-plug-it-in-is-now-wrong-for-five-of-six-causes.md`, written by the
`core/077` worker as it landed decision 59's second amendment. Filed verbatim except for this
header and the note below. I re-checked the `Hardware: none` claim and it holds: two format strings
and the prose around them, no board.

**Supervisor note — `embarch-core` has already moved, so read `main`, not a branch.** `core/077`
landed (code `6905c62`, doc `2c14f34`) and with it Core's own plain-text lead changed from
`"probe not attached for role …"` to `"probe unavailable for role …"` in `describe_topology_error`
and `describe_gate_error`. **So the suite currently says two different things about the same
condition**: Core says "unavailable", `embarch-api` says "not attached" and then adds "plug it in".
Matching Core's wording is the obvious move but it is not the only one — say which you chose and
why. **`kind`'s wire value is untouched and stays `"not_attached"`; do not change it**, and do not
reach into `embarch-core`.
**Source:** `embarch-core` decision 59's second amendment (`decisions/surfaces.md`,
landed by `tasks/core/077`), reading `embarch-api/src/tools.rs`'s `validate` tool
(around line 992) and `embarch-api/src/cli.rs`'s `validate` command (around line
827).
**Scope:** api
**Hardware:** none — a code-reading and prose-editing question, no board needed.
**Owner:** no

## What

Both `embarch-api`'s MCP `validate` tool and its `validate` CLI command handle
`TopologyMismatchError::is_not_attached()` by formatting:

```
"probe not attached for role '{}' (probe {}, chip '{}'): {} (recorded \
 hardware_id {}) — plug it in; this is not a topology mismatch"
```

That fixed `"— plug it in; this is not a topology mismatch"` suffix was accurate
when the only reachable cause of `kind: "not_attached"` was the enrolled probe
missing from `probe-rs`'s own device list. As of `embarch-topology` decision 34
(`topology/058`, landed 2026-09-17) and `embarch-core`'s own decision not to add
a third `kind` for it (decision 59's second amendment, `tasks/core/077`),
`"not_attached"` now also covers five more causes, all with `live_hardware_id:
None` and none fixed by plugging anything in: the probe was found but its
`.open()` failed (another process holding it, permission denied, a half-wedged
debug probe), its target-power check failed (board genuinely unpowered),
`.attach()` failed, core-select failed, or the hardware-ID read itself failed.
`mismatch.reason` already carries the specific, correct instruction for each of
these — `embarch-api` has it in hand and formats it into the message already —
but then appends its own generic "plug it in" advice on top, which is simply
false for five of the six now-reachable causes.

This needs no new `kind` value and no wire change: `embarch-core` deliberately
kept the classifier two-valued (weighing the cost of a third `kind` reaching
`embarch-api`/`embarch-ui`/the user guide against the fact that no consumer
today branches structurally on which of the six causes fired) and recorded that
`reason` is the only place the distinction lives. The fix here is local:
`embarch-api` should stop asserting "plug it in" as if it always applies, and
either drop the suffix (letting `reason`'s own already-included fix-it text
stand alone) or replace it with something true for every cause (e.g. "check the
probe's own USB connection and any process that might be holding it open").

## Why now

`tasks/core/077` read `embarch-topology`'s five newly-`raise`-routed failure
`reason` strings and `embarch-core`'s `kind` classifier together, decided
collapsing them into `"not_attached"` was the right call for `embarch-core`
itself, and in doing so noticed this specific downstream consequence in
`embarch-api`'s own hardcoded text — real, but out of `embarch-core`'s
ownership row to fix.

## Done when

- [ ] `embarch-api/src/tools.rs`'s `validate` tool and `embarch-api/src/cli.rs`'s
      `validate` command no longer claim "plug it in" (or an equivalent
      single-cause instruction) for every `kind: "not_attached"` result.
- [ ] Whatever replaces it is true for all six reachable causes (absent, stuck
      opening, unpowered, attach failure, core-select failure, hardware-ID-read
      failure) — trusting `reason`'s own text rather than re-asserting a
      narrower claim on top of it.
- [ ] Existing tests around these two call sites updated to match; any new
      test the fix warrants added.
- [ ] Gate green in `embarch-api`.
