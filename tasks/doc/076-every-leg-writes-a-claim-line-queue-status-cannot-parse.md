# 076 — Every leg writes a claim line `queue-status.py` cannot parse, so a live claim reports as `recoverable` with no branch

**State:** done — `.claude/leg.md` quotes the claim line at the claim step; `tasks/README.md` says the `claimed by agent/<scope>/<NNN-slug>, <yyyy-mm-dd HH:MM>` prefix is the only parsed part and anything after it is prose (not a leg number: since `tasks/doc/054` a leg has none); the improvised form is deliberately not a second grammar. The gate that refuses a malformed claim is `tasks/doc/084`. embarch-fleet `56f35e5`.
**Source:** leg 132, 2026-09-17. Found by running `queue-status.py` against this leg's own two live
claims.
**Scope:** doc
**Hardware:** none — a format mismatch between a doc, a script and what every leg actually writes.
Nothing is built, no board, no probe, no live Core.
**Owner:** required — the fix belongs in `.claude/leg.md` (generated from
`embarch-fleet/scripts/install.py`'s template) and possibly in `scripts/queue-status.py`. Both are
owner-reserved, and a supervisor that rewrote the instruction telling it how to claim would be
rewriting its own interlock. Filed rather than fixed.

## What

`tasks/README.md:81` states the claim format exactly:

> - **claimed** — the claim line becomes
>   `**State:** claimed by agent/<scope>/<NNN-slug>, <yyyy-mm-dd HH:MM>`.

**No recent leg has written that.** The form actually in the history is
`**State:** claimed (leg NNN unit N)` — leg 132's own first two units wrote it, and
`git log` shows the same shape in earlier legs' claim commits (`claim suite/042 (leg 130 unit 4)`,
`claim topology/054 (leg 132 unit 2)`). Against that form `queue-status.py` prints, for each live
claim:

```
  recoverable api    ./tasks/api/107-....md
              -> claim line carries no parseable timestamp; branch None
```

Corrected to the documented form, the same two tasks immediately read `claimed ... (respected)`.

## Why it costs something

**The branch name is the one thing a recovery needs and the one thing the improvised form drops.**
`.claude/leg.md`'s step 0 tells a successor to reclaim stale claims, and `tasks/README.md` settles
staleness by the process tree — *"if no supervisor is running, every claim is stale"*. So a leg that
dies mid-flight leaves claims its successor must reclaim, and with `branch None` the successor has
no handle on the `agent/*` branch that may already carry finished, pushed work. `.claude/leg.md`
separately makes a pushed branch with commits the one legal positive signal that a worker finished
— **the recovery path and the claim line disagree about whether the branch name is recorded
anywhere.**

`recoverable` for a claim held by a *live* worker is also exactly the reading that produced the
double-dispatch of leg 012 (`umbrella/012` run twice, concurrently, in the same trees). Nothing went
wrong here because one supervisor was alive and respected its own claims — but the classification a
script hands the next leg should not depend on that.

## Where the mismatch actually lives

`.claude/leg.md` says only *"Claim it — commit the state line before dispatch"* and **never gives
the format**, so every leg improvises the same wrong thing. That is the likely root: the format is
documented in `tasks/README.md`, which a supervisor reads for task *shape*, and not in the file it
reads for what to *do*. Possibly related to `tasks/doc/054` (the leg number a leg writes into claims
is self-assigned) — the `(leg NNN unit N)` suffix is where that self-assigned number is going.

## Done when

- [x] A supervisor following `.claude/leg.md` alone writes a claim line `queue-status.py` parses —
      by the template naming the format, or by the format being quoted where the claim step is.
- [x] Decided and recorded: is `(leg NNN unit N)` worth keeping as a **suffix** after the
      documented prefix (leg 132 kept it, and it is useful for reading `git log`), or should it go?
      Either is fine; what is not fine is it replacing the parseable part.
- [x] Checked whether `queue-status.py` should *also* accept the improvised form, given how much of
      the history is in it — or deliberately not, so the format stays single.
- [x] Checked against `tasks/doc/054` for whether these are one defect.

## Not yours

Do not retrofit older task files. The claims that matter are live ones, and a historical `done` task
whose claim line was never parseable costs nothing. Leg 132 corrected only its own two in-flight
claims and left `tasks/README.md` untouched.

## Shipped

- **Format quoted where a leg acts on it**: the claim step in `.claude/leg.md` now carries the
  line verbatim, with the reason a different shape is dangerous.
- **`(leg NNN unit N)` may follow the time as prose, never replace the prefix.** `tasks/README.md`
  names the prefix as the only parsed part. Since `tasks/doc/054` (embarch-fleet `9cd022a`) a leg
  has no number, so the README's example of a suffix is a window's `ts`, not a leg number.
- **The improvised form is not accepted.** Measured: before 2026-09-18, 253 of 509 claim lines
  used another shape and 146 of those named no branch anywhere, so a wider parser would have read
  them as claimed with nothing to recover. Since 2026-09-18 it is 1 of 156 (a `suite` claim
  written `claimed by the supervisor`). `queue-status.py`'s pattern now also requires the
  `agent/` branch; over all 666 historic claim lines it accepts exactly the same 411.
- **Not one defect with `tasks/doc/054`.** 054 is what the leg number *is*; this was the number
  displacing the parsed prefix. With the prefix mandatory the number is unparsed prose, so 054's
  choice could not break a claim; it has since dropped the number (embarch-fleet `9cd022a`).
