# 003 — `embarch-promptu` decision 40 follows the chat rail's one-colour icons

**State:** claimed by agent/promptu/003-decision-40-follows-the-one-colour-rail, 2026-11-09 19:48 — unparked 2026-11-09 by `chat/009`'s fold: the rail draws one-colour SVGs in `currentColor` (embarch-chat `468547a`), and `embarch-chat` decision 94 now says so and names this task for the promptu side.
**Source:** Linear issue EMB-56, filed by the owner — the owner changing his own earlier pick
**Issue:** EMB-56
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

`embarch-promptu` decision 40 ("The rail's icons are emoji at the bottom, beside the input") no longer says the rail's icons are emoji. It says they are one-colour SVGs drawn in `currentColor`, as `embarch-chat` decision 94 now records (`tasks/chat/009`), and keeps whatever else it decided, the rail's placement included.

This is the Promptu half of EMB-56. The code change and `embarch-chat` decision 94's amendment are `tasks/chat/009`.

## Why now

EMB-56's last `Done when` asks for both decisions amended. A decision that names emoji the code no longer draws misleads the next reader.

## Dispatch notes

- **Doc only.** The `embarch-promptu` worktree is there to read; leave it clean and do not push it.
- Amend in place, dated the day `tasks/chat/009` landed (its fold commit shows it); do not append a new decision.
- Check `embarch-promptu/spec.md` and `interfaces.md` for the same emoji and correct them too.
- **In reserve:** `embarch-promptu/spec.md` (9,564/10,240 B, 676 B left), parked as `tasks/promptu/004` (`blocked`, `In flux: yes`). A grep at dispatch found the word "emoji" only in `decisions/chat.md`, so you should not need to touch `spec.md`. If you do, the edit must leave it no larger, and keep `promptu/004`'s `Must not delete:` items.
- **Burndown leg: no new numbered decision.** This task amends decision 40 in place, which is fine.
- Close by rewriting the `State:` line so `done` (or `blocked`) is its first word with nothing glued to it — `done,` and a left-over `claimed` are both refused by `check-task-state.py`.

## Done when

- [ ] Decision 40 describes the rail's icons as `embarch-chat` decision 94 now does.
- [ ] No `embarch-promptu` doc names the rail's emoji as current.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
