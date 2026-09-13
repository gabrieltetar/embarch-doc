# 035 — compact `embarch-topology`: `decisions/crate.md` and `spec.md` are both in reserve

**State:** claimed — leg 103, 2026-09-12.

**Source:** filed by leg 100 on 2026-09-12 in the same commit as the work that spent the reserve
(`suite/020` half (a), `embarch-topology` decision 31). The rule is `.claude/leg.md`'s: the actor
that pushes a file into reserve files the debt while it still holds the context nobody else will.
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** `embarch-topology/decisions/crate.md`, `embarch-topology/spec.md`
**Size debt due:** 2026-10-12
**In flux:** per file — `embarch-topology/decisions/crate.md` no, `embarch-topology/spec.md` yes.

## What

Decision 31 added ~2.9 KB to `decisions/crate.md` (11,926/12,288 B, **362 B left**) and a paragraph
to `spec.md` (9,570/10,240 B, **670 B left**). Both are now inside the last 10% of their caps.

## In flux, per file

- **`decisions/crate.md` — not in flux, and it wants a split rather than a squeeze.** It holds eight
  decisions (1, 2, 3, 4, 6, 8, 13, 31) answering two different questions that have drifted apart:
  1, 2, 3, 6, 13 are *"one crate, called live, in-process"* — settled for weeks, nothing pending
  touches them. 4, 8 and 31 are *"what a consumer may link, and what the crate owes a consumer that
  cannot link all of it"* — 4 and 8 have each been qualified twice (2026-09-08 and 2026-09-12) and
  **both currently say in their own text that they are not yet true as written**, because
  `tasks/suite/035` has not landed. A verbatim split along that seam gives the churning half its own
  12,288 B cap, exactly as `core/035` did for `decisions/flashing.md` on 2026-09-12. Suggested new
  file: `decisions/consumer-boundary.md` carrying 4, 8, 31.
- **`spec.md` — in flux.** Its "What each consumer owns now" section is precisely what
  `tasks/suite/035` rewrites: when `embarch-core-client` stops mirroring, the three-feature
  paragraph this unit added gets a fourth sentence and the `embarch-api` bullet changes. Leave it
  alone until `suite/035` lands, then compact both in one pass.

## Must not delete

- `cargo tree -e normal --no-default-features --features wire` and its three-crate answer — it is
  the only stated way to verify the feature boundary actually holds.
- The reason `detected_by` became a `String` (a `&'static str` field cannot derive `Deserialize`).
- The reason the types were **not** moved to a new module (`super::`-relative rustdoc links).
- Decision 4's and 8's "still not true as written until `suite/035` lands" clauses. Those are the
  honest record of a half-finished change and must not be tidied away before it finishes.

## Dispatch note (leg 103)

**`suite/035` has landed** — `embarch-api` `7d817a3`, `embarch-topology` `83af7ed`, folded on
`embarch-doc` `2b9c258` at 12:45 today. That is the thing this task named as what unparks
`spec.md`, so **both files are yours in one pass** and the `In flux: per file` line above is
now stale: neither is in flux. Update that line as part of the work.

Two consequences you must check rather than assume:

- Decisions 4 and 8's "not yet true as written until `suite/035` lands" clauses. `suite/035`
  landed, and its own fold entry says decisions 4 and 8's "holds now" claims were rewritten to
  match the landed code. Read what is on `main` today before you carry those clauses forward
  verbatim — the `Must not delete:` item was written when they were still false.
- `spec.md`'s "What each consumer owns now" section was rewritten by `suite/035`'s doc side.
  Compact what is there now, not what the task description above describes.

Do the split verbatim: `decisions/consumer-boundary.md` carrying 4, 8 and 31, and
`decisions.md`'s index table updated to name it. A verbatim split restates nothing, so it
cannot introduce a contradiction — resist the urge to also reword while you are in there.

## Done when

- [ ] `decisions/crate.md` is out of reserve, by a verbatim split along the seam above.
- [ ] `decisions.md`'s index table names the new file and the decisions in it.
- [ ] `spec.md` is either out of reserve or its item here is struck off with `suite/035` named as
      what unparks it.
- [ ] Gate green.
