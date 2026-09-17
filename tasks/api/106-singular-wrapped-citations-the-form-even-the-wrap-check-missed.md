# 106 — The 18 singular-wrapped citations: the form even `core/068`'s wrap-check could not see

**State:** open
**Source:** leg 128's refill sweep, 2026-09-16, measured directly rather than inferred. `core/068`
found on 2026-09-16 that a citation wrapped across a comment continuation is invisible to a
line-based census, and its fix was the grep `grep -rlIE '[Dd]ecisions[[:space:]]*$'` — **plural
only**. Re-running it with the singular alternation, `grep -rInE '[Dd]ecisions?[[:space:]]*$'`,
finds **18 lines in 12 files** in this repo, and `api/104`'s plural re-check (which closed clean at
13 lines / 29 instances) could not have seen any of them.
**Scope:** api
**Hardware:** none — Rust doc comments, one `config.example.toml` comment and one test-file header.
Nothing is built for a board, no probe, no live Core, no deploy, no study. Classified fresh at
filing.
**Owner:** no

**Doc-size reserve for `api`:** `embarch-api/spec.md` (9,102/10,240 B, 1,138 B left) is in the last
10% of its cap, filed as `tasks/api/083-compact-api.md`, **blocked**. This is a source-comment sweep
and should not need to write it; if you must, spend the bytes and say so in your report. If your
work pushes any other `api` doc into reserve, file `tasks/api/<next free NNN>-compact-api.md` in the
same commit per `tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Eighteen lines, measured 2026-09-16 with
`grep -rInE '[Dd]ecisions?[[:space:]]*$' embarch-api --include='*.rs' --include='*.toml'`, target
excluded:

```
config.example.toml:82                              (decision
tests/json_surface.rs:3                             decisions.md` decision
src/main.rs:539                                     (decision
src/logging.rs:26                                   (decisions
src/resolve.rs:17                                   (decision
src/resolve.rs:310                                  (decision
src/reflash.rs:6                                    (`embarch-core` decision
src/reflash.rs:182                                  is decision
src/config.rs:255                                   (decision
src/build.rs:51                                     (decision
src/tools.rs:101                                    (decision
src/zephyr.rs:445                                   per decision
crates/embarch-core-client/src/user_dirs.rs:9       (`embarch-ui` decision
crates/embarch-core-client/src/client.rs:17         (config.rs, decision
crates/embarch-core-client/src/client.rs:346        (`embarch-api` decision
crates/embarch-core-client/src/client.rs:355        `embarch-api` decision
crates/embarch-core-client/src/client.rs:841        per `embarch-api` decision
crates/embarch-core-client/src/client.rs:1723       (`embarch-core` decision
```

The number lives on the **next** line. Three spot-checks confirmed the shape before this task was
filed — `src/build.rs:51-52` continues `/// 19).`, `src/logging.rs:26-27` continues
`/// 4 and 3, 10)`, and `crates/.../client.rs` carries several.

Re-check each citation the way every sweep in this chain has: does the number resolve, does it
resolve in the repo the line names, and does the sentence around it still assert something true.
Fix what is wrong; leave what is right and say so.

## Why now

**This is the first read of these lines, not a re-read.** `embarch-api` has been declared swept
several times over; every one of those censuses used a grep that could not match this form, exactly
as `api/104` was the first read of the plural form. Two of the three repos that ran the plural
wrap-check found citations no earlier sweep could see, and `ui/061` found that a citation whose
numbers all resolve can still assert a false relationship — so a clean number is not a clean line.

`crates/embarch-core-client/` is where four of the eighteen sit, and it is the crate `embarch-ui`
and `embarch-umbrella` both path-depend on, so a wrong number there is read from three repos.

## Careful of

- **The repo-prefix trap, in its sharpest form.** Several of these lines name a *different* repo's
  decisions (`embarch-core`, `embarch-ui`) and several name this one; on a wrapped line the prefix
  and the number are on different lines, so the usual glance is even less reliable. Read the code
  to decide whose decision a number is, never the grep column.
- **`src/reflash.rs:182`** reads `...the difference is decision` — the citation is the sentence's
  object, not a parenthetical, so re-wrapping it carelessly changes what the sentence says.
- Do **not** reflow comment blocks wholesale to "fix" the wrapping. The wrap is not the defect; an
  unchecked citation is. Changing line breaks across twelve files would bury the real edits.

## Done when

- [ ] All 18 lines checked, with the count of distinct decision instances behind them reported.
- [ ] Every wrong number, dead reference or false sentence fixed; every line deliberately left
      alone named with the reason.
- [ ] The measurement repeated after the edits, so the closing report states a number rather than
      an impression.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build --all-targets`,
      `cargo test`, `cargo clippy --all-targets -- -D warnings` in `embarch-api`, and
      `check-docs.py` in `embarch-doc`.
- [ ] `changelog.d/` fragment dropped. No decision is created or amended unless you find one that
      is actually wrong, in which case say so rather than editing quietly.
