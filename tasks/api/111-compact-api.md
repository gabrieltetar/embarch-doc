# 111 — `embarch-api/decisions/failure-reporting.md` is in reserve after decision 76

**State:** done
**Source:** `api/110`'s decision 76 (the `validate` `not_attached` lead wording) pushed this file
past its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/failure-reporting.md
**Size debt due:** 2026-09-27
**In flux:** no — for the move this task makes. Unparked at claim, 2026-09-28, one day past its
clock, on this task's own second condition: the file is judged safe to **split** along the seam it
names, because a verbatim move restates nothing (`DOC-BUDGET.md`'s split-first rule; the same
reading `core/093` got today). The file is untouched since `bf73fcf1` (2026-09-17). The old answer,
kept as history, still governs any **squeeze** of 71/73/76: *yes — `validate`'s `kind`/`reason`
split has taken three amendments this month alone (71, 73, now 76) and `embarch-core`'s own
classifier for the condition changed again the same morning this decision landed
(`tasks/core/077`). A compaction pass run now risks shortening prose the next such amendment will
need to build on within days. Unparked once a unit lands here without adding a new amendment to
decisions 71/73/76, or once the file is judged safe to split (its own natural seam: decision 57/67,
the parity-rule entries, versus 71/73/76, the `validate` `kind`-classification thread).*
**Must not delete:**
- Decision 71's own text describing the three-layer fix (wire shape, `is_not_attached()`
  predicate, two call sites) — the only record of why the client-side inference was rejected.
- Decision 73's "Against leaving it" paragraph — the concrete hazard (`fix_it_url` inviting
  re-enrolment on an unclassifiable response) that justified the `"unknown"` value.
- Decision 76's three named alternatives and why each was rejected — the second supervisor note on
  `api/110` asked for this explicitly, and it is the only place the reasoning behind the chosen
  wording is recorded.

## Why now

`python3 scripts/check-doc-size.py` names `embarch-api/decisions/failure-reporting.md` at
11578/12288 B (94.2%, 710 B left) — inside the last 10% reserve band (`RESERVE_FLOOR` = 1200 B),
crossed by `api/110`'s decision 76 addition.

## Dispatch note (supervisor, 2026-09-28)

**Split only; squeeze nothing.** Move 71, 73 and 76 byte-identical into a new topic file (e.g.
`decisions/validate-kind.md`), or the seam you find better, said why — and rewrite none of them:
the unpark above covers a move and nothing else. Update `decisions.md`'s routing row. Check inbound
links to 57, 67, 71, 73 and 76 across the suite before cutting (`grep -rn` over `embarch-doc` and
the code repo, including tool descriptions under `src/`, which decision 57 says cite by `<repo>
decision N`) and repoint any that name the file rather than a bare number; a link in another
sub-project's directory you cannot write goes in an `inbox/` drop at
`/home/gabriel/Github/embarch/embarch-doc/inbox/` (absolute path), and the supervisor repoints it at
the fold.

**Also in reserve in `api`, not yours to write:** `spec.md` 858 B left (`tasks/api/083`, blocked),
`open.md` 665 B left (`tasks/api/113`, blocked). If your work pushes any other `api` file into
reserve, file `tasks/api/<NNN>-compact-api.md` in the same commit.

## Done when

- [x] `embarch-api/decisions/failure-reporting.md` is back under its reserve band, its "must not
      delete" facts intact — a split along the seam above is one honest way to do it, not the only
      one.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment.

## Closed

Split along the seam the dispatch note named, verbatim: decisions 71, 73 and 76 (`validate`'s
`kind`-classification thread) moved unchanged into new `embarch-api/decisions/validate-kind.md`;
57 and 67 stayed in `failure-reporting.md`. Byte-identical move, checked line-for-line against the
original before truncating it — nothing squeezed.

**Sizes:** `failure-reporting.md` 11578 B → 5657 B (57/67 only). `validate-kind.md` (new) → 6980 B
(71/73/76). Both files' Status lines bumped to 2026-09-28 (the split itself); no decision content's
own dates changed. `decisions.md`'s routing row split into two matching rows.

**Inbound-link check:** `grep -rn` over `embarch-doc` and the `embarch-api` code repo (including
`src/` tool descriptions) for `failure-reporting`, and for bare `decision 57/67/71/73/76` citations
that might be `embarch-api`'s. Every citation in the code repo (`tools.rs`, `cli.rs`, `main.rs`,
`client.rs`) is a bare `embarch-api decision N`, per decision 57's own convention — none names a
filename, so none went stale. Two doc files link straight at `failure-reporting.md` for decision 67
(`interfaces/tools-topology.md`, `interfaces/tools-dev-bench.md`) — 67 stayed in that file, so both
stay correct. No file anywhere links to `failure-reporting.md` for 71, 73 or 76 specifically — only
`decisions.md`'s own row named them, and that row moved with them. **No inbox drop needed**: nothing
outside `api` referenced the moved decisions by file path.

**Gate:** `check-docs.py` 11/11 green, including `check-decision-refs.py` (no stale topic-file
links) and `check-doc-size.py` (both files well clear of cap and reserve). `check-ownership.py
--scope api` (doc worktree) and `--code-repo` (api worktree) both clean. `check-client-names.py`
clean in both. `embarch-api`: `cargo build`/`test`/`clippy --all-targets -- -D warnings` all green
on the workspace (no code changed by this task; both `crates/*` are workspace members, so the gate
reaches them).

**DOC-COMPACTION-PASS.md's human question** ("Can `spec.md` alone answer what someone needs to
work on this component today?"): unaffected by this task — `spec.md` is untouched, and a verbatim
split moves bytes between two decision files without deleting or restating anything, so whatever
`spec.md` could answer before this task, it still can. This was a split, not a squeeze; the
hot/cold second pass was explicitly out of scope (dispatch note: "split only, squeeze nothing").
