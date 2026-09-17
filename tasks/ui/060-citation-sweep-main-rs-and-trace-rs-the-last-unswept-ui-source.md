# 060 — Citation sweep: `src/main.rs` and `src/trace.rs`, the last unswept `ui` source

**State:** done
**Source:** `tasks/ui/054`, which swept `assets/app.js` and excluded these two **by scope, not by
running out of room** — it said so at filing and its worker said so again in its report. Filed here
so the remainder is written down rather than rediscovered, the way the `study-designer/044`–`055`
chain has been doing it.
**Scope:** ui
**Hardware:** none — source comments in Rust files. Nothing is built for a board, the UI is not
launched, no probe, no live Core.
**Owner:** no

**Doc-size reserve for `ui`: nothing in reserve.** `embarch-ui`'s files are all clear after `ui/050`,
`ui/053` and `ui/054`. If your work pushes a `ui` doc into the last 10% of its cap, file
`tasks/ui/<next free NNN>-compact-ui.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

```
src/main.rs    26 citation lines
src/trace.rs   25 citation lines  (ui/048 already fixed one of them, a bare decision 35)
```

About 50 grep lines, and **the instance count will be higher** — every chain that measured both
found them differing. `ui/054` found one citation its own census could not see at all:
`decisions 53/55` at line 853 of `app.js`, missed because the **plural** "decisions" does not match
`decision` followed by a space and a digit. `core/067` independently hit the same thing the same day.
**Re-census with a pattern that catches the plural**, and treat the line counts above as a floor.

Take `src/main.rs` first, unless you find a reason to reorder and say what it is. If you run out of
budget, sweep what you take thoroughly and file the remainder — a half-read file reported as swept is
worse than an honest partial.

## Method

1. **Does the cited decision exist**, in the repo the citation's form says it is in? A bare
   `decision N` means `embarch-ui`'s own; a foreign one must carry the `` `<repo>` `` label
   (`DOC-CONVENTIONS.md`, "Referring to a decision").
2. **Read the cited decision's body, then the sentence around the citation.** A number that resolves
   is not evidence the claim holds, and that is where nearly all of this chain's yield has come from.
3. **Check every number in the cited sentence**, not just the decision number.
4. **Check `file:line` suffixes for drift**, not only path correctness.

## Watch for

- **`check-decision-refs.py` reads `*.md` only, inside the doc repo.** It has never read a `.rs`
  file in `embarch-ui`. Nothing fails if a citation here is wrong.
- **The 44-character attribution window.** A `` `<repo>` `` label earlier in a sentence does not
  carry to a second citation further along. `api/091` closed that shape in `client.rs`, `api/097`
  reintroduced it eight words away, `api/099` closed it again, and `ui/054` measured the one
  borderline case in `app.js` and found it inside the window. Measure rather than eyeball.
- **Low bare numbers in this repo are `embarch-ui`'s own and are correct bare.** `ui/054` found
  `decision 10` used with **four distinct meanings** in one file. Do not relabel a bare citation
  without establishing which repo it means.
- **A comment may cite a dated amendment the decision no longer records.** `ui/054` and `api/102`
  both hit this on the same day, in different repos: compaction folds the amendment note away and
  the citing comment goes on naming the date. Both units corroborated the date from `embarch-doc`
  git history and **left the comment standing**, which is the precedent. Do it the same way, and say
  so, rather than deleting a true claim because the doc no longer restates it.
- **A citation can be falsified by an amendment in another repo, with nothing here changing.**
  `study-designer/054` found exactly that on 2026-09-16. If a cross-repo citation's sentence borrows
  an argument from the far decision, read the far decision's **current** text including its
  amendment blocks.

## Done when

- [x] Both files swept — or one swept thoroughly and the other filed as its own task.
- [x] Every citation checked for existence, repo label, and whether its sentence is true, counted as
      *instances* rather than grep lines, with a census pattern that catches plural citations.
- [x] Wrong numbers and false sentences reported as **separate** counts with the total checked.
      "Checked N, found none" is a legitimate and useful result: whether this vein is exhausted is an
      open question and honest zeros are the only thing that answers it.
- [x] No new bare cross-repo citation introduced anywhere in the diff.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/ui-*` fragment reporting the counts.

## Result

Re-census with `[Dd]ecisions? [0-9]+` (catches the plural; none found in either file):
`main.rs` 26 grep lines / 27 citation instances, `trace.rs` 25 grep lines / 27 citation
instances — both match the task's floor exactly, no undercounted plurals this time.

**54 instances checked. 1 wrong number, 0 false sentences.**

- `src/trace.rs`'s module doc (the "two clocks" section) misstated the row-86 incident:
  "4286 of **9205** spans read as unmeasurable" — every other account of the same incident
  (`embarch-ui` decision 10 (trace), `embarch-outpost/spec.md`'s resolution table,
  `reversals/rows-73-92.md` row 86, and suite decision 4's own placement writeup) says
  **4955**. `9205` is this same file's own row count for an unrelated capture (`~490 rows of
  a 9205-row capture`, used correctly two paragraphs later) — a transposition, not a second
  measurement. Fixed to `4286 of 4955 spans`; nothing else in that sentence needed changing.
- Every decision-number resolution checked against the cited repo's actual text: all 27
  citations in `main.rs` and all 27 in `trace.rs` resolve to a decision that exists and whose
  body backs the sentence citing it, including the three-way bare `decision 10` collision
  (routing/trace/chart) — every bare `decision 10` in both files resolves unambiguously from
  its surrounding sentence, and two of them (`main.rs:423`, `trace-chart.md`'s own text) are
  already explicit about which half they mean.
- One unverifiable-but-not-contradicted date: `trace.rs:33-34` cites "`embarch-outpost`
  decision 4's 2026-08-27 rework" while `trace.rs:67-68`'s own account puts layout 3's restore
  "the day before" the file's own fix (dated 2026-08-27) — i.e. 2026-08-26. No decision doc
  pins an exact date for the layout 2→3 change, so this could not be resolved either way and
  was left standing rather than guessed at. Flagging it here for whoever sweeps `trace.rs`
  next.
- `tasks/ui/051` (cited twice, `trace.rs:268` and `main.rs:489`/`609`) no longer exists as a
  file — normal task retirement — but its claim ("`embarch-ui` stopped recomputing the load
  arithmetic locally") is corroborated in `history/ui.md`'s Changed section and left standing,
  same precedent as the dated-amendment case in the Watch-for list.

## Not yours

`history/ui.md` is assembled from fragments.
