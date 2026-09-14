# 097 — Citation sweep remainder: `embarch-core-client/src/client.rs`

**State:** open
**Source:** `tasks/api/095`, cut short by a fleet stop mid-sweep on 2026-09-14. `095` read the whole
file end to end (2625 lines, all citation contexts noted) but cross-checked citations against the
cited decision's **body** for only six decision files before stopping. This task is the remainder:
finish the primary-source check for everything below.
**Scope:** api
**Hardware:** none — source comments only.
**Owner:** no

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

- [ ] Every citation listed above checked against its decision's body (not just resolved).
- [ ] The L403 and L561 items settled one way or the other, with the reasoning stated.
- [ ] Wrong numbers and false sentences counted and reported separately, added to `095`'s tally
      (3 wrong labels already found/fixed, 0 false sentences found in the set `095` checked).
- [ ] Cross-repo citations carry the labelled `<repo> decision N` form; same-repo ones stay bare.
- [ ] Any suite-level citation correction (L1726) filed to `embarch-doc/inbox/`, never edited directly.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment, including if the remaining count is zero defects.
