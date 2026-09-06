# 014 — The `-args<hash>` build-directory segment uses `DefaultHasher`, which is not stable across Rust releases

**State:** done, 2026-09-05, on `agent/api/014-extra-args-hash-not-stable`.
**Source:** embarch-umbrella/005 (doctor check 16, 2026-09-05) — found while counting per-target build directories
**Scope:** api
**Hardware:** none

## What

`embarch-api`'s `zephyr::Target::build_dir_name` folds `extra_args` into the
directory name as `-args{:016x}` computed with
`std::collections::hash_map::DefaultHasher`. **`DefaultHasher`'s output is
explicitly not guaranteed stable between Rust releases** — the standard library
documents it as an implementation detail that may change — so a toolchain bump
silently renames every `-args*` build directory.

Nothing breaks loudly. The next build for the same target simply misses its
cache and creates a second directory beside the first, and the first is now
unreachable by any selection: an orphan nothing will ever reuse and nothing
prunes. The unit test that guards this (`build_dir_name_folds_in_extra_args…`)
asserts stability *within one process*, which is exactly the property that holds
across a toolchain change too, so it cannot catch this.

A stable hash fixes it — a small explicit FNV-1a or SipHash with a pinned key
over the joined args, or a sorted-and-sanitised literal spelling if the args are
short enough to keep the "readable listing" property decision 19 wanted.

## Why now

Cheap, and it is one of the two mechanisms behind unbounded build-tree growth
that `embarch-umbrella` decision 26 exists to bound. Orphans made this way are
the worst kind for a future `doctor --prune`: they belong to a *currently-valid*
target, so the "never delete a valid target's directory" rule protects them
forever while nothing will ever build into them again.

No evidence this has bitten yet — it needs a toolchain bump plus a project that
actually uses `extra_args`, and nobody has reported a duplicated build directory.

## Done when

- [x] `build_dir_name`'s `extra_args` segment is computed by a hash whose value
      is fixed by this crate rather than by the toolchain, or by a non-hash
      spelling.
- [x] A test asserts the hash of a known argument list equals a **hard-coded
      literal**, so a future change to the hashing is a failing test rather than
      a silent rename.
- [x] Decision 19 records the change, and says what happens to directories
      already named by the old scheme.
- [x] `changelog.d/` fragment; gate green.

**Reserve, measured by leg 012 at dispatch (2026-09-05 22:12):** **nothing in the suite is
in reserve** — `api/012` landed an hour ago and took `embarch-api/spec.md` from 98.7% to
87.6%. The file this task's decision belongs in, `decisions/build.md`, is at 7.2K / 12K.
The one to watch is **`interfaces/config.md` at 11,035 / 12,288 B (89.8%) — 24 bytes below
the reserve line**, so if you write there you will almost certainly cross it. That file's
compaction is already carried by `tasks/api/013`, which is closed, so if you push it into
reserve you owe the ride-along in your own commit (`DOC-COMPACTION.md` §2): shorten it
there and then, rather than filing a task. Measure with
`python3 scripts/check-doc-size.py --pressure` before you report — do not assume.

## What was done

`zephyr::extra_args_hash` — FNV-1a (64-bit), written out in `src/zephyr.rs`, over
a **length-prefixed** encoding of each argument (so `["-p", "always"]` and
`["-p always"]` cannot collide). `DefaultHasher` is gone from the crate.

FNV over a keyed SipHash because `extra_args` comes from this machine's own
project config, never an untrusted caller — there is no hash-flooding threat a
key would answer, only accidental collision over a few short flags — and a key
is one more thing that has to stay in step with names already on disk. A
sanitised non-hash spelling was rejected: an arbitrary flag has no length bound,
its escaping is a second thing to hold stable, and `target.json` already answers
"what produced this directory" better than a name can.

`build_dir_name_args_hash_matches_a_hard_coded_literal` pins
`ref_board-default-2-widget-args6222ab5e7fce6ae9` and three raw hash values; the
pre-existing same-process test now carries a comment saying why it could not
catch this. Decision 19 records the change **and** that every existing `-args*`
directory is orphaned by it, deliberately and once, with the reason no migration
is soundly buildable (recomputing an old name means reproducing the
`DefaultHasher` output of whichever toolchain wrote it).

`decisions/build.md` went to 10,934 / 12,288 B (89.0%) — under the reserve line,
confirmed with `check-doc-size.py --pressure`: nothing in the suite is in
reserve. `decisions.md`'s size column for that file was updated. `interfaces/
config.md` was **not** touched: its `-args<hash>` description is still true.

Not done: nothing hardware-side, and no directory cleanup — the orphaned
directories are a human's to delete, and `doctor --prune` still must not.
