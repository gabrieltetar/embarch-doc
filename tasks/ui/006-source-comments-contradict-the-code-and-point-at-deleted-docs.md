# Fix `embarch-ui` source comments that contradict the code and point at deleted docs

**State:** open
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

- [ ] `config.rs`'s `study_designer` doc comment states decision 14's behaviour; `main.rs`'s header
      names live docs; `logs.rs` says `GET`.
- [ ] No `milestone-*.md` reference remains in `src/`.
- [ ] Every decision number cited still resolves against `embarch-doc/embarch-ui/decisions/`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
