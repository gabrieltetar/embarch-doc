# 094 — An MCP tool for the outpost's own answer: the half of suite decision 4 that closes its property

**State:** done — leg 111, 2026-09-13, branch `agent/api/094-mcp-tool-for-outpost-load-shares`.
**Source:** `tasks/core/057`'s own "Sequencing" section, which named this follow-up and said
explicitly that it must **not** be filed until `core/057` landed, because a worker given it earlier
would be building against a route that did not exist. It landed 2026-09-13 (code `a131f63` in
`embarch-core`, doc `886a0bc` in `embarch-doc`), so it is filed now, in the same fold.
**Scope:** api
**Hardware:** none to build it. A live `embarch-core` is only needed to exercise it end to end, and
that is not required for this task — `embarch-api` has its own test surface and `core/057` shipped
a route with tests against a real firmware fixture.
**Owner:** no

## What

[Suite decision 4](../../suite/decisions.md) states the property this closes:

> An agent can obtain an outpost capture's **per-subject load shares and its coverage line**
> without re-implementing the timeline, and exactly one implementation of that timeline exists in
> the suite.

`core/057` built the first half — the computation, and `GET /study/{id}/stream/{name}/load` to
reach it (`embarch-core` decision 62, `decisions/streams.md`; documented in
`embarch-core/interfaces/studies.md` with its `400`/`404`/`422` cases). **Today an agent still
cannot ask for it**, because nothing in the MCP surface calls that route. Until that exists, the
decision's property is half-true: the computation is in one place, and the agent path to it is
missing.

Add the MCP tool, alongside the existing study-stream tools, and give it a CLI subcommand like
every other tool has.

## Why now

**This is the unit that makes suite decision 4 worth having.** The whole argument for moving the
computation into Core rather than leaving it in `embarch-ui` was that Core is on **both** paths —
the agent's, through `embarch-api`, and the human's, through the UI's Core client. Only one of
those two paths is built. The human already had an answer before any of this work started (the UI
renders it), so an agent reaching it is the entire new capability.

Note the sibling follow-up, deliberately ranked **below** this one: `tasks/ui/051`, retiring
`embarch-ui`'s own copy of the timeline arithmetic. The UI is correct today; the agent path does
not exist at all.

## Watch for

- **`list_study_streams` already describes `bytes_written: 0` as "a tap that was declared and
  produced nothing".** Whatever this tool returns for a capture with no usable rows should not
  collide with that wording — `tasks/suite/029` is open on exactly the ambiguity that phrasing
  creates.
- **The route can answer `422`** when the CSV's column list does not match the shared crate's
  header (`core/057` carried `embarch-ui` decision 10 (trace)'s check across deliberately). That
  refusal is load-bearing — reversals row 86 is why — so **relay it as a refusal, do not smooth it
  into an empty result.**
- **The MCP binary on this machine goes stale against a schema bump** and the running server keeps
  the old one. If this task changes any tool schema, say so in the changelog fragment; verifying it
  is the owner's, through the CLI, not an agent's through the live MCP server.

## Done when

- [x] An MCP tool returns an outpost capture's per-subject load shares and coverage line for a
      study stream, by calling Core's route rather than computing anything. `study_stream_load`
      (`src/tools.rs`) calls the new `CoreClient::get_study_load` (`crates/embarch-core-client/src/client.rs`),
      which hits `GET /study/{id}/stream/{name}/load` and parses Core's `LoadAnswer` — no arithmetic
      on this side of the wire.
- [x] It has a CLI subcommand, like every other tool (decisions 3/10's superset rule — the task's
      own "decision 40" is `suite/features.md`'s `api-040` row, not a decision number; corrected
      here rather than repeated). `study-stream-load` in `src/main.rs`/`src/cli.rs`.
- [x] `embarch-api/tools.md` documents it and the tool index count stays consistent.
      `interfaces/tools.md`'s Studies bullet and `interfaces/studies.md`'s table both gained the
      row; `src/cli.rs`'s hardcoded subcommand-arm count (26 → 27) and `tests/json_surface.rs`'s
      `EVERY_SUBCOMMAND` both updated, so the mechanized surface counts stayed true rather than
      going stale.
- [x] The `422` column-mismatch case reaches the caller as a refusal with its reason intact.
      `get_study_load` passes every non-2xx body through `format_study_error` untouched — Core's
      handler returns the mismatch's own text as the body, and nothing here substitutes an empty
      result for it.
- [x] A numbered `embarch-api` decision only if something was actually decided — wiring an
      existing route to an existing tool pattern decides nothing. **None written**: this followed
      `study_stream_data`'s existing shape (mirrored struct, same three-refusal relay pattern, same
      CLI/MCP pairing) with no new choice to record.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`/`cargo test`/
      `cargo clippy --all-targets -- -D warnings` all clean in `embarch-api` (including the new
      `get_study_load` sweep coverage in `tests/core_client_http.rs` and a wire-shape deserialize
      test in `crates/embarch-core-client/src/client.rs`); `scripts/check-docs.py` all 11 green;
      `check-client-names.py --repo embarch-api` clean; `check-ownership.py --scope api` and
      `--code-repo` both clean.
- [x] `changelog.d/` fragment. `changelog.d/api-outpost-load-tool.added.md`, naming the schema
      change explicitly per this task's own "Watch for" note.

## Dispatch note — leg 111, 2026-09-13

**Doc-size reserve in your sub-project, so you plan instead of discovering.** One file is in
reserve: **`embarch-api/spec.md`, 9,102/10,240 B — 1,138 B left (88.9%)**. Its compaction task
`tasks/api/083` is **`blocked` on `In flux: yes`**, and per `.claude/leg.md` a blocked compaction
task parks the *pass*, not the *reserve*:

- **If this unit writes into `embarch-api/spec.md`, compact that file as part of this unit**,
  carrying `api/083`'s `Must not delete:` list verbatim (the §2 invariants, the Session-0/UNC
  failure signature, `base_url = "auto"`'s resolution order and its "a `401` counts as an answer"
  line, and every row *and* Provenance tag in §7's constants table). `api/083` itself names the
  file's natural seam — §§1-2 "what it is and what must always hold" vs §§3-7 "how it does it" —
  and a **verbatim split restates nothing, so `In flux: yes` cannot forbid one.** A split is the
  cheaper move if one fits.
- **If it does not write into `spec.md`, file nothing new** — the debt is already filed against
  `api/083`. Nothing here asks you to do the whole compaction pass.

Everything else you will touch has room: `embarch-api/interfaces/tools.md` 4,366 B and
`interfaces/studies.md` 5,422 B are well clear.

**If your work pushes any other `embarch-api` doc into its reserve band and nothing has filed
against it**, file `tasks/api/095-compact-api.md` in the same commit (`tasks/README.md` has the
shape; **`tasks/api/`, your own scope — never `tasks/doc/`**, which `check-ownership.py` refuses to
every worker). You are not asked to do the compaction, only to record the debt while you still hold
the one piece of context nobody else will have: whether that part of the subsystem is still in flux.

**One repo, one branch, one task.** Code in `embarch-api`, docs in `embarch-doc`, both on
`agent/api/094-mcp-tool-for-outpost-load-shares`. `embarch-api`'s worktree has
`embarch-study-designer` and `embarch-topology` symlinked beside it — the path-dep closure — so
`cargo build` resolves.
