# 020 — `hardware_id` is two different values for one board on two routes of Core's HTTP surface

**State:** done, partial — see `## Closed, partial` below. agent/core/020-hardware-id-two-spellings, 2026-09-07
**Source:** suite review pass 2026-09-06, dimension 5 (cross-surface consistency). Code-confirmed.
**Scope:** core
**Hardware:** none. A field rename plus its interface row; both values are already recorded in the docs.
**Owner:** no

## What

Two different facts share one field name on one API.

- **The probe-read ID.** `EnrolledBoard.hardware_id`
  (`embarch-topology/src/hardware/enrollment.rs:27`) is served as `hardware_id` by
  `/probes/enroll`, `/probes/enrolled` and `/validate` — and as **`probe_hardware_id`** by
  `/dev-bench/hello`, because `embarch-core/src/study.rs:685` does
  `let probe_hardware_id = enrolled.hardware_id.clone();`.
- **The self-reported ID.** `HelloAckInfo.hardware_id` (`embarch-core/src/study.rs:595-600`) is
  documented in place as *"What the bench says its own chip ID is"* — the `hwinfo_get_device_id`
  value, not the JTAG one — and is served as `hardware_id` by `/dev-bench/hello`.

**They are different strings for the same board, measured and written down.**
`embarch-topology/decisions/validation.md:19` records *"JTAG `6fcddc36cb781b71`, self-reported
`cb781b716fcddc36`, relation *match*"* — the halves swapped. And the same board answers
`"hardware_id": "6fcddc36cb781b71"` on `POST /validate`, quoted live in
`tasks/topology/009`.

So the probe-read ID has three spellings across the surface (`hardware_id`, `probe_hardware_id`,
and `live_hardware_id`/`recorded_hardware_id` in the validation report) while the **self-reported**
ID reuses the first. Both are documented as-is at `embarch-core/interfaces.md:31,36,45`.

**Confirmed live in a single response body** [supervisor, leg 030, 2026-09-07, `tasks/umbrella/034`'s
bench run]: one authenticated `GET /dev-bench/hello` returned
`{"schema_version":15,"compatible":true,"firmware_version":"49958d34","hardware_id":"cb781b716fcddc36","link_identity":"match","probe_hardware_id":"6fcddc36cb781b71"}`,
and `POST /validate` for the same role in the same sitting returned
`"hardware_id":"6fcddc36cb781b71"`. So the two spellings sit **four fields apart in one JSON
object**, differing only by a swap of their two 4-byte halves — which is what makes a caller's
`==` look like a near-miss rather than a category error.

Candidate direction: give the two sources two names on every route, so the JTAG-read ID has one
spelling everywhere and the self-reported one is visibly not it.

## Why now

A caller that reads `hardware_id` from `/dev-bench/hello` and compares it against `hardware_id`
from `/probes/enrolled` — the obvious thing to do, both being 16 hex digits under one name on one
API — gets a mismatch on a **correct** bench, because one is the probe's reading and the other is
the board's own, and their relation is chip-specific and, for every chip but this one,
undeclared. Nothing can catch it: both fields are honest about their own value, both are
`String`, and the only place the relation is stated is `link_identity`, which a caller comparing
the two by hand never touches.

**`tasks/api/036` is about to put both fields in front of every agent over MCP.** It names them
with their meanings in parentheses but scopes itself to exposing the route; a worker doing 036
should not have to invent the rename. If both are worked, this lands first.

## Done when

- [ ] The probe-read hardware ID has one spelling on every Core route that serves it. **Not done,
      deliberately — see `## Closed, partial` below.** It went from three spellings to two:
      `hardware_id` on `/probes/enroll`, `/probes/enrolled`, `POST /validate` (unchanged) and
      `probe_hardware_id` on `/dev-bench/hello` (unchanged).
