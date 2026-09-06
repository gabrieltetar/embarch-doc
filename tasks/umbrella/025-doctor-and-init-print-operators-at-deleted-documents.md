# Stop `doctor` and `init` printing operators at documents the four-file split deleted

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `DOC-PROTOCOL.md:86` records this class going unnoticed for a week
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Three user-visible strings name documents that no longer exist:

- `src/doctor.rs:274` — check 1's Pass detail says "(milestone-6.md §3.7)".
- `src/doctor.rs:1090` — check 9's **fix line** ends "see ../embarch-doc/embarch-api/design.md §12".
- `src/install.rs:142` — the marker written into a user's `~/.bashrc` cites
  `embarch-umbrella/design.md decision 28`.

All three were deleted by the four-file split (`embarch.md` §6: "Deleted, not indexed"). The
`embarch.toml` comments `init` writes (`init.rs:486`, `:534`) are in the same class.

Every string a human is *shown* should name a document that exists — `spec.md`,
`decisions/<file>.md`, or a decision number, which `scripts/check-decision-refs.py` can resolve.

**`ensure_not_sourced` must still recognise the old marker text**, so an uninstall on a machine set
up before this change still removes the comment it wrote. That is the half that is easy to lose.

## Why now

These are error and fix lines that route an operator to a `git show`-only file. `DOC-PROTOCOL.md:86`
says nothing mechanical guards this class and that a doc-shape change means sweeping the pointers in
the same pass — the source strings were never swept.

## Done when

- [ ] No user-visible string in `src/` names `design.md` or `milestone-*.md`.
- [ ] `ensure_not_sourced` removes both the new and the legacy marker; a test pins the legacy case.
- [ ] A test asserts no `Check.detail` / `Check.fix` contains `design.md` or `milestone`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
