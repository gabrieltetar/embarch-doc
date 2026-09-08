# 022 — `limits.md`'s `MAX_DISCOVERED_SERVICES` row reasserts the service count decision 57 exists to retire

**State:** open
**Source:** `embarch-reviewer` on `study-designer/011` (doc merge `f22a6b4`), filed
as an `inbox/` drop 2026-09-07 and promoted here by leg 047. This is the first
finding in this log that a reviewer caught and the supervisor did not — the
supervisor had flagged the row's `[measured]` tags and mis-framed the actual
problem.
**Scope:** study-designer
**Hardware:** none — this is a documentation-accuracy question. Confirming which
service count is current reads `reference-dut-fw` source, not a board.

## What

`embarch-study-designer/interfaces/limits.md`'s `MAX_DISCOVERED_SERVICES` row
says `reference-dut-fw`'s `lib/ble/ble_def.h`/`ble.c` declares **2** services
today, sourced from `src/limits.rs:80-84`'s doc comment (written `c8bb166`,
2026-08-23).

`decisions/gatt-extract.md` **decision 57** was written 2026-08-31 — later —
and exists *precisely because that two-file bounded read undercounts*. Its own
words: *"Validated against the real checkout: three services where a bounded
read found two."* So the row asserts as current fact a number a locked decision
already established as an artifact of the known-incomplete extraction method,
and it does so **without citing decision 57 at all** — the row `011` replaced
did cite it, and said 3 declared / 7 via live discovery.

The file now also contradicts itself with nothing bridging the two: the
surviving `MAX_MONITOR_TARGETS` row a few lines down still says *"7 services in
total once an encrypted link reaches the rest of the table"*.

## Why now

`011` was not wrong to do what it was asked — it reconciled the doc against the
crate's own doc comment. **The upstream cause is that `src/limits.rs:80-84`'s
comment was never updated when decision 57 landed**, so the doc faithfully
transcribed a stale source. The fix therefore spans both repos, and is a
statement about what a real DUT declares — which is exactly the class of fact a
supervisor must not author at a fold from a source read. Left alone, a reader
hitting `limits.md` gets a worse answer on that one row than the file gave
before `011`.

## Done when

- [ ] `src/limits.rs:80-84`'s doc comment and `interfaces/limits.md`'s
      `MAX_DISCOVERED_SERVICES` row agree with decision 57's validated
      3-services finding — **or**, if the two-file extractor's 2 is genuinely
      what the code bounds against today, the constant's rationale says so
      explicitly. Either way both cite decision 57.
- [ ] `MAX_DISCOVERED_SERVICES` and `MAX_MONITOR_TARGETS` no longer read as
      contradicting each other unexplained (2 declared vs 7 total, same DUT).
- [ ] The row carries an honest provenance tag: the `[measured <date>]` on
      these rows is the date `git log -S` says the *constant was written*, and
      the counts behind it are transcribed from the crate's own doc comments —
      a read of `reference-dut-fw` source, not a live measurement. Do not call
      that measured.

## Do not revert

A plain `git revert f22a6b4` would take the other 43 constants `011` correctly
enumerated with it. Hand-edit the one row.
