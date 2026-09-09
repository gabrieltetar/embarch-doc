# 051 — The drain's stream-decoding policy is filed inside decision 18, which is about the truncation cap

**State:** open
**Source:** `inbox/api-030-review-finding.md` — `embarch-reviewer` on unit `api/030`
(code merge `a0950ec` in `embarch-api`, doc merge `d2ab624` in `embarch-doc`),
filed into the queue by leg 055 on 2026-09-08.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api/decisions/build.md` decision 18 is about what a *truncated* build log
keeps — the head/tail split at `OUTPUT_CAP_BYTES`, and the UTF-8-boundary rounding
on the two cuts. `api/030` amended it with a paragraph describing a change to
`drain_stream`: reading raw bytes with `read_until`, decoding per line, falling
back to `from_utf8_lossy` for only the failing line and naming the substitution in
a marker. That fix lives upstream of truncation and fires on logs that are nowhere
near the cap, so it is a design call on a different axis — how the drain reads a
child stream — with real rejected alternatives (decode the whole buffer lossily;
fail the build on bad bytes) recorded nowhere.

Settle it one of two ways, and only one of them is a new decision:

- give the drain-decoding policy its own numbered decision in
  `decisions/build.md`, moving the amendment's substance there and leaving
  decision 18 about the cap; **or**
- widen decision 18 deliberately, in which case its heading must say so — it
  becomes "faithful and complete log capture" rather than "what a truncated log
  keeps".

**Not dispatchable under burndown.** The first disposition authors a new numbered
decision, which [burndown.md](../../embarch-fleet/burndown.md) forbids outright,
and the second is a call that should not be forced by which mode the fleet happens
to be in. Leave this task for a normal-mode or attended leg. It is filed `open`
rather than `blocked` because nothing needs to be unblocked — only the mode has to
be off.

Note the byte pressure before starting: `decisions/build.md` is 11,134 / 12,288 B
and already across its reserve line, with `tasks/api/050-compact-api.md` filed
against it and blocked on `In flux: yes`. Moving a paragraph within the file is
byte-neutral; adding one is not.

## Why now

The reviewer's own reason, and it stands: cheapest to settle before another unit
builds on decision 18 assuming it covers stream-decoding policy. The suite's
`embarch-decision-reversals.md` calls a decisions file that describes the wrong
thing the worse variant of its most common failure, and leg 054's own log entry
records this as the thing it was least sure about leaving in `inbox/`.

## Done when

- [ ] One of the two dispositions above is applied to `decisions/build.md`.
- [ ] No code change to `a0950ec` — this is an attribution question, and the
      reviewer verified the code and decision 18's boundary arithmetic are both
      correct as they stand.
- [ ] `changelog.d/` fragment dropped; no `status.d/` fragment is expected.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
