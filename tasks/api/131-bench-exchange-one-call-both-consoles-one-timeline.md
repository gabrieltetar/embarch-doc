# 131 — One call drives a console sequence and returns every listened console as one filtered timeline

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — console traffic was 434 calls and 2.0% of all context tokens: about 70 PowerShell `SerialPort` listeners, 101 calls through a sourced helper whose `with_log` ran a command on one console while recording the other, 33 hand-built `(sleep N; send) & capture` commands averaging 1.25 KB of command text, and 72 runs of 2 to 5 back-to-back status reads (180 calls)
**Scope:** api
**Hardware:** verify-only — reclassified from `bench` on filing by the 2026-10-25 leg: the tool, its filters and snapshots are client code testable against the mock Core; the two-console bench check and the replay are its hardware-verification debt. It builds on `tasks/core/100` (Core's background capture), so dispatch it after that lands.
**Owner:** no

## What

The client half of Core's background capture (drafted alongside as `core-capture-a-signal-in-the-background`), shaped so an interactive session spends one call where it spent three to five. A new tool `bench_exchange` (CLI `bench-exchange`) takes `steps`, each `{signal, write, until?, timeout_ms?, delay_ms?}` run in order, and `listen`, a list of signals recorded from before the first step until `tail_ms` after the last. It returns one timeline, one line per row (`+ms`, signal, text), on Core's receive clock, with each step's reply in place, and applies filters before anything reaches the caller: per-signal include and exclude patterns, a Zephyr log-level floor (`<wrn>` drops `<inf>` and `<dbg>`), and a per-signal line cap that reports how many lines it dropped. Named snapshots in project config (a list of status commands across signals, for example both PD stacks' status and a sense reading) run with `snapshot: "<name>"` and answer in the same shape. Escape stripping comes from the plain-replies item (`api-plain-console-replies`), not a second implementation here.

## Why now

The field sessions rebuilt this helper by hand in each bench session, and wrote the capture plumbing into the command line every time; in the six weeks bench work overall was 1,290 calls and 6.2% of context tokens, and the console part of it is the share one tool can take.

## Done when

- [ ] `bench_exchange` on MCP and CLI runs `steps` and `listen` in one Core request set and returns the merged timeline.
- [ ] Include, exclude, level floor and line cap apply per signal; dropped-line counts appear in the answer.
- [ ] Named snapshots in project config, validated against declared signals at load.
- [ ] Bench check on two consoles: a command on one console and an expected log line on the other land in the right order with their receive times.
- [ ] Replay: one recorded role-swap check (a command on the partner console, the DUT log recorded for 3 s, then both stacks' status: 3 to 4 helper calls and about 1.9 KB of output in the field) runs as one call; compare calls, command characters and result characters.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
