# 058 — `decisions/bind.md` says `saved.host` is sticky for every class; `apply_plan` clears it

**State:** done — 2026-09-13
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

- [x] `bind.md:29` describes what `apply_plan` does now, and **cites decision 51 as what changed
      it** rather than being silently rewritten — the reason the field was once sticky is part of
      why clearing it needed a decision.

  Fixed at `embarch-doc/embarch-umbrella/decisions/bind.md:29`: the claim is now past tense
  ("was sticky … until decision 51 (`sticky-host.md`) made `apply_plan` write `None` there
  instead"). Re-derived from `embarch-umbrella/src/setup.rs:349`, unchanged since the task was
  filed: `host: if plan.class == TopologyClass::Remote { plan.host } else { None },`.

- [x] `sticky-host.md:27`'s citation points at something that exists, or the clause is rewritten to
      make its point without a dead pointer. Do not invent a `state.rs` comment to match it.

  Fixed at `embarch-doc/embarch-umbrella/decisions/sticky-host.md:27`. The quote was real, not
  invented: `git show e63ce13:src/state.rs` (the original `setup`/`up`/`down` commit) has the
  literal comment `/// Only meaningful for \`remote\`.` — it just isn't there any more. It was
  rewritten twice: `umbrella/050` (`3fecfa4`) replaced it per decision 48's own finding, then
  `umbrella/056` (`bbe998c`, decision 51) rewrote it again to the clearing-rule text that's live
  today at `embarch-umbrella/src/state.rs:26-32`. The clause now says the quote "is gone now, not
  dead" and points at `src/state.rs`'s current comment instead of re-asserting the old text as
  present tense. `grep -rn "Only meaningful" embarch-umbrella/src/` still returns only the 3
  `config.rs` hits about `discovery =`, confirmed unchanged by this task.

- [x] `sticky-host.md:63`'s "stays open" no longer contradicts decision 51 five lines below it.

  Fixed at `embarch-doc/embarch-umbrella/decisions/sticky-host.md:69` (line moved by the
  edit above): "That half stayed open — until decision 51, immediately below, settles it."

- [x] Each fix re-derived from `embarch-umbrella/src/` as it is now, with the file:line recorded in
      the task file. Done above; also confirmed no other `state.rs`/`config.rs` comment needed
      updating for this task's three claims.
- [x] Gate green; `changelog.d/` fragment.

  `changelog.d/umbrella-sticky-host-stale-claims.fixed.md` added. Gate: `cargo build`, `cargo
  test`, `cargo clippy --all-targets -- -D warnings` all clean in the code worktree (no code
  changed); `check-docs.py` 11/11 green in the doc worktree; `check-doc-size.py` initially went
  RED (decision 22's per-decision baseline, `bind.md#22` pinned at 10752 B, grew to 10879 B on
  the first draft of the fix) — tightened the wording to a net +86 B and it's green again, no
  compaction task filed since neither file entered a fresh reserve band because of this change.
  `check-client-names.py --repo <code worktree>` clean; `check-ownership.py --scope umbrella` and
  `--code-repo` both clean on both branches.

## Do not

**Do not delete decision 48's body or rewrite history.** This suite keeps a decision's original
reasoning and amends it in place — a superseded argument is evidence about how the design moved,
and `embarch-decision-reversals.md` exists because that record has value. Amend, mark what is
historical, and keep the why.

**Do not change `apply_plan`.** The code is right; the docs are wrong. If you find a case where the
code is actually the wrong one, that is a finding for
`/home/gabriel/Github/embarch/embarch-doc/inbox/`, not a change to make inside a doc task.
