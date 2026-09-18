# 086 — Date the two `study_results/` size readings instead of harmonising them

**State:** claimed 2026-09-17 leg 142 unit 4 — `agent/umbrella/086-date-study-results-readings`.
Drained from `inbox/umbrella-date-the-study-results-size-figures.md` at `api/116`'s fold the same
day and numbered `086`; body unchanged apart from this line and the verification note below.
**Doc-size reserve for `umbrella`** (leg 142, at dispatch): `decisions/install.md` 217 B left,
`decisions/bind.md` **755 B left (93.9%, already in reserve)**, `decisions/projects.md` 1125 B left
(90.8%), `open.md` 770 B left (85.0%) — `install.md`, `bind.md`, `projects.md` and `open.md` are each
already filed against a blocked compaction task (`umbrella/079`, `009`, `084`, `077` respectively).
**Two of the files this unit edits are in that list**, which is why the note below caps what it may
write. **Do not file a duplicate compaction task** for a file whose debt is already filed; only file
one if you push a *different* file into the last 10%.
**Owner:** no

> **Verified by the supervisor at the drain, because one claim in the parent task was wrong.**
> `tasks/api/116`'s own body said `embarch-umbrella/open.md`'s bullet *"no longer carries the figure
> at all"* after `umbrella/082` rewrote it. **It does** — `open.md`'s decision-26 `--prune` bullet
> still reads *"`study_results/`'s 803 MiB is a separate, already count-bounded gap"*, undated, and
> the second `Done when` box below is therefore live and correct. I checked this by grep against
> `main` at the drain rather than taking either file's word for it. `decisions/bind.md`'s undated
> 809 MiB was not re-verified beyond the drop's own citation.
>
> **Two corrections from `api/116`'s reviewer, which re-derived the provenance instead of confirming
> it. Read these before the body below, because the body is the drop as written and carries both
> errors.**
>
> 1. **It is decision 39, not "decisions 37/39".** The literal dated capture
>    *"50 entries, 802.9 MiB"* lives in `embarch-umbrella/decisions/reporting.md` decision **39**
>    alone. Decision 37 is the unrelated `code`-field decision and has nothing to do with this
>    figure. The body's "decisions 37/39" is wrong in both places it appears.
> 2. **`802.9` and `803` are not in the same file, and the difference matters to the argument.**
>    `802.9 MiB` is in `reporting.md` decision 39; the prose string `803 MiB` that `embarch-api`
>    decision 77 quotes verbatim is in `open.md`, edited by the *same* commit `fc4f4ac0` — almost
>    certainly 802.9 rounded for a prose bullet, **not a second independent capture**. So the
>    independence claim holds at the level of *809 (2026-09-05) vs 802.9 (2026-09-06)* — two
>    commits, two days, two doctor runs — and **not** at the level the parent unit's commit message
>    implies.
>
> **And the counter-argument the parent unit never answered, which a decision already on the books
> disposes of.** Both readings say **50 entries**, which is what a copy looks like rather than two
> `du` runs a day apart, and `tasks/api/116` raised that and then did not address it.
> `embarch-umbrella/decisions/projects.md` decision 26's 2026-09-05 amendment is the answer:
> `embarch-core` ships `sweep_study_results` with `EMBARCH_STUDY_RESULTS_KEEP` defaulting to **50**,
> swept at every `POST /study`. **50 is a retention ceiling, so once a bench has run 50 studies every
> later reading shows exactly 50 by construction** while the byte total drifts with *which* 50 are
> retained. That makes the identical entry count inevitable rather than suspicious, and it is the
> piece of evidence that actually closes this, and three documents have now gestured at decision 26
> without stating it.
>
> **But do not spend the reserve writing it down.** Amended by leg 142 at dispatch: all three
> candidate files are already in the size reserve — `decisions/bind.md` **93.9%**,
> `decisions/projects.md` **90.8%**, `open.md` **85.0%** — and decision 26 already *contains* the
> mechanism, so adding a paragraph would be restating a decision in three places that have no room
> for it. **The required work is the two date stamps, roughly 40 bytes total.** If a short
> parenthetical citing decision 26 fits without pushing a file further into reserve, add it; if it
> does not, say so and leave it. The mechanism is recorded here and in `supervisor-log.md`, which is
> where it needs to survive.

