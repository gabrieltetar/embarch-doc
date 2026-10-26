# 131 — One call drives a console sequence and returns every listened console as one filtered timeline

**State:** done — host side shipped and mock-tested; the two-console bench check and the replay are hardware-verification debts below (also in `embarch-api/open.md`)
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — console traffic was 434 calls and 2.0% of all context tokens: about 70 PowerShell `SerialPort` listeners, 101 calls through a sourced helper whose `with_log` ran a command on one console while recording the other, 33 hand-built `(sleep N; send) & capture` commands averaging 1.25 KB of command text, and 72 runs of 2 to 5 back-to-back status reads (180 calls)
**Scope:** api
**Hardware:** verify-only — reclassified from `bench` on filing by the 2026-10-25 leg: the tool, its filters and snapshots are client code testable against the mock Core; the two-console bench check and the replay are its hardware-verification debt. It builds on `tasks/core/100` (Core's background capture), so dispatch it after that lands.
**Owner:** no

## Dispatch note, 2026-10-26 05:59 leg

**Three facts the text below assumes and the code does not provide. Read them before designing.**

- **Core's capture carries no per-line receive time.** `GET /signals/{name}/capture` (decision 92, `embarch-doc/embarch-core/decisions/signal-capture.md`; client type `SignalCaptureResponse` from `api/143`) returns a byte range with `offset`, `next_offset`, `elapsed_ms` and `gaps`, nothing per line. A merged timeline "on Core's receive clock" cannot be built from that. Never label a client-side time as Core's. Either stamp and order rows by what the client actually observes and say so in the answer and the decision, or ship the one-call sequence with per-signal sections and drop `/home/gabriel/Github/embarch/embarch-doc/inbox/core-capture-line-receive-times.md` (full task format, `tasks/README.md`) asking Core to stamp lines. Your call; record it as a decision. `tasks/core/101` stamps lines only inside a host-study tap, so it does not cover this.
- **An exchange on a captured signal goes through the capture** (decision 92's tee paragraph): its reply bytes also land in that signal's capture. When a step writes to a signal in `listen`, the timeline must not show the reply twice.
- **There is no "plain-replies item".** Nothing named `api-plain-console-replies` exists in `tasks/` or `inbox/`. Do not build escape stripping here: pass Core's text through, make the level floor and patterns work on text that still carries ANSI codes, and say so in the decision.

**Reuse `api/143`'s client calls** (capture start/read/stop in `embarch-core-client`). That crate is a shared path dependency of `embarch-ui`: additive changes only, nothing renamed. **Doc reserve:** `embarch-api/decisions/client-crate.md` 11,581 / 12,288 B (707 B left), filed under `tasks/api/140` (open, not yours). A new decision goes in `decisions/tool-wrapping.md` or a new topic file, indexed in `decisions.md`. The two-console bench check and the replay are hardware-verification debts: write them in this file.

**Isolation, not optional.** No live Core (never the WSL2 gateway or `:4884`), no desk on `:4891`, no real serial ports or probes, no owner data or config dirs (`/var/lib/embarch`, `~/.config`, `%PROGRAMDATA%`, `~/.claude`): the mock Core and any CLI run use scratch ports and a scratch token file. Never call the `mcp__embarch-api__*`, desk, Slack or Linear tools (they reach live services as the owner), never run `claude -p`, and never `pkill` by name; stop only PIDs you started.

## What

The client half of Core's background capture (drafted alongside as `core-capture-a-signal-in-the-background`), shaped so an interactive session spends one call where it spent three to five. A new tool `bench_exchange` (CLI `bench-exchange`) takes `steps`, each `{signal, write, until?, timeout_ms?, delay_ms?}` run in order, and `listen`, a list of signals recorded from before the first step until `tail_ms` after the last. It returns one timeline, one line per row (`+ms`, signal, text), on Core's receive clock, with each step's reply in place, and applies filters before anything reaches the caller: per-signal include and exclude patterns, a Zephyr log-level floor (`<wrn>` drops `<inf>` and `<dbg>`), and a per-signal line cap that reports how many lines it dropped. Named snapshots in project config (a list of status commands across signals, for example both PD stacks' status and a sense reading) run with `snapshot: "<name>"` and answer in the same shape. Escape stripping comes from the plain-replies item (`api-plain-console-replies`), not a second implementation here.

## Why now

The field sessions rebuilt this helper by hand in each bench session, and wrote the capture plumbing into the command line every time; in the six weeks bench work overall was 1,290 calls and 6.2% of context tokens, and the console part of it is the share one tool can take.

## Done when

- [x] `bench_exchange` on MCP and CLI runs `steps` and `listen` in one Core request set and returns the merged timeline. (`src/bench_exchange.rs`; times are client-observed, decision 89; `tests/bench_exchange_cli.rs`.)
- [x] Include, exclude, level floor and line cap apply per signal; dropped-line counts appear in the answer.
- [x] Named snapshots in project config, validated against declared signals at load. (Shape validated at load; the declared-signal check runs at the start of each call, before any capture or write, because Core is not reachable at load. Decision 89.)
- [ ] Bench check on two consoles: **hardware-verification debt**, below.
- [ ] Replay: **hardware-verification debt**, below. Host-side measure: the whole replay is one CLI call of 281 characters (`--listen dut --tail-ms 3000`, a level-floor filter, three steps) in place of 3 to 4 helper calls; result characters need the real bench.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## What shipped

`bench_exchange` / `bench-exchange`, decision 89 in `embarch-api/decisions/bench-exchange.md`. Core's capture has no per-line time, so rows carry client-observed times (a captured line is stamped by the poll that first saw it, within `poll_ms`, default 100) and every answer says so; the Core ask is `inbox/core-capture-line-receive-times.md`. A reply on a listened signal appears once (through its capture); no escape stripping, filters are substring and level-tag matches on text that keeps its ANSI codes. Snapshots: `[projects.snapshots.<name>]`. `embarch-core-client` is unchanged; `embarch-firmware-build`'s `ProjectConfig` gained an additive `snapshots` field. Filed `tasks/api/144` (open.md is in reserve).

## Hardware-verification debts

- **Two-console order check.** Needs: two declared direct signals on a real board pair (a bench console and a DUT console, both USB-UART), Core running. Run: `embarch-api bench-exchange --listen dut --poll-ms 50 --steps '[{"signal":"bench","write":"<a command that makes the DUT log a known line>","until":"uart:~$ "}]' --tail-ms 2000`. Expect the `bench>` row first, the DUT line after it with a time at most `poll_ms` later than the wire, the reply once, and `captures.dut.state` stopped. Also run it across a DUT reset (USB re-enumeration) and confirm the `[embarch: port lost]` marker rows and `gaps` appear, and that a second concurrent call is a clean 409.
- **Replay.** One recorded role-swap check (command on the partner console, DUT log recorded 3 s, then both stacks' status) as one call; record calls, command characters (281 for the sketch above) and result characters against the field's 3 to 4 calls and about 1.9 KB.
