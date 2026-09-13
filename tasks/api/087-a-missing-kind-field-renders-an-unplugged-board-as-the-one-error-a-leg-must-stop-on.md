# 087 — A missing `kind` field renders an unplugged board as the one error a leg is told to stop on

**State:** claimed by agent/api/087-missing-kind-renders-as-mismatch, 2026-09-13 17:47
**Source:** `inbox/api-validate-renders-an-unplugged-board-as-a-topology-mismatch-against-an-old-core.md`,
observed live by the leg of 2026-09-13 17:05 running `validate` with `role: dev-bench` as the bench
pre-check `.claude/leg.md` requires. Filed by the leg of 2026-09-13 17:5x.
**Scope:** api
**Hardware:** none. The observed instance needed a running Core and an unplugged probe, but nothing
here needs either: the rendering decision, the code change and the test are all host-side. **The
redeploy of the live Windows service Core is explicitly the owner's and is NOT part of this task** —
it closes the observed instance without closing the class, which is the class this task is about.
**Owner:** no

## What was observed, verbatim

```
topology mismatch for role 'dev-bench' (probe 001057729826, chip 'nRF54L15'): probe
'001057729826' enrolled as role 'dev-bench' is not currently attached (recorded hardware_id
6fcddc36cb781b71, live None) — fix it at http://127.0.0.1:4890/#topology
```

The board was simply unplugged. Both halves of the fix are already landed on `main` — `tools.rs`
branches on `mismatch.is_not_attached()` first and suppresses the `fix_it_url`, and `embarch-core`
emits `kind`. The message above is the **second** branch's format string, so the MCP binary is
current and `is_not_attached()` returned `false`. `client.rs`'s `is_not_attached()` is
`self.kind == "not_attached"`, and `kind` carries
`#[serde(default = "default_mismatch_kind")]`. The live Core is older than the field, so `kind`
defaulted to `"mismatch"` and an unplugged board rendered as a genuine one.

## Why this is not a cosmetic wording bug

`.claude/leg.md` gives a supervisor two **opposite** instructions keyed on exactly this distinction:

- **not attached** → leave the task `open`, say it once, carry on. A board coming back is normal.
- **topology mismatch** → **stop**, never re-enrol, name both IDs, **alert the owner**.

