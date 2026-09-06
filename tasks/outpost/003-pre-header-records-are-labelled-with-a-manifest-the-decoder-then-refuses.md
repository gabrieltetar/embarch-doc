# Stop labelling pre-header records with a manifest the decoder then refuses

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-outpost/spec.md:60`'s "a mismatched manifest refuses to render the names" leaks in the case the repeating header exists for
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

`scripts/decode_outpost.py:302-321` — the build-ID check runs only when the *first* header frame is
reached, while `:319-322` has already rendered every `records` frame that preceded it through the
loaded manifest. `tests/native_sim_stream/assert_stream.py:136-138` asserts "a refused manifest still
labelled records", but only over a capture that begins at process start — so the mid-stream case is
unguarded.

A stream whose header disagrees with `--manifest` should produce **zero named rows**, including rows
decoded before the first header frame: `manifest_refused: true` and named output become mutually
exclusive. The natural fix is a two-pass decode — the whole stream is already read into memory at
`:292` — which also gives pre-header rows a correct `us` column once `cycles_per_sec` is known.

Pure Python; `tests/cross_decoder.py` runs without west.

## Why now

`spec.md:60` says "A mismatched manifest refuses to render the names", and `interfaces/wire.md:37`
says the header repeats precisely so a host attaching mid-stream can decode. That is exactly the
case where this leaks.

## Done when

- [ ] Decoding a stream whose first bytes are a records frame, against a mismatched manifest, yields
      no non-empty `name` in any row.
- [ ] `us` is populated for pre-header rows once a header is seen anywhere in the stream, or is
      empty for the whole trace consistently — say which, in `decisions.md`.
- [ ] A host-side test feeds a synthesized records-frame-then-header stream and asserts both.
- [ ] `tests/native_sim_stream/assert_stream.py` still passes unchanged.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
