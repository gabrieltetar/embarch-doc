# 055 — `resolve_probe` keeps its own copy of a selection rule `embarch-topology` is about to expose

**State:** blocked
**Blocked on:** `tasks/topology/038` landing on `main`. That task exposes
`embarch-topology`'s probe-selection rule as a `pub` function; until it does, there is nothing for
this change to call and a `core`-scoped worker may not write `embarch-topology`. **Unparks the
moment `topology/038` is merged** — a supervisor checking this task should verify that
`pub` function exists in `embarch-topology` on `main` and then flip this to `open`.
**Source:** `inbox/core-resolve-probe-duplicates-topology-enroll-selection.md`, the follow-up to
`tasks/topology/037` and `embarch-topology` decision 32. Split into two tasks by the leg of
2026-09-13 17:5x because the drop's own "Done when" names a `topology` prerequisite that a `core`
worker cannot satisfy.
**Scope:** core
**Hardware:** none — a code-structure change; nothing is executed.
**Owner:** no

## What

`embarch-core::resolve_probe` (`src/hardware.rs`, `pub(crate)`) is an independently maintained
second copy of the probe-selection rule that also lives inline in
`embarch_topology::hardware::validate::enroll`. They were one implementation before `embarch-core`
decision 22 moved the board-identity gate (`board_gate.rs`) wholesale into `embarch-topology`;
`pub(crate)` cannot cross the crate boundary that move created, so the move silently forked one rule
into two.

**They have already drifted** — `topology/038` enumerates three concrete differences that exist on
`main` today (the zero-probe special case and its usbipd hint, `len() > 1` versus `len() != 1`, and
every error string). Read that task file before you start; it is where the reconciliation was
argued, and it names what the shared function gives up.

Once `topology/038` lands, make `resolve_probe` call the shared function and drop its own inline
copy.

## The one thing to be careful about

`resolve_probe`'s zero-probe message is the only genuinely diagnostic string in either copy:

> no debug probe found — check the USB connection (and usbipd attach, if Core is on a Pi and the
> probe is elsewhere)

That hint is specific to **Core's** deployment topology — Core on a Pi, probe elsewhere — and is
about the thing `embarch-topology` has no business knowing. If `topology/038`'s reconciled wording
dropped it, **do not accept the loss silently**: either the shared function takes a caller-supplied
context and `resolve_probe` supplies this one, or `resolve_probe` wraps the shared error and adds
it. Say in your commit and changelog fragment which you did. Losing that sentence is a real
regression in an error a human reads at exactly the moment they are confused.

Also update `open_probe`/`resolved_serial`'s doc comments, which describe `resolve_probe` as
resolving the choice itself — **that becomes false when it delegates.** Do not repoint the citation
without reading whether the surrounding sentence also went false; that has been the real yield of
four consecutive citation units this week.

## Flag back, do not fix

`embarch-topology` decision 32 and `embarch-topology/open.md` carry the matching bullet saying the
duplication is open. Closing them is `topology`'s edit, not yours (`topology/038` amends decision 32
with a dated note naming this task). **If this lands and no matching topology-side update has
happened, file an `inbox/` drop saying so** — do not write `embarch-topology`.

## Reserve, for planning

`embarch-core/decisions/auth.md` is **11,356/12,288 B — 932 B left, 92.4%**, filed against
`tasks/core/046` (`blocked`). This unit should have no reason to touch it; if it does, or if your
work leaves any `embarch-core` doc in the last 10% of its cap unfiled, file
`tasks/core/<next>-compact-core.md` in the same commit — **your own scope**, never `tasks/doc/`.

## Done when

- [ ] `resolve_probe` calls `embarch-topology`'s shared selection function and keeps no inline copy.
- [ ] The usbipd/zero-probe hint survives somewhere a caller of `resolve_probe` still sees.
- [ ] `open_probe`/`resolved_serial` doc comments corrected, not just repointed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including a native Windows build note if
      one is owed — `core/015`'s outstanding native build already carries twelve landed changes.
- [ ] `spec.md`/`decisions.md` updated, `changelog.d/` fragment dropped.
