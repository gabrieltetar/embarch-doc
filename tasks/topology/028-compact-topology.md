# 028 — `decisions/validation.md` is in reserve

**State:** claimed — leg 084, 2026-09-11
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by the STM32G0 amendment to decision 25, 2026-09-11
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/decisions/validation.md
**Size debt due:** 2026-09-18

**Reserve in `embarch-topology` at dispatch (leg 084):** `decisions/validation.md` 12,278/12,288 B
(10 B left) — the file this task pays. Nothing else in the sub-project is in reserve, so a split
that moves text into a *new* topic file has the whole cap to land in. If your work leaves any
`embarch-topology` file in reserve that nothing has filed, file
`tasks/topology/<NNN>-compact-topology.md` in the same commit.

## What

Adding an STM32G0 arm to `classify_chip` (96-bit `UID_BASE` readback, so an ST
board can be enrolled and pass the identity gate) amended decision 25 and put
this file at **12,278 / 12,288 B (99.9%), 10 B left**. The amendment was already
cut roughly in half against a first draft before landing; the remaining text is
load-bearing, so the next edit to this file has nowhere to go.

`tasks/topology/014` also lists this path, but predates the vendor-arm material
entirely — the reserve was spent again after it was filed.

## Why now

Ten bytes is not headroom. The next arm added to `classify_chip` — and there
will be one, since the whole shape of decisions 21/25 is "a family at a time,
on evidence" — cannot be documented here at all without first doing this work.

## In flux: no

Decisions 21 and 25 are both closed units. Nothing queued against
`embarch-topology` touches the chip classifier further as of 2026-09-11.

## Done when

- [ ] `decisions/validation.md` is out of reserve, or the task says why it
      cannot be and what was deleted instead.
- [ ] Prefer a split per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 before
      deleting live reasoning. A seam is already visible: 21 is *the
      self-report comparison* (what a board says about itself vs. JTAG), 25 is
      *the classifier* (which register pair holds the ID at all) — two
      questions that now have three vendors' worth of argument between them.
- [ ] Whichever it was — split or delete — is stated, with byte numbers before
      and after.

## What the pass may not delete

- **Why `classify_chip` returns `None` for nRF54H rather than guessing a
  register pair**, and that this is an *abstention* while `embarch-core`'s
  `requires_vendor_tool` is a *positive refusal*. The file says explicitly that
  reading the second as agreement with the first is how someone unifies them by
  mistake; that warning has already been re-litigated twice.
- **Why the two matchers are deliberately not unified** (the paragraph citing
  `tasks/suite/024`). It exists so a third reader stops filing it as new.
- **Why the STM32 prefix stops at `stm32g0`** — `UID_BASE` moves between STM32
  families, so a vendor-wide prefix reads a plausible-looking value off the
  wrong address. The narrowness is the correctness argument, not a detail.
- **The `read_words` two-word compatibility note**: a two-word slice must keep
  emitting byte-identical output or every `hardware_id` already in
  `enrollment.toml` silently stops matching at its next gate check.

**Human question (`DOC-COMPACTION-PASS.md`):** can `embarch-topology/spec.md`
alone answer what someone needs to know to add the next chip family? Answer it
in the report, in your own words.
