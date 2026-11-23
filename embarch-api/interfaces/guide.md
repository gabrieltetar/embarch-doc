# embarch-api: `guide`

**Status:** active, 2026-11-23.

Decision: [108](../decisions/guide.md). Index: [tools.md](tools.md).

`embarch-api guide hil [mode]` prints the hardware-in-the-loop guide embedded in the binary. CLI only; needs no config, no Core and no `embarch-doc` on disk.

| Call | Prints |
|---|---|
| `guide hil` | the "Every mode" part: the words, the trust claim, choosing a mode, what comes before any hardware, what the agent never does |
| `guide hil live` / `study` / `test` | that mode's section |
| `guide hil <anything else>` | exit 1, stderr names the modes `live, study, test` |

`--json` gives `{success, mode, text}`, or `{success: false, error}`. Each section is the `## ` heading of `guide/hil-guide.md` in the `embarch-api` repo, a pinned copy of [suite/hil-guide.md](../../suite/hil-guide.md). "Every mode" and "Study" are written (HIL M1.13, EMB-228); "Live" and "Test" say they are not written yet. The Study section carries a BLE GATT data-acquisition study inline, which is `tests/fixtures/ble_gatt_rate_study.json`: `tests/ble_gatt_rate_fixture.rs` runs Core's pre-flight rules over it, checks the guide's copy against it, and runs the publish oracle over the guide's prose example.

The `embarch-hil` skill, `skills/embarch-hil/SKILL.md` in the same repo, holds the "which mode" table, says to read the shared part first, and points at these four commands; a test runs each of them. Installing it into a firmware repo is `embarch-umbrella`'s (`embarch init`) and is not done.
