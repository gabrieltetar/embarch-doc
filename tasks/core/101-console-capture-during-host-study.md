# 101 — Capture both PD stacks' consoles for a whole host study while its steps write to them

**State:** claimed by agent/core/101-console-capture-during-host-study, 2026-10-26 09:03
**Reserve (2026-10-26 09:03 leg):** `open.md` **50 B left**, `spec.md` 474 B left, `decisions/probes.md` 1,025 B left, all three filed against `core/112` (blocked, `In flux: yes`). Do not grow `open.md` or `spec.md`; if you must, compact that file in this unit, carrying `core/112`'s `Must not delete:` list and closing only that file's item there.
**Dispatch note:** two boxes below are not a worker's. The CY4500 decision needs the analyzer's capture format confirmed on the analyzer, which no worker can do: do not decide it by inference; drop an `inbox/` file for it (absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/`) and leave the box open. The bench check is a hardware debt for the supervisor: write it into this file. Close the task `done` when every other box is ticked.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — every exchange drops what the console printed since the last one (`discard_pending`, `embarch-core/src/exchange.rs:223`), and a listen lasts at most 10 s. The field scripts listened in 42 windows of 1.5 to 6 s. The 8-Hard-Reset count (56 s, two consoles) bypassed Core with two PowerShell readers, and 44 Bash calls opened COM ports directly
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

In a host study, a `Signal` tap on a writable direct signal opens its port once, on its tap thread, for the whole study. An `Exchange` step on that signal writes through the tap thread and takes its reply from the same byte stream, starting at its own write, with the echo rule applied. **Nothing the console prints between steps is lost**, and Windows' one-open-per-COM-port limit is respected (`embarch-host-study-proposal.md` §Core). Two consoles tapped in one study, the PD partner's and the DUT's, give both sides of each PD exchange on Core's one receive clock. Today a tap record is whatever one `port.read()` returned (`read_signal_tap`, `embarch-core/src/study.rs:2648-2668`), and the tap claims the port for itself (`study.rs:2635`). After this change, a chunk is split at newlines before it is stored, so each line has its own receive time. The raw bytes stay on disk, and ANSI is stripped only in views. Outside a study, `signal-exchange` is unchanged.

## Why now

The field project had no scope, and the CY4500 analyzer is a Windows GUI that nothing reads. So its timing evidence came from the two stacks' INF logs, for example a 13.52 s PPS timeout measured between two console lines. An event that fell between listen windows was lost. The only complete two-console capture took a hand-written PowerShell script outside Core's lock.

## Done when

- [ ] A tapped and exchanged signal is opened once, and the exchange reply equals the tap bytes between the write and `until`.
- [ ] Two direct console taps with exchanges on both run in one study. A test covers it with two virtual serial pairs.
- [ ] Each stored line carries Core's receive time, on one monotonic clock across taps.
- [ ] `decisions.md` records a decision on the CY4500. Either a `Prompt` asks the operator to save the analyzer's capture and Core attaches that file to the study result, or the analyzer is declared out of scope. The capture format is confirmed on the analyzer before either.
- [ ] Bench check, run by the supervisor: 8 Hard Resets sent from `pd-bench` with both consoles tapped. The event counts match a direct read of the same ports.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
