# 051 — The drain's stream-decoding policy is filed inside decision 18, which is about the truncation cap

**State:** claimed — leg 068, `agent/api/051-drain-decoding-decision`

**Dispatch note, leg 068 — the disposition is decided, and so is how you pay for it.**

**Take the first arm: the drain-decoding policy gets its own numbered decision in
`embarch-api/decisions/build.md`'s successor file, and decision 18 goes back to being about the
cap.** The task offered two arms; I am closing that as the supervisor. Widening decision 18 would
make one decision cover two axes that fire at different times — the drain reads every line, the cap
fires only past `OUTPUT_CAP_BYTES` — and this suite's `embarch-decision-reversals.md` names a
decisions file that describes the wrong thing as the worse variant of its commonest failure. Move
the substance of `api/030`'s amendment out of decision 18 into the new decision, and record the two
rejected alternatives the task names: decode the whole buffer lossily, and fail the build on bad
bytes.

**Do the split FIRST, and do it verbatim.** `decisions/build.md` is 11,134/12,288 B — 1,154 B left,
inside its reserve — and its compaction task `tasks/api/050` is blocked on `In flux: yes`. That park
does not forbid you here: `tasks/api/050` names the unpark itself as *"a mission split ... judged
safe to do verbatim"*, and a verbatim split restates nothing, so `In flux: yes` cannot forbid one
(`DOC-COMPACTION.md` §2, split-first). The four missions `api/050` identifies are decision 5's
generic-command call, decision 18's log capture/truncation/drain, decision 19's `target.json`
provenance, and decision 42's `base_address`. Split by mission, **moving text byte-for-byte** — no
shortening, no rewording, no "while I am here" edits — then author the new decision in the
log-capture file, where there is now room.

**Carry `tasks/api/050`'s `Must not delete:` list through the split intact**: decision 18's
`[assumed]` provenance note on the 1:3 head/tail split and the exact condition that would move it;
the amendment's point that a drain reading a decode error as EOF is a defect closed rather than a
polish; decision 19's full three-call `target.json` reasoning; decision 42's rejected per-call
`base_address` override. Every one must still be readable in whichever file it lands in. When you
are done, update `tasks/api/050` — strike `embarch-api/decisions/build.md` off its `Compacts:` line
by **deleting** it (never `~~struck~~` in place; that breaks the size gate's parse) and say in the
body that the split paid it.

**No code change.** The reviewer verified `a0950ec` and decision 18's boundary arithmetic are both
correct; this is an attribution question only. Do not touch `src/`.

**Other doc-size reserve in your scope:** `decisions/core-link.md` 188 B left, `open.md` 357 B left,
`spec.md` 815 B left, `interfaces/tools.md` 1,008 B left, `decisions/tool-wrapping.md` **66 B left**
— all filed against blocked tasks. Stay out of all of them; if you must write to one, file the
compaction task in the same commit.
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
decision, which [burndown.md](../../../embarch-fleet/burndown.md) forbids outright,
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
