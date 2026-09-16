# 065 — decision 44's compaction cut a live `/logs/recent` claim that is now documented nowhere

**State:** done
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

**Decision (leg 065's worker):** `embarch-core/interfaces/logs.md`'s `/logs/recent` row. Decision
16/29 is titled around "one implementation, three front ends" and never mentions tail/partial-line
behaviour at all — folding this fact in there would be attaching it to a decision whose own text does
not cover it sentence by sentence, exactly the failure this leg's dispatch note calls out. The
interfaces row is where a caller reads before writing a consumer, which is the audience that gets it
wrong, and it needed no restructuring — the retirement paragraph for decision 44 already sits right
there. The `embarch-ui` half is dropped to `inbox/` at
`/home/gabriel/Github/embarch/embarch-doc/inbox/ui-debug-tab-diff-new-lines-fallback.md` rather than
stated from this side, since verifying what `diff_new_lines` actually does today is `embarch-ui`'s
call, not a fact `embarch-core`'s docs can respeak secondhand from a retired decision's old quote.

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

## Dispatch note — leg 119, 2026-09-16

**In reserve for `core`:** `embarch-core/decisions/auth.md` is 11,356/12,288 B, **932 B of headroom**,
filed against `tasks/core/046-compact-core.md` (blocked, `In flux: yes`). You are not writing that
file — but if your work does push a file into reserve, or leaves one there that nothing has filed,
file `tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md` has the shape;
`scripts/check-task-numbers.py --next core` gives a safe number — **do not read the directory**).

**Per-decision cap:** `embarch-core` has no unpinned over-cap decision right now. Whichever home you
pick, check the entry you are writing into stays at or under **4,096 B** — `python3
scripts/check-doc-size.py --decisions` only prints the twenty largest in the suite, so it will not
warn you about a smaller entry you just pushed over (`tasks/doc/064`).

**The rule this leg is watching, and it caught nothing when stated loosely.** If you justify a cut —
or a decision *not* to restate something — by pointing at another decision, **open that decision and
confirm it covers the whole hunk sentence by sentence, not the topic.** This exact failure landed
twice in leg 118 under an explicit instruction to quote cuts verbatim.

## Done when

- [x] The trailing-partial-line fact about `read_recent`/`tail_lines`, **with its "why it is
      acceptable" clause**, is stated in a live `embarch-core` doc. — `embarch-core/interfaces/logs.md`'s
      `/logs/recent` row now carries it.
- [x] The `embarch-ui` `diff_new_lines` half is either stated in an `embarch-core`-owned doc that can
      legitimately mention it, or dropped to `inbox/` for a `ui` worker — not silently left out. —
      dropped to `inbox/ui-debug-tab-diff-new-lines-fallback.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). — all 11 `check-docs.py` checks, plus
      `check-client-names.py` and `check-ownership.py` (doc and code repo), green. No `embarch-core`
      source change was needed: this is doc prose only, and the code's behaviour was already what the
      restored sentence describes.

## What shipped

- `embarch-core/interfaces/logs.md`: added a paragraph after the `/logs/stream` retirement note
  restating the trailing-partial-line fact and its "correct for 'show me the tail as it stands now'"
  justification, scoped to the `/logs/recent` row rather than to decision 16/29 (reasoning above under
  "Decision (leg 065's worker)").
- `inbox/ui-debug-tab-diff-new-lines-fallback.md`: filed for a `ui` worker to add `diff_new_lines`'s
  fallback to `embarch-ui/decisions/debug-tab.md`#13, verified against the real implementation rather
  than against the retired decision 44 quote.
- `changelog.d/core-logs-recent-partial-line.fixed.md`.
- No `status.d/` fragment: nothing suite-level changed. No `features.d/` fragment: no capability
  shipped, retired, or changed maturity. No compaction task filed: neither touched file entered
  reserve (`interfaces/logs.md` is 1,681 B; the reserve item on file remains `decisions/auth.md`,
  untouched by this unit).
