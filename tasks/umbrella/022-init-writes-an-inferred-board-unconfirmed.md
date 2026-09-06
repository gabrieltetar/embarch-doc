# 022 — `embarch init` writes a board it inferred from a build artifact, unconfirmed

**State:** done, 2026-09-06 — agent/umbrella/022-init-inferred-board
**Source:** [embarch-umbrella/open.md](../../embarch-umbrella/open.md) — "Whether `init` should
warn on a repo holding more than one recorded build is undecided … a static-discovery repo with
several recorded builds still silently gets one picked for it" — and
[embarch-api/open.md](../../embarch-api/open.md)'s first bullet, which names the *same* defect
from the consumer side and names the cheap fix: "`init` refusing to **write** an inferred board
unconfirmed — cheap, and enough."
**Scope:** umbrella
**Hardware:** none. `src/init.rs` reads a repo tree and writes a TOML file; the whole thing is
exercisable against fixture directories, and `init.rs` already builds one
(`BUILD_INFO`, `src/init.rs:581`).
**Owner:** no

## What

**`embarch init`'s static-discovery path must stop asserting an inferred hardware fact as
fact.** For a non-Zephyr repo `init` derives its `build_command` from
`build/build_info.yml` (`src/init.rs:374-470`), and that string carries `-b <board>` — for the
fixture, `-b roadrunner@2/nrf54l15/cpuapp`. `build_info.yml` records **whatever was last
built**, which is not the board on the desk; `embarch-api/open.md` records a day of bring-up
lost to exactly this, against a config whose board came from an ad hoc dev build rather than
the production board the prior config targeted.

Two things are to be true when this is done, and the second is the undecided half:

