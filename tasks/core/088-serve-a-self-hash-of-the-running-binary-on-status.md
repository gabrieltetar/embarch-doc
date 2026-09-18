# 088 — Serve a self-hash of the running binary on `/status`

**State:** done — built on `agent/core/088-status-self-hash`, 2026-09-17.

> **THE WINDOW IS CLOSED AND THIS IS DISPATCHED.** Leg 144, 2026-09-17 18:56 MDT. The 30 minutes
> expired at epoch `1789692350`; I polled the thread again afterwards
> (`fleet-read.py --thread 1789690550.857739`) and it still carries **one message, my predecessor's
> own announcement, and nothing else — no reply, 0 actionable.** That is three legs' worth of
> polling with silence throughout. No second announcement was posted and the clock was not
> restarted. Nothing below needs re-doing; it is kept as the record of how the window ran.
>
> **SUPERVISOR: DO NOT DISPATCH THIS UNTIL YOU HAVE ANNOUNCED IT.** Added to the header by leg 141
> at `core/078`'s fold, 2026-09-17, because the flag was in the body and `queue-status.py` shows
> this task as an ordinary `open` `core` unit alongside six others. **Adding a field to
> `StatusResponse` is a wire-schema bump**, and `embarch-fleet/ops.md` §4 requires the supervisor to
> post to #embarch-fleet, record the `ts` **in this file**, park the task, and run it as a leg's
> **last** unit only if 30 minutes have passed with no objection. It is still a single-repo task, so
> once the window has closed it dispatches to a `core` worker normally — the announcement is the
> gate, not the execution. `embarch-core/interfaces.md`'s `/status` row and the `StatusResponse`
> serialized-key test must move in the same change, and three consumers read that surface.
>
> **The announcement has now been posted.** Leg 142, 2026-09-17, `ts` **`1789690550.857739`** in
> #embarch-fleet. The 30 minutes expire at epoch **1789692350**. No `--action` was used, per
> `.claude/leg.md`: an announcement whose mechanism is silence-as-consent does not page the owner.
> **If you are a later leg reading this: do not restart the clock.** Poll it with
> `embarch-fleet/scripts/fleet-read.py --thread 1789690550.857739` at your unit boundaries; if the
> window has expired with no objection, this dispatches to a `core` worker as your **last** unit. A
> reply saying go runs it immediately; a reply saying cancel drops this to plain `open` with the
> reply quoted here and the `ts` struck.
>
> **Leg 142's handover on this window, written at its last fold.** I opened the clock and then ran
> out of leg before it closed — I hit my 4-unit cap with roughly **11 minutes** still to run, which
> is the case `ops.md` §4 and `.claude/leg.md` both describe explicitly. **Polled four times**
> (`fleet-read.py --thread 1789690550.857739`) at every unit boundary: **no reply, no objection, 0
> actionable, each time.** The only message in the thread is my own detail reply.
>
> **So the next leg inherits a window that has already expired on the clock, not one to restart.**
> Poll the thread once to confirm nothing arrived after I stopped looking, and if it is still clean
> this dispatches to a `core` worker as that leg's **last** unit. Do **not** post a second
> announcement: a fresh clock here would mean this task is re-announced every twenty minutes forever
> and never runs, which is the exact failure the "the next leg completes the window" rule exists to
> prevent.
>
> **One thing the worker will need that has moved since this task was written.**
> `embarch-core/decisions/surfaces.md` is at **10,896 B against a 12,288 B cap (88.7%)**, so the 90%
> reserve line is at 11,059 B — **163 bytes of headroom.** A numbered implementation decision will
> not fit. Expect to file `tasks/core/<NNN>-compact-core.md` in the same commit, and do **not**
> solve it by putting the decision in a file that has room: that is the `embarch-api` 96-byte
> failure `.claude/leg.md` names by name.

