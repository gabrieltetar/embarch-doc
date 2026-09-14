# 093 — Sweep decision citations in `resolve.rs`, `tools.rs`, `cli.rs`

**State:** open
**Source:** `api/091` swept `crates/embarch-core-client/src/client.rs` (99 citations) and
`src/config.rs` (37 citations) end to end and ran out of scope before reaching the rest of the
surface named in that task's own count: `src/resolve.rs` (~32), `src/tools.rs` (~24),
`src/cli.rs` (~17).
**Scope:** api
**Hardware:** none — source comments only; no board, no live Core, no deploy.
**Owner:** no

## What

Continue the same sweep, in this order: `resolve.rs`, `tools.rs`, `cli.rs`. For each citation,
resolve the number, say which repo's decision set it resolves against (bare same-repo, labelled
`<repo> decision N` for a foreign referent — `client-crate.md`/`hardware-selection.md` already
show `embarch-api` and `embarch-core` sharing numbers, and `client.rs` additionally cited
`embarch-study-designer`, `embarch-outpost`, `embarch-topology` and `embarch-ui`), and read the
cited decision's body against the sentence around the citation, not just the number.

## Why now

`api/091` found `client.rs`'s 99 citations were mostly sound but not flawless: one real
wrong-number defect (`embarch-api` decision 59 cited four times, including once inside a
user-facing string literal, for content that decision 60 states) and two ambiguous/unlabelled
foreign citations (`embarch-topology` decision 14, `embarch-study-designer` decision 40, both
appearing bare immediately after a differently-labelled sibling citation in the same sentence).
`config.rs`'s 37 checked clean. `resolve.rs`/`tools.rs`/`cli.rs` are unswept.

## Done when

- [ ] `resolve.rs`, `tools.rs` and `cli.rs` are swept end to end, in that order, as far as
      honestly reached; any remainder filed as `tasks/api/<next>` naming the files not reached.
- [ ] Every cross-repo citation in the swept files carries the labelled `<repo> decision N` form.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment. A numbered decision only if something was actually decided.
