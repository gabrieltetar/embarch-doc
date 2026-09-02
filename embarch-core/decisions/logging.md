# embarch-core decisions: Logging

**Status:** active, 2026-09-02.

Core's own log file, its HTTP surface, and the bench's separate debug file.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Logging

### 16, 29 — One daily-rolling log file, one implementation, three front ends
`tracing` output used to go wherever stderr landed — a real file only for a foreground `run` a human is watching, which is why the SCM start failure was diagnosed from the Windows Event Log by luck rather than design. **Setting up the writer is allowed to fail** without taking the CLI down: an unprivileged human on a machine where the log directory is not writable must not lose a CLI that worked before. `init_tracing()` runs before subcommand dispatch, so the foreground and SCM paths are covered by construction.

The HTTP pair mediates the *same* file for `embarch-ui`'s Debug tab, which had proposed a second size-capped logfile without knowing this one existed. Deliberately **not** a custom `tracing` layer broadcasting each line, which would mean modifying `init_tracing` in a live service; served as plain text, because reformatting a deployed service's output into JSON for one client is a bigger change than this needs. This decision read as shipped for days while the CLI subcommand did not exist — the third instance of that drift in one session, after decisions 9 and 11.

### 37 — A separate `dev-bench.log`, and a handshake that tolerates a log line before `HelloAck`
Once the bench turned `CONFIG_LOG` on, a log line stopped being a rare diagnostic and started carrying Zephyr's subsystem output and the fatal-error dump. **Why a third destination:** `core.log` is Core's account of what the *service* did, and interleaving a firmware's full output drowns what a reader opened it for; the study's reserved tap is scoped to one study by construction, so it cannot hold a line from a handshake that failed before the study started. A second *file*, not a second log *mechanism*.

**Two Core-side changes only running it surfaced, both of which would have made the firmware's half useless.** The handshake did one `recv` and failed anything that was not `HelloAck`, so turning firmware logging on would have broken every study and read as a protocol bug. And the boot record was reliably produced and reliably lost: the bench holds its boot log until the first `Hello` and flushes it after the ack — that flush *is* how a reboot becomes visible — but the handshake endpoint returned the instant it had the ack. **Core also writes the level each study asked for**, because otherwise a quiet file means either "the bench had nothing to say" or "this study asked for `Warn`", which are opposite conclusions about a study that just failed.

---
