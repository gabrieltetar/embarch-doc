# embarch-api: decisions

**Status:** active, 2026-09-03.

Why it is the way it is, split by mission. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Config: [interfaces/config.md](interfaces/config.md). Tools: [interfaces/tools.md](interfaces/tools.md), [interfaces/studies.md](interfaces/studies.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions | Size |
|---|---|---|
| [Scope and boundaries](decisions/shape.md) — what this is, what it is not, the one-way relationships, where the tests can reach, and the one target a `static` project has | 1, 2, 3, 4, 6, 7, 8, 9, 10, 25, 46, 53 | 7.7 KB |
| [The tool and CLI surface](decisions/surface.md) — what is exposed, how failures are shaped, watching a study live, what this binary says about itself | 16, 23, 24, 29, 34, 35, 41, 47, 50, 52 | 10.7 KB |
| [Running a build](decisions/build.md) — the generic per-project command, what a truncated log keeps, where the output lands, and the one address a `bin` needs | 5, 18, 19, 42 | 5.1 KB |
| [Target discovery and selection](decisions/zephyr.md) — the Zephyr exception, what a call may name, and what a `static` project refuses rather than ignores | 12, 13, 20, 21, 22, 51 | 7.3 KB |
| [Reaching Core](decisions/core-link.md) — addressing, artifact transfer, the shared client, the event stream, the stack | 11, 14, 15, 17, 26, 36, 37, 38, 43, 48, 49 | 10.6 KB |
| [Submitting and orchestrating studies](decisions/studies.md) — seals, schemas, reflash | 27, 28, 30, 31, 33, 39, 40, 44 | 11.0 KB |
| [The dev-bench pipeline](decisions/dev-bench.md) — outside `[[projects]]`, and no longer constants | 32, 45 | 3.6 KB |

**Decisions 31 and 33 are one decision under two numbers.** The commit that added decision 32 inserted it in the middle and **renumbered the entry below it from 31 to 33**, so every prose reference to `decision 31` written before that commit silently began pointing at a different entry. One entry owns both numbers, in [studies.md](decisions/studies.md) — which is why numbers are permanent here now (DOC-COMPACTION.md §5).
