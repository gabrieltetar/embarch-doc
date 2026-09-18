# 070 — The Study Designer authors every field a `Study` carries

**State:** done — landed 2026-09-17 by the owner's session.
**Source:** embarch-study-designer/open.md — "Missing authoring paths"; embarch-ui/spec.md's Study Designer row
**Scope:** ui
**Hardware:** verify-only
**Owner:** no

## What

Five capabilities that had no path anywhere in the suite, each with a downstream
implementation already waiting for a caller: `Study.protocols` + `RunProtocol`,
running a hand-authored `Study` JSON, `record_checks`, `dev_bench_log_level`,
and registry edit/delete plus payload layouts.

## Why now

Every one of them was fully executable on the far side: dev-bench has a complete
`.eap` interpreter, Core runs `verify_declared_records` on both exit paths and
`dev_bench_log.c` applies and reverts the level. Only the authoring end was
missing, which is why the only studies that could carry any of it were the exact
ones this tab could neither edit nor launch.

## Done when

- [x] `01b7b6f` — the blocking defect first: `seal_crc` sealed two of three
      seals, the same hardcoded-arity trap `embarch-api` hit (reversal row 76).
- [x] Server: `2e7bcc8` record checks + log level, `9e88440` served facts,
      `3da4113` protocol/registry/struct routes + the reference scan,
      `3da11b2`/`33cf2fd` pre-flight, summary and run-as-is.
- [x] Browser: `91014d0`, `0764abb`, `482d739`, `792c2db`, `777a91c`, `5c85de5`.
- [x] Two defects the real-clicks leg found and nothing else could: `c60e96c`
      (the editor opened every file as the string "undefined") and `910dab9`
      (three copies of the adopt-and-render sequence, already drifted).
- [x] Gate green per commit; 44 headless browser checks against the deployed
      release binary via `geckodriver`, plus the light-theme contrast leg.
- [x] `embarch-ui` decisions 29/30, `spec.md`'s tab row and four new
      invariants, `interfaces.md`'s served-fields and route tables,
      `open.md` for the unrun hardware legs and the divergence pointer.

## Legs E and J, run 2026-09-18 on a live nRF54L15 bench

Bench `5540469a-dirty`, `link_identity: match`, **no DUT attached** — which
turned out not to matter: `StudyStart`'s guards pass, so the level is applied
and the steps' own failure is irrelevant to what these legs measure.

**Leg E — 5/5.** Against a live Core reading the bench over `HelloAck`: within
caps the note is silent, 17 steps names 17 and 16, Run stays enabled, and the
run dialog's block carries the same sentence plus a real `/preflight` reading.

**Leg E's second half describes a state this design cannot produce, and that is
the plan's own doing, not a defect.** It expected "unplug the bench → the block
reads unknown". The advisory caps are `embarch-study-designer::limits`
constants — mirrors of dev-bench's headers, which is what the plan's own
decision made them — so they are served identically whether a bench is attached
or Core is unreachable entirely (**measured: byte-identical `dev_bench_limits`
from a live-Core UI and a dead-Core one**). `unknown` is the "the actions
response has not been read" state, which was verified headless. The leg asked
for a reading off the bench; nothing reads off the bench.

**Leg J — 6/6 in the browser, plus the end-to-end A/B.** Two studies saved
through this tab differing *only* in the level (**identical `steps_crc`**, which
is itself the confirmation that no seal covers it), each run through the new
`/studies/{slug}/run` route on real hardware:

| level | `dev-bench` tap |
|---|---|
| `Off` | **0 bytes** |
| `Debug` | **7,440 bytes**, 129 lines — 125 `<dbg>`, 3 `<wrn>`, 1 `<err>` |

`Off` forwarding nothing, including the fatal dump, is exactly what the UI's
note for it says. The `Debug` capture also measured the cost that note warns
about: three `log: N log record(s) dropped before this backend saw them`
warnings, **138 records lost** to link bandwidth. The capture came back with
`records: null`, which the browser renders as *not checked* — the invariant, on
a real capture rather than a synthetic one.

**Left undone:** the clamp note itself never fired, because `app/prj.conf` is
`CONFIG_LOG_DEFAULT_LEVEL=4` with runtime filtering — `Debug` is reachable, so
`reached == want` and `main.c:1389` correctly says nothing. Its delivery path is
proven; only the trigger is unexercised. Carried in `embarch-ui/open.md`.
