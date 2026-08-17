# embarch-atlas: design

**Status:** Paused, no repo yet.

Placeholder — this doc becomes the source of truth once `embarch-atlas` design work resumes. See [embarch.md](../embarch.md) §2 for its lineage (the original `gabrieltetar/embarch` C#/WPF static-analysis GUI) and §3 for its one-line purpose, and [embarch-roadmap.md](../embarch-roadmap.md)'s Later bucket.

## Open questions, recorded before resuming (so they aren't re-litigated from scratch)

- **Transport is unresolved: reachable over `embarch-api`'s existing MCP surface, or its own server.** `embarch.md` §2 currently calls MCP "a plausible transport `embarch-api` could expose it over, not the defining shape of the capability itself" — true, but exactly the kind of open question that gets forgotten and re-derived from scratch once this sub-project actually resumes, closing item 58 of the 2026-08-15 design-improvement review by writing it down here explicitly rather than leaving it implicit in a sentence about something else. Two real options, neither chosen: (a) a new tool on `embarch-api`'s existing MCP surface (`embarch.md` §5's "every hardware-facing capability reachable both by an agent and a human" principle would extend naturally, but `embarch-api` gains a dependency on a structural-analysis engine it has no other reason to link); (b) `embarch-atlas` as its own MCP server (keeps `embarch-api` unchanged, but means a second server an MCP client has to register, and a second process for the C#/WPF GUI's future debug-facing mode, §2, to talk to). No lean recorded either way — this is a decision for whoever resumes the work, not one to make speculatively now.

## Changelog

- 2026-08-15 — Recorded the MCP-transport-vs-own-server open question explicitly (closing item 58 of that day's design-improvement review, `.claude/design-improvements-2026-08-15.md`), rather than leaving it implicit in `embarch.md` §2's "plausible transport" phrasing. No lean taken; still paused, still no repo.
- 2026-07-20 — Placeholder created alongside the embarch-doc per-sub-project restructure.
