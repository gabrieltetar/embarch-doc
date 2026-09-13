# 045 — `study_designer.rs:1524` cites `§4.3` for `Uuid`'s serialize form, and `§4.3` was never about `Uuid`

**State:** open
**Source:** the `embarch-reviewer` on `ui/044`, 2026-09-13, flagged deliberately as a report note
rather than a finding — it is a citation-accuracy defect, not a contradiction of any decision, and it
predates the unit the reviewer was reading. Filed by the supervisor (leg 109).
**Scope:** ui
**Hardware:** none — one doc comment, no logic change.
**Owner:** no

## What

`embarch-ui/src/study_designer.rs:1524` cites `embarch-study-designer/interfaces/types.md §4.3` for
`Uuid`'s raw-array-versus-hyphenated `Serialize` form.

**`ui/044` checked this site and correctly left it alone** — its *file* is right, because the `Uuid`
material is `Action`/GATT content that did **not** move in `study-designer/038`'s split. What the
reviewer then found by going further is that the *section* was never right:

- `interfaces/types.md` carries no numbered headings and has not since the 2026-09-02 split, so
  `§4.3` resolves to nothing today.
- In the pre-split monolithic `design.md`, where `§4.3` did exist, **it was `Action`** — not this
  raw-array note.
- No interfaces file (`types.md`, `gatt-types.md`, `result-types.md`) and no
  `embarch-study-designer` decision describes that raw-array-versus-hyphenated split under any
  section number at all.

So this is an imprecise citation carried through the repo-wide `design.md` sweep (`eca2fa1`)
unchanged, and it has pointed at the wrong thing for longer than the split has existed.

## Done when

- [ ] `study_designer.rs:1524`'s citation names something that is actually there. **Find where the
      raw-array `Serialize` form is documented before you edit** — if it is documented nowhere, say
      so in the task file and drop the section number rather than inventing one, which is what
      `ui/044` did with the dead `§4.8` on line 780 and is this repo's established precedent.
- [ ] A statement, either way, of whether the raw-array form is documented anywhere in
      `embarch-study-designer`. **If it is not, that is a finding worth more than this fix** — drop
      it in `inbox/` at the absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/` for the
      supervisor to file against `study-designer`, because an undocumented serialization form that
      two repos depend on is a different and larger problem than a bad pointer to it.
- [ ] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green in
      `embarch-ui`. A doc comment, so this is confirmation rather than risk.
- [ ] `changelog.d/` fragment only if something reader-visible changed; say which way you judged it.
      `ui/044` judged the equivalent repoint not reader-visible and did not drop one.

## Why now

Cheap, and it closes `embarch-ui`'s half of a class the suite has now paid for four times in a
fortnight (`core/050`, `dev-bench/030`, `study-designer/039`, `ui/044`). After this, **both** of the
two `embarch-study-designer/interfaces` citations in `embarch-ui` are correct — the reviewer's grep
found exactly two in the whole repo, so this task finishes the sweep rather than sampling it.

## Not in scope

- `tasks/study-designer/041`, the same defect class in `embarch-study-designer`'s own docs
  (40 `§N` references into the retired `design.md`). Different repo, different owner, already filed.
- `study_designer.rs:780`, fixed by `ui/044` and landed at `364afe3`.
