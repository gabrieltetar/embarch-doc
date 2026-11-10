# embarch-desk: constants, continued

**Status:** active, 2026-11-09. Split out of [../spec.md](../spec.md) §4 on 2026-11-09, verbatim, when that file reached its reserve line. The table continues there from "Refresh".

| Constant | Value |
|---|---|
| Harvest entries | today every 2 min; a day with a waiting tile 10 min [chosen] and again at ✓ (62) |
| Reference index | 1,000 issues; 300 PRs per repo; each desk every 5 min, by its own task's pass every 30 s (56) |
| Harvest entries read | 2,000 per account per call, paged by 100; `truncated` when cut [chosen] (59) |
| Open issues read, assigned or all | 500 per workspace, paged by 50; `truncated` when cut [chosen] (59, 71) |
| Acted-on tiles archived to `history/YYYY-MM.jsonl` | after 7 days |
| Least time after a ✓ dealt as a continuation | 5 min [chosen] (64) |
| Brief | 16,000 characters, about 4K tokens (48) |
| Mailbox entry life | 10 min, as a launch claim (46); an `end` or `unfinished` waits for its window or folder, and once taken is kept 10 min (83) [chosen] |
| Memory note versions kept | 20 per file (52) |
| Notes, worst case | 8.2 MB of state, 20 ms a write [measured 2026-10-23] (55) |
| Polish model | `sonnet`, `EMBARCH_DESK_MODEL` |
| `claude -p` cost, stripped | $0.0007 for a trivial prompt [measured 2026-10-22], against $0.20 unstripped ([decision 19](../decisions.md)) |
