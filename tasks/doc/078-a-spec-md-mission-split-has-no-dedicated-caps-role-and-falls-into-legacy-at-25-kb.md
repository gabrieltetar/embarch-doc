# 078 — A `spec.md` mission split has no dedicated CAPS role; it falls into `legacy` at 25 KB

**State:** open
**Filed by:** leg 137, 2026-09-17, from `inbox/doc-spec-split-legacy-cap.md`, written by the
`topology/057` worker as it landed the split that produced the first such file. Filed verbatim
except for this header, the `**Owner:**` line below, and the note at the end. I re-checked the
`Hardware: none` claim and it holds: this is a read of `scripts/check-doc-size.py` and
`DOC-BUDGET.md`.
**Owner:** required — the fix is an entry in `scripts/check-doc-size.py`'s `CAPS` list and a row in
`DOC-BUDGET.md`, both owner-reserved. Recorded here so it is visible in the queue rather than
nowhere; `queue-status.py` gates it out of the dispatchable count by itself.
**Source:** `topology/057`, 2026-09-17 — filed while paying `embarch-topology/spec.md`'s reserve
debt by splitting its "Storage and roles" section verbatim into
`embarch-topology/spec/storage-and-roles.md`, per `DOC-BUDGET.md`'s split-first rule and
`DOC-PROTOCOL.md` §3's "each [of the four files] splits into `<topic>/` files by mission when it
outgrows one."
**Scope:** doc
**Hardware:** none

## What

`scripts/check-doc-size.py`'s `CAPS` list has a dedicated, tightly-scoped pattern for a
`decisions.md` split (`decision-group`, 12 KB, `embarch-[a-z-]+/decisions/[a-z-]+\.md`) and for an
`interfaces.md` split (`interface-group`, 12 KB, the same shape). It has no equivalent
`spec-group` pattern for `embarch-[a-z-]+/spec/[a-z-]+\.md`. `embarch-topology/spec/storage-and-roles.md`
(new this task) falls through every named role and lands in the catch-all `("legacy", 25 * KB,
re.compile(r"^(embarch-[a-z-]+/|embarch[-.]|DOC-|README)"))` — the bucket whose own comment says
"anything else still under a sub-project or the root is legacy, and the migration's job is to turn
it into one of the roles above."

So the new file is capped (25 KB, not uncapped — I initially assumed a CAPS miss meant invisible to
the gate and traced through `role_and_cap`/`docs()` to confirm it is not), but at four times the cap
its sibling split shapes get, with no reserve-band or ratchet reasoning behind that number — it is
simply the generic legacy fallback, not a considered cap for this shape.

## Why now

This is the first time a sub-project's `spec.md` has split by mission in this corpus (verified:
`find . -type d -name spec` returned nothing before this task). `decisions.md` and `interfaces.md`
both got a purpose-built `CAPS` entry the first time *they* needed to split. If `spec.md` splits
become routine the way `tasks/doc/052` documented decision-file splits becoming routine on
2026-09-13, every one of them will sit in `legacy` at 25 KB rather than a considered cap, and
`scripts/` is reserved to the owner, so no worker or supervisor can add the entry.

## Done when

- A `spec-group` `CAPS` entry exists for `embarch-[a-z-]+/spec/[a-z-]+\.md` (owner's call on the
  number; `decision-group`/`interface-group`'s 12 KB is the closest precedent, but a spec-topic file
  reads more like reference prose than a decision entry, so it may deserve its own number), **or**
  the owner decides `legacy` at 25 KB is fine for this rare a shape and says so, closing this task
  with that reasoning recorded.
- `DOC-BUDGET.md`'s caps table gains the corresponding row either way, so `--report`'s `spec-group`
  vs `legacy` label matches what the table says a spec split actually costs.

## Not in scope

- Whether `embarch-topology/spec.md` *should* have split this way at all — that call was made in
  `tasks/topology/057` and is not reopened here. This is only about the cap the new file landed
  under.
