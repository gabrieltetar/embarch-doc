# embarch-api decisions: The served HIL guide

**Status:** active, 2026-11-20.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/guide.md](../interfaces/guide.md).

### 108 — `guide hil` embeds a pinned copy of the guide in this repo; a drift test guards it where `embarch-doc` is reachable

`tasks/api/163` (EMB-227). An adopter's agent has the binary and no `embarch-doc`, so the guide has to travel in the binary, versioned with the tools it describes. **CLI only, host-side only**: it prints compiled-in text, so `main` dispatches it before config or Core, like `versions`.

- **The text is `guide/hil-guide.md` in this repo, compiled in with `include_str!`.** A pinned copy of `embarch-doc`'s `suite/hil-guide.md`. Sections are its `## ` headings: `Every mode` (what `guide hil` prints), `Live`, `Study`, `Test`. An unknown mode exits 1 and lists the modes. **Amended 2026-11-23 (EMB-228):** the shared section was `Choosing a mode`; the guide's words, trust claim and before-any-hardware steps belong to every mode, and only the shared section and a mode's own are served, so they live in it, renamed.
- **How a guide edit reaches the binary:** the edit lands in `suite/hil-guide.md` (an `embarch-doc` unit), then the same text is copied over `guide/hil-guide.md` in an `embarch-api` unit and ships with the next build. M1.13 wrote the suite guide on 2026-11-23 (EMB-228); until then the pinned file was a skeleton and the only copy.
- **What catches the two drifting apart:** `tests/guide_cli.rs` compares the pinned copy with `suite/hil-guide.md` in `$EMBARCH_DOC_DIR`, else a sibling `embarch-doc`, and fails on a difference. It is silent where none is reachable, which is every adopter and a CI with one repo, so **it is a guard for the fleet and the owner's machine, not a proof**: a drift on a machine with no checkout is caught by the next one that has it.
- **Rejected: a `build.rs` read of a pinned `embarch-doc` by relative path.** It breaks a worktree build (siblings are symlinked, not guaranteed) and a published crate (no sibling at all), and it would make a docs-only edit change this binary with no commit here to show it.

**Measured:** the built command run from an empty directory with no config prints each section; every command the `embarch-hil` skill names is run by the test. **Assumed:** that a copy step per guide edit is cheap enough, at one guide edited in a few units; if it is forgotten often, move the copy to a `scripts/` sync.
