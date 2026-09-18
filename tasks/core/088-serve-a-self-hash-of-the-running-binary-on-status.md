# 088 — Serve a self-hash of the running binary on `/status`

**State:** open

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

- [ ] `StatusResponse` carries the new field, computed once and cached, not re-hashed per request.
- [ ] The pinned-field-set test in `api.rs` (decision 13) is updated to expect it.
- [ ] `embarch-core/interfaces.md` (or `interfaces/*.md`) documents the new `/status` field —
      name, shape, what it proves, and what it reads as if the self-read fails.
- [ ] `embarch-core/decisions/surfaces.md` gets the implementation decision (numbered), citing
      decision 67 — the field's exact shape, the dependency chosen, and the failure-mode answer.
      **Check `scripts/check-doc-size.py --pressure` before writing** — decision 67 already used
      most of the reserve this compaction bought back; if `surfaces.md` is back in the band, file
      `tasks/core/<NNN>-compact-core.md` in the same commit rather than picking a file by where
      there is room.
- [ ] `embarch-core/open.md` loses the "designed, not built" bullet this closes, if one exists there
      by the time this runs (it does not exist yet at filing — decision 67 is not phrased there as
      an open item, since it resolved to "build it" rather than "defer it").
- [ ] A `changelog.d/` fragment. A `status.d/` fragment for `embarch-umbrella`'s `open.md` bullet
      this closes — that file is not this task's to edit (`suite`/cross-repo docs are out of scope
      for a `core`-scoped worker), so the fragment is how the fact reaches the fold.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.

## Not yours

- **Do not change `embarch-umbrella`** — not check 15, not `decisions/schema-skew.md`, not its
  `open.md`. Consuming the new field is that repo's own unit, once this lands.
- **Do not bump any other route's response shape.** This is additive to `/status` alone.
- **Do not skip the announcement** because the field feels harmless to add.
