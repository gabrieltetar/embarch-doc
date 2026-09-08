# Fix `embarch-ui` source comments that contradict the code and point at deleted docs

**State:** claimed by agent/ui/006-source-comments-contradict-the-code, 2026-09-07 18:10
**Source:** owner's repo survey, 2026-09-06 — `DOC-PROTOCOL.md:86` records this class going a week unnoticed
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Three statements in `src/` are false, and the module headers point at deleted files:

- `src/config.rs:16-20` — "Absent means the Study Designer tab is unavailable", which
  `src/main.rs:82-90` and `decisions/study-designer.md` 14 both say is no longer true ("It used to
  be `Option` … which made the whole tab unreachable").
- `src/main.rs:3-11` — opens on `milestone-1.md` and `design.md`, both deleted.
- `src/logs.rs:39` — calls `/logs/recent` a `POST` where `spec.md` and the client both make it a `GET`.

Fix those three and the top-of-file pointers, citing `spec.md` / `decisions/<file>.md` or a decision
number. **Scope it there.** This is not a repo-wide rewrite of every `design.md §3 decision N`
citation — `../../DOC-CONVENTIONS.md` says that form still parses, and a 74-site sweep is a different
task with a different risk.

## Why now

`DOC-PROTOCOL.md:86` records this exact class going a week unnoticed because nothing mechanical can
see it. A comment asserting that a `None` config kills the tab is the one an agent reads before
touching `study_designer`.

## Done when

- [x] `config.rs`'s `study_designer` doc comment states decision 14's behaviour; `main.rs`'s header
      names live docs; `logs.rs` says `GET`.
- [x] No `milestone-*.md` reference remains in `src/`.
- [x] Every decision number cited still resolves against `embarch-doc/embarch-ui/decisions/`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Verification against the code, 2026-09-07

All three survey claims re-checked against the branch as it stands today, not
against the 2026-09-06 survey text:

- **`config.rs`'s `study_designer` comment**: still false, in the same way the
  survey recorded. `AppState.study_designer` (a `StudyDesigner`, always
  present) is unrelated to `Config.study_designer` (an `Option`, the field
  this comment is on) — the tab has been unconditionally reachable since
  decision 14 landed, and this config field is only the zero-click default
  for a single-repo bench. Comment rewritten to say that, citing decision 14.
- **`main.rs`'s header**: `milestone-1.md` and `design.md` are both still
  absent from `embarch-doc/embarch-ui/`. Rewritten to point at `spec.md` and
  `decisions/`.
- **`logs.rs:39`'s `POST` vs `GET`**: checked against the wire per the
  supervisor's direction, not against another comment.
  `embarch_core_client::CoreClient::logs_recent`
  (`embarch-api/crates/embarch-core-client/src/client.rs:1172`) issues
  `self.client.get(url)` — a plain GET. **The code was already correct; only
  the comment was wrong.** No behaviour change, no bug — this stayed a
  comment fix.

Additionally swept every other `milestone-1.md`/`milestone-11.md` reference
left in `src/` (`logs.rs:1`, `study_designer.rs:1,13,58,284`, `main.rs:130,167`
by pre-edit line numbers) per the "no milestone-*.md reference remains"
checklist item, while leaving the separate legacy `design.md §3 decision N`
citation form untouched everywhere it appears, per the task's explicit scope
note and `../../DOC-CONVENTIONS.md`.

No `decisions/study-designer.md` write: read decision 14, did not add to it,
and this unit needed no new decision (the fix is entirely descriptive of
already-decided behaviour). No `spec.md`/`decisions.md`/`open.md` edit either
— nothing there was made false by a comment-accuracy fix with no design or
behaviour change, so nothing suite-level went false and no `status.d/`
fragment was warranted.

Gate: `cargo build`, `cargo test` (103 passed, 0 failed), `cargo clippy
--all-targets -- -D warnings` all clean in the code worktree (single-crate
repo, no non-member `Cargo.toml`). `scripts/check-docs.py` all 10 checks
green in the doc worktree. `scripts/check-ownership.py --scope ui` (doc
branch) and `--code-repo --scope ui` (code branch) both green.
`scripts/check-client-names.py --repo <code worktree>` clean against 7
denylist entries. Both branches pushed.

## Supervisor direction, leg 041

**Check each of the three claims against the code before you rewrite it, and be
willing to find that one of them is now false in a different way.** These were
observed in a survey on 2026-09-06 and `embarch-ui` has landed two units since
(`ui/013` corrected a `Cargo.toml` comment on exactly this class of defect, and
`ui/012` corrected the same overstatement in `spec.md` the day before). A
comment you "fix" to a claim that is itself wrong is strictly worse than the one
you replaced — `ui/013`'s reviewer was spawned specifically to check that, and
found the new wording held. Expect the same check.

**`logs.rs:39`'s `POST` vs `GET` is the one to verify against the wire, not
against another comment.** `embarch-ui/spec.md` and the client both say `GET`;
confirm what the code actually issues rather than assuming the comment is the
only thing wrong. If the *code* sends a `POST`, that is a bug and a much bigger
finding than a stale comment, and it stops being a comment task — say so in the
task file rather than quietly changing behaviour.

**The scope line in "What" is binding**: three sites plus the module headers, not
a 74-site citation sweep.

## Doc-size reserve for `ui`

Three `ui` files are in reserve, and one of them is nearly full:

- `embarch-ui/decisions/study-designer.md` — 12064/12288 B, **224 B left**,
  filed against `tasks/ui/011-compact-ui-study-designer-decisions.md` (open).
  Decision 14 lives here and this task cites it. **Read it; do not add to it.**
  224 bytes is not enough for a new decision, and this unit should not need one.
- `embarch-ui/spec.md` — 9461/10240 B, **779 B left**, filed against
  `tasks/ui/018-compact-ui-spec.md` (open).
- `embarch-ui/decisions/trace-chart.md` — 11833/12288 B, **455 B left**, filed
  against `tasks/ui/019-compact-ui-trace-chart.md` (open).

All three already have a compaction task filed, so you owe no new one for them.
If your work pushes some *other* `ui` file into the last 10% of its cap, file
`tasks/ui/<next NNN>-compact-ui-<what>.md` in the same commit per
`tasks/README.md`.
