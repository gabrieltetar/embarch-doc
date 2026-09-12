# 043 — The stream index's documented shape is three fields short, and `self_excluded` is the one missing

**State:** done (leg 090, 2026-09-11)
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

- [x] `interfaces/studies.md`'s response shape lists every field `StreamIndexEntryResponse`
      serializes, verified by reading the struct.
- [x] `interfaces/result-layout.md` says three booleans, names `self_excluded`, and gives its meaning.
- [x] The meaning is sourced from the code or `embarch-outpost/spec.md`, not composed.
- [x] A pass over both files' other field lists is reported here.
- [x] No code changes and no wire change.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.

## Report (leg, 2026-09-11)

Verified against `embarch-core/src/study.rs:2848-2876` (`StreamIndexEntryResponse`) and
`embarch-core/src/stream_store.rs` (`StreamIndexEntry`): both carry `named`, `timed`,
`self_excluded` alongside the previously-documented fields. `embarch-outpost/spec.md:90`'s
"three independent booleans" wording agrees with both structs' own doc comments — no
disagreement to flag, so no decision needed.

- `interfaces/studies.md`'s `/study/{id}/streams` row now lists `named?, timed?, self_excluded?`
  in the response shape, with a one-clause pointer to `result-layout.md`.
- `interfaces/result-layout.md`'s `index.json` file-tree line now lists `named, timed,
  self_excluded`; its prose sentence now says three booleans and gives `self_excluded`'s meaning
  (firmware-decided self-exclusion of the outpost's own drain thread/UART interrupt), sourced from
  `stream_store.rs`'s own comment and `embarch-outpost` decision 19/spec.md:90.
- Pass over the rest of both files' field lists: checked `/study/{id}`, `/study/{id}/steps`
  (`StudyStepsResponse`/`StudyStepEntryResponse`) and `/study` responses against `src/study.rs` —
  all match what's documented. No further discrepancies found.
- No code changes, no wire change (fields were already serialized).
