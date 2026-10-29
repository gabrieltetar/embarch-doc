# 020 — A bump's second look batches every changed fact, and compares every value the reader is asked for

**State:** claimed by agent/atlas/020-second-look-batches-and-compares-what-changed, 2026-10-29 17:08
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-atlas findings 3 and 15), verified by Opus against embarch-atlas@0cf93cec
**Scope:** atlas
**Hardware:** none — Both halves are queue and comparison logic over records and readings, testable with fixture queues and fixture readings the way `tests/test_update.py` and `tests/test_secondlook.py` already do. No board, no build, no LLM.
**Owner:** no

## What

**A fact that changed but keeps its id is never batched by a bump.**
- Every second-look queue item carries `key`, a hash over the fields the look checks for its kind (`secondlook.CHECKED`, `src/embarch_atlas/secondlook.py:35-46`).
- `owed_by` returns only the ids that the previous atlas's queue held (`secondlook.py:239-244`). Both `update` (`update.py:205-206`) and `second-look queue --diff-from` (`secondlook.py:336-340`) drop every item whose id is in that set.
- A limit that the previous atlas still owed, and whose `min` the new atlas changed, gets a new key and is queued. It is then left out of `second_look_batches.json` and counted as "already owed before".
- It stays in `second_look_queue.jsonl`, so a later full `--top N` pass reaches it. The bump's own batches never do, although they are the batches the skill tells the session to run.

**The deterministic compare drops values the reader returns.**
- The blind reader is told to return `cond` for a limit or timing, `condition` for a strap and `width` for a register (`secondlook.py:470-474`). `compare_one` (`secondlook.py:676-760`) never looks at any of the three.
- A limit is queued *because* it is condition-bearing (`secondlook.py:87-88`). A reading taken under another condition still comes back `confirmed` when its numbers match, and that verdict is frozen.
- The fields that `ask()` builds the question from (`sym`, `param`, a pin's number, a bus's `iface`, `secondlook.py:100-129`) are premises, not readings. They are out of scope here.

One possible direction:
- Tell the backlog from the diff by `(id, key)` instead of by id.
- Compare `cond` and a strap's `condition` by meaning, not wording. `text_value_verdict` already does this for mode straps. Compare `width` numerically.
- Deciding whether a different condition is a `conflict` or `unresolved` is part of the work.

## Why now

- DESIGN.md:477 says a bump's batches hold "only the diff (new or changed facts; the previous atlas's backlog is counted)". `update.py:206` batches new facts only.
- The one test of the split sets `key` equal to `id` (`tests/test_update.py:26-39`), so it cannot see the difference.
- For the second half, DESIGN.md "Caching" says a verdict holds while "the fields the second look checks" are unchanged. For `cond`, `condition` and `width`, the look asks but does not check.

## Done when

- [ ] An item that the previous atlas's queue held under a different checked key is in the new atlas's batches and counted as changed, both through `update` and through `second-look queue --diff-from`. An item with the same id and key stays backlog. One fixture test covers both items.
- [ ] A limit or timing reading whose `cond` means something other than the first pass's is not `confirmed`. A reading that words the same condition differently is. The same holds for a strap's `condition`. Fixture tests cover each case.
- [ ] A register reading whose `width` differs from the first pass's is a conflict.
- [ ] Whether the stricter compare re-opens verdicts already frozen under the current key is decided and stated in DESIGN.md "Caching", for example by a `CHECKED_VERSION` bump or deliberately not.
- [ ] `tasks/atlas/001` edits the same `update.py` lines for the backlog (`second-look queue --used`). Whichever lands second rebases onto the other, and neither undoes the `(id, key)` split.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` updated (the `update` and `second-look` rows, and "Caching"; embarch-atlas has no `spec.md`, so DESIGN.md is its contract). `changelog.d/` fragment dropped.
