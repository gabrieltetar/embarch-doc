# Bring `interfaces/wire.md` up to what the firmware actually puts on the wire

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `wire.md` calls itself the spec three implementations must agree on, and its header field order is wrong
**Scope:** outpost
**Hardware:** none
**Owner:** no

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
