# embarch-ui interfaces: the bench editor's routes, assets and events

**Status:** active, 2026-11-02.

Moved verbatim from [topology.md](topology.md) on 2026-11-02, when making a bench live, documented there, would have put that file over its cap; phase 4's events and globals are new, and phase 5 added to both. Why: [../decisions/bench-model.md](../decisions/bench-model.md), [../decisions/bench-editing.md](../decisions/bench-editing.md), [../decisions/part-editor.md](../decisions/part-editor.md), [../decisions/bench-live.md](../decisions/bench-live.md). Index: [../interfaces.md](../interfaces.md).

## The bench editor's routes

Under `/api/bench/`, JSON shaped as the TOML files field for field (decisions 71–74). **No route here calls Core** — making a bench live, under the same prefix, is [topology.md](topology.md)'s — and **every one answers `409` with no project open, whatever the body** — the vocabulary and the built-ins included — in the Atlas and Study Designer tabs' sentence. Every refusal is plain text, and a `409` also names which it is in `x-embarch-refusal` (below). A cable end is `<part>.<connector>`, or `<part>` alone for a hub.

| Method | Path | Notes |
|---|---|---|
| `GET` | `bench/vocabulary` | `{kinds, power_kinds, sides, joins, hub_kind, power: {providers, consumers, either, pass}, categories, bench_board_categories, looks, functions, roles, interface_functions, line_functions, template, config_name}`: the lists a file is parsed against, and the rules between its fields — the kinds that take a power role, the functions that take an interface or line facts. `template` is `{max_connectors, numbers: {<field>: {min, max}}, line_facts: [{name, numeric}]}`, the limits a template file is held to (decision 88). `bench_board_categories` are the categories whose role-less part is a bench board, offered a board type (decision 86); `config_name` is `{max_bytes, refused, refused_at_ends, rule}` — the UTF-8 byte cap, code-point runs as `[first, last]` refused anywhere and only at the ends, and the sentence a save refuses in (decision 97). A kind in no `joins` pair that is not `hub_kind` is never cabled |
| `GET` | `bench/parts` | `{parts, errors}`: the built-ins, then `embarch/parts/*.toml`, each with `source` (`builtin`/`repo`) and `version` (null for a built-in). An `errors` entry is `{file, error}`, plus `id` (the file stem) when it is about one template file |
| `POST` | `bench/parts` | One part as served (`source` ignored) creates `embarch/parts/<id>.toml`: `201` with the whole catalog. `409` for a built-in's id or anything already at the path, `400` for a template that does not check (over 64 connectors included), naming a refused field by its path, `connectors[0].functions[0].interface` |
| `PUT` | `bench/parts/{id}` | Replaces it, naming the `version` it read: `200` with the catalog. `400` when the path and the body's id differ or no version is named, `404` with no such file, `409` when it changed since or does not load as a template |
| `GET` | `bench/benches` | `{benches: [{slug, name, legacy}], errors}`, newest first. An `errors` entry carries `slug` when it is about one bench file a route could address |
| `POST` | `bench/benches` | Creates the bench at the slug derived from `name`: `201` with the bench as `GET` now answers it. `409` when anything is at that path, parseable or not |
| `GET` | `bench/benches/{slug}` | `{slug, name, legacy, version, parts, cables, configs, signals}`; `signals` are `SignalLink` verbatim. A legacy file comes back laid out as parts with `legacy: true`, its file untouched. `404` when missing, `400` when it will not load |
| `PUT` | `bench/benches/{slug}` | Saves the new shape, naming the `version` read: `200` with the bench and its new `version`. `404` when missing; `409` when it changed since, does not parse (left alone), or `name` no longer derives the slug — renaming is refused |
| `POST` | `bench/check` | `{bench, config}` → `{findings: [{level, code, text, parts, cables}]}`; a null `config` checks the bench-level cables alone, and a cable is named by its two ends |
| `POST` | `bench/candidates` | `{bench, config, from}` → `{verdicts: {<end>: {fit, why?}}}` for every end on the bench, `fit` one of `ok`, `refused` (with `why`) or `hidden`. **From a stack plug, where its part may be mounted instead**: each stack socket on another part `ok` or `refused` (its board full, or a ring), everything else `hidden` (decision 81). `400` when `from` is no end a cable can start at |

