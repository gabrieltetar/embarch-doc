# embarch-doc

## Docs

This repo *is* the EmbArch suite's documentation. Read [DOC-PROTOCOL.md](DOC-PROTOCOL.md) first — it defines the repo layout, where a given doc lives, and when/how to update one. [embarch.md](embarch.md) is the suite overview and sub-project index; start there for what the suite is before diving into a specific sub-project's `design.md`.

## Git

**Work directly on `main` — no feature branches, no PRs (2026-08-25).** Commit and push straight to `main` once the change builds and its tests and `clippy --all-targets -- -D warnings` are clean. This **overrides** the general "if you're on the default branch, branch first" default, for this suite only. It ends when the repo owner explicitly says it does, and on no other condition — not on an agent's read of whether the project has outgrown it. Reasoning, the sequencing rules that keep it safe, and the one case that still warrants a branch: [embarch-dev-workflow.md](embarch-dev-workflow.md) §6.

## Parallel agent work

Background agent threads run under [embarch-parallel-agents.md](embarch-parallel-agents.md): one supervisor, 4–6 short-lived workers, one repo each, on branches. That doc's §3 ownership map says what a worker may and may not write — notably **not** the shared suite-level docs, and **never** hardware. It does not change how an interactive session works. Start a batch with `/supervise` — or, from a phone or browser where a custom slash command may not expand, just say **"run a supervisor batch"**, which means the same thing: load [.claude/commands/supervise.md](.claude/commands/supervise.md) and follow it. Starting, sizing, watching and stopping one: [embarch-parallel-agents-ops.md](embarch-parallel-agents-ops.md). **Closing VS Code stops the fleet — that is the kill switch, by design.**
