# 014 — The `-args<hash>` build-directory segment uses `DefaultHasher`, which is not stable across Rust releases

**State:** claimed by agent/api/014-extra-args-hash-not-stable, 2026-09-05 22:12
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

- [ ] `build_dir_name`'s `extra_args` segment is computed by a hash whose value
      is fixed by this crate rather than by the toolchain, or by a non-hash
      spelling.
- [ ] A test asserts the hash of a known argument list equals a **hard-coded
      literal**, so a future change to the hashing is a failing test rather than
      a silent rename.
- [ ] Decision 19 records the change, and says what happens to directories
      already named by the old scheme.
- [ ] `changelog.d/` fragment; gate green.

**Reserve, measured by leg 012 at dispatch (2026-09-05 22:12):** **nothing in the suite is
in reserve** — `api/012` landed an hour ago and took `embarch-api/spec.md` from 98.7% to
87.6%. The file this task's decision belongs in, `decisions/build.md`, is at 7.2K / 12K.
The one to watch is **`interfaces/config.md` at 11,035 / 12,288 B (89.8%) — 24 bytes below
the reserve line**, so if you write there you will almost certainly cross it. That file's
compaction is already carried by `tasks/api/013`, which is closed, so if you push it into
reserve you owe the ride-along in your own commit (`DOC-COMPACTION.md` §2): shorten it
there and then, rather than filing a task. Measure with
`python3 scripts/check-doc-size.py --pressure` before you report — do not assume.
