# embarch-umbrella decisions: Integrating a firmware repo

**Status:** active, 2026-09-06.

What `embarch init` derives from a firmware repo, and what it refuses to guess. The footprint it leaves is [integration.md](integration.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 13 — `init` derives what it can *by looking rather than assuming*, and refuses to guess the rest

For a Zephyr/west repo it reads the build system's own **recorded** command when one exists, because that is the only reliable answer to a working-directory-versus-positional-app-path question that **has already silently broken this suite once.**

**What it will not guess is the probe-rs chip name.** Zephyr's board identifier and probe-rs's target name are **different namespaces with no mechanical mapping**, so `init` writes a placeholder plus the exact invocation to resolve it, and `doctor` fails loudly while the placeholder is still there. **Guessing a chip name would produce a config that flashes the wrong target rather than an error.**

**The same principle applied twice more.** The artifact path is resolved by **searching the build tree for a real firmware image, shortest match wins**, rather than assuming a layout — a sysbuild nests it a level deeper than a plain build and **which applies depends on the SDK.** And a pristine-rebuild flag found in the recorded command is **reported, not removed**: with a separate build directory the user may well still want it, so that is their call.

### 17 — `init` stops guessing a single board for a Zephyr/west repo; board and chip are deferred to call time

**Prompted directly by running `init` for real against a real firmware repo**: it has four real boards, and reading whichever recorded build happened to exist **silently picked a dev board's build over the production one, with no signal that a choice had even been made.**

For a repo shaped like a Zephyr/west project, `init` now writes the minimal discovery schema — no build command, no chip, no artifact paths — instead of guessing a board. **Decision 13's chip-placeholder behaviour no longer applies to this case at all**, because chip has nowhere to be written down: it is resolved per call from the selected SoC. Decision 13's command-derivation and path-translation logic **move out of `init` and become `embarch-api`'s call-time logic** — same computation, different call site: once at scaffold time becomes every time a target is resolved. A repo that is not Zephyr/west-shaped is unchanged.

**Verified as real cross-repo interop, not three components unit-tested in isolation:** `init` detected the shape and wrote a config with nothing to hand-edit; **that same config, unmodified, loaded directly into a real `embarch-api` binary** whose target listing returned the correct file-backing-validated set; and `doctor` branched all three affected checks correctly, including one that **genuinely failed because `west` was not on that sandbox's `PATH`.**

**Amended: the target count check now shells out to `embarch-api`'s own listing instead of maintaining a second scanner.** The trimmed copy this decision introduced was deliberately coarser than the real scan — it counted a hardware revision as backed if *any* revision-suffixed file named it, rather than checking the exact tuple. But **unlike topology detection or token parsing, there is no bootstrapping problem here**: by the time that check runs, `init` has already run and a real config exists, so nothing stops asking the real thing. The lightweight *shape detection* stays, because `init`'s own detection genuinely does run before a config exists.

**Built 2026-09-05**, having been documented as truth since 2026-09-02 and
found unbuilt by the 2026-09-03 audit. Check 8 runs `embarch-api --config
<config> --json list-targets <project>` and passes on a non-empty `targets`
array; `zephyr::count_valid_targets` and the revision, variant and soc
modelling behind it are **deleted**, leaving only the shape detection `init`
needs. Three outcomes, not two, because they are different facts: an empty
list or `embarch-api`'s own error text is a **fail** about the repo, and
*nobody to ask* — no located binary, no config, no JSON object — is a **warn
naming which**, never a pass.

**The deletion bought more than one less copy.** The trimmed scanner counted
the declared *default* revision as backed unconditionally, so for any repo with
a parseable `boards/` and an `app/` it could not return zero — the "every
declared revision is missing its overlay" fail its own comment promised was
**unreachable**, and check 8 was re-asserting `init`'s shape test under a
stronger name. An approximation that errs only toward passing is not a
conservative pass/fail signal; it is the absence of one.

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
  it here.

So: **measure now, delete never.** With 17's amendment built, `--prune` is
deferred by choice rather than blocked: nothing has reported disk pressure,
which is the reason visibility is the proportionate step and not the reason to
skip it — "grows forever" is still
literally true of build directories, and check 16 is what makes it visible.
[../spec.md](../spec.md) claimed the flag until the 2026-09-03 audit and now
says what actually ships.

### 41 — `init` never writes an inferred board as fact, and picks none of several recorded builds

Serving [`embarch-api/spec.md`](../../embarch-api/spec.md) §2 — **an inferred hardware fact is never recorded as fact** — whose last violation was `init`'s most load-bearing field: `build_command` came out of `build_info.yml` carrying its `-b <board>`, and that file records **whatever was last built**, not what is on the probe. A day of bring-up was lost to exactly that.

**The mechanism is the placeholder `chip` has always used** (decision 13): the board becomes `CHANGE-ME`, and the displaced value is quoted back in a comment and on stdout with **how old that build is** — an age, not a date, since `init` runs today either way. Nothing else is redacted; the west binary and app path are this repo's own facts. **Rejected: a marker beside a working value**, which changes nothing when the comment is skipped — and skipped is the whole failure. Commenting `build_command` out loses too: it leaves a config `embarch status` cannot load.

**Several recorded builds — [open.md](../open.md)'s undecided half — are all named and none picked.** `init` walks the repo for every `build_info.yml` rather than only `build/`, reports each with the board and age it recorded, and scaffolds the bare template. **Rejected: taking the newest** — the dev build behind the incident *was* the newest, so an ordered guess is the same defect with a rule attached. **The Zephyr/west arm is unchanged**; decision 17 settles it structurally there.
