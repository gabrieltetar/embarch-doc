# 084 — A tool description tells a connecting agent to call `study_steps`, which is not a tool

**State:** claimed — leg 111, 2026-09-13, `agent/api/084-study-steps-and-two-stale-citations`
**Source:** leg 111's refill sweep — a read-only hunter over `embarch-api`, run because
`--refill-owed` fired on scope spread. Every finding below was verified against both sides before
filing.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Three findings. The first is the one that matters: **an MCP tool description instructs an agent to
make a call that cannot succeed.**

### 1. `study_steps` is named on both sides and exists on neither

`src/tools.rs:1219`, inside `study_watch`'s description: "*the study is unaffected and its own
record on disk is complete, so re-read it with `study_status`/`study_steps`.*" And
`embarch-api/interfaces/studies.md:25`: "*`study_status`/`study_steps` hold the complete record.*"

There is **no `study_steps` MCP tool and no `study-steps` CLI subcommand.** It exists only as a
method on the internal client crate (`crates/embarch-core-client/src/client.rs:1745`). The parity
test that derives the whole surface from source (`tests/tool_subcommand_parity.rs`) yields 26 tools
and 27 subcommands and none of them is `study_steps`. This is a `lagged`-recovery instruction, so
the agent reading it is one that has already lost frames.

`study_status` alone is the real answer — the same description says so two paragraphs earlier
("`study_status` is still the way to get one snapshot or the finished `StudyResult`").
`list_study_streams` is the other real read surface if a per-tap answer is meant; **decide which,
from the surrounding text, rather than deleting the second name reflexively.**

`tasks/api/080` swept every count and name in `interfaces/tools.md` and found nothing else wrong —
`studies.md` was a different file and was not in that sweep, which is why this survived.

### 2. `src/tools.rs:1387` cites `embarch-study-designer spec.md §4.8`, a section that does not exist

That repo's `spec.md` §4 is "What a study carries", a table of *submitted* `Study` fields with **no
numbered subsections at all**, and it does not mention `StudyResult` or `streams`. The entry that
actually defines `StreamRef` is `embarch-study-designer/interfaces/result-types.md` — "*`streams`
carries one `StreamRef { name, bytes_written, truncated, records }` per declared tap, including one
that produced nothing*", which is the `truncated` passthrough the comment goes on to justify.
**Cite it in the current cross-repo form; do not invent a section number for it.**

### 3. `enroll-probe`'s clap help carries a citation `decisions/surface.md` already records as wrong

`src/main.rs:320-322` — the doc comment that produces `embarch-api enroll-probe --help` — says
"*Enroll a physical probe with `embarch-core`'s `known_boards` table (`embarch-core` decision 22)*".
Two things are stale: `embarch-core` decision 22 is the wrong entry, and `known_boards` is the
pre-`embarch-topology` name (`embarch-topology/decisions/storage.md`: the directory
`known_boards.toml` "already used **before this crate existed**").

**The MCP twin is already right** — `src/tools.rs:945`: "*Enroll a physical probe with
`embarch-topology`'s enrollment storage (`embarch-topology` decision 14)*" — so the two front ends
currently tell a user two different things. `embarch-api/decisions/surface.md` states the fix
outright: "*`enroll_probe`'s named one but the wrong number either way (cited decision 22; the real
entry is `embarch-topology` decision 14)*". Decision 57 scoped its mechanical fix to
`#[tool(description = ...)]` strings only, which is exactly why `main.rs` was missed.

Two sibling sites carry the same stale pair and belong in this unit: `src/tools.rs:389` and
`crates/embarch-core-client/src/client.rs:188-192`.

## Notes for whoever runs this

- **Re-derive every decision number from its own body**, not from this task file. Line numbers here
  came from a hunter and may be off by a commit.
- **Say explicitly in your report whether your own grep for `study_steps` and for the stale
  `known_boards`/`decision 22` pair found the same sites this task names.** A count that matches is
  worth as much as one that does not.
- **Files in reserve for this sub-project:** `embarch-api/decisions/surface.md` — 11258/12288 B,
  **1030 B left** (parked against `tasks/api/069`); `embarch-api/spec.md` — 9090/10240 B, **1150 B
  left** (parked against `tasks/api/083`). Nothing here should need either. If your work pushes a
  file into reserve or leaves one there unfiled, file `tasks/api/<NNN>-compact-api.md` in the same
  commit, picking the number with `python3 scripts/check-task-numbers.py --next api`.

## Done when

- [ ] `src/tools.rs:1219` and `embarch-api/interfaces/studies.md:25` name only surfaces that exist.
- [ ] `src/tools.rs:1387` points at something real, in the current citation form.
- [ ] `src/main.rs:320-322`, `src/tools.rs:389` and
      `crates/embarch-core-client/src/client.rs:188-192` agree with `src/tools.rs:945`.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.
