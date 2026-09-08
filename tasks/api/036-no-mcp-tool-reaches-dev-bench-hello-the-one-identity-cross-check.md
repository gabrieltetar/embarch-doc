# 036 — No MCP tool reaches `GET /dev-bench/hello`, the one endpoint that returns the identity cross-check

**State:** claimed (leg 045)
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

## Supervisor direction (leg 045)

**Read Core's serialized struct for the wire shape; do not mirror the topology
crate's type.** `embarch-core` is what actually serves `GET /dev-bench/hello`, and
a mirror built from the upstream crate's shape rather than from Core's response
body is a struct that compiles, passes every test you write for it, and fails
against the real Core. Find `HelloAckInfo` as Core serializes it and mirror that.
An earlier unit in this chain (`api/045`) hit exactly this and only avoided it
because the shape was written into the task file.

**`link_identity` is the whole point of the tool and the field most likely to be
lost.** A `not-reported` or `undeclared` **is not a pass**. Do not collapse it to
a boolean, do not flatten it into a summary string, and do not let a `None`
render as anything a reader could mistake for "verified". If you find yourself
choosing a representation, choose the one that makes an absent or unreported
identity impossible to read as a confirmation.

**Distinguish the two failure codes in the tool's error text**, not just in the
HTTP layer: `409` means a study is in flight and the route refused rather than
raced, `502` means the handshake itself failed. Those send an operator to
completely different places. The description must also say the call opens and
closes the bench link, because an agent that does not know that will call it
during a study and read the `409` as a bug.

**Reserve line for `api`, and this one needs a decision from you before you write
anything.** `embarch-api/decisions/surface.md` is **11,873 / 12,288 B — 415 bytes**
— and its compaction task `tasks/api/043` is parked `In flux: yes` **for exactly
the reason that applies to you**: it is the tool-and-CLI surface file that grows
every time a tool is added, and you are adding a tool. That park cannot mean
"nobody may ever write here", or the file would grow until it hit the wall
mid-unit. `DOC-COMPACTION.md` §2's split-first rule applies — **a verbatim split
restates nothing, so `In flux: yes` cannot forbid one.** Split `surface.md` along
a topic seam, moving entries byte-for-byte without rewording any of them, carry
`api/043`'s `Must not delete:` list forward verbatim, tick only that file's item,
and leave the task blocked for whatever it still covers. `decisions.md`'s index
table must name the new file, its decision numbers and both files' sizes, and
`check-decision-refs.py` must resolve every number.

Also in reserve for this sub-project: `open.md` **386 bytes** (parked on
`tasks/api/026`, whose flux is the SSE event stream — a different seam from
anything you are touching, so do not disturb it) and `spec.md` 1,153 bytes.
If your work spends a reserve nothing has filed against, file
`tasks/api/<NNN>-compact-api.md` in the same commit per `tasks/README.md`.

**Decision numbers are global across `decisions/*.md`, not per file.** Take the
next number from the whole directory's maximum.

**Out of scope, and both are traps:** `tasks/api/034` is an open task about
`docs/tools.md` already omitting `reset_dev_bench` — do not fix it here, but do
not re-introduce its shape either, so add your entry in whatever form that file
should have had. `tasks/api/044` changes the `hardware_id` spelling in this same
client; leave it alone. Two wire-shape changes in one diff is how a revert stops
being possible.

**Why this one matters beyond its own Done-when:** `tasks/core/020` carries a
hardware-verification debt that is gated on this task rather than on a board, so
landing this is what makes that debt payable.

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
