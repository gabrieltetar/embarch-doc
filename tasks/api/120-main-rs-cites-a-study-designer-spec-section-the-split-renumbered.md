# 120 — `embarch-api/src/main.rs:538` cites a study-designer `spec.md` section number that split renumbered

**State:** claimed by agent/api/120-main-rs-spec-section-cite, 2026-09-29 21:05
**Source:** `inbox/api-stale-study-designer-spec-section-cite.md`, dropped by the
`study-designer/032` worker (2026-09-28) and filed by the supervisor at that unit's fold.
Splitting `embarch-study-designer/spec.md` §4 ("What a study carries") to `spec/carriage.md`
renumbered the old §5/§6/§7 down to §4/§5/§6. `embarch-api/src/main.rs:538` reads:

    // `embarch-study-designer` spec.md §7 already tracked from a smaller
    // 2-step case — this is that same bug, not a new one, just the first

Old §7 ("Constants", the `RUST_MIN_STACK`/host-shape-size note, `decisions/limits.md` decision 63)
is now §6. This is a simple integer citation that matched a real heading before the split — not
one of the legacy `§4.8`/`§5.1`-style decimal citations `embarch-core/src/study.rs` carries, which
never matched a current heading and are out of scope here. `embarch-study-designer`'s own
`src/study.rs` had the same citation and was repointed in `b9a2d5d`.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Repoint the comment at `embarch-api/src/main.rs:538` from `spec.md §7` to what it actually means.
**Prefer the decision over the section number**: cite `embarch-study-designer` decision 63
(`decisions/limits.md`), which is what that section points at and which survives the next split,
where a section number does not. `spec.md §6` is the fallback if the comment reads worse that way.

## Why now

A cross-repo section citation the `study-designer/032` split made stale. That worker could not fix
it — `embarch-api` is outside its ownership row.

## Done when

- [x] `embarch-api/src/main.rs:538`'s comment cites decision 63 (or `spec.md §6`), and says so in
      the report. Repointed to `embarch-study-designer` decision 63 (`decisions/limits.md`).
- [x] `grep -rn 'spec.md §' src/ crates/` in `embarch-api` shows no other citation into
      `embarch-study-designer/spec.md` by a section number that moved. Grep returns nothing.
- [x] Gate green in `embarch-api` (`cargo build`/`test`/`clippy --all-targets -- -D warnings`,
      `check-client-names.py`), `changelog.d/` fragment. All green;
      `changelog.d/api-spec-section-cite.fixed.md` added.
