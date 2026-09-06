# 017 — decision 22(a-c): three first-day `doctor` checks, designed and never built

**State:** done, 2026-09-05 (agent/umbrella/017-decision-22-three-first-day-checks)
**Source:** `embarch-umbrella/open.md` — "Two designed pieces are confirmed unbuilt; open is
whether each is still wanted. Decisions 22(a-c) and 27/29." Swept 2026-09-05 by leg 014 when
the queue hit zero.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

[decision 22](../../embarch-umbrella/decisions/doctor.md) designs three checks and its own
last line says **all three are unbuilt**: `doctor` assembles exactly checks 1-16, and
*firewall* and *disk* appear nowhere in the crate. It has been in that state long enough
that `open.md` now asks the right question about it — *is each of these still wanted?* —
rather than treating it as work in progress.

**Resolve all three, one way or the other.** For each of (a), (b), (c): build it, or retire
that part per `DOC-CONVENTIONS.md`'s tombstone shape. A part that is retired must carry the
argument against building it, and a part that is built must carry the argument against
retiring it — the entry has to hold the losing case either way. **"Still deferred" is not an
outcome here**; that is the state it is already in and the state `open.md` is asking about.

**(a) is the one with a real, already-possible failure behind it and is the core of this
unit.** A Core that bound loopback under the new default *without `setup` having widened it*
is exactly the "reachable from this interface but not the one WSL2 can actually use" failure
that default made possible. Two facts the decision records for whoever implements it, both
worth re-verifying rather than trusting:

- `embarch-topology` already exposes the recommended-bind-address function, and `setup`
  already calls it and bakes it into the `install` invocation. **What is missing is only the
  check that would notice when it hadn't been.** `embarch-topology/open.md` independently
  calls umbrella's bind-versus-topology check "a separate, still-unwired consumer of the same
  function", so the two docs agree that the function is there and the caller is not.
- The check compares **the address `/status` was reached at** against what the detected
  topology needs, and **fails when they disagree** rather than reporting bare unreachability.
  Those are different signals and the decision is explicit about which it wants.

**(b) firewall state** is best-effort and informational by design — it names a likely-active
profile when a connectivity probe fails and Core cannot be ruled out as simply not running.
**(c) disk space** warns below a generous threshold on the filesystem backing the build and
results directories, because a build failing from a full disk reads as a mystifying compiler
error. Both are cheap; neither is obviously still wanted, and **the honest answer for either
may be a tombstone.** If building one would push this unit past a single sitting, retire it
or file a follow-up task naming it — do not half-build a check.

**A new check is a new row in `spec.md`'s twenty-row `doctor` table**, and that table's
built/unbuilt distinction per row is the thing `tasks/umbrella/009`'s `Must not delete:`
list protects. Keep the distinction exact: a check you build moves to built, a decision you
retire leaves the table's unbuilt count *lower*, and `009` records "twenty rows / two unbuilt
decisions" as of `umbrella/007`. Update that count in `009` if you change it.

## Reconcile the other half of the source bullet before you touch it

The same `open.md` bullet names **27/29** alongside 22 as "confirmed unbuilt". **That half
looks stale and is yours to settle first**, cheaply: `embarch-umbrella/decisions/release.md`
27/29 now states that each of the four release workflows carries a `verify-version` job the
build matrix `needs:`. `embarch-topology/.github/workflows/release.yml` and its three
siblings are readable from here — **read them** (reading another repo is fine; writing one is
not) and either delete 27/29 from the bullet because it is built, or say precisely which of
the four is still missing it. Do not leave the bullet asserting both halves are unbuilt when
one is not.

## Why now

`open.md` states it today, so it reconciles. It is also the last **designed-and-unbuilt**
group in this sub-project other than 26's `--prune`, which is deferred by choice and blocked
on `embarch-api` — so resolving 22 either finishes umbrella's design backlog or shortens it
by three entries.

## Reserve

Nothing in `umbrella` is in reserve right now, and both of the tight files are close:
`embarch-umbrella/spec.md` **8,795 / 10,240 B (85.9%)** and `embarch-umbrella/open.md`
**4,509 / 5,120 B (88.1%)**. Adding a `doctor` table row plus a decision amendment is exactly
the size of edit that puts `spec.md` back in. `decisions/doctor.md` has room (7.6K / 12K).

**If your work leaves either file at or above 90%, you owe a compaction task** —
`tasks/umbrella/<NNN>-compact-umbrella.md`, filed in the same commit, per `tasks/README.md`.
`tasks/umbrella/009-compact-docs.md` is the existing umbrella compaction task and it is
`blocked` with `In flux: yes`; if your edits spend the reserve, prefer **updating `009`'s
numbers and file list** over filing a second one, and say in it that this task is what put
the file back in.

