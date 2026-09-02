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

### 13 — `init` derives what it can *by looking rather than assuming*, and refuses to guess the rest

For a Zephyr/west repo it reads the build system's own **recorded** command when one exists, because that is the only reliable answer to a working-directory-versus-positional-app-path question that **has already silently broken this suite once.**

**What it will not guess is the probe-rs chip name.** Zephyr's board identifier and probe-rs's target name are **different namespaces with no mechanical mapping**, so `init` writes a placeholder plus the exact invocation to resolve it, and `doctor` fails loudly while the placeholder is still there. **Guessing a chip name would produce a config that flashes the wrong target rather than an error.**

**The same principle applied twice more.** The artifact path is resolved by **searching the build tree for a real firmware image, shortest match wins**, rather than assuming a layout — a sysbuild nests it a level deeper than a plain build and **which applies depends on the SDK.** And a pristine-rebuild flag found in the recorded command is **reported, not removed**: with a separate build directory the user may well still want it, so that is their call.

### 17 — `init` stops guessing a single board for a Zephyr/west repo; board and chip are deferred to call time

**Prompted directly by running `init` for real against a real firmware repo**: it has four real boards, and reading whichever recorded build happened to exist **silently picked a dev board's build over the production one, with no signal that a choice had even been made.**

For a repo shaped like a Zephyr/west project, `init` now writes the minimal discovery schema — no build command, no chip, no artifact paths — instead of guessing a board. **Decision 13's chip-placeholder behaviour no longer applies to this case at all**, because chip has nowhere to be written down: it is resolved per call from the selected SoC. Decision 13's command-derivation and path-translation logic **move out of `init` and become `embarch-api`'s call-time logic** — same computation, different call site: once at scaffold time becomes every time a target is resolved. A repo that is not Zephyr/west-shaped is unchanged.

**Verified as real cross-repo interop, not three components unit-tested in isolation:** `init` detected the shape and wrote a config with nothing to hand-edit; **that same config, unmodified, loaded directly into a real `embarch-api` binary** whose target listing returned the correct file-backing-validated set; and `doctor` branched all three affected checks correctly, including one that **genuinely failed because `west` was not on that sandbox's `PATH`.**

**Amended: the target count check now shells out to `embarch-api`'s own listing instead of maintaining a second scanner.** The trimmed copy this decision introduced was deliberately coarser than the real scan — it counted a hardware revision as backed if *any* revision-suffixed file named it, rather than checking the exact tuple. But **unlike topology detection or token parsing, there is no bootstrapping problem here**: by the time that check runs, `init` has already run and a real config exists, so nothing stops asking the real thing. The lightweight *shape detection* stays, because `init`'s own detection genuinely does run before a config exists.

### 26 — `study_results/` retention and per-target build-directory pruning get an explicit policy instead of "grows forever"

Both currently have **no cleanup mechanism at all.** A `doctor --prune` flag — **opt-in, never automatic, because deleting build artifacts or study results is not something `doctor`'s normal read-only pass should ever do silently.** It always *reports* how many result entries exist and their size, and how many distinct build-directory combinations exist per project; with the flag it offers to delete results older than a configurable age and build directories for a target combination **no longer among the project's currently-valid targets** — never a currently-valid target's directory regardless of age, **since rebuilding it is the expensive part.**
