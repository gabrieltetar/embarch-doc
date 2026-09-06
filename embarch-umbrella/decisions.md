# embarch-umbrella: decisions

**Status:** active, 2026-09-06.

Why the onboarding binary is shaped this way. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-umbrella decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/release.md](decisions/release.md) | 1, 2, 27, 29 | The binary, its name, and the tag-versus-manifest assertion |
| [decisions/install.md](decisions/install.md) | 3, 4, 5, 14, 21, 25, 28 | Core as an autostarting service, `up`/`down` as a fallback, the release archive, and what `setup` really writes |
| [decisions/topology.md](decisions/topology.md) | 6, 7, 8, 9, 30, 38 | Detecting where Core is, elevation, the WSL2 loopback ambiguity, and which `embarch-core` a `wsl-host` machine actually runs |
| [decisions/integration.md](decisions/integration.md) | 10, 12 | Where a repo's `embarch/` config lives, and how little of it anyone else can see |
| [decisions/projects.md](decisions/projects.md) | 13, 17, 26, 41 | What `init` derives from a firmware repo, and what it refuses to guess |
| [decisions/doctor.md](decisions/doctor.md) | 18, 19, 31, 42 | The check chain, the states it refuses to conflate, and which `embarch-api` it is about |
| [decisions/bind.md](decisions/bind.md) | 22 | Check 17: whether Core is listening where this topology can reach it |
| [decisions/mcp.md](decisions/mcp.md) | 23, 40 | Check 10: finding our MCP registration in the agent CLI's config, and making it answer |
| [decisions/reporting.md](decisions/reporting.md) | 11, 37, 39 | What `doctor` and `status` hand back, and the fields a consumer reads |
| [decisions/schema-skew.md](decisions/schema-skew.md) | 24, 33, 34, 35, 36 | What checks 11 and 15 compare, where each number comes from, and why skew warns |
| [decisions/mirrors.md](decisions/mirrors.md) | 15, 16, 20 | The liftable-copy pattern, and what survived `embarch-topology` |
| [decisions/deploy.md](decisions/deploy.md) | 32 | `deploy-core`, and the verification that is the point of it |

**Decisions 27 and 29 are one decision under two numbers** — an insertion renumbered it. See [release.md](decisions/release.md).
