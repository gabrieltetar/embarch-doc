# Bring `interfaces/wire.md` up to what the firmware actually puts on the wire

**State:** claimed by leg 023, 2026-09-06 — `agent/outpost/007-wire-md-behind-firmware`
**Source:** owner's repo survey, 2026-09-06 — `wire.md` calls itself the spec three implementations must agree on, and its header field order is wrong
**Scope:** outpost
**Hardware:** none
**Owner:** no

## Doc-size reserve for `outpost` (supervisor, leg 023)

**No `embarch-outpost` doc is in reserve** — `wire.md`, `integration.md`,
`spec.md` and the `decisions/` files all have room, so this unit can grow them.
If your work pushes one into its last 10%, file
`tasks/outpost/<NNN>-compact-outpost.md` in the same commit (`tasks/README.md`
has the shape).

**`suite/features.md` is at a hard wall and it is not yours to fix:**
20,259 / 20,480 B, **221 bytes left**, with its compaction task `suite/004`
`blocked` on the owner. This unit is documentation catching up to code that
already shipped, so it almost certainly owes a `changelog.d/` fragment and **no
`features.d/` row at all**. Do not write one to be thorough.

## No toolchain, and that is expected

`embarch-outpost` has **no `Cargo.toml`** and you have no `west` or
`ZEPHYR_BASE`. Do not attempt a firmware build. `python3 scripts/check-docs.py`
in `embarch-doc` plus `check-ownership.py` and `check-client-names.py` are this
repo's gate — `outpost/006` landed on exactly that last leg.

## Read the firmware, do not trust this task file's line numbers

Every citation below came from a repo survey and line numbers drift. **Open each
cited file and confirm the fact before you write it into `wire.md`** — the whole
product of this unit is that a fourth implementer can build a decoder from the
doc, so a doc corrected to a second stale reading is worse than the stale doc.
In particular, read the header writer in `src/outpost.c` in full rather than
just the field named below; if the order differs from both the doc and this
task, the firmware wins and say so in your report.

## What

Three divergences, all in `embarch-doc/embarch-outpost/`:

- `interfaces/wire.md:37` documents the header payload as `record_layout_version, flags,
  outpost_version, build_id` — but `src/outpost.c:251` writes a `cycles_per_sec` varint **between
  `flags` and `outpost_version`**.
- `wire.md:15` lists record kinds only through `Gap`, while `src/outpost_priv.h:141` and `:152`
  define `GPIO_DISPATCH = 9` and `GPIO_CALLBACK_DONE = 10`.
- `wire.md:43` lists seven flag families and omits `OUTPOST_FLAG_TRACE_GPIO = BIT(6)`
  (`outpost_priv.h:170`).

`interfaces/integration.md`'s Kconfig table — which `spec.md` §4 calls "every Kconfig symbol" — is
also missing `EMBARCH_OUTPOST_TRACE_GPIO` and `EMBARCH_OUTPOST_TX_TIMEOUT_MS` (`Kconfig:134`, `:226`).

Carry across the "read `GPIO_CALLBACK_DONE` literally, it is an exit marker" warning and the
`b`-is-not-the-pin-mask reason already written at `outpost_priv.h:132-140`.

## Why now

`wire.md` opens by calling `outpost_priv.h` the specification with "three implementations that must
agree". A fourth reader building a decoder from this doc gets the header field order wrong and
mis-decodes every stream.

## Done when

- [ ] The header frame's field list in `wire.md` matches `src/outpost.c:241-266` field for field.
- [ ] Kinds 9 and 10 and flag bit 6 appear in `wire.md`, with the exit-marker warning carried across.
- [ ] `integration.md`'s table lists every `config EMBARCH_OUTPOST_*` symbol in `Kconfig`.
- [ ] No decision number is renumbered, and `scripts/check-decision-refs.py` still resolves.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
