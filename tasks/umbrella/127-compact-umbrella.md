# 127 — compact `embarch-umbrella/open.md`

**State:** blocked — install-core is still gaining halves (grant, self-elevation), so open.md is moving

**Unparks when:** the owner has run the install-core hardware debt or self-elevation lands, whichever is first
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/open.md
**Size debt due:** 2026-12-18
**In flux:** yes
**Must not delete:** every hardware-debt line that names a check to run (checks 13, 15, 17, 5, the desk steps, `install-core`'s two debts) until its owner has run it.

## What

`open.md` is at 4,553 of 5,120 B (reserve starts at 3,891) after `umbrella/124` added the `--agent-in-container` grant's hardware debt. The `install-core` debts (decisions 61, 69, 70, 72) are four entries for one command and can be one entry per platform once the owner has run any of them.

## Done when

- [ ] The file is out of reserve (`scripts/check-doc-size.py --pressure`) and every `Must not delete:` item survives.
- [ ] The human question is answered in the commit message: can the install-core debt be read as one checklist per platform?
