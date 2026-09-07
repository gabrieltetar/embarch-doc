# 010 — The outpost record-kind table lives in three languages and the header-flag table in three places, and the one cross-check that exists cannot see either

**State:** open
**Source:** suite review pass 2026-09-06, dimension 2 (DRY across modules). Code-confirmed.
**Scope:** outpost
**Hardware:** none. `tests/run-all.sh` builds against an external `ZEPHYR_BASE`; verified 2026-09-06 that all four legs pass over a bare `git archive` copy with only `WEST` and `ZEPHYR_BASE` set (`tasks/README.md`).
**Owner:** no

## What

One wire vocabulary, three independent copies:

- **Producer** — `src/outpost_priv.h:110-152`: `OUTPOST_KIND_THREAD_SWITCH_IN = 0 …
  OUTPOST_KIND_GPIO_CALLBACK_DONE = 10`; `:164-184`: `OUTPOST_FLAG_TRACE_THREADS = BIT(0) …
  OUTPOST_FLAG_TRACE_SELF = BIT(7)`.
- **Rust decoder** — `embarch-study-designer/src/outpost.rs:102-143` (`RecordKind`, `from_byte`,
  `as_str` — three restatements of the same 11 rows) and `:217-241` (`HeaderFlags`, all 8 bits).
- **Python decoder** — `scripts/decode_outpost.py:30-50`: a `KIND_NAMES` dict plus
  `KIND_THREAD = (0, 1, 5, 6)`, `KIND_IRQ = (2, 3)`, `KIND_MARKER = 7`, `KIND_GPIO_DISPATCH = 9`,
  `KIND_GPIO_CALLBACK_DONE = 10`. It decodes **no flags at all.**
- A fourth spelling of one flag: `tests/native_sim_stream/assert_stream.py:84` —
  `FLAG_TRACE_SELF = 1 << 7`, hand-written, and the only bit any test asserts.

**It has already drifted once, and the code records it.**
`embarch-study-designer/src/outpost.rs:226-228`: *"Added 2026-08-27, and it had been on the wire
since layout 3's GPIO record kinds shipped the day before **without ever being mirrored here** —
nothing read it, so nothing noticed."*

**The check that exists was scoped to the wrong pair.** `tests/cross_decoder.py` diffs the *two
decoders'* rendered CSV over one committed fixture. It never reads `outpost_priv.h` — so the
producer's table, which is the definition, is compared against nothing — and since the Python side
decodes no flags, a C-versus-Rust flag divergence is invisible to it by construction.

The good shape exists next door, for contrast: `embarch-ui/src/trace.rs:681-685` reverse-maps
names out of `RecordKind` rather than restating them, and `:1298-1303` refuses a CSV whose header
is not `outpost::csv_header()`.

Candidate direction: make one of the three the definition and derive or check the others against
it, and extend `cross_decoder.py`'s reach (or add a peer to it) so the C producer's kind and flag
tables are compared — not just the two decoders' output on a fixture that happens to contain
neither a new kind nor a new flag.

## Why now

`embarch-outpost/open.md` makes appending a record kind the cheap operation — *"no layout bump;
appending a kind never costs one"* — so this is the edit most likely to happen and the one with
three places to remember. The flag table has already gone a full day out of step with the code
noting it, and the note is now the mitigation. `embarch-study-designer/src/outpost.rs:14-19`
names the firmware encoder as a mirror, unpinned, rather than as out of scope.

## Done when

- [ ] Appending a record kind or a header flag on one side fails a check on the others, or is
      derived from one definition.
- [ ] `cross_decoder.py` (or a peer) compares the C producer's kind and flag tables, not only the
      two decoders' rendered output.
- [ ] `assert_stream.py`'s `FLAG_TRACE_SELF` is no longer a fourth hand-written copy.
- [ ] `tests/run-all.sh` green with `WEST` and `ZEPHYR_BASE` set.
- [ ] Gate green; `changelog.d/outpost-*` fragment.

**Adjacent, and worth doing in the same sitting:** the
`outpost-the-cross-repo-check-sits-below-a-guard-it-does-not-need` drop in this batch makes this
check actually run.
