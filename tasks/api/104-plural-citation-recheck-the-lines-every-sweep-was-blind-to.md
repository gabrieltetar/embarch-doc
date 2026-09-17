# 104 — Plural-citation re-check: the 13 lines every `api` sweep was structurally blind to

**State:** done — worker agent/api/104-plural-citation-recheck, 2026-09-16. 13 lines, 29 instances
checked against the 13-line floor; 0 wrong numbers, 0 false sentences; no edits needed.
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-api` was declared citation-swept after `api/095`, `097`, `101` and `102`. **Every one of
those sweeps censused with `grep -cE '[Dd]ecision [0-9]'`, which cannot match `decisions 2/8/14` or
`decisions 50, 55`** — so these lines were never in any sweep's input at all. This is not a re-read
of checked work; it is the first read.
**Scope:** api
**Hardware:** none — doc comments, one `Cargo.toml` comment, one workflow comment and one MCP tool
description string. Nothing is built for a board, no probe, no live Core, no deploy, no study, no
route called. Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `api`:** one file, `embarch-api/spec.md` at **9,102/10,240 B (1,138 B left)**,
filed as `tasks/api/083` and **blocked**. Nothing else in scope is in reserve. A source-comment
sweep should not need to write it; if it does, say why. If your work leaves an `api` doc inside the
last 10% of its cap with nothing filed against it, file `tasks/api/<next free NNN>-compact-api.md`
in the same commit per `tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Thirteen lines, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo excluding
`.git` and `target`:

```
tests/study_events_sse.rs:664                       decisions 48/49          bare — own repo
crates/embarch-core-client/Cargo.toml:13            decisions 2/8/14         (topology, per context)
crates/embarch-core-client/src/api_log.rs:18        `embarch-topology` decisions 2/8/14
src/main.rs:87                                      (decisions 3, 10)        bare — own repo
src/main.rs:324                                     (embarch-api decisions 58/59)
src/cli.rs:1503                                     (decisions 3/10; `suite/features.md`'s ...)
.github/workflows/release.yml:21                    embarch-umbrella decisions 27/29
crates/.../client.rs:403                            (decisions 37, 38) + `embarch-topology` decision 31
crates/.../client.rs:543                            `embarch-outpost` decisions 4, 17
crates/.../client.rs:1065                           `embarch-topology` decisions 2, 3
crates/.../client.rs:1127                           `embarch-api` decisions 50, 55
src/tools.rs:916                                    an MCP tool description string — read the whole line
crates/.../token_discovery.rs:76                    `embarch-topology` decisions 4, 8
```

**Thirteen lines, roughly 30 distinct decision instances** — treat the line count as a floor and
report the instance count you actually checked.

Three things to notice:

- **`crates/embarch-core-client/Cargo.toml:13` carries no repo prefix at all** — *"decisions 2/8/14
  already established for topology detection/enrollment"* — and the sibling line at `api_log.rs:18`
  spells the same three numbers **with** the `embarch-topology` prefix. The bare one is the one to
  check, and if it is right it is right by luck of a neighbouring word rather than by the chain's
  own rule.
- **`src/tools.rs:916` is a shipped MCP tool description**, so whatever it claims travels to an
  agent client, not just to a reader of the source. `tasks/ui/038` records the same class — a
  same-repo citation in a shipped string — as an open question about citation *form*; do not settle
  that here, just check the numbers and the sentence.
- **`client.rs:403` mixes a plural and a singular citation on one line**, so a sweep that found the
  singular half may have read the line and still not checked `decisions 37, 38`. `api/085` left four
  `embarch-core` decision 22 citations in this same file standing for a contextual look
  (`inbox/api-stale-decision-22-citations-remaining.md`, if it is still there); that is a different
  finding and is not yours to close here.

## How

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** Report your number against the
   thirteen above.
2. **For each cited number, check the decision exists in the file the citation points at**, and
   remember a bare `decision NN` in another sub-project's file means *that* sub-project's NN.
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** `api/102` found a comment citing a real, existing, topically wrong decision
   this way, and `study-designer/054` found a citation that went false when another repo amended
   the decision it cited. A number that resolves is not a sentence that holds.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation is a finding for `inbox/`, not an edit.

## Done when

Every plural-form citation line in `embarch-api` has had the existence-and-truth pass, the report
states the instance count checked against the thirteen-line floor, and each defect found is either
fixed here or filed with its reason for not being fixed here.

## Result

**Re-census with `[Dd]ecisions? [0-9]` found exactly the same 13 lines** as the filing task's
`[Dd]ecisions [0-9]` census — a broader check for any `decisions`-then-non-digit-then-digit form
(parenthesized, comma-first, etc.) turned up nothing further, so 13 lines is the true floor here,
not just the mandatory-plural-form one.