**Shared refusals.** `400`: a path that is not a slug (never slugified into another bench's name), a bench over a cap — 500 parts, 2,000 cables at the bench level or in one config, 100 configs, 32 USB bindings on one part — a config the bench lacks, and on a save a `usb` key that is no connector of the part's template, two parts under one id, two configs under one name, a config name no host study could write (in `config_name`'s sentence, decision 97), or a name with no letter or digit in it. `500`: a write whose text would not read back as what was sent, the file left as it was (decision 74).

**Which `409`.** `x-embarch-refusal` carries a word beside the sentence: `no-project` (every route), `exists` (`POST` parts and benches), `builtin-id` (`POST` and `PUT` parts), `version-changed` and `unparseable` (`PUT` parts and benches), `rename` (`PUT` benches). Only `version-changed` is cured by reading the file again, so it is the only one the editor answers with Reload (decision 80).

## The bench editor's assets and events

`/bench.js` (the canvas) and `/bench-parts.js` (the part editor, loaded after it, which a test checks) are served by the binary beside `app.js`, `atlas.js` and `desk.js`, embedded and revalidated the same way, and `tests/element_ids.rs` holds both to the same two rules. They reach `app.js` and each other through document events, never a second stream (decision 77):

| Event | From → to, when | `detail` |
|---|---|---|
| `embarch:snapshot` | `app.js` → canvas, on every snapshot it renders | the snapshot as the SSE frame carries it |
| `embarch:verdicts` | `app.js` → canvas, after a Validate pass and whenever a verdict is dropped | `{roles: {<role>: {status, text}}, boards: {<probe serial>: {status, text}}, pass}`; `pass` is new per pass and unchanged while a verdict is merely dropped (decision 85) |
| `embarch:benches-changed` | `app.js` → canvas, after a save or delete on the Saved benches panel | none: the canvas re-reads the list, keeping the bench on screen and its unsaved edits |
| `embarch:project` | `app.js` → canvas and part editor, on a project switch (older than the canvas) | `{path, initial}`: the canvas reloads everything; `initial` marks the page's first read, which is no switch |
| `embarch:bench-saved` | canvas → `app.js`, after a save or a new bench | `{slug}`: the Saved benches list re-reads |
| `embarch:edit-part` | canvas → part editor, from the bin's *Edit* and *New part…* | `{id}`, null for a new part |
| `embarch:parts-changed` | part editor → canvas, after every save | `{id, file}`: the canvas re-reads the catalog |
| `embarch:live-changed` | canvas → any listener, after a make-live, a re-apply, a config recorded or Stop being live; `app.js` → canvas, after the operator prompt marks a config | `{slug, config}`, both null when no bench is live here now (decision 93); the prompt's carries `source: "prompt"`, on which the canvas reads the record again (decision 99) |
| `embarch:role-changed` | canvas → `app.js`, after a Confirm, a retracted role, or a make-live row changing a role's board type or the link | `{role, probe_serial}`: Validate's verdict on that role is dropped, or with `role` null the bench board's on that probe (decision 93) |
| `embarch:boards-changed` | `app.js` → canvas, whenever Board types renders the catalog | none: the inspector's pickers are read again |
| `embarch:boards-pinned` | canvas → `app.js`, after *Build as* writes a pin | `{board}`: the catalog list re-reads (decision 86) |
| `embarch:bench-marked` | canvas → `app.js`, after it marks what a `#topology?board=` link names, or a load settles | `{count}`: whether Board types opens (decision 94) |

**Two globals, each feature-detected by its caller.** `window.embarchBench`: `previewTemplate(svg, template)`, a pure draw with the canvas's renderer that touches nothing the canvas holds; `unsaved()`, the bench's edits or the part draft; `confirmLeave(what)`, a promise of whether they may go, `what` one of `tab`, `project`, `desk`, `bench`; `leaveDone(ok)`, whether the switch it was asked for happened (decision 84); and since phase 4 `markedParts(board)`, the parts a board link marks, `settled()`, whether a load has finished so that none means none, and `showBench(slug, why)`, Saved benches' Open and the desk banner putting a bench on the canvas (decisions 90, 94); and since phase 5 `configChange(bench, from, to, catalog)`, the cables to unplug and to plug between two configs by part and connector label, and `previewChange(svg, bench, from, to, catalog)`, that change drawn with the canvas's renderer, both pure, for the operator prompt (decision 99). `window.embarchParts`: `unsaved()`, and `discard()`, closing a draft the leave guard already asked about.
