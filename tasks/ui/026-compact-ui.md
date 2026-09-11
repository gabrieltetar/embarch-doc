# 026 — `embarch-ui/open.md` is in reserve against its own baseline

**State:** done — leg 083, 2026-09-11

**Doc-size reserve in your scope (`embarch-ui`).** Exactly one file is in reserve and it is the one
this task pays: `embarch-ui/open.md` 4,295/5,120 B (83.9%), filed against this task. Nothing else in
`embarch-ui` is in reserve. **Note the ratchet that caught leg 082 twice:** `check-doc-size.py`
measures `open.md` against its own **baseline**, not only against the 5,120 B cap, so a shorter file
can still go RED. Get it out of reserve in one pass rather than shaving.
**Source:** `scripts/check-doc-size.py` went RED during leg 082's `tasks/suite/019` unit, which
added one bullet to `embarch-ui/open.md`.
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-10-11
**In flux:** no — see "Why this is dispatchable" below.
**Must not delete:**

- **Every measured number in the 250,000-row bullet, with its date and its conditions.** Decode
  257 ms → 604 ms → 1.69 s and resident view JSON 4.48 MB → 9.03 MB → 18.1 MB at 250k/500k/1M
  [2026-09-09]; encode 4.6 ms → 8.3 ms → 23.5 ms and in-process total 210 ms → 518 ms → 1.32 s
  [2026-09-10]; `/bins` staying at 165 KB / 180 KB / 1.5 KB. The bullet's whole point is that the
  cap is kept **against measurement rather than extrapolation**, and a shortened version that keeps
  the conclusion and drops the figures inverts that — it becomes an assertion.
- **The three unmeasured Core calls** (`study_streams`, `get_study_stream`, `study_steps`) and the
  statement that no synthetic capture stands in for a live Core, because that is what stops someone
  reading 1.32 s as the end-to-end cost.
- **The reflash bullet's three shapes** and which one is settled — the list is the reason
  "the UI cannot reflash" reads as a limitation rather than a design goal (decision 11).
- **The release-archive bullet's trigger** — *the first engineer who is not the repo owner walks
  the studies guide end to end* — and the fact that the call belongs to `embarch-umbrella`'s
  decision 14 and the suite, not to this repo. Without the attribution the bullet reads as work
  this repo is declining to do.
- **The stale-prefix bullet's `18 records` and `STALE_PREFIX_MAX_ROWS` (512)**, and that the 512 is
  an assumption about a bridge FIFO nobody has measured.

## Why this is dispatchable

**`In flux: no` is a real answer here, not a default.** Three of the five bullets are settled
records of measurement or of a deferral with a trigger; the two live ones — the trace-placement
comparison and the stale prefix — are **hardware-gated**, waiting on a board rather than on further
design in this repo. Nothing in the file is mid-rewrite. Compare `tasks/suite/004`, which is
correctly `blocked`: its files are prose about a capability that is about to be exercised for the
first time.

## What is actually over

**4,295 / 5,120 B against the cap is only 83.9%** — the file is nowhere near its cap. What it is
over is **90% of its own recorded baseline**, which is the ratchet: a file that shrank once is not
allowed to drift back. That makes this a *cheaper* pass than most, because the target is a few
hundred bytes and not a structural rewrite. The 250,000-row bullet is the obvious candidate — it is
two measurement runs written as continuous prose and would lose nothing as a small table — and that
is a reshaping, not a deletion, so the `Must not delete:` list above stays satisfied.

## Done when

- [x] `embarch-ui/open.md` is out of reserve against its baseline, with every item above intact.
      3,875/5,120 B (75.7%), reshaped the 250,000-row bullet into an intro sentence plus a
      measurement table and tightened three unprotected bullets; `check-doc-size.py --pressure`
      now reports it `PAID`.
- [x] `DOC-COMPACTION-PASS.md`'s human question is answered in the fold's log entry, in the
      compactor's own words: can `spec.md` alone answer what someone needs to work on this
      component today? **Yes.** `spec.md` carries what it is, the six tabs, every Core call it
      makes, the invariants, the design system and the verification technique — everything an
      engineer needs to start working on the component today. `open.md` is deliberately not part
      of that answer: it holds what is still unresolved (two hardware-gated, one a release-surface
      call outside this repo, one a location call already settled), which `decisions.md` explains
      the why of. The three-file split is doing its job here; this pass reshaped `open.md`, it
      did not need to touch `spec.md` at all.
- [x] Gate green; `changelog.d/` fragment dropped.
