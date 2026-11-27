# 228 — the hello mirror paragraph names the drift test

**State:** done — paragraph now names decision 49 drift test; file 10,995 B
**Source:** EMB-600 — a reviewer's finding on `api/226`: two api decisions still described the client's copies of Core's wire as unchecked after `api/226` held them to Core's own types
**Issue:** EMB-600
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`api/226` made `embarch-core-client` path-depend on `embarch-core-wire`
(`embarch-core` decision 164) and added drift tests: each pinned `StudyEvent`
line, and the hello answer, goes through the wire crate's own type, then the
client's, and must serialize back to the same JSON (decision 49, amended in
`decisions/study-events.md`). Decision 101's half of the finding was fixed in
`api/226`'s fold. **Left:** `decisions/hardware-selection.md`'s paragraph
beginning "Mirrors Core's own serialized `HelloAckInfo` field-for-field"
(around line 20). It says the client's hello type is never checked, so a struct
built from the wrong side "compiles and passes its own tests while failing
against a real Core".

Read the paragraph against what `api/226` built, and make it true. The
reviewer and the last supervisor read "the two are never checked against each
other" differently: as the client type against Core's serialized answer (now
covered by decision 49's hello drift test), or as Core's answer against
`embarch_topology::hardware`'s comparison type (not covered by anything new).
Check the code (`crates/embarch-core-client/src/client.rs`, the hello drift
test, and what the paragraph's parenthesis says about the `hardware` feature)
and write whichever reading is the true one: say what is now held by decision
49's drift test, and keep what is still unchecked, if anything is.

Amend in place; do not add a decision. **Do not let the file grow into its
reserve:** `decisions/hardware-selection.md` is 10,991 B, its reserve line is
68 B above that. Rewrite the paragraph's parenthesis (the `SignalLink` history
is decision 72's and can be a link) so the edit is net zero or shorter. If it
cannot be, file `tasks/api/<NNN>-compact-api.md` in the same commit per
`tasks/README.md`.

**Not yours:** every other repo and every other sub-project's docs. No code
change is expected; if the paragraph turns out to describe a gap the drift test
does not cover, say so in the paragraph and in `open.md`, and do not write the
test here.

## Why now

The decision files are the only description of why the client keeps a lenient
hello type, and this one still describes the state before `api/226`.

## Where to look

- `embarch-doc/embarch-api/decisions/hardware-selection.md` (the paragraph)
- `embarch-doc/embarch-api/decisions/study-events.md` (decision 49, the
  2026-11-27 paragraph), `decisions/lease.md` (decision 101, already fixed:
  the shape to follow)
- `crates/embarch-core-client/src/client.rs` (`HelloAckResponse`) and the hello
  drift test `api/226` added (`caa03e5`)
- **Size:** `decisions/client-crate.md` is in reserve (456 B left,
  `tasks/api/222`); you should not need it.

## Done when

- [x] The paragraph says what decision 49's hello drift test holds, links it,
      and states only what is still true about anything unchecked.
- [x] `decisions/hardware-selection.md` is no larger than 11,059 B, or a
      compaction task is filed in the same commit.
- [x] `python3 scripts/check-docs.py` green; `changelog.d/` fragment.
