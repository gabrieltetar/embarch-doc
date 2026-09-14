# 056 — `study.rs` is `embarch-core`'s largest unswept citation surface, and `api.rs` was swept around it

**State:** claimed by agent/core/056-study-rs-citations, 2026-09-13 19:18
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

- [ ] Every citation in the range you took is confirmed against the cited body or fixed, with
      **wrong numbers and false sentences counted separately**.
- [ ] Cross-repo citations carry their repo name.
- [ ] A follow-up task is filed for the remainder naming where you stopped — or a fold line saying
      the file is fully swept.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/core-*` fragment.
