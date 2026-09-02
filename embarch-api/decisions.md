# embarch-api: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Config: [interfaces/config.md](interfaces/config.md). Tools: [interfaces/tools.md](interfaces/tools.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §7.2–7.4). `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions | Size |
|---|---|---|
| [Scope and boundaries](decisions/shape.md) — what this is, what it is not, the one-way relationships | 1, 2, 3, 4, 6, 7, 8, 9, 10, 25 | 3.3 KB |
| [The tool and CLI surface](decisions/surface.md) — what is exposed, how failures are shaped | 16, 18, 23, 24, 29, 34, 35, 41 | 4.6 KB |
| [Build orchestration and target discovery](decisions/zephyr.md) — the generic command, and the Zephyr exception | 5, 12, 13, 19, 20, 21, 22, 42 | 5.7 KB |
| [Reaching Core](decisions/core-link.md) — addressing, artifact transfer, the shared client, the stack | 11, 14, 15, 17, 26, 36, 37, 38, 43 | 8.6 KB |
| [Submitting and orchestrating studies](decisions/studies.md) — seals, schemas, reflash | 27, 28, 30, 31, 33, 39, 40, 44 | 12.0 KB |
| [The dev-bench pipeline](decisions/dev-bench.md) — outside `[[projects]]`, and no longer constants | 32, 45 | 3.6 KB |

**Decisions 31 and 33 are the same decision, recorded twice** — byte-identical text, the duplicate created in the very commit that deleted 31. One entry owns both numbers, in [studies.md](decisions/studies.md).
