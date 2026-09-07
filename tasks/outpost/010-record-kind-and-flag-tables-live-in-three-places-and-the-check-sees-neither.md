# 010 — The outpost record-kind table lives in three languages and the header-flag table in three places, and the one cross-check that exists cannot see either

**State:** claimed — leg 035, 2026-09-07, **worker finished and pushed; the leg died before folding — see the recovery note at the bottom of this file**, branch `agent/outpost/010-one-record-vocabulary`.
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

## Recovery note — owner's session, 2026-09-07 12:1x

**The worker finished, pushed both halves, and the supervisor never woke to land
it.** Leg 035 dispatched this unit at 11:30, said "two workers in flight,
holding", and stopped. This worker reported complete at 11:36, both branches
pushed:

- code `agent/outpost/010-one-record-vocabulary` (0517e59) on `embarch-outpost`'s origin
- doc `agent/outpost/010-one-record-vocabulary-doc` (e80da7f) on `embarch-doc`'s origin

The completion notification was delivered to the **listener session's** main
loop instead of to the supervisor subagent that spawned this worker. The
listener read it, correctly concluded "worker report to the running supervisor,
not a leg completion — no listener action", and did nothing. The supervisor was
never resumed, so nothing folded, `.fleet/tick` was last touched at 11:30:42,
and the deadman pulled the pump latch at 12:09.

**So phase-0 recovery must RE-LAND this, not block it.**
[tasks/README.md](../README.md)'s rule — a worktree with commits ⇒ `blocked`
naming the branch — is written for a worker that died mid-edit. This one did
not: it ran to completion and its own report is in the leg's transcript. Leg
033 took exactly this route this morning for `api/040` and `ui/003`, and its
log entries say why: re-dispatching throws away finished green work to buy a
self-report you already have a better substitute for.

**Gate on the merge result, not the branch**, and note the branch predates four
owner commits (through `54c6882`), so the doc half needs a rebase before it will
fast-forward. **`check-doc-size.py` changed while this worker ran**: reserve is
now `max(1.2 KB, 10%)`, so re-check whether this unit's own additions put a
file into reserve that its author had no reason to file.
