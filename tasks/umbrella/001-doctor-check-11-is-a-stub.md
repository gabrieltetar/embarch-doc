# 001 — `doctor` check 11 checks nothing, and its stated reason is false

**State:** open
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
