# embarch-user-guide.md: changelog archive

Entries beyond the 8 most recent, moved here from [embarch-user-guide.md](embarch-user-guide.md)
by `scripts/archive-changelog.py`, per `DOC-PROTOCOL.md` §5. Newest-first,
same as the live doc's own Changelog.

- 2026-08-17 — §11: `cargo build --release` changed to plain `cargo build` for day-to-day iteration (release mode is for actually shipping something, not every edit-compile-test cycle), and added a pointer to the new [embarch-dev-workflow.md](embarch-dev-workflow.md) — §11 told you to build each repo independently but never said how to wire a dev `embarch-api` to a dev `embarch-core`, or how to test an `embarch-umbrella` change without it overwriting a real install.
- 2026-08-05 — Replaced the placeholder with the real getting-started guide, written for a firmware engineer new to EmbArch and written *ahead of* the `embarch` setup tool it describes, so it serves as [Milestone 6](embarch-roadmap.md#6---onboarding)'s specification and acceptance criteria ([embarch-umbrella/design.md](embarch-umbrella/design.md) §11). Appendix A carries the manual procedure that actually works today and is expected to shrink as that milestone lands. Both of `embarch-api`'s front-ends are presented as peers (§1, §6, §7) rather than treating the CLI as secondary to the agent path. Dev bench and studies are included per request but clearly marked unusable (§10).
