# embarch-core decisions: Bootloading over MCUboot serial recovery

**Status:** active, 2026-09-30.

The second way firmware reaches a DUT, beside a probe's `POST /flash`: a signed image handed to the DUT's own MCUboot serial-recovery bootloader over its USB CDC ACM port. The cross-repo design, and what is still to build: [bootload-proposal.md](../../bootload-proposal.md). The SMP client is [`embarch-smp`](../../embarch-smp/spec.md); the two port identities are [`embarch-topology` decision 36](../../embarch-topology/decisions/link-declares.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 77 — `POST /bootload` checks the image first, refuses a tapped port by name, and reports whether the application came back

**Serial recovery, not an application-side SMP server**: the bootloader writes the image straight into the primary slot and works when the application is broken, which is the case a bench most needs covered. The cost is that an upload overwrites the running application, so every check that can refuse is placed **before the first chunk**, and the ones that need no device before `hw_lock`:

- **The image is parsed before the lock is taken.** It must be an MCUboot image carrying a SHA TLV (`embarch_smp::ImageInfo`), because MCUboot validates every image against one at boot. An unsigned `zephyr.bin` is a `400` naming `zephyr.signed.bin`, rather than an image the bootloader accepts, writes over the application, and then refuses to boot.
- **A port a study's direct-route tap holds is a `409` naming it.** Those taps take no lock (decision 30(a)), and Windows lets one process open a COM port once, so without this the upload fails mid-study with an opaque open error. `AppState::tap_ports` is the registry: a tap claims its port when it opens and releases it after its reader thread joins. Checked for both declared ports up front, and for the bootloader's again once it enumerates.
- **An ambiguous identity is a `409` before anything is written** — both declared identities are resolved at the start, not only the one needed first.

**Getting in is declared, never guessed** ([embarch.md](../../embarch.md) §5). A bootloader already enumerated needs nothing, and that is checked first. Otherwise the project's `entry_command` and line ending are written to the application's port, the port is closed, and the bootloader's identity is polled for. No command, no application port, or neither port enumerated is a `409` saying which.

**The result says what happened, not only whether.** `entered_via` (`already-in-bootloader` | `shell-command`), bytes, requests, `duration_ms`, `upload_ms`, and **`app_reappeared`, reported rather than asserted**: an image the bootloader took and the application then failed to start is a real outcome and must not read as a transport error. It is `null` when no application identity is declared, since there was nothing to watch for. A failure the DUT caused — no enumeration, an SMP error or timeout, a failed reset — is a `502` carrying whatever the bootloader printed outside SMP, because on a shared console that is often the only account of why it went quiet.

**The DUT's outpost manifest is cleared just before the first chunk**, keyed by the enrolled DUT row's chip — the same rule `/flash` follows for an image with no manifest, applied at the moment the old image stops existing rather than on success, since a failed upload has already erased it.

**Every timeout is a named placeholder** (`bootload::PLACEHOLDER_TIMEOUTS`): nothing has been timed on a real DUT. The flow runs through a `Bench` trait, so the tests drive it end to end against `embarch_smp::sim` with a simulated re-enumeration. **Multipart only**: a signed image is small, and `/flash`'s JSON path exists for a same-machine case that bootload does not need to distinguish.

### 78 — The DUT's bootload ports are declared through Core, with no role in the path

`PUT`/`GET`/`DELETE /bootload/ports` wrap `embarch_topology::hardware::bootload`. **Core is the writer for the same reason it is for `/signals`**: `enrollment.toml` sits inside the service's NTFS permission wall, so a terminal-side writer would not work where the suite actually runs. The role is always `dut` — dev-bench firmware goes on by probe, and topology refuses any other role — so putting it in the path would offer a choice that has one answer. An overlapping pair is a `400` before `hw_lock`; `DELETE` answers `404` when nothing was declared, the distinction `DELETE /signals/{name}` draws.
