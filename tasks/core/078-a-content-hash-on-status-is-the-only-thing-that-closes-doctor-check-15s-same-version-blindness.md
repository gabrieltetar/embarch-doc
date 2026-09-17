# 078 — A content hash on `/status` is the only thing that closes `doctor` check 15's same-version blindness, and it is this repo's call

**State:** done — decided by agent/core/078-status-content-identity, 2026-09-17. Decision: **yes**, a
self-hash of the running binary (not a git SHA, not a build timestamp) is the field worth building.
Recorded as decision 67, `embarch-core/decisions/surfaces.md`. Not implemented here — it is a
wire-schema bump on `/status`; the build is filed as `tasks/core/088`, `open`, awaiting a supervisor
announcement per `ops.md` §4 before it can be dispatched.
**Source:** refill sweep, leg 137, 2026-09-17, from
[`embarch-umbrella/open.md`](../../embarch-umbrella/open.md)'s standing bullet: *"**Check 15 is not
a hash comparison and must not be read as one.** It catches a *cross-version* stale deploy and is
blind to a same-version one: `core_version` is `CARGO_PKG_VERSION`, so a rebuild and failed deploy
at one version reads as a match ([decision 34](../../embarch-umbrella/decisions/schema-skew.md)). A
content hash on `/status` would close it, `embarch-core`'s call."* The bullet has named this repo as
the deciding one and **nothing has ever been filed here**, so the call has no owner.
**Scope:** core
**Hardware:** none — this is a decision about what `/status` carries, answered by reading
`src/api.rs`'s status handler, `decisions/surfaces.md` and the build. **Do not deploy, do not run a
live Core, do not flash anything.**
**Owner:** no

**Doc-size reserve, re-read at dispatch (leg 141, 2026-09-17) — this supersedes the filing-time
reading below, and it changes what you owe.** `embarch-core/decisions/surfaces.md` — the file this
task's `Done when` names as the likely home for your decision — is **11,253/12,288 B (91.6%), IN
RESERVE, 1,035 B left**. Its compaction task `tasks/core/079-compact-core.md` is **`blocked` on
`In flux: yes`**, and `.claude/leg.md` is explicit that a blocked compaction task parks the *pass*,
not the reserve: **if you write into `surfaces.md`, you compact `surfaces.md` as part of this unit**,
carrying `tasks/core/079`'s `Must not delete:` list verbatim (read that file first — it names
decision 12's scope/trigger paragraph, decision 59's original resolution, `core/074`'s correction and
`core/077`'s settlement) and bringing the file back under 90%. You are the actor making the flux, so
you are the only one who can shorten what you are rewriting without writing a clean statement of
something about to be wrong. Do **not** close `tasks/core/079` — say in your report what you paid and
leave the task for the supervisor to settle.

**If the topic-correct home for your decision turns out not to be `surfaces.md`, none of the above
applies** — say which file you chose and why, and check its headroom instead. What you must not do
is pick a file by where there is room; `embarch-api` filed a decision in the wrong topic file on
2026-09-05 for exactly that reason, with 96 B left, and nothing failed.

**Doc-size reserve for `core`, read at filing:** `embarch-core/decisions/auth.md` is
**11,356/12,288 B (932 B left)**, filed as `tasks/core/046` and blocked — do not write into it.
`decisions/surfaces.md` and `interfaces.md` have room. Run `python3 scripts/check-doc-size.py
--pressure` before and after; if your edits push another file into the band, file
`tasks/core/<NNN>-compact-core.md` in the same commit.

## What

`embarch-umbrella`'s `doctor` check 15 compares the `core_version` a running Core reports against
the version the umbrella expects. `core_version` is `CARGO_PKG_VERSION`, so it answers *"is the
running binary from a different release"* and cannot answer *"is the running binary the one I just
built"*. **The failure it misses is the common one on this bench**: a rebuild at the same version
whose deploy silently did not land. `deploy-core` is already recorded elsewhere in this suite as
something that reports "landed" when nothing installed, which is exactly the case check 15 reads as
a match.

Decide, for `embarch-core` and only `embarch-core`:

1. **Should `/status` carry a content identity** — a hash of the running binary, a build fingerprint,
   a git SHA baked at compile time, or nothing — and if so, which? Weigh what each actually proves:
   a `git` SHA baked in at build time proves *what source was compiled*, which is not the same as
   *what bytes are running*, and a self-hash of the running executable is the only one that answers
   the second. Say which question is worth answering, not just which is easy.
