# 055 — `embarch-ui` decision 25 is over the per-decision cap, and was invisible to the census that was supposed to find it

**State:** done — agent/ui/055-decision-25-over-cap, 2026-09-16. Decision 25 squeezed from 4,307 B to
3,758 B; see "Resolution" below.
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

- [x] `embarch-ui` decision 25 is at or under 4,096 B, or split, with the branch justified.
- [x] The 1.12:1 measurement and both `oklch` values survive.
- [x] `embarch-ui/decisions.md`'s index matches, if split. (Not split — index already reads `4, 8, 25` for `decisions/shell.md`, unchanged.)
- [x] Every inbound citation still resolves to the claim it was citing.
- [x] Every cut hunk quoted verbatim in this task file.
- [x] No pin added to `scripts/decision-size-baseline.json`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Resolution — squeeze, not split

**Byte count, measured directly (`decisions()`'s own boundary: the `### 25` heading through end of
file, since 25 is the last decision in `shell.md`), not via the census, which cannot see this range:**

- Before: **4,307 B** (211 B over the 4,096 B cap, 105%).
- After: **3,758 B** (**338 B under cap**, 92% of the limit).
- `shell.md` as a whole: 6,736 B → 6,187 B, against a 12,288 B `decision-group` cap (no reserve
  pressure created).

**Why squeeze, not split.** The entry is one claim — the mark's red and `--danger` are
perceptually the same colour, so the accent stays cyan rather than brand red — argued once, plus
three long paragraphs of *how* the logo asset (an SVG traced from a raster master) is generated and
validated. That generation detail is cold by `DOC-COMPACTION-PASS.md`'s own test ("validation
records" and "measurements" not cited elsewhere), not a second argument for the decision, so it does
not meet the bar for a second decision number — consistent with the task's own steer that 105% over
is a hard case to make for a split.

**Cut hunks, verbatim and complete** (all four are the removal of a validation record / measurement
that confirms the tracer tooling works, never the claim, the "why not", or a location that's cited
elsewhere):

1. From the header-glyph paragraph — vertex/byte counts for `trace_mark.py`'s output, immediately
   after "the straight lines the art was drawn with":
   > : 22 vertices plus a 4-vertex counter for the E, 15 plus a 4-vertex counter for the A, 657 B inline.
   (the sentence now ends "...the art was drawn with.")

2. From the standalone-SVG paragraph — the traced file's own size/vertex count, inside the opening
   parenthetical:
   > , 693 B, 53 vertices
   (parenthetical now reads "(`assets/brand/embarch-mark.svg`)").

3. From the same paragraph — the tolerance-sweep's numeric results, after "the sweep says it is the
   right one":
   > — against the master, 1.2 buys 0.04/255 for 8 more vertices and 0.8 buys 0.5 for 505, because those vertices trace the render's antialias wobble rather than the art.
   (the bolded conclusion "**Tolerance 1.6 is the glyph's number and the sweep says it is the right
   one.**" is kept verbatim and now ends the sentence itself.)

4. From the end of the same paragraph — the raster-vs-vector accuracy measurement, after "two
   independent downscales that could drift":
   > Both land within 1.9/255 of the bitmaps they replace. What tracing a 256px raster costs is half a pixel of edge placement, measured at −0.24 to −0.43 px on the A's left edge and varying in sign, so it is grid quantisation rather than a bias worth correcting.

**Kept verbatim, because they are the load-bearing content:** the 1.12:1 measurement sentence in
full (`**The mark's red is `oklch(63% 0.194 29)` and `--danger` is `oklch(66% 0.19 25)`: measured in
the browser they sit at 1.12:1 against each other, which is to say they are the same colour.**`),
the "why not" (a red accent would read as destructive), the `--brand`/`--accent` split and its
"exactly two things" call-site count (cited by `history/ui.md:39`), the tracing-vs-bitmap theming
rationale, the union-mode rationale, and the light/dark contrast paragraph in full.

**Inbound citations checked** (`grep -rn "decision 25"` across the whole doc repo, per the task's
instruction): `changelog.d/ui-brand-token.added.md`, `embarch-ui/spec.md:81`, and
`history/ui.md:39` all cite `embarch-ui` decision 25 and all three claims they cite (brand-vs-danger
colour identity; the `--brand`/`--accent` split; the "two declarations, two call sites, not three"
count) are still present verbatim. Every other `decision 25` hit in the repo (`embarch-core`,
`embarch-topology`, `embarch-api`, `embarch-umbrella`) is that sub-project's own unrelated decision
25, confirmed by reading each one, not by the number alone.

**Census caveat honoured.** `check-doc-size.py --decisions` was not used to verify this — it only
ever prints the 20 largest decisions in the suite and 27 pinned entries fill those slots, so a
4,307 B → 3,758 B entry is invisible to it either way (`tasks/doc/064`). Verified instead with
`decision_state()`'s own boundary logic run directly against the file, shown above.

**No pin added to `scripts/decision-size-baseline.json`** — not touched; `scripts/` is
owner-reserved and this entry no longer needs one.

**Human question (`DOC-COMPACTION-PASS.md`):** *Can `spec.md` alone answer what someone needs to
work on this component today?* Yes, unaffected by this unit — `spec.md:81` already states the
load-bearing fact (`--brand` holds the logo red, it equals `--danger`, so it's never the accent) and
cites decision 25 for the "why". This unit only trimmed decision 25's own cold detail; it did not
add or remove anything `spec.md` depends on.

**Left undone:** nothing in scope. `embarch-ui`'s other four unpinned/pinned decisions and the
census mechanism itself (`tasks/doc/064`) are out of this task's scope — `doc`, owner-reserved.