So against a Core older than `kind`, every unplugged bench role currently renders as the
stop-and-alert case, complete with a `fix_it_url` inviting the re-enrolment that the enrolment
safety property exists to prevent (`embarch-topology` decision 20's failure: *"a bench that flashed,
booted, ran, and timed out"*). The observing leg read past it only because the `reason` prose says
*"is not currently attached"* and `live None` is not an ID — **which is the reverse of what
`client.rs`'s own test asserts is the right thing to read** (*"`is_not_attached()` reads the field,
not `reason`'s wording"*). That inversion is the finding.

## Read decision 71 first, and engage with its argument rather than around it

**This is not an oversight; it is a reasoned choice you are revisiting.** `embarch-api` decision 71
(currently in `decisions/surface.md`) chose the `"mismatch"` default deliberately, so a Core older
than `embarch-core` decision 59 — which only ever sent that shape for a genuine mismatch — still
parses. Its last paragraph is the load-bearing one: neither wrapper may infer the condition from
`live_hardware_id.is_none()` locally, because *"re-deriving it client-side would silently drift from
Core's own rule the moment Core's criteria for `not_attached` change."* Any answer you propose has
to survive that sentence, and **"just look at `live_hardware_id`" does not** — do not propose it.

Note the distinction that does survive it: reasoning about the **absence of the field** is a fact
about *which Core answered*, not an inference about *which condition holds*. Decision 71's rule
forbids the second. Whether it should also forbid the first is the question.

`embarch-api` decision 58 already settles the structurally identical case for the sibling field:
`validated_at_utc_ms: null` is documented to mean *"this Core did not report a live-check time, not
that the check happened at an unknown time."* There is no equivalent for a missing `kind`, and the
missing one falls to the more alarming of the two readings.

## The three candidates from the drop

Pick one, write it down as a decision, and say in the decision body why the other two lose:

1. **Treat a missing `kind` as "this Core cannot tell me"** — a third rendering that says so plainly
   and **suppresses the `fix_it_url`**, on the ground that offering a fix-it link on an answer the
   client could not classify invites the one destructive action.
2. **Keep the current fallback but say so in the message**, naming the Core version that added
   `kind`, so a reader knows the classification is unavailable rather than negative.
3. **Leave it**, and record that the discrimination is only as good as the deployed Core, with the
   deploy as the fix. Cheapest; makes the hazard known rather than surprising.

Serde's `default` cannot distinguish "absent" from "explicitly `mismatch`" — if you take 1 or 2,
`kind` has to become `Option<String>` (or gain a sentinel) and every existing reader of it updated
in step. Say in the decision what that costs, because it is the real price of 1 and 2 and the real
argument for 3.

## Doc routing, and the split that has to happen first

`embarch-api/decisions/surface.md` is **11,258/12,288 B — 1,030 B left, 91.6%, in reserve**. Its
compaction task `tasks/api/069` is `blocked` on `In flux: yes`, and a blocked compaction task parks
the *pass*, not the reserve (`.claude/leg.md`, `DOC-COMPACTION.md` §2) — so **you compact it as part
of this unit**, and the cheapest honest way is the mission split `api/069` names in its own body:

> this file's own natural seam: "JSON shape and versioning" (16, 24, 50) vs "how a failure is
> reported and attributed" (57, 67, 71)

Move decisions **57, 67 and 71 verbatim** into a new `embarch-api/decisions/failure-reporting.md`,
byte-for-byte — **a verbatim split restates nothing, which is why `In flux: yes` cannot forbid
one.** Then file your new decision there, where there is room, rather than into 1,030 B.

Three things the split must not lose, from `api/069`'s **Must not delete** list:

- Decision 50's argument for why `error_kind` was *retired rather than built* — the
  "Core-status-code-is-coarser-than-a-real-code-enum" point. **This one stays in `surface.md`** (50
  is a shape decision); check it survives the edit intact.
- Decision 67's scope note about `tool-wrapping.md`'s own headroom, which is the reason that entry
  sits where it does. It **moves with 67**, and after the move that note is about a *different*
  file's headroom than the one it is now in — read it and say in the fold whether it still parses.
- Decision 71's three concrete facts: `kind` defaults to `"mismatch"` for an older Core, `503` is
  dispatched through the same parse `409` already used, and both `tools.rs` and `cli.rs` call
  `is_not_attached()` rather than re-deriving from `live_hardware_id.is_none()`. If your chosen
  option changes the first of those, **amend decision 71 in place with a dated amendment** — do not
  delete or silently rewrite it, because reverting any of the three is the regression `api/068`
  exists to prevent.

**`tasks/doc/052` applies:** a verbatim split silently drops the per-decision size pin of every
decision it moves. Check `decision-size-baseline.json` for pins on 57, 67 and 71 before you move
them, and carry any that exist.

Update `tasks/api/069` to reflect what the split paid: delete `embarch-api/decisions/surface.md`
from its `Compacts:` line if the file is out of reserve, and say so in the body — **delete the
entry, never strike it through**, or the size gate stops recognising the line.

## Reserve, for planning

`embarch-api/decisions/surface.md` 1,030 B left (handled above). `embarch-api/spec.md`
9,102/10,240 B, **1,138 B left**, filed against `tasks/api/083` (`blocked`). If your work pushes
`spec.md` further into reserve or leaves it there unfiled, file
`tasks/api/<next>-compact-api.md` in the same commit — **your own scope**, never `tasks/doc/`.

## Done when

- [ ] One of the three is chosen, implemented, and written as a numbered `embarch-api` decision that
      says why the other two lose and what the `Option<String>` cost is.
- [ ] `decisions/surface.md` is out of its reserve band via a **verbatim** mission split, with all
      three Must-not-delete items accounted for and `tasks/api/069` updated.
- [ ] A unit test covers a `TopologyMismatchError` with **no `kind` field at all** — not just
      `kind: "not_attached"` and `kind: "mismatch"`. That absent-field case is the one nothing tests
      today and the one that produced the observed message.
- [ ] If the rendering changed, `client.rs`'s test comment (*"reads the field, not `reason`'s
      wording"*) is re-read and corrected if the split made it false.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md` updated, `changelog.d/` fragment dropped.
