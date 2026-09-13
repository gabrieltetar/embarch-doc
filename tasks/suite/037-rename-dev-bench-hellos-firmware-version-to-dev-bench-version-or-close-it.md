# 037 — Rename `GET /dev-bench/hello`'s `firmware_version` to `dev_bench_version`, or close the question for good

**State:** blocked — leg 108, 2026-09-13. **The announcement window is closed and is no longer what
holds this.** Leg 107 posted it at `ts` `1789326123.058939` and left the task `open` so a successor
would complete the clock rather than restart it; leg 108 read the thread with
`scripts/fleet-read.py --thread 1789326123.058939` at 2026-09-13 ~13:35, found one app-authored
reply and **no objection from the owner**, and the 30 minutes had elapsed. So §4's consent is
satisfied and spent. What remains is the gate, and it is not a leg's to clear — see "Why leg 107
announced it and then did not execute it" below, which is unchanged and still the whole story.
**Unparks when:** the owner produces a native Windows build of `embarch-core`
(`embarch-dev-workflow.md` §4a sync→build→deploy, outstanding as `tasks/core/015`) **and takes this
task in that same sitting** — or says explicitly that the rename may land gated on host checks
alone. Either one is his; neither is a supervisor's to grant.
**Why `blocked` and not `open`:** `open` was right while the clock was running, because a leg could
still have finished it. It is wrong now. Four consecutive legs have re-read this task, re-derived
that they cannot gate it, and left it — `blocked` is what `.claude/leg.md` means by "nothing here
can be done", and it keeps the task visible to the one actor who can act on it instead of offering
it to legs that cannot. **Do not re-announce.** The window is spent; a new one would buy nothing
the first did not already buy.
**Source:** split out of `suite/036` by leg 105, 2026-09-13, when that task's documentation half
landed (`embarch-doc` `6f369d3`, `embarch-api` `72e8b12` + `265c8ff`). **This is the half it could
not take**, because leg 105's announcement window covered documenting the field and this is a
breaking change to a served field in three repos.
**Scope:** suite
**Hardware:** none — an HTTP response field, its client types and its consumers. Nothing reaches a
board. (But see "The old-Core half" — the Core *running* on this machine matters here even though
no board does.)
**Owner:** no
**Announced:** `#embarch-fleet` `ts` `1789326123.058939`, leg 107, 2026-09-13 — the 30-minute
window under `ops.md` §4 **ran and closed with no objection** — leg 108 checked the thread with
`scripts/fleet-read.py --thread 1789326123.058939` at 2026-09-13 ~13:35 and found one app-authored
reply and nothing from `U0AGQGSHM2P`. It names all three repos and the breaking-change half in its
threaded detail, so this task's first `Done when` item is **satisfied**. **Do not re-announce it**,
and do not start a fresh clock: the consent §4 exists to produce has been produced, and it does not
expire because the leg that collected it died. A later reply saying go runs the task immediately; a
cancel drops it to plain `open` with the reply quoted here.

**Why leg 107 announced it and then did not execute it, so the next leg does not rediscover this.**
The window is not the obstacle; the **gate** is. This task's fourth `Done when` item requires a
native Windows build of `embarch-core`, and `.claude/leg.md` requires the same of any leg landing a
change where `embarch-core` is involved. Producing that build is the owner's attended
`embarch-dev-workflow.md` §4a sync→build→deploy sitting, it is outstanding as `core/015`, and an
unattended leg cannot run it. So the rename half of this task **cannot be gated by a leg**, and
landing it ungated would put an un-buildable breaking change on `main`.

**The other branch is not a free way out either.** Closing the task and recording the answer as an
`embarch-core` decision would mean deciding *against* a rename this task argues for, on the
strength of a tolerance problem the task itself already names the fix for (`Option` +
`#[serde(default)]` under `embarch-api` decision 58, plus an explicit decision about what the
reflash gate does when the field is absent, which must not be "treat it as matching"). That is a
real design call and it should be made because someone judged it right, not because the leg that
reached it could not compile the other branch.

**So the honest state is: decided-how, blocked-on-whom.** The next actor to take this needs either
the owner's native build in the same sitting, or the owner's explicit say-so to land the rename
gated on host checks alone. Neither is a leg's to grant.

## The argument, stated here in full

`suite/036`'s file was retired by its own fold, as every completed task is, so this does not point
at it: the long form is in `embarch-doc` commit **`6f369d3`** and in `supervisor-log.md`'s
`suite/036` entry. Everything load-bearing is below.

