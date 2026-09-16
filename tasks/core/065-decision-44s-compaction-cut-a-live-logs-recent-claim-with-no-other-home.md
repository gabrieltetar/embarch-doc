# 065 — decision 44's compaction cut a live `/logs/recent` claim that is now documented nowhere

**State:** open
**Source:** `embarch-reviewer` on `core/064` (merge `74f3708` in `embarch-doc`), filed to `inbox/` as
`core-decision-44-residue-live-route-claim.md` and drained into the queue by leg 118. Re-checked at
drain: the `Hardware:` claim is correct — this is doc prose about behaviour the reviewer already
verified against `src/logs.rs`, and confirming it needs no board.
**Scope:** core
**Hardware:** none — doc prose only. No board, no probe, no live Core, no route called.
**Owner:** no

## What

`core/064` compacted `embarch-core/decisions/logging.md#44` — a decision retired with the
`GET /logs/stream` route it documents — and cut this sentence along with the rest of the
anchor/self-correction paragraph:

> **`read_recent`/`tail_lines` are unchanged and still return a trailing partial as a line** —
> correct for "show me the tail as it stands now," and `embarch-ui`'s `diff_new_lines` already
> has a documented fallback for a window whose last entry changes under it.

The commit's justification for cutting that paragraph was that it is "provenance for a route no live
code can hit anymore." **That is true of the rest of the paragraph and false of this sentence.**
`read_recent`/`tail_lines` back **`/logs/recent`**, which is `embarch-core`'s only live log-reading
route today.

The reviewer then established the part that makes this a task rather than an opinion:

- The claim is **still true of the code** — `src/logs.rs`'s `tail_lines` runs `.lines()` over
  `read_to_string`'s output, so a read landing inside a mid-write line yields an unterminated last
  line.
- The claim is **now stated nowhere else in the repo.** `embarch-core/interfaces/logs.md`'s
  `/logs/recent` row omits it, `embarch-core/spec.md:58`'s `logs.rs` row omits it, and
  `embarch-ui/decisions/debug-tab.md`#13 — the poll/diff consumer of `/logs/recent` — omits
  `diff_new_lines`'s fallback too. `diff_new_lines` does not appear anywhere in the doc repo outside
  the deleted sentence and `core/064`'s own quote of it.

This contradicts no locked decision. It is the **residue** case: a cut hunk carrying a statement
about live behaviour, filed under a justification that only covered retired behaviour.

## Where it should go

Pick one and say why — this is the judgement the task exists for, and it is why leg 118 did not fix
it inline in the fold:

- **`embarch-core/decisions/logging.md` decision 16 or 29**, whichever already covers
  `/logs/recent`'s front end. Keeps the fact with the decision that owns the route.
- **`embarch-core/interfaces/logs.md`'s `/logs/recent` row.** Keeps it where a caller reads before
  writing a consumer, which is the audience that gets it wrong.

Either way the `embarch-ui` half — that `diff_new_lines` has an accepted fallback for a window whose
last entry changes under it — needs a home too, and **`embarch-ui` is not this worker's to write.**
If the right home for that half is `embarch-ui/decisions/debug-tab.md`#13, file it to
`inbox/` for a `ui` worker rather than reaching across the ownership map.

## Why now

A future `/logs/recent` consumer, or a Core maintainer changing `tail_lines`, has lost the one place
that said a trailing partial line is expected **and why it is acceptable** ("correct for 'show me the
tail as it stands now'"). That reasoning is what stops someone treating it as a bug and
"fixing" it into a behaviour `embarch-ui` is not expecting.

## Watch for

- **Restate, do not un-retire.** Decision 44 stays retired and stays compacted; `core/064`'s cut was
  right about everything except this one sentence's classification.
- **This is a class, not an incident.** `DOC-COMPACTION-PASS.md`'s hot/cold test asks what a reader
  needs to work on this component today, and a *retired* entry reads as uniformly cold — which is
  exactly how a live claim inside one gets cut. Whether that test needs a clause about retired
  entries is an `inbox/` finding for the owner, not something to change here (`DOC-COMPACTION.md` is
  owner-reserved).

## Done when

- [ ] The trailing-partial-line fact about `read_recent`/`tail_lines`, **with its "why it is
      acceptable" clause**, is stated in a live `embarch-core` doc.
- [ ] The `embarch-ui` `diff_new_lines` half is either stated in an `embarch-core`-owned doc that can
      legitimately mention it, or dropped to `inbox/` for a `ui` worker — not silently left out.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
