# 092 — A history roll breaks every relative link it moves, and the reserve demands a debt for a file that rolls itself

**State:** done — `roll_if_over_cap` re-bases moved links (`rebase_links`, `scripts/test_build_changelog.py`); `history` role exempt from the reserve, DOC-BUDGET.md row says so; replaying the real 2026-10-26 roll writes the hand-fixed bytes (owner/doc-size, 2026-10-29)
**Source:** the 2026-10-26 07:42 leg, folding `api/136`. The fold's `build_changelog.py --only` pushed
`history/api.md` to 18,475 / 20,480 B (90.2%), and `check-doc-size.py` failed "1 file(s) in reserve with
no debt filed". The supervisor paid it by calling `build_changelog.roll_if_over_cap` with the cap
lowered to 18,000 B, which moved the `## 2026-09` window to `history/archive/api-2026-09--2026-09.md`;
`check-links.py` then went red on 19 links in the moved window, all `](../embarch-api/...)`, correct
from `history/` and one directory short from `history/archive/`. Fixed by hand in that file.
**Scope:** doc
**Hardware:** none
**Owner:** required — both fixes are in `scripts/` (`build_changelog.py`, `check-doc-size.py`), which
`check-ownership.py --supervisor` reserves.

## What

Two defects, both met the first time any `history/<scope>.md` approached its cap.

1. **`roll_if_over_cap` copies a window verbatim into `history/archive/`** without re-basing relative
   links. Every `](../<path>)` in a fragment is written relative to `history/`, so in the archive it
   points one level short. The first real roll at the 20 KB cap would turn `check-docs.py` red inside a
   fold, on a file the fold never meant to touch. Re-base `](../` to `](../../` on the moved text (and
   keep `../<scope>.md` back-links right), or have fragments link from the repo root.
2. **`check-doc-size.py`'s reserve rule applies to `history/*.md`**, which the assembler rolls by
   itself at the cap. A filed compaction task is the wrong remedy (no worker may write `history/`, and
   the roll is mechanical); either exempt the role from "no debt filed", or make the assembler roll at
   the reserve line rather than the cap, so the file never rests inside it.

## Done when

- [x] A roll leaves `check-links.py` green, with a test that rolls a window holding a relative link.
- [x] A history file inside its reserve either fails nothing or rolls at assembly; the docs that state
      the cap (`DOC-BUDGET.md` row, the history header sentence) agree with what the code does.
