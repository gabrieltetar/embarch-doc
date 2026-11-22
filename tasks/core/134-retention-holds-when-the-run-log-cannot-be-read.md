# 134 — Retention sweeps nothing when the run log cannot be read

**State:** claimed by agent/core/134-retention-holds-when-the-run-log-cannot-be-read, 2026-11-21 22:07
**Source:** Fleet Ready issue: Core's retention sweeps unpublished captures when the run log cannot be read. Found by the reviewer of `tasks/core/131` (the run log, `embarch-core` decisions 111 and 112).
**Issue:** EMB-239
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Retention (`EMBARCH_STUDY_RESULTS_KEEP`) spares every run the run log has not seen published or discarded (decision 111). The set of runs it spares is read from the log, and **a line that cannot be read or parsed makes that set empty rather than failing**, so an unreadable or tampered log turns retention back into a sweep by count, deleting unpublished runs' captures.

An unreadable run log must stop the sweep: nothing is deleted, and Core's log says why at `error`. A log that does not verify is already never extended; retention treats it the same way. `GET /studies` follows the same split as retention today (decision 111), so check whether it reads the same set and say what it does with an unreadable log.

## Where

- `embarch-core`, `src/run_log.rs`: the function that lists the runs retention must spare, and its caller in the result sweep.
- `embarch-core` decision 111, `decisions/run-log.md`.

## Dispatch notes

- **`embarch-core/open.md` is in reserve: 4,764 of 5,120 B, 356 B left**, and its compaction, `tasks/core/133`, is parked on `In flux: yes`. If this unit adds to `open.md`, **compact it as part of this unit** by moving reference detail verbatim into `open/` with a link left behind, until `check-doc-size.py --pressure` no longer lists it, carrying `core/133`'s **Must not delete**: every open item's owner-run step (the `icacls` debts, the unexercised paths) and every decision citation. Better: this fix should need no new `open.md` line at all.
- `decisions/run-log.md` is 6,208 B; amend decision 111 in place rather than adding a new decision, unless the behaviour is a new choice.
- The native Windows build stays a debt (`../../embarch-fleet/gate.md`); do not try it from the worktree.
- Out of scope: anchoring the log's tail (M1.8), and the in-memory declarations ledger.

## Done when

- [ ] A test with a corrupted run-log line shows the sweep deletes nothing and logs why.
- [ ] A test with a run-log file that cannot be opened (present but unreadable, or a directory in its place) shows the same.
- [ ] Decision 111 says what retention does when the log cannot be read; `spec.md` and `interfaces/` updated if they state the sweep; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope core` on both branches).
