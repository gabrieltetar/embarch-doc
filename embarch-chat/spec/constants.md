# embarch-chat spec: constants

**Status:** active, 2026-10-30.

Split verbatim from [../spec.md](../spec.md) §4 on 2026-10-30, under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: `spec.md` had 10 bytes before its reserve when `embarch-promptu`'s build step 3 had to write into it. The table is unchanged, plus Promptu's rows. Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

| Constant | Value |
|---|---|
| Idle close | 5 min, `embarchChat.idleMinutes` (41) |
| The column | 80 % of the pane, never under 56rem, centred; prose 64rem; gutter and step indent `clamp(8px, 2.5vw, 16px)` (91) |
| Full resume | ready 0.66 s, first token 1.46 s [measured 2026-10-22] |
| Memory per chat process | 457 MB full, 242 MB stripped [measured 2026-10-22] |
| Prompt cache a reply writes | 1 hour [measured 2026-10-23, every recorded reply] (69) |
| Thread list poll | 3 s visible, 15 s hidden; mailbox 3 s; past chats 30 s |
| Reload window | 90 s; at most 2 reruns; none for a step over 1 h (63) |
| Autosave wait | 5 s, then the tool goes on (61) |
| Tested `claude` | 2.1.287–2.1.308; outside it, one line of warning (30) |
| Assistant | ghost text after a 300 ms pause, first token 0.82–0.89 s; cards on a 2 s pause, 3.8 s; chips and name 2.6 s; $0.002–0.004 a call [measured as built] (26) |
| Cards with the desk's references | 2.34 s median, a replace naming the PR 8 of 8 [measured 2026-10-25 on a synthetic vague-PR case; 3.9 s and a question before] (88) |
| `<desk_references>` block | at most 8 lines, about 600 tokens; a title clipped at 90 characters (88) |
| Things a folded run lists | 3, then "N more" (87) |
| Send held for cards | up to 4.5 s, drafts of six words or more (26) |
| Terminal context | last 100 lines (58) |
| Paste marked as pasted | over 800 characters or 2 line breaks (56) |
| Usage banner | from 70 % (67) |
| Not responding | 60 s without a CLI line while a turn runs (68) |
| Transcripts | Claude Code's 30 days (12) |
| Long chat | 60 turns, 600 steps: a delta 3.5 ms p50, frame p95 17 ms [measured 2026-10-23] (85) |
| The rail | 30 px folded, 140 px under the pointer (94) |
| Promptu's commands' time limits | `prep` 40 s (the pass's own is 15 s), `next` and `render` 10 s, `memory` 20 s [assumed] (96, 98) |
| A work item's brief for the pass | 2,000 characters, as the terminal skill cuts it (96) |
