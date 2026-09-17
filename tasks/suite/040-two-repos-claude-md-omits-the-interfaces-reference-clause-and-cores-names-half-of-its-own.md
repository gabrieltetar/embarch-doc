# 040 — Two repos' `CLAUDE.md` omits the interfaces Reference clause, and `embarch-core`'s names half of its own

**State:** open — **announced 2026-09-16 20:35, `ts` `1789612542.894959`**, leg 126. The 30-minute
`ops.md` §4 window closes ~21:05. If this leg ends before then, the next leg reads this `ts` and
completes the window rather than restarting it.
**Source:** `umbrella/072`'s worker, 2026-09-16, which noticed the omission in
`embarch-umbrella/CLAUDE.md` and correctly declined to fix it — a single-repo citation sweep is not
where a suite-wide template question gets settled. Leg 124 measured it across all eight repos before
filing, so this task carries the census rather than the suspicion.
**Scope:** suite
**Hardware:** none — eight `CLAUDE.md` files and a `ls`. Nothing is built, flashed, or run.
**Owner:** no — but **supervisor-executed, not dispatchable to a worker**, because it writes files
in several code repos at once (`../../embarch-fleet/protocol.md` §8). It needs
`../../embarch-fleet/ops.md` §4's announcement-and-park window before it runs.

## The template

`DOC-PROTOCOL.md:71-73` is the source of the per-repo `CLAUDE.md` "Four files, not one" paragraph,
and its last clause is **conditional**:

> Unresolved: open.md. `[Reference: interfaces.md, where there is one.]`

"Where there is one" is doing the work. A repo with an interfaces doc should carry the clause; a
repo without one should not.

## The census (taken 2026-09-16, `ls` against `embarch-doc/<sub-project>/`)

| repo | has an interfaces doc | clause in `CLAUDE.md` | verdict |
|---|---|---|---|
| `embarch-core` | `interfaces/` **and** `interfaces.md` | names `interfaces.md` only | **half right** |
| `embarch-api` | `interfaces/` | names `interfaces/` | correct |
| `embarch-outpost` | `interfaces/` | names `interfaces/` | correct |
| `embarch-study-designer` | `interfaces/` | names `interfaces/` | correct |
| `embarch-ui` | `interfaces.md` | **absent** | **defect** |
| `embarch-umbrella` | `interfaces/` | **absent** | **defect** |
| `embarch-dev-bench` | none | absent | correct |
| `embarch-topology` | none | absent | correct |

So: **two plain omissions, one partial, five correct.** The five correct ones are why this is worth
a unit — the template is being followed, which makes the three exceptions drift rather than a
convention nobody adopted.

`embarch-umbrella`'s is the most recent and the most traceable: `umbrella/046` split
`interfaces/doctor-chain.md` out of `spec.md`, creating the repo's first interfaces doc, and nothing
went back to the `CLAUDE.md` that was written before it existed.

## What to do

- `embarch-ui/CLAUDE.md` — add `Reference: [interfaces.md](../embarch-doc/embarch-ui/interfaces.md).`
- `embarch-umbrella/CLAUDE.md` — add
  `Reference: [interfaces/](../embarch-doc/embarch-umbrella/interfaces/).`
- `embarch-core/CLAUDE.md` — **decide, do not guess.** It has both a directory and a file. Read what
  each holds before choosing: if `interfaces.md` is an index over `interfaces/`, naming the file
  alone is right and this row is not a defect at all; if the two are siblings holding different
  things, the clause hides half the reference surface from every agent that reads that file.
  Say which it is in the log entry either way.

Match each repo's existing link style — relative from the code repo into `../embarch-doc/`, the way
line 5 of every one of these files already does it. **Do not touch `DOC-PROTOCOL.md`**: it is
owner-reserved and, on this evidence, it is also correct.

## Why it matters more than a missing sentence

`CLAUDE.md` is the first thing every agent working in that repo reads. An omitted Reference clause
does not fail a gate, does not break a link, and is invisible to `check-links.py` — it just means an
agent in `embarch-umbrella` never learns `interfaces/doctor-chain.md` exists, and writes its
interface facts into `spec.md` instead, which is the drift the four-file split was created to stop.

## Done when

- [ ] The two omissions closed and the `embarch-core` question answered explicitly.
- [ ] The census re-taken after the change and all eight rows correct.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) in every repo touched.
- [ ] Announcement window observed per `../../embarch-fleet/ops.md` §4, with its `ts` recorded
      in this file.
