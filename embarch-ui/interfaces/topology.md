# embarch-ui interfaces: the Topology tab's routes

**Status:** active, 2026-11-01.

The first section moved verbatim from [../interfaces.md](../interfaces.md) on 2026-11-01, when the bench editor's routes would have put that file in its reserve; nothing in it is reworded. The bench editor's routes and the canvas's events are new. Why: [../decisions/topology-boards.md](../decisions/topology-boards.md), [../decisions/saved-benches.md](../decisions/saved-benches.md), [../decisions/bench-model.md](../decisions/bench-model.md). Index: [../interfaces.md](../interfaces.md).

## The Topology tab's own routes

Two kinds, and the split is the point (decision 44). `/api/enroll`, `/api/signals`, `/api/enrolled/{role}` and `/api/topology/link` are **proxies**: the write is Core's, and this binary holds the bearer token so the browser never sees it. The rest read and write **project files** in the open firmware repo — `embarch/boards.toml` and `embarch/topologies/` — and answer `409` with the way out when no project is open, since the catalog is not missing, it is unanswerable.

| Method | Path | Notes |
|---|---|---|
| `POST` | `enroll` | `{role, chip, probe_serial?, name?}` → Core's `POST /probes/enroll`. Binds the **probe** half of a role and reads an identity through it; `chip` and `name` come from the board *type* already in that role (45), not from anything typed |
| `POST` | `topology/roles/{role}/board` | `{board, chip}` → Core's `PUT /probes/enrolled/{role}/board`. The **board** half: which board type is in the role. **Opens no probe**, works with nothing plugged in, and leaves any recorded hardware ID alone so a validate pass can disagree with it |
| `GET` | `topology/pickers` | What each role's board picker offers: `dut` from the open project's catalog, `dev-bench` from the suite's supported pair, each `{board, label, chip}`. **Served, never restated in `app.js`** |
| `POST` | `topology/boards/rescan` | Merges the west targets this repo builds for into the catalog. **Only ever adds**: an entry already in the file keeps every field, and one the scan does not find is reported in `not_in_scan` and kept, since a repo builds for boards on branches that are not checked out |
| `DELETE` | `enrolled/{role}` | → Core's `DELETE /probes/enrolled/{role}`. `404` when nothing held that role. Takes a role outside the pair on purpose: clearing exactly those is what it is for |
| `POST` | `topology/link` | `{serial?, interface?}` → Core's `POST /dev-bench/link`. Its caller is a confirmed profile proposal, not a form |
| `POST` | `topology/validate` | One pass: each role through Core's `POST /validate`, the dev-bench port resolved live, each declared signal's carrier, and any enrolled name absent from the catalog. `{ok, verdict, failed, warned, checked_at_utc_ms, checks: [{id, label, status, detail, log?}]}` — `status` is `pass`/`fail`/`warn`/`empty`, **`warn` is never a pass** (`verdict`: failed/warned/empty/passed; the tab draws it, not `ok`), and `log` is Core's own words verbatim. `502` when Core is unreachable |
| `GET`/`POST` | `topology/boards` | The catalog, and an upsert by name. `POST` takes a `{name, chip, build_target, variant, revision, notes}`; both answer the whole list back |
| `DELETE` | `topology/boards/{name}` | Forgets a board. **Unenrols nothing** — a role holding it keeps the name, which then renders as *not in catalog* |
| `GET`/`POST` | `topology/profiles` | Saved benches, newest first, and a save of the bench as it stands. **A file that will not parse is listed with its error, never skipped** |
| `DELETE` | `topology/profiles/{slug}` | Deletes the file, not the bench |
| `POST` | `topology/profiles/{slug}/apply` | Declares the signals and (where dev-bench is already enrolled) the link, then returns `proposals` — one per role, each with the board, chip, probe serial, whether that probe is attached, and who it would displace. **It enrols nothing** |

## The bench editor's routes

