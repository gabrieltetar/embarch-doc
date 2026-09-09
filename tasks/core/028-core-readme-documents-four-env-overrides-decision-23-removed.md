# embarch-core README documents four dev-bench env overrides that decision 23 removed

**State:** claimed
**Source:** found while fixing dev-bench/005 (README board-and-links); promoted from
`inbox/core-readme-stale-dev-bench-env-overrides.md` by leg 049, unchanged apart from this line
and the note at the end
**Scope:** core
**Hardware:** none

## What

`embarch-core/README.md` (around the `/dev-bench/port` section) still documents
`EMBARCH_DEV_BENCH_PORT`, `EMBARCH_DEV_BENCH_SERIAL`, `EMBARCH_DEV_BENCH_PRODUCT`
and `EMBARCH_DEV_BENCH_INTERFACE` as live env overrides. `embarch-core`'s own
`decisions/probes.md` decision 23 — "The four dev-bench env overrides are gone,
with no replacement knob" — says these are exactly the four, removed in favor
of `embarch-topology`'s enrollment (decision 22's `link_port_serial`/
`link_port_interface`). None of the four names appear anywhere in
`embarch-core`'s own `.rs` sources (checked with a repo-wide grep), consistent
with them being gone rather than just undocumented elsewhere.

`embarch-dev-bench`'s own README carried the same stale claim for its ESP32-C5
build section (fixed in dev-bench/005, conservatively — removed the dead env
var, did not assert which enrollment fact replaces it for a board with no VCOM
interface, since that would be a guess).

## Why now

A new engineer reading either README will set an env var that no longer does
anything and get silent non-effect, which is exactly the failure shape
decision 22/23 exists to prevent (a stale operator-typed override with nothing
to notice it's stale).

## Done when

- [ ] `embarch-core/README.md`'s env-override table is corrected or removed to
      match decisions/probes.md decision 23.
- [ ] If espressif-family port selection has a real current story (e.g. an
      enrollment fact for boards with no VCOM interface), it's stated somewhere
      readable — decisions/probes.md decision 22, or a new one.

## Supervisor note — leg 049

**The second Done-when box may not be answerable without the owner, and that is an acceptable
outcome.** `dev-bench/005` hit the same question from the other side and deliberately declined to
answer it: the ESP32-C5-WROOM-1 DK enumerates as a plain USB Serial/JTAG device with no VCOM, so
there is no `link_port_interface` to state, and asserting a replacement would be inventing a
hardware fact. **Do not infer one from firmware or from `embarch-topology`'s source.** If the
honest answer is that no current story exists, say so in `embarch-core/open.md` as an open question
and close only the first box. Note also that `core/010` landed this same leg and touched
`EMBARCH_FLASH_BACKEND` in `src/flash_backend.rs` — a different env var and a different file, but
read `decisions/flashing.md` decision 52 before writing about env overrides generally, so the two
do not end up describing the same mechanism two ways.
