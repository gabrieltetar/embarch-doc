# 095 — Citation sweep: `embarch-core-client/src/client.rs`, the suite's densest unswept file

**State:** open
**Source:** leg 112's refill sweep, 2026-09-13. `queue-status.py --refill-owed --wave 6` reported
five distinct scopes against a wave of six, with `api` holding nothing dispatchable — its only open
task is `tasks/api/059`, which is `Hardware: bench`. Counted the same day: **103 lines matching
`[Dd]ecisions? [0-9]+` in `embarch-api/crates/embarch-core-client/src/client.rs`**, the largest
unswept citation surface left in any host-side repo in the suite.
**Scope:** api
**Hardware:** none — source comments only. No board, no probe, no live Core, no deploy. Nothing here
changes what any binary does.
**Owner:** no

## What

Sweep `embarch-api/crates/embarch-core-client/src/client.rs` — every `decision N` citation checked
against the cited decision's **body**, not merely resolved. Counted in the main checkout on
2026-09-13, the whole `embarch-api` citation surface stands at:

```
103  crates/embarch-core-client/src/client.rs   <- this task
 48  src/config.rs
 34  src/resolve.rs
 23  src/tools.rs
 19  src/zephyr.rs
 18  src/cli.rs
 17  src/main.rs
  9  tests/smoke_harness.rs
  9  src/reflash.rs
  7  crates/embarch-core-client/src/api_log.rs
  6  src/study.rs
  4  tests/core_client_http.rs
```

**Take `client.rs` and nothing else unless it goes quickly.** When you run out of budget, file
`tasks/api/<next>` naming exactly which files remain — **in `tasks/api/`, your own scope**, never
`tasks/doc/`, which `check-ownership.py` refuses to every worker. `check-task-numbers.py --next api`
is the only safe way to pick the number; `ls tasks/api/ | tail -1` is not a high-water mark, because
a `done` task's file is gone.

## Why this file, specifically

**The series has a hypothesis and this file is its sharpest remaining test.** Results so far:
`core/054` (`api.rs`) 3 wrong in 54 · `umbrella/065` (`doctor.rs`) 2 in ~129 · `study-designer/044`
0 in ~53 · `ui/049` 0 in 74 · `umbrella/066` 113 held / 1 wrong across eleven files ·
**`core/056` (`study.rs`) 10 in 109**, the worst rate the series has produced. The hypothesis, first
guessed by `ui/049` and reinforced by `core/056`: **the dirty files are the ones that restate other
repos' decisions; the clean ones explain their own code.**

`client.rs` is the strongest instance of the dirty side left. It is `embarch-api`'s HTTP client for
`embarch-core`, so nearly every comment in it narrates an `embarch-core` route decision from outside
`embarch-core` — and it is a **shared crate**, consumed by `embarch-ui` and by `embarch-api` itself,
so a bare `decision N` in it is read from more than one repo's default citation index. That is the
exact ambiguity `study-designer/047`'s brief calls out for its own repo.

**Report the count even if it is zero.** A clean `client.rs` would be real evidence *against* the
hypothesis, and the log has treated "checked N, found none" as a legitimate product of these units
five times now.

## Method (carried from `core/054`, `core/056`, `umbrella/065`, `umbrella/066`, `study-designer/046`)

**Read the cited decision's body, then read the sentence around the citation, in that order.** A
number that resolves is not evidence the claim holds. The real yield across a week of these sweeps
has been prose a decision made false, or a citation pointing at the wrong but real decision — not
bare typos. **Count wrong *numbers* and false *sentences* separately and report both.**

**Check cross-repo labelling first.** A bare `decision N` is same-repo by convention; another repo's
decision must read `<repo> decision N`. The general form is still open and owner-reserved
(`tasks/doc/055`), so do not invent a new form — use the labelled one already in use. **Check every
bare `decision N` against `embarch-api`'s own decision set first, whether or not the topic looks
foreign** — `core/056` found four citations where the right answers were two different numbers,
**two of which should have carried no repo prefix at all.**

**Git history of the decisions file is worth checking when a citation's credit looks off.**
`study-designer/046`'s two false-sentence findings both resolved by `git log --follow -p --
<decisions file>` — one decision walking back its own earlier claim, one fact folded into an
*earlier* number "the same session". Do not stop at "does the decision doc currently say this".

**Four shapes found so far, none of them a typo:** a real decision cited in the wrong *repo*; a
structural rule attributed to the decision that *used* it rather than the one that *established*
it; an over-cited pair from a different table row; and — `umbrella/067`, 2026-09-13 — **a citation
that resolves, to a real decision, in the right repo, that has nothing to do with the code it
annotates.** Only reading the body detects the fourth. **Deleting such a citation is a legitimate
fix**; `umbrella/067` deleted one rather than replacing it with a differently wrong one.

**And do not adjudicate your own doubt in your own favour.** `umbrella/066` reported 114/0; a
reviewer sampling 12 citations found one the worker had itself flagged as "defensible either way"
and folded into the zero. The honest tally was 113/1. **A zero-defect sweep's characteristic failure
is not missing a defect, it is the sweeper resolving an ambiguity toward zero.** If you find one you
cannot settle, report it as unsettled and say so plainly — that is a better result than a clean
number.

## Watch for

- **Do not file a numbered decision for this.** A citation sweep that corrects citations decides
  nothing. If it turns up something that genuinely needs deciding, file `tasks/api/<next>` and say
  so in your closing section.
- **`embarch-api/spec.md` is in reserve** (9,102 / 10,240 B, 1,138 B left) and its compaction task
  `tasks/api/083` is `blocked` on `In flux: yes`. A comment sweep should not need it. If your work
  writes into it anyway, `.claude/leg.md`'s rule applies: a blocked compaction task parks the pass,
  not the reserve — compact that file in this same unit, carrying `083`'s `Must not delete:` list,
  and close only that file's item.
- **`api/094` landed three new structs in this very crate on 2026-09-13** — `LoadAnswer`,
  `LoadSummary`, `LoadSubject`, hand-mirroring `embarch-core/src/outpost_load.rs` field for field,
  with a doc comment saying why no shared type pins them. Their citations are hours old and were
  reviewed once. **Sweep them like everything else** rather than assuming recency means correct.

## Done when

- [ ] `crates/embarch-core-client/src/client.rs` read end to end, every `decision N` citation checked
      against the cited decision's body, not just resolved.
- [ ] Wrong numbers and false sentences counted and reported separately, with the total read, and any
      citation you could not settle reported as unsettled rather than folded into either count.
- [ ] Cross-repo citations carry the labelled `<repo> decision N` form; same-repo ones stay bare.
- [ ] A remainder task filed as `tasks/api/<next>` naming exactly which files are left.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment — including if the answer was zero defects, because the count is the
      product of this unit.
