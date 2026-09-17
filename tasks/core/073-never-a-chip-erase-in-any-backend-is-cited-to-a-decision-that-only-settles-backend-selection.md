# 073 — "`erase` never becomes a chip erase in **any** backend" is cited to decision 36, which only settles backend *selection*

**State:** open
**Source:** leg 133's reviewer on `core/071`, as the honest answer to a directed check rather than as
a contradiction finding. `core/071` moved this citation from decision 32 to decision 36 — correctly,
because 32 does not establish the property either — and the reviewer then established that **36 does
not fully establish it either**. Filed so it does not live only in a log entry.
**Scope:** core
**Hardware:** none. Settled by reading `flash_backend.rs`, its tests, and the `decisions/` tree.
**Do not flash anything and do not run a live Core** — the subject is which document asserts a
property, not an observation of an erase.
**Owner:** no

**Doc-size reserve for `core`:** `embarch-core/decisions/auth.md` is **11,356/12,288 B (932 B left)**,
filed as `tasks/core/046` and blocked — do not write into it. `decisions/flashing.md` and
`decisions/flash-backend.md` both have room. Check `python3 scripts/check-doc-size.py --pressure`
before and after; if you push a file into the band, file `tasks/core/<NNN>-compact-core.md` in the
same commit.

**These coordinates are second-hand — a reviewer's, not read by me.** Re-derive each and correct the
record in your report. **"This does not hold" is a correct outcome.**

## What

`embarch-core/interfaces/hardware.md` (around line 10) asserts:

> *"`erase` never becomes a chip erase in any backend (decision 36)"*

Decision 36's body in `decisions/flash-backend.md` is about **which backend a chip family gets, and
why probe-rs is refused for the RRAM families**. It is reported never to state that the vendor-tool
backends — `jlink`, `nrfutil` — refrain from a chip erase. That half of the property is reported to
live **only in code and tests**: `flash_backend.rs` maps `erase` to
`chip_erase_mode=ERASE_RANGES_TOUCHED_BY_FIRMWARE` for `nrfutil`, and a `jlink_script` test asserts
the script contains `"erase\n"` and not `"erase_chip"`. A grep of the whole `decisions/` and
`interfaces/` tree for *"chip erase"* and *"ERASE_RANGES"* is reported to find **no decision text
asserting this for the vendor arms at all.**

## Why it costs something

**This is the same defect `core/071` just fixed, one hop over, and it is the one the fleet keeps
re-finding: a true sentence resting on a reference that does not carry it.** A reader who follows the
citation to check the guarantee finds a decision about backend selection and cannot tell whether the
never-a-chip-erase property was decided, measured, or assumed. On a project that has already bricked
a part with an erase, *"where is this guaranteed"* is a question someone will actually ask.

It is **not** a contradiction — decision 36 does not say the opposite, and the code does honour the
property — which is exactly why nothing catches it: `check-decision-refs.py` resolves the number, and
the sentence is true.

## What resolving it probably looks like

Two candidate shapes; **decide which, and say why.**

1. **Amend decision 36** with one paragraph recording that each vendor arm's erase mode is
   deliberately range-scoped rather than a chip erase, naming `ERASE_RANGES_TOUCHED_BY_FIRMWARE` and
   the `jlink` script's `erase`, so the property lives where the citation points.
2. **Re-point the citation** at whichever decision genuinely covers the vendor arms — if one exists.
   Establish that by reading, not by looking for a plausible number; if none exists, option 1 is the
   answer and option 2 is how this defect gets recreated.

**Whichever you choose, the `[measured]`/`[assumed]` distinction has to survive it.** The vendor arms'
erase behaviour is known from the *script this crate generates*, which is a contract with the vendor
tool, not an observation of an erase on silicon. Do not write it as measured.

## Done when

- [ ] The property is either **recorded where `interfaces/hardware.md` points**, or the citation
      re-pointed at a decision that genuinely carries it — with the reading that established which.
- [ ] Your report says plainly whether the reviewer's claim held: that no decision text anywhere
      asserts the vendor arms' non-chip-erase behaviour. Re-run the grep.
- [ ] Nothing asserts the vendor arms' behaviour as observed on hardware.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      in `embarch-core`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

**Do not change any erase behaviour, erase mode, or backend routing.** This is about where a
guarantee is written down. The code already honours it.

**Do not re-open decision 32.** `core/071` amended it on 2026-09-17 to record that sector-erase is
what ships, confined by decision 36; that amendment is settled and this task is downstream of it.

**Do not touch `embarch-decision-reversals.md` or anything under `reversals/`** — suite-level,
supervisor-owned. There is a separate, already-filed gap there about decision 32's second drift
(`inbox/core-071-reversals-gap-decision-32-second-drift.md`); leave it.

**Do not touch `decisions/auth.md`** — in reserve, parked under `tasks/core/046`.

**Do not do `tasks/core/072`'s two items** — `interfaces.md`'s plain-text/`503` invariants versus
decision 59, and the retired `alias` field. Separate unit, may be in flight.