> **Leg 144's three additions to the brief, all about the same 163 bytes.**
>
> 1. **`embarch-core/decisions/surfaces.md` is 10,896 B against a 12,288 B cap — the 90% reserve line
>    is 11,059 B, so you have 163 bytes before you are in the band.** Your numbered decision will not
>    fit in that. **Write it tightly**: the shape chosen, the dependency, the failure-mode answer,
>    and the rejected alternatives in one line each. Resist restating decision 67's reasoning — cite
>    it. A decision that is 400 B and complete beats one that is 1,200 B and thorough here.
> 2. **File `tasks/core/091-compact-core.md` in the same commit if your edit spends the reserve**
>    (pushes `surfaces.md` past 11,059 B, or leaves it there with nothing filed). **091 is the number
>    to use** — `090` was taken by leg 144's inbox drain and `core/079`, the old compaction task for
>    this file, is already closed, so there is nothing standing to inherit. `tasks/README.md` has the
>    shape; answer `In flux:` **per file**, and it is your call, not a formality — you will be the
>    only actor who knows whether this surface is still moving.
> 3. **Update `surfaces.md`'s size cell in `embarch-core/decisions.md` in the same edit** — line 21,
>    currently `| [Error and version surfaces](decisions/surfaces.md) | 12, 13, 55, 59, 67 | 10.6 KB |`.
>    Your new decision number goes in that row's *Decisions* cell **and** the size cell gets the
>    measured new value. `tasks/core/084` is an open task to re-measure that whole table; it was
>    deliberately not dispatched this leg because this unit invalidates the row it would fix, so
>    **fix your own row and leave the other twenty alone.**
>
> **Do not solve a shortage of room by filing the decision somewhere that has room.** That is the
> `embarch-api` 96-byte failure `.claude/leg.md` names by name: a decision filed in the wrong topic
> file, with nothing failing.

**Source:** `tasks/core/078` (`embarch-core` decision 67, `embarch-core/decisions/surfaces.md`)
decided `/status` should carry a content identity to close `embarch-umbrella` doctor check 15's
same-version blindness, and filed the building as this task rather than doing it itself (decision 67
is a decision, not an implementation).
**Scope:** core
**Hardware:** none — build and test on Linux; the Windows service-binary case is the same
`std::env::current_exe()` call, not something this task needs a Windows machine to verify by
inspection of the code path, but say so plainly if you find a reason it differs.
**Owner:** no

## What

Add a field to `StatusResponse` (`src/api.rs`) carrying a hash of the currently-running executable's
own bytes, read via `std::env::current_exe()`. Decision 67 already settled *why* (a self-hash is the
only candidate that answers "what bytes are running," which is what a "did the deploy land" check
needs — a git SHA or build timestamp only proves what was compiled) and *when* (hashed once at
process start into a cached value, never per request — the running process's own bytes cannot change
under it mid-run). Left to this task:

1. **The field's name and shape.** Full hex SHA-256, a truncated prefix, or something else —
   decision 67 deliberately left this open.
2. **A hashing dependency.** None of this crate's current dependencies hash (checked at filing —
   `grep -iE "sha|digest|hash" Cargo.toml` found nothing but comments). `sha2` is the obvious choice;
   confirm it against whatever this suite's other crates already use before adding a new one, so this
   doesn't become the second hashing crate in the workspace for no reason.
3. **Read-once-at-startup wiring.** A `std::sync::OnceLock<String>` (or equivalent) populated on
   first access or at process start, not re-read per `/status` call. Handle the read failing (the exe
   path unreadable, permissions) without taking `/status` itself down — decide what the field reads
   as in that case (omitted, `null`, or an explicit error string) and say so in the decision that
   documents this.
4. **The pinned-field-set test.** Decision 13 records that `StatusResponse`'s serialized key set is
   pinned by a test in `api.rs`; that test will need the new field added deliberately, which is the
   point of it existing.