- **The defect.** `GET /dev-bench/hello` serves the **bench's** build as `firmware_version`. The
  `Study` field it corresponds to is `requires.dev_bench_version`. The identically named
  `requires.firmware_version` on the same struct is the **DUT's**. A caller matching name to name
  pins a DUT requirement to the bench's build, and `embarch-core` only *compares*
  `requires.firmware_version` when a run supplies `flashed_firmware_version` — so in the normal
  no-reflash case the wrong value is accepted and recorded as `Declared`.
- **The precedent.** `embarch-core` decision 47 made exactly this rename on exactly this route
  (`hardware_id` → `self_reported_hardware_id`) for exactly this defect class.
- **The count does not change, so a "third spelling" is not a reason to refuse.** `036` first
  argued that it would; leg 105 corrected that, and its reviewer re-derived the enumeration from
  `embarch-study-designer/src/protocol.rs:67`, `embarch-core/src/study.rs:621`,
  `embarch-study-designer/src/study.rs:280-281` and `src/result.rs:44,49`, confirming `Provenance`
  reuses the same two spellings and adds no third:

| | wire (`HelloAck`) | HTTP (`/dev-bench/hello`) | study (`Requirements`) | distinct |
|---|---|---|---|---|
| today | `firmware_version` | `firmware_version` | `dev_bench_version` | **2** |
| renamed | `firmware_version` | `dev_bench_version` | `dev_bench_version` | **2** |

- **What the rename actually moves is where the crossing happens, and it cuts *for* the rename.**
  Today the crossing is in the caller's hands, at the exact point where the HTTP name collides with
  a field on the same struct holding a different board's version. After the rename the crossing is
  inside Core, where Core composes the response and no caller crosses anything.

## The old-Core half, which is the actual work

**This is not a mechanical field rename.** `embarch-api` decision 58 is the crate-wide rule that
every response field Core may not yet send is `Option<T>` with `#[serde(default)]`; decision 60 is
that rule applied to `dev_bench_hello`'s three identity fields, precisely because decision 47's
rename meant an older Core does not send them. `firmware_version` is a plain `String` on
`embarch-core-client` today (`crates/embarch-core-client/src/client.rs`), and `embarch-api`'s
reflash gate **compares** it (`src/reflash.rs:259-270`).

So a renamed Core plus an un-tolerant client gives a silent empty string where a version check
should be — **a real check turned vacuous, which is worse than the collision this task exists to
fix.** And this is not hypothetical: the Core running on this machine is the Windows service, which
is behind `main` by `core/015`'s outstanding native build, so "an older Core" is the bench.

## Consumers

- **`embarch-core`** — the response type for `GET /dev-bench/hello` (`src/study.rs`'s
  `HelloAckInfo`), and `interfaces/studies.md`'s row, which already documents the collision and
  would document the rename instead.
- **`embarch-api`** — `embarch-core-client`'s response struct and its doc comment,
  `src/reflash.rs`'s use, `src/cli.rs`'s `--json` key, `render_hello_ack`'s human line, the
  `dev_bench_hello` MCP tool's output, and `interfaces/tools-dev-bench.md`.
- **`embarch-ui`** — **two lines only.** It already spells the value `dev_bench` on its own
  surface (`src/study_designer.rs:1581`, `:1645`); what changes is the field it deserializes. No
  rendering changes and no `embarch-ui` doc mentions the field.
- **Neither suite guide mentions it** — checked, leg 105.

## Done when

- [ ] **Announced in `#embarch-fleet` with its own 30-minute window**, naming the three repos and
      the breaking-change half. `suite/036`'s window does not cover this.
- [ ] Either the rename lands across every consumer above **with the old-Core tolerance answered**
      — `Option` + `#[serde(default)]` under decision 58, and an explicit decision about what the
      reflash gate does when the field is absent, which must not be "treat it as matching" — **or**
      this task is closed and the answer recorded as a numbered decision in `embarch-core`, since
      it owns the route.
- [ ] Whichever way it goes, `embarch-study-designer` decision 74 gains a sentence pointing at the
      answer. 74 deliberately left this open and says so; it should not stay open in 74 after it is
      closed here.
- [ ] Gate green in every repo touched, **including a native Windows build where `embarch-core` is
      involved**; `changelog.d/` fragments for each.

## Do not

**Do not rename `HelloAck.firmware_version` on the wire.** `embarch-study-designer` decision 74
rejected that on cost — it is a schema bump that reflashes every bench and redeploys Core in one
sitting — and its reversal condition is the next wire bump taken for another reason. Taking it here
would be reversing a decision one day old for a reason it already weighed.
