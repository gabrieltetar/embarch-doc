# 036 — No MCP tool reaches `GET /dev-bench/hello`, the one endpoint that returns the identity cross-check

**State:** done — reworked per "The rendering call, settled — leg 046"; see "Closed" at the bottom.
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

## The rendering call, settled — leg 046

**This is the design decision the previous leg deferred, and it is now made. It
is not a suggestion; implement it as written, and record it as the decision this
unit files.**

**1. The three fields become `Option<String>` with `#[serde(default)]`**, per
`embarch-api` decision 58. No other field of `HelloAckResponse` changes in this
unit.

**2. The tool never computes an identity verdict of its own.** Core already
serves `link_identity` — its own answer to the cross-check. Re-deriving a verdict
in the client from the two hardware ids would be this crate asserting a semantic
it did not measure, which is the exact failure `embarch-topology` decision 20
paid for. **Surface Core's answer; do not replace it.**

**3. There are two rendering states and they must not be reachable from each
other.**

- **Complete response** — all three fields present. Render each under its own
  label, **verbatim, as the bytes Core sent**. `not-reported` and `undeclared`
  reach the reader unaltered and unmapped, because they are the board's own
  answers and are real bench results. Add one sentence to the rendered output
  saying that `not-reported` and `undeclared` are answers, not confirmations.
- **Incomplete response** — *any* of the three is `None`. The output **leads**
  with a line saying the identity cross-check is **unavailable**, and names which
  field or fields were absent. It must say, in words, that this Core did not send
  them — pointing at `embarch-core` decision 47's rename of
  `hardware_id` → `self_reported_hardware_id` as the known cause, and at
  `embarch-api` decision 58 as why the client tolerates it rather than failing.
  **The remaining present fields may still be rendered, but never above that
  line and never in a shape that reads as a cross-check.**

**4. `None` has exactly one rendering and it is a sentence, not a token.** Never
an empty string, never `null`, never `-`, never `unknown`, and — the one that
matters — **never `not-reported`**, which is a different fact with a different
cause: `not-reported` is *the board* declining to state an identity, `None` is
*this Core* not having the field at all. Collapsing those two is precisely the
defect this task was blocked for, one level up.

**5. Why "unavailable" rather than a failure.** Decision 58 exists so an older
Core degrades instead of erroring. A tool that returned an error here would be
the `api/045` behaviour decision 58 was written to end; a tool that rendered a
partial answer as a pass would be worse than either. Unavailable is the third
thing, and it is the honest one.

**Record this as a numbered decision** in the same file the tool's other
wrapping decisions live in after your split, with the reasoning above in your own
words, and cite `embarch-api` 58 and `embarch-core` 47 by number.

**Also, in the same fold:** the `inbox/` drop your predecessor left about
`embarch-umbrella/decisions/schema-skew.md` citing decision 52 at its old
`surface.md` path has been rescued to
`/home/gabriel/Github/embarch/embarch-doc/inbox/umbrella-schema-skew-cites-a-moved-api-decision-path.md`
by leg 046 and is the supervisor's to file. **You do not need to re-file it** —
do not write into `inbox/` for this, and do not touch `embarch-umbrella`.

## Done when

- [x] The three new `HelloAckResponse` fields are `Option<String>` with
      `#[serde(default)]`, and the tool renders them per "The rendering call,
      settled — leg 046" above — including the `None`-is-not-`not-reported`
      rule, which is the whole reason this unit was refused. — `client.rs`'s
      `render_hello_ack` implements the two-state (complete/unavailable)
      rendering; recorded as decision 60 in `decisions/tool-wrapping.md`.
- [x] A test exercises the **incomplete** response — a JSON body with
      `self_reported_hardware_id` absent entirely — and asserts the tool
      deserializes it and renders the unavailable line. A round-trip test over a
      body you construct with every field present does not exercise this. —
      `an_incomplete_response_renders_the_unavailable_line_first` (and
      `an_older_core_missing_all_three_identity_fields_still_deserializes`).
- [x] An MCP tool serves `GET /dev-bench/hello`, returning `HelloAckInfo`
      unflattened — `link_identity` in particular must survive, since a
      `not-reported`/`undeclared` is **not a pass** and a tool that collapses it
      to a boolean would make it look like one.
- [x] Its `409` (a study is in flight) and `502` (handshake failed) are distinct
      in the tool's error text, and the description says the call opens and
      closes the bench link.
- [x] `docs/tools.md` lists it. Note `tasks/api/034` is an open task about that
      file already omitting `reset_dev_bench`; do not fix that one here, but do
      not re-introduce its shape. — `interfaces/tools.md`'s row updated for the
      complete/unavailable rendering, `reset_dev_bench` left as `034` found it.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
      — `decisions.md`/`decisions/tool-wrapping.md` updated (decision 60);
      `spec.md`/`open.md` deliberately left untouched, same as the original
      unit, both separately parked on `tasks/api/026`'s unrelated SSE flux and
      nothing either states became false here.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Closed — `api/036` rework, 2026-09-07

Rebased both branches onto `main` (taking `main`'s rewritten copy of this task
file, per the dispatch). Fixed the refused defect: the three identity fields on
`HelloAckResponse` are now `Option<String>` with `#[serde(default)]`
(`embarch-api` decision 58), and `dev_bench_hello` renders the settled two-state
design — complete (all three present, rendered verbatim with a
not-a-confirmation note) vs. unavailable (any `None`, leading line naming which
field(s) this Core did not send, citing `embarch-core` 47 and `embarch-api` 58,
remaining fields rendered only below that line). Recorded as decision 60 in
`decisions/tool-wrapping.md`. That file crossed its own 12,288 B cap's reserve
line at 12,222 B in the same commit that added decision 60 — filed
`tasks/api/047-compact-api.md` (`In flux: yes`, same reason `api/043` gave for
this exact file) and ticked `api/043`'s own now-resolved item (`surface.md`
itself is clear at 5.5 KB). Left everything the refusal called correct
untouched: the verbatim `surface.md`→`tool-wrapping.md` split, `link_identity`
as its own string, the two downcastable error types. Did not re-file the
`embarch-umbrella/decisions/schema-skew.md` inbox note (leg 046 already rescued
it) and did not touch `embarch-umbrella`. Gate green in both repos
(`cargo build`/`test`/`clippy --all-targets -- -D warnings`,
`check-docs.py`, `check-client-names.py`, `check-ownership.py` both repos,
`check-decision-refs.py`).
