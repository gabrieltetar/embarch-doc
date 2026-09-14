# 056 — `study.rs` is `embarch-core`'s largest unswept citation surface, and `api.rs` was swept around it

**State:** done — worker agent/core/056-study-rs-citations, 2026-09-13. See "Result" below.
**Source:** `tasks/core/054` swept `embarch-core/src/api.rs` (54 citations, three wrong) and the
supervisor log's carry-forward recorded that **no sweep had been filed for `embarch-core`'s own
source as a whole**. The leg of 2026-09-13 17:5x counted the repo: **240 citations across `src/`,
107 of them in `study.rs` alone** — more than any other single file in any repo in the suite.
**Scope:** core
**Hardware:** none — source comments only; nothing is flashed, no study runs, no live Core is
touched.
**Owner:** no

## What

`embarch-core/src/study.rs` carries 107 lines matching `decision[s] N`.
**`check-decision-refs.py` resolves decision numbers only inside `*.md`**, so a wrong number in a
source comment fails no gate and never has. `core/054` already proved the rate is not negligible in
this repo: three of `api.rs`'s 54 were wrong.

## Why this class keeps being worth running

Across four consecutive days of these sweeps the count of wrong *numbers* has been the less
interesting half of every result. The real yield has been **prose a decision made false and nobody
updated** — `umbrella/063` fixed four things and only two were numbers; the other two were sentences
that went false the same day a decision landed. `core/054`, `ui/040` and `dev-bench/020` each found
the same shape.

So **read the cited decision's body, then read the sentence around the citation**, in that order.
A number that resolves is not evidence the claim holds. Report the two categories separately, and
report how many held — "ninety held, three were numbers, four were false sentences" is the useful
shape.

## Bounding

107 citations is more than one pass. **Take `study.rs` top to bottom and get as far as you honestly
can inside your unit**, then file `tasks/core/<next>` for the remainder, naming the **exact line
number or function** you stopped after so the next worker starts cleanly. A half-finished sweep that
says precisely where it stopped is a good outcome; a rushed complete one is not. Do not pad the
count by skimming.

Two things specific to this file:

1. **`study.rs` is where the wire contract lives**, so its comments cite `embarch-dev-bench` and
   `embarch-study-designer` decisions as often as `embarch-core`'s own. A bare `decision N` here may
   resolve against `embarch-core`'s index when it meant another repo's. Where a citation crosses a
   repo boundary, write `<repo> decision N` — the form `embarch-api` decision 57 fixed on. **This is
   the most likely defect in this particular file and worth checking first.**
2. **You may not edit another repo's docs.** If a sweep turns up that the *decision body* is wrong
   rather than the citation, that is an `inbox/` drop, written by **absolute path** to
   `/home/gabriel/Github/embarch/embarch-doc/inbox/` — not an edit.

## Reserve, for planning

`embarch-core/decisions/auth.md` is 11,356/12,288 B — **932 B left, 92.4%** — filed against blocked
`tasks/core/046`. A comment sweep should not touch it. If your work leaves any `embarch-core` doc in
the last 10% of its cap unfiled, file `tasks/core/<next>-compact-core.md` in the same commit —
**your own scope**, never `tasks/doc/`.

## A standing debt to note, not to pay

`core/015`'s native Windows build now carries **twelve** landed `embarch-core` changes. A
comment-only sweep adds nothing behavioural to it, but say in your changelog fragment that it is
comment-only so the count stays honest.

## Done when

- [x] Every citation in the range you took is confirmed against the cited body or fixed, with
      **wrong numbers and false sentences counted separately**.
- [x] Cross-repo citations carry their repo name.
- [x] A follow-up task is filed for the remainder naming where you stopped — or a fold line saying
      the file is fully swept.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/core-*` fragment.

## Result, 2026-09-13

**109 citations read** (the file's own count is 109 matching `decision[s]? [0-9]` lines; the task
header's 107 undercounted by two — no other discrepancy found). **`study.rs` swept top to bottom,
fully — no remainder task.**

**99 held, 6 wrong numbers, 4 false sentences.**

**Wrong numbers** (right repo, wrong number — all `embarch-study-designer` except the two that
should have carried no repo prefix at all, being `embarch-core`'s own):
- Lines 86, 1349 — cited `embarch-study-designer` decision 63 (that decision is study-designer's own
  `cargo test` harness stack overflow, unrelated) for the `GET /study/{id}` clone-by-value crash and
  the accumulate-then-build fix. Both are `embarch-core` decision 24's own finding — fixed to bare
  `decision 24`.
- Lines 2538, 4211 — same wrong decision 63, this time for the **~1.3 MB StudyResult measurement**
  itself, which is `embarch-study-designer` decision 49's own table (`1,293,608` bytes, "before").
  Fixed to decision 49.
- Line 2528 — cited `embarch-study-designer` decision 30 (Core's own per-message receipt-time stamp)
  for "the clock-resync gap" — that's decision 72 (`rx_utc_ms` carries bench uptime, the seeding half
  never built). Fixed.
- Line 4552 — cited `embarch-study-designer` decision 35 (the custom-action registry, BLE writes) for
  "no sniff, no fallback" on a `Raw`-encoded stream tap — an unrelated feature. The same claim at
  line 2299 correctly cites decision 39 (the tap model); fixed line 4552 to match.

**False sentences** (citation resolves, decision body no longer supports the claim):
- Lines 141, 567, 2818 — three places describe `embarch-topology` decision 12 as a
  "durable-log-plus-live-push shape," mirrored by Core's own SSE broadcast. Topology's own decision
  19 retired that crate's live-push half (its only consumer, a standalone UI, was deleted) — decision
  12's own text now reads it struck through. Reworded all three to state the live-push retirement
  explicitly rather than claim topology still does what Core's SSE route does.
- Lines 1908–1910 — claimed an outpost trace record "carries none of its own" clock, so Core's
  receipt-time stamp is "the trace's only clock." `embarch-outpost` decisions 4 and 17 are exactly
  the opposite: every record carries its own `cycles` stamp (the *measuring* clock); decision 17's
  whole point is **two** clocks, not one. Reworded to state what each clock actually does (DUT
  `cycles` measures, Core's receipt time places).

None of the ten needed an `inbox/` drop — every defect was in `embarch-core`'s own prose, not in
another repo's decision body, and all ten are fixed in this commit (comment-only, `src/study.rs`).
`core/055` (landed same day, `resolve_probe` → `embarch_topology::select_probe`) did not make any
`study.rs` citation false — the one place that logic is discussed (the dev-bench board-identity gate,
~line 853) is a different code path (`embarch_topology::hardware::validate_role`) that never touched
`resolve_probe` either before or after that landing.

Gate: `cargo build`/`test`/`clippy --all-targets -- -D warnings` green (197 passed, 0 failed, 2
ignored); `check-docs.py` 11/11 green; `check-client-names.py` clean; `check-ownership.py
--scope core` and `--code-repo` both green.
