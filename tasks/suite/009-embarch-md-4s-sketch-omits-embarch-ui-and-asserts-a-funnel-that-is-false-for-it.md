# 009 — `embarch.md` §4 — the suite's only layering picture — has no node for `embarch-ui` or `embarch-core-client`, and its stated invariant is false for the UI

**State:** claimed (leg 082) — announced in #embarch-fleet at 02:05:20 MDT, `ts 1789113920.427309`;
**window closed 02:35:20 with no objection in the thread and none in the channel**, so it runs.
**Source:** suite review pass 2026-09-06, dimensions 4 and 3 (two hunters, one finding). Doc claim design-only; the code half code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch.md` §4's sketch draws Claude Code over MCP, *"human, direct: `embarch-api <subcommand>
...`"*, `embarch-api` → `embarch-core` → hardware, the dev-bench link, the outpost bypass, and
umbrella off to the side. **`embarch-ui` appears nowhere in it**, and neither does
`embarch-core-client`, the crate both HTTP clients are.

`embarch-ui` is a shipped six-tab binary and **Core's second HTTP+Bearer client, a peer of
`embarch-api` rather than below it**: `embarch-ui/Cargo.toml` carries
`embarch-core-client = { path = "../embarch-api/crates/embarch-core-client" }`, no `reqwest`, no
`probe-rs`, and `embarch-ui/spec.md:25-45` lists 15 Core endpoints it calls directly.

So the paragraph under the sketch — *"**Everything hardware-facing still funnels through the API to
Core to the probe**"* — is false for it. `embarch-ui/spec.md`'s own Invariants get it right:
*"over HTTP+Bearer **to Core**"*.

§3's table does list `embarch-ui`, so the omission is the picture's alone. And
`suite/user-guide.md` mentions the UI zero times while `suite/studies-guide.md` treats the
Topology, Study Designer and Trace tabs as mandatory — the *"a rule that exists in some of the
places it applies"* shape (`embarch-decision-reversals.md` rows 27, 97).

Candidate direction: §4 gains the UI as a second client of Core, and names the shared client crate
on the edge both use. The invariant sentence becomes *through Core to the probe*, which is the
property that is actually true and actually load-bearing.

## Why now

This is the one place the suite writes down its dependency direction, and it is handed to every
reviewer and every hunter as the measuring stick — **this run included**. A reader deciding where a
new capability belongs is measuring against a picture with a shipped binary missing from it, and
because the sketch shows one human path and it is the CLI, the parity principle reads as satisfied
by the CLI alone. That is precisely why the
`api-surface-cores-signal-and-dev-bench-link-writers` drop in this batch went unnoticed.
`check-staleness.py` watches status tables and `collect-open-questions.py` watches `open.md`
bullets; neither reads a prose architecture sketch.

## Done when

- [ ] `embarch.md` §4's sketch shows every process a human or an agent enters the suite through.
- [ ] The funnel sentence is true of every client in the sketch.
- [ ] `embarch.md` is not pushed into reserve by the change (it is not in reserve now).
- [ ] Gate green.

**Note:** `tasks/suite/004` (doc-size reserve) and `tasks/suite/008` (§5's rustfmt bullet) are the
only queued `embarch.md` items and neither touches §4.
