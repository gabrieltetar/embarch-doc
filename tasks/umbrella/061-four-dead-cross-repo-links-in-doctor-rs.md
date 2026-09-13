# 061 — Four cross-repo relative links in `doctor.rs` resolve to nothing, and two are strings an operator reads

**State:** claimed — leg 108, unit 2, 2026-09-13, branch `agent/umbrella/061-doctor-cross-repo-links`.
**Doc-size reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` 11533/12288 B (**755 B
left**, filed as blocked `tasks/umbrella/009`). This task should need no new decision — it is link
text in comments and `fix` strings — but if you conclude one is owed, check
`embarch-umbrella/decisions.md`'s index and pick the right topic file rather than the nearest one.
If you push any `umbrella` doc into reserve, file `tasks/umbrella/<NNN>-compact-docs.md` in the same
commit.
**Source:** the reviewer pass on `umbrella/060` (merge `b9452abd`), filed to `inbox/` by leg 107 and
taken into the queue by leg 108 (2026-09-13).
**Scope:** umbrella
**Hardware:** none — comment text and two `fix` strings. No behaviour, no board.
**Owner:** no

## What already happened, so nobody fixes it twice

`060` changed `src/doctor.rs:1269`'s markdown link from `../../embarch-doc/...` to
`../embarch-doc/...`, on the ground that two other sites in the same file already used the shallower
form. **That precedent is itself broken**, so a working link was made dead by matching a dead one.
**The supervisor reverted line 1269 in `umbrella/060`'s own fold** (`319f0357`) — that half is done
and is **not** this task. Do not touch line 1269.

The filesystem, verified against the real checkouts (no symlink, no submodule — plain sibling
directories):

- `src/doctor.rs` lives at `embarch-umbrella/src/doctor.rs`, and `embarch-doc` is a **sibling of
  `embarch-umbrella`**, not a child of it.
- `../embarch-doc/...` from `src/` resolves to `embarch-umbrella/embarch-doc/...` — **does not
  exist.**
- `../../embarch-doc/...` resolves to `embarch/embarch-doc/...` — **exists.**

## What is left

Four sites still carry the dead shallow form:

| site | what it is | text |
|---|---|---|
| `doctor.rs:721` | **a `fix` string an operator reads** | `"see ../embarch-doc/embarch-token.md"` |
| `doctor.rs:750` | **a `fix` string an operator reads** | `"...doesn't match Core's. See ../embarch-doc/embarch-token.md — if ..."` |
| `doctor.rs:569` | rustdoc link | `[decision 43](../embarch-doc/embarch-umbrella/decisions/message-rendering.md)` |
| `doctor.rs:2753` | rustdoc link | `[embarch-token.md](../embarch-doc/embarch-token.md) §5's` |

Line numbers are from before `319f0357` landed — **re-grep rather than trusting them.**

The two `fix` strings matter most: `doctor` prints them to a human who is being told where to go
read, and the path they name does not exist from anywhere.

## Worth settling while you are there

`embarch-core` does not use a relative form at all — its comments say
`embarch-doc/embarch-core/interfaces.md`, suite-root-relative, with no `../`. So this file's
convention disagrees with a sibling repo's, and **`DOC-CONVENTIONS.md` governs decision citation
form but says nothing about cross-repo relative-link depth.** Either form works as prose; only one
of them works as a link from `src/`. Pick one for this file, apply it to all four, and say in the
report which and why. **Do not amend `DOC-CONVENTIONS.md`** — that file is reserved, and a
convention gap is an `inbox/` drop, not an edit.

## Done when

- [ ] All four sites resolve to a file that exists from `embarch-umbrella/src/`.
- [ ] The two `fix` strings still read as instructions, not as citations.
- [ ] The report names the form chosen and why, and whether any further site in `doctor.rs` shares
      the defect.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.
