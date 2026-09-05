# embarch-umbrella: decisions

**Status:** active, 2026-09-03.

Why the onboarding binary is shaped this way. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-umbrella decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/release.md](decisions/release.md) | 1, 2, 27, 29 | The binary, its name, and the tag-versus-manifest assertion |
| [decisions/install.md](decisions/install.md) | 3, 4, 5, 14, 21, 25, 28 | Core as an autostarting service, `up`/`down` as a fallback, the release archive, and what `setup` really writes |
| [decisions/topology.md](decisions/topology.md) | 6, 7, 8, 9, 30 | Detecting where Core is, elevation, and the WSL2 loopback ambiguity |
| [decisions/projects.md](decisions/projects.md) | 10, 12, 13, 17, 26 | What `init` writes into a firmware repo, and what it refuses to guess |
| [decisions/doctor.md](decisions/doctor.md) | 11, 18, 19, 22, 23, 31 | The check chain, and the states it refuses to conflate |
| [decisions/schema-skew.md](decisions/schema-skew.md) | 24, 33, 34, 35, 36 | What checks 11 and 15 compare, where each number comes from, and why skew warns |
| [decisions/mirrors.md](decisions/mirrors.md) | 15, 16, 20 | The liftable-copy pattern, and what survived `embarch-topology` |
| [decisions/deploy.md](decisions/deploy.md) | 32 | `deploy-core`, and the verification that is the point of it |

**Decisions 27 and 29 are one decision under two numbers** — an insertion renumbered it. See [release.md](decisions/release.md).
