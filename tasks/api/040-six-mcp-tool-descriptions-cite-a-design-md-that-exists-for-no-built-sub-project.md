# 040 — Six citations inside shipped MCP tool descriptions point at a `design.md` that exists for no built sub-project, and one names the wrong decision

**State:** done by agent/api/040-mcp-descriptions-cite-a-missing-design-md, 2026-09-07
**Source:** suite review pass 2026-09-06, dimension 7 (the newcomer — the agent one). Code-confirmed.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`find /home/gabriel/Github/embarch/embarch-doc -name design.md` returns **only**
`embarch-promptu/design.md` and `embarch-atlas/design.md` — the two sub-projects with no repo.
`grep -c 'design\.md' embarch-api/src/tools.rs` returns 15, of which **six are inside
`#[tool(description = ...)]` strings**: `:792` (`reset`), `:813` (`enroll_probe`), `:830`
(`validate`, twice), `:861` (`alerts`), `:1145` (`study_gatt_data`).

These are not source comments. They are strings shipped over the wire to every agent that
connects, and they are the one part of the suite an agent reads before doing anything. An agent
that follows one lands on a sub-project that was never built.

**Four of the six name no repo at all** — a bare `design.md §3 decision 28` — so an agent cannot
resolve them even by guessing. And `enroll_probe`'s is wrong in both readings: it cites
*"embarch-topology's enrollment storage (design.md decision 22)"*, but `embarch-api` decision 22
is "The uncached scan's cost bound is written down" and `embarch-topology` decision 22 is "A
remote Core's declared host stays with each consumer". The real entry is `embarch-topology`
decision **14** (`embarch-topology/decisions/enrollment.md:9`). The other two checked resolve by
number but not by file (`embarch-topology` 12 → `decisions/alerts.md:17`;
`embarch-study-designer` 54 → `decisions/removed.md:27`).

Also in the same file: `src/tools.rs:232`'s doc comment cites a deleted `milestone-8.md`.

Candidate direction: mechanical, per `tasks/topology/005`'s own recipe —
`design.md §3 decision N` → `<sub-project> decision N` — with a judgement call where a *section*
is cited. Worth also naming the repo in the four bare cases, since an agent has no cwd to
disambiguate from. Verify each number against the current four-file layout rather than assuming
it survived the split.

## Why now

`DOC-CONVENTIONS.md:17` makes decision numbers permanent precisely so references keep resolving,
and `DOC-COMPACTION.md` §2 preferred the split that deleted these files. The suite already has
four per-repo repointing tasks — `tasks/topology/005`, `tasks/ui/006`, `tasks/outpost/004`,
`tasks/study-designer/016`, `tasks/umbrella/025` — and **none of them is `embarch-api`**, and none
of them is about strings that reach an agent.

## Done when

- [x] No `#[tool(description = ...)]` string in `embarch-api` cites `design.md` or a
      `milestone-N.md`.
- [x] Every decision number cited in a tool description resolves to the file that currently holds
      it, verified rather than assumed.
- [x] Every citation names the sub-project it belongs to.
- [x] Gate green; `changelog.d/api-*` fragment.

## Done

Fixed all six `#[tool(description = ...)]` citations in `embarch-api/src/tools.rs`
(`reset` :792, `enroll_probe` :813, `validate` :830 ×2, `alerts` :861,
`study_gatt_data` :1145), plus the `milestone-8.md` doc-comment cite at :232 found
in the same file. Every decision number was verified by opening the target file
and grepping the cited text, not assumed to have survived the 2026-09-04 split:

- `reset` (792): `design.md §3 decision 12` → `embarch-api decision 12`
  (`decisions/zephyr.md:9`, live target discovery — matches).
- `enroll_probe` (813): `design.md decision 22` → `embarch-topology decision 14`
  (`decisions/enrollment.md:9`) — the wrong-number citation the task flagged;
  `embarch-api` 22 and `embarch-topology` 22 are both real and neither is it.
