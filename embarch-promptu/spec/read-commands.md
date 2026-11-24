# embarch-promptu: read-only session commands

**Status:** active, 2026-11-23.

Moved verbatim from [spec.md](../spec.md) §2.

- **`promptu calls <session> [--subagent <id>] [--class <name>] [--json]`**: a recorded session's tool calls and result characters, per subagent (and the main thread) and per activity class (`git`, `build`, `config`, `source`, `other`), so a before/after replay is a measurement; with `--class`, that class's calls one per line with their result sizes. The class rules are one table in `src/calls.rs` (`classify`), pinned by a test. Reads Claude Code's transcripts; synthetic fixtures only in tests.
- **`promptu prior <prompt-file> [--projects <dir>] [--json]`** (EMB-185): what the earlier runs of a prompt asked and were answered. A transcript matches when its first user turn is the prompt (text equal after trimming; a footer-only file matches a first turn ending in that footer; the footer has no run id, so the text decides); the same footer under other text is a near-match, counted, not listed. Lists each session's `AskUserQuestion` calls with the `tool_result` that answered them. Read-only, one folder, `src/prior.rs` on `used.rs`'s reader. Contract §13.