Under `/api/bench/`, JSON shaped as the TOML files field for field (decisions 71–74). **No route here calls Core**, and **every one answers `409` with no project open, whatever the body** — the vocabulary and the built-ins included — in the Atlas and Study Designer tabs' sentence. Every refusal is plain text. A cable end is `<part>.<connector>`, or `<part>` alone for a hub.

| Method | Path | Notes |
|---|---|---|
| `GET` | `bench/vocabulary` | `{kinds, joins, hub_kind, power: {providers, consumers, either, pass}, categories, looks, functions}`: the lists a file is parsed against. A kind in no `joins` pair that is not `hub_kind` is never cabled |
| `GET` | `bench/parts` | `{parts, errors}`: the built-ins, then `embarch/parts/*.toml`, each with `source` (`builtin`/`repo`) and `version` (null for a built-in). An `errors` entry is `{file, error}`, plus `id` (the file stem) when it is about one template file |
| `POST` | `bench/parts` | One part as served (`source` ignored) creates `embarch/parts/<id>.toml`: `201` with the whole catalog. `409` for a built-in's id or anything already at the path, `400` for a template that does not check (over 64 connectors included) |
| `PUT` | `bench/parts/{id}` | Replaces it, naming the `version` it read: `200` with the catalog. `400` when the path and the body's id differ or no version is named, `404` with no such file, `409` when it changed since or does not load as a template |
| `GET` | `bench/benches` | `{benches: [{slug, name, legacy}], errors}`, newest first. An `errors` entry carries `slug` when it is about one bench file a route could address |
| `POST` | `bench/benches` | Creates the bench at the slug derived from `name`: `201` with the bench as `GET` now answers it. `409` when anything is at that path, parseable or not |
| `GET` | `bench/benches/{slug}` | `{slug, name, legacy, version, parts, cables, configs, signals}`; `signals` are `SignalLink` verbatim. A legacy file comes back laid out as parts with `legacy: true`, its file untouched. `404` when missing, `400` when it will not load |
| `PUT` | `bench/benches/{slug}` | Saves the new shape, naming the `version` read: `200` with the bench and its new `version`. `404` when missing; `409` when it changed since, does not parse (left alone), or `name` no longer derives the slug — renaming is refused |
| `POST` | `bench/check` | `{bench, config}` → `{findings: [{level, code, text, parts, cables}]}`; a null `config` checks the bench-level cables alone, and a cable is named by its two ends |
| `POST` | `bench/candidates` | `{bench, config, from}` → `{verdicts: {<end>: {fit, why?}}}` for every end on the bench, `fit` one of `ok`, `refused` (with `why`) or `hidden`. `400` when `from` is no end a cable can start at |

**Shared refusals.** `400`: a path that is not a slug (never slugified into another bench's name), a bench over a cap — 500 parts, 2,000 cables at the bench level or in one config, 100 configs, 32 USB bindings on one part — a config the bench lacks, and on a save a `usb` key that is no connector of the part's template, two parts under one id, two configs under one name, or a name with no letter or digit in it. `500`: a write whose text would not read back as what was sent, the file left as it was (decision 74).

## The canvas's asset and events

`/bench.js` is served by the binary beside `app.js`, `atlas.js` and `desk.js`, embedded and revalidated the same way, and `tests/element_ids.rs` holds it to the same two rules. It reaches `app.js` through document events, never a second stream (decision 77):

| Event | Sent by `app.js` | `detail` |
|---|---|---|
| `embarch:snapshot` | on every snapshot it renders | the snapshot as the SSE frame carries it |
| `embarch:verdicts` | after a Validate pass, and whenever a verdict is dropped | `{roles: {<role>: {status, text}}, boards: {<probe serial>: {status, text}}}` |
| `embarch:benches-changed` | after a save or delete on the Saved benches panel | none: the canvas re-reads the list, keeping the bench on screen |
| `embarch:project` | on a project switch (older than the canvas) | `{path}`: the canvas reloads everything |
