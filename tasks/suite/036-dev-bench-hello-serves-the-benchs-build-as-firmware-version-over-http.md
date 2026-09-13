# 036 — `GET /dev-bench/hello` serves the bench's build as `firmware_version`, the one rename `embarch-core` decision 47 already made on this exact route

**State:** open — announced in `#embarch-fleet` by leg 105, `ts 1789317643.030479`, 2026-09-13
10:50. Silence-as-consent window closes 11:20. If this leg ends before the window closes, the
next leg **completes** that window rather than restarting it: re-poll
`scripts/fleet-read.py --thread 1789317643.030479` and run it if nothing objected.
**Source:** leg 104, 2026-09-13, while running `tasks/suite/010`. Split out rather than taken,
because it changes a served field and `suite/010`'s announcement window covered the `clamp_version`
fix and the doc comments, not an API rename.
**Scope:** suite
**Hardware:** none — an HTTP response field and its consumers; nothing reaches a board.
**Owner:** no

## What

`embarch-core`'s `GET /dev-bench/hello` returns `firmware_version`
(`embarch-core/interfaces/studies.md`). That value is the **bench's** build. A `Study`'s
`requires.firmware_version` is the **DUT's**. The field a caller should copy this into is
`requires.dev_bench_version` — and `embarch-api`'s reflash gate and `embarch-core`'s study start
both do that crossing by hand.

`embarch-study-designer` decision 74 (landed by `suite/010`) settles the two *wire-and-storage*
spellings: they keep their names, and every reader is told whose build the value is. It explicitly
leaves this third surface open, because the argument that decided the other two does not apply
here.

## Why this one is different

**The rename is cheap on HTTP.** No reflash, no schema bump, no saved study or `StudyResult` on
disk changes — only Core's response body and its consumers.

**And this suite has already made exactly this rename, on exactly this route.** `embarch-core`
decision 47 (2026-09-07, `tasks/core/020`) renamed this endpoint's `hardware_id` to
`self_reported_hardware_id`, because a caller comparing `hardware_id` from here against
`hardware_id` from `/probes/enrolled` got **a near-miss byte-swap rather than a category error**.
That is the same defect shape as this one, one field over, and it was judged worth a breaking
rename.

## The counter-argument, stated so whoever takes this weighs it

Renaming the HTTP field to `dev_bench_version` leaves `HelloAck.firmware_version` on the wire
still called that. So the suite would then have **three** spellings for the bench's build (wire
`firmware_version`, HTTP `dev_bench_version`, study `dev_bench_version`) instead of two, and a
reader tracing one value end to end crosses a rename in the middle. Decision 47's case did not have
that problem: `self_reported_hardware_id` renamed a field Core itself composed.

Whether that is worse than today's collision is the actual question, and it is not obvious.

## Consumers to move if it is taken

- `embarch-core` — the response type for `GET /dev-bench/hello`, and `interfaces/studies.md`.
- `embarch-api` — `dev_bench_hello()`'s response struct and `src/reflash.rs`'s use of it; the
  `dev_bench_hello` MCP tool's output shape.
- `embarch-ui` — check whether anything renders it.
- `suite/user-guide.md` / `suite/studies-guide.md` — check for the field name in a worked example.

## Done when

- [ ] Either the rename lands across every consumer above, **or** this task is closed with the
      reasoning recorded in `embarch-study-designer` decision 74 as the answer that stands.
- [ ] Gate green in every repo touched; `changelog.d/` fragments for each.