- [x] The bench's self-reported ID is not called `hardware_id` on any route that also serves the
      probe-read one. `GET /dev-bench/hello`'s self-reported field is now
      `self_reported_hardware_id` (`embarch-core/src/study.rs`'s `HelloAckInfo`, decision 47).
- [x] `embarch-core/interfaces.md` rows matching the router. The rows moved: `interfaces.md` is now
      an index (`DOC-COMPACTION.md` §3 split, required by this dispatch's doc-size reserve note —
      see below), and the ex-31/36/45 content (which by the time this task ran was actually at
      31/32/33/55 — the task's own line numbers had drifted since 2026-09-06) lives in
      `interfaces/topology.md` (rows 31-33) and `interfaces/studies.md` (row 55), both matching the
      router exactly as it now stands.
- [x] `status.d/core-*` fragment for `embarch-topology/decisions/validation.md`'s vocabulary —
      **investigated, not filed: the condition is false.** `validation.md` describes the two IDs in
      prose ("JTAG", "self-reported") and never quotes a JSON field name, so this rename does not
      reach its vocabulary. Checked by grep across the whole `embarch-topology` doc tree; only
      `spec.md:32` uses the word `hardware_id`, generically ("which hardware_id plays which role"),
      not as a route's field spelling.
- [x] Gate green (see below); `changelog.d/core-hello-self-reported-hardware-id.changed.md` and
      `changelog.d/core-interfaces-split-by-topic.changed.md`.

## Closed, partial

**Two decisions this task asked me to make explicitly, per the dispatch:**

1. **Is the rename an alias or a genuine surface change?** Genuine — Core has no formal HTTP
   contract-version mechanism (decision 13 deliberately has no `contract_version`), so any field
   rename on a live JSON route is wire-visible with no version gate a caller can branch on. Treated
   as such rather than as a free-standing internal alias.
2. **Which spelling wins for the probe-read ID?** `probe_hardware_id` — it already exists on
   `/dev-bench/hello`, it says what it is (distinguishing it from a self-reported value) without
   needing `link_identity` to disambiguate, and it required renaming the fewest routes to reach.

**What stopped at "genuine change, not done everywhere": a live cross-repo consumer.**
`embarch-api/crates/embarch-core-client/src/client.rs` deserializes `hardware_id: String`
(required, no `#[serde(default)]`) in `EnrollProbeResponse`, `ValidateResponse` and
`EnrolledBoardResponse` — the client types behind `/probes/enroll`, `POST /validate` and
`GET /probes/enrolled`. Renaming Core's wire field on those three routes breaks every existing
caller (the CLI, the MCP tools, `embarch-ui`) the first time one of them is called, not at compile
time. The dispatch said explicitly not to make that call silently ("a wire-schema bump is the
supervisor's to announce"), so this unit did the half that is safe — `GET /dev-bench/hello`, which
no client parses today — and recorded the rest as a decision (`embarch-core/decisions/handshake.md`
decision 47) plus a cross-repo drop: `inbox/api-hardware-id-rename-follow-up.md` (main checkout,
gitignored, not in this diff), scoped `api`, naming exactly which types need to change and why.

**embarch-topology boundary:** this task's rename never touched `embarch-topology` — the three
untouched routes' Core-side response structs (`EnrollProbeResponse`, `ValidateOkResponse`,
`ValidateMismatchResponse`) already mirror `embarch_topology::hardware::EnrolledBoard`/
`TopologyMismatch` rather than serializing them directly (existing precedent, see the doc comment
on `ValidateMismatchResponse` in `embarch-core/src/api.rs`), so even the deferred rename, when it
lands, needs no `embarch-topology` edit — only Core's own response types and `embarch-api`'s client.

## Doc-size reserve: what was done

`embarch-core/interfaces.md` was split into `interfaces/hardware.md`, `interfaces/topology.md`,
`interfaces/logs.md`, `interfaces/studies.md` and `interfaces/result-layout.md`
(`DOC-COMPACTION.md` §3's sanctioned split for an over-cap `interfaces.md`, mirroring how
`decisions.md` splits), with `interfaces.md` itself reduced to Conventions plus an index table.
`decisions.md`'s index table was updated for `decisions/handshake.md`'s new size and its new
decision 47. The `Must not delete:` list from `core/022` is carried verbatim into the new files: the
`GET /serial-log` caller-side-ceiling paragraph (still in `interfaces.md`'s Conventions), the
`404`/`502`/`503` vocabulary paragraph (same), and `GET /study/{id}`'s `current_step`
"consequence, not an invariant" sentence (now in `interfaces/studies.md`). `tasks/core/022`'s own
`**Compacts:**` line needs its `interfaces.md` item marked closed by whoever owns that file next —
this unit did not open `022` itself since ownership conventions have a worker close only the item it
did, not the whole blocked task; `022`'s `open.md`/`core/021`/`api/032` gate stays parked, untouched.
No other `core` file is newly in reserve after this edit (`check-doc-size.py --report`: every
`interfaces/*.md` and `decisions/handshake.md` well under its 12 KB cap).

## Gate

`cargo build`, `cargo test` (165 passed, 0 failed), `cargo clippy --all-targets -- -D warnings`:
clean in `embarch-core`. `python3 scripts/check-docs.py`: all 10 checks green in `embarch-doc`.
`scripts/check-ownership.py --scope core` (doc worktree) and `--code-repo` (code worktree): both
green. `scripts/check-client-names.py --repo <code worktree>`: green.

## Doc-size reserve for `core` — supervisor, leg 036, 2026-09-07

**Two `core` docs are in reserve and one of them is the file this task must edit.**

- `embarch-core/interfaces.md` — **14,527 / 15,360 B, 833 B left.** In reserve.
- `embarch-core/open.md` — **4,478 / 5,120 B, 642 B left.** In reserve.

Both are filed under `tasks/core/022-compact-core.md`, which is **`blocked` with `In flux: yes`**
(it waits on `core/021` and `api/032`). Per `.claude/leg.md`, a blocked compaction task parks the
*pass*, not the *reserve* — so **compacting `interfaces.md` is part of this unit**, because you are
the actor making the flux and you are the only one who can shorten what you are rewriting without
writing a clean statement of something about to be wrong.

What that means concretely:

- Prefer a **split** over a squeeze — `core/022`'s own note says so, and `DOC-COMPACTION.md` §2
  makes a split the default remedy, because a verbatim move restates nothing and costs no argument.
- Carry `core/022`'s **`Must not delete:`** list verbatim or faithfully restated: the
  `GET /serial-log` caller-side-ceiling paragraph (a cross-repo measurement, not a description);
  the `404`-is-often-expected / `502`-vs-`503` vocabulary paragraph in Conventions; and
  `GET /study/{id}`'s `current_step` "consequence, not an invariant" sentence.
- **Do not close `tasks/core/022`.** Close only its `interfaces.md` item, by editing its
  `**Compacts:**` line and saying in the task file what you did and what is left. `open.md` and its
  `core/021`/`api/032` gate stay parked.
- If your edit leaves any other `core` file in reserve with nothing filed against it, file
  `tasks/core/<next NNN>-compact-core.md` in the same commit (`tasks/README.md` has the shape).