**Source:** `tasks/api/116` (established the provenance below; `api`'s own half —
`embarch-api/decisions/target-json.md` decision 77 — is already fixed in that
unit). `embarch-umbrella/**` is not `api`'s to edit, so this half is dropped
here per `protocol.md` §3.
**Scope:** umbrella
**Hardware:** none — dating two existing prose statements from evidence already
in git history, no new measurement.

## What

`study_results/`'s size (50 entries throughout) is stated with two different
byte counts across the suite, and neither carries a measurement date in its
current text. Both are **real, independent, dated readings**, not a
transcription error — full provenance below. Fix is to date each statement in
place, not to reconcile them to one number.

- **809 MiB** — the *first* live reading, `git log -S '809 MiB'` →
  `de07c827` ("The first doctor run against a Core that actually got
  deployed", 2026-09-05 20:37:56). That commit's own prose: *"Check 16's
  first live reading is 809 MiB across 50 entries."* This is the figure
  `history/umbrella.md`'s changelog line already carries (correctly, and
  that file is append-only — leave it). It is also the figure
  `embarch-umbrella/decisions/bind.md` decision 22 carries, **undated**:
  *"Check 16 already measures what grows here — `study_results/` at 809 MiB
  across 50 entries"* — written by `0824325f` (2026-09-06 01:30:24), i.e.
  citing the previous day's reading, before the second reading (below)
  existed later that same day.
- **803 MiB** (802.9 MiB precisely) — a *second*, later live reading the
  next day. `git log -S` on the bare digits makes this look like a
  transcription error at first (identical entry count, one day apart), but
  it is not: `fc4f4ac0` ("umbrella/027: doctor runs live, and the check
  waiting for a bench was waiting for a timeout", 2026-09-06 18:52:37) is
  where the number changes, and the same commit independently fills in
  `embarch-umbrella/decisions/reporting.md` decisions 37/39 with:
  *"**Verified live** [measured 2026-09-06, `embarch doctor` and `embarch
  doctor --json` on the primary `wsl-host` bench]: `detail` read
  `study_results/ at /mnt/c/ProgramData/embarch/study_results: 50 entries,
  802.9 MiB`"* — a literal capture of `doctor`'s own output text, decimal
  precision, explicitly dated. That is where "803 MiB" (802.9 rounded) comes
  from, and it is genuine: two doctor runs, one day apart, same entry count,
  slightly different bytes — an ordinary week for a directory that both
  grows and gets swept (decision 26's amendment), not a copy-paste error.
  The same commit's `open.md` edit restates this reading in the `--prune`
  bullet, **also undated**, and that undated form is what later got quoted
  verbatim into `embarch-api` decision 77 (`tasks/api/109`, 2026-09-17) and
  from there into `embarch-umbrella/open.md`'s current bullet
  (`f61b43ff`, umbrella/082) — so the missing date has now propagated to a
  second sub-project's decision file. `api`'s copy already carries
  `[measured 2026-09-06]` as of this drop.

## Why now

Same as `tasks/api/116`: cheap now, more expensive once more things cite an
undated number. `embarch-api` decision 77 already resolved its own copy;
leaving the `umbrella`-side originals undated means the next reader who
diffs the two sub-projects' decisions finds the same unexplained mismatch
again, having lost the archaeology this drop just did.

## Done when

- [ ] `embarch-umbrella/decisions/bind.md` decision 22's `809 MiB` sentence
      gains `[measured 2026-09-05]`.
- [ ] `embarch-umbrella/open.md`'s current bullet (the one closing decision
      26's `build_dir_name` prerequisite, added by `f61b43ff`) has its
      `803 MiB` gain `[measured 2026-09-06]`.
- [ ] `embarch-umbrella/decisions/reporting.md` decisions 37/39 already carry
      a date on `802.9 MiB` — no change needed there; do not touch it.
- [ ] `history/umbrella.md`'s changelog line is append-only history and needs
      no change — leave it as is.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] No `changelog.d/` fragment needed — no reader-facing number changes,
      only provenance dates are added to existing statements.
