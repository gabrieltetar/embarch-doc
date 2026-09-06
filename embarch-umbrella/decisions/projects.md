# embarch-umbrella decisions: Integrating a firmware repo

**Status:** active, 2026-09-02.

What `embarch init` writes into somebody else's repo, and what it refuses to guess.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Per-repo project config lives in an `embarch/` subfolder of that repo, scaffolded by `embarch init`

Three things follow from that shape:

- **Scoped by construction.** An `embarch-api` started with this config sees only this repo's projects, so **`list_projects` in a firmware repo cannot offer up an unrelated board to flash.**
- **A separate build directory is the default, not an option.** Sharing one build tree with the engineer's interactive builds means **EmbArch and the human clobber each other** — different board revisions, different pristine-vs-incremental state. `init` writes the separate directory into the scaffolded command and points the artifact path at it.
- **It is a complete config, not a fragment.** The Core section gets duplicated into every repo, which is real duplication — **accepted because that section is three lines and an include mechanism is new code in `embarch-api`'s config loader.** Carried to [../open.md](../open.md).

### 12 — Local-only integration touches nothing that is committed

For a repo owned by someone else — a client's firmware repo — **`init` must not dirty tracked files.** So the folder is excluded via `.git/info/exclude`, **not** by editing the repo's committed ignore file, and the MCP server is registered at the agent's per-project, per-user scope rather than by writing a config at the repo root. **Both are reversible and invisible to anyone else cloning the repo.** Committing the integration later is a deliberate follow-on step, not the default.

**And the shape it takes when a team does commit it: a checked-in registration naming `embarch-api` on `PATH`, with a repo-relative config path** — portable, and `embarch setup` already puts the binary on `PATH` (decision 28). Every other shape loses: env expansion is two variables to get wrong with an opaque failure when unset, a wrapper script needs a Windows twin, absolute paths break for every other engineer, and umbrella-as-the-MCP-server is refused outright (decision 5).

### 13 — `init` derives what it can *by looking rather than assuming*, and refuses to guess the rest

For a Zephyr/west repo it reads the build system's own **recorded** command when one exists, because that is the only reliable answer to a working-directory-versus-positional-app-path question that **has already silently broken this suite once.**

**What it will not guess is the probe-rs chip name.** Zephyr's board identifier and probe-rs's target name are **different namespaces with no mechanical mapping**, so `init` writes a placeholder plus the exact invocation to resolve it, and `doctor` fails loudly while the placeholder is still there. **Guessing a chip name would produce a config that flashes the wrong target rather than an error.**

**The same principle applied twice more.** The artifact path is resolved by **searching the build tree for a real firmware image, shortest match wins**, rather than assuming a layout — a sysbuild nests it a level deeper than a plain build and **which applies depends on the SDK.** And a pristine-rebuild flag found in the recorded command is **reported, not removed**: with a separate build directory the user may well still want it, so that is their call.

### 17 — `init` stops guessing a single board for a Zephyr/west repo; board and chip are deferred to call time

**Prompted directly by running `init` for real against a real firmware repo**: it has four real boards, and reading whichever recorded build happened to exist **silently picked a dev board's build over the production one, with no signal that a choice had even been made.**

For a repo shaped like a Zephyr/west project, `init` now writes the minimal discovery schema — no build command, no chip, no artifact paths — instead of guessing a board. **Decision 13's chip-placeholder behaviour no longer applies to this case at all**, because chip has nowhere to be written down: it is resolved per call from the selected SoC. Decision 13's command-derivation and path-translation logic **move out of `init` and become `embarch-api`'s call-time logic** — same computation, different call site: once at scaffold time becomes every time a target is resolved. A repo that is not Zephyr/west-shaped is unchanged.

**Verified as real cross-repo interop, not three components unit-tested in isolation:** `init` detected the shape and wrote a config with nothing to hand-edit; **that same config, unmodified, loaded directly into a real `embarch-api` binary** whose target listing returned the correct file-backing-validated set; and `doctor` branched all three affected checks correctly, including one that **genuinely failed because `west` was not on that sandbox's `PATH`.**

**Amended: the target count check now shells out to `embarch-api`'s own listing instead of maintaining a second scanner.** The trimmed copy this decision introduced was deliberately coarser than the real scan — it counted a hardware revision as backed if *any* revision-suffixed file named it, rather than checking the exact tuple. But **unlike topology detection or token parsing, there is no bootstrapping problem here**: by the time that check runs, `init` has already run and a real config exists, so nothing stops asking the real thing. The lightweight *shape detection* stays, because `init`'s own detection genuinely does run before a config exists.

**The amendment is not built, as of 2026-09-03** — everything above it is.
Check 8 still calls this crate's own `zephyr::count_valid_targets`, the trimmed
scanner the amendment says was replaced, and its code comment still records the
deliberate overcount it describes: a revision counts as backed if *any*
revision-suffixed file in the board directory names it. Nothing in the crate
shells out to `embarch-api list-targets` — the one mention of that command is a
fix line telling a human to run it. The bootstrapping argument the amendment
makes is untouched by this; it simply was never acted on.

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
- **Nothing in this crate can name a valid build directory, only count
  directories.** `crate::zephyr` returns a count and deliberately overcounts
  (decision 17); it does not model variant names or cpucluster, so it cannot
  produce `embarch-api`'s `build_dir_name`. Naming them is
  `embarch-api list-targets`'s job, and **wiring that shell-out is decision
  17's amendment, which is itself unbuilt.** Deleting on an oracle this crate
  does not have is precisely what "never a currently-valid target's directory"
  exists to prevent.
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
  directories it has no evidence about. That removes the second of this
  bullet's two blockers and not the first: naming the currently-valid targets
  still needs decision 17's unbuilt `embarch-api list-targets` shell-out.

So: **measure now, delete never, and no `--prune` until a valid-target oracle
exists.** Nothing has reported disk pressure, which is the reason visibility is
the proportionate step and not the reason to skip it — "grows forever" is still
literally true of build directories, and check 16 is what makes it visible.
[../spec.md](../spec.md) claimed the flag until the 2026-09-03 audit and now
says what actually ships.
