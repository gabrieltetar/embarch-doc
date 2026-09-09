# embarch-outpost decisions: One wire vocabulary, one definition

**Status:** active, 2026-09-07.

The record-kind and header-flag names, and the check that keeps their four copies honest.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 23 — `src/outpost_priv.h` is the definition; the other three copies are diffed against it by a dedicated check, not generated from it

The wire's kind and flag names exist in four places: `src/outpost_priv.h` (the C
producer), `embarch-study-designer/src/outpost.rs` (`RecordKind`, `HeaderFlags`
— a sibling repo this one may read but not write), `scripts/decode_outpost.py`
(`KIND_NAMES`, and now `FLAG_NAMES`), and, until this decision, a fourth
hand-written `FLAG_TRACE_SELF = 1 << 7` in
`tests/native_sim_stream/assert_stream.py`. One of the four had already drifted
for a day, silently, before anything read it (`outpost.rs:225-227`), and the
only cross-check that existed — `tests/cross_decoder.py` — diffs two decoders'
*rendered CSV*, which cannot see a flag neither decoder renders and never reads
the producer at all.

**The producer is the definition, not a vote among four.** The firmware that
ships is built from `outpost_priv.h`; nothing on the wire can exist that this
file does not declare, and nothing this file declares can be absent from a
faithful mirror. The other three are restatements, graded by how far they can
drift before something notices.

**Check, not generate — a real fork, decided against generation for a boundary
reason as much as a cost one.** A generator run at Zephyr module build time
could turn `outpost_priv.h` into `scripts/decode_outpost.py`'s tables
mechanically and close that gap for good. It cannot do the same for
`embarch-study-designer/src/outpost.rs`: that file is in a repo this one may
not write (`../../embarch-fleet/protocol.md` §3, §5), so even a perfect
generator only closes three of the four copies and the fourth still needs
exactly the read-and-diff logic a checker would have needed anyway. Given that
the cross-repo half is irreducibly a check, making the in-repo half a check
too is one mechanism instead of two, and it is the one that already existed in
shape (`cross_decoder.py`'s sibling-read-and-skip convention, decisions/testing.md
decision 22) rather than a new build-time code-generation step in a Zephyr
module — where a generator bug fails as a build failure in someone else's
firmware image, not as a test failure in this repo's own suite.

*Rejected: derive `decode_outpost.py`'s tables from `outpost_priv.h` by
parsing it at import time.* Would close the in-repo gap for good rather than
just checking it, but buys that only for the copy that was already the
cheapest to check (same file, same repo, same language of build tooling) while
leaving the cross-repo copy — the one that has actually drifted — exactly
where a check would leave it. Revisit if a fifth in-repo copy ever appears;
one is not enough restatement to be worth a parser two ways instead of one.

**`tests/vocab_check.py`** parses `enum outpost_kind` and `enum
outpost_header_flag` out of `outpost_priv.h` by regex, and diffs the resulting
`{value: name}` tables against `scripts/decode_outpost.py`'s `KIND_NAMES` and
`FLAG_NAMES` (imported directly, not re-parsed, so this check cannot itself
drift from what the decoder uses) and, read-only and only if the sibling repo
is checked out beside this one, against `outpost.rs`'s `RecordKind` (enum
discriminants joined to `as_str()`'s match arms) and `HeaderFlags`. Missing
sibling is a loud `SKIP:`, never a failure — the same convention decision 22
established for `cross_decoder.py`, for the same reason: a solo clone of this
repo has no obligation to have `embarch-study-designer` beside it. It needs
neither `west` nor `ZEPHYR_BASE` and runs in `tests/run-all.sh` above the
`WEST` guard, alongside `decoder_unit.py`.

**`assert_stream.py`'s fourth copy of `FLAG_TRACE_SELF` is deleted, not
checked.** It now imports `decode_outpost.FLAG_TRACE_SELF`; there is nothing
left there to drift independently, so `vocab_check.py` does not need to name
it as a fifth target.

Verified [2026-09-07]: `vocab_check.py` passes standalone (`PASS: 11 kinds and
8 flag bits agree between outpost_priv.h, decode_outpost.py`, plus `, and
outpost.rs` when the sibling is present) and as part of a full green
`tests/run-all.sh` with `WEST` and `ZEPHYR_BASE` set. A kind appended to
`outpost_priv.h` alone was confirmed to fail the check (both the
`decode_outpost.py` and `outpost.rs` legs report the new value as missing)
before being reverted.
