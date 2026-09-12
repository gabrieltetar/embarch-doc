# 053 — `deploy-core` still reports "landed" through both defects its own decision amendment named

**State:** claimed — leg 088, 2026-09-11.
**Doc-size reserve for this sub-project:** `embarch-umbrella/decisions/doctor.md` is at 90.2%
(11,082/12,288 B) and `decisions/bind.md` at 93.2% (11,447/12,288 B), both filed against blocked
tasks. **`decisions/deploy.md` is NOT in reserve** — that is the file this unit writes to. If your
work pushes another file into its last 10%, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the
same commit.
**Source:** refill sweep, leg 088, 2026-09-11. `embarch-umbrella/decisions/deploy.md`'s amendment
against `embarch-umbrella/src/deploy.rs`, both read.
**Scope:** umbrella
**Hardware:** none — the fix and its tests are host-side and pure. Confirming it against a real
cancelled UAC prompt is a hardware debt to record, not a precondition for this task.
**Owner:** no

## What

`decisions/deploy.md`'s amendment describes two defects, found the hard way — *"the installed binary
never changed, confirmed by hash"*, twice on consecutive invocations — and prescribes a fix for each.
**Neither fix is in the code.** The amendment reads as settled mechanism and `spec.md`'s `deploy-core`
row promises to *"verify the binary changed"*; what ships is the verification the amendment declared
incapable of that.

1. **"It has to hash."** `src/deploy.rs:286` is still
   `pub fn landed(built_len: u64, installed_len_after: u64) -> bool { built_len == installed_len_after }`,
   fed from `std::fs::metadata(..).len()` at `:404` and `:502`. The no-op warning the amendment
   quotes against itself is still printed verbatim at `:410`. Its own tests (`:790-791`) pin the
   length semantics, so they have to move with it.
2. **"An explicit cancellation is a hard failure and must exit non-zero."** `:496-531`: a missing
   elevated transcript only *prints a note* — *"the elevated child never started"* — and control
   falls straight through to the length check. When the two builds are the same size (exactly the
   cancelled-deploy case the amendment describes) the command prints
   *"deploy-core: landed, and {service} is running"* and returns **0**. `grep -n cancel src/deploy.rs`
   finds nothing outside prose.

So a script branching on `deploy-core`'s exit code trusts a deploy that never happened, which is the
failure the whole module says it exists to catch.

## What to do

Hash both sides and compare the digests instead of the lengths; keep `landed` pure and separate for
the same reason its own doc comment gives, and rename its parameters so a length can no longer be
passed to it by mistake. Make a **missing elevated transcript a hard failure in its own right**,
before the content check — the amendment says the success line must not depend on the service being
`RUNNING`, which is true of a deploy that did nothing at all.

**Do not widen the diagnosis while you are in there.** The amendment is explicit that
*"a dialog nobody answered"* and *"a dialog that never appeared"* have completely different fixes and
that the wrong one was believed for an hour; narrowing that message is a separate, real task and
**not this one**. If you want it, file it rather than doing it.

**One adjacent bug, in scope because it is in the same function's output:** `src/deploy.rs:454` tells
the user to *"re-run with `--verify-only`"*, and no such flag exists — `DeployCore` in
`src/main.rs:129-160` has none and the string appears nowhere else in `src/`. Either add the flag or
fix the message; say in this file which you chose and why.

## Why now

This is the one command in the suite whose entire job is to tell the truth about whether something
landed, and it has already told the repo owner the opposite twice. It is also cheap: the fix is a
pure function, a guard, and their tests.

## Done when

- [ ] `landed` compares content digests, not byte counts, and its tests assert the same-length
      different-content case explicitly — that is the case the amendment was written about.
- [ ] A missing elevated transcript exits non-zero on its own, without reaching the content check.
- [ ] No path prints "landed" while returning 0 on a deploy that did not install.
- [ ] `src/deploy.rs:454`'s `--verify-only` either exists or is gone from the message.
- [ ] `decisions/deploy.md` records that the amendment's two clauses are now built, as a fired
      condition rather than a rewrite of the history — the amendment's account of how it was found is
      the valuable half and must survive.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.

**Hardware debt to record in the task file when you finish:** nothing here has met a real cancelled
UAC prompt. The fix is unit-testable and untested against the event it exists for, and that stays
true until the owner runs `deploy-core` on the Windows machine — which also waits on `core/015`'s
outstanding native build.
