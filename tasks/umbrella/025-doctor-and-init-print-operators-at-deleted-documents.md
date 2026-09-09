# Stop `doctor` and `init` printing operators at documents the four-file split deleted

**State:** done by agent/umbrella/025-stale-doc-pointers, 2026-09-08
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

- [x] No user-visible string in `src/` names `design.md` or `milestone-*.md`. Fixed the four call
      sites named in What: `doctor.rs`'s check-1 Pass detail (now `(decision 42)`), check 9's fix
      line (now `spec.md, check 9`), `install.rs`'s rc marker (now `embarch-umbrella decision 28,
      decisions/install.md`), and `init.rs`'s two `embarch.toml` comments (`init.rs:486` now points
      at `embarch-api decision 12 (decisions/zephyr.md)`, `init.rs:534` at `decision 16,
      decisions/mirrors.md`). The many other `design.md`/`milestone` hits `grep` finds in `src/` are
      all inside `//`/`///` developer comments, never shown to an operator — left alone, and pinned
      by the new test below as out of scope on purpose.
- [x] `ensure_not_sourced` removes both the new and the legacy marker; a test pins the legacy case.
      Added `LEGACY_MARKER` (the exact old text) alongside the new `MARKER`; `ensure_not_sourced`
      strips a line matching either. New test:
      `install::tests::ensure_not_sourced_removes_the_legacy_pre_four_file_split_marker`.
- [x] A test asserts no `Check.detail` / `Check.fix` contains `design.md` or `milestone`. Added
      `doctor::tests::no_check_text_names_a_document_the_four_file_split_deleted` — scans
      `doctor.rs`'s own production source (everything above `mod tests`) line by line, skips
      comment-only lines, and fails on any remaining line naming either string. This is a source
      scan rather than an exhaustive runtime enumeration of every `Check` (many need a live Core
      probe or subprocess to construct); it is precise here because every current occurrence of
      both strings in `doctor.rs` is a `//`/`///` comment, verified by hand before landing.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`, `cargo test` (218 passed),
      `cargo clippy --all-targets -- -D warnings` all clean in the code worktree;
      `scripts/check-docs.py` green in the doc worktree (see report).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. No `spec.md`/`decisions.md`/`open.md` edit
      was made: none of the three named the stale strings this task fixed, so there was nothing
      false to correct, and `decisions/install.md` (decision 28) was left alone rather than amended
      because the smallest useful sentence still pushed it into the doc-size reserve (see below).
      `changelog.d/umbrella-doctor-init-stale-doc-pointers.fixed.md` dropped. No `status.d/`
      fragment: nothing suite-level (`embarch.md`, `suite/*.md`) asserted these strings either, so
      nothing suite-level went false.

**Considered and rejected: a new numbered decision.** This leg runs in burndown mode, which forbids
authoring one — but it would have been the wrong shape anyway. A source string naming a document
that no longer exists is a bug the four-file split introduced, not a new design choice; there is
nothing here an operator or a future worker needs to *decide* differently going forward, only the
stale pointers to fix (which decision 28 already covers structurally: the marker text and its
uninstall counterpart).

**Doc-size reserve, checked before and after.** Tried amending `decisions/install.md` decision 28
with one sentence recording the marker-text fix and the legacy-compat guarantee; even trimmed to a
single short clause, it pushed the file from 11009 B (89.6% of 12288) to 90.8%+, into the reserve
band `check-doc-size.py` flags as needing a filed debt. Reverted rather than file a new
`tasks/umbrella/<NNN>-compact-umbrella.md` for one sentence — the fix itself needed no decisions.md
change (see above), so the file is untouched and still at its original 11009 B / 89.6%. The three
files the dispatch note named as already in reserve (`spec.md`, `open.md`, `decisions/bind.md`)
were not touched by this task at all.

## Supervisor's dispatch note, leg 053 (2026-09-08, burndown)

**This leg runs in burndown mode, which adds one constraint to your unit: do not author a new
numbered decision.** Implement, document and fix freely; if you conclude this change genuinely
needs a new numbered decision in `embarch-umbrella/decisions/`, **stop and say so in your report**
instead, and leave the task file with a state line explaining what the decision would say.
Amending or correcting an *existing* decision is fine and is not this rule.

**Two things about this task specifically.** The `ensure_not_sourced` legacy-marker requirement in
the What section is the half that is easy to lose — a test pinning the legacy case is in the Done
when list and it is the item most worth landing. And when you pick the replacement strings, prefer
a decision *number* or a `decisions/<file>.md` path that `scripts/check-decision-refs.py` can
actually resolve; a fix line that names a second nonexistent document is this bug again.

**Doc-size reserve for `umbrella` — every one of these is inside the last 10% of its cap:**

| file | size/cap | headroom | filed against |
|---|---|---|---|
| `embarch-umbrella/spec.md` | 9784/10240 | 456 B | `tasks/umbrella/038-compact-umbrella.md` (open) |
| `embarch-umbrella/open.md` | 4630/5120 | 490 B | `tasks/umbrella/038-compact-umbrella.md` (open) |
| `embarch-umbrella/decisions/bind.md` | 11409/12288 | 879 B | `tasks/umbrella/009-compact-docs.md` (blocked, `In flux: yes`) |

Plan around this rather than discovering it. Two rules follow:

1. **If your work spends the reserve** — pushes a file into it, or leaves one there that nothing has
   filed — file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit, per
   `tasks/README.md`. Use `python3 scripts/check-task-numbers.py --next umbrella` for the number;
   do not read the directory.
2. **`umbrella/009` is blocked on `In flux: yes`, which parks the pass and not the reserve.** If an
   edit of yours would push `decisions/bind.md` *past* its cap, you compact that file as part of
   this unit — read `tasks/umbrella/009-compact-docs.md`'s `Must not delete:` list first, which is
   long and specific, and carry it verbatim. Otherwise aim net-neutral. `spec.md`'s eighteen-row
   `doctor` table and which of its rows are **designed and unbuilt** is on that list; do not
   shorten it as a side effect of this unit.
