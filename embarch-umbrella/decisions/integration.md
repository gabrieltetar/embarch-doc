# embarch-umbrella decisions: The footprint an integration leaves

**Status:** active, 2026-09-06.

Where a repo's `embarch/` config lives, what it is allowed to touch, and the shape it takes if a team ever commits it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Per-repo project config lives in an `embarch/` subfolder of that repo, scaffolded by `embarch init`

Three things follow from that shape:

- **Scoped by construction.** An `embarch-api` started with this config sees only this repo's projects, so **`list_projects` in a firmware repo cannot offer up an unrelated board to flash.**
- **A separate build directory is the default, not an option.** Sharing one build tree with the engineer's interactive builds means **EmbArch and the human clobber each other** — different board revisions, different pristine-vs-incremental state. `init` writes the separate directory into the scaffolded command and points the artifact path at it.
- **It is a complete config, not a fragment.** The Core section gets duplicated into every repo, which is real duplication — **accepted because that section is three lines and an include mechanism is new code in `embarch-api`'s config loader.** Carried to [../open.md](../open.md).

### 12 — Local-only integration touches nothing that is committed

For a repo owned by someone else — a client's firmware repo — **`init` must not dirty tracked files.** So the folder is excluded via `.git/info/exclude`, **not** by editing the repo's committed ignore file, and the MCP server is registered at the agent's per-project, per-user scope rather than by writing a config at the repo root. **Both are reversible and invisible to anyone else cloning the repo.** Committing the integration later is a deliberate follow-on step, not the default.

**And the shape it takes when a team does commit it: a checked-in registration naming `embarch-api` on `PATH`, with a repo-relative config path** — portable, and `embarch setup` already puts the binary on `PATH` (decision 28). Every other shape loses: env expansion is two variables to get wrong with an opaque failure when unset, a wrapper script needs a Windows twin, absolute paths break for every other engineer, and umbrella-as-the-MCP-server is refused outright (decision 5).

### 59 — `init` installs the `embarch-hil` skill from a pinned copy, at the agent's project-skills path, excluded locally

**The text is a copy pinned in `embarch-umbrella` (`src/skills/embarch-hil/SKILL.md`, `include_str!`), and a unit test fails if it differs from `embarch-api/skills/embarch-hil/SKILL.md`.** The other route, asking the located `embarch-api` for its skill at `init` time, would couple `init` to an `embarch-api` new enough to answer, and `embarch-api` has no command that prints the skill (only the guide, decision 108 there); `embarch-api` is not this unit's to change. The cost accepted: the copy lags until someone copies it over, and the test catches that only where the sibling checkout sits beside this one (it panics, like the config-mirror test, rather than skipping).

**Where:** `<repo>/.claude/skills/embarch-hil/SKILL.md`, the project-skills location Claude Code documents. **[assumed]** — read from memory of that documentation this run, not re-confirmed against a live CLI. **Excluded** through a second `.git/info/exclude` entry under decision 12; `--uninstall` removes the directory and then `.claude/skills` and `.claude` if empty, never a neighbouring skill. **`--dry-run`** is new on `init`: it names every write or removal and does none.

**Not covered:** a repo `init`ed earlier gets it from a second `init` (decision 60). `doctor` does not check the skill, and the guide it points at is a skeleton until plan unit M1.13.

### 60 — `init` on a repo whose config exists installs what it lacks, exits `0`, and neither reads nor rewrites the config

The skill and each `.git/info/exclude` entry are checked by file and line only, and added when absent; the config is never opened, so one `init` cannot parse is not this path's business, and it is never reformatted. **Exit `0`, changed from `1`:** the repo is in the state `init` exists to reach, and a nonzero exit would make the workaround `--uninstall` (which deletes the edited config, decision 41) look like the cure. A script that relied on `1` to detect "already initialised" now sees `0`; it can test for the config itself. A repo that lacks nothing says so and changes nothing. `--dry-run` names each piece it would add. Decision 12 holds.

**The MCP registration is not checked or repaired on this path.** Whether it exists means asking `claude mcp list`, whose output shape is not pinned here, and re-running `mcp add` on a registered server errors; so the path prints the `claude mcp add` line instead. The config is not read, so the path of `embarch-api` to register stays the engineer's to confirm.