## Done when

- [x] Each of 22(a), 22(b), 22(c) is either built or retired, and the amendment is made
      **in the decision's heading as well as its body** — a heading that still promises three
      unbuilt checks under a body that retired two is the defect `umbrella/015` fixed.
- [x] Anything built has unit tests, including the disagreement case for (a) — a bind address
      that does not match what the topology needs must **fail**, not warn, and a test has to
      pin that.
- [x] `spec.md`'s `doctor` table reflects the new state per row, with the built/unbuilt
      distinction intact.
- [x] `embarch-umbrella/open.md`'s "Two designed pieces are confirmed unbuilt" bullet is
      rewritten or deleted, with the 27/29 half settled against the actual workflow files.
- [x] `tasks/umbrella/009-compact-docs.md`'s row/decision counts updated if you changed them.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/umbrella-*` fragment
      dropped, and a `features.d/umbrella-*` row for any check that now exists.

## What shipped

**22(a) built as `doctor` check 17.** `judge_bind_address` in `src/doctor.rs`,
pure and fully unit-tested, plus `parse_sc_qc_bind_address` in `src/locate.rs`
reading `--bind` off the same `sc.exe qc` line `locate_core` and `deploy-core`
already parse. Seven new check-17 tests and four parser tests; 174 pass.

**The comparison is not the one the entry sketched, and the entry now says
why.** "The address `/status` was reached at versus what the detected topology
needs" is tautological as written: check 3's class *is* derived from whichever
candidate answered, so the winner always agrees with itself. The independent
half is **the class `setup` recorded in machine state**; with none recorded the
check warns `no-recorded-class` rather than passing vacuously.

**And the failure the decision names is mostly invisible from the reachable
side**, which is why the check reads the service registration. A Core that
answered has already proved its bind covers that route; the narrow-bind failure
shows up as *nothing answering anywhere*, and the registration is what tells
"Core is down" from "Core is up and bound where you cannot reach it". So there
are two Fails on different evidence — `bind-too-narrow` (reached at loopback,
recorded class needs `0.0.0.0`) and `bound-narrow` (nothing reachable,
registered `--bind 127.0.0.1`) — and a `bind-not-the-cause` warn, which is the
useful negative.

**One carve-out, recorded with its losing argument:** bound *wider* than the
recorded class needs warns, it does not fail. That machine works, and a red
`doctor` where nothing is broken is the failure this chain exists to avoid.

**22(b) and 22(c) retired unbuilt**, each with the argument against building it
in the entry. (b): permanently amber on this topology by its own admission, no
actionable fix line, and (a) now answers the same question with a cause instead
of a suspicion. (c): `std` has no free-space API, so it costs a dependency or a
per-platform shell-out in a crate explicit about what it refuses to link, and
check 16 already measures what actually grows here.

**27/29 was stale and is settled.** All four release workflows —
`embarch-umbrella`, `embarch-core`, `embarch-api`, `embarch-topology` — carry a
`verify-version` job that the `build` matrix `needs:`. Read from the files, not
inferred. That half is deleted from the `open.md` bullet.

## Hardware-verification debt

**Check 17 has never met a real narrow-bound Core.** This bench's service is
registered `--bind 0.0.0.0`, so the check passes here by agreement rather than
by discriminating anything; both Fail branches and the `bind-wider-than-needed`
warn are unit-tested against synthetic evidence only. Settling it needs a Core
deliberately installed `--bind 127.0.0.1` on a `wsl-host` machine: `embarch
doctor --json` should show check 17 `bound-narrow` with nothing reachable, then
`bind-too-narrow` from a `doctor` run on the Windows side, which can still reach
loopback. Filed as an `open.md` bullet, not only here.

## Reserve

`spec.md` **went down**, 9014 → 8966 B (87.6%), because retiring 22(b-c) deleted
two table rows. `open.md` **went into reserve**, 4509 → 4840 B (94.5%): the
27/29 half of the old bullet was deleted, but the check-17 verification debt
above is a new open question that has to live somewhere. Per this task's
instruction that is filed by updating `tasks/umbrella/009-compact-docs.md`
rather than filing a second task — its `Compacts:` line now names `open.md` as
an unpaid item (the strikethrough was what `check-doc-size.py` could not see),
its counts are refreshed to **eighteen rows / one unbuilt decision**, and it
says `umbrella/017` is what put the file back in. `decisions/doctor.md` ended at
10,634 B (86.5%) after a deliberate second pass — the first draft of the
amendment put it at 95.6%.
