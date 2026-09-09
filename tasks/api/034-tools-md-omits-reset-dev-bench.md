# `interfaces/tools.md` omits `reset_dev_bench`; add a CLI↔MCP parity test

**State:** claimed — leg 057, 2026-09-09, `agent/api/034-tools-md-reset-dev-bench`
**Source:** owner's repo survey, 2026-09-06 — `interfaces/tools.md:5`'s own premise is unchecked
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`src/tools.rs:772-790` defines the `reset_dev_bench` MCP tool and `src/main.rs:325` /
`src/cli.rs:91` its `reset-dev-bench` CLI half. `embarch-doc/embarch-api/interfaces/tools.md:40-44`'s
"Dev bench" table lists only the three build/flash tools. The doc's whole premise is "**One table,
because these are two front-ends over one implementation** — not two surfaces to keep in sync"
(`tools.md:5`), and nothing checks it.

Add the missing row, carrying the reason the tool description already gives (flashing halts the
core rather than starting it running). Then add a test that derives the tool list from
`include_str!("../src/tools.rs")` and the subcommand list from `include_str!("../src/main.rs")` and
asserts every tool has a kebab-case subcommand — with the two documented asymmetries (`versions`
CLI-only, `study_watch` reached as `study-status --follow`) as a **named constant with a comment**
pointing at `spec.md` §1, never an inline skip.

## Doc-size reserve in `embarch-api`, at dispatch (leg 057, 2026-09-09) — read this before you write a doc line

**`embarch-api` is the tightest sub-project in the suite and four of its files are in reserve behind
`blocked` compaction tasks you may not do:**

| file | size | left | filed under |
|---|---|---|---|
| `decisions/tool-wrapping.md` | 12,222 / 12,288 B | **66 B** | `tasks/api/047` — **blocked** |
| `decisions/core-link.md` | 12,076 / 12,288 B | **212 B** | `tasks/api/026` — **blocked** |
| `open.md` | 4,802 / 5,120 B | **318 B** | `tasks/api/026` — **blocked** |
| `spec.md` | 9,350 / 10,240 B | **890 B** | `tasks/api/026` — **blocked** |
| `decisions/build.md` | 11,134 / 12,288 B | 1,154 B | `tasks/api/050` — **blocked** |

`interfaces/tools.md`, the file this task's main edit belongs in, is **10,329 B and not in reserve**
— that is where the new `reset_dev_bench` row goes and there is room for it.

**So: keep this unit's doc footprint inside `interfaces/tools.md` if you possibly can.** The
`spec.md`/`decisions.md`/`open.md` line in "Done when" below is boilerplate, not a requirement to
write to all three: update one only if this change makes something in it *false*. `decisions.md` is
a 2,919 B index and is not tight.

**If you genuinely must spend the reserve on `spec.md` or `open.md`**, `DOC-COMPACTION.md` §2 and
`.claude/leg.md` say what you owe: compact that file as part of this same unit, carrying
`tasks/api/026-compact-api.md`'s `Must not delete:` list forward and closing only the item for the
file you touched. Do **not** touch `decisions/tool-wrapping.md` (66 B) or `decisions/core-link.md`
(212 B) at all — at those margins an edit is a cap failure. `api/026`'s park is about the event
stream (decisions 48/49, since split into `decisions/study-events.md`) and it still stands.

**This leg runs in burndown, which forbids authoring a new numbered decision.** This unit is a
missing doc row plus a parity test over existing, already-decided behaviour; it should need none. If
you conclude one is needed, stop and say so in your report rather than writing it. Recording the
test's two documented asymmetries as a named constant pointing at `spec.md` §1 is *citing* an
existing decision, not making one — that is in scope and is what the task asks for.

## Why now

`spec.md` §1 asserts the CLI is a superset with "`versions` having no tool", and
`suite/studies-guide.md:45` already tells an engineer to run `reset-dev-bench` — a command the
interface reference does not list.

## Done when

- [ ] `interfaces/tools.md`'s Dev bench table lists `reset_dev_bench`.
- [ ] One test fails if a new `#[tool]` gains no matching `Commands::` variant, or vice versa,
      outside the two named exceptions.
- [ ] The exception list is a named constant with a comment, not an inline skip.
- [ ] `tools.md` stays inside its size cap.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
