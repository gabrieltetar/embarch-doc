# 013 — `target.json` is documented as beside every build directory and is never written

**State:** done, 2026-09-05, on agent/api/013-target-json-not-written
**Source:** embarch-umbrella/005 (doctor check 16, 2026-09-05) — found while looking for a build directory's provenance
**Scope:** api
**Hardware:** none

**Compacts:** embarch-api/interfaces/config.md
**In flux:** yes — by this task, which is the point: `tasks/api/012-compact-api.md` is `blocked` on exactly
that, and a blocked compaction task parks the pass, not the reserve (`DOC-COMPACTION.md`
§2). You are the unit that rewrites that file's build-directory paragraph, so **compact it as part of this
commit**, honour `tasks/api/012-compact-api.md`'s `Must not delete:` list, and close only its item there.
**Headroom: 873 B of 12,288** — enough to write the answer, not enough to write it
cleanly and leave the file usable. `Must not delete:` here, carried from 012: decision 21's
*first* paragraph as written, decision 18's `[assumed]` 1:3 split, and decision 22's cost
bound — all three are provenance that reads as measurement once shortened.

## What

`embarch-api` decision 19 says "**a `target.json` recording the full resolved
selection**" is written beside every per-target build directory, and
`embarch-api/interfaces/config.md`'s build-directory paragraph states it as
current truth: "each build directory gets a `target.json` recording the full
resolved selection so a human can recover what produced it without
reverse-engineering a hash."

**Nothing writes it.** `grep -rn 'target\.json' embarch-api` over the whole repo
(`.rs` and `.md`) returns only the two doc mentions above and no source hit at
all; `resolve.rs` assembles `build_dir` and the build command and never touches
a manifest file. So the decision's own stated remedy for the `-args<hash>`
segment — the thing that makes a directory listing debuggable — does not exist.

Either build it (a serde write of the resolved `Target` + snippets + extra_args
into `<build_dir>/target.json`, at the point `resolve.rs` returns the plan) or
retire that half of decision 19 with a tombstone and drop the sentence from
`interfaces/config.md`. **The doc stating it as truth is the part that must not
survive either way.**

## Why now

It is load-bearing for something already deferred on it. `embarch-umbrella`
decision 26's `doctor --prune` would delete build directories for targets no
longer valid, and the only sound per-directory evidence of *which* target
produced one is this file — the directory name is not reliably parseable back
into a target, because board, app and snippet names all contain `-`
(`…-ble-shell_wdt31`). Umbrella deferred `--prune` on 2026-09-05 partly for this.

Not urgent on its own; it is a two-line doc fix or a small write, and it unblocks
somebody else's decision.

## Done when

- [x] Either `target.json` is written beside each `zephyr-west` build directory
      with the resolved board/variant/revision/app, snippets and extra_args, and
      a test asserts it round-trips — or decision 19's `target.json` half is
      retired with a tombstone.
- [x] `embarch-api/interfaces/config.md` no longer states as truth whatever is
      not built.
- [x] `changelog.d/` fragment; gate green.

## Shipped

**Built, not retired** — `embarch-umbrella` decision 26 is already deferred
partly on this, so the cheaper doc fix would have left the blocker standing.

- `build::TargetManifest` + `write_target_manifest`, called from
  `run_build_locked`; `resolve_zephyr` fills it with **the descriptor value
  itself**, so a directory's provenance and the answer its caller got are one
  object rather than two serializations. `None` for `static` (no selection
  resolved) and dev-bench (west's default `build/`).
- Written **after** the build command, **only into a directory that already
  exists**, and never creating one — so it is evidence about a build directory
  rather than manufactured evidence, and nothing this crate does has to be
  correct for `west build -d` to own an empty directory. A **failed** build's
  directory gets one too.
- Through `json_out::pretty`, so it carries `schema_version` like every other
  JSON object this crate emits — this one is read by another repo, which is the
  case decision 50's promise exists for.
- **Absence means "unattributable", never "orphaned"**, and the write is
  best-effort. Stated in decision 19 and dropped in `inbox/` for
  `embarch-umbrella`, whose decision 26 still says the file is not written and
  whose `--prune` would be the consumer that could get this wrong.
- Four tests: the round trip, the no-directory case, a real `run_build`
  leaving one, and a failed build still leaving one. The first two are
  cross-platform; the `run_build` pair is `#[cfg(unix)]` like the rest of that
  file's end-to-end tests, which is this suite's known platform gap.

**Ride-along compaction, in this commit:** `interfaces/config.md` **11,415 →
10,944 B** (92.9% → 89.1%), out of reserve, with the corrected build-directory
paragraph already in it. Nothing on the `Must not delete:` list lives in that
file; what went was reasoning restated from decisions (the upward search's
rationale and its rejected alternative **moved into decision 25**, not deleted;
`base_address`'s "advice, not a check" and the dev-bench intro's rationale
dropped in favour of the pointers already beside them). `tasks/api/012`'s item
for this file was already ticked when it was narrowed, so nothing there needed
closing.

**No hardware debt.** Nothing here needs a board: the write is exercised through
a real child process. One thing is *unverified rather than undone* — that a real
`west build -d` is unaffected — and it is unverifiable here by construction,
since the write happens after west has already run and creates no directory west
could trip over. A first real Zephyr build will confirm the file appears.
