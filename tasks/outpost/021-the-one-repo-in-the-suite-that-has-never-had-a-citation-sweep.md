# 021 — `embarch-outpost` is the one repo in the suite that has never had a citation sweep

**State:** open
**Source:** leg 131 refill, 2026-09-17. Every other code-bearing repo in this suite has been
swept for wrong decision citations — `embarch-study-designer` across seventeen files
(`044`–`059`), `embarch-dev-bench` (`031`–`033`), `embarch-core` (`068`, `069`), `embarch-api`
(`091`, `106`), `embarch-umbrella` (`074`), `embarch-topology` (`052`), `embarch-ui` (`063`).
**`tasks/outpost/` contains no citation task of any kind**, and `grep -rl citation
tasks/outpost/` returns nothing. This is a gap in coverage, not a re-census.
**Scope:** outpost
**Hardware:** none — source comments and scripts read as text. **Nothing is built, no board, no
probe, no flash, no `west`, no Zephyr SDK.** This is C and Python source read as text; it is
**not** one of this repo's toolchain-gated tasks. `embarch-outpost` has no `Cargo.toml`, so the
cargo half of the gate selects nothing — that is expected and is not a red gate.
**Owner:** no

**Doc-size reserve for `outpost`: none.** `scripts/check-doc-size.py --pressure` at dispatch lists
twelve files in reserve and **not one of them is under `embarch-outpost/`**. You have headroom in
every file of this sub-project. Re-check fresh rather than trusting this line.

## What

`grep -rnIE '[Dd]ecisions? [0-9]+'` over `embarch-outpost`, excluding `.git` and `build/`, returns
**49** lines across 20 files. Taken at `b12ced1`; `main` moves, so **re-run it yourself and report
the count you actually got.** Concentration:

```
7  src/outpost_priv.h                      3  scripts/gen_outpost_manifest.py
6  src/outpost_hooks.c                     2  tests/vocab_check.py
5  tests/run-all.sh                        2  scripts/decode_outpost.py
5  src/outpost.c                           2  include/embarch/outpost.h
3  tests/native_sim_stream/assert_stream.py 2  README.md, Kconfig, CMakeLists.txt
1 each: tests/unit/src/main.c, tests/native_sim_stream/app.overlay, tests/decoder_unit.py,
        src/outpost_time.h, src/outpost_ring.c, src/outpost_markers.c,
        cmake/outpost_build_id.h.in, .github/workflows/host-tests.yml
```

**Take the top three files** — `src/outpost_priv.h`, `src/outpost_hooks.c`, `src/outpost.c` — 18
lines between them. If they go quickly, take `tests/run-all.sh` too. **Do not try to sweep all
twenty files**; file the remainder as `tasks/outpost/<next>` naming exactly which files are left,
the way `tasks/study-designer/060` does.

**This repo's decision surface is `embarch-doc/embarch-outpost/decisions.md` plus twelve topic
files under `embarch-outpost/decisions/`** (`capture`, `clocks`, `hardware`, `layout`, `manifest`,
`markers`, `module`, `naming`, `testing`, `tracing`, `transport`, `wire`). Establish the real
highest decision number yourself before you call any citation unresolvable — a number above the
top one is a different defect from a number that resolves to the wrong decision, and only the
second is common.

## What to check, per citation

Read the cited decision's **body**, then the sentence around the citation, in that order. A number
that resolves is not evidence the claim holds. Answer three separate questions and count them
separately — the chain has found defects in all three categories, so do not collapse them:

1. **Does the number resolve?** In the repo the sentence names — this repo's own decisions when
   unlabelled, the named repo's when labelled.
2. **Is it the right repo?** A bare `decision N` is same-repo by convention; another repo's must
   read `<repo> decision N`. Check every bare *and* every labelled citation against **this
   module's own** decisions first regardless. This repo cites `embarch-core` and
   `embarch-study-designer` heavily (the manifest, the decoder, the wire), so a dropped prefix here
   is likelier than average.
3. **Is the sentence true?** The one a resolution check cannot answer, and the one that has
   produced this chain's most expensive defects. Read the cited decision's own text and check it
   says what the comment says it says.

**Four shapes the chain has already paid for, all live here:**

- **Right topic, wrong neighbour.** `study-designer/059` and `ui/063` both found a citation that
  was on-topic, correctly labelled cross-repo, and still named the wrong decision — the one three
  paragraphs later in the same file said the thing verbatim. When a cited decision's *topic* is
  right but the *specific claim* is not close to verbatim in its text, read its neighbours in the
  same decisions file before concluding the citation is correct.
- **Real decision, never said the thing.** `study-designer/058`: a number resolving to a real,
  current, same-repo decision whose body never made the claim at all.
- **A migration attributed to the wrong repo's decision.** `topology/052` found two sibling files
  carrying "formerly `embarch-core`'s own X" with this-repo numbers, where `embarch-core`
  decision 22 is the one that records the move. **This repo's history has the same shape** —
  record layout went 2 → 3, the host decoder and the manifest generator both moved surface around
  — so a "formerly" or "used to" sentence is worth extra suspicion.
- **A dated count that has drifted.** `study-designer/053` found a test count in a comment stale
  against the real suite. `tests/run-all.sh` and `.github/workflows/host-tests.yml` both cite
  decisions *and* describe how many tests run. If a number in a comment is a measurement, re-take
  it; if it drifted, say so rather than silently editing.

## The wrap-aware grep, run fresh

`grep -rnIE '[Dd]ecisions?[[:space:]]*$'` over the whole repo catches a citation whose word sits at
the end of one comment line and whose number sits on the next — invisible to every line-based
census (`core/068` found the class, `tasks/doc/071` named it). **At `b12ced1` this returns exactly
one line, in `tests/run-all.sh`.** Check whether it is a real wrapped citation or a coincidence,
say which, and do not fix a line that is not one. Run it fresh; do not trust this sentence.

## How to report

Report **every cited occurrence**, not deduplicated `(repo, number)` pairs — one line citing two
numbers is two instances, and the same number on two lines is two instances. Give four explicit
numbers, each of which may legitimately be zero: **lines matched, distinct citation instances
checked, wrong numbers found, false sentences found**, plus unlabelled cross-repo citations as a
fifth. **A zero is a real, reportable result, not a null one** — `api/106` and `umbrella/074` both
came back true zeros and both were worth having.

## Done when

- [ ] `src/outpost_priv.h`, `src/outpost_hooks.c` and `src/outpost.c` fully swept, with the four
      counts reported separately and every plain number and implementation-status claim in a cited
      sentence checked — not only the decision number.
- [ ] The real highest decision number in this sub-project established and stated, so an
      "unresolvable" finding can be told apart from a "wrong decision" finding.
- [ ] The whole-repo wrap grep run fresh and its hit adjudicated as real or coincidental.
- [ ] A follow-up task filed naming exactly which files remain.
- [ ] Gate green (`../../../embarch-fleet/protocol.md` §10) — noting there is no `Cargo.toml` here,
      so the cargo legs select nothing and that is not a failure.
- [ ] `changelog.d/outpost-*` fragment carrying the counts.
