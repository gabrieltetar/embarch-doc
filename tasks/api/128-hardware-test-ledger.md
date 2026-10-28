# 128 — Keep a hardware test ledger: what ran, on what, and what waits for which hardware

**State:** claimed by agent/api/128-hardware-test-ledger, 2026-10-28 16:32
**Dispatch note (supervisor):** `embarch-api/open.md` is in reserve, 473 B left, filed against `tasks/api/144` (open). Keep this unit's open.md change to one short bullet (the ledger's bench debt) or none; if it would cross the cap, compact that file in this unit under `api/144`'s `Must not delete:` list and say so. The bench check in Done when is owed by a leg, not this worker: record it as a hardware-verification debt in this file.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the engineer asked for a test log and a pending list per hardware on 2026-10-12; both were kept by hand (log 55 calls / 30 writes, pending 38 / 20, test plan 80 / 42) across 5–6 sessions in 8 days, alongside a bench-state header restated in each session
**Scope:** api
**Hardware:** verify-only
**Owner:** no

## What

Give each project a hardware test ledger under its untracked `embarch/` folder. It has three parts. **Test definitions** have stable ids, pass criteria, the image or configuration each needs, and the topology roles and instruments it requires (for example a dual-role partner board or an electronic load). **Ledger rows** are appended per run: date, branch and commit, image hash, the roles attached, test id, result, and notes that keep failures and one-offs. **A bench-state header** records what is attached and what is known broken, such as a dead port. The pending view is computed, not hand-kept. `ledger pending` groups each test that has not run, or must rerun, by the hardware it is missing, and lists "runnable now" from the roles currently attached according to topology. A row whose commit is no longer reachable from its branch (folded or rebased away), or whose image hash no longer matches a rebuild, is flagged for rerun. CLI and MCP tools are `ledger_add`, `ledger_show` and `ledger_pending`, and `run_study` appends its own row.

## Why now

In the field, the log and the pending-by-hardware list were the engineer's own request. Hardware arrived on different days (a partner board, then an e-load, then a lab supply), and one board had a dead port. Before the files existed, results were scattered across plan-file sections and memory notes. Every history fold meant working out by hand which tests had to rerun. On 2026-10-14 the engineer asked "did we run all tests that need me at the office?", and only the hand-kept pending list could answer.

## Done when

- [ ] The ledger format is documented, with `ledger add/show/pending` CLI and MCP tools.
- [ ] With a stub topology, the pending view groups tests by missing role, and attaching a role moves its tests to "runnable now".
- [ ] A row whose commit is unreachable from its branch, or whose image hash changed, is flagged for rerun.
- [ ] `run_study` appends a row on completion.
- [ ] Verified once on a bench: a study run lands a row, and the pending view matches the attached roles.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
