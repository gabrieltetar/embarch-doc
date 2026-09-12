# 043 — The stream index's documented shape is three fields short, and `self_excluded` is the one missing

**State:** claimed (leg 090, 2026-09-11)
**Source:** refill sweep for scope spread, leg 089, 2026-09-11. Filed rather than dispatched because
leg 089 reached its four-unit cap; not yet re-verified by a supervisor, so **check every line number
below against the source before you act on it** — they are as the sweep reported them.
**Scope:** core
**Hardware:** none.
**Owner:** no

## What

Two `embarch-core` interface docs describe the stream index, and both describe a smaller structure
than the code serializes.

**1. `embarch-core/interfaces/studies.md:16`** documents the route's response as:

> `{streams: [{id, name, encoding, alias, rendered, note?}]}`

`StreamIndexEntryResponse` (`embarch-core/src/study.rs:2849-2876`) serializes those **plus `named`,
`timed` and `self_excluded`**.

**2. `embarch-core/interfaces/result-layout.md:22`** says:

> `named` and `timed` are two independent booleans in the index and on the wire — a trace can be
> named and untimed, or neither.

`StreamIndexEntry` (`embarch-core/src/stream_store.rs:208,215,233`) carries **three**: `named`,
`timed` and `self_excluded`, the last one documented *in the code* as "The third way a trace can be
incomplete". The same file's line 14 lists the index entry without them too.

**A third document already has it right.** `embarch-outpost/spec.md:90` says *"three independent
booleans … `named`, `timed`, and `self_excluded`"*. So two `embarch-core` docs disagree with an
`embarch-outpost` doc about the contents of an `embarch-core` struct.

## Why it costs something

That route exists, by its own doc row, to answer *why a trace has no names when it has none*. The
booleans that answer it are exactly the ones the documented shape omits — so a client written to
this table has no field to branch on and falls back to pattern-matching `note`'s prose, which the
code's own comments explicitly warn against.

`result-layout.md`'s version is worse than incomplete: it asserts there are **two** and that they are
the whole story. A reader who trusts it treats an interval no lane covers as a defect, when
`self_excluded` declares it as deliberate.

## What to do

Correct both files to the shape the code actually serializes, **counting the struct fields yourself
rather than trusting this task or either doc** — a doc that is wrong about a field set is exactly
the thing not to take a field set from.

`result-layout.md`'s sentence needs more than a number: it explains what the booleans *mean*, so
`self_excluded` needs its one-sentence meaning there too, in the same register as the other two.
Take that meaning from the code's own comment and from `embarch-outpost/spec.md:90` — **do not invent
one**, and do not widen this into a decision about self-exclusion's semantics. If the three
documents turn out to disagree about what `self_excluded` means rather than merely how many there
are, stop and say so here rather than picking a winner.

**Then check the rest of both files' field lists against the structs they describe.** Two independent
instances in two files is a pattern, not a coincidence.

## Wire-shape note

This is documentation catching up to shipped code — the fields are already serialized, so nothing
here changes the wire and **no announcement window is owed**. If your reading says otherwise, that
is a reason to stop, not to proceed.

## Done when

- [ ] `interfaces/studies.md`'s response shape lists every field `StreamIndexEntryResponse`
      serializes, verified by reading the struct.
- [ ] `interfaces/result-layout.md` says three booleans, names `self_excluded`, and gives its meaning.
- [ ] The meaning is sourced from the code or `embarch-outpost/spec.md`, not composed.
- [ ] A pass over both files' other field lists is reported here.
- [ ] No code changes and no wire change.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
