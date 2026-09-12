# 044 — Decision 56 calls three doc comments "the whole remaining work", and none of them exists

**State:** open
**Source:** refill sweep for scope spread, leg 091, 2026-09-11. **Line numbers are as the sweep
reported them — re-check each against the source before you act on it.**
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/decisions/handshake.md:49` (decision 56) says:

> `EnrollProbeResponse`, `ValidateResponse` and `EnrolledBoardResponse` each carry a doc comment
> saying their `hardware_id` is the probe-read value and pointing here… **That is the whole
> remaining work**, and `embarch-core`'s wire surface does not change.

Three things are reported wrong about that sentence:

- `src/api.rs:696-701` — `EnrollProbeResponse`'s `hardware_id: String` carries **no doc comment**.
- `src/api.rs:978` — the validate-success type is named **`ValidateOkResponse`**, not
  `ValidateResponse`, and its `hardware_id` is bare too; the doc comment on the *next* field,
  `confirmed_at_utc_ms`, came from decision 50 and is a different subject.
- There is **no `EnrolledBoardResponse` type in this crate at all**: `src/api.rs:737` serves
  `embarch_topology::hardware::EnrolledBoard` directly, so the promised comment could not live here
  even in principle. The only occurrence of the name is a comment at `api.rs:1784` describing a
  "hand-maintained mirror".

## Why it costs something

Decision 56 traded away a rename **on the explicit condition** that the probe-read-versus
self-reported distinction be legible at the struct and not only on the wire. The payment was never
made, so the next reader of `hardware_id` on those routes re-derives the distinction across two
repos — which is the confusion decision 47 was written about.

## What to do

Verify all three claims yourself. Then **pay the decision rather than weaken it**: add the doc
comments decision 56 promised, on whichever types actually carry a probe-read `hardware_id` in this
crate, and correct decision 56's own sentence to name the real types. If one of the three genuinely
cannot carry a comment here because the type belongs to `embarch-topology`, say that in the decision
body — do **not** cross the ownership line to add a comment in that repo; if the comment belongs
there, file it to `/home/gabriel/Github/embarch/embarch-doc/inbox/` as a `topology`-scoped task.

No new numbered decision: this is decision 56's own unpaid half.

## Done when

- [ ] Every type decision 56 names either exists and carries the comment, or the decision names the
      type that really exists instead.
- [ ] The `EnrolledBoardResponse` claim is resolved one way or the other, in writing.
- [ ] No wire-surface change (decision 56 says there is none; keep that true).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.

## A second, separable thing in the same sub-project

`src/flash_backend.rs:47-49` cites **decision 50** for the `nrfjprog` retirement. The retirement is
`decisions/flashing.md:99`, **decision 54**; decision 50 is `decisions/enrollment.md:20`, the
`/validate` timestamp field. The comment also dates it 2026-09-10 where `flashing.md:104` dates the
review 2026-09-06. Correct the citation and the date, in the settled form (bare `decision N`
same-repo). Note `enrollment.md:25` records a prior `54`→`57` renumber, so **read both bodies before
concluding which number is right** rather than trusting the heading.
