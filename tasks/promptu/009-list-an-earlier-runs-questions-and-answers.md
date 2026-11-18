# 009 — List the questions an earlier run of a prompt asked, and the answers

**State:** open
**Source:** EMB-185, filed by an audit after a rerun interview prompt asked the owner the same questions again and the session dug the earlier answers out of old transcripts with a throwaway script
**Issue:** EMB-185
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

A Promptu prompt whose mode is an interview ("interview me before proposing")
can be cut off part-way. When the owner reruns the same prompt, the new session
cannot see what the earlier run already asked or what he answered, so he answers
twice or a decision made in the first run is missed.

Add a read-only CLI verb, for example `promptu prior <prompt-file>
[--projects <dir>] [--json]`:

- **Input:** the prompt text (a file, or its Promptu footer) and a Claude Code
  transcript folder (`projects/<encoded cwd>/`). Default the folder the way
  Promptu's existing transcript readers do; take an explicit one with a flag.
- **Match:** a transcript belongs to the prompt when its first user turn is that
  prompt. Say in `spec.md` how the match works (the footer's run id where there
  is one, otherwise the text) and what it does with a near-match.
- **Output:** per earlier session, its start time, then each `AskUserQuestion`
  call in order: the question, its options, and the answer recorded in the
  `tool_result` that answered it. Numbers and text only; never another tool's
  output.
- **Never write.** It reads only the folder it is given.

Promptu already walks transcripts (`src/used.rs`); reuse its reader rather than
writing a second JSONL parser.

**Public repo.** Tests use synthetic JSONL fixtures in a temp folder. No real
transcript, no real login path.

**Burndown leg: no new numbered decision.** Record the verb in `spec.md` and
`interfaces.md`. A real design fork goes to `scripts/fleet-linear.py file --from
decision`.

**What you may change.** Only `embarch-promptu` and `embarch-doc/embarch-promptu/`.

**Doc reserve.** `embarch-promptu/decisions/patterns.md` is in reserve: 11,138
of 12,288 B, 1,150 B left. Its compaction task `tasks/promptu/008` is `blocked`
on `In flux: yes`. This unit should not need to touch it; if it must, compact
that file in the same unit, keeping `tasks/promptu/008`'s `Must not delete:`
list, and close only that file's item there.

## Why now

The owner moved EMB-185 to Fleet Ready.

## Done when

- [ ] Given a prompt and a transcript folder holding an earlier session started from it, the verb lists that session's `AskUserQuestion` questions, options and the owner's answers.
- [ ] A transcript started from a different prompt is not listed; a test covers it.
- [ ] The verb writes nothing and reads only the folder it is given.
- [ ] `spec.md` and `interfaces.md` name the verb, its match rule and its output.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
