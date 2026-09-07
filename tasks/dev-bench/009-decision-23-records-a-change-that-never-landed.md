# 009 — Decision 23 says `BleAddress`'s byte order is stated in the crate that owns the type; it is not

**State:** blocked — on [`tasks/study-designer/014`](../study-designer/014-bleaddress-byte-order-was-never-stated-in-the-crate.md), which makes the claim true. Unparks the moment that lands.
**Source:** supervisor, leg 025, from a reviewer drop on the bench unit `api/029` — the drop's own `Done when` spanned two sub-projects, and `check-ownership.py` refuses `embarch-dev-bench/**` to a `study-designer` worker, so it is two tasks
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

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

## Why blocked

**`study-designer/014` is the change decision 23 describes.** Amending the decision before that
lands would be writing a clean statement of something about to change; running it after is one
sentence. Nothing else parks it.

## Why now

**A decision that says a change landed when it did not is worse than one that never claimed it:
the next reader stops looking.** `design-improvements-2026-08-15.md` item 47 flagged this exact
gap *before* decision 23 claimed to close it, and the failure mode it named is silent — a wrong
guess at the byte order means `BleConnect` with an explicit address never matches, and the step
reports a plain timeout with no census (`tasks/dev-bench/008`).

## Done when

- [ ] Decision 23 is true as written, or amended to record when the crate-side statement actually
      landed rather than implying it landed with the decision.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped if anything user-visible changed; a decision correction
      alone may not warrant one — say which and why.
