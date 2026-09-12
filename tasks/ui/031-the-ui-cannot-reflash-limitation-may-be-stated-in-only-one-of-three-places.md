# 031 — "The UI cannot reflash" is a limitation, and `open.md` asserts the run dialog says so — check that it does

**State:** claimed by agent/ui/031-reflash-limitation-stated, 2026-09-12 01:21
**Source:** `embarch-ui/open.md` — "**Where the reflash selector should live is genuinely
undecided.** … Settled as the third for now (the run dialog says so) — 'the UI cannot reflash' is a
limitation, not a design goal. Decision 11."
**Scope:** ui
**Hardware:** none — confirmable by reading the run dialog's own string in the UI source.
**Owner:** no

## What

`open.md` resolves an undecided question by asserting a fact about the shipped UI: **the run dialog
says the UI cannot reflash.** That assertion has never been checked against the source, and it is
the load-bearing half — if the dialog is silent, then the question is not "settled as the third for
now", it is unstated, and a user meets a missing capability with no explanation.

Three places should agree: the run dialog's text, `embarch-ui`'s own docs, and the suite-level
guides. **Check all three; fix whichever is silent or says something else.** If the dialog does say
it, the fix may be nothing but striking the uncertainty from `open.md` — that is a valid outcome
and should be reported as one.

## Why now

This is the exact defect class this suite keeps finding: a doc asserting a user-facing string
exists, with nothing checking it. It is cheap — one grep in the UI source and two doc reads — and
it either closes a standing open question or finds a real gap where a user meets one.

**Do not build the reflash selector.** Where it should live is genuinely undecided and stays that
way; this task is only about whether the current limitation is stated where someone meets it.

## Done when

- [ ] The run dialog's actual text is quoted in the report, and the three surfaces agree.
- [ ] Whichever surface was silent or wrong is fixed — and if none was, that is said plainly rather
      than a change being manufactured.
- [ ] `embarch-ui/open.md`'s bullet reflects what is true, with the undecided half still open.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment if anything reader-facing changed.
