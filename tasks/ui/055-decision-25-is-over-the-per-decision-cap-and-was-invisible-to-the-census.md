# 055 — `embarch-ui` decision 25 is over the per-decision cap, and was invisible to the census that was supposed to find it

**State:** claimed by agent/ui/055-decision-25-over-cap, 2026-09-16 14:25
**Source:** leg 118, 2026-09-16. Leg 117 ran a suite-wide per-decision census, reported five breaches
and filed four tasks; leg 118 landed all four, then found the census had never been capable of
seeing the rest. `check-doc-size.py --decisions` prints the **twenty largest decisions in the suite**
and marks which are over cap, so an unpinned breach below that line is printed nowhere — 27 pinned
over-cap entries fill the slots. Read through `decision_state()` directly, five unpinned breaches
remain and this is one of them. The mechanism is `tasks/doc/064` (owner-reserved; `scripts/`).
**Scope:** ui
**Hardware:** none — doc prose only. No board, no probe, no live Core, no UI launched.
**Owner:** no
**Compacts:** `embarch-ui/decisions/shell.md`
**In flux:** no. Decision 25 is a **closed** colour decision: the project has a logo, the mark's red
measured 1.12:1 against `--danger`, and the accent stays cyan. The measurement is done, the ramp is
chosen, and nothing in flight is re-opening the palette. `shell.md` is 6,736 B against a 12 KB
`decision-group` cap, so there is no file-level pressure here either — this is purely the
per-decision cap.

## What

`embarch-ui/decisions/shell.md#25` — *"The mark's red is a brand token, deliberately not the
accent"* — is **4,307 B** against the 4,096 B per-decision cap: 211 B over, 105% of the limit, and
unpinned.

The fork, the same one leg 118's four units faced:

- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full.
- **One decision that has accreted several arguments** → split into two numbered decisions and update
  `embarch-ui/decisions.md`'s index, same commit. **A new decision number is the most expensive thing
  in this suite to reverse**, so the burden of proof is on this branch, and at 105% of cap it is a
  hard case to make.

211 B is a realistic squeeze. Read the entry before choosing anyway rather than assuming the small
breach settles it.

## Watch for

- **Keep the measurement and keep the "why not".** The load-bearing content is the *number* —
  `oklch(63% 0.194 29)` against `oklch(66% 0.19 25)` at **1.12:1**, measured in the browser — and the
  consequence, that a red accent would make every primary button read as destructive and stop
  failures standing out. A compaction that keeps the conclusion and drops the measurement invites the
  accent being re-proposed by someone who thinks it was a taste call. **That measurement is the one
  thing in this entry nothing else in the suite records.**
- **The `core/064` failure mode, which hit this class twice in leg 118 alone.** A cut justified as
  "provenance" or as "duplicates decision N" is exactly where a live claim goes missing: once when a
  retired decision's compaction cut a live-route behavioural fact (`tasks/core/065`), once when a
  "duplicates decision 35" justification covered only part of the cut paragraph
  (`inbox/umbrella-locate-api-list-targets-shape-orphaned.md`). Before cutting anything, ask of it:
  *is this still true, and is it stated anywhere else?* If you justify a cut by pointing at another
  decision, **open that decision and confirm it covers the whole hunk, sentence by sentence** — not
  the topic.
- **Quote every cut hunk verbatim and completely** in this task file. Err toward over-inclusion; two
  reviewers in leg 118 found unitemized single-word drops even under an explicit instruction.
- **Do not add a pin to `scripts/decision-size-baseline.json`.** `scripts/` is owner-reserved, and
  pinning an over-cap decision is the papering-over move.
- **Grep the whole doc repo for inbound `decision 25` citations first**, and remember a bare
  `decision 25` in another sub-project's file means *that* sub-project's 25 — `embarch-topology`,
  `embarch-api` and `embarch-ui` all have a real, unrelated decision 25.
- **Report before/after byte counts and the margin left.** Three of leg 118's four compactions
  finished inside 150 B of the cap; if yours does too, say so plainly, because nothing mechanical
  distinguishes "paid" from "paid, barely".

## Dispatch note — leg 119, 2026-09-16

**In reserve for `ui`: nothing.** No `embarch-ui` file is inside the last 10% of its cap —
`shell.md` is 6,736/12,288 B — so this is purely the per-decision cap and you have file-level room.
If your work does push a file into reserve, file `tasks/ui/<NNN>-compact-ui.md` in the same commit
(`scripts/check-task-numbers.py --next ui` for the number — **do not read the directory**).

**Do not use the census to check your work.** `check-doc-size.py --decisions` prints only the twenty
largest decisions in the suite, and 27 pinned over-cap entries fill those slots, so a 4,307 B entry
dropping to 4,000 B simply vanishes from the list whether or not it is under cap (`tasks/doc/064`,
owner-reserved). Count decision 25's bytes directly, before and after, and report both.

**Standing `ui` debt, for context only, not yours to pay:** `embarch-ui`'s 18-record stale prefix has
still never met a real stale prefix. Nothing in this unit touches it.

## Done when

- [ ] `embarch-ui` decision 25 is at or under 4,096 B, or split, with the branch justified.
- [ ] The 1.12:1 measurement and both `oklch` values survive.
- [ ] `embarch-ui/decisions.md`'s index matches, if split.
- [ ] Every inbound citation still resolves to the claim it was citing.
- [ ] Every cut hunk quoted verbatim in this task file.
- [ ] No pin added to `scripts/decision-size-baseline.json`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
