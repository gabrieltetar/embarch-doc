# api — `dev_bench_hello` is MCP-only, contradicting decision 3/10's "identical capabilities" and spec.md §1's CLI ⊇ MCP superset

**State:** claimed — leg 048
**Promoted** from `inbox/api-dev-bench-hello-mcp-only-breaks-cli-superset.md` by leg 048, unchanged
apart from this line, the number, and the dispatch note at the bottom.
**Source:** reviewer, api/036 (merge SHAs: embarch-api `95c1954e40d5fbadc79bf5ad2448dfcb69d2e36f`, embarch-doc `cf12cae`+`8005396`)
**Scope:** api
**Hardware:** none — this is a doc/decision-consistency contradiction, not something a board can confirm or refute.

## What

`embarch-api/decisions/shape.md` decision 3/10 ("Three responsibilities, and a
CLI alongside MCP rather than instead of it") states the CLI and MCP front-ends
expose **"the identical capabilities."** `spec.md` §1 states the same thing more
strongly: "the same as CLI subcommands — a **superset**, `versions` having no
tool" — naming exactly one exception, and it runs CLI-only (MCP lacks
`versions`, humans still get everything agents get). `decisions/tool-wrapping.md`
52 leans on this explicitly: "spec.md §1 guarantees CLI ⊇ MCP — a human can do
anything an agent can — which a CLI-only diagnostic leaves intact."

api/036 adds `dev_bench_hello` as an **MCP tool with no CLI subcommand at all**
(`src/tools.rs`, the new `#[tool(description = ...)] async fn dev_bench_hello`
at the merge SHA above — `cli.rs` is untouched by the whole unit, confirmed via
`git show --stat 95c1954e40d5fbadc79bf5ad2448dfcb69d2e36f`). `embarch-doc`'s own
`interfaces/tools.md` row for it says so outright: "No CLI subcommand: this is
the one place `docs/tools.md` names an MCP tool with no CLI twin **other than**
`versions`' own reverse case" — treating the two as symmetric when they are not.
`versions` being CLI-only leaves "a human can do anything an agent can" intact;
`dev_bench_hello` being MCP-only **breaks it** — there is now something an agent
can reach that a human using the CLI cannot, which is the exact guarantee
decision 52's own text invokes.

Neither `spec.md` §1 nor `decisions/shape.md` 3/10 was touched by either doc
commit in this unit (`git show 8d18fb3:embarch-api/spec.md` vs
`git show 8005396:embarch-api/spec.md` are identical at that line). This isn't
a refinement recorded in the same diff (protocol.md §10's carve-out) — the
standing invariant is left standing, unamended, while a tool that violates it
ships.

## Why now

This is the shape risks.md calls out: it passes every check (build, clippy,
tests — none of them assert CLI/MCP parity mechanically) and quietly
contradicts a locked decision and the spec's own stated guarantee, in a unit
that already went through one merge-time refusal and rework (leg 045/046) for
an unrelated, narrower issue (the `Option<String>` rendering call) — so the
CLI-superset break rode through unnoticed on the second pass too.

## Done when

Either:
- a `dev-bench-hello` (or similarly named) CLI subcommand is added restoring
  CLI ⊇ MCP, and `interfaces/tools.md`'s "no CLI twin" line is retracted; or
- a decision explicitly amends decision 3/10 and `spec.md` §1 to record a
  second, opposite-direction exception (an agent-only capability), with the
  "a human can do anything an agent can" language in decision 52 and spec.md
  either scoped down or reconciled — not left asserting a guarantee this tool
  already breaks.

## Revert notes

- `embarch-api` `95c1954e40d5fbadc79bf5ad2448dfcb69d2e36f` (parent `a1330f9`):
  adds the tool method, two error types, and `HelloAckResponse`'s new fields —
  self-contained to `client.rs`/`tools.rs`, no other call sites touch either
  new symbol, so a revert of just this commit looks clean.
- `embarch-doc` `cf12cae` then `8005396` (parent of the pair `8d18fb3`): `8005396`
  edits lines `cf12cae` introduced (`decisions/tool-wrapping.md`,
  `interfaces/tools.md`'s `dev_bench_hello` row) and adds decision 60 on top, so
  reverting requires both, in reverse order (`8005396` first, then `cf12cae`) —
  not a revert of `8005396` alone.

## Also noted, not filed as a separate contradiction

`embarch-api/decisions/study-events.md`'s decision 48 entry still links
`[decision 47](surface.md)` — decision 47 moved to `decisions/tool-wrapping.md`
in this same unit's `cf12cae`. Confirmed via `git show 8d18fb3` that the link
was correct before this unit's split and has been dangling since; unlike the
cross-repo `embarch-umbrella/decisions/schema-skew.md` citation the unit's own
commit message flagged and filed to inbox, this same-repo one was missed. Not
filed as its own drop — it's a broken cross-reference, not a decision the code
contradicts — but worth a one-line fix (`surface.md` → `tool-wrapping.md`)
whenever `study-events.md` is next touched.

## Dispatch note — leg 048

**The two arms of "Done when" are not equally right, and I am directing you to the
first.** Add the CLI subcommand. Reasons, so you can push back with evidence if you
find them wrong rather than just complying:

- `suite/features.md` carries `api-040 — CLI subcommands for every tool` as a
  shipped capability. An MCP tool with no subcommand does not just contradict a
  decision, it makes a shipped feature row false.
- Decision 52's rationale *leans on* CLI ⊇ MCP to justify a CLI-only diagnostic.
  Amending 3/10 and `spec.md` §1 to admit an agent-only capability would knock the
  ground out from under a decision that is otherwise fine, and would be a much
  larger design call than this defect earns.
- `dev_bench_hello` is an identity cross-check — *is the board on the link the board
  the probe verified?* That is precisely the question an operator at a keyboard asks.

**Take the second arm only if the first turns out to be structurally impossible**,
and if so say exactly what blocks it in the task file rather than writing a decision
that ratifies the gap.

**Also fix in this unit** (both are one line each, same scope, and leaving them
costs a future reader more than they cost you now): `interfaces/tools.md`'s "no CLI
twin other than `versions`" line, which becomes false the moment you add the
subcommand; and `decisions/study-events.md`'s decision 48 entry, which still links
`[decision 47](surface.md)` after `api/036` moved 47 into `tool-wrapping.md`.

**Doc-size reserve for `api`, so you plan rather than discover.**
`decisions/tool-wrapping.md` is **12,222 / 12,288 B — 66 bytes left**, and its
compaction task `tasks/api/047` is `blocked` with `In flux: yes`. `open.md` is
4,734 / 5,120 (386 B) and `spec.md` is 9,087 / 10,240 (1,153 B), both parked under
`tasks/api/026`.

**Where your decision goes:** `decisions/shape.md` (7,654 / 12,288 — comfortable).
This is a decision about the *front-end shape* — what the CLI and MCP surfaces
guarantee about each other — which is what `shape.md` holds, not a per-tool wrapping
call. Decision 3/10 already lives there. **Do not write it into
`tool-wrapping.md`**; 66 bytes is not a home. If you conclude it genuinely belongs
in `tool-wrapping.md` anyway, then per `DOC-COMPACTION.md` §2 you compact that file
as part of this unit, carrying `tasks/api/047`'s entire `Must not delete:` list
forward and closing only that file's item — you are the actor making the flux, so
you are the only one who can shorten it safely. Say which you did and why.

**Reserve rule you owe:** if your work pushes any `api` file into reserve, or leaves
one there that nothing has filed, file `tasks/api/<next free NNN>-compact-api.md` in
the same commit.
