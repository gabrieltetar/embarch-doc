# embarch-study-designer: the type model

**Status:** active, 2026-09-02.

The study and result types. Field-level, concrete enough that a `serde`-derived translation is mechanical. Every sequence and string is fixed-capacity ([../decisions/limits.md](../decisions/limits.md) holds each bound). GATT and transcript types: [gatt-types.md](gatt-types.md). Stream taps: [taps.md](taps.md). Payload layouts: [decoders.md](decoders.md). Protocol manifests: [eap.md](eap.md). Why: [../decisions.md](../decisions.md).

## `Study`

| Field | Notes |
|---|---|
| `name` | Human-readable, **not required to be unique** — uniqueness, if ever needed, is a caller's concern |
| `requires: Requirements { dev_bench_version, firmware_version }` | The builds this study is meant to run against. Both mandatory, `any` a legal explicit value. **No serde default, deliberately:** an omitted `requires` fails to deserialize rather than defaulting to `any`, which is what makes "it has to be *said*" true rather than aspirational |
| `streams: Vec<StreamTap>` | Declared capture channels. `#[serde(default)]`, unlike `requires`: a study authored before taps existed captured nothing, and still does |
| `gatt: Option<DeclaredGatt>` | The table this study was authored against and where it came from (`Vendor` / `Extracted { repo, revision }` / `Authored`). Host-side only; reconciled against a live discovery, **with the live table winning and the difference reported** |
| `steps: Vec<Step>` | Run in order. Entirely static once submitted — no generator construct, because fuzzing treats a `Study` as its *output* |
| `decoders: Vec<StructLayout>` | Host-only payload layouts; a tap carries only an index. See [decoders.md](decoders.md) |
| `protocols: Vec<ProtocolDef>` | Resolved from `.eap` at build time. See [eap.md](eap.md) |
| `dev_bench_log_level` | How loud the bench should be for this run. `#[serde(default)]` to `Warn`, which is what earlier studies effectively ran at — so **the default is the *right* value, not merely a permissive one** |
| `steps_crc` / `streams_crc` / `protocols_crc` | Three sibling seals, each over the one span it names. Recomputed and overwritten by whoever submits, so no stored value is ever trusted. `streams_crc` is `#[serde(default)]` where `steps_crc` is not: `0` is the genuine CRC of zero bytes rather than a sentinel |

## `Step`

`name` (a label carried into results for human correlation, never for machine correlation), `action`, `timeout_ms` (how long the *action* may take), `delay_before_ms` (how long the bench waits **before** starting it — **not deducted from `timeout_ms`**, so `TimedOut` keeps meaning "the action took too long" rather than "the delay was long"), and `continue_on_fail` (default `false`: abort immediately, since most steps are prerequisites for what follows — a failed connect makes every later exchange moot).

`power_sample` was here and is **retired**: a power tap scoped to the same step range says the same thing, and was already the only one of the two anything read.

## `Action`

