# 007 — Promptu rewrites the rough prompt and keeps the original in its log

**State:** open
**Source:** EMB-196, the build of `embarch-promptu` decision 42 (owner, 2026-11-17)
**Issue:** EMB-196
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Today the pass picks a pattern, the dialog asks what is missing, and `render`
puts the rough prompt verbatim under Goal with the answers in the other five
sections (decision 9). A pasted brief keeps its text and gets only its gaps
answered (decision 24). Nothing is stored beyond the footer and the last answers
(decisions 13 and 27). The weekly loop compares the owner's edits against that
rendered prompt (decision 14).

Decision 42 (`decisions/patterns.md`) changes that. Build it:

- After the last question, Promptu writes a better prompt from the rough text,
  the answers and the plan, and that rewrite is what lands in the draft.
- The original rough prompt is kept in Promptu's log, one entry per run, beside
  the last answers in the state folder, and **one CLI verb prints it for a given
  run**. `embarch-chat`'s card (EMB-197, the next unit) calls that verb to
  restore the draft, so state its name, arguments, output and exit codes in
  `interfaces.md`.
- A pasted brief (`mode=brief`) is not rewritten: decision 24 stands for it.
- The weekly loop's edit signal compares the owner's edits against the rewrite.
- The footer says the prompt was rewritten, so a reader of the draft can tell.

Where to look: `src/run.rs` (rendering), `src/pass.rs` and `src/pass_system.md`
(what the pass returns), `src/state.rs` (the state folder), `src/footer.rs`, and
`embarch-doc/embarch-promptu/interfaces.md`.

**Which model rewrites and the wait after the last question are open in
decision 42, and stay the owner's.** Make the model a setting with a sensible
default, and record the model and the wait for each run where the build can
report them (the log entry is the natural place). Measuring p50 and p95 over at
least ten real prompts needs real `/promptu` runs, which this unit cannot make:
leave a command or a log query that computes both, and write the measurement
here as owed, owner-side.

**Burndown leg: no new numbered decision.** Decision 42 is the decision; record
the verb, the log's shape and the footer wording in `spec.md` and
`interfaces.md`. A design fork decision 42 does not settle is filed with
`scripts/fleet-linear.py file --from decision`, and you take the narrower
reading. Decisions 9 and 24 are amended by 42 already; if their text still
reads as current, add the "amended by 42" pointer, nothing more.

**What you may change.** Only `embarch-promptu` and `embarch-doc/embarch-promptu/`.

**Doc reserve.** Nothing of `embarch-promptu`'s is in reserve.

## Why now

The owner moved it to Fleet Ready with EMB-197, which depends on its CLI verb.

## Done when

- [ ] A rough prompt run through the pass lands in the draft rewritten, and a pasted brief lands with its text unchanged; tests cover both.
- [ ] Each run's original is in Promptu's log, and one CLI verb prints it for a given run; the verb is in `interfaces.md`.
- [ ] The weekly loop's edit input is the diff between the rewrite and what was sent.
- [ ] Each run records which model rewrote and the wait after the last question, and a command prints p50 and p95 over the logged runs; the real-prompt measurement is written here as owed.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
