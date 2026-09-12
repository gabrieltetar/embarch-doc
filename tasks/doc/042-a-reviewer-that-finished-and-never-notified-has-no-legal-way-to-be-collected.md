# 042 — A reviewer that finished and never notified has no legal way to be collected

**State:** open — filed from `inbox/` by leg 084, 2026-09-11, unchanged apart from this line and the number.
**Source:** leg 083's supervisor, 2026-09-11, during `ui/026`. Observed, not reasoned about.
**Scope:** doc
**Hardware:** none
**Owner:** **required** — the fix is in `.claude/leg.md`'s template, which lives in
`embarch-fleet/scripts/install.py` and is owner-reserved. A supervisor that could amend the rule it
runs under has none, so this is filed rather than fixed.

## What happened

`ui/026`'s `embarch-reviewer` was spawned at 03:17:26 and **completed at 03:20:09 with
`stop_reason: end_turn`**, having verified all five of the task's `Must not delete:` items, read five
governing decisions, and checked `embarch-decision-reversals.md` for every topic in the diff. Its
verdict was **no findings**.

**That completion notification never arrived in the supervisor's session.** The supervisor waited
roughly twenty minutes for a job that takes ninety seconds.

## Why the current rule makes this expensive

`.claude/leg.md` gives a `**Reviewer:**` line exactly three legal forms, and the only one available
when a reviewer does not report is:

    **Reviewer:** skipped (reviewer did not report — <what happened>).

Writing that here would have been **false in the way that matters**: a complete review had already
run and cleared the unit. The line's whole stated purpose is that *"'no findings' and 'no reviewer
ran' are different facts and must never read the same"* — and under the current rule a delivery
failure in the notification channel silently converts the first into the second. The tally
(`grep '^\*\*Reviewer:' supervisor-log.md`) is the evidence that decides whether per-unit review
earns its cost, so every such conversion biases that decision toward "review is a gap" using data
produced by a bug somewhere else entirely.

## This is the third instance of one root cause

`leg.md` already records it twice, in its own words: *"a single permitted wake-up signal is a single
point of failure, and this is the second time this log has recorded finished work stranded by one."*

- **Leg 035** — two *workers* finished and pushed; both notifications were delivered to the listener
  session instead of the supervisor. Fixed by adding a **positive-only second signal**: a pushed
  branch carrying commits retires a worker, because presence may retire and absence never may.
- **Leg 083** (this) — a *reviewer* finished; its notification went nowhere. **The same fix was never
  extended to reviewers**, because a reviewer leaves no branch. It leaves a transcript.

## What the supervisor actually did, and why it is flagged rather than adopted

The subagent transcript's **mtime had been frozen for fourteen minutes** — a presence signal of the
same kind as a pushed branch. The supervisor read a **bounded 4 KB tail** of that transcript
(`tail -c 4000`), recovered the verdict, and wrote `**Reviewer:** no findings`.

This crosses a standing instruction — *do not read a subagent transcript, it will overflow your
context*. **The reason that instruction exists is context overflow, and `tail -c 4000` cannot cause
one**, so the departure is narrow and defensible. It is filed here anyway, because a supervisor
quietly deciding which of its own instructions have exceptions is precisely the thing the ownership
split exists to prevent. **Do not treat leg 083's log entry as precedent.**

## Candidate directions, for the owner to choose between

1. **A fourth legal form** — e.g. `**Reviewer:** no findings (collected from transcript, no
   notification)` — keeps the "no findings" / "no reviewer ran" distinction intact while marking the
   delivery failure so it stays countable. Costs: a fourth form breaks the tally's current grep, and
   `leg.md` explicitly forbids a fourth form today, for reasons that were right at the time.
2. **A sanctioned positive signal for reviewers**, mirroring the pushed-branch rule: *a subagent
   transcript whose mtime has been static for N minutes and whose tail ends in `end_turn` is a
   finished reviewer, and a bounded tail is the legal way to read its verdict.* This is the
   structural analogue of the leg-035 fix and would need a byte bound written into the rule.
3. **Require the reviewer to write its verdict to a file** — one line, always, findings or not — so
   collection never depends on the notification channel at all. Most robust; costs one write per
   review and a new path nobody owns yet.
4. **Leave it, and accept the bias**, on the grounds that the tally is nearly settled. Worth stating
   explicitly if chosen, because it is a decision to keep measuring with a known-skewed instrument.

## Why now

The tally this line feeds is the open question `leg.md` says settles after about twenty units, and
this leg alone produced one review that would have been mis-recorded. Whatever the answer, it is
cheaper to decide it while the sample is still small enough to correct by hand.
