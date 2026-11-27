# 064 — The agent guide places the Test tools, and nothing links the retired ledger tools

**State:** claimed by agent/suite/064-the-agent-guide-places-the-test-tools, 2026-11-26 21:53 — window 1795750706.059469 closed 21:08 with no reply; run by the leg itself
**Source:** EMB-390 — agent-guide permission lists do not place the Test tools; EMB-583 — docs outside api still name the retired ledger tools
**Issue:** EMB-390
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch-api` decision 142 replaced `ledger_show`, `ledger_pending` and
`ledger_add` with `test_show`, `test_pending` and `test_add`, and moved the
interface doc to `embarch-api/interfaces/tools-test-ledger.md`, leaving a
retired stub at `tools-ledger.md` so two links in `notes/hil/` hold.
`suite/agent-guide.md` §1.1 still places the three retired tools and has no line
for `run_test`, `test_status`, `test_show`, `test_pending`, `test_add`,
`test_propose`, `test_plan`, `cancel_study` or `export_audio`. When this is
done:

- **Every tool `embarch-api/src/tools.rs` registers on `origin/main` sits in
  exactly one of §1.1's two lists** (64 on 2026-11-26), and no `ledger_*` name
  is left. The list's count and date say so.
- **Allow**: `test_status`, `test_show`, `test_pending`, `test_plan`,
  `test_propose` and `run_test`, which prepares a run and never starts one
  (EMB-390's direction; `run_test` asking too is the owner's alternative).
- **Ask**: `test_add`, a manual verdict relayed by the agent.
- **`cancel_study` and `export_audio`** placed by the page's own rule, with the
  reason in the prose if it is not obvious from it.
- **One sentence** says the person's terminal subcommands (`embarch-api person
  ...`, api decision 141, and `--as-person`, 143) are the person's and not MCP
  tools.
- **`notes/hil/03-test.md` and `07-procedure-doc.md`** link
  `tools-test-ledger.md`, and the stub `embarch-api/interfaces/tools-ledger.md`
  is deleted once nothing links it.

## Why a `suite` task

`suite/agent-guide.md` and `notes/hil/` sit outside every worker's ownership
row, and the stub is in `embarch-api/`'s docs, so no one worker scope covers it.
Doc-only, one repo, no code and no wire change.

## Done when

- [ ] §1.1's two lists hold every registered tool exactly once, no `ledger_*`.
- [ ] The notes link the new interface doc; the stub is gone; nothing links it.
- [ ] `python3 scripts/check-docs.py` green.
- [ ] After the fold is pushed, `scripts/fleet-linear.py close EMB-583 --why
      '...'` naming the fold: the `**Issue:**` field holds one key, so `finish`
      closes EMB-390 and never reaches EMB-583.
