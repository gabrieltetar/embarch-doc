# 100 — The umbrella README says "LLM coding agent", not "AI coding agent"

**State:** open
**Source:** Fleet Ready issue: the owner chose "LLM" over "AI" for every EmbArch doc in EmbArch's own voice (`notes/goals/01-scope.md`, "LLM", not "AI").
**Issue:** EMB-194
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

EmbArch's own voice says "LLM coding agent", or "LLM agent" where "coding" adds nothing, never "AI coding agent". A whole-word search for `AI` over the suite's Markdown (history, `changelog.d/` and vendored trees excluded) finds three places in EmbArch's own voice, and every other match is a quote, a product or company name, or landscape research, which keep their words:

- `embarch-umbrella/README.md`, the opening paragraph: "from a terminal or from an AI coding agent". **This repo, so yours to change.**
- `embarch-doc/suite/agent-guide.md`, the Status line: "letting an AI coding agent drive EmbArch".
- `embarch-doc/suite/user-guide.md`, the opening paragraph: "including from an AI coding agent".

The two `suite/` docs are shared suite-level docs, which a worker never edits. Write one `status.d/` fragment per doc instead (`status.d/README.md` has the three-line shape: `Target`, `Was` quoted exactly, `Now`), named `status.d/umbrella-llm-agent-guide.md` and `status.d/umbrella-llm-user-guide.md`, and the supervisor folds them when it lands this unit.

## Why now

The owner moved the issue to Fleet Ready. `notes/goals/` already says "LLM" throughout, so these three lines are what is left.

## Dispatch notes

- `embarch-doc/embarch-umbrella/spec.md` is in reserve (9147 of 10240 B) and its compaction (`tasks/umbrella/099`) is parked on `In flux: yes`. This task should not need to touch it; if it does, stop and say so in this file rather than editing it.
- Burndown: no new numbered decision. None should be needed.
- Run the whole-word search yourself on both repos before you finish (`grep -rnw --include='*.md' AI`, excluding `history/`, `changelog.d/`, `embarch-atlas/research/`, `notes/hil/11-prior-art.md` and any vendored tree) and say in this file what it found.

## Done when

- [ ] `embarch-umbrella/README.md` reads "LLM coding agent" (or "LLM agent") where it said "AI coding agent".
- [ ] Two `status.d/` fragments name the exact `Was` text of the two `suite/` lines and what each should say.
- [ ] The whole-word search over embarch-doc's and embarch-umbrella's Markdown finds `AI` only in a quote, a product or company name, the landscape research, or the two lines the fragments cover.
- [ ] Gate green (`../../embarch-fleet/gate.md`: cargo, client names on the code repo, `check-docs.py`, ownership on both branches).
