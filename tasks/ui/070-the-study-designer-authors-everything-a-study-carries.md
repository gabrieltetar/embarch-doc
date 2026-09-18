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

**Left undone, deliberately:** legs E and J need the dev bench plugged in — the
caps note against a live `dev_bench_limits`, and a `Debug` run's clamp on the
bench's own log stream. Carried in `embarch-ui/open.md` as hardware debt.
