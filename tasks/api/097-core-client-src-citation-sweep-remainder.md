# 097 — Citation sweep remainder: `embarch-core-client/src/client.rs`

**State:** done — `agent/api/097-core-client-src-citation-sweep-remainder`, leg 116, 2026-09-16
**Source:** `tasks/api/095`, cut short by a fleet stop mid-sweep on 2026-09-14. `095` read the whole
file end to end (2625 lines, all citation contexts noted) but cross-checked citations against the
cited decision's **body** for only six decision files before stopping. This task is the remainder:
finish the primary-source check for everything below.
**Scope:** api
**Hardware:** none — source comments only.
**Owner:** no

**Doc-size reserve for `api` (leg 116, 2026-09-16): one file.** `embarch-api/spec.md` is
9,102/10,240 B, 1,138 B left, filed as `tasks/api/083-compact-api.md` and **blocked**. This unit is a
source-comment sweep and should not need to write it; if you do, say so, and if you leave it deeper
in reserve than you found it, file `tasks/api/098-compact-api.md` in the same commit per
`tasks/README.md`. Do not compact `spec.md` as part of this unit — it has a live park.

**`095` was closed `done` and its file removed, not left `blocked`** — leg 115's correction, made
because the worker had written `blocked` for a task nothing was blocking. A `fleet stop` is not a
standing condition anyone can clear, and every line `095` did not reach is enumerated below, so
there was nothing left for a park to hold. **This task is therefore the only live record of what
remains**; `095`'s own tally lives in the `2026-09-14 api/095` entry of
`embarch-fleet/supervisor-log.md`. Do not read the absence of `tasks/api/095` as the sweep having
finished.

## What `095` actually verified (do not re-check these)

Decision bodies read directly: `embarch-api/decisions/core-link.md`, `client-crate.md`,
`surface.md`, `failure-reporting.md`, `hardware-selection.md`; `embarch-core/decisions/handshake.md`.

Citations checked clean against those bodies (repo, decision, client.rs lines): api 11 (L17); api 15
(L1183, L1269); api 34 (L194, L1387); api 50 (L1127, L1159); api 55 (L1127); api 58 (L259, L788,
L815, L855, L911, L2355); api 60 (L787, L827, L863); api 72 (L413, L2013); api 73 (L289, L320, L328,
L347, L356, L2216, L2251); core 31 (L701, L723); core 35 (L796, L2341); core 47 (L784, L802, L817,
L854, L909, L2356); core 56 (L224, L246, L809). All matched their decision's body — **zero false
sentences found in this set.**

**Three wrong-label defects found and fixed in `095`:** bare `decision 59` at L292, L344, L357 —
each in its own fresh doc-comment paragraph, not sharing a paragraph with any explicit
`` `embarch-core` decision 59 `` — which, read under the stated "bare is same-repo" convention,
resolves to **`embarch-api`'s own decision 59** (`hardware-selection.md` — `dev_bench_hello`,
`link_identity`), a real decision that has nothing to do with the `kind`/`fix_it_url` splitting these
comments actually describe. Relabelled `` `embarch-core` decision 59 `` at all three sites. (L288 has
the same bare form but sits in the *same* doc-comment paragraph as an explicit `` `embarch-core`
decision 59 `` four lines above it — judged defensible anaphora, not a defect; recheck this judgment
if you disagree.)

**One unsettled finding, deliberately not fixed — needs a decision, not a guess:** L403's
`` `this crate must never link `probe-rs`/`serialport` (decisions 37, 38)` `` — `client-crate.md`'s
current text for decisions 37/38 is about *why the crate was extracted* (one implementation instead
of two), not a link prohibition. The "must never have [probe-rs/serialport] dependencies" language is
decision 72's, verbatim, established two lines later in this same client.rs comment block. Read
`embarch-topology/decisions/consumer-boundary.md` (decision 31, the `wire`-feature split this same
sentence also cites) alongside `client-crate.md` 37/38/72 before touching this — it's possible 37/38's
original founding session also stated the link prohibition and the compacted decisions.md entry just
dropped it; do not resolve toward "clean" without checking.

## What is still unswept — read the body, don't just resolve the number

