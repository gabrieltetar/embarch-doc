# `ValidateResponse` now hard-requires a Core new enough to send `validated_at_utc_ms`

**State:** open
**Source:** `tasks/api/045` (leg 043), raised by me at the merge diff and
independently by that unit's reviewer, which found no decision either way and
correctly declined to file it as a contradiction.
**Scope:** api
**Hardware:** none

## What

`api/045` added `validated_at_utc_ms` to
`crates/embarch-core-client/src/client.rs`'s `ValidateResponse` as a **required**
serde field. It mirrors `embarch-core`'s `ValidateOkResponse` exactly, which is
right, and every gate passed.

But this same file carries an explicit precedent going the other way. At least
two fields — `link_port_interface` and `study_designer_schema_version` — are
`#[serde(default)]`, and a test near the end of `client.rs` asserts in so many
words that *an older Core that predates `link_port_interface` still parses*. So
the crate has, at least twice, chosen to keep deserializing a Core that predates
a field. `validate` now does the opposite: against an `embarch-core` older than
`tasks/core/026` (merged `b0bf60d`), **every** `validate` call fails at
deserialization rather than coming back with the one timestamp that Core does
send.

**This is not hypothetical on this machine.** The live Core is a deployed
Windows service and `embarch-api` is built separately; the two are not
guaranteed to move together, and "the MCP binary goes stale after a schema bump"
is already a recorded gotcha. A rebuilt `embarch-api` against a
not-yet-redeployed Core is the exact configuration this breaks, and the failure
is a parse error rather than a missing field — which reads like a broken client,
not a version skew.

## The question, which is the point of the task

**Does `embarch-core-client` promise to parse an older `embarch-core`?** The
reviewer looked in `embarch-api/decisions/core-link.md` and `spec.md` and found
no decision stating one way or the other, so today it is a per-field judgement
call made three times with two different answers. That is the defect: not the
missing `#[serde(default)]`, but that nothing says whether it should be there.

Two honest answers, and either is fine as long as it is written down:

- **Yes, within reason.** Then `validated_at_utc_ms` takes `#[serde(default)]`
  (a `0` or an `Option`, whichever reads honestly at the call sites — a `0`
  timestamp presented as "validated at 1970" would be worse than the bug), the
  CLI and MCP surfaces say "not reported by this Core" rather than printing a
  zero, and the two existing precedents stop being accidents.
- **No.** Then say so, and the existing `#[serde(default)]` fields are the
  anomaly rather than the rule — and something should fail loudly and legibly on
  a version skew instead of at a serde error.

## Why now

Not urgent — nothing is broken against a current Core, and `api/045` is not
wrong. It is filed while the context that produced the question still exists,
which is the only cheap moment to file it.

## Done when

- [ ] An `embarch-api` decision states whether `embarch-core-client` parses an
      older Core's responses, and on what basis — citing the
      `link_port_interface` precedent and this field as the two data points.
      Decision numbers are global across `decisions/*.md`; take the next number
      after the directory's maximum, not the file's.
- [ ] `ValidateResponse`'s `validated_at_utc_ms` matches whatever that decision
      says, and if it gains a default, no surface prints a fabricated timestamp
      for a Core that never sent one.
- [ ] If the answer is "yes", the two existing `#[serde(default)]` fields are
      named in that decision as the same rule rather than left as precedent
      nobody cited.

**Note on the reserve:** `embarch-api/decisions/core-link.md` had **22 bytes**
of headroom as of 2026-09-07, with its compaction task (`tasks/api/026`) parked
`In flux: yes`. This decision plausibly belongs in that file. Whoever takes this
must read `DOC-COMPACTION.md` §2 first: compacting the file you are writing into
is part of this unit, carrying `tasks/api/026`'s `Must not delete:` list
verbatim and closing only that file's item.