2. **What it costs.** A self-hash means reading the executable's own file at startup or on request;
   on Windows that is the installed service binary. Say plainly whether that is acceptable and
   whether it is done once at start or per request.
3. **Whether the answer is "no".** It legitimately might be: this is a diagnostic for one consumer,
   the failure is already visible by other means, and adding a field to `/status` is a wire surface
   three consumers read. **Recording a considered "no" with the reasoning is a complete outcome** and
   is the cheaper one. What it must not stay is unanswered in another repo's `open.md`.

## Why now

Not urgent and not a defect — nothing is broken, a capability is missing. It is worth a unit because
it is a **decision parked in the wrong repo's `open.md`**: `embarch-umbrella` cannot make it,
correctly says so, and has said so since decision 34 landed. Nothing was ever filed here, so the
sentence *"`embarch-core`'s call"* has been true and unactioned the whole time. One unit ends it
either way.

## Done when

- [x] Re-derived from `src/api.rs` (the status handler lives there, `status_handler`/`StatusResponse`
      at lines ~238–288) exactly what `/status` carries today: `status`, `probes`,
      `study_designer_schema_version`, `core_version` — confirmed against the code, not this task's
      summary of it.
- [x] A numbered decision in `embarch-core/decisions/surfaces.md` recording the field, what it
      proves, and what it costs — decision 67. `surfaces.md` was the topic-correct file (it already
      holds decision 13, the `core_version` decision this one extends) and had room once compacted
      (see below); `auth.md` was never written to.
- [x] The answer is yes and it changes `/status`'s response shape, so **it is not landed here** — the
      decision is made, the implementation is filed as `tasks/core/088` (`open`, a wire-schema bump
      awaiting a supervisor announcement per `ops.md` §4), and this is said plainly in this task's
      `State:` line and in the worker's report.
- [x] `embarch-core/interfaces.md`/`interfaces/hardware.md` checked against decision 67: `/status`'s
      field set is unchanged by this unit (the field is decided, not built), so the existing row
      already matches — no edit needed, and none made.
- [x] `embarch-core/open.md` gains the open item: a new "Designed, not built" bullet for decision 67,
      naming `tasks/core/088` and the wire-schema-bump note, matching the pattern decision 64's
      bullet already used.
- [x] A `changelog.d/` fragment: `changelog.d/core-status-content-hash.decided.md`.
- [x] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-core` (unchanged by this unit — no source edits were needed, since the
      unit is a decision plus a filed follow-up task); `python3 scripts/check-docs.py` in
      `embarch-doc`.

## Doc-size debt paid in this unit

`embarch-core/decisions/surfaces.md` was 11,253/12,288 B (91.6%, in reserve) at dispatch, with its
compaction task `tasks/core/079` `blocked` on `In flux: yes`. Per this task's dispatch note, writing
decision 67 into it meant compacting it in the same unit, carrying `tasks/core/079`'s `Must not
delete:` list verbatim. Paid: decision 55 (a retired-name entry, not on the must-not-delete list)
tightened from 1,116 B to 631 B; decision 59's four amendment paragraphs (the two on the
must-not-delete list — `core/074`'s correction and `core/077`'s settlement — plus its unprotected
intro and closing paragraphs) tightened in wording only, every fact from the must-not-delete list
still present (decision 12's scope/trigger citation untouched; decision 59's original `kind`
field/`503`/`409` split/`fix_it_url: None` reasoning intact; `core/074`'s four call sites and the
un-downcastable failure list intact; `core/077`'s considered-collapse reasoning, the
`.claude/leg.md` downstream-handling argument, the wire-change cost list, and the `embarch-api`
"plug it in" inbox drop all intact). Net: file now 10,896/12,288 B (88.7%), decision 67 added, all
five decision numbers (12, 13, 55, 59, 67) still resolving. **`tasks/core/079` was not closed** —
left `blocked` for the supervisor to settle, per this task's own instruction not to close it.

## Not yours

- **Do not change `embarch-umbrella`** — not check 15, not `decisions/schema-skew.md`, not its
  `open.md`. Once this decision exists, the umbrella side can consume it on its own unit.
- **Do not implement the wire change** if you decide in favour. Decide, then file.
- **Do not touch `deploy-core` or anything under `scripts/`.**
