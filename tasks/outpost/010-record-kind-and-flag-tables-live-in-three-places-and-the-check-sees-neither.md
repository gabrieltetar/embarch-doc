# 010 — The outpost record-kind table lives in three languages and the header-flag table in three places, and the one cross-check that exists cannot see either

**State:** done — leg 035, 2026-09-07, branch `agent/outpost/010-one-record-vocabulary`.
**Source:** suite review pass 2026-09-06, dimension 2 (DRY across modules). Code-confirmed.
**Scope:** outpost
**Hardware:** none. `tests/run-all.sh` builds against an external `ZEPHYR_BASE`; verified 2026-09-06 that all four legs pass over a bare `git archive` copy with only `WEST` and `ZEPHYR_BASE` set (`tasks/README.md`).
**Owner:** no

**Scope boundary, and it is the reason this task looks bigger than it is (leg 035, at dispatch).**
Three of the four copies named below are in `embarch-outpost` — `src/outpost_priv.h`,
`scripts/decode_outpost.py`, `tests/native_sim_stream/assert_stream.py` — and the fourth,
`embarch-study-designer/src/outpost.rs`, is **not yours to write.** A worker owns exactly one
sub-project (`../../embarch-fleet/protocol.md` §3, §5). So:

- You **may read** `embarch-study-designer/src/outpost.rs`, and a new check that lives in
  `embarch-outpost/tests/` may read it as an input. Reading another repo is not writing it.
- You **may not edit** it, add a test to it, or change its `RecordKind`/`HeaderFlags` tables.
- Every `Done when` below is reachable without touching it: item 1 is satisfied by a check that
  compares all three tables and fails when one drifts, and items 2 and 3 are both
  `embarch-outpost` files.
- If you conclude the *right* fix requires a change in `embarch-study-designer` — deriving its
  tables from a generated file, say — that is a finding, not a change to make. Drop it in
  `/home/gabriel/Github/embarch/embarch-doc/inbox/` (that absolute path, in the main checkout,
  **not** in your worktree) and implement the version that stays inside your repo.

**Doc-size reserve in `embarch-outpost` (leg 035, measured at dispatch).** Three files are in
reserve, every one already filed: `open.md` **4,891 / 5,120 B (95.5%, 229 B left)** and
`decisions/module.md` **7,730 / 8,192 B (94.4%, 462 B left)**, both against `tasks/outpost/012`
(`open`); and `decisions/tracing.md` **7,408 / 8,192 B (90.4%, 784 B left)** against
`tasks/outpost/008` (`open`). **`open.md` has 229 bytes — treat it as full.** A new numbered
decision for this work is most naturally `decisions/wire.md` or a peer with headroom, not
`module.md`. If your work spends the reserve — pushes a file into it, or leaves one there that
nothing has filed — file `tasks/outpost/<NNN>-compact-outpost.md` in the same commit
(`tasks/README.md` has the shape; the path is `tasks/outpost/`, never `tasks/doc/`).

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

- [x] Appending a record kind or a header flag on one side fails a check on the others, or is
      derived from one definition. Done via a check: `tests/vocab_check.py`, decisions/wire.md
      decision 23. Verified by actually appending a kind to `outpost_priv.h` and watching both
      `decode_outpost.py` and (via a temporary sibling symlink) `outpost.rs` report it missing,
      then reverting.
- [x] `cross_decoder.py` (or a peer) compares the C producer's kind and flag tables, not only the
      two decoders' rendered output. Peer: `tests/vocab_check.py`, parses `outpost_priv.h`
      directly and diffs it against `decode_outpost.py` and, read-only, `outpost.rs`.
- [x] `assert_stream.py`'s `FLAG_TRACE_SELF` is no longer a fourth hand-written copy. It now
      imports `decode_outpost.FLAG_TRACE_SELF`.
- [x] `tests/run-all.sh` green with `WEST` and `ZEPHYR_BASE` set. See report below for numbers.
- [x] Gate green; `changelog.d/outpost-*` fragment. `changelog.d/outpost-vocab-check-fixed.fixed.md`.

## Report (leg 035)

