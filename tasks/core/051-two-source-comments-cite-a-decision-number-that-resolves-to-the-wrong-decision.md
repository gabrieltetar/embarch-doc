# 051 — Two source comments cite a decision number that resolves to the wrong decision, and `interfaces/logs.md` still says "both routes"

**State:** claimed — leg 111, 2026-09-13, `agent/core/051-wrong-decision-citations`
**Source:** leg 111's refill sweep — a read-only hunter over `embarch-core`, run because
`--refill-owed` fired on scope spread and every remaining `open.md` bullet is a hardware debt or a
deferred-with-named-trigger. Every finding below was verified against both sides before filing.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Three things, two of them the expensive class: **a decision number that is wrong and still
resolves.** `scripts/check-decision-refs.py` walks `*.md` in `embarch-doc` only — it never reads
`src/**` — so a Rust comment citing a live-but-wrong number fails nothing, renders in `cargo doc`,
and reads as authoritative.

### 1. `src/study.rs:3724` cites `§3 decision 18`; the rule is decision 39

The doc comment on `validate_study_rejects_a_run_protocol_step_naming_a_protocol_that_is_not_there`
says "*§3 decision 18's rule is that Core names the specific failure rather than letting a raw index
fail*". **The same file gets it right 3,456 lines earlier**: `src/study.rs:266-269` carries the
identical sentence citing `decision 39`. Decision 39 (`embarch-core/decisions/streams.md`) is "the
third pre-flight seal, and the two indices a manifest cannot check about itself", and its body names
exactly this case — a `RunProtocol`'s protocol index and entry state. Decision 18
(`embarch-core/decisions/flashing.md`) is "10, 18 — Multipart upload, and `Format::Bin` at the merge
address", which has nothing to do with index validation.

### 2. `src/api.rs:690` cites `§3 decision 15`; 15 is the `study_lock` decision

The doc comment on `EnrollProbeRequest::probe_serial` attributes the `/enroll` drag-and-drop UI's
always-sending-a-serial behaviour to `§3 decision 15`. Decision 15 lives in
`embarch-core/decisions/platform.md` under "4, 14, 15 — One `hw_lock`, `study_lock` for the bench,
and a `503` naming the holder on contention" — lock arbitration, not the enroll page.

**Do not take a replacement number on trust.** The hunter's candidate is decision 25
(`embarch-core/decisions/enrollment.md`, "`GET /enroll`, a static page served by Core (retired
2026-08-24, see `embarch-ui` decision 1)"), and `src/api.rs:128-131` in the same file already cites
that page correctly via `embarch-ui` decision 1. But **the hunter also checked and could not find
the "drag-and-drop" detail anywhere in `embarch-doc`** — `grep drag` returns only `embarch-ui`
trace-chart hits. So 25 is the enroll-surface entry and does not itself describe drag-and-drop.
Read 25 and `embarch-ui` decision 1 in full and decide what the sentence should actually cite; if
the honest answer is that no decision records the drag-and-drop behaviour, **say so and reword the
comment to claim only what a decision supports**, rather than pointing it at the nearest entry.

### 3. `embarch-core/interfaces/logs.md:7` says "both routes"; there is one route

"*The CLI's `logs` subcommand is one implementation behind both routes.*" `src/api.rs:150` is the
only `/logs*` registration in `build_router` and there is no `/logs/stream`. **The same file
contradicts itself twelve lines down** (`logs.md:13`: "`GET /logs/stream`, a live-tail SSE
counterpart, was retired (`tasks/core/021`)"), and its own table carries one row.

## Also do

Both wrong citations use the **legacy `§3 decision N`** form, which `DOC-CONVENTIONS.md` records as
"still parses, unmaintained", and which `embarch-dev-bench` decision 47 rules against because it
names no document. While you are in these two comments, write the current form. **Do not sweep every
`§3 decision` in the repo as part of this unit** — that is a different, larger task, and if you
think it is worth doing, file it rather than doing it.

## Done when

- [ ] `src/study.rs:3724` cites decision 39 in the current citation form, re-derived by you from
      decision 39's own body rather than from this task file.
- [ ] `src/api.rs:690` either cites a decision whose body actually supports the sentence, or the
      sentence is reworded to claim only what is supported. Say in your report which you did and why.
- [ ] `embarch-core/interfaces/logs.md:7` no longer claims two routes.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.
