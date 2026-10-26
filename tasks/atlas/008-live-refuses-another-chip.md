# 008 — Refuse to decode a live read taken from another chip, or from another board than the console

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the bench board's console was declared under role `dev-bench` while that role's probe belonged to another project's nRF54L15 DK; 1 `live_stacks` call paired an STM32G0 shell with the nRF54L15 probe
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`reg_read` decodes whatever words Core returns against the atlas's own SVD, and `live_stacks` compares flash words with the ELF, without checking that the chip Core read is the atlas's MCU. Core's answer names it (`read['chip']`), and the atlas only prints it in the `src:` line (`embarch-atlas/src/embarch_atlas/live.py:389-390`). When done: before decoding, `reg_read` and `image_check` compare `read['chip']` with the atlas's MCU part (the SVD document's device, the MCU line of `MAP.md`) and refuse on a mismatch, naming both and the role. `live_stacks`, which takes its console from one place (the signal's `origin_role`) and its flash check from another (the role's enrolled probe), says so when the probe's chip is not the atlas MCU: "the console of role X and its probe are different boards". `image_check` stops reporting a different chip as "the board runs another build" (`live.py:788-789`, `854-855`).

## Why now

Bench boards hold no role since topology decision 41 (`93a83d9`), and a signal names only a role (`embarch-topology/src/hardware/signal.rs:58-63`), so the only way to give the ST eval board a console was to declare it under a role whose probe is another board. In that state `shell role=dev-bench` reached the STM32G0 and `reg_read role=dev-bench` would have read the nRF54L15 and printed the words decoded as STM32G0 registers. It stayed loud only because the nRF board was unplugged that day.

## Done when

- [ ] Unit test with a fake `mem-read` answer whose `chip` is `nRF54L15`: `reg_read RCC.APBENR1` refuses and names both chips; the same answer with the atlas's chip decodes as today.
- [ ] Unit test: `live_stacks` with a mismatched chip says the console and the probe are different boards, and does not say "another build".
- [ ] The chip comparison tolerates package and suffix variants (`STM32G0B1VE` against `stm32g0b1`), with a test.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` "Live" updated, `changelog.d/` fragment dropped; the signal-names-a-board fix itself is `suite-bench-board-owns-signals-and-live-reads`.
