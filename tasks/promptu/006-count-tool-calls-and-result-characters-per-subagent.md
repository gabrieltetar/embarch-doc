# 006 — Count a session's tool calls and result characters per subagent and activity

**State:** open
**Source:** EMB-149, filed by an audit after a lookup replay (atlas task 002) needed yet another throwaway counting script
**Issue:** EMB-149
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Every replay of recorded sessions rewrites the same throwaway script to count a
session's tool calls and result characters per subagent, and each draws its
class boundaries differently: the same eight review rounds came out at 63 to 78
calls under one script and 33 to 133 under another. Give `promptu` one command
for it, so a before/after replay is a measurement.

It reads Claude Code transcripts: a session's main `<session>.jsonl` and its
`<session>/subagents/*.jsonl`, with each subagent's `*.meta.json` description.
It reports, per subagent (and for the main thread):

- the number of tool calls and the total characters of their results, joining
  each `tool_use` to its `tool_result` by id;
- the same split by activity class: reads a source tree, runs git history (`git
  log`, `git diff`, `git show <rev>:`), reads Kconfig, devicetree or manifest
  files, builds, and an `other` class for the rest;
- with a class selected, that class's calls one per line with their result size,
  so a replay can map each one to the call that replaces it.

The issue's direction, which you may improve on and must say so if you do: a
verb such as `promptu calls <session> [--subagent <id>] [--class <name>]`, with
the class rules in one table. `src/used.rs` already finds and walks the
transcripts Claude Code keeps; reuse it rather than writing a second walker.

**Public repo.** Tests use synthetic transcript fixtures only; never a real
transcript.

**Burndown leg: no new numbered decision.** Describe the verb in `spec.md` and
`interfaces.md`. If its shape needs a design choice that would normally be a
numbered decision, write it under a `## Withheld decision` heading in this file
and leave `decisions.md` alone; the supervisor files it.

**What you may change.** Only `embarch-promptu` and `embarch-doc/embarch-promptu/`.

**Doc reserve.** Nothing of `embarch-promptu`'s is in reserve.

## Why now

The owner moved it to Fleet Ready; atlas lookups are measured by exactly this
count, and a measurement that changes with the script is not one.

## Done when

- [ ] One command prints calls and result characters per subagent of a session, and per activity class.
- [ ] The class rules are defined in one place, and a test pins what each class matches.
- [ ] It lists one class's calls with their result sizes, for a replay to map.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`interfaces.md` updated, `changelog.d/` fragment dropped.
