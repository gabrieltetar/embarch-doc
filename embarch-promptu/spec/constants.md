# embarch-promptu spec: constants

**Status:** active, 2026-10-30.

Split verbatim from [../spec.md](../spec.md) §4 on 2026-10-30, under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: `spec.md` had 14 bytes before its reserve when build step 3's status had to go into it. The table is unchanged. Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

| Constant | Value |
|---|---|
| Hook call, release build, through `sh -c` as Claude Code runs it | p50 0.9–1.0 ms, p95 under 1.4 ms [measured 2026-10-29, WSL2, 300 calls per case] |
| Hook timeout in `hooks.json` | 5 s |
| Index line limit | 150 characters |
| `review-by` horizon | after today, at most 90 days |
| Memory id | first 6 hex digits of the SHA-1 of the topic file's name |
| The pass, Sonnet 5.5 at effort medium | wall p50 3.9 s, p95 7.3 s; 18 of 20 picks right; about $0.02 a run [measured 2026-10-29, 23 of the owner's prompts]; timeout 15 s |
| `promptu render` / `prep` without the model, release build | p50 3.1 ms / 7.2 ms; the hook unchanged at p50 0.66 ms [measured 2026-10-29, WSL2] |
| A dialog page | at most 4 questions: 3 plus "Rest" while more remain |
