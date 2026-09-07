# 036 — No MCP tool reaches `GET /dev-bench/hello`, the one endpoint that returns the identity cross-check

**State:** open
**Source:** hit by the supervisor running `tasks/topology/002`, 2026-09-06
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`GET /dev-bench/hello` runs the dev-bench `Hello`/`HelloAck` handshake and closes
the link — no study, no flash — and returns `HelloAckInfo`, which is **the only
place in the suite that serves the JTAG-read identity, the board's self-reported
identity and the relation between them as data**:

```
hardware_id (self-reported) · probe_hardware_id (JTAG) · link_identity
firmware_version · schema_version · compatible
```

`embarch-api` exposes no MCP tool for it. The surface has `status`, `validate`,
`alerts`, `serial_log`, `reset_dev_bench`, the build/flash pair and the study
family — and nothing that reaches this route. So an agent asking *is the board on
the link the board the probe verified?* can get to neither half of the answer,
while a human with `curl` and the token gets both.

`topology/002` needed exactly this and had to read the comparison out of Core's
own rotating log file on the host instead — which worked, and is not a surface
anything should depend on.

## Why now

Three separate things point at this route and none can call it:

- `embarch-umbrella/decisions/doctor.md` names it as check 13's data source, and
  `embarch-umbrella/open.md` still carries doctor checks that are dark.
- `embarch-topology` decision 21's Nordic arm is only ever exercised here, and
  its confirmation had to be quoted from a log line.
- `tasks/umbrella/027` is a bench task that will want the same three fields.

It is a read-only route that takes a lock it already respects — it returns `409`
rather than racing a study — so the tool is a thin wrapper, not new behaviour.

## Done when

- [ ] An MCP tool serves `GET /dev-bench/hello`, returning `HelloAckInfo`
      unflattened — `link_identity` in particular must survive, since a
      `not-reported`/`undeclared` is **not a pass** and a tool that collapses it
      to a boolean would make it look like one.
- [ ] Its `409` (a study is in flight) and `502` (handshake failed) are distinct
      in the tool's error text, and the description says the call opens and
      closes the bench link.
- [ ] `docs/tools.md` lists it. Note `tasks/api/034` is an open task about that
      file already omitting `reset_dev_bench`; do not fix that one here, but do
      not re-introduce its shape.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
