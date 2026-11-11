# embarch-dev-bench: open questions

**Status:** active, 2026-09-04.

What is unresolved, and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Root-caused, not fixed

- **The bench resets mid-transmission, and a truncated `StepResult` is its shadow** — a step failure surfaces only as a *connection error*. Core's side is fixed ([embarch-core](../embarch-core/decisions/studies.md) decision 40); the reset itself is not.

  **Failure signature, consistent with a crash, not a transport fault:** a byte-perfect prefix with the tail simply absent; a last byte that can be *corrupt*, the line having gone idle mid-byte so the remaining bits sample as idle `1`; nothing following, not even a close; only long frames losing their tail, since short ones finish before the window; and **intermittency**, shown by consecutive handshakes at wildly different uptimes rather than any byte pattern.

  ***Rejected: a 16-byte TX boundary.*** "The number that identifies it is 16" came from subtracting a delimiter-inclusive length from an exclusive one; six captured occurrences were short by different amounts, none of them 16. **There is no boundary to find.** What needs finding is why the bench reboots.

## Never exercised

- **Bond clearing has never been observed firing on real hardware.** Decision 11's clearing step is reasoned, not observed — an attempt to verify it stopped before connecting; the owner accepted the risk instead. **Still not an observation.**
- **The fatal-error path is designed and untested.** No fault has been induced to watch a Zephyr fatal dump reach Core through the synchronous fatal-path sink (spec §4).
- **Nothing has been validated against a DUT with no input/output capability.** Against such a peer, Just Works is forced, L4 unreachable, and the security step should `Fail` reporting the level reached (decisions 34, 37) — untested, because the bench's real DUT requires and supplies L4.

## Unmeasured

- **What a loud study costs is unmeasured.** Verbosity is per-run (decision 39); nobody has measured what a `Debug` run costs a study's own timing on a wire the protocol shares — including whether the log buffer's overrun (spec §5) matters to it.
- **Clock-resync accuracy is not validated.** No timestamp this firmware produces is UTC-corrected — arrival stamps come off device uptime with no host-clock offset tracking.

## Deferred, with the reason

- **GPIO/analog stimulus.** Real future scope; needs a new `Action` variant upstream first, not just firmware.
- **Power-sampling hardware and the DUT connector**, at the repo owner's call. Decision 24's PPK2 pick is provisional, unordered.
- **A local hardware watchdog** (decision 14) — deferred, not rejected; revisit on real hangs.
- **On-board status indication** — revisit if polling proves insufficient for debugging.
- **An independent host-side BLE scan confirming advertising**, not just the bench's self-report.
- **Cross-vendor Zephyr-revision reconciliation** (decision 3) — could two vendor families share one workspace? The per-family layout works; nothing forces it.
- **[Boreas](https://github.com/intercreate/boreas) as a future ESP-IDF path.** Rejected for standing the ESP32-C5 up (decision 26); worth separate consideration.

## Carried, not upstream

- **pd-bench's six USB-C patches are carried, not upstream** (decision 58), so every pin move re-applies them. Closes when a release holds all six and `workspaces/pd-bench/` needs no `patches.yml`.
- **Which copy of a patch leads, and how a fix reaches the other, waits on the owner.** The workspace they came from is on v4.5.0 now, and its copies differ.

## Structural

- **Detecting "the bench isn't actually connected"** — unplugged, wrong port — is `embarch-core`'s responsibility, not this firmware's.
