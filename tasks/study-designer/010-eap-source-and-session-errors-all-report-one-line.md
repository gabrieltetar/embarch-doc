# Give `.eap` source and session errors their own source line

**State:** claimed by agent/study-designer/010-eap-error-lines, 2026-09-08 22:07
**Source:** owner's repo survey, 2026-09-06 — `interfaces/eap.md` states line-accurate errors as a property; it is untrue for a whole class
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`src/eap_parse.rs:1167` computes `line0` as *the first state's* line, then uses it for every
source-scoped error (`:1175`, `:1182`, `:1187`), every session-variable error (`:1322`, `:1328`,
`:1330`) and the protocol-name and validate errors (`:1430`, `:1439`). So a duplicate `source`
declared at line 4 of a long manifest is reported at whatever line the first `state` happens to sit
on. `EapError`'s own doc at `:110-113` says each error carries the source line; the only test of
that (`:1752-1758`) covers a lexer error.

`AstProtocol`'s sources and session variables should carry the line they were parsed at, and
`resolve` should report each error against its own declaration.

## Why now

`decisions/protocols.md` decision 58 justifies a purpose-built grammar over TOML on legibility, and
`interfaces/eap.md` states line-accurate errors as a property of it. This is that property being
untrue for every error an author is most likely to hit.

## Done when

- [x] Sources and session variables carry a line through the AST, and no resolve-time error for
      either uses `line0`.
- [x] Tests assert the reported line for a duplicate source, an over-long source name and a
      duplicate session variable, in a manifest where the first `state` is many lines away.
- [x] The remaining uses of `line0` (protocol name, `validate_protocol`) are either given a real
      line or documented as protocol-wide.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features eap-parse`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Resolution (2026-09-08, agent/study-designer/010-eap-error-lines)

`AstProtocol::sources`/`session` each now carry the line they were declared at (captured in the
parser), and `resolve` reports duplicate/over-long-name errors against that line rather than
`line0`. `line0` itself is gone: the protocol-name error and `validate_protocol`'s error now use a
new `AstProtocol::line` (the `protocol <name> {` line) — a real line, not the first state's, chosen
because `validate_protocol` runs over the resolved, index-only `ProtocolDef` and its checks can
span several states/frames/sources at once, so no single declaration line is "the" line for one of
its failures; the protocol's own opening line is the smallest scope that legitimately covers all of
them. No new numbered decision: this is a repair of the line-accuracy property decision 58 and
`interfaces/eap.md` already claim, not a new one. `spec.md`, `decisions.md` and `open.md` did not
need edits — none of them state the bug's wrong behavior as fact, so nothing there was false.
`changelog.d/study-designer-eap-source-session-error-lines.fixed.md` dropped; no `status.d/`
fragment, since nothing suite-level changed (this is an internal parser-only fix, no capability
shipped/retired/changed maturity). Gate green: `cargo build`, `cargo test`,
`cargo test --no-default-features --features eap-parse`, and
`cargo clippy --all-targets -- -D warnings` all pass in the code worktree; `check-docs.py`,
`check-client-names.py --repo <code worktree>` and `check-ownership.py` (both repos) all pass.

## Supervisor's dispatch note, leg 053 (2026-09-08, burndown)

**This leg runs in burndown mode, which adds one constraint to your unit: do not author a new
numbered decision.** Implement, document and fix freely; if you conclude this change genuinely
needs a new numbered decision in `embarch-study-designer/decisions/`, **stop and say so in your
report** instead, and leave the task file with a state line explaining what the decision would say.
Amending or correcting an *existing* decision is fine and is not this rule. Note that this task is
squarely a *repair of a property decision 58 and `interfaces/eap.md` already claim*, so it should
need no new decision at all — if it seems to, that is the signal to stop and report.

**The third Done-when item is the one with a judgement in it.** `line0`'s remaining uses (the
protocol name at `:1430` and `validate_protocol` at `:1439`) may legitimately be protocol-wide
rather than a bug; if you conclude they are, say so in `interfaces/eap.md` in one sentence rather
than inventing a line for them. What must not survive is a source or session-variable error still
reported at the first state's line.

**Doc-size reserve for `study-designer` — every one of these is inside the last 10% of its cap:**

| file | size/cap | headroom | filed against |
|---|---|---|---|
| `embarch-study-designer/decisions/registry.md` | 11827/12288 | 461 B | `tasks/study-designer/019-compact-study-designer.md` (open) |
| `embarch-study-designer/open.md` | 4662/5120 | 458 B | `tasks/study-designer/006-compact-study-designer.md` (blocked, `In flux: yes`) |
| `embarch-study-designer/spec.md` | 9136/10240 | 1104 B | `tasks/study-designer/006-compact-study-designer.md` (blocked) |

Plan around this rather than discovering it. Two rules follow:

1. **If your work spends the reserve** — pushes a file into it, or leaves one there that nothing has
   filed — file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit, per
   `tasks/README.md`. Use `python3 scripts/check-task-numbers.py --next study-designer` for the
   number; do not read the directory.
2. **`study-designer/006` is blocked on `In flux: yes`, which parks the pass and not the reserve.**
   If an edit of yours would push `open.md` or `spec.md` *past* its cap, you compact that file as
   part of this unit — read that task's `Must not delete:` list first and carry it verbatim,
   closing only that file's item. Otherwise aim net-neutral.
