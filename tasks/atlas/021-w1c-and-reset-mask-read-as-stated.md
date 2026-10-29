# 021 — Read write-one-to-clear and an SVD's reset mask as stated: W1C is not read-to-clear, and an undefined reset bit is not 0

**State:** claimed by agent/atlas/021-w1c-and-reset-mask-read-as-stated, 2026-10-29 16:02
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-atlas findings 4 and 9), verified by Opus against embarch-atlas@0cf93cec
**Scope:** atlas
**Hardware:** none — The guard, the SVD parse and the decode are all exercised against fixture SVDs, fixture part records and fake `mem-read` answers, as `tests/test_live.py` and `tests/test_svd.py` already do. The change is to what is refused and how a value is labelled, and no board is needed to prove either.
**Owner:** no

## What

**The read-to-clear guard refuses write-one-to-clear registers.**
- `side_effects` (MCU registers, `src/embarch_atlas/live.py:229-232`) and `_ext_effects` (external parts, `live.py:599-600`) treat any `access` containing `"clr"` as clearing on read.
- That also matches `woclr`, which `svd.py` makes from `modifiedWriteValues="oneToClear"` (`svd.py:45`) and `regparse` from a printed `R/W1C` or `W1C` (`regparse.py:129-130`). It matches `wclr` too.
- Reading a W1C flag does not clear it. Yet the register is refused by name with "is cleared by the read (…: readAction)", although the SVD has no readAction there, and it is left out of a whole-peripheral read.
- With `allow_clear=true`, the answer then says the read cleared it.
- In the public vendor SVDs under embarch-dev-bench's Zephyr workspaces, 63 of 101 distinct files use `oneToClear`, and the nRF54L15 application SVD has 380 lines with it. The two STM32 SVDs there have none, which is why STM32 use has not shown this.

**The SVD's reset is invented where the SVD gives none.**
- A register with no `resetValue` anywhere in its inheritance chain gets reset `0` (`svd.py:230`).
- `resetMask` is parsed (`svd.py:232`), stored as `reset_mask` (`svd.py:239`) and never read again. `build_records` (`svd.py:372-377`) writes a register reset and field resets that claim every bit.
- `reg_read`'s decode then marks fields "at reset" or "not at reset" (`*`) against bits whose reset the SVD leaves undefined (`live.py:319-337`).
- `mcu vote` reads a missing SVD reset as 0 (`vote.py:634`), so an honest `null` would turn into a false "reset differs" unless vote learns it too.
- No `resetValue` anywhere: none of the 101 files. A resetMask that is not all ones: 53 of them, none of them the nRF54L15 or STM32 files.
- The record schema already allows `reset: null`.

One possible direction:
- Have the guard fire only on read-side semantics (`rclr`, an SVD `readAction`, and the text checks), and on nothing that describes a write.
- Carry the mask into the records, or set an undefined reset to `null`, so that the decode and vote compare only bits that have a defined reset.

## Why now

- DESIGN.md "Live" (lines 386-389) says a register is refused "when the SVD marks a field `readAction` (access `rclr`) or the reference manual's field text says reading it clears something". W1C is neither, so the code refuses registers the design does not.
- A false refusal followed by a false "this read cleared" is the habit-forming failure that `tasks/atlas/006` is filed against: callers learn to pass `allow_clear=true` by reflex.
- The reset half costs little beside it, because it is the same decode path. It would not clear the bar alone.
- `tasks/atlas/006` rewrites `_ext_effects`' attribution and pins the list of guarded registers over the fixture atlases. This drop changes that function's `access` test and so changes that pinned list. Land one after the other, or fold this drop's `_ext_effects` half into 006.

## Done when

- [ ] A field whose only clear semantics is W1C (SVD `oneToClear`, or a printed `R/W1C`) does not by itself guard its register, on either the MCU or the external path. A field with `readAction="clear"` (`rclr`) still does. Tests cover both.
- [ ] A whole-peripheral `reg_read` over a fixture SVD with W1C status registers reads and decodes them.
- [ ] A fixture SVD register whose `resetMask` leaves bits undefined yields records, and a `reg_read` decode, that claim no reset for those bits. A register with no `resetValue` anywhere yields no claimed reset. A test pins each.
- [ ] `mcu vote` reports no "reset differs" on bits that the SVD leaves undefined.
- [ ] The records `mcu svd` writes from an SVD with full masks and every `resetValue` given are byte-identical to today's.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Live" (the read-to-clear guard) updated (embarch-atlas has no `spec.md`, so DESIGN.md is its contract). `changelog.d/` fragment dropped.
