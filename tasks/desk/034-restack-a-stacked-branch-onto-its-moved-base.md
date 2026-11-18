# 034 — Restack a stacked branch onto its moved base, hunk by hunk

**State:** done
**Source:** Fleet Ready issue: when a base PR gains commits, a session restacks the branch on it by hand and writes a throwaway script that deletes or keeps conflict-marker blocks with a regex.
**Issue:** EMB-142
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

The desk gives a session one tool to restack a branch whose PR sits on another open PR, after that base gains commits. Given the stacked branch and its base branch, in the session's repo or worktree, it rebases the branch onto the base's current tip. When the rebase stops on a conflict it lists every conflicted hunk with file and line, and lets the session resolve each hunk as **ours**, **theirs** or **neither** without hand-editing markers. Before the rebase continues it shows the conflicted files' diff against the base, so the session can check the result. It refuses to continue while any conflict marker remains in a tracked file, and it never force-pushes and never pushes at all.

The shape is the worker's call within `embarch-desk`: an MCP tool on `embarch-desk mcp` (for example `desk_restack`, with a step to resolve hunks and a step to continue or abort), a CLI subcommand, or both, whichever fits the existing tools and `interfaces/cli.md` best. Recording a resolution rule on the work item is not required; a session passes the per-hunk choice.

## Why now

The owner moved the issue to Fleet Ready. Every stacked PR whose base takes review fixes costs a session a hand-written marker script, and in the case that prompted the issue both hunks resolved to neither side.

## Dispatch notes

- **Burndown: no new numbered decision.** Document the tool in `spec.md` or `interfaces.md` without authoring a decision, as `github_pr_threads` was (EMB-176). If the design genuinely needs one, implement the part that does not, file the decision with `scripts/fleet-linear.py file --from decision` (a `Type: decision` body per `LINEAR-PROTOCOL.md`), and say so in this file.
- Test against throwaway git repositories created in a temp directory: a clean restack, a conflict resolved each of the three ways, and a refusal while a marker remains. Never run it against a real repo in the suite.
- No file of this sub-project is in reserve.

## Done when

- [x] One call rebases a stacked branch onto its base's current tip and lists every conflicted hunk with file and line.
- [x] A hunk can be resolved as ours, theirs or neither without hand-editing markers, and the result is shown as a diff against the base before the rebase continues.
- [x] It refuses to continue while any conflict marker remains in a tracked file, and it never pushes.
- [x] Tests cover the cases above; gate green (`../../embarch-fleet/gate.md`); `spec.md`/`interfaces.md` updated, `changelog.d/` fragment dropped, `features.d/desk-<NNN>-*` row if it is a user-visible feature.

## Done

MCP tools only (no CLI, no desk route): `desk_restack`, `desk_restack_resolve`, `desk_restack_continue` (diff first, `confirm=true` to proceed), `desk_restack_abort`, in `src/restack.rs`. Git runs in the MCP process against the session's repo (`repo` param or cwd); `old_base` covers a rewritten base. No decision authored.