1. **An inferred board or build command is never written as though it were confirmed.** Pick a
   mechanism and say why in the decision: emit it commented-out, emit it with a
   `# inferred from build/build_info.yml on <date> — confirm this is the board on your desk`
   marker next to it, or refuse to write it and print the line for the user to paste. **Do not
   add an interactive prompt** — `init` must stay runnable in a non-TTY (`decisions/install.md`
   and decision 7's print-the-command posture are the precedent).
2. **A repo holding more than one recorded build never gets one silently picked for it.** Today
   the first `build_info.yml` found wins. Detect the several-builds case, say so, and name every
   candidate it saw rather than choosing. `embarch-umbrella/open.md` records this as *undecided*
   — **deciding it is part of this task**, so the decision entry must state the alternative you
   rejected, not only the one you took.

The Zephyr/west arm is **out of scope and must not change**: decision 17's live discovery
already answers this structurally for that path (`src/init.rs:377-383` says so), and the
comment there is the record of `init`'s old silent-pick behaviour. Keep it.

## Why now

`embarch-api/spec.md` §2's no-inference-as-fact invariant is the suite's strongest standing
rule about DUT facts, and this is the one place a tool violates it on the most load-bearing
fact it writes. The consumer repo has carried the bullet since before its `[[projects]]`
discovery work and named this exact fix as *cheap, and enough*; nothing has built it because
the code is in a different repo from the open question's loudest half.

## Reserve, at dispatch — read this before you plan

Your sub-project has **one file in reserve and it is at the wall.**

- **`embarch-umbrella/open.md` — 5,080 / 5,120 B, 40 bytes left.** Filed against
  `tasks/umbrella/009-compact-docs.md`, which is `blocked` on `In flux: yes`.
  **You cannot add a line to this file.** You do not need to: closing item 1 above **deletes**
  the "Whether `init` should warn…" bullet, which is the honest form of the compaction leg 016
  said was all this file has left — *drop whole items and name each as answered*. Do that, and
  carry `009`'s `Must not delete:` list while you are in the file.
- `embarch-umbrella/decisions/projects.md` — **10,907 B, and the reserve line is 11,059**, so
  you have **152 bytes** before it enters reserve. This is where an `init` decision belongs
  (decisions 12 and 17 are there). A normal decision entry is 600–1,400 B, so **plan on it
  entering reserve.** When it does: **extend `tasks/umbrella/009` rather than filing a second
  compaction task** — `017`, `020` and `021` all set that precedent, and `009` is this
  sub-project's standing debt. Add `projects.md` to its `Compacts:` field and add whatever
  `Must not delete:` items your new decision creates.
- `embarch-umbrella/decisions/bind.md` is at 11,409 / 12,288 (92.8%), in reserve, filed. **Do
  not write to it** — nothing here belongs there.
- Every other `embarch-umbrella/decisions/*.md` is under 9.5 K with room. `install.md` (10,807)
  is the other tight one; nothing here belongs there either.

## Not yours, and drop it rather than reaching for it

**`embarch-api/open.md`'s first bullet is half-answered by this unit** — its `init` half closes,
its `validate`/`status`-compare-against-hardware half does not — and that file belongs to
another sub-project, which `../../embarch-fleet/protocol.md` §3 forbids you to touch. **Drop a
note in `inbox/` naming the file, the bullet, exactly which clause is now built, and which
clause survives.** Do not edit it, and do not leave the fact unrecorded.

## Done when

- [x] `init` never writes an inferred board or build command as confirmed fact, by a mechanism
      that works with no TTY.
- [x] A repo with several recorded builds is reported, with every candidate named, and none is
      picked silently.
- [x] The Zephyr/west arm is byte-identical.
- [x] Tests cover: one recorded build (inferred, marked), several recorded builds (reported, not
      picked), and none (unchanged behaviour).
- [x] A decision entry in `embarch-umbrella/decisions/projects.md` naming the mechanism, the
      rejected alternative, and `embarch-api/spec.md` §2 as what it serves; `decisions.md`'s
      index row added if the file is new.
- [x] `embarch-umbrella/open.md`'s "Whether `init` should warn…" bullet deleted as answered,
      and the file still under its 5,120 B cap.
- [x] `tasks/umbrella/009` extended if this unit spends `projects.md`'s reserve.
- [x] An `inbox/` drop for `embarch-api/open.md`'s half-answered bullet.
- [x] `changelog.d/` fragment; `features.d/` row if this is user-visible behaviour.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What was decided

Recorded as [decision 41](../../embarch-umbrella/decisions/projects.md).

- **The mechanism is the `CHANGE-ME` sentinel `chip` has always used**, not a marker comment
  beside a working value and not a commented-out or withheld `build_command`. A comment cannot
  stop the failure it describes, and a config `embarch status` cannot load is a worse trade than
  one field a human must confirm — which is the trade `chip` already made and proved.
- **Several recorded builds: every candidate named, none picked.** Rejected taking the newest,
  because the ad hoc dev build behind the original incident *was* the newest.
- **An age, not a date**, on the inferred value — `init` runs today either way, so a date stamped
  at scaffold time dates the scaffolding rather than the build the board came from.
- **`decisions/projects.md` was split rather than compacted.** Decision 41 is 1,548 B against
  1,381 B of headroom, so decisions 10 and 12 moved verbatim into a new
  [`decisions/integration.md`](../../embarch-umbrella/decisions/integration.md), leaving
  `projects.md` at 10,491 B (85.4%). See `009`'s **Reserve** field, including why decision 26 —
  the obvious candidate — is the wrong one to move.

## Hardware-verification debt

**None of this has been run against a real firmware repo or a real `embarch-api`.** Unit tests
cover the three cases against fixture data; `init` itself was deliberately not executed, because
its non-scaffolding half shells out to `claude mcp add` and would mutate the owner's real agent
config. What is owed, in an owner session: `embarch init` in a static-discovery repo that has a
`build/build_info.yml`, confirming the written config loads in `embarch-api` with the board still
`CHANGE-ME`, and the same in a repo with a second `build_info.yml` elsewhere in the tree.

## Left for someone else

`embarch-api/open.md`'s first bullet is half-answered and is another sub-project's file — dropped
as `inbox/api-init-half-of-the-no-inference-bullet.md`.

`find_artifact` still picks the shortest `zephyr.hex` under `build/` silently, and was left alone
deliberately: it infers a *path shape* (sysbuild versus plain) rather than a hardware fact, so
`embarch-api/spec.md` §2 does not reach it, and the not-found case already warns.

