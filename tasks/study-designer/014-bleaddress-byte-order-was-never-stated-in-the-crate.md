# 014 — `BleAddress`'s byte order was never stated in the crate, and two documents say it was

**Filed by the supervisor, leg 025**, from a reviewer drop on the bench unit `api/029`, whose own
`studies-guide.md` §3b was the second of the two documents and has been corrected in the same fold.
`Hardware:` re-checked: `none`.

**The `embarch-dev-bench` half is not this worker's.** Decision 23 in `embarch-dev-bench` claims
the crate states the order — a decision recording a change that never landed — and
`check-ownership.py` refuses `embarch-dev-bench/**` to a `study-designer` worker. **Do the crate
half here and leave decision 23 alone**; it is `tasks/dev-bench/009`. Note in your own work that
the two are paired, because decision 23 becomes true only when this lands.

**State:** claimed by agent/study-designer/014-bleaddress-byte-order, 2026-09-06 20:28
**Source:** reviewer of the supervisor's bench unit `api/029`, leg 025, 2026-09-06 — checked a
citation in `suite/studies-guide.md` §3b against `embarch-study-designer` at `origin/main`
`726a76d`
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Reserve (supervisor, leg 026)

`scripts/check-doc-size.py --pressure` at dispatch: **`embarch-study-designer/decisions/crate.md`
is at 91.7% — 11,267 / 12,288 B, 1,021 B left.** Nothing else in this sub-project is in reserve.
It is filed against `tasks/study-designer/006-compact-study-designer.md`, which is **`blocked` on
`In flux: yes`** — so the pass is parked, but the debt is not.

**This unit should not need to write a numbered decision at all** — it is a doc comment stating an
order that `interfaces/types.md:44` already states in prose, plus a `changelog.d/` fragment. If you
find yourself reaching for `decisions/crate.md`, stop and reconsider: the fact is already recorded
in two places and a third entry is the thing that spent this file's reserve. If a decision genuinely
is owed, put it in whichever `decisions/*.md` the *mission* points at (leg 023 and leg 025 both
split by mission rather than squeezing) and say in your report which you chose and why. If your work
does push a file into reserve, file `tasks/study-designer/<NNN>-compact-study-designer.md` in the
same commit.

## What

`embarch-study-designer/src/ids.rs` does not document `BleAddress`'s byte order. At
`origin/main` (`726a76de4e18a0bfd27c149662bb7ac661083057`) the whole doc comment is:

```rust
/// A BLE device address: 6 raw address bytes plus its public/random kind.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct BleAddress {
    pub bytes: [u8; 6],
    pub kind: BleAddressKind,
}
```

"6 raw address bytes" — no order. `git log --all -- src/ids.rs` has exactly two commits
(`07e2166`, `bc861fd`), neither of them this; `grep -rn -i "display order\|most.significant"
src/` in that repo returns nothing. **The order has never been in the crate.**

Two documents say otherwise:

- `embarch-dev-bench/decisions/ble.md:20`, decision 23 — *"`BleAddress` byte order is stated in
  the crate that owns the type … previously asserted only *here*. **Now stated there**, so the
  assumption is backed by the authoritative source instead of standing alone."* It is not
  stated there. Decision 23 records a change that did not land.
- `suite/studies-guide.md` §3b, added by `api/029` — *"That is a stated contract on both sides
  — `embarch-study-designer/src/ids.rs` documents the order and `ble_bridge_real.c`'s
  `to_bt_addr` reverses it for Zephyr — not a convention to be re-derived."* Half of that
  citation points at a file that does not say it, and the sentence's whole purpose is to tell a
  reader they need not re-derive it.

**The order itself is correct.** `ble_bridge_real.c`'s `to_bt_addr` writes
`out->a.val[i] = params->target_address[5 - i]`, so `bytes[0]` is the leftmost byte as
`bt_addr_le_to_str` prints it, and `embarch-study-designer/interfaces/types.md:44` states it in
prose. Nothing is broken at runtime — leg 025 connected to `C4:82:E1:42:B1:26` with
`[196, 130, 225, 66, 177, 38]`. What is missing is the doc that decision 23 says exists, and
`design-improvements-2026-08-15.md` item 47 flagged the same gap before decision 23 claimed to
close it: *"A wrong guess means `BleConnect` with an explicit address silently never matches."*

## Why now

An author reading `ids.rs` to find out which end goes first finds nothing, and a wrong guess
fails silently — the step just never matches, which is the failure mode decision 43 exists to
remove. And a decision that says a change landed when it did not is worse than one that never
claimed it: the next reader stops looking.

## Done when

- [ ] `BleAddress`'s doc comment in `src/ids.rs` states display order, most-significant first,
      the way `Uuid`'s comment already states big-endian.
- [ ] `embarch-dev-bench` decision 23 is true as written, or amended to say when it became true.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
