# 036 — No MCP tool reaches `GET /dev-bench/hello`, the one endpoint that returns the identity cross-check

**State:** blocked — **the work is done and pushed; it was refused at the merge, by me, on a judgement the mechanical gate cannot make.** See "Why this was refused" below. **Unparked by:** the three new `HelloAckResponse` fields being made `Option<String>` with `#[serde(default)]`, and the MCP tool and its description saying in words that this Core did not report them, per `embarch-api` decision 58.
**Branches, both pushed and both green on every mechanical check:**
`agent/api/036-dev-bench-hello-tool` in `embarch-api` and `embarch-doc`. **Do not
re-dispatch from scratch** — rebase these and amend them; the split of
`decisions/surface.md` alone is most of the unit and it is correct.
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

## Why this was refused at the merge — leg 045

**The unit contradicts `embarch-api` decision 58, which was written an hour
earlier, in the same file, by the leg immediately before this one.**

Decision 58 (`decisions/core-link.md`, from `tasks/api/046`) says: *every response
field this crate deserializes that Core may not yet send is `Option<T>` with
`#[serde(default)]`.* It was written **because `api/045` had just added
`ValidateResponse::validated_at_utc_ms` as a bare required field**, and every
`validate` call against a Core that predated it then failed at deserialization —
looking like a broken client rather than a version skew.

This unit adds three bare required `String` fields to `HelloAckResponse`:

    self_reported_hardware_id · link_identity · probe_hardware_id

**`self_reported_hardware_id` is the live problem.** `embarch-core` decision 47
(`tasks/core/020`) renamed this field from `hardware_id` **today, at 15:34**
(`embarch-core` `bd9adbc`). An `embarch-core` older than that commit serves
`hardware_id` and does not serve `self_reported_hardware_id` at all — so against
it, `serde` fails on a missing required field and **every call to the new tool
returns a deserialization error rather than the identity cross-check.**

**This is not hypothetical and it is not a future risk.** The live Core on this
machine is a separately-built Windows service, and **the native Windows build for
`core/020` has never been run** — it is an outstanding hardware debt in the
supervisor log. So the deployed Core almost certainly still serves the old
spelling, and this tool would have failed on its first real call, on the one
route whose entire purpose is to answer *is the board on the link the board the
probe verified?* Decision 58 names this exact configuration in its own reasoning:
the deployed Core and this crate are known not to move together.

**Nothing mechanical could have caught this.** `cargo test` passes because the
round-trip test constructs the JSON it then parses. `check-docs.py` passes. Both
ownership checks pass. `check-decision-refs.py` passes. The contradiction is
between a new struct and a decision in a different file, and only reading the
diff against the decisions finds it.

**What the fix looks like, and why it is not a one-line change.** The three fields
become `Option<String>` with `#[serde(default)]`. But `None` then has to be
rendered, and **the whole point of this task is that an absent or unreported
identity must not read as a pass** — so the MCP tool, its description and
decision 59 all have to distinguish *"this Core did not report it"* from
*"not-reported"* (a real bench answer) from *"undeclared"* (also a real bench
answer, and today's answer for every chip). Three different absences that a
careless rendering collapses into one. That is a design question, which is why
this went back to the queue rather than being patched at the merge.

**What is right about the unit and must not be thrown away.** The split of
`decisions/surface.md` was verified verbatim and is exactly what
`DOC-COMPACTION.md` §2's split-first rule asks for; the general decisions
(16/24/50/57) stayed and the per-tool wrapping decisions (23/29/34/35/41/47/52)
moved byte-for-byte into a new `decisions/tool-wrapping.md`. `link_identity` is
correctly kept as its own string and never folded into `compatible`. The two
downcastable error types for `409`/`502` are right. **Rebase and amend; do not
start over.**

**One deferred follow-up.** The worker filed an `inbox/` drop noting that
`embarch-umbrella/decisions/schema-skew.md` cites decision 52 at its old
`surface.md` path. **That drop is only true once this unit lands** — the split
has not landed, so the citation is still correct today, and filing it now would
create a task that is wrong until something else happens. It is left in the
worker's worktree at
`/home/gabriel/Github/embarch/.worktrees/embarch-doc/036-dev-bench-hello-tool/inbox/umbrella-schema-skew-cites-a-moved-api-decision-path.md`.
**Whoever lands this unit files it in the same fold.**

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
