# 011 — The weekly pass's contract: the week commands, the desk command and the sheet

**State:** claimed by agent/promptu/011-weekly-pass-contract, 2026-11-23 18:03
**Source:** embarch-promptu/open.md — the two step 4 lines; decisions 43 to 47 (`decisions/learning.md`, the owner's step 4 answers, 2026-11-23)
**Issue:** EMB-272
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

Promptu's weekly pass (build step 4) has no interface yet: the code repo's
`docs/contract.md` §9 (`promptu desk --json`) and §10 (`sheet.json`) still say
"sketch", §11 lists them as open until built, and no `promptu week` command is
specified. Decision 3 has each step build against the contract, written first,
so this unit writes it before any step 4 code. When this is done:

- `docs/contract.md` specifies each `promptu week` command (pack, draft, run,
  status, show, mark, apply and timer) and `promptu desk`: arguments, JSON
  output carrying `"promptu": 1`, exit codes, and the files each reads and
  writes.
- It names the state path for a week's files (a new folder beside §7.5's) and
  the new config keys: the schedule, the drafter's model, its time limit, and
  where an approved pattern change lands.
- It gives the pack's record shapes: a run's events, a session's events, an
  unmatched task start, an outcome.
- §9 and §10 no longer say "sketch", and §11 lists what step 4 fixes. Keep
  everything §11 already fixes; add only the new folder, keys and commands.
- From decision 14: every event becomes a proposal, and each names a question, a
  new question, the template, the picker, a memory entry or a new pattern. A
  specific, stable fact becomes a memory entry, so patterns stay generic.
- Decision 14 records the chat's Promptu card as a second place the weekly pass
  shows (owner, 2026-11-07); it still says the Desk section alone.
- `open.md`'s line saying `promptu week --pack` was never stubbed is updated.

Build on decisions 43 to 47: where an approved pattern change lands, how a sent
prompt is matched to its run, how next run and a missed run are known, one sheet
or several, and what step 4's first cut holds. **A choice they leave open goes
to `docs/forks.md`**, ranked, with a recommendation, running on its most
reversible default and marked provisional.

## Why now

Every other step 4 unit, in `embarch-promptu`, `embarch-desk`, `embarch-ui` and
`embarch-chat`, builds against this contract; thirteen Fleet Ready issues wait
on it, directly or through each other.

**Burndown leg: no new numbered decision.** Amend decisions 14, 15 and 30 in
place where the contract changes what they say; an open choice is a
`docs/forks.md` entry, not a decision. The `embarch-desk`, `embarch-ui` and
`embarch-chat` sides are other scopes: name what they will need in the contract,
and change nothing there.

## Done when

- [ ] `docs/contract.md` specifies each `promptu week` command and `promptu
      desk`: arguments, output, exit codes, files read and written.
- [ ] §9 and §10 no longer say "sketch", and §11 lists what step 4 fixes.
- [ ] The week folder and every new config key are in the contract and in the
      "Files" table of `interfaces.md`.
- [ ] Decision 14 records the chat's card as a second place the weekly pass
      shows (owner, 2026-11-07).
- [ ] Every choice the owner has not made is in `docs/forks.md` with a
      provisional default.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
