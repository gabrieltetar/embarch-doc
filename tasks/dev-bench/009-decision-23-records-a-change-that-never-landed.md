# 009 — Decision 23 says `BleAddress`'s byte order is stated in the crate that owns the type; it is not

**State:** done — **unparked by the supervisor, leg 026, 2026-09-06.** `study-designer/014` landed
(`embarch-study-designer` `79a4c00`, doc `2378b58`), so decision 23's claim is now true *of the
crate*; what is left is making the decision's own text honest about **when** it became true. Its
task file is deleted, as a `done` task file is — the commit above is the record.
**Source:** supervisor, leg 025, from a reviewer drop on the bench unit `api/029` — the drop's own `Done when` spanned two sub-projects, and `check-ownership.py` refuses `embarch-dev-bench/**` to a `study-designer` worker, so it is two tasks
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## Doc-size reserve — supervisor, leg start 2026-09-07 09:44

**No `embarch-dev-bench` doc is in reserve.** `check-doc-size.py --pressure` lists twelve files
across the suite and none of yours, so you owe a compaction task only if your own edits push a
`embarch-dev-bench/*` file into the last 10% of its cap — in which case file
`tasks/dev-bench/<NNN>-compact-dev-bench.md` in the same commit, per `tasks/README.md`.

**One suite-wide hazard applies to you: `suite/features.md` has 60 bytes of headroom** (20,420 of
20,480 B) and is *assembled* from `features.d/` fragments, so **a new `features.d/` fragment turns
the fold red.** This unit corrects a decision's own record and should ship no feature row; if you
think it warrants one, write the row's text into this task file instead and say so.

## What

`embarch-dev-bench/decisions/ble.md`'s decision 23 reads:

> `BleAddress` byte order is stated in the crate that owns the type … previously asserted only
> *here*. **Now stated there**, so the assumption is backed by the authoritative source instead
> of standing alone.

**It is not stated there.** `embarch-study-designer/src/ids.rs`'s whole `BleAddress` doc comment
at `origin/main` `726a76d` is *"A BLE device address: 6 raw address bytes plus its public/random
kind"* — no order, while `Uuid`'s comment immediately above states its own. `git log --all --
src/ids.rs` has two commits and neither is this one.

The order itself is right and nothing is broken at runtime: `ble_bridge_real.c`'s `to_bt_addr`
does `out->a.val[i] = params->target_address[5 - i]`, and leg 025 connected to
`C4:82:E1:42:B1:26` using `[196, 130, 225, 66, 177, 38]`. What is wrong is the **record**.

When this is done, decision 23 is either true as written — because `study-designer/014` landed —
or amended to say what actually happened and when.

## Why it was blocked, and what landed

**`study-designer/014` is the change decision 23 describes.** Amending the decision before that
landed would have been writing a clean statement of something about to change; running it after is
one sentence. Nothing else parked it, and it is unparked.

What `study-designer/014` actually put in the crate, so this task need not go and look: `src/ids.rs`
now states the order on `BleAddress` itself — display order, most significant first, with
`C4:82:E1:42:B1:26` as `[0xc4, 0x82, 0xe1, 0x42, 0xb1, 0x26]` as the worked example — plus that the
order is the same for both `BleAddressKind`s, that the derived serde impls carry `bytes` in index
order, and that nothing in that crate reverses it. `BleAddressKind` also gained a comment saying the
kind does not change the layout. **It did not touch `embarch-dev-bench`**, deliberately, and its own
report and the `status.d/` fragment it wrote both phrase the change as what it makes possible rather
than as anything this repo now says.

## Why now

**A decision that says a change landed when it did not is worse than one that never claimed it:
the next reader stops looking.** `design-improvements-2026-08-15.md` item 47 flagged this exact
gap *before* decision 23 claimed to close it, and the failure mode it named is silent — a wrong
guess at the byte order means `BleConnect` with an explicit address never matches, and the step
reports a plain timeout with no census (`tasks/dev-bench/008`).

## Done when

- [x] Decision 23 is true as written, or amended to record when the crate-side statement actually
      landed rather than implying it landed with the decision. — Verified against
      `embarch-study-designer/src/ids.rs` at `origin/main` before writing anything: the `BleAddress`
      doc comment now states display order, most-significant first, the `C4:82:E1:42:B1:26` worked
      example, that both `BleAddressKind`s share the order, that the derived serde carries `bytes`
      in index order, and that nothing in that crate reverses it — `study-designer/014` really did
      land it. Amended decision 23 in `embarch-dev-bench/decisions/ble.md` with a dated note saying
      the crate-side statement was not yet true when the decision first claimed it, and naming what
      landed and citing `embarch-study-designer decision 14`.
      **Supervisor correction at the fold, 2026-09-07:** that citation was wrong and I replaced it
      before merging. `study-designer/014` is a **task** number, not a decision number —
      `embarch-study-designer` decision 14 is *"Correlation by array position (`step_index: u32`),
      not by `Step.name`"* and has nothing to do with `BleAddress`. **No numbered decision in that
      crate covers the byte order at all**; the change is commit `79a4c00` and only that. The
      amendment now names the commit and says outright that no decision covers it — which is also
      the reason decision 23 could claim the statement prematurely and nothing caught it.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). — see report.
- [x] `changelog.d/` fragment dropped if anything user-visible changed; a decision correction
      alone may not warrant one — say which and why. — **No fragment.** Nothing user-visible
      changed: the crate's own behavior and its own changelog entry are unchanged by this unit;
      this only corrects `embarch-dev-bench`'s decision record to say honestly when the crate-side
      statement landed. A changelog fragment pointing at "a decision text was corrected" would be
      noise a reader of `history/dev-bench.md` gets nothing from.
- [x] `embarch-dev-bench/decisions/ble.md` crossed into doc-size reserve (94.2%, 710 B left) as a
      side effect of the amendment; filed `tasks/dev-bench/012-compact-dev-bench.md` in this same
      commit per `tasks/README.md`, marked `In flux: yes` since BLE decisions in this file have
      changed twice recently (decision 31, and this one).

**State:** done
