# 153 — Core keeps a service store or a development store, and says which

**State:** open
**Source:** EMB-323 — Core has one store whatever runs it, so service and development share it
**Issue:** EMB-323
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`token_store::local_data_dir()` is Core's only root. It holds the token pair,
`signing-key`, `run-log.jsonl`, `call-log.jsonl`, `logs/`, `study_results/`
and, through `embarch-topology`, `topology/enrollment.toml`. `GET /status`
gives the version, binary hash, probes, lease and `last_images`, but no mode
and no key. The HIL design (`embarch-doc/notes/hil/12-prevention.md`, "The root
of trust") gives the attested Core a protected store only its own account can
open, and a development Core a store and token pair of its own, each Core's
status saying `service` or `development` with its key fingerprint. When this is
done:

- **`run --service`**: the store is `<data dir>/store/`, and Core never creates
  it; a missing store is a start failure naming the elevated install. It holds
  `signing-key`, `public-key` (the raw public key in hex, written when the key
  is created), `run-log.jsonl`, `call-log.jsonl` and the identity store
  (`<store>/topology/`, through `embarch-topology`'s existing
  `hardware::paths::set_data_dir`). The token files and `study_results/` stay
  in `<data dir>`.
- **`run --store <dir>`**: all of the above plus the token pair and
  `study_results/`, inside `<dir>`, created if missing. This is the
  development Core.
- **Neither flag**: today's layout exactly, so a source-installed service runs
  unchanged until the first signed install.
- **`GET /status`** gains `mode` (`service` with `--service`, else
  `development`), `keyid` and `study_in_flight` (the study id, or null). The
  challenge answer carries `mode` beside its signature, unsigned: it is Core's
  own word. The signed record's `observed` gains `mode`.
- `install` is not changed here.

Where: `src/token_store.rs` (`local_data_dir`, the token paths),
`src/signing.rs` (`signing_key_path`, `CoreKey::load_or_create`, the challenge
answer), `src/run_log.rs` (`resolve`), `src/call_log.rs`, `src/study.rs` (the
results root), `src/main.rs` (`Run`, `serve`), `src/api.rs`
(`StatusResponse`). `embarch-topology`'s setter already exists; this task does
not edit that repo. If it turns out it must, stop and say so here.

## Why now

EMB-323, unit A.4 of the HIL attested phase
(`embarch-doc/notes/hil/14-implementation-plan.md`, "The Test and attested
phases"). The elevated install, `deploy-core`'s development Core, the client's
token-pair choice, the report naming its Core and the identity routes all key
on this mode. The shape is the plan's recommendation; the owner may strike it
later.

**A new numbered decision is yours to write.** Amend decision 53
(`decisions/auth.md`) with a dated pointer to it, and update spec §3 and
`interfaces/signing.md`. **Do not grow decision 110** (`decisions/signing.md`):
it is already 2,486 B over its per-decision limit. Put the new decision in
`auth.md` or a new topic file, not in `signing.md`. `decisions/lease.md`
(decision 93) has 35 B left and `decisions/run-log.md` (111) 120 B: leave both
alone.

No file is in reserve on the size ledger at dispatch.

## Done when

- [ ] `run --service` with no store refuses to start, naming the elevated
      install; with one, every file listed above is read and written inside
      it, and nothing else but the token files and `study_results/` under
      `<data dir>`.
- [ ] `run --store <tmp>` keeps its own token pair, key, logs and results in
      `<tmp>`; two such Cores have different keys.
- [ ] With neither flag, every path is today's and the existing tests pass.
- [ ] `/status` and the challenge answer carry `mode` and `keyid`;
      `public-key` hashes to `keyid`; `study_in_flight` names a running study.
- [ ] The Windows-gated parts type-check with
      `cargo check --target x86_64-pc-windows-msvc`
      (`embarch-dev-workflow.md` §4); the native Windows build stays a debt in
      this file for the owner.
- [ ] A new decision; spec §3, `interfaces/signing.md` and decision 53
      amended.
- [ ] Gate green; `changelog.d/` fragment dropped; `status.d/` fragment for
      anything suite-level it made false.
