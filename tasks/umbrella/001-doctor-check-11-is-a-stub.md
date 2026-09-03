# 001 — `doctor` check 11 checks nothing, and its stated reason is false

**State:** open — reclaimed 2026-09-03 by leg recovery. Its worker died mid-write when batch 004 hit repeated HTTP 529; the branch had no commits and the worktrees held only uncommitted edits, both deleted. Nothing of that attempt survives; start from scratch.
**Source:** embarch-umbrella/open.md — "**`doctor` check 11 never checks anything, and its stated reason is false.**"
**Scope:** umbrella
**Hardware:** verify-only

## What

Check 11 returns a hardcoded warn reading *"not available yet —
`embarch-study-designer` isn't wired into `embarch-core`/`embarch-api` as a
dependency yet"*. It **is** a direct dependency of both; Core has served the
version on `/status` since 2026-08-25 and `embarch-api` compares its own
compiled copy before every submit. So the check's stated reason is untrue and
the check compares nothing.

This is not cosmetic. On 2026-08-26 the live pair sat at Core wire v13 against a
bench flashed to v14 — a state the handshake refuses correctly and loudly, but
**only to whoever calls the handshake endpoint by hand.** `doctor` is the
surface whose whole job is saying that unasked, and it said "not available yet"
the entire time.

`open.md` already names the three numbers worth comparing and where each is
already reachable from: **Core's served host version (check 3), the version the
located `embarch-api` was built against (check 1), and the wire version the
bench reports (check 12).** Nothing new has to be fetched.

## Why now

The suite's only unattended deploy-gate check is a stub, and the exact failure
it exists to catch has already happened once undetected.

## Done when

- [ ] Check 11 compares the three versions above and reports pass / warn / fail
      with all three values in its message, never a hardcoded string.
- [ ] It degrades honestly when a number is genuinely unavailable (Core down,
      no bench) — that is a *skip with the reason*, not a pass and not the old
      false reason.
- [ ] Unit-tested at the comparison boundary with the numbers injected, so the
      logic is covered without a live Core.
- [ ] `embarch-umbrella/open.md`'s first bullet is rewritten to whatever is
      still open (the live run, if that is all that is left).
- [ ] **Hardware-verification debt recorded**: running `doctor` against the real
      deployed Core and a flashed bench is the owner's, not a worker's.
- [ ] Gate green (`embarch-parallel-agents.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Amended 2026-09-03 by the supervisor: a fourth number

Folded in from `inbox/umbrella-doctor-check-11-fourth-number.md`, dropped by
the `core/002` worker. **Amended into this task rather than filed as its own,
because otherwise check 11 gets touched twice** — this task is open and
unclaimed and the field already exists with no reader.

`GET /status` now also serves **`core_version`**, Core's own crate version
compiled in from `CARGO_PKG_VERSION` (`embarch-core/interfaces.md`'s `/status`
row, decision 13, built and merged 2026-09-03). Note carefully what this does
*not* change: the three numbers named above stay the three numbers, and
**nothing this task needed was blocked on `core/002`.** The task text's earlier
implication that check 11 was waiting on Core was wrong — Core's served *host*
version is `study_designer_schema_version` and has existed since 2026-08-25.

`core_version` answers a **different question** from schema skew: a Core running
an **older binary than the one that was built and deployed.**
`embarch-dev-workflow.md` §4a records `deploy-core` printing `landed` twice in
one session when the elevated child was cancelled and nothing installed, and its
own check compares byte *length*, which cannot discriminate a release rebuild of
one constant.

- [ ] Check 11 (or whichever check owns it) reports the `core_version` Core
      answered with, and **does not present it as a skew check** against the
      three schema numbers — it is a different question, reported separately.
- [ ] `embarch-umbrella/open.md` states the honest limit: `core_version` only
      moves when the crate version does, so this catches a **cross-version**
      stale deploy and **not** a same-version one. Strictly better than nothing,
      not a hash comparison.