**Fork taken: check, not generate — decisions/wire.md decision 23.** `outpost_priv.h` is the
definition (the producer). A generator run at Zephyr module build time could turn it into
`decode_outpost.py`'s tables mechanically, but cannot write `embarch-study-designer/src/outpost.rs`
(out of scope — a different repo), so it would still need the same read-and-diff logic for that
copy that a checker needs anyway. Chose one mechanism (a check) over two (a generator plus a
check for the one copy it cannot reach). Rejected: deriving `decode_outpost.py`'s tables from
`outpost_priv.h` by parsing it at import time — closes only the cheapest of the three gaps and
leaves the one that actually drifted (the cross-repo one) exactly where a check would leave it.

**Written (this repo only):**
- `tests/vocab_check.py` (new) — parses `enum outpost_kind` / `enum outpost_header_flag` out of
  `src/outpost_priv.h` by regex; diffs against `scripts/decode_outpost.py`'s `KIND_NAMES` /
  `FLAG_NAMES` (imported, not re-parsed); and, read-only and only if
  `embarch-study-designer/src/outpost.rs` is checked out beside this repo, against its
  `RecordKind` and `HeaderFlags` (regex-parsed as text — never written). Skips loudly, exit 0,
  when the sibling is absent, matching `cross_decoder.py`'s convention (decision 22).
- `scripts/decode_outpost.py` — added `FLAG_NAMES`/bit constants (kinds already had `KIND_NAMES`).
- `tests/native_sim_stream/assert_stream.py` — deleted its hand-written `FLAG_TRACE_SELF = 1 << 7`
  in favour of importing `decode_outpost.FLAG_TRACE_SELF`.
- `tests/run-all.sh`, `README.md` — wired `vocab_check.py` in as a third host-only leg, above the
  `WEST` guard, alongside `decoder_unit.py`.

**Read-only (never written):** `embarch-study-designer/src/outpost.rs` — read by
`vocab_check.py` at test time only, as the task's scope boundary requires. No edit was made or
considered necessary there; every `Done when` item was reachable without it.

**Gate:**
- `tests/run-all.sh`, with `WEST=/home/gabriel/Github/embarch/.west-venv/bin/west` and
  `ZEPHYR_BASE` pointing at a fresh `west init -m zephyr --mr main` + `west update` checkout (no
  suite-owned `ZEPHYR_BASE` existed on this machine outside client workspaces, which this worker
  will not touch or reference — built a clean one instead): all five legs ran; decoder unit 20/20,
  vocab check PASS (11 kinds, 8 flag bits; sibling not present in the worktree so that half
  reported SKIP, confirmed separately by temporarily symlinking the real sibling in — PASS with
  ", and outpost.rs"), cross-decoder SKIPPED (sibling fixtures not present in the worktree — same
  documented convention, decision 22, unrelated to this change), unit ztest ran (native_sim build
  succeeded), module-off ran, e2e stream PASS (37 frames, 725 records). Full transcript available
  on request.
- Doc worktree: `python3 scripts/check-docs.py` — **all 10 checks green** (bare, full run).
- `scripts/check-client-names.py --repo <code worktree>` — clean against all 7 denylist entries.
- `scripts/check-ownership.py --scope outpost` (doc worktree) and `--code-repo --repo .` (code
  worktree) — both OK.

**Unsure about / worth a second look:** `vocab_check.py`'s Rust parser is a hand-rolled regex over
`outpost.rs`'s text (enum body + `as_str()` match arms + `HeaderFlags` impl block), not a real Rust
parser — it is deliberately narrow to this one file's two specific shapes and will need updating,
loudly (it fails with 0 kinds/flags parsed rather than silently passing) if that file's structure
changes shape rather than content. Considered acceptable since `outpost_priv.h`'s own C parsing is
equally narrow, and the alternative (a real Rust AST parser dependency) seemed disproportionate to
a repo with no other Rust tooling.

**Adjacent, and worth doing in the same sitting:** the
`outpost-the-cross-repo-check-sits-below-a-guard-it-does-not-need` drop in this batch makes this
check actually run.
