# 070 — umbrella/068: a live claim about `embarch-api list-targets`'s output shape was cut with no home left

**State:** claimed by agent/umbrella/070-list-targets-output-shape-home, 2026-09-16 14:23
**Source:** embarch-reviewer on umbrella/068, filed to inbox/ and drained into the queue by leg 118; the Hardware claim was re-checked at drain and is correct. Originally: embarch-reviewer, umbrella/068 (merge `ad8d535`) — reading `embarch-umbrella/decisions/locate-api.md`#42's diff against `embarch-umbrella/decisions/schema-skew.md`#35
**Scope:** umbrella
**Hardware:** none — a documentation gap, not a hardware question. Confirming which check actually depends on the missing shape claim would need re-reading `embarch-api`'s `tools.rs`, not a board.
**Owner:** no

## What

`umbrella/068` cut this paragraph from decision 42 (`embarch-umbrella/decisions/locate-api.md`), justified in the commit and task file as duplicating `schema-skew.md`#35:

> `--json` and `--config` are top-level and must precede the subcommand — clap exits **2** otherwise, which is what [check 11](../../embarch-umbrella/decisions/schema-skew.md) reports as an `embarch-api` too old to know `versions`; `versions` answered `host_type_schema_version` **17**, Core's own number, from both binaries; **`list-targets` answered `{success: true, targets: [...]}` on exit 0 and `{success: false, error}` on exit 1, both on `stdout`, with its own log line on stderr.** Every shape checks 8 and 11 had only read off `embarch-api`'s source is therefore observed.

I read `schema-skew.md`#35 in full (`embarch-umbrella/decisions/schema-skew.md`, section "35 — Check 11 asks the located `embarch-api`..."). It confirms the `--json`-before-subcommand/clap-exit-2 claim and the `host_type_schema_version` v17 claim, sentence for sentence. **It says nothing about `list-targets` at all** — decision 35 is entirely about the `versions` subcommand that feeds check 11; `list-targets` feeds check 8 (`embarch-umbrella/decisions/projects.md`#17: "Check 8 runs `embarch-api --config <config> --json list-targets <project>` and passes on a non-empty `targets` array"). Decision 17 states check 8's pass/fail rule but never states the wire shape — exit codes, which stream `success`/`error` land on, or that there's a separate stderr log line.

I grepped the rest of the suite (`embarch-umbrella/`, `embarch-api/decisions/`) for `list-targets`/`list_targets`: the only other hits are `projects.md` (the pass/fail rule, no shape) and `mirrors.md` (a different command, `list-projects`). Nowhere else records that `list-targets` puts both its success and its error object on stdout, that failure is exit 1, or that there's a separate stderr log line — the fact that lets check 8 (or anything shelling out to `list-targets`) distinguish "no targets" from "process talked to the wrong stream."

## Why now

This is the `core/064` shape the leg is being watched for: a cut justified as "duplicates decision N" where the duplication is real for **part** of the removed text (the `versions`/clap portion) but not for all of it (the `list-targets` portion). The task file's own hunk-6 quote from decision 35 only ever quotes the `versions`/clap sentences back — it never produces a decision-35 sentence that covers `list-targets`, because there isn't one. The claim now exists nowhere in `embarch-doc`.

This is a refinement, not a decision contradiction — nothing in the surviving text asserts the opposite of the cut claim — so it is not a revert-worthy defect on its own. It is exactly the class the charter asks to flag anyway: a live claim about another component's behaviour that a compaction pass mis-classified as provenance and that now has no home.

## Dispatch note — leg 119, 2026-09-16

**Decision 42 has almost no room, and that is the first thing to know.** `umbrella/068` compacted
`locate-api.md`#42 to **4,019 B against the 4,096 B per-decision cap — 77 B of margin**, the thinnest
entry that leg produced. The paragraph you are restoring is several hundred bytes. **So "restore it
into decision 42" is very likely not available**, and `projects.md`#17 next to check 8's pass/fail
rule is the home to price first. Measure `projects.md`#17's own size before you write into it, and
say the before/after bytes and the margin left for whichever entry you touch. **Do not add a pin to
`scripts/decision-size-baseline.json`** — `scripts/` is owner-reserved and pinning is the
papering-over move.

**In reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` is 11,533/12,288 B, **755 B of
headroom**, filed against `tasks/umbrella/009-compact-docs.md` (blocked). You are not writing that
file. Two `umbrella` decisions are also over the per-decision cap and are **not yours** —
`mirrors.md`#16 (4,347 B) and `sticky-host.md`#48 — both filed as `tasks/umbrella/069`; leave them
alone. If your work pushes any file into reserve or leaves one there unfiled, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit (`scripts/check-task-numbers.py --next
umbrella` for the number — **do not read the directory**).

**The rule this leg is watching.** If you justify a cut, or a decision that something is already
stated elsewhere, by pointing at another decision, **open that decision and confirm it covers the
whole hunk sentence by sentence, not the topic.** That is the exact defect that produced this task.

## Done when

- [ ] Either the `list-targets` shape claim (exit 0 with `{success: true, targets: [...]}`, exit 1 with `{success: false, error}`, both on stdout, log line on stderr) is restored somewhere it can be cited from — decision 42 itself, or `projects.md`#17 next to check 8's pass/fail rule — or someone determines the claim really is redundant with something I missed and says where.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Not filed as a contradiction

Everything else checked out: decision 49's two live open questions ("whether the nine vendor IDs are the right nine", the wrong-machine "why not" argument) survive in force; decision 42's "neither check 8 nor check 11 has run inside a live `doctor` yet" survives and `suite/features.md` line 149 / `features.d/umbrella-030-*.md`'s citation to it still resolves; the vendor-name table row cut from decision 49 is genuinely redundant with `doctor.md`#18, which states the same nine names verbatim (checked). No decision reads as contradicted or retired.
