# 186 — The api README carries no counted inventory

**State:** claimed by agent/api/186-the-api-readme-carries-no-counted-inventory, 2026-11-24 03:19
**Source:** suite review audit, 2026-11-23: three code-repo READMEs describe the suite as of September
**Issue:** EMB-297
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api/README.md` says the MCP server exposes seven tools and Core has
four endpoints (the tool inventory in `src/tools.rs` is far larger), and its
getting-started has the reader copy `config.example.toml`, hand-edit it and
set `EMBARCH_TOKEN`, where `suite/user-guide.md` says `embarch init` with a
discovered token.

When this is done the README says what the repo is, where the guide is and
how to build, carries **no counted inventory and no list of tools or
endpoints**, and points at the owning interface docs instead
(`embarch-doc/embarch-api/interfaces/`, the tools doc). Its getting-started
matches `suite/user-guide.md`; check each step against that guide and against
the code, not against memory. The glossary already states the precedent: no
counts or constant values in a page that goes stale.

## Why now

The README is the first thing anyone arriving from GitHub reads, and it gives
them the wrong setup path. EMB-297, which also files `core/149` and
`umbrella/104` for the other two READMEs.

**Burndown leg: no new numbered decision.** None should be needed.

**Doc-size reserve (dispatch note):** no `embarch-api` file is in reserve.

## Done when

- [ ] `embarch-api/README.md` states no tool, endpoint or command count or
      list, and links the interface docs that own them.
- [ ] Its getting-started matches `suite/user-guide.md`.
- [ ] `cargo build` and `cargo test` still green in `embarch-api` (README-only
      change; `clippy` as the gate requires).
- [ ] `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
