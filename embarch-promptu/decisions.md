# embarch-promptu: decisions

**Status:** active, 2026-10-30.

Why Promptu is shaped this way. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). 1–17 are the design the owner approved on 2026-10-29, after a research pass over published prompting practice, prior tools and his own sessions; they hold from build step 1 on, and the step that builds each one may refine it here. 18–21 are his answers the same evening to four forks step 1 raised. Cite them as `embarch-promptu decision N`. 22–24 are his answers to build step 2's measurement and its first forks, 25–28 and 31 his answers to its later forks, and 29–30 his requirement that Promptu work without the rest of EmbArch. 32–33 were built in step 3 where the design left the mechanics open; on 2026-10-30 the owner amended 33 and answered step 3's forks as 34–40. Choices the design leaves open are in the repo's `docs/forks.md` until the owner picks: F1–F4 (18–21), S1–S8 (22–28, 31) and P1–P11, P13, P14 (33–40) are decided, and P16–P17 too, recorded in `embarch-chat` decisions 94 and 99; F5–F10, P12, P15, P18–P19 are open.

The entries live in one file per mission:

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/what.md](decisions/what.md) | 1, 29, 2, 3, 20 | What Promptu is and owns, what it stands beside, and how it ships. |
| [decisions/memory.md](decisions/memory.md) | 4, 5, 6, 18, 21, 7, 8 | The labels, the hook and its checks, the inventory the memory menu draws. |
| [decisions/patterns.md](decisions/patterns.md) | 9, 22, 10, 11, 23, 24, 25, 26, 27, 28, 31, 12, 13 | The pass, the guard, the patterns and their questions, paging, the footer. |
| [decisions/learning.md](decisions/learning.md) | 14, 30, 15 | The weekly sheet and what it learns from. |
| [decisions/chat.md](decisions/chat.md) | 16, 17, 19, 32, 33, 34, 35, 36, 37, 38, 39, 40 | Promptu in `embarch-chat` and on desk Start work: step 3, and the owner's answers to its forks. |
