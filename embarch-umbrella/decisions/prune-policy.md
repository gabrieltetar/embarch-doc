# embarch-umbrella decisions: Pruning results and build directories

**Status:** active, 2026-10-26.

Whether `doctor` ever deletes `study_results/` or per-target build directories, and what a `--prune` would need first. Split verbatim out of [projects.md](projects.md) on 2026-10-26 (`umbrella/084`); decision 26 is the file's still-moving half, so it now has headroom of its own.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 26 — `study_results/` retention and per-target build-directory pruning get an explicit policy instead of "grows forever"

Both currently have **no cleanup mechanism at all.** A `doctor --prune` flag — **opt-in, never automatic, because deleting build artifacts or study results is not something `doctor`'s normal read-only pass should ever do silently.** It always *reports* how many result entries exist and their size, and how many distinct build-directory combinations exist per project; with the flag it offers to delete results older than a configurable age and build directories for a target combination **no longer among the project's currently-valid targets** — never a currently-valid target's directory regardless of age, **since rebuilding it is the expensive part.**

**Amended 2026-09-05: the reporting half is built as `doctor` check 16; the
`--prune` half is deferred, and the `study_results/` half of the premise is
dead.** Three things the 2026-09-03 audit could not see, each found by reading
the other repos rather than this one:

- **`study_results/` retention is not unaddressed, and is not this
  sub-project's.** `embarch-core` ships `sweep_study_results` /
  `EMBARCH_STUDY_RESULTS_KEEP` (default 50, `0` disables), swept at
  `POST /study`, unit-tested, and documented as a user-facing knob in
  [../../suite/studies-guide.md](../../suite/studies-guide.md). This entry's
  "no cleanup mechanism at all" was true of both halves when written and is
  now true of one. **Umbrella will not build a second retention policy for a
  directory it does not own and cannot even reach on a `remote` topology** —
  that is the mirror-that-drifts mistake decision 17's amendment already
  refused for the target scan. What survives is a real gap check 16 reports
  instead: the sweep bounds a **count**, so the bytes behind those 50 runs are
  still nobody's bound.
- **Nothing in this crate can name a valid build directory**, and decision
  17's amendment (**built 2026-09-05**) deleted the overcounting scanner rather
  than growing it: the tuple oracle is a process away and this crate models
  less than before. Deleting on an oracle it does not have is what "never a
  currently-valid target's directory" exists to prevent.
- **The rule is under-specified against the build-dir name it would judge.**
  `embarch-api` decision 19 later folded snippets and an `extra_args` hash into
  that name, so a directory is not a target tuple and is not reliably parseable
  back into one — every segment can contain `-`, as `…-ble-shell_wdt31` shows.
  The sound test is a prefix match against enumerated valid names, which is the
  previous bullet's blocker. **Per-directory provenance does now exist**: as of
  2026-09-05 `embarch-api` writes `<build_dir>/target.json` for a `zephyr-west`
  build — the resolved `{project, board, soc, cpucluster, variant, revision,
  app, snippets, extra_args}` plus `schema_version`, written after the build
  command into a directory that already exists (its decision 19). The one rule
  a consumer must not get wrong: **absence means "unattributable", never
  "orphaned"** — every directory built before that date has none, the write is
  best-effort, and a `static` or dev-bench build never gets one, so a `--prune`
  reading a missing file as "no valid target claims this" deletes exactly the
  directories it has no evidence about. **What is left is one ask.**
  `list-targets`' JSON carries the tuple and not `build_dir_name`, which folds
  snippets and an `extra_args` hash a listing never sees — so a `--prune`
  needs `embarch-api` to publish that name, never a second attempt to derive
  it here. **Shipped 2026-09-17** (decision 77): `list-targets` now names
  `build_dir_name` for each row's *default* combination; a non-default build
  still needs `target.json` above. `--prune` needs both, not this alone.

So: **measure now, delete never.** With 17's amendment built, `--prune` is
deferred by choice rather than blocked: nothing has reported disk pressure,
which is the reason visibility is the proportionate step and not the reason to
skip it — "grows forever" is still
literally true of build directories, and check 16 is what makes it visible.
[../spec.md](../spec.md) claimed the flag until the 2026-09-03 audit and now
says what actually ships.
