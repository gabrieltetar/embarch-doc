# 029 — Three citation sweeps left bare `§N` pointers at a document that no longer exists

**State:** done — leg 107, unit 4, 2026-09-13. All `Done when` boxes ticked below; see "What was
done" for the per-hit breakdown.
**Doc-size reserve for `dev-bench`, and read this before you pick a file for the new decision:**
`embarch-dev-bench/open.md` 4782/5120 B (**338 B left**, filed as blocked `tasks/dev-bench/012`),
`embarch-dev-bench/spec.md` 9460/10240 B (780 B left, same blocked task), and
`embarch-dev-bench/decisions/link.md` 11241/12288 B (1047 B left, filed as blocked
`tasks/dev-bench/014`). `decisions/link.md` is about the serial link, and the decision this task
owes is about citation form — so **it almost certainly belongs in a different topic file**; check
`embarch-dev-bench/decisions.md`'s index and pick the right one rather than the nearest one.
`embarch-api` filed a decision into the wrong topic file on 2026-09-05 for exactly this reason and
nothing failed. If the right file genuinely is one of the three above and your edit will not fit,
compact that file in-unit per `DOC-COMPACTION.md` §2, carrying the parked task's `Must not delete:`
list and closing only that file's item. If you push any `dev-bench` doc into reserve, file
`tasks/dev-bench/<NNN>-compact-dev-bench.md` in the same commit.
**Source:** `dev-bench/022`'s reviewer, 2026-09-13, asked the question directly and answered it
plainly. Counts below are from the merge result (`embarch-dev-bench` `15c8796`).
**Scope:** dev-bench
**Hardware:** none — comment text in C files. No behaviour, no wire, no board.
**Owner:** no

## What

`dev-bench/019`, `020` and `022` repointed ~200 citations of the deleted
`embarch-study-designer/design.md §3` and `embarch-dev-bench/design.md` filenames. Where a citation
carried a decision **number**, it became `` `<repo>` decision N `` and resolves. Where it carried
only a **section** number — `design.md §4.8`, `§4.3a`, `§4.5`, `§4`, `§1` — the dead filename was
stripped and the bare section number left behind.

**Start by re-deriving the count, because the two that exist disagree.**
`grep -cE '§[0-9]' app/src/main.c app/src/ble_bridge.h app/src/serial_protocol.c
app/tests/serial_protocol/src/main.c` → **5, 6, 6, 5 = 22**, which counts *lines*; `022`'s reviewer
counted **21** post-merge, which is probably *occurrences* — one line carrying two, or one `§`
that is not a citation at all. Neither number has been checked against the other, and this task
family exists because of numbers nobody checked, so do not inherit either. That is the four files
`022` touched; `019` and `020` left more in `eap.h`, `eap_interp.h`, `eap_interp.c`,
`serial_protocol.h` and `ble_bridge_real.c`, and no count exists for those at all.

`ble_bridge.h:88` is the shape: *"the crate's own docs state this explicitly for `Uuid` but not for
`BleAddress` (§4)"* — §4 of what.

## Why now, and why this is not just tidying

**The reviewer's read, which is the reason this is filed rather than accepted:** a bare `§N` is
*"a different dangling reference, not an improvement — it drops the repo name too, so a reader can
no longer even tell which repo's history to search; less traceable than the dead-but-named path it
replaced."*

That is the part worth acting on. The old form was wrong but self-describing: a reader saw
`embarch-study-designer/design.md §4.8`, found no such file, and could search that repo's history
for what §4.8 became. The new form names neither the document nor the repo, so the same reader has
nothing to search. Three units have now applied this treatment on each other's precedent, which is
how a convention gets established by accident.

## What was done

All 46 in-scope hits, by file and how each resolved (decision number / named-but-live-doc /
deleted). "dedup" means the line already carried a resolving decision number and only the
redundant trailing `§N` was dropped.

- **main.c** (4): `§4.5` (Outcome/StepResult shape) deleted, repo already named in prose;
  `§4` ×2 (open questions about the reset cause and the untested fatal-path) repointed to
  `open.md`, which is where those two questions actually live now; `§3 decision 7` (dangling
  prefix, same bug class as `022`'s decision-18 fix) → bare `decision 7` (dev-bench's own,
  `decisions/link.md`).
