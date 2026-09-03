# 001 — `doctor` check 11 checks nothing, and its stated reason is false

**State:** done — agent/umbrella/001-doctor-check-11-is-a-stub, 2026-09-03 (leg 005). An earlier attempt died mid-write on HTTP 529 with no commits; nothing of it survived and this was built from scratch.
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

- [x] Check 11 compares the three versions above and reports pass / warn / fail
      with all three values in its message, never a hardcoded string.
- [x] It degrades honestly when a number is genuinely unavailable (Core down,
      no bench) — that is a *skip with the reason*, not a pass and not the old
      false reason.
- [x] Unit-tested at the comparison boundary with the numbers injected, so the
      logic is covered without a live Core.
- [x] `embarch-umbrella/open.md`'s first bullet is rewritten to whatever is
      still open (the live run, if that is all that is left).
- [x] **Hardware-verification debt recorded**: running `doctor` against the real
      deployed Core and a flashed bench is the owner's, not a worker's.
- [x] Gate green (`embarch-parallel-agents.md` §10).
- [x] `changelog.d/` fragment dropped.

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

- [x] Check 11 (or whichever check owns it) reports the `core_version` Core
      answered with, and **does not present it as a skew check** against the
      three schema numbers — it is a different question, reported separately.
- [x] `embarch-umbrella/open.md` states the honest limit: `core_version` only
      moves when the crate version does, so this catches a **cross-version**
      stale deploy and **not** a same-version one. Strictly better than nothing,
      not a hash comparison.


## Done, 2026-09-03 — what was built and what it does not do

**Check 11** is `judge_schema_versions`, a pure function over three injected
numbers, wrapped by a thin fetcher. It compares Core's served
`study_designer_schema_version` against this `embarch` binary's compiled
`HOST_TYPE_SCHEMA_VERSION` (**fail** on a difference — `embarch-api` refuses to
submit across it), and reports the bench's wire version together with Core's own
`compatible` verdict (**fail** on `false`, the 2026-08-26 state). Every missing
number is a `Warn` naming which number and why — Core unreachable, no token, no
bench, a `409` mid-study, a Core predating the field — and a `Fail` always
outranks a skip. Sixteen unit tests cover the matrix with no Core and no bench.
`/dev-bench/hello` is now fetched once in the driver and shared with check 13,
because that endpoint opens the serial link.

**Check 15** is new: `/status`'s `core_version` against the located
`embarch-core` binary's `--version`. Warn, never fail (`embarch-core` decision
13, `embarch-umbrella` decision 24), and the check's own output states its
limit — a same-version stale deploy is invisible to it.

`embarch-umbrella` decisions **33** and **34**. `spec.md`'s check table
renumbered: the flashing-backend check really is 14, so the four designed-only
checks are now 16-19 rather than colliding with what shipped.

### Hardware-verification debt — the owner's, not a worker's

**Neither new check has ever run against anything real.** One
`embarch doctor` against the live deployed Core and the flashed bench closes it,
and it establishes three things no host test can:

1. The deployed Core's `/status` actually carries **both**
   `study_designer_schema_version` and `core_version`. The check reads them by
   name; a Core older than 2026-08-25 / 2026-09-03 respectively makes each a
   named skip, which is correct behaviour but not the behaviour wanted here.
2. `/dev-bench/hello` returns a `compatible` field the check can read. Without
   it check 11 warns "no `compatible` verdict" — a state only a live bench can
   distinguish from a field-name mistake here.
3. Check 11 reads **pass** on a pair that is genuinely in step, and check 15
   reads **pass** against a Core deployed from the located binary. A false warn
   on a healthy machine is the failure mode that gets a deploy gate ignored.

Recorded in `embarch-umbrella/open.md` as its first open item.

### Not done, and filed rather than faked

Check 11 compares **this** binary's compiled host constant, not the located
`embarch-api`'s — `embarch-api` exposes that number on no surface at all. Exact
whenever check 1's manifest agrees; wrong for a hand-built mixed install.
Closing it is an `embarch-api` change, so it went to
`inbox/api-expose-compiled-host-schema-version.md` rather than across the
ownership boundary.
