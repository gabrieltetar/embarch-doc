# embarch-doc

## Docs

This repo *is* the EmbArch suite's documentation. Read [DOC-PROTOCOL.md](DOC-PROTOCOL.md) first — it defines the repo layout, where a given doc lives, and when/how to update one. [embarch.md](embarch.md) is the suite overview and sub-project index; start there for what the suite is before diving into a specific sub-project's `design.md`.

## Git

**Work directly on `main` — no feature branches, no PRs (2026-08-25).** Commit and push straight to `main` once the change builds and its tests and `clippy --all-targets -- -D warnings` are clean. This **overrides** the general "if you're on the default branch, branch first" default, for this suite only. It ends when the repo owner explicitly says it does, and on no other condition — not on an agent's read of whether the project has outgrown it. Reasoning, the sequencing rules that keep it safe, and the one case that still warrants a branch: [embarch-dev-workflow.md](embarch-dev-workflow.md) §6.

## Parallel agent work

Background agent threads run under [embarch-parallel-agents.md](embarch-parallel-agents.md): a supervisor keeps 4–6 short-lived workers in flight, one repo each, on branches. That doc's §3 ownership map says what a worker may and may not write — notably **not** the shared suite-level docs, and **never** hardware. It does not change how an interactive session works.

**Three windows** ([ops](embarch-parallel-agents-ops.md) §1, §5.1). A **listener** window, armed with `/fleet start`, reads **#embarch-fleet** and spawns agents — it has no hands and never does work itself (see [.claude/commands/fleet.md](.claude/commands/fleet.md)). Saying `fleet start` in that channel latches the **pump**: one `embarch-supervisor` **leg** at a time, four tasks each, landing and folding as it goes, and each leg's death spawns the next until `fleet stop`. This window — an ordinary session — is the third: standing rules, `scripts/`, `.claude/`, hardware, and drops into `inbox/`. `/supervise` still runs one leg by hand; from a phone, **"run a supervisor batch"** means the same thing. **Closing VS Code stops the fleet — that is the kill switch, by design.**
