# 058 — Citation sweep: `embarch-core/src` remainder after `api.rs` and `study.rs`

**State:** open
**Source:** leg 111's refill sweep, 2026-09-13. `core/054` swept `src/api.rs` (3 defects in 54) and
`core/056` swept `src/study.rs` (10 defects in 109, the worst rate the series has produced).
Neither filed a remainder task, so the ~92 citations in the rest of `src/` have had no owner since.
`supervisor-log.md`'s carry-forward has named `embarch-core`'s own source as an unfiled sweep since
2026-09-12.
**Scope:** core
**Hardware:** none — source comments only. No board, no probe, no live Core, no deploy, and nothing
here changes what any binary does.
**Owner:** no

## What

Counted in the main checkout on 2026-09-13: **257 lines matching `decisions? [0-9]+` across
`embarch-core/src` and `crates/`.** Of those, `api.rs` (54) and `study.rs` (111) are swept. The
remainder, by file:

```
21  src/stream_store.rs
13  src/main.rs
13  src/hardware.rs
 7  src/dev_bench_link.rs
 5  src/outpost_manifest.rs
 5  src/outpost_load.rs
 5  src/logs.rs
 5  src/flash_backend.rs
 5  src/dev_bench_log.rs
 5  src/chip_resolve.rs
 4  src/service.rs
 4  src/elevate.rs
```

**Take `src/stream_store.rs` first, then as many of the small files as the budget allows.** When
you run out of budget, file `tasks/core/<next>` naming exactly which files remain, the way
`study-designer/046` does — **in `tasks/core/`, your own scope**, never `tasks/doc/`, which
`check-ownership.py` refuses to every worker.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A wrong number or a
stale sentence in a source comment fails no gate and never has. `embarch-core` is the repo with the
most inbound decision surface in the suite — it narrates `embarch-study-designer`,
`embarch-topology`, `embarch-dev-bench` and `embarch-outpost` decisions as well as its own — which
is exactly the property the series has already identified as the predictor of a dirty file.

**`core/056` is the reason to expect defects here rather than a clean sheet.** The series reads
`core/054` (`api.rs`) 3/54 · `umbrella/065` (`doctor.rs`) 2/129 · `study-designer/044` 0/53 ·
`ui/049` 0/74 · `umbrella/066` 1/114 · **`core/056` (`study.rs`) 10/109**. The hypothesis
`core/056` landed on — first guessed by `ui/049` — is that the dirty files are **the ones that
restate other repos' decisions**, and the clean ones are those that explain their own code.
`stream_store.rs` is the one remaining `embarch-core` file that plainly fits the dirty side of
that prediction: it is Core's stream storage narrating `embarch-outpost`'s and
`embarch-study-designer`'s wire contracts. **Sweeping it is a test of the hypothesis as much as a
fix**, so report the count even if it is zero — a clean `stream_store.rs` would be real evidence
against it, and that is worth as much as a defect.

## Method (carried from `core/054`, `core/056`, `umbrella/066`, `study-designer/045`)

**Read the cited decision's body, then read the sentence around the citation, in that order.** A
number that resolves is not evidence the claim holds. The real yield across a week of these sweeps
has been prose a decision made false, or a citation pointing at the wrong but real decision — not
bare typos. **Count wrong *numbers* and false *sentences* separately and report both**, honestly,
even if one or both is zero: "checked N, found none" is a legitimate result and the log treats it
as one.

**Check cross-repo labelling.** A bare `decision N` is same-repo by convention; another repo's
decision must read `<repo> decision N`. The general form is still open and owner-reserved
(`tasks/doc/055`), so do not invent a new form — use the labelled one that is already in use.
`core/056` found `embarch-study-designer` decision **63** cited four times for two *different*
claims where the right answers were two different numbers, **two of which should have carried no
repo prefix at all**. Check every bare `decision N` against `embarch-core`'s own decision set
first, whether or not the topic looks foreign.

**A wrong number is not always a nearby-digit typo.** The three shapes found so far: a real
decision in the wrong *repo*; a structural rule attributed to the decision that *used* it rather
than the one that *established* it; and an over-cited pair from a different table row.

**And one shape no gate and no number check can see** (`umbrella/067`, 2026-09-13): a citation that
**resolves, to a real decision, in the right repo, that has nothing to do with the code it
annotates.** The only detector is reading the cited decision's body and asking whether it is about
this. If you find one, **deleting the citation is a legitimate fix** — `umbrella/067` deleted one
rather than replacing it with a differently wrong one, and that was the right call.

## Watch for

- **Do not file a numbered decision for this.** A citation sweep that corrects citations decides
  nothing. If the sweep turns up something that genuinely needs deciding, file it as
  `tasks/core/<next>` and say so in your closing section.
- **`embarch-core/decisions/auth.md` is in reserve** (11,356 / 12,288 B, 932 B left) and its
  compaction task `tasks/core/046` is `blocked` on `In flux: yes`. A comment sweep should not need
  it. If your work writes into it anyway, `.claude/leg.md`'s rule applies: a blocked compaction
  task parks the pass, not the reserve, so the file you write into is the file you compact in the
  same unit, carrying `046`'s `Must not delete:` list.
- **The outstanding native Windows build.** `core/015`'s debt now carries eight landed
  `embarch-core` changes that have not been built as the Windows service. A comment-only sweep adds
  a ninth; say so in your report so the ledger stays honest, and do not attempt a Windows build —
  that is the owner's.

## Done when

- [ ] `src/stream_store.rs` read end to end, every `decision N` citation checked against the cited
      decision's body, not just resolved.
- [ ] Wrong numbers and false sentences counted and reported separately, with the total read.
- [ ] Cross-repo citations carry the labelled `<repo> decision N` form; same-repo ones stay bare.
- [ ] A remainder task filed as `tasks/core/<next>` naming exactly which files are left, unless
      every file above was swept.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment — including if the answer was zero defects, because the count is the
      product of this unit.