- `validate` (830, first): `design.md §3 decision 28` → `embarch-core decision 28`
  (`decisions/surfaces.md:37`, `POST /validate` and `GET /alerts` together —
  number was already correct, just bare).
- `validate` (830, second): `embarch-topology/design.md §3 decision 12` →
  `embarch-topology decision 12` (`decisions/alerts.md:17` — number already
  correct, just named `design.md` instead of the repo alone).
- `alerts` (861): `design.md §3 decision 28` → `embarch-core decision 28` (same
  entry as validate's first citation).
- `study_gatt_data` (1145): `embarch-study-designer/design.md decision 54` →
  `embarch-study-designer decision 54` (`decisions/removed.md:27` — number
  already correct).
- `:232` doc comment: `embarch-doc/embarch-api/milestone-8.md §3.8` → `embarch-api
  decision 31, 33` (`decisions/studies.md:16` — the JSON-schema-as-string client
  bug).

Citation style follows `tasks/topology/005`'s own recipe (`<repo> decision N`,
no file path — a repo's `decisions.md` is the index that resolves it) rather
than naming a specific file, since decision numbers are what's declared
permanent, not files.

**Out of scope, left alone, and said so in decision 57 itself:** nine other
`design.md` references in this same file are doc comments on parameter
structs and inline code comments, not `#[tool(description = ...)]` strings —
`tools.rs:101,104,303,389,405,411,422,568,956,1213`. Several of those (the
struct-level ones on `TargetParams`, `EnrollProbeParams`, `ValidateParams`,
`AlertsParams`, `StudyStreamParams`) plausibly also reach a connecting agent,
via `schemars`-generated JSON Schema `description` fields on the tool's input
schema — the same wire-exposure concern this task was filed over, just via a
different mechanism than `#[tool(description = ...)]`. This task's own `Done
when` list scopes only the six description strings, so I did not touch them;
worth a follow-up `api` task if the owner wants the same treatment applied
there.

Filed `embarch-api` decision 57 in `decisions/surface.md` (citation-format
rule; topic is the MCP surface, per this task's Reserve note — did not touch
`core-link.md`). That pushed `surface.md` from 10,946 B to 11,785 B, past the
11,059 B reserve line (still under the 12,288 B cap) — filed
`tasks/api/043-compact-api.md` in the same commit, `In flux: yes` (this file
is the active tool/CLI surface and keeps taking new entries, most recently
this same decision).

Gate: `cargo build`, `cargo test` (181 passed across 7 binaries), `cargo clippy
--all-targets -- -D warnings` all green in the code worktree; `scripts/check-docs.py` (10/10),
`scripts/check-client-names.py --repo <code worktree>`, and
`scripts/check-ownership.py --scope api` (doc worktree) /
`--code-repo` (code worktree) all green. Both worktrees committed and pushed
on `agent/api/040-mcp-descriptions-cite-a-missing-design-md`.

## Reserve — read before you write a doc (supervisor, leg 030)

One `embarch-api` file is in reserve: **`embarch-api/decisions/core-link.md`, 12,266 / 12,288 B,
22 bytes left**. It is filed against `tasks/api/026-compact-api.md`, which is **`blocked` on
`In flux: yes`** — decisions 48/49 have never met a real `embarch-core`.

**Do not write into that file.** If this unit earns a numbered decision — and a citation-format
rule plausibly does — its topic is the MCP surface, so it belongs in
`embarch-api/decisions/surface.md`, which has room. If you find yourself reaching for
`core-link.md`, stop and say so in your report rather than squeezing 22 bytes: an `embarch-api`
decision went into the wrong topic file on 2026-09-05 for exactly this reason and nothing failed.

If your work pushes any other file into its last 10%, file
`tasks/api/<NNN>-compact-api.md` in the same commit (`tasks/README.md`, Compaction tasks).
