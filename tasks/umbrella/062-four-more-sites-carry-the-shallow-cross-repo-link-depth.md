# 062 — Four more sites carry the shallow cross-repo link depth `doctor.rs` was fixed for

**State:** done
**Source:** `inbox/umbrella-more-shallow-cross-repo-links.md`, dropped while closing
`tasks/umbrella/061` (the `doctor.rs` cross-repo link-depth fix) and named there as outside that
task's scope. Filed by the leg of 2026-09-13 16:20.
**Scope:** umbrella
**Hardware:** none — comment and citation text only. No behaviour, no board, no running service.
**Owner:** no

## What

`umbrella/061` fixed four sites in `embarch-umbrella/src/doctor.rs` that wrote `../embarch-doc/...`.
`embarch-doc` is a sibling of `embarch-umbrella`, so from `embarch-umbrella/src/` the correct depth
is `../../embarch-doc/...`. The drop names four more sites in the same repo with the same defect:

| site | form |
|---|---|
| `src/config.rs:33` | backtick citation `` `../embarch-doc/embarch-umbrella/decisions/mirrors.md` `` |
| `src/config.rs:296` | same target, same form |
| `src/setup.rs:32` | markdown link `[embarch-core/spec.md](../embarch-doc/embarch-core/spec.md)` |
| `src/main.rs:220` | markdown link `[embarch-core/interfaces.md](../embarch-doc/embarch-core/interfaces.md)` |

**Verify each one against the real filesystem before and after**, the way `061` did — resolve the
path from the directory the file actually lives in and confirm the target exists. **Line numbers in
that table are already stale**: `suite/038` landed in `src/config.rs`, `src/init.rs` and
`src/doctor.rs` an hour before this was dispatched. Find the sites by their text, not by line.

## What to be careful about

- **Sweep the repo rather than trusting the list of four.** The drop found these by grep after
  fixing `doctor.rs`; run your own `grep -rn '\.\./embarch-doc' src/` and fix every site the same
  way. If the count is not four, say so — a list that was right an hour ago is evidence, not a
  bound.
- **Check the target exists, not only that the depth is plausible.** `../../embarch-doc/<path>` with
  a `<path>` that has since moved is the same defect with a longer prefix. Two of these name
  `embarch-core/spec.md` and `embarch-core/interfaces.md`; both are real files today — confirm it.
- **Do not change the citation *form*.** The drop notes that `embarch-core`'s own comments use a
  third, suite-root-relative form (`embarch-doc/embarch-core/interfaces.md`, no `../`), so the suite
  has two conventions and `DOC-CONVENTIONS.md` settles neither. **Picking one suite-wide is a
  decision and it is not yours** — fix the depth, leave the form alone, and if you think the suite
  should settle it, write an `inbox/` drop (absolute path:
  `/home/gabriel/Github/embarch/embarch-doc/inbox/`) rather than deciding.

## Why now

Same defect family as `061`, same repo, same root cause — a wrong depth copied as precedent. Two of
the four are markdown links printed into files a reader follows literally; `061`'s own finding was
that two of its sites were strings shown to an operator as a fix.

## Doc-size reserve for `umbrella`

`embarch-umbrella/decisions/bind.md` is at **93.9%** (11533/12288 B, **755 B left**), filed against
`tasks/umbrella/009-compact-docs.md` (blocked). Nothing else in `embarch-umbrella`'s doc tree is in
reserve. This unit should need no decision; if your work pushes any `embarch-umbrella` doc file into
its last 10%, file `tasks/umbrella/<next>-compact-umbrella.md` in the same commit
(`scripts/check-task-numbers.py --next umbrella` for the number).

## Done when

- [x] Every `../embarch-doc/` site in `embarch-umbrella/src/` resolves to a file that exists from the
      directory containing it, and your report states how many sites there were.
- [x] No citation changed form, only depth.
- [x] `cargo build` / `cargo test` / `cargo clippy --all-targets -- -D warnings` green in
      `embarch-umbrella`.
- [x] `changelog.d/` fragment in `embarch-doc`.
- [x] `python3 scripts/check-docs.py` green in `embarch-doc`.

## Result

Found exactly four sites, matching the drop's list (line numbers had shifted, text hadn't):
`src/config.rs:33`, `src/config.rs:291` (was :296), `src/setup.rs:32`, `src/main.rs:220`. A full
`grep -rn '\.\./embarch-doc' src/` after the fix turned up nothing shallower than `../../embarch-doc`;
`doctor.rs`'s six `061`-fixed sites were already correct. Two other `main.rs` sites
(`main.rs:3`, `main.rs:127`) use the suite-root-relative form (`embarch-doc/...`, no `../`) — left
alone per the task, since picking a suite-wide form is not this task's call.

Each fixed target confirmed to exist from its citing file's directory:
- `../../embarch-doc/embarch-umbrella/decisions/mirrors.md` (config.rs, both sites)
- `../../embarch-doc/embarch-core/spec.md` (setup.rs)
- `../../embarch-doc/embarch-core/interfaces.md` (main.rs)

Did not touch: the suite-root-relative citations, the `github.com/.../embarch-doc/...` URLs in
`deploy.rs`, or `DOC-CONVENTIONS.md` — the two-conventions question is flagged for the suite via an
`inbox/` drop, not decided here.
