**Target:** embarch.md §3 — the `embarch-outpost` row
**Was:** "emitting a thread/ISR/marker timeline out a TX-only UART"
**Now:** the timeline is thread/ISR/**GPIO-callback**/marker — `CONFIG_EMBARCH_OUTPOST_TRACE_GPIO` ships `default y`, has since 706aeb1, and is reported as header flag `BIT(6)`.

`embarch-glossary.md`'s **outpost** row carries the same three-family wording and wants the same word. Neither was made false by this unit; both have been incomplete since the capability landed. The wire contract is [wire.md](../embarch-outpost/interfaces/wire.md), the Kconfig row [integration.md](../embarch-outpost/interfaces/integration.md).