- **ble_bridge.h** (6): `§4.9` dedup (decisions 58-62); `§4` (Uuid/BleAddress byte-order asymmetry)
  deleted, no owning decision found and crate already named; `§4.3a` → `embarch-study-designer`
  decisions 31/32 (GattCharacteristicInfo/GattServiceInfo, matches decision 31's "raw, not
  symbolic" stance verbatim); `§1` (`Step.timeout_ms`) named-not-numbered — no decision owns a bare
  Study/Step field, so named `` `embarch-study-designer`'s `Step.timeout_ms` `` instead of guessing
  one; `§4` (Sample.value f32 mapping, explicitly "still open") deleted — an unresolved question
  isn't a decision or a stable doc location, and neither `embarch-study-designer`'s nor this repo's
  `open.md` tracks it; `§4.3b` → decision 36 (GattTranscriptEntry, matches decision 36's streamed
  transcript content).
- **serial_protocol.c** (6): `§3 decision 39` dangling-prefix → decision 39 (×2); `§4.9` dedup
  (×2, decisions 58-62 / decision 58); `§4.8` deleted, repo+file already named; `§4.3b` → decision
  36.
- **app/tests/serial_protocol/src/main.c** (5): `§3 decision 39` → decision 39; `§4.9` dedup;
  `§3 decision 60` → decision 60 (×2); `§3 decision 18` → decision 18 (same content as `022`'s
  already-fixed sibling: "raw array subscript... name the specific failure", `embarch-study-designer`
  decision 18's real subject per `decisions/seals.md`).
- **eap.h** (3): `§4.9` dedup (×2); `§4.9` (worked-protocol arm count) deleted — no numbered
  decision states "both worked protocols use one arm per state" and the crate is already named
  two lines up.
- **eap_interp.h** (2): `§4.9` dedup; `§3 decisions 31/32` — a genuine **miscitation**, not a
  dedup: 31/32 are GATT-discovery decisions, unrelated to "wire types in the crate, executor here."
  Corrected by content to decisions 59/60 (the primitive split and the RunProtocol executor
  decision, which is what the sentence actually describes).
- **eap_interp.c** (1): `§4.9` dedup.
- **serial_protocol.h** (12 across 11 lines): `§3 decision 39, §4.8` → decision 39 (both trailing
  markers collapsed into the one resolving citation); `§4.9` dedup (×2); `§4.9` (BDS worked-example
  byte count) deleted, same reasoning as the `eap.h` case; `§4.3b` → decision 36 (×2); `§4.8`
  deleted (×2, repo+file already named); `§3 decision 18` → decision 18; `§4.3` (display-order
  convention) deleted, repo already named in the same sentence; `§4.3a` → decisions 31/32.
- **ble_bridge_real.c** (8, one deliberately untouched): `§4.3` deleted, decisions 31/32 already
  named two lines up; `§4.3a` (×2) → decisions 31/32 and decision 32 specifically (the second one
  is the flattening-index convention, which decision 32's text states almost verbatim); `§3
  decision 53` → decision 53; `§3 decision 60` (×2) → decision 60; `§3 decision 18` → decision 18.
  **Left alone:** `§1.3` at line 380 — Bluetooth Core Spec Vol 4 Part E, an external standard with
  its own real numbered sections, not this suite's `design.md`. Same `§N` shape, unrelated
  reference; resolving it as if it were ours would have been the exact mistake decision 47 exists
  to prevent.

Two miscitations found and corrected by rereading the surrounding paragraph rather than trusting
the number already present (per `022`'s own precedent, which found two of these): `eap_interp.h`'s
`§3 decisions 31/32` (should be 59/60) and every `§3 decision 18` (already correctly identified as
`embarch-study-designer`'s in `022`'s prior fix; carried forward consistently here).

## Done when

- [x] A decision is taken and written down about what a section-only citation into a deleted
      document should become. The candidates, and none is obviously right: **(a)** resolve each to
      the decision number that absorbed that section, where one exists; **(b)** name the repo and
      say the section is historical — `` `embarch-study-designer`, historically design.md §4.8 ``
      — which keeps traceability without pretending the file exists; **(c)** delete the pointer
      where the sentence stands without it. Expect the answer to differ per hit.
      **Done.** All three applied, per hit, in `embarch-dev-bench` decision 47
      (`decisions/conventions.md`). See the "What was done" section below for the full per-hit
      breakdown.
- [x] Every bare `§N` in this repo's C sources either resolves, names its repo, or is gone.
      Confirmed by a repo-wide `grep -rn '§[0-9]' app/ --include='*.c' --include='*.h'` after the
      edits: zero bare hits remain in the 9 files this task and `019`/`020` touched. Two classes of
      `§N` deliberately left untouched, both out of this task's scope: (1) `ble_bridge_real.c:380`'s
      `§1.3` cites the real Bluetooth Core Specification, not our dead `design.md` — a different
      reference wearing the same shape; (2) several files `019`/`020`/`022` never touched at all
      (`study_ffi.h`, `ble_bridge_stub.c`, `scan_seen_names.h`, `scan_seen_mfg.h`, `dev_bench_log.c`,
      `dev_bench_log.h`, `study_ffi_real.c`, `study_ffi_stub.c`, `app/tests/dev_bench_log/src/main.c`)
      still carry the dead filename attached (`embarch-dev-bench/design.md §3 decision N`) rather
      than a bare section number — self-describing, and `DOC-CONVENTIONS.md`'s "Legacy `§3 decision
      39` still parses, unmaintained" line explicitly tolerates that form. Left alone as out of
      scope; not a citation this task's problem statement describes.
- [x] The count is re-derived, including `019`'s and `020`'s files, not taken from this task.
      Re-derived from scratch: the task's own `grep -c` line (5,6,6,5=22) does not match a fresh run
      of the same command, which gives **4,6,6,5=21** — matching the reviewer's count, not the task
      header's. The task's own arithmetic was wrong (`main.c` has 4 matching lines, not 5). Adding
      `019`/`020`'s five untouched files (`eap.h`=3, `eap_interp.h`=2, `eap_interp.c`=1,
      `serial_protocol.h`=12, `ble_bridge_real.c`=8) brings the true total to **47** raw `§[0-9]`
      occurrences across the nine files, of which 46 were this task's to fix and one
      (`ble_bridge_real.c:380`) was the Bluetooth-spec false positive above.
- [x] Whatever is decided is recorded as a numbered `embarch-dev-bench` decision, since two earlier
      units already followed the unwritten version of it and a third would make it folklore.
      `embarch-dev-bench` decision 47, `decisions/conventions.md` (new topic file — none of the
      existing nine missions fit a documentation-citation-form convention; forcing it into the
      nearest one would have been exactly the `embarch-api` 2026-09-05 mistake this task's header
      warns against). Indexed in `decisions.md`.
- [x] Host-side checks green; say what could and could not be run (no `west`, no Zephyr SDK in a
      worker's worktree — standing debt, not introduced here).
      This repo has no `Cargo.toml` anywhere (pure C/Zephyr firmware) — `cargo build`/`test`/
      `clippy` do not apply; there is nothing for them to select. `west` is not on `PATH` in this
      worktree and no Zephyr SDK is installed (standing debt per `CLAUDE.md`'s own build note, not
      introduced by this unit), so an actual firmware or native_sim test-suite build could not run.
      What was checked instead: every touched comment's `/* ... */` pairing balances (verified with
      a paired-count scan per file, all equal), and a full repo-wide `§[0-9]` re-scan confirms no
      unresolved bare citation remains. `scripts/check-docs.py` (11/11), `check-client-names.py`
      and `check-ownership.py` (both repos) are green — see report.
- [x] `changelog.d/` fragment.
      `changelog.d/dev-bench-bare-section-citations-resolved.decided.md`.

## Do not

Do not resurrect `design.md`, and do not invent a section number for a document nobody can read.
Where the original section cannot be identified, option (c) is better than a guess — this whole
task family exists because a citation that looks resolvable and is not costs more than no citation
at all.
