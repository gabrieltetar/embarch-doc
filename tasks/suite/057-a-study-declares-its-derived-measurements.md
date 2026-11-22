# 057 — A study declares its derived measurements, a host-type schema bump across four repos

**State:** open
**Source:** Fleet Ready issue: Core does not compute measurements when a study ends. `notes/hil/02-study.md`, "Measurements": derived measurements are "declared by name in the study", and a Study's own declared values (a `dut` value's resolution and `U`, a declared sample rate) are "declared by the study, unconfirmed". `notes/hil/14-implementation-plan.md`, unit M1.7. Nothing yet fixes how a study declares either: `embarch-study-designer/interfaces/hil-shapes.md` fixes `measurements.json`, the output, and `hil-reducers.md` the reducers' `Input` and `window`, but `Study` has no field that names a measurement.
**Issue:** EMB-222
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

**A `measurements` field on `Study`**, in `embarch-study-designer`, `#[serde(default)]` and bounded like every other list on it: one declaration per derived measurement, each naming the measurement, the reducer (a name the `reducers` registry knows), the capture it reads (a tap, and the field where the tap is a struct), and the reducer's window parameters (`hil-reducers.md`); plus the values a Study declares for itself, each one labelled `study` in `u_source` when Core writes it (a `dut` source's resolution and `U`, a declared sample rate). The crate refuses at load a declaration naming an unknown reducer, a tap the study does not have, a repeated name, or a window the reducer does not take.

**It bumps `HOST_TYPE_SCHEMA_VERSION`** (`embarch-study-designer` decision 12: any change to a type crossing the api-Core hop), and it is a cross-repo pass because **`embarch-core`, `embarch-api` and `embarch-ui` each build `Study` as a struct literal in their tests**, so the crate cannot land on its own without turning three consumers' `cargo test` red. The pass, in §8's order:

1. `embarch-study-designer`: the type, the field, the load checks, the bump, a fixture per refusal; `decisions/` (a new topic file beside `hil-reducers.md`), `interfaces/` (the declaration's shape, beside `hil-shapes.md`), `spec.md`.
2. `embarch-core`, `embarch-api`, `embarch-ui`: each test literal gains the field; nothing else changes. Gated against the branch's crate before anything lands.
3. `embarch-doc`: the changelog fragments, and `notes/hil/02-study.md` pointing at the new shape.

## Why now

M1.7 (`tasks/core/132`, Core writes `measurements.json`) cannot start without it: Core cannot compute a measurement nobody declared, and a Core worker cannot change the shared crate.

## Notes for whoever runs it

- **A host-type bump means a deployed Core and a rebuilt embarch-api refuse each other until both are rebuilt** from the new `main`, and the running MCP binary goes stale against it. That is a deploy the owner makes; the fold's log entry says so as a debt, and nothing here deploys.
- Read the consumers' manifests for the feature sets they build the crate with (`../embarch-fleet/gate.md`), and gate each set.
- `embarch-study-designer` decisions near their size limit (`check-doc-size.py --pressure`): `streams` #39, `versioning` #12, `seals` #17, `declares` #40, `authoring` #73 and `protocols` #58 each have under 150 B; a new topic file is the home.
- Out of scope: computing anything (that is `core/132`), and the Test phase's definition-time refusals on an undeclared `U`.

## Done when

- [ ] A study with a `measurements` list round-trips through the crate, and each refusal above has a fixture.
- [ ] `HOST_TYPE_SCHEMA_VERSION` bumped, its history line written.
- [ ] `embarch-core`, `embarch-api` and `embarch-ui` build, test and pass `clippy --all-targets -- -D warnings` against the new crate, each on its own `main`.
- [ ] `spec.md`, `decisions/`, `interfaces/` updated in `embarch-study-designer`; `changelog.d/` fragments dropped.
- [ ] `check-docs.py` green.
