# 070 — umbrella/068: a live claim about `embarch-api list-targets`'s output shape was cut with no home left

**State:** open
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

## Done when

- [ ] Either the `list-targets` shape claim (exit 0 with `{success: true, targets: [...]}`, exit 1 with `{success: false, error}`, both on stdout, log line on stderr) is restored somewhere it can be cited from — decision 42 itself, or `projects.md`#17 next to check 8's pass/fail rule — or someone determines the claim really is redundant with something I missed and says where.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Not filed as a contradiction

Everything else checked out: decision 49's two live open questions ("whether the nine vendor IDs are the right nine", the wrong-machine "why not" argument) survive in force; decision 42's "neither check 8 nor check 11 has run inside a live `doctor` yet" survives and `suite/features.md` line 149 / `features.d/umbrella-030-*.md`'s citation to it still resolves; the vendor-name table row cut from decision 49 is genuinely redundant with `doctor.md`#18, which states the same nine names verbatim (checked). No decision reads as contradicted or retired.