**13 lines, 29 distinct decision-number instances, all checked for existence and for the sentence
around each still being true:**

| Site | Decision(s) cited | Repo | Verdict |
|---|---|---|---|
| `tests/study_events_sse.rs:664` | 48, 49 | api, own (bare) | correct — `study-events.md` #48/49; the no-per-request-timeout claim matches decision 48's "Core holds the stream open indefinitely" and the `timeout: None` streaming design at `client.rs:1127` |
| `crates/embarch-core-client/Cargo.toml:13` | 2, 8, 14 | topology (bare, no prefix) | correct — `crate.md` #2 (shared crate, one impl), `consumer-boundary.md` #8 ("one implementation, multiple call sites" — the exact phrase quoted), `enrollment.md` #14 (which states it extends "decision 8's principle... to enrolling as well as validating"), together covering both "detection" and "enrollment" as claimed |
| `crates/embarch-core-client/src/api_log.rs:18` | 2, 8, 14 | topology (prefixed) | correct, same three decisions, same verdict as above |
| `src/main.rs:87` | 3, 10 | api, own (bare) | correct — `shape.md` #3/10 ("a CLI alongside MCP... two front-ends over one set of modules") |
| `src/main.rs:324` | 58, 59 | api | correct — `client-crate.md` #58 (older-Core `Option<T>`/`#[serde(default)]` parsing rule) and `hardware-selection.md` #59 (`dev_bench_hello`'s three identity fields); the sentence's `embarch-core decision 47` aside also checked and correct (`handshake.md` #47, the `hardware_id`→`self_reported_hardware_id` rename) |
| `src/cli.rs:1503` | 3, 10 | api, own (bare) | correct, same two decisions as `main.rs:87` |
| `.github/workflows/release.yml:21` | 27, 29 | umbrella | correct — `release.md` #27/29 (one entry under two numbers, per that file's own note); sentence about gating the build matrix on a `--version`/tag mismatch matches |
| `crates/embarch-core-client/src/client.rs:403` | 37, 38 (+ topology 31, singular) | api, own + topology | correct — `client-crate.md` #37/38 ("this crate must never have probe-rs/serialport") and topology `crate.md`#31 ("wire feature... plain data types, pure serde, no C toolchain"); decision 72 (api's own) tells the identical story in its own words, confirming both halves |
| `crates/embarch-core-client/src/client.rs:543` | 4, 17 | outpost | correct — `layout.md` #4 (DUT's per-record `cycles` measures) and `clocks.md` #17 (two clocks, cycles measures/rx_utc_ms places) — matches the comment's "Core's own receipt time... DUT's own per-record cycles" exactly |
| `crates/embarch-core-client/src/client.rs:1065` | 2, 3 | topology | correct — `crate.md` #2/3 (shared crate, live in-process, no write-ahead file) |
| `crates/embarch-core-client/src/client.rs:1127` | 50, 55 | api | correct — `surface.md` #50 ("unconditional by construction, not by convention" — the literal phrase) and `client-crate.md` #55 (the one bearer-auth funnel) |
| `src/tools.rs:916` | 58, 59 | api | correct, same two decisions and same verdict as `main.rs:324` — read as a whole line since it is a shipped MCP tool description; the `embarch-core decision 47` aside is also correct. Not settling `ui/038`'s open question about same-repo citation *form* in a shipped string, per the task's own instruction — just the numbers and the sentence |
| `crates/embarch-core-client/src/token_discovery.rs:76` | 4, 8 | topology | correct — `consumer-boundary.md` #4/8, and #8's own text is the literal phrase quoted in the comment ("one implementation, called live, not mirrored") |

**0 wrong numbers, 0 false sentences. No edits made anywhere in `embarch-api`** — every citation
already checks out, so there is no fact to fix. `client.rs:403`'s mixed plural+singular line was
read as a whole per the task's warning; both halves check out independently.

`inbox/api-stale-decision-22-citations-remaining.md`'s four `embarch-core` decision 22 citations in
`client.rs` (lines 199, 381, 1249, 1333) are singular-form and outside this task's scope; not
touched, not widened into.

No `api` doc entered or left the last-10%-of-cap reserve — this was a source-comment-only sweep, no
`spec.md`/`decisions.md`/`open.md` edits were needed since no defect was found, so nothing new to
file against `tasks/api/083`.

`cargo build`, `cargo test --workspace` (46 passed), `cargo clippy --all-targets -- -D warnings` all
green in `embarch-api`, `crates/embarch-core-client` included as a workspace member.
