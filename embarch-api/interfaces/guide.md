# embarch-api: `guide`

**Status:** active, 2026-11-20.

Decision: [108](../decisions/guide.md). Index: [tools.md](tools.md).

`embarch-api guide hil [mode]` prints the hardware-in-the-loop guide embedded in the binary. CLI only; needs no config, no Core and no `embarch-doc` on disk.

| Call | Prints |
|---|---|
| `guide hil` | the "Choosing a mode" part |
| `guide hil live` / `study` / `test` | that mode's section |
| `guide hil <anything else>` | exit 1, stderr names the modes `live, study, test` |

`--json` gives `{success, mode, text}`, or `{success: false, error}`. Each section is the `## ` heading of `guide/hil-guide.md` in the `embarch-api` repo; today every one says it is not written yet and names `embarch-hil-proposal.md`.

The `embarch-hil` skill, `skills/embarch-hil/SKILL.md` in the same repo, holds the "which mode" table and points at these four commands; a test runs each of them. Installing it into a firmware repo is `embarch-umbrella`'s (`embarch init`) and is not done.
