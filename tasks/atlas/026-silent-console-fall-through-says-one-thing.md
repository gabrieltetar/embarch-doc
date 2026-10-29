# 026 — DESIGN.md states one rule for a silent console reply, and an older Core's silence follows it

**State:** done
**Source:** `atlas/005`'s review (2026-10-29 fold of `atlas/005`, code `b1d4e6e`): the reviewer found no contradiction of a standing rule, and named two residuals as the owner's to weigh
**Scope:** atlas
**Hardware:** none — both halves are `Console.exchange` logic and DESIGN.md wording, testable with the fake `call_api` `tests/test_live.py` already uses.
**Owner:** no

## What

`atlas/005` made `Console.exchange` (`src/embarch_atlas/live.py`) move to the next declared console when a reply carries no text and no `port_lost`, on the ground that "not a byte came back (no echo), so nothing written was read, so nothing ran". Two edges it left:

- **DESIGN.md now says two things about an older Core.** The fall-through paragraph still says a Core without the `written`/`port_lost`/`echo_seen` fields "gets the same treatment (a silent reply says 'this Core did not say whether the line was written, so it may have run')". After `atlas/005` that holds only on the last declared console; on an earlier one the same silence moves on and the line is sent again elsewhere. Decide which is meant and make the code and the paragraph agree. One reading: a Core that sends `echo_seen` lets "no byte and no echo" mean "nothing ran", and a Core that does not is treated as "may have run" on every console, not only the last.
- **The rule assumes a shell that echoes.** "No byte came back" means "nothing ran" only when the image's shell echoes what it reads, which Zephyr's shell does by default. State that assumption in the "Which console" paragraph, and say what the answer is for an image with echo off. **Gating the fall-through on `written` is not the fix** (the reviewer's first suggestion): a USB-UART bridge takes every byte, so `written` is true in exactly the case the fall-through exists for.

## Why now

The paragraph is in a public repo and a reader now gets two rules for one case. The cheapest moment to settle it is while `atlas/005` is fresh and before a bench run (its open debt) exercises the two-console path.

## Done when

- [x] DESIGN.md's fall-through paragraph and "Which console" paragraph state one rule for a silent reply, including an older Core's and a shell with echo off.
- [x] Unit test: the older-Core case on a non-last console behaves as the paragraph says.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped.
