# dev-bench/007 review finding: combined truncation+overflow silently drops the census-full signal

**State:** claimed — leg 070, `agent/dev-bench/015-combined-truncation-markers`

**Supervisor's pre-dispatch direction (leg 070, 2026-09-10).** Take the fix the task calls
right-sized: make the combined case say **both** things. Do not add a third combined marker that
names neither condition — decision 45 already rejected that shape in writing, and re-adding it
would be contradicting the decision a second time rather than repairing it. Budget the 64-byte
`fail_reason` so that when both conditions hold, both markers survive; if the budget genuinely
cannot hold both plus any name, shorten the *name list*, not the markers — a marker is the
diagnostic and a name is the payload. Then amend decision 45 in `decisions/scanning.md` to state
the combined case explicitly, and fix `app/src/scan_seen_names.h`'s header, which cites a
`decisions/ble.md` decision 43 that does not exist (the real ones are 32 and 45 in
`decisions/scanning.md`) — that citation fix is part of this task, not a follow-up.

**Build honesty.** If this environment has no `west`/`ZEPHYR_BASE` and the firmware cannot be
built or its tests run from here, say so plainly in your report and in the task file and leave the
change reasoned-but-unbuilt — do **not** claim a gate you did not run. That debt is already
recorded for `embarch-outpost` and would be the same class here.

**Doc-size reserve in this sub-project is tight:** `embarch-dev-bench/open.md` is 4782/5120 B
(338 B left), `spec.md` 9460/10240 B (780 B left) — both filed as `tasks/dev-bench/012`
(`blocked`) — and `decisions/link.md` 11241/12288 B (1047 B left), filed as `tasks/dev-bench/014`
(`blocked`). `decisions/scanning.md`, the file you are editing, is not in reserve. If your work
pushes any `embarch-dev-bench` doc into the last 10% of its cap unfiled, file
`tasks/dev-bench/<NNN>-compact-dev-bench.md` in the same commit.
**Source:** reviewer (dev-bench/007)
**Filed from `inbox/` by leg 067, 2026-09-10**, in the same fold as `dev-bench/007`, the unit whose review produced it. **Owner: no.** The secondary note at the bottom — `scan_seen_names.h`'s header cites a decision 43 in `ble.md` that does not exist — is part of this task, not a separate one: fix the citation to decisions 32 and 45 in `decisions/scanning.md` in the same change.
**Scope:** dev-bench
**Hardware:** none — a code-read finding; confirming the live frequency of the combined case would need a bench with 256+ advertisers on air, but the code path is provable by inspection alone.

## What

`embarch-dev-bench` merge `79d474345fa9753f93abdc9e92f891f08539391a`, `app/src/ble_bridge_real.c` (`connect_as_central`, around the new marker-selection block, ~line 1270):

```c
return outcome_fail("%s%s%s", SCAN_SEEN_PREFIX, summary,
                    names_truncated  ? SCAN_SEEN_TRUNCATED_MARKER
                    : scan_seen_overflowed ? SCAN_SEEN_OVERFLOW_MARKER
                                           : "");
```

When both `names_truncated` and `scan_seen_overflowed` are true at once — the name list filled the 64-byte `fail_reason` *and* more than 256 distinct advertisers were seen this scan — only `(truncated)` is ever written. The `(census full)` signal is silently dropped in that case; nothing in `fail_reason` records that `SCAN_SEEN_MAX` was also exceeded.

## Why this contradicts a locked decision, not a refinement

`decisions/scanning.md` #32 states the invariant this code exists to serve: **"A cap that silently truncates defeats the diagnostic entirely — 'not in the list' has to mean 'not on the air', not 'the list was full.'"** That is exactly what happens in the combined case: an advertiser dropped by the 256-entry census cap now reads only as an ordinary name-list truncation, indistinguishable from the common case decision #45 itself names ("three or four names"). Decision #45's own text describes the two conditions as always independently signalled ("Two distinct overflow conditions now get two distinct markers") and explicitly rejects a combined marker "because it would say something was cut without saying which" — but the implemented priority order silently re-collapses the two conditions back into one, in precisely the combined case decision #45 was written to prevent. Neither #32 nor #45 documents this priority choice or its cost; the decision as written describes both markers as always distinctly available, which is not what the code does when both conditions co-occur.

## What it would take to undo

Merge SHA `79d474345fa9753f93abdc9e92f891f08539391a` in `embarch-dev-bench`. A revert of this commit is clean (single self-contained commit, no later commit in the unit touches these lines) but would restore the pre-existing worse bugs (bug #1 and #2 that #007 fixed) — reverting is not the right fix. The right-sized fix is local: reserve enough of the 64-byte budget to write both markers concatenated (or a combined form that still names both), and only decision #45 needs updating to describe the combined case, since this is a design choice within `embarch-dev-bench`'s own sub-project rather than a rule owned elsewhere.

## Secondary note (not filed as a separate finding)

`app/src/scan_seen_names.h`'s file header cites this work as "decisions/ble.md decision 43" — there is no decision 43 in `ble.md`; the actual decision is #32 (`SCAN_SEEN_MAX`/name filter) and #45 (this unit) in `decisions/scanning.md`. Miscited, not contradicted — flagging in case it is worth a follow-up comment fix.