**This is a wire-schema bump.** Per `../../embarch-fleet/ops.md` §4, the supervisor announces it in
`#embarch-fleet` and the announcement window must close with no objection before this task is
dispatched to a worker — do not self-dispatch this because the shape feels additive. `/status`'s
response is read by `embarch-api`, `embarch-ui` and `embarch-umbrella`; an added field is unlikely to
break a consumer that only reads known keys, but that is exactly the kind of assumption the
announcement step exists to catch before it lands, not after.

## Why now

`embarch-core` decision 67 decided this should ship rather than stay a "no": the gap it closes for
content is the same gap decision 13 already closed for version, and decision 13 was built on
identical reasoning. Not urgent — nothing is broken, a capability is missing.

## Done when

- [x] `StatusResponse` carries the new field, computed once and cached, not re-hashed per request.
      Field: `binary_sha256: Option<String>`, full 64-char lowercase hex SHA-256 of
      `std::env::current_exe()`'s bytes, hashed once via a `static HASH: OnceLock<Option<String>>`
      in `api.rs`. `None`/`null` if the exe path or its read fails.
- [x] The pinned-field-set test in `api.rs` (decision 13) is updated to expect it. Also added
      `status_serves_a_self_hash_of_its_own_binary`, mirroring the existing `core_version` test:
      hits `/status` in-process and checks the served hash against an independently-computed
      SHA-256 of the same test binary's own exe bytes.
- [x] `embarch-core/interfaces/hardware.md`'s `/status` row documents the new field — name, shape,
      what it proves, and the `null`-on-read-failure case.
- [x] `embarch-core/decisions/surfaces.md` gets decision 68, citing decision 67. **This did spend
      the last of the 163 B headroom** — the file is now 11579/12288 B (94.2%), so
      `tasks/core/091-compact-core.md` is filed in this commit, `In flux: yes` (four edits to this
      file in one day: `core/074`, `core/077`, `core/078`, this one). `decisions.md` line 21's
      Decisions and Size cells are updated for this row only, per the header's instruction not to
      touch the other twenty.
- [x] `embarch-core/open.md` loses the "designed, not built" bullet this closes.
- [x] A `changelog.d/` fragment (`changelog.d/core-status-binary-hash.added.md`) and a
      `features.d/` row update (`features.d/core-010-get-status-connected-probes-plus.md`, the
      existing `/status` row, now naming `binary_sha256` and decision 68).
- [x] **The task file's `status.d/` instruction does not hold — filed as a finding, not done as
      written.** `embarch-umbrella/open.md` is not one of the six shared suite-level docs
      `status.d/README.md` and `DOC-PROTOCOL.md` §2 name (`embarch.md`, `suite/roadmap.md`,
      `suite/features.md`, `embarch-decision-reversals.md`, `embarch-glossary.md`,
      `suite/user-guide.md`) — it's `embarch-umbrella`'s own sub-project doc, out of a
      `core`-scoped worker's ownership row the same way any other repo's file is. Dropped
      `/home/gabriel/Github/embarch/embarch-doc/inbox/umbrella-status-hash-landed.md` instead (full
      task format, quoting the stale bullet verbatim) — the mechanism this repo's own worker
      contract names for exactly this case.
- [x] Gate green per `../../embarch-fleet/protocol.md` §10 — `cargo build`/`test`/`clippy
      --all-targets -- -D warnings` clean in `embarch-core`; `check-docs.py` in `embarch-doc` is
      10/11 green, the one red (`check-links.py`, `tasks/umbrella/087...md -> ../open.md`) is a
      pre-existing broken link in a file this unit never touched (`embarch-umbrella`'s own task,
      not core's); `check-ownership.py` clean in both worktrees;
      `check-client-names.py --repo <core worktree>` clean.

## Not yours

- **Do not change `embarch-umbrella`** — not check 15, not `decisions/schema-skew.md`, not its
  `open.md`. Consuming the new field is that repo's own unit, once this lands.
- **Do not bump any other route's response shape.** This is additive to `/status` alone.
- **Do not skip the announcement** because the field feels harmless to add.
