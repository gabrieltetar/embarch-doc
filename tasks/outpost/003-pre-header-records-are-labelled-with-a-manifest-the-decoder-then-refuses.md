# Stop labelling pre-header records with a manifest the decoder then refuses

**State:** done — leg 060, 2026-09-09, `agent/outpost/003-two-pass-decode`
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

- [x] Decoding a stream whose first bytes are a records frame, against a mismatched manifest, yields
      no non-empty `name` in any row.
- [x] `us` is populated for pre-header rows once a header is seen anywhere in the stream, or is
      empty for the whole trace consistently — say which, in `decisions.md`. **Answer: populated**,
      recorded as prose in `spec.md` (not a new numbered decision — burndown; see report). Two-pass
      decode gives pre-header rows the header's `cycles_per_sec` before any row renders.
- [x] A host-side test feeds a synthesized records-frame-then-header stream and asserts both.
      `TestPreHeaderRowsUnderARefusedManifest` in `tests/decoder_unit.py` — confirmed to actually run
      (verified by name in `-v` output), not skip. Also added a matching-manifest control case.
- [ ] `tests/native_sim_stream/assert_stream.py` still passes unchanged. **Not run**: needs
      `west`/`ZEPHYR_BASE`, unbuildable in this worktree per the task's own note. `render()` itself
      (which that test exercises) is untouched by this fix — only `main()`'s dispatch loop changed —
      so the risk to that test is low, but this is not verified execution.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `tests/decoder_unit.py` (31/31 pass, incl.
      the 2 new), `tests/vocab_check.py` (PASS, partial-skip is pre-existing/expected — sibling repo
      not checked out), `tests/cross_decoder.py` (SKIP, silently, as this fleet's standing debt says
      it always does here — sibling fixtures absent). `scripts/check-docs.py`: 10/10 green.
      `check-ownership.py --scope outpost` and `--code-repo`: both OK. `check-client-names.py`: clean.
      No cargo crate in this repo.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. `spec.md`'s manifest-refusal bullet extended
      (within the 725 B headroom, not exceeded — 449 B left after). No `decisions.md`/`open.md` edit:
      no new numbered decision per the burndown note, and `decisions/manifest.md` decision 9 is
      **pinned** (`check-doc-size.py` rejects any growth on a pinned decision) so prose was kept out
      of it after a first attempt tripped that check. Nothing suite-level went false; no `status.d/`
      fragment.

## Supervisor's dispatch note, leg 060 (burndown)

**No new numbered decision** ([burndown.md](../../../embarch-fleet/burndown.md)). The "Done when"
bullet asking you to *"say which, in `decisions.md`"* about the `us` column is the one place this
bites. **Do the two-pass decode**, populate `us` for pre-header rows once a header is seen anywhere
in the stream (the task itself calls that the natural fix, and the whole stream is already read into
memory at `:292`), and record that choice as **prose in `spec.md` / `open.md`**, not as a new
numbered entry. If you judge it genuinely deserves a number, say so in your report and note it in
`open.md` as owed.

**Beware `tests/cross_decoder.py`.** A standing debt of this fleet is that it **skips silently in
every fleet worktree** (`tasks/outpost/005`), so do not read a green run as coverage: check that
your new test actually executed, by name, and say in your report whether it ran or skipped. Your new
host-side test must be one that runs without west.

**Doc reserve for `outpost`:** `embarch-outpost/spec.md` 9515/10240 B (**725 bytes left**) and
`decisions/tracing.md` 7408/8192 B (**784 bytes left**). Both already have **open** (not blocked)
compaction tasks filed — `tasks/outpost/014-compact-outpost.md` and `tasks/outpost/008`. An open
compaction task is somebody else's future unit, **so do not compact them**; keep your edits inside
that headroom, and if you spend it further, file `tasks/outpost/<next free NNN>-compact-outpost.md`
in the same commit per `tasks/README.md`.

**No hardware.** No board, no study, no live Core — this is pure host-side Python and its tests.
