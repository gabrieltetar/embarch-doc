# 106 — The 18 singular-wrapped citations: the form even `core/068`'s wrap-check could not see

**State:** done — worker agent/api/106-singular-wrapped, 2026-09-16. 18 lines, 20 decision-number
instances checked; 0 wrong numbers, 0 dead references, 0 false sentences; no edits needed.
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

- [x] All 18 lines checked, with the count of distinct decision instances behind them reported.
- [x] Every wrong number, dead reference or false sentence fixed; every line deliberately left
      alone named with the reason.
- [x] The measurement repeated after the edits, so the closing report states a number rather than
      an impression.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build --all-targets`,
      `cargo test`, `cargo clippy --all-targets -- -D warnings` in `embarch-api`, and
      `check-docs.py` in `embarch-doc`.
- [x] `changelog.d/` fragment dropped. No decision is created or amended unless you find one that
      is actually wrong, in which case say so rather than editing quietly.

## Result

Re-ran `grep -rInE '[Dd]ecisions?[[:space:]]*$' embarch-api --include='*.rs' --include='*.toml'`
(target excluded): the same 18 lines the task filed, no others. Each line's wrapped citation was
read in its surrounding sentence, resolved against the repo the sentence actually names (not the
grep column — several of these are cross-repo: `embarch-core` decisions 31, 62 and `embarch-ui`
decision 14 sit among the eighteen), and checked against that decision's current text.

Every one of the 18 checked out clean:

- 15 lines cite exactly one decision number each: `config.example.toml:82` (api/40),
  `src/main.rs:539` (api/52), `tests/json_surface.rs:3` (api/50), `src/build.rs:51` (api/19),
  `src/reflash.rs:6` (`embarch-core`/31), `src/reflash.rs:182` (api/40), `src/resolve.rs:17`
  (api/21), `src/resolve.rs:310` (api/51), `src/zephyr.rs:445` (api/12),
  `crates/embarch-core-client/src/user_dirs.rs:9` (`embarch-ui`/14), `src/config.rs:255` (api/32),
  `src/tools.rs:101` (api/12), `crates/.../client.rs:17` (api/11), `crates/.../client.rs:346`
  (api/73), `crates/.../client.rs:355` (api/73), `crates/.../client.rs:841` (api/60), and
  `crates/.../client.rs:1723` (`embarch-core`/62).
- 1 line, `src/logging.rs:26`, cites three: "(decisions 4 and 3, 10)" — `Mode::Mcp` against
  decision 4 ("MCP over stdio"), `Mode::Cli` against decisions 3, 10 ("Three responsibilities, and
  a CLI alongside MCP") — matching `decisions.md`'s own merged heading for 3/10.

**18 lines / 20 decision-number instances, 0 wrong numbers, 0 dead references, 0 false sentences.**
No edits needed anywhere in `embarch-api`.

Two lines got the extra read the task flagged: `src/reflash.rs:182` ("the difference is decision
40's verification asymmetry") is the sentence's object, re-checked as prose rather than a
parenthetical — it states exactly what `study-reflash.md` decision 40 says ("the difference *is*
the verification asymmetry showing up as control flow"). `src/config.rs:255`'s "dev-bench remains
... one at a time" was checked against decision 45 (which falsifies "there is exactly one
dev-bench board" as a *board-identity* premise) — decision 45 itself says "the bench is still one
at a time" for the build-lock key, so the citation still holds; the two decisions are about
different axes (which board vs. how many concurrently).

No comment blocks were reflowed; only the task file and one `changelog.d/` fragment changed.
`embarch-api/spec.md` untouched (9,102/10,240 B, unchanged) — no compact task needed.
