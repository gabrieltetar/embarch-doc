# 078 — eight `embarch-api` source comments cite a `milestone-*.md` that does not exist

**State:** claimed — leg 100, 2026-09-12, branch `agent/api/078-milestone-md-citations`.

**Doc-size reserve for `api`** (check before you write): `decisions/client-crate.md` 649 B left,
`interfaces/config.md` 1090 B left, `decisions/surface.md` 1030 B left — all three already filed
against a blocked compaction task. If your work pushes another `api` doc into reserve, file
`tasks/api/<NNN>-compact-api.md` in the same commit. This unit should be comment-only in source;
if it needs a doc edit at all, prefer a file not on that list.
**Source:** leg 099's refill sweep, 2026-09-12. Verified by reading both sides.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`find /home/gabriel/Github/embarch -name 'milestone-*.md'` returns **nothing** — every one of those
execution docs was folded into its sub-project's four files and deleted (`suite/roadmap.md` says so
explicitly). Eight comments in `embarch-api` still cite them:

- `Cargo.toml:27-29` — ``# 2026-08-24: `core_client.rs`/`config::CoreConfig`/`token_discovery.rs`
  extracted into this shared crate (`embarch-ui` decision 5, `embarch-ui`'s milestone-1.md §4.1)``
- `src/config.rs:9` — ``` `embarch-ui` decision 5's resolution, `embarch-ui`'s milestone-1.md §4.1 ```
- `crates/embarch-core-client/Cargo.toml:9` — ``resolution, `embarch-ui`'s milestone-1.md §4.1)``
- `crates/embarch-core-client/src/lib.rs:7` — ``//! `embarch-ui`'s milestone-1.md §4.1 for the full
  rationale.``
- `crates/embarch-core-client/src/client.rs:51, :206, :212` — ``(`embarch-ui/milestone-1.md` §4.4)``
  and `§4.5` twice
- `crates/embarch-core-client/src/token_discovery.rs:18` — ``per embarch-token.md §2 /
  milestone-2.md §3.1``

**The co-cited half is live and must be kept.** `embarch-ui` decision 5 really exists
(`embarch-doc/embarch-ui/decisions/wiring.md:9`) and `embarch-doc/embarch-token.md` really exists.
So this is not a repointing job in most places — it is **dropping the dead clause and leaving the
live citation standing**. Do not invent a decision number to replace a `§4.4` with; if no decision
covers what a `§` reference was pointing at, delete the reference rather than substituting one.

## Why now

Same defect class `ui/033`, `ui/034` and `ui/039` cleared out of `embarch-ui` — and `ui/039`'s task
file explicitly left the `embarch-api` side to this repo, because the citation crosses repos and
`embarch-ui`'s worker could not confirm it. `check-decision-refs.py` only resolves decision numbers
in `*.md` under the repo root, so a citation living in a `Cargo.toml` comment or a `//!` doc comment
is invisible to every gate. `ui/039` landed this morning for exactly the `Cargo.toml` half of it.

## Done when

- [ ] `grep -rn "milestone-" /home/gabriel/Github/embarch/embarch-api` returns zero.
- [ ] Each of the eight sites either cites a resolvable target or has had the dead clause dropped —
      no invented decision numbers, and `embarch-ui` decision 5 / `embarch-token.md` still cited
      wherever they were before.
- [ ] Cross-repo citations use the settled form: bare `decision M` same-repo,
      `` `<repo>` decision M `` cross-repo (`api/052`, adopted by `umbrella/043` and `core/008`).
- [ ] `cargo build`/`test`/`clippy --all-targets -- -D warnings` green — this is comment- and
      crate-metadata-only, so a behaviour change means something went wrong.
