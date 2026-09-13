# 053 — `resolve_probe`'s doc comment still calls `board_gate.rs` this crate's own file, 42 lines above the comment that gets it right

**State:** claimed — leg of 2026-09-13 16:20, `agent/core/053-resolve-probe-board-gate-comment`
**Source:** `inbox/core-hardware-rs-stale-board-gate-comment.md`, dropped by `core/052`'s worker
while re-verifying that task's ride-alongs and named there as out of its own scope. Filed by the leg of 2026-09-13 16:20 (the
leg-number field is self-assigned and has collided twice today; the timestamp is the handle).
**Scope:** core
**Hardware:** none — a source doc comment, nothing executed.
**Owner:** no

## What

`embarch-core/src/hardware.rs:74`, the doc comment on `resolve_probe`, asserts as present tense that
this function is *"also `board_gate.rs`'s one and only source of 'which probe did this call mean'
(`enforce`/`enroll`)"*. **`src/board_gate.rs` does not exist in this crate** — verify that yourself
(`ls`/`git ls-files`) before touching anything; the drop's claim is the thing you are checking, not a
premise you inherit.

42 lines later, `open_probe`'s own doc comment (`src/hardware.rs:116`) already carries the corrected
story in the form this repo settled on: *"`embarch_topology::hardware::validate_serial` (the
board-identity gate, formerly this crate's own `board_gate.rs`)"*. Line 74 was never updated when the
gate moved out; line 116 either was, or was written afterwards. **Reword line 74 to match line 116's
phrasing** — name `embarch_topology::hardware::validate_serial` as the board-identity gate and say
`board_gate.rs` only in the past tense, or not at all.

## What to be careful about

- **Keep the claim, fix the referent.** The sentence is doing real work: it explains why
  `resolve_probe` is `pub(crate)` rather than a private helper, and that the selection rule is shared
  rather than copied. A reword that deletes the reason leaves the visibility unexplained. Two
  consecutive legs have now had a reviewer check whether a deletion lost a fact; do not create one.
- **Check the decision citation in the same comment before you keep it.** The passage ends
  *"(see decision 9's own text)"*. Read decision 9's body — not the index line — and confirm it still
  says what the comment says it says. If it does not, say so in your report; repointing it is in
  scope only if you can re-derive the correct number from the decision bodies themselves. If you
  cannot, leave the number alone and name the problem rather than guessing.
- **Do not sweep.** Other stale citations in this repo are somebody else's task. Fix line 74 and
  anything line 74's own sentence directly makes false.

## Why now

Same drift class `core/052` fixed in `embarch-core/README.md` the unit before: a comment naming a
file that moved to another crate, read next by whoever lands in that function. It is one comment, it
is verified against the filesystem, and the corrected wording already exists 42 lines below it.

## Doc-size reserve for `core`

`embarch-core/decisions/auth.md` is at **92.4%** (11356/12288 B, **932 B left**), filed against
`tasks/core/046-compact-core.md` (blocked, `In flux: yes`, size debt due 2026-09-26). Nothing else in
`embarch-core`'s doc tree is in reserve. This unit should not need to write a decision at all; if it
somehow does, it does not go in `auth.md`, and if your work pushes any `embarch-core` doc file into
its last 10% you file `tasks/core/<next>-compact-core.md` in the same commit
(`scripts/check-task-numbers.py --next core` for the number).

## Done when

- [ ] `src/hardware.rs:74`'s doc comment names `embarch_topology::hardware::validate_serial` as the
      board-identity gate and does not assert `board_gate.rs` as a file in this crate.
- [ ] The reason the function is `pub(crate)` survives the reword.
- [ ] Decision 9's citation in that same comment is read against decision 9's body and either kept,
      corrected with the derivation stated, or flagged in your report.
- [ ] `cargo build` / `cargo test` / `cargo clippy --all-targets -- -D warnings` green in
      `embarch-core`.
- [ ] `changelog.d/` fragment in `embarch-doc`.
- [ ] `python3 scripts/check-docs.py` green in `embarch-doc`.
