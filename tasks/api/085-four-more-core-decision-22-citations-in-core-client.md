# 085 — Four more `embarch-core` decision 22 citations in `embarch-core-client`, untouched by 084

**State:** done — leg 108, unit 1, 2026-09-13, branch `agent/api/085-core-decision-22-citations`.
**Doc-size reserve for `api`:** `embarch-api/decisions/surface.md` 11258/12288 B (**1030 B left**,
filed as blocked `tasks/api/069`) and `embarch-api/spec.md` 9090/10240 B (1150 B left, filed as
blocked `tasks/api/083`). This task should need no new decision — it is citation text in doc
comments — but if you conclude one is owed, check `embarch-api/decisions.md`'s index and pick the
right topic file rather than the nearest one. If you push any `api` doc into reserve, file
`tasks/api/<NNN>-compact-api.md` in the same commit.
**Source:** `tasks/api/084`'s own worker report, filed to `inbox/` by leg 107 and taken into the
queue by leg 108 (2026-09-13). Found while fixing the `known_boards`/decision-22 pair that `084`
named at three sites, none of which this one includes.
**Scope:** api
**Hardware:** none — doc comments in Rust source. No behaviour, no wire, no board.
**Owner:** no

## What

`embarch-core` decision 22 says its own mechanism (the probe/board identity gate and its storage
table) was "moved wholesale into `embarch-topology`"; the current entry is `embarch-topology`
decision 14 (`embarch-topology/decisions/enrollment.md`). `tasks/api/084` fixed three sites that
paired this stale decision number with the pre-`embarch-topology` name `known_boards`
(`src/main.rs:320-322`, `src/tools.rs:389`,
`crates/embarch-core-client/src/client.rs:188-192`), matching `src/tools.rs:945`'s already-correct
MCP tool description.

Four more `` `embarch-core` decision 22 `` citations remain in
`crates/embarch-core-client/src/client.rs`, at lines 199, 381, 1249 and 1333 — doc comments for
`EnrollProbeRequest::probe_serial`, `EnrolledBoardResponse`, `CoreClient::enroll_probe` and
`CoreClient::list_enrolled` respectively. **None of these pairs the stale decision number with
`known_boards` wording** — they cite the HTTP routes `POST /probes/enroll` / `GET /probes/enrolled`
directly — which is why `084` did not treat them as "the same stale pair" its `Done when`
enumerated.

**This is not a find/replace.** Whether each should now read `embarch-topology` decision 14 (the
storage/enrollment-mechanism entry) or is legitimately citing `embarch-core` decision 22 as the
historical origin of the HTTP *route* — which stayed in `embarch-core` when the storage moved —
needs a read of each site in context. Read both decision bodies in full before deciding, and say
per site which you chose and why. A citation that resolves to the wrong decision is exactly the
defect this task exists to close, and repointing a correct one re-creates it in the other
direction.

**`embarch-core-client` is a shared crate** — it lives inside `embarch-api` but `embarch-ui`
path-depends on it. This change is comment-only, so nothing consumers rely on moves; keep it that
way.

## Why now

Found as a side effect of `084`'s grep-parity check, not from a fresh sweep — real, but `084`'s
scope was the three named sites plus `src/tools.rs:945`'s consistency, and expanding it would have
gone beyond that task's `Done when`. Note also that `check-decision-refs.py` reads `*.md` only and
never `src/**`, so **nothing in the gate will catch a wrong number here**; the read is the check.

## Done when

- [x] `crates/embarch-core-client/src/client.rs:199,381,1249,1333` each either keep `embarch-core`
      decision 22 (**with a stated reason in the comment itself** that it is the correct, historical
      citation there) or are updated to `embarch-topology` decision 14, matching
      `src/tools.rs:945`'s current wording.
- [x] The report says, per site, which way it went and on what evidence from the two decision
      bodies.
- [x] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [x] `changelog.d/` fragment.

## Resolution

Read both decision bodies in full: `embarch-core/decisions/probes.md` #22 (the identity-gate
mechanism: a machine-local table keyed by probe serial, "exactly one attached" enrollment
enforcement, live-readback fail-closed comparison — its own text says this **"moved wholesale
into `embarch-topology`"**) and `embarch-topology/decisions/enrollment.md` #14 (that crate's own
storage now backing exactly that mechanism; #28 there confirms the *HTTP routes*
`POST /probes/enroll`/`GET /probes/enrolled` stayed in `embarch-core`, but only as a thin surface
over topology's storage).

Line numbers had drifted from `319f0357`/`43ee8517`; re-grepped and confirmed all four sites
still existed at 199, 381, 1249, 1333 (`EnrollProbeRequest::probe_serial`, `EnrolledBoardResponse`,
`CoreClient::enroll_probe`, `CoreClient::list_enrolled`).

All four **repointed to `embarch-topology` decision 14** — none legitimately keep `embarch-core`
decision 22:

- **:199 (`probe_serial` field)** — cited "`embarch-core` decision 22's own doc comment" for the
  "exactly one attached" fallback default, which is decision 22's own mechanism text verbatim, now
  living in `embarch-topology`. The sibling sites `084` already fixed for this *exact same field*
  (`src/main.rs:332-334`, `src/tools.rs:404-406`) both dropped the decision-22 citation entirely
  and kept only `embarch-topology` decision 15 (the optional-serial addition). Repointed to
  decision 14 (naming the "exactly one attached" requirement explicitly) plus 15, rather than
  dropping the first citation outright, to match this same file's own struct-level comment three
  lines above (`:188`, already fixed by `084` to `embarch-topology` decision 14).
- **:381 (`EnrolledBoardResponse`)** — `EnrolledBoardResponse = EnrolledBoard` is a **type alias of
  `embarch_topology::hardware::EnrolledBoard`** (see line 396) — the struct itself is topology's,
  not Core's. Repointed to match the sibling write-side comment's now-fixed pattern
  (`:188`, "`embarch-topology` decision 14's `POST /probes/enroll`") with the read-side route:
  "`embarch-topology` decision 14's `GET /probes/enrolled`".
- **:1249 (`CoreClient::enroll_probe`)** — same route as `:188`'s struct comment, describing the
  same mechanism ("records which physical board `role`'s probe is"). Repointed to decision 14;
  the accompanying `embarch-api` decision 34 (this crate's own two-layer-wrapper rationale,
  confirmed at `embarch-api/decisions/hardware-selection.md`) is untouched — out of scope, unrelated
  to the storage/mechanism question.
- **:1333 (`CoreClient::list_enrolled`)** — the doc comment's **own following sentence** already
  said "a pure read of `embarch-topology`'s own storage on Core's side", directly contradicting
  citing `embarch-core` decision 22 in the same breath. Repointed to decision 14.

No site cited the HTTP route as a historical fact independent of the storage mechanism — all four
were, on inspection, describing the mechanism/data itself (the identity-gate table, the enrolled-
board record, the optional-serial fallback), which is exactly what decision 22 says moved. No new
decision needed (comment-only fix); no wire, struct, or serde change — `embarch-ui`'s path-dep on
this crate is unaffected.
