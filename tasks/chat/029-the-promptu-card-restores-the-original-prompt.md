# 029 — The Promptu card restores the original prompt after a rewrite

**State:** open
**Source:** EMB-197, filed by the owner once `embarch-promptu` decision 42 made Promptu rewrite the rendered prompt
**Issue:** EMB-197
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

Since `embarch-promptu` decision 42, `promptu render` may rewrite the
structured prompt, and the rewrite is what lands in the chat's draft. The
original the owner typed is kept in Promptu's per-run log, and
`promptu original <run> [--json]` prints it (Promptu's contract §8.4 to §8.6,
landed with `tasks/promptu/007`).

Give the Promptu card (`webview/chat/promptu.tsx`) one action that replaces the
draft with that original, verbatim:

- It reads the original through `promptu original <run>`, called the way
  `src/promptu/cli.ts` calls every other Promptu verb, for the run the chat
  itself just rendered (`src/promptu/runs.ts` holds the run id it passed to
  `render`). Never read Promptu's log files directly.
- It shows only while the draft holds a rewrite from that run. Read whether a
  run was rewritten from what `render` already returns or from the footer
  (`rewritten=yes`); confirm which in Promptu's contract before relying on it.
  A run that was not rewritten (a pasted brief, an offline run, rewrite off)
  shows no action.
- It asks nothing: one click, the draft is the original.

If the chat cannot learn the run id or the rewritten flag from what Promptu
already hands it, stop and report it: that is a change in `embarch-promptu`,
which this unit may not make.

**Public repo.** Tests use a fake `promptu` the way the existing Promptu tests
do; no real prompt text.

**Burndown leg: no new numbered decision.** Record the card's behaviour where
the card is already described. **`decisions/promptu.md` decision 96 has 204 B
left**; do not grow it. If the behaviour has to sit in a decision entry, amend
in place within the limit or put it in `spec` and point to it. A real design
fork goes to `scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-chat` and `embarch-doc/embarch-chat/`.

**Doc reserve.** Nothing of `embarch-chat`'s is in reserve; decision 96's
headroom is above.

## Why now

The owner moved EMB-197 to Fleet Ready. It waited for EMB-196's read-back verb,
which landed with `tasks/promptu/007`, and for `tasks/chat/028`, which landed
2026-11-17.

## Done when

- [ ] After a rewritten run, the card's restore action puts the original prompt in the draft, verbatim.
- [ ] The action is absent for a run that was not rewritten, such as a pasted brief.
- [ ] A webview check covers both cases.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
