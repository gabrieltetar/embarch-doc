# embarch-ui interfaces: the Topology tab's routes

**Status:** active, 2026-11-01.

The first section moved verbatim from [../interfaces.md](../interfaces.md) on 2026-11-01, when the bench editor's routes would have put that file in its reserve; phase 4 amended five of its rows. The bench editor's file routes, assets and events moved on to [bench.md](bench.md) on 2026-11-02, when making a bench live, below, would have put this file over its cap; phase 5 added the record-only config route. Why: [../decisions/topology-boards.md](../decisions/topology-boards.md), [../decisions/saved-benches.md](../decisions/saved-benches.md), [../decisions/bench-live.md](../decisions/bench-live.md). Index: [../interfaces.md](../interfaces.md).

## The Topology tab's own routes

Two kinds, and the split is the point (decision 44). `/api/enroll`, `/api/signals`, `/api/enrolled/{role}` and `/api/topology/link` are **proxies**: the write is Core's, and this binary holds the bearer token so the browser never sees it. The rest read and write **project files** in the open firmware repo — `embarch/boards.toml` and `embarch/topologies/` — and answer `409` with the way out when no project is open, since the catalog is not missing, it is unanswerable.

| Method | Path | Notes |
|---|---|---|
| `POST` | `enroll` | `{role, chip, probe_serial?, name?}` → Core's `POST /probes/enroll`. Binds the **probe** half of a role and reads an identity through it; `chip` and `name` come from the board *type* already in that role (45), not from anything typed. Its page caller is the live report's Confirm (decision 90) |
| `POST` | `topology/roles/{role}/board` | `{board, chip}` → Core's `PUT /probes/enrolled/{role}/board`. The **board** half: which board type is in the role. **Opens no probe**, works with nothing plugged in, and leaves any recorded hardware ID alone so a validate pass can disagree with it. No page caller since phase 4 (decision 94) |
| `GET` | `topology/pickers` | What each role's board picker offers: `dut` from the open project's catalog, `dev-bench` from the suite's supported pair, each `{board, label, chip}`. **Served, never restated in `app.js`** |
| `POST` | `topology/boards/rescan` | Merges the west targets this repo builds for into the catalog. **Only ever adds**: an entry already in the file keeps every field, and one the scan does not find is reported in `not_in_scan` and kept, since a repo builds for boards on branches that are not checked out |
| `DELETE` | `enrolled/{role}` | → Core's `DELETE /probes/enrolled/{role}`. `404` when nothing held that role. Takes a role outside the pair on purpose: clearing exactly those is what it is for |
| `POST` | `topology/link` | `{serial?, interface?}` → Core's `POST /dev-bench/link`. No page caller since phase 4: making a bench live declares the link (decision 90) |
| `POST` | `topology/validate` | One pass: each role through Core's `POST /validate`, the dev-bench port resolved live, each declared signal's carrier, and any enrolled name absent from the catalog. `{ok, verdict, failed, warned, checked_at_utc_ms, checks: [{id, label, status, detail, log?}]}` — `status` is `pass`/`fail`/`warn`/`empty`, **`warn` is never a pass** (`verdict`: failed/warned/empty/passed; the tab draws it, not `ok`), and `log` is Core's own words verbatim. `502` when Core is unreachable |
| `GET`/`POST` | `topology/boards` | The catalog, and an upsert by name. `POST` takes a `{name, chip, build_target, variant, revision, notes}`; both answer the whole list back. `POST` is also the inspector's *Build as* (decision 86) |
| `DELETE` | `topology/boards/{name}` | Forgets a board. **Unenrols nothing** — a role holding it keeps the name, which then renders as *not in catalog* |
| `GET`/`POST` | `topology/profiles` | Saved benches, newest first, and a save of the bench as it stands. **A file that will not parse is listed with its error, never skipped** |
| `DELETE` | `topology/profiles/{slug}` | Deletes the file, not the bench |
| `POST` | `topology/profiles/{slug}/apply` | Declares the signals and (where dev-bench is already enrolled) the link, then returns `proposals` — one per role, each with the board, chip, probe serial, whether that probe is attached, and who it would displace. **It enrols nothing.** The page no longer calls it; kept for API callers (decision 90) |

## Making a bench live