**`embarch-api`** (own decision set, check bare citations against this first):
- `decisions/zephyr.md` (12, 20, 21, 51) — L1532 `resolve.rs, decision 12` (bare; near `embarch-core`
  decision 8 at L1530, so check it isn't anaphoric to the wrong repo the way L205/L292 were)
- `decisions/smoke-harness.md` (30, 74) — L1159 `decision 74` (bare, but cross-referenced by an
  explicit `decisions/smoke-harness.md` path in the same clause, so low ambiguity risk — still unread)

**`embarch-core`** (`embarch-doc/embarch-core/decisions/`):
- `probes.md` (8, 9, 22, 23, 26, 34, 61) — L203 (`decision 22`, explicitly labelled), L1295
  (`decision 9`), L1530 (`decision 8`)
- `enrollment.md` (25, 27, 28, 50, 54→57, 57) — L231, L1401, L1450 (`decision 28`); L253, L2134
  (`decision 50`)
- `surfaces.md` (12, 13, 55, 59) — L1001, L1244 (`decision 12`); **read this file's own decision 59
  entry directly** — `095`'s understanding of core decision 59's content came secondhand, from
  `embarch-api/decisions/failure-reporting.md`'s description of it, never from `surfaces.md` itself.
  All the *labelled* `` `embarch-core` decision 59 `` sites (L271, 282, 306, 319, 335, 2164, 2213,
  2230, 2249) still need a primary-source check against that.
- `streams.md` (30, 38, 39, 62, 63) — L508 (`decision 30(c)`), L593 (`decision 62`), L1687
  (`decision 30`), L2459 (`decision 63`)
- `flashing.md` (10, 18, 21, 32) — L1282 (`decision 18`)
- `logging.md` (16, 29, 37, 44, 51, 58) — L1963 (`decision 37`)

**`embarch-topology`** (`embarch-doc/embarch-topology/decisions/`):
- `enrollment.md` (14, 15, 16, 28) — L190, L203, L429, L1385, L1463, L1786 (`decision 14`); L201
  (`decision 15`, explicit); L205 (`decision 15`, bare — judged anaphoric to L201 in `095`, same
  reasoning as the L288 call above, but unverified against the body); L191 (`that crate's decision
  28`, referring to topology 28)
- `link-declares.md` (20, 27) — L441, L862, L2092 (`decision 20`); L430 (`decision 27`, bare —
  **`embarch-api` also has its own decision 27** in `study-reads.md`, so check this one against
  api's own set first per the Method, the same trap that produced the three decision-59 defects)
- `validate-timing.md` (26) — L252, L2134 (`decision 26`)
- `links.md` (18) — L1774 (`decision 18`)
- `alerts.md` (5, 12, 19) — L307 (`decision 12`)
- `crate.md` (1, 2, 3, 6, 13) — L1065 (`decisions 2, 3`)
- `consumer-boundary.md` (4, 8, 31) — L2018 (`decision 31`) — see the L403 unsettled item above, same
  decision

**`embarch-outpost`** (`embarch-doc/embarch-outpost/decisions/`):
- `manifest.md` (9, 24) — L136, L536 (`decision 9`)
- `tracing.md` (2, 19, 25) — L550 (`decision 19`)
- `layout.md` (4) / `clocks.md` (17, 18) — L543 (`decisions 4, 17` — two different files, one per
  number; check both)

**`embarch-study-designer`** (`embarch-doc/embarch-study-designer/decisions/`):
- `versioning.md` (12, 30, 47, 72) — L66, L79, L105, L1557 (`decision 12`)
- `declares.md` (40, 74) — L701, L704 (`decision 40`); L779 (`decision 74`)
- `streams.md` (11, 20, 21, 27, 39) — L1660 (`decision 39`)

**`embarch-ui`** (`embarch-doc/embarch-ui/decisions/`) — **decision 10 is split across three files
with different parenthetical qualifiers** (`topology-tab.md`: "10 (routing)"; `trace-view.md`: "10
(trace)"; `trace-chart.md`: "10 (chart)") — check each client.rs site resolves to the right file's
sub-entry, not just "decision 10 exists somewhere":
- `wiring.md` (5, 6, 24, 26) — L213, L432, L460 (`decision 5`)
- `debug-tab.md` (7, 13) — L667, L1502 (`decision 7`)
- `topology-tab.md` / `trace-view.md` — L530 (`decision 10, trace half`), L1745 (`decision 10
  (trace)`), L1865 (`decision 10, routing half`)

**`embarch-dev-bench`** (`embarch-doc/embarch-dev-bench/decisions/`) — **highest-priority single
item in this task.** L561 cites `` `embarch-dev-bench` decision 24 `` for "a source `embarch-dev-bench`
has no front end for — power sampling". `embarch-dev-bench/decisions.md`'s own table maps decision 24
to `boards.md` ("Boards — which board is the bench, and why it changed twice"), which on its face has
nothing to do with power-sampling front-end coverage. Read `boards.md`'s decision 24 entry directly
before anything else in this task — if it doesn't discuss power sampling, this is a wrong-number
defect in `StudyStreamEntry::source_deferred`'s own doc comment, landed same-day by `api/096`
(`c26d930`) per the `095` dispatch note, and per that task's own instruction to sweep it "like
everything else" rather than assuming recency means correct.

**Cross-suite, read-only check (no edit possible from this repo):** L1726 cites `suite decision 4`,
`../../embarch-doc/suite/decisions.md` — verify the number resolves, but any correction there is an
`inbox/` drop, never an edit — `suite/decisions.md` is not `api`'s to touch.

## Method

Same as `095` — carried from `core/054`, `core/056`, `umbrella/065`, `umbrella/066`,
`study-designer/046`. Read the cited decision's **body**, not just the fact that the number resolves.
Check every bare `decision N` against `embarch-api`'s own decision set first, even when it looks
foreign — `095` found three real defects exactly this way (bare `decision 59` silently landing on
api's own unrelated decision 59). Count wrong numbers and false sentences **separately**. Report
anything you cannot settle as unsettled — do not fold a doubt into a clean zero.

## Done when

- [x] Every citation listed above checked against its decision's body (not just resolved).
- [x] The L403 and L561 items settled one way or the other, with the reasoning stated.
- [x] Wrong numbers and false sentences counted and reported separately, added to `095`'s tally
      (3 wrong labels already found/fixed, 0 false sentences found in the set `095` checked).
- [x] Cross-repo citations carry the labelled `<repo> decision N` form; same-repo ones stay bare.
- [x] Any suite-level citation correction (L1726) filed to `embarch-doc/inbox/`, never edited directly.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment, including if the remaining count is zero defects.

## Result (leg 116, 2026-09-16)

**Tally, added to `095`'s (3 wrong labels, 0 false sentences):** this unit checked every
remaining citation enumerated above against its decision's body. Found **2 more wrong-number
defects, 0 false sentences.** Combined running total: **5 wrong labels, 0 false sentences**, across
the whole file.

**Defects found and fixed:**
- **L430** — `EnrolledBoardResponse`'s doc comment read `` (`link_port_serial` added decision 27) ``.
  Neither `embarch-api`'s own decision 27 (`study-reads.md`, seal/capacity validation) nor
  `embarch-topology`'s decision 27 (`link-declares.md`, `NotFound`'s exclusion reason and
  clear-link-fact CLI flags) is about adding the field. `embarch-topology` decision 17
  (`links-port.md`) is: "an enrolled board gains the link port's *own* USB serial: a directly
  declared fact" — the field's actual origin. Relabelled to `` `embarch-topology` decision 17 ``.
- **L667** — `LogsRecentResponse`'s doc comment attributed "no server-side structuring/filtering"
  to `` `embarch-ui` decision 7's resolution of that open question ``. `embarch-ui` decision 7
  (`debug-tab.md`) never discusses formatting — verified against its full history, not just its
  current body (no commit ever added such a clause). The actual reasoning — "served as plain text,
  because reformatting a deployed service's output into JSON for one client is a bigger change
  than this needs" — is `embarch-core` decision 16's (`logging.md`), which names `embarch-ui`'s
  Debug tab as the consumer it was weighing the cost against. Relabelled to
  `` `embarch-core` decision 16 ``. (The *other* `embarch-ui` decision 7 citation in this same
  file, L1502, is correct: "never reads Core's logfile directly... handed the data" matches
  decision 7's actual body.)

**L403 settled: not a defect.** Checked `embarch-topology/decisions/consumer-boundary.md` decision
31 and the git history of `embarch-api/decisions/client-crate.md` (not just its current body, per
the task's own instruction). At the api/067 split (`d048f67`), decisions 37/38's text read: "the
real ones sit behind the feature that links `probe-rs`, and this crate never links hardware" —
the link-boundary fact genuinely originated in 37/38's founding content. The `suite/035` fold
(`2b9c258`, 2026-09-12) replaced that sentence with "Retired by decision 72 below" when decision 72
was written, and decision 72 now carries the explicit "dependencies this crate must never have"
phrasing verbatim. So citing `(decisions 37, 38)` for the link-prohibition context in `client.rs`'s
comment is grounded in real (if since-compacted) history, and the comment separately and correctly
cites decision 72 two lines later for the current explicit wording. Left as-is.

**L561 settled: not a defect — the task's own suspicion was wrong.** Read
`embarch-dev-bench/decisions/boards.md`'s decision 24 entry directly, as instructed. Despite the
index table's generic file-level description ("Boards — which board is the bench, and why it
changed twice"), decision 24's actual body is titled "The power front end: a Nordic PPK2 as an
external instrument, provisional" and is entirely about the unscoped/unbuilt power-sampling front
end ("Not ordered, not wired into any workspace"). This matches `client.rs`'s citation exactly —
`source_deferred`'s doc comment names decision 24 for "a source `embarch-dev-bench` has no front
end for... power sampling, today." No defect; the index table's topic line is just generic, the
decision text itself is on point.

**L1726 (cross-suite, `suite decision 4`) verified, no `inbox/` drop needed.** `suite/decisions.md`
lists decision 4 at `decisions/placement.md`, whose body ("The outpost's own answer is computed
once, in `embarch-core`, the only component on both paths and in the release archive") matches
`embarch-core` decision 62's own citation of the same suite decision, which `client.rs`'s
`get_study_load` doc comment mirrors. The number resolves and the content matches.

**One unsettled item, named rather than resolved toward clean:** L1774's
`` `embarch-topology` decision 18's 2026-08-25 amendment `` (on `declare_signal`'s doc comment).
The substantive claim (declaring is idempotent, re-declaring is the migration path) matches
decision 18's body correctly. But decision 18's current text carries no documented amendment dated
2026-08-25, unlike the structurally identical pattern at L213/L432 (`` `embarch-ui` decision 5's
amendment ``), where decision 5's own body documents a same-day reversal ("Originally split along a
mutation/read-only line instead; reversed the same day"). No corresponding reversal/amendment
exists in `links.md` decision 18's text, and no commit around 2026-08-25 in `embarch-topology`
touching signal declaration was found. Left uncorrected — the underlying claim is true, only the
"amendment" framing is unverified — rather than guessed at either way.

**Everything else enumerated in the task** (`embarch-api` zephyr.md/smoke-harness.md;
`embarch-core` probes.md/enrollment.md/surfaces.md/streams.md/flashing.md/logging.md;
`embarch-topology` enrollment.md/link-declares.md (decision 20 sites)/validate-timing.md/links.md
(the idempotency claim itself)/alerts.md/crate.md/consumer-boundary.md (decision 8);
`embarch-outpost` manifest.md/tracing.md/layout.md+clocks.md; `embarch-study-designer`
versioning.md/declares.md/streams.md; `embarch-ui` wiring.md/topology-tab.md/trace-view.md)
checked clean against the cited decision's body — every bare `decision N` checked against
`embarch-api`'s own decision set first per the Method, including the L205/L1532 sites flagged for
anaphora risk (both resolved correctly: L205 genuinely anaphoric to topology decision 15 at L201,
L1532 genuinely `embarch-api`'s own decision 12 despite sitting near an explicit `embarch-core`
decision 8 citation).

**Gate:** `cargo build`/`test`/`clippy --all-targets -D warnings` green at the workspace root and
explicitly `-p embarch-core-client` (now a workspace member per `embarch-api` decision 56, so the
root run already covers it — confirmed by running the scoped form anyway). `check-docs.py` 11/11
green. `check-client-names.py` clean against both worktrees. `check-ownership.py` clean in both.
`check-doc-size.py`: 13 in reserve, all filed — no new reserve debt (neither `spec.md` nor any
other `api` doc was touched by this unit).
