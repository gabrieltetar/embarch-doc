# embarch-study-designer: a bench board's characterisation file

**Status:** active, 2026-11-20; split out of [hil-shapes.md](hil-shapes.md) verbatim by `tasks/study-designer/086`, which is the group's index and holds the conventions every HIL file shares. Why each open detail went the way it did: [decisions/hil-shapes.md](../decisions/hil-shapes.md), decision 90.

## A bench board's characterisation

`characterisation.json`, one per bench board type, **shipped with the board's released firmware** (03: resolution, `U` and range "ship with its released firmware"). Written by an EmbArch release, never by a study or the agent; read by Core at M1.7 and by `verify` (M1.11); carried in the zip at `characterisation/<board>.json`, its hash in the measurement's `instrument.characterisation` (06, "Instruments"). **Nothing in milestone 1 ships one**: every Study value from such a board reads `U undeclared` (02).

```json
{ "schema": 1, "board": "dev-bench", "firmware": { "version": "…", "image_sha256": "…" },
  "characterised": "2026-11-20", "valid_days": 365,
  "channels": [ { "name": "clock", "unit": "us", "range": { "min": 0, "max": 4294967295 },
                 "resolution": 1, "uncertainty": { "U": 2, "k": 2, "basis": "characterisation" } } ] }
```

| Key | Type | Meaning |
|---|---|---|
| `board` | string | The board type, as its identity names it |
| `firmware` | `{version, image_sha256}` | The released image this was measured on; ties it to the `released` hash list (03, smoke check) |
| `characterised` | date | The day it was measured (06: "a date") |
| `valid_days` | integer, at least 1 | The validity period (06). **Valid until** `characterised` + `valid_days`, inclusive; a measurement with `at_utc_ms` after it is `inconclusive`, `calibration_expired`, as an instrument's due date is *(shape: days, and the end inclusive)* |
| `channels` | array | One per thing it times or measures: `{name, unit, range {min, max}, resolution, uncertainty}`, `uncertainty` the `{U, k, basis}` above with `basis` `characterisation` |

