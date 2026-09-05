# embarch-dev-bench: open questions

**Status:** active, 2026-09-02.

What is unresolved, and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Root-caused, not fixed

- **The bench resets mid-transmission, and a truncated `StepResult` is its shadow** — so the one message whose job is to explain a step failure is the one that cannot get through, and the study died reported as a *connection error*. Core's side is fixed ([embarch-core](../embarch-core/decisions/studies.md) decision 40); the reset itself is not.

  **Failure signature, all of it consistent with a crash and none of it with a transport fault:** a byte-perfect prefix with the tail simply absent; a last byte that can be *corrupt*, the line having gone idle mid-byte so the remaining bits sample as idle `1`; nothing following, not even a close; only long frames losing their tail, since short ones finish before the window; and **intermittency**. The proof is an uptime comparison rather than a byte pattern — consecutive handshakes reported 899,843 ms then 46,320 ms.

  ***Rejected: a 16-byte TX boundary.*** "The number that identifies it is 16" came from subtracting a delimiter-inclusive length from a delimiter-exclusive one, and six captured occurrences were short by 15, 17, 17, 13, 17 and 13 — none of them 16, with a seventh identical frame arriving complete. **That number was the whole basis of the previous diagnosis and there is no boundary to find.** What needs finding is why the bench reboots; the candidates have not been narrowed.

## Never exercised

- **Bond clearing has never been observed firing on real hardware.** The handshake is confirmed against a real board, but decision 11's clearing step has only been reasoned about — nothing has shown a study starts from a genuinely unbonded link rather than one that happened to be clean.
- **The fatal-error path is designed and untested.** Switching to synchronous, lock-free writing inside the faulting context is what would carry a Zephyr fatal dump out to Core, and no fault has been induced to watch it.
- **Nothing has been validated against a DUT that presents no input/output capability.** Against such a peer the spec's own matrix forces Just Works whatever this bench declares, L4 becomes unreachable, and the security step will `Fail` reporting the level it did reach — correct behaviour, untested, because the DUT this bench has requires L4 and supplies the capability for it.

## Unmeasured

- **What a loud study actually costs is still unmeasured.** Per-study verbosity replaced a compile-time ceiling, so the bandwidth question is now per-run rather than global — but nobody has measured what a `Debug` run costs a study's own timing on a wire the protocol shares. The 1 KB log buffer overruns on a debug burst and reports it; whether that matters to a measurement is unknown.
- **Clock-resync accuracy is not validated.** No timestamp this firmware produces is UTC-corrected — arrival stamps come off device uptime, and no host-clock offset tracking is implemented for any of them.

## Deferred, with the reason

- **GPIO/analog stimulus.** Real future scope, and it needs a new `Action` variant upstream first, not just firmware.
- **Power-sampling hardware and the DUT connector**, as a whole, at the repo owner's call. Decision 24's PPK2 pick is provisional and unordered.
- **A local hardware watchdog** (decision 14) — deferred, not rejected; revisit on real hang experience.
- **On-board status indication** — revisit if polling proves insufficient for bench-side debugging.
- **A host-side BLE scan as independent confirmation of advertising**, rather than only the bench's self-report.
- **Cross-vendor Zephyr-revision reconciliation** (decision 3) — whether two vendor families could ever share one workspace. Deliberately unsolved; the per-family layout works and nothing forces it.
- **[Boreas](https://github.com/intercreate/boreas) as a future ESP-IDF path.** Rejected for the narrow task of standing the ESP32-C5 up (decision 26); a real idea worth its own consideration separately.

## Structural

- **`tx_scratch` holds a `struct dbm_study_start` it can never contain**, ~15.7 KB. The union is sized by its largest member regardless of which tag a send uses, and Core is the only sender of a `StudyStart`. A TX-only message type would reclaim it — **the single largest remaining lever on ESP32-C5 SRAM**, which has overflowed three times.
- **Detecting "the bench isn't actually connected"** — unplugged, wrong port — is entirely `embarch-core`'s responsibility, not this firmware's.
- **Only a build that links the real staticlib exercises the FFI schema-version call.** `native_sim` links no crate to compare against, by construction, so decision 20's fix closes the number being *wrong* and not the blind spot itself.
