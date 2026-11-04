# embarch-doc

## Docs

This repo *is* the EmbArch suite's documentation. Read [DOC-PROTOCOL.md](DOC-PROTOCOL.md) first — it defines the repo layout, where a given doc lives, and when/how to update one. [embarch.md](embarch.md) is the suite overview and sub-project index; start there for what the suite is before diving into a specific sub-project's `spec.md`.

## Git

**Work on a branch, land when the owner asks — no PRs (2026-11-03).** Work in a worktree, with one branch name across every repo the change touches, and push the branch. Land on `main` only when the repo owner asks: rebase on `origin/main`, confirm `scripts/check-docs.py` is green, fast-forward, push, delete the branch. The owner's explicit call ended the earlier commit-straight-to-`main` rule, and changing this one is the owner's call too, not an agent's read of what the project needs. The fleet lands under its own protocol. Reasoning, setup and the landing order across repos: [embarch-dev-workflow.md](embarch-dev-workflow.md) §6.

## Parallel agent work

Background agent threads run under [the protocol](../embarch-fleet/protocol.md): a supervisor keeps 4–6 short-lived workers in flight, one repo each, on branches. That doc's §3 ownership map says what a worker may and may not write — notably **not** the shared suite-level docs, and **never** hardware. It does not change how an interactive session works.

**The fleet's rules live in a separate repo, [`embarch-fleet`](../embarch-fleet/README.md), and a leg never checks it out** (2026-09-04). A supervisor that can edit its own constraints has none, and a denylist of filenames inside *this* repo had already failed once — the risk register stopped being reserved purely by moving. What that repo holds: the protocol, the ops doc, the risks, `supervisor-log.md`, and the scripts. What stays here: the queue (`tasks/`, `inbox/`, `status.d/`, `changelog.d/`), because the claim commit on this repo's `main` is the double-dispatch interlock. This repo's `.claude/`, its four protocol READMEs and its `scripts/fleet` shims are **generated** by `embarch-fleet/scripts/install.py` — edit the template there, not the copy here, and `install.py --check` is what catches the difference.

**Three windows** ([ops](../embarch-fleet/ops.md) §1, §5.1). A **listener** window, armed with `/fleet start`, reads **#embarch-fleet** and spawns agents — it has no hands and never does work itself (see [.claude/commands/fleet.md](.claude/commands/fleet.md)). Saying `fleet start` in that channel latches the **pump**: one `embarch-supervisor` **leg** at a time, four tasks each, landing and folding as it goes, and each leg's death spawns the next until `fleet stop`. This window — an ordinary session — is the third: standing rules, `scripts/`, `.claude/`, hardware, and drops into `inbox/`. `/supervise` still runs one leg by hand; from a phone, **"run a supervisor batch"** means the same thing. **Closing VS Code stops the fleet — that is the kill switch, by design.**
