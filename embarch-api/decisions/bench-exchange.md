# embarch-api decisions: bench_exchange

**Status:** active, 2026-10-26.

Index: [../decisions.md](../decisions.md). Surface: [../interfaces/tools-capture.md](../interfaces/tools-capture.md). Built on [tool-wrapping.md](tool-wrapping.md) 88 and `embarch-core` decision 92.

### 89 — `bench_exchange`: one call runs a console sequence and returns every listened console as one timeline, on this client's clock
Field use on a USB PD board spent 434 calls on console traffic: listeners, a helper that ran a command on one console while recording the other, and runs of back-to-back status reads. The tool takes `steps` (`{signal, write, until?, timeout_ms?, delay_ms?}`) and `listen` (signals recorded from before the first step to `tail_ms` after the last), and answers with one `timeline` string: `+ms signal> write` for a command, `+ms signal| text` for received text. It is built on the capture calls (88): it starts one capture per listened signal, polls them while the steps run through `signal_exchange_with`, then drains and stops them. `max_s` of each capture is sized from the steps' own budget (+10 s, at most Core's 600).

**Times are the client's, not Core's, and the answer says so (`time_basis`).** Core's capture returns a byte range with no per-line receive time (`embarch-core` 92), so a captured line is stamped with the poll that first saw it: a ceiling within `poll_ms` (default 100, minimum 20), a write is stamped just before its request, an unlistened step's reply when it returned. Rows sort by that time, ties by arrival order. A gap shorter than `poll_ms` between two consoles is not a measurement. **Measured: no. Assumed: 100 ms is fine enough for a human-paced bench.** Exact order wants Core to stamp lines: `inbox/core-capture-line-receive-times.md`.

**A reply on a listened signal appears once.** An exchange on a captured signal goes through its capture (92), so its bytes are already there; the step's reply is dropped from the rows and the capture's rows carry it (`reply_in: "capture rows"` in the step summary). A step on an unlistened signal puts its reply into the timeline at the time it returned.

**No escape stripping here.** Nothing named `api-plain-console-replies` exists. Core's text goes through with its ANSI codes, and filters work on text that still carries them: `include`/`exclude` are case-sensitive substrings (no regex dependency), and the level floor (`err|wrn|inf|dbg`, tag `<wrn>` etc. searched anywhere in the line) keeps a line with no tag. Writes are never filtered. Per signal, or `"*"` for the rest; a per-signal `max_lines` keeps the first N and the counts of what filters and caps dropped come back under `dropped`.

**Declared-signal checks.** Config load checks a snapshot's shape (non-empty steps, signal and write, no empty `until`); that every signal is *declared* is Core's to say, so `bench_exchange` calls `list_signals` first and refuses an undeclared name, listing the declared ones, **before any capture or write** (the earliest point Core is reachable; a snapshot cannot be checked at load). A capture that cannot start (Core's `409`) stops the call with nothing written. A failed step stops the later ones; the answer still carries the timeline so far with `success: false`.

**Snapshots** live in `[projects.snapshots.<name>]` (`steps`, `listen?`, `tail_ms?`); `snapshot` (+ `project` when several declare it) runs after the explicit `steps` and joins `listen`.

*Rejected: stamping rows with Core's `elapsed_ms`* (one value per read, not per line: it would label a client poll as Core's clock). *Rejected: a regex filter*: a new dependency for a substring the field used.
