# Stop `doctor` and `init` printing operators at documents the four-file split deleted

**State:** claimed by agent/umbrella/025-stale-doc-pointers, 2026-09-08 22:07
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
