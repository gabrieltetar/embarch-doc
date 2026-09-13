# 058 — `decisions/bind.md` says `saved.host` is sticky for every class; `apply_plan` clears it

**State:** claimed by agent/umbrella/058-saved-host-no-longer-sticky, 2026-09-13 12:08
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified on both sides. Re-read each file:line
rather than trusting the quotes below.
**Scope:** umbrella
**Hardware:** none — three prose assertions in two decisions files. No code change.
**Owner:** no

## What

Three claims in `embarch-umbrella`'s decision corpus were true when written and are not now.
Decision 51 changed the behaviour and `open.md` was updated; these were not.

**(a) `decisions/bind.md:29`** — *"And `saved.host` is sticky: `apply_plan` writes
`host.map(…).or(saved.host)` for **every** class, so a `--host` from any earlier run outlives a
later `setup`…"*, citing `../open.md` as its witness.

The code does the opposite. `embarch-umbrella/src/setup.rs:349`:
`host: if plan.class == TopologyClass::Remote { plan.host } else { None },`. And the witness now
says so too — `embarch-doc/embarch-umbrella/open.md:15`: *"`apply_plan` **now clears**
`saved.host` on a non-`remote` `setup` conclusion"*, decision 51.

**(b) `decisions/sticky-host.md:27`** quotes *"`state.rs`'s 'Only meaningful for `remote`'
comment"*. `grep -rn "Only meaningful" embarch-umbrella/src/` returns **3** hits, all in
`config.rs` and all about `discovery =`; **none** in `state.rs`, which was rewritten
(`src/state.rs:26-32`). The citation names the wrong file and the wrong subject.

**(c) `decisions/sticky-host.md:63`** says the clearing *"stays open"* — while decision 51, five
lines below at `:68` in the same file, settles it.

## Why now

(a) and (c) are the expensive kind: a decision file that states the current behaviour of code, and
states the opposite of it. A reader debugging a surprising `--host` carry-over reads bind.md,
concludes the carry-over is by design, and stops looking. No gate sees any of the three —
`check-decision-refs.py` resolves decision numbers and `check-links.py` resolves links; a prose
claim about a code path is neither, and (b)'s citation is to a symbol, not a link.

## Done when

- [ ] `bind.md:29` describes what `apply_plan` does now, and **cites decision 51 as what changed
      it** rather than being silently rewritten — the reason the field was once sticky is part of
      why clearing it needed a decision.
- [ ] `sticky-host.md:27`'s citation points at something that exists, or the clause is rewritten to
      make its point without a dead pointer. Do not invent a `state.rs` comment to match it.
- [ ] `sticky-host.md:63`'s "stays open" no longer contradicts decision 51 five lines below it.
- [ ] Each fix re-derived from `embarch-umbrella/src/` as it is now, with the file:line recorded in
      the task file.
- [ ] Gate green; `changelog.d/` fragment.

## Do not

**Do not delete decision 48's body or rewrite history.** This suite keeps a decision's original
reasoning and amends it in place — a superseded argument is evidence about how the design moved,
and `embarch-decision-reversals.md` exists because that record has value. Amend, mark what is
historical, and keep the why.

**Do not change `apply_plan`.** The code is right; the docs are wrong. If you find a case where the
code is actually the wrong one, that is a finding for
`/home/gabriel/Github/embarch/embarch-doc/inbox/`, not a change to make inside a doc task.
