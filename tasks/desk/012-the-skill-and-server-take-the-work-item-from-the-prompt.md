# 012 — The desk skill and the server instructions take the work item from the prompt first

**State:** open
**Source:** Linear issue EMB-105, filed by a reviewer of `tasks/desk/009`
**Issue:** EMB-105
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

Every text the desk gives a session about an unset work item says what the start hook already says (decision 7 as amended for EMB-16): an issue key of a connected team found in the opening prompt or a handoff is set with `desk_set_work_item` without asking, the session says which in one line, and the user is asked only when there is no such key.

Today the hook text (`ask_text` in `src/events.rs`) says that, but three other texts still say only "ask the user":

- `plugin/skills/desk/SKILL.md`, "The work item", step 1.
- `src/mcp.rs`, the server instructions string, its last sentence ("when the desk asks which work item a session is on, ask the user and call desk_set_work_item").
- `src/mcp.rs`, the two tool replies that tell a session with no item "Ask the user which one it is and call desk_set_work_item" (around the `ask` strings).

## Why now

A session reads the skill and the server instructions as well as the hook, so it sees two rules for one moment. Found while reviewing the unit that amended decision 7.

## Where to look

- `src/events.rs` `ask_text` — the wording to match, including that a lookalike key in prose does not count and `linear_teams` names the connected teams
- `plugin/skills/desk/SKILL.md` — "The work item"
- `src/mcp.rs` — the instructions string and the two `ask` replies
- The tests that assert on any of these strings

## Dispatch notes

- This amends no decision and adds none: decision 7 already says it. If the worker finds a text whose change needs a new decision, it files an issue (`fleet-linear.py file --from decision`) and leaves that text alone; this leg runs in burndown, which authors no new numbered decision.
- No `embarch-desk` doc is in reserve at the split.

## Done when

- [ ] The skill's work-item step, the server instructions and both tool replies say a key in the prompt or a handoff is taken before the user is asked.
- [ ] None of them tells a session to ask when a valid key is already present.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `embarch-desk` docs updated if they quote the old wording; `changelog.d/` fragment dropped.