| Variant | What it does |
|---|---|
| `BleAdvertise { local_name?, service_uuids, adv_interval_ms }` | Advertise as a peripheral for the DUT to discover |
| `BleConnect { role, target_address?, target_name? }` | `target_name` matches the advertised Local Name **exactly**; blank means no filter. Both may be set and both must then match. **Both `None` means "whichever connectable peripheral advertises first", which on any bench with another BLE device in range is a coin toss** — decision 43 has the live evidence |
| `DataExchange { service_uuid, characteristic_uuid, operation }` | `Read`, `Write { payload }`, `Notify { timeout_ms }`, `Indicate { timeout_ms }` (both bounded independently of the step's own budget, since a notify-wait is often shorter), or `Subscribe` (arm without waiting). **UUIDs are raw, not symbolic** — no name-resolution table to maintain |
| `GattDiscover {}` | Walk every primary service and characteristic, reporting the table and **acting on it no further** |
| `GattMonitorAll {}` | That same walk, then subscribe to everything notify- or indicate-capable and capture until the step's timeout |
| `GattMonitorStart {}` / `GattMonitorStop {}` | The same walk, **leaving subscriptions armed so the window outlives this step**. This is the one pair that makes stimulate-and-capture expressible at all. A `Stop` with no open window is a no-op `Pass` |
| `GattMonitorSelected { targets }` / `GattMonitorSelectedStart { targets }` | Narrowed to the characteristics the study names. **May not be empty** — "monitor these" with nothing named is refused rather than promoted to "everything". A target absent from the DUT, or that can neither notify nor indicate, **fails the step naming it** |
| `BleSecurity { level }` | Request at least `level` and wait for the link to reach it, or drop, within the step's timeout. **`L1` is authorable and means "this DUT needs none", said out loud.** A link already at or above `level` is a `Pass` — as is a procedure already in flight when the step started, which is what real hardware produced. Carries **no** passkey, IO capability or bonding: those are the bench's |
| `BleUnbond {}` | Clear the bond table mid-study, so "pair, work, drop, pair again" is authorable. **Disconnects**, because clearing a peer's keys disconnects it — so a study that unbonds needs its own connect afterwards |
| `RunProtocol { protocol, entry_state }` | Hand the link to a declared state machine for one step. Both fields are indices. See [eap.md](eap.md) |

`StreamCapture` was a sixth `GattOperation` and is **removed outright** rather than left as a dead variant: an authorable action nothing dispatches is the silently-captures-nothing failure decision 36 was opened by.

**`BleAddress`'s six raw bytes are display order, most-significant first**, matching this crate's big-endian UUID convention. Previously unstated — a real risk, since a wrong guess means an explicit `target_address` silently never matches.

A step's `Outcome` is the only on-device signal: **did the action complete without a protocol-level error or timeout.** Whether the content it produced was *correct* is a separate question, and the answer is no longer post-hoc validation — see [../decisions/removed.md](../decisions/removed.md).

## Results

- **`Provenance { dev_bench_version, firmware_version, dev_bench_source, firmware_source, overrides }`** — what the study ran against, **how each version was established**, and which requirements it was allowed past. The source is `ReportedByDevBench` / `ReportedByOutpost` / `FlashedThisRun` / `Declared`, and **it is not bookkeeping**: a `Declared` version is an assertion nobody checked, and a result rendering it identically to a verified one would reintroduce exactly the mislabelling this exists to close. The bench is always `ReportedByDevBench`, read off the live handshake. `FlashedThisRun` is **structurally impossible for Core to produce alone** and is supplied by the process that sequenced both the flash and the submission.
- **`overrides`** — one entry per requirement this run proceeded past, empty in the normal case, each carrying the subject plus **both strings**. A record rather than a flag, **because neither string is recoverable from the rest of the result**: `requires` never travels into it. A bare boolean would say a rule was bent without saying which or by how far — the same half-answer `Declared` exists to stop this type giving.
- **`StudyResult { study_name, steps, provenance, streams }`** — `steps` is **not guaranteed to match the submitted length**: a failing step with `continue_on_fail` false aborts, leaving a proper prefix. `streams` carries one `StreamRef { name, bytes_written, truncated }` per declared tap, **including one that produced nothing** — a missing entry and an empty one are different facts.
- **`StepResult { step_name, outcome, captured_data?, gatt_services?, security_level?, protocol? }`** — `Outcome` is `Pass`, `Fail { reason }`, or `TimedOut`. `security_level` is populated **for every step, not only a security one**, which is a deliberately larger claim and the one that pays: a disconnect during discovery at L1 and the same failure at L4 are different findings, and nothing in a result could distinguish them before. `None` means there was no connection to ask about, **never that nobody looked**.

`gatt_activity`, `power_samples_ref` and `waveform_ref` were here and are **retired** — see [../decisions/removed.md](../decisions/removed.md).

