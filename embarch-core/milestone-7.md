# embarch-core: milestone 7 — Flash & Build (real hardware)

**Status:** done, 2026-08-18. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 1 ("Flash & Build (real hardware)" — filed on disk as `milestone-7`, per that doc's filename note). Companion to [embarch-api/milestone-7.md](../embarch-api/milestone-7.md) — that doc covers embarch-api's half, including the live target-discovery steps that drive what gets flashed here. See [design.md](design.md) for the durable architecture record.

## 1. Goal, restated for Core

Core's half of Milestone 1 (Flash) already proved Core runs natively on Windows, is reachable from WSL2, and can `/flash`/`/reset`/`/serial-log` against real hardware — against `project-a-board`. This milestone doesn't re-prove any of that mechanism; it re-points the same, already-working Core at a different physical board (a real reference-dut board, via `embarch-api`'s live-discovered target — [embarch-api/milestone-7.md](../embarch-api/milestone-7.md) §3.4) and confirms nothing board-specific breaks. Given this suite's track record — every real-hardware/real-repo contact so far has surfaced at least one genuine gap the design assumed away (Milestone 1's `internal_err` swallowing and UNC-path bug; Milestone 6's `init` board-ambiguity and revision-overlay findings) — this milestone stays alert for a reference-dut-specific surprise rather than assuming Core's existing Windows setup just works unchanged.

## 2. Scope for this milestone

- **Board:** whichever real reference-dut target `embarch-api/milestone-7.md` §3.4 lands on via live `list_targets` discovery — not pre-selected here either, for the same reason it isn't pre-selected there.
- **Deployment:** reuse the existing Windows-native Core setup validated in Milestone 1 (§3.1–3.4 there) — no new Windows build/toolchain work expected unless something reference-dut-specific breaks it.
- Confirm the physical probe attached for the reference-dut board (may or may not be the same J-Link used for `project-a-board` — a Nordic DK's onboard debugger, if that's what's in use, is a different enumeration path worth confirming rather than assuming identical).
- Out of scope: `embarch-dev-bench`'s own DK/transport (Milestone 2, a different board entirely), multi-probe selection, ESP-IDF/`esptool` fallback (not relevant — reference-dut is Zephyr/nRF54L15 like `project-a-board`).

## 3. Steps

### 3.1 Confirm Core is up and reachable from WSL2, same as Milestone 1 left it

- If Core's already running (foreground or as the installed Windows service from Milestone 1 §3.5), confirm it's still reachable at the `base_url` embarch-api's reference-dut project config uses (`embarch-api/milestone-7.md` §3.2) — the WSL2 host-gateway IP is dynamic across restarts (`milestone-1.md` §3.4), so re-confirm rather than assume last session's address still holds.
- If Core needs restarting, prefer the already-validated foreground run (`embarch-core.exe run` with `EMBARCH_TOKEN` set) for this milestone's first attempt — the installed-service path (`milestone-1.md` §3.5) had an `EMBARCH_TOKEN` delivery gap that may or may not be fully closed; confirm the service path separately if it's the one actually in use.

### 3.2 Identify the physical probe for the reference-dut board

```
probe-rs list
```

Confirm what's actually attached — a standalone J-Link, or a Nordic DK's onboard debugger — and that probe-rs enumerates it on Windows the same way Milestone 1 §3.1 confirmed for `project-a-board`'s probe. If it's a different debugger type than Milestone 1 exercised, this is new ground for probe-rs's Windows USB backend, worth calling out explicitly rather than assuming parity.

### 3.3 Confirm the chip string for the live-discovered target

Once `embarch-api/milestone-7.md` §3.4 reports a real (board, variant, revision, app) tuple, confirm its SoC resolves via `/resolve-chip` to the expected probe-rs chip string:

```
probe-rs chip list | grep -i nrf54
```

Reference DUT is nRF54L15 per the suite's existing SoC coverage — this step confirms that holds for the actual selected board/cpucluster, not just family resemblance to `project-a-board`.

### 3.4 Validate `/flash`, `/reset`, `/serial-log` against the real board, from WSL2

Same manual isolation Milestone 1 §3.3 used — exercise each endpoint directly (or via embarch-api's CLI) before trusting the full `build_and_flash` chain, so a failure is attributable to Core vs. to embarch-api's build/discovery layer:

- `GET /status` — the probe (§3.2) appears.
- `POST /reset` — succeeds against the confirmed chip string (§3.3).
- `GET /serial-log` — confirm the real UART/CDC port Windows assigns this board (expect a different `COM<N>` than `project-a-board`'s `COM5`) and that a capture returns real output.
- `POST /flash` — deferred to `embarch-api/milestone-7.md` §3.7 (config-only path); do not flash manually here ahead of that step.

## 4. Definition of done

- ✅ Core is confirmed running and reachable from WSL2 at the address embarch-api's reference-dut config actually uses (§3.1) — `http://172.22.128.1:4884`, `wsl-host` topology.
- ✅ The reference-dut board's physical probe is confirmed visible to probe-rs on Windows (§3.2) — a standalone J-Link (`vid=0x1366, pid=0x1024, serial=000852006107`), same enumeration path as `project-a-board`'s, not a DK onboard debugger.
- ✅ The live-discovered target's SoC resolves to the correct probe-rs chip string via `/resolve-chip` (§3.3) — `nrf54l15` → `nRF54L15`, **but only after fixing a real gap**: the installed Core binary was stale (missing `/resolve-chip` entirely, last synced ~Aug 4). See §6.
- `/status`/`/reset` succeed against the real reference-dut board from WSL2 (§3.4) — ✅ both, repeatedly. `/serial-log` (via `embarch-api serial-log`) returned **no lines captured** across several attempts at the real UART port (`COM5`) — **root-caused and closed 2026-08-18, not a Core bug**: `/serial-log` was never actually meant to reach a DUT's own console UART, only `embarch-dev-bench`'s link (`design.md` §5, `embarch-decision-reversals.md` row 11); see `embarch-api/milestone-7.md` §4/§5 for the full finding.
- ✅ `/flash` succeeds against the real reference-dut board — via `embarch-api/milestone-7.md` §3.7–3.8's config-only CLI calls, against the **installed service**, not a foreground workaround. Along the way found a real, previously-unknown gap: the installed Windows service (`LocalSystem`, Session 0) cannot reach `artifact_path_for_core`'s `\\wsl.localhost` UNC path at all — confirmed by direct A/B test. **Fixed the same day**: `flash` uploads bytes instead of a path for this case now. Full detail: `embarch-api/design.md` §9. MCP path (§3.9 there) not yet exercised this session.
- ✅ No `usbipd attach`/`usbipd bind` anywhere in the path (same invariant as Milestone 1).
- ✅ Reference DUT-specific gaps found (stale binary/`/resolve-chip`, Session-0 UNC gap, `COM5` reused rather than a new port, empty `serial-log`) folded back into `design.md`/`embarch-api/design.md`/`embarch-decision-reversals.md` per DOC-PROTOCOL.md §5.

## 5. Open questions / risks carried into execution

- ~~**Probe type for the reference-dut board is unconfirmed**~~ — resolved: a standalone J-Link, same enumeration path as `project-a-board`'s (§3.2).
- ~~**Which `COM<N>` port the reference-dut board's UART/CDC lands on**~~ — resolved, but not as expected: `COM5`, the **same** port `project-a-board` used, not a different one. Not investigated further whether this is coincidence (both boards' J-Links happening to enumerate identically on this machine) or something more structural — not a blocker either way, just worth knowing if a third board ever needs distinguishing by port alone.
- ~~**Whether the installed-Windows-service path's `EMBARCH_TOKEN` delivery gap (Milestone 1 §3.5) is actually closed**~~ — moot for this finding: the foreground `run` path (which does work, per Milestone 1 §3.5's own guidance to prefer it "for this milestone's first attempt") resolved the token fine either way. The *installed-service* path has a different, more fundamental problem now (below) that makes the token question secondary.
- ~~**The installed service can't flash at all**~~ (§4) — Session 0 isolation blocked `\\wsl.localhost` access regardless of token delivery. Fixed the same day: `flash` uploads bytes instead of a path now. Full detail: `embarch-api/design.md` §9.
- ~~**`serial_log` returned empty**~~ — resolved 2026-08-18: not a capture-timing bug — `/serial-log` was never actually meant to reach a DUT's own console UART at all, only `embarch-dev-bench`'s link. `design.md` §5 corrected; `embarch-decision-reversals.md` row 11.
- Given every prior real-hardware/real-repo touch in this suite has surfaced at least one unanticipated gap, this run was no exception — two found (stale binary, Session-0 UNC gap), consistent with the pattern this section already flagged.
