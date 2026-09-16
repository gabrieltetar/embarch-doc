# 069 — two more `embarch-umbrella` decisions are over the per-decision cap, both invisible to the census that missed them

**State:** claimed by agent/umbrella/069-two-decisions-over-cap, 2026-09-16 16:08
**Source:** `agent/umbrella/068-two-decisions-over-cap` found `mirrors.md#16` while closing
`tasks/umbrella/068` and filed it to `inbox/` rather than reaching past its own task — the right
call. Leg 118 drained that drop, re-ran the census through `decision_state()` directly instead of
through the printer, and found `sticky-host.md#48` as well. **Why both were missed is
`tasks/doc/064`:** `check-doc-size.py --decisions` prints the twenty largest decisions in the suite
and marks which are over cap, so an unpinned breach below that line is printed nowhere. Neither of
these is a regression — `mirrors.md#16` was already 4,330 B at `91e75f5^` on 2026-09-13, before
`umbrella/064` touched it.
**Scope:** umbrella
**Hardware:** none — doc prose only. No board, no probe, no live Core, no `doctor` run.
**Owner:** no
**Compacts:** `embarch-umbrella/decisions/mirrors.md`, `embarch-umbrella/decisions/sticky-host.md`
**In flux:** no, both, and each was checked separately rather than answered once for the line.
Decision 16 is the `doctor`-mirrors-`embarch-api` rule; `mirrors.md`'s last two commits are
`umbrella/064` (a citation repoint) and a `suite/038` fold, neither rewriting the argument.
Decision 48 said what a sticky `saved.host` means and **left the clearing open** — that opening was
closed by **decision 51** (`umbrella/056`, then `umbrella/058` correcting the claims about it), and
`embarch-umbrella/open.md` line 15 now records the clearing as settled with a hardware debt against
it. A hardware debt is not doc flux: no board is coming to rewrite decision 48's text.

## What

Two entries, both over the 4,096 B per-decision cap, neither pinned in
`scripts/decision-size-baseline.json`:

```
4,347 B  embarch-umbrella/decisions/mirrors.md#16      (+251 B, 106% of cap)
4,193 B  embarch-umbrella/decisions/sticky-host.md#48  (+ 97 B, 102% of cap)
```

Both are small breaches. For each, the same fork the four units of leg 118 faced:

- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full.
- **One decision that has accreted several arguments** → split into two numbered decisions and update
  `embarch-umbrella/decisions.md`'s index, same commit. **A new decision number is the most
  expensive thing in this suite to reverse**, so the burden of proof is on this branch, and at 102%
  and 106% of cap it is a hard case to make for either.

Decision 16's heading is a warning sign worth reading before choosing: *"`doctor`'s token check
needed the same treatment, **and so did its config reading**"* — a heading with an "and so did" in
it is the shape that sometimes really is two decisions. Read it and say which you found.

## Watch for

- **Do not add pins to `scripts/decision-size-baseline.json`.** `scripts/` is owner-reserved, and
  pinning an over-cap decision is the papering-over move rather than the fix.
- **Quote every cut hunk verbatim and completely** in this task file. Leg 117 landed a compaction
  whose quote list had an unmarked gap; leg 118 made the rule explicit in every dispatch and a
  reviewer still found three single words cut without being itemized. Err toward over-inclusion.
- **The `core/064` failure mode, which cost this class a real claim.** That unit compacted a
  *retired* decision and cut a sentence about `read_recent`/`tail_lines` — functions backing a
  **live** route — as if the whole entry were retired-route provenance. The fact then existed nowhere
  (`tasks/core/065`). Before cutting anything, ask of it: *is this provenance about something already
  settled, or a statement about behaviour that is still true and documented nowhere else?*
- **Two live claims that must survive in readable form.** Decision 16's reason for the mirror — that
  a `doctor` resolving the token differently from the `embarch-api` it diagnoses is **worse than no
  check** — is the entry's reason for existing. Decision 48's meaning-of-the-field claim is what
  decision 51 builds on; `open.md` line 15's **hardware debt** ("confirm on a real machine") must not
  end up reading as confirmed.
- **Grep the whole doc repo for inbound `decision 16` and `decision 48` citations first**, and
  remember a bare `decision 16` in another sub-project's file means *that* sub-project's 16. That
  collision is what `api/099` spent a whole unit fixing.
- **If only one fits in a sane unit, do that one properly and file the remainder** as
  `tasks/umbrella/<NNN>-...` in the same commit.
- **Report before/after byte counts and the margin left** for each entry you touch. Three of leg
  118's four compactions finished inside 150 B of the cap; if yours does too, say so plainly, because
  nothing mechanical distinguishes "paid" from "paid, barely".

## Dispatch note (leg 120, 2026-09-16)

**Doc-size reserve for `umbrella`:** one file, and it is not one of yours —
`embarch-umbrella/decisions/bind.md` at 11,533/12,288 B, **755 B left**, PARKED under
`tasks/umbrella/009` which is `blocked`. Both files this task compacts are *out* of reserve
(`mirrors.md` 86.7%, `sticky-host.md` 60.1%) and `check-doc-size.py` lists both as **PAID — close
its item** once you are under. If your work pushes any `embarch-umbrella` doc into the last 10% of
its cap and nothing has filed it, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.

**Do not touch `decisions/locate-api.md`#42.** A separate live task, `tasks/umbrella/071`, owns it —
decision 42 cites decision 35 for a `list-targets` shape decision 35 does not record, and it has 77 B
of margin. Leave it alone entirely so the two units do not collide.

**The justification test, stated as this leg is stating it to every worker.** Five units in two legs
have now cut a hunk on a justification that was true of the hunk's *topic* and false of one clause
inside it. When you justify a cut with "this is already recorded in X", open X and read it **against
the hunk sentence by sentence**, not against the hunk's subject. If X is a paraphrase, the cut is not
covered. Quote the evidence, not the conclusion.

## Done when

- [ ] `embarch-umbrella` decision 16 is at or under 4,096 B, or split, with the branch justified.
- [ ] `embarch-umbrella` decision 48 likewise, **or** left untouched with a follow-up task filed.
- [ ] `embarch-umbrella/decisions.md`'s index matches, if anything was split.
- [ ] Every inbound citation to a touched decision still resolves to the claim it was citing.
- [ ] Every cut hunk quoted verbatim in this task file.
- [ ] No pin added to `scripts/decision-size-baseline.json`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