Under `/api/bench/`, beside the editor's file routes ([bench.md](bench.md)), and **the one place a bench reaches Core** (decisions 90–93) — all but `bench/live/config`, which records and calls nothing (98). Every route answers `409` `no-project` with no project open and names each `409` in `x-embarch-refusal`. A bench file that cannot be read (an I/O error) is a `500` with its reason everywhere, never a state of the file; so is a record file that will not read or parse, and a UI with no per-user data directory, whose sentence says to set `EMBARCH_UI_STATE`.

| Method | Path | Notes |
|---|---|---|
| `GET` | `bench/live` | `{live, superseded}`. `live` is this repo's last live bench or null: `{slug, config, since_utc_ms, missing, config_missing, unparseable}` — its file gone, its config gone from the file, the file not parsing. `superseded` is `{repo, slug, config}` once another repo went live after it, naming the repo holding the machine now; this repo's bench is then not live, and a save does not write through |
| `POST` | `bench/benches/{slug}/live` | `{config, version, write_through}` → `{live, applied, proposals, not_proposed, leftovers}`. Reads the bench as saved at `version`; a null `config` counts the bench-level cables alone. `write_through: false` is an explicit make-live and takes the machine; `true` re-applies only this repo's live bench and config |
| `POST` | `bench/live/retract` | `{kind, id}` → `{ok, text, leftovers}`, the list recomputed. Only what the current list offers; `ok: false` and nothing retracted when Core did not answer the read for that kind |
| `POST` | `bench/live/config` | `{config, slug, renamed_from?}` → `{live, superseded: null}`, as `GET` answers. **Records which config the live bench is wired as, and calls nothing in Core** (decision 98). `config` is a config of the bench as saved, or null for the bench-level cables alone; `slug` the bench the caller believes is live; `renamed_from` the old name of a rename just saved, which keeps `since_utc_ms` when the record names it and the bench no longer has it |
| `DELETE` | `bench/live` | `204`. Clears this repo's entry, and the machine's only when it points here. **Touches nothing in Core** |

**Refusals.** Making live: `400` with no `write_through`, no `version`, or a config the bench lacks; `404` for no such bench; `409` `version-changed`, `unparseable`, `config-missing` (the record's own config, gone from the bench: make one it has live) and, for a write-through only, `not-live` (not this repo's live bench), `superseded`, `config-differs` (another config than the record's, `null` against one included). Retracting: `409` `not-live` (no record, or its file gone), `unparseable`, `superseded`, `config-missing`, `not-offered`. Recording a config: `400` with no `config` or no `slug`; `409` `not-live` (no record, its file gone, or `slug` another bench), `superseded`, `unparseable`, `config-missing` (the bench as saved lacks it).

**The report.** An `applied` row is `{what, route, ok, text}`, `text` Core's own words on a refusal. `route` is the Core route; `(not sent)` for what was not declared and why — a template that would not load, a part whose template is missing, a binding on a connector that does not carry it, a bootload binding on a part not holding `dut`; `GET /probes/enrolled` for Core's board type or dev-bench link differing from the bench; the read's own route, `GET /signals` and the like, for a Core read that failed; `(this UI)` when the record was not written. A proposal is `{kind: "enroll", role, name, chip, probe_serial, part, text}`, `role` null for a bench board; the page sends `role` (`""` for null), `chip`, `probe_serial` and `name` to `/api/enroll` as they are. A row not proposed is `{part, text}`, and a leftover `{kind, id, text}`:

| `kind` | `id` | Retract calls Core's |
|---|---|---|
| `signal` | its name | `DELETE /signals/{name}` |
| `instrument` | its name | `DELETE /instruments/{name}` |
| `bench-board` | its probe serial | `DELETE /probes/by-serial/{serial}` |
| `role` | the role | `DELETE /probes/enrolled/{role}`, then the bench's board type written back, and dev-bench's link |
| `bootload` | the pair's role | `DELETE /bootload/ports` |

**The record** is `live-benches.json` under the per-user data directory's `ui/`, or in the directory of the file `EMBARCH_UI_STATE` names: `{repos: {<canonical repo path>: {slug, config, since_utc_ms, superseded_by?}}, machine: {repo, slug, config, since_utc_ms} | null}`, read strictly. A re-apply of the same bench and config keeps its `since_utc_ms`, and so does recording the config already live, or a rename.
