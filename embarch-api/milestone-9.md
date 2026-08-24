# embarch-api: milestone 9 — Study Designer: Feature-Branch Iteration

**Status:** in progress, 2026-08-20 — the dev-bench build/flash pipeline prerequisite (§6) is done and deployed; §3.1/§3.2 actually ran for real (DUT flashed on the real `bugfix/gpio-debounce-ppg-work-queue` branch, not `fix/bouncing_dock` — §2 corrected below), but §3.3 onward are now blocked on a second, deeper prerequisite found flashing/resetting real hardware for the first time this milestone (`embarch-core/design.md` decision 22 — see [embarch-core/milestone-9.md](../embarch-core/milestone-9.md) §6 for the full narrative). **`enroll_probe`/`enroll-probe` (decision 34) is now implemented and Linux-tested** — still needs a Windows deploy and both real boards actually enrolled before §3.3 can resume. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 3 ("Study Designer: Feature-Branch Iteration" — filed on disk as `milestone-9`). Companion to [embarch-study-designer/milestone-9.md](../embarch-study-designer/milestone-9.md) (new wire types), [embarch-dev-bench/milestone-9.md](../embarch-dev-bench/milestone-9.md) (dispatching them on real firmware), and [embarch-core/milestone-9.md](../embarch-core/milestone-9.md) (the concurrent DUT-flash + dev-bench-study validation). See [design.md](design.md) §5/§5a for the `build_and_flash`/`run_study`/`study_status` surface this milestone drives, all already implemented and validated separately (Milestone 1, Milestone 2) — the new thing here is running both together against two real, independent boards in one session.

## 1. Goal, restated for embarch-api

Milestone 1 proved `build_and_flash` against the real `reference-dut-fw` repo. Milestone 2 proved `run_study`/`study_status` against real dev-bench hardware, with no DUT involved. Neither has ever been exercised *together* — this milestone is that: flash a real reference-dut DUT via the same config-only, live-`list_targets`-discovered path Milestone 1 established, then submit a `Study` that has dev-bench connect to that exact DUT, discover its GATT table, and monitor it — all through this project's existing tool surface, no new MCP tool or CLI subcommand needed.

## 2. Scope for this milestone

- ~~**DUT repo/branch: `reference-dut-fw`, checked out at `fix/bouncing_dock`.**~~ — **corrected at execution time**: that branch had no commits past `main`, so the real DUT branch used is `bugfix/gpio-debounce-ppg-work-queue` (real landed fix, `5ba862c`) instead, checked out directly in the main checkout (not a worktree — see §6 for why). This milestone's Definition of Done is unaffected either way: the chain working end to end, independent of whatever fix eventually lands on that branch (`embarch-dev-bench/milestone-9.md` §2).
- **Target selection: not hardcoded here, same discipline as Milestone 1** (`design.md` §3 decision 12, `embarch-api/milestone-7.md` §2) — run `list_targets` live against this checkout rather than assuming Milestone 1's discovered `dut_dev@7`/`reference-dut`/`ble-shell` combination still applies to this branch/config; confirm rather than reuse.
- **Dev-bench board: ESP32-C5-WROOM-1 DK**, already connected and powered as of this milestone's design pass — no new board bring-up needed, unlike Milestones 1/2.
- **The `Study` fixture** (new, checked into `embarch-study-designer` or authored directly for this run — exact location TBD at execution time): `BleConnect` (central, no `target_address`) → `GattDiscover` → `GattMonitorAll`, `steps_crc` auto-filled by `run_study` (decision 26) as always. No `PowerSampleWindow`, no `validations` — matches the DoD decided in this milestone's design pass (data landing in `events.json`, not a content assertion).
- **Both CLI and MCP paths**, matching Milestones 1/2's own precedent of validating each separately rather than assuming one implies the other (`embarch-api/milestone-8.md` §3.8 found a real MCP-only schema bug the CLI path structurally couldn't hit).
- **Standing autonomy applies unchanged** (`embarch-api/milestone-7.md` §2's own note, generalized 2026-08-17): the one real precondition is physical — both boards need to actually be connected and powered, which as of this milestone's design pass is already true (dev-bench) or is this milestone's own first step (the DUT). Once both are, every step below runs straight through.
- **Out of scope:** any new MCP tool/CLI subcommand (none needed, §1); power-data/waveform-data content (still correctly empty, same as Milestone 2); a second reference-dut board/variant.

## 3. Steps

### 3.1 Run `list_targets` live against the real `fix/bouncing_dock` checkout

Confirm which board/variant/revision is actually file-backed on this branch, rather than assuming Milestone 1's discovered combination still holds — same live-discovery discipline that milestone's own §2 already established as this project's permanent mode, not a one-time bootstrap.

### 3.2 `build_and_flash` the reference-dut DUT, config-only

Same config-only path Milestone 1 validated (no `--firmware-path` override) — confirms that path still works against a different branch/commit than Milestone 1 originally flashed, not just the one commit that happened to be checked out then.

### 3.3 Confirm the DUT boots and advertises

A plain post-flash sanity check (via whatever the DUT's own BLE advertising looks like — the reference-dut firmware's normal boot behavior, not a new embarch-api capability) before submitting a `Study` that assumes something is there to connect to.

### 3.4 Author and submit the milestone's `Study` fixture via `run_study` (CLI)

The `BleConnect`→`GattDiscover`→`GattMonitorAll` sequence (§2). Poll `study_status` to a terminal state.

### 3.5 Confirm the result

`study_status`'s `result.steps` shows `BleConnect` reaching `Pass` against a real peer address (not dev-bench's own), `GattDiscover`'s `gatt_services` populated with real UUIDs, and `GattMonitorAll`'s `gatt_activity` reflecting real captured traffic (cross-checked against [embarch-dev-bench/milestone-9.md](../embarch-dev-bench/milestone-9.md) §3.8/§3.9's own verification).

### 3.6 Repeat §3.4–3.5 via MCP, not just CLI

Matching Milestone 2's own precedent (`embarch-api/milestone-8.md` §3.8) of never assuming the CLI path validates the MCP path — run the identical `Study` through a real MCP client this time.

### 3.7 Confirm concurrent DUT-flash + dev-bench-study behavior, alongside [embarch-core/milestone-9.md](../embarch-core/milestone-9.md) §3.3/§3.4

From this project's side: issue a `build_and_flash` and a `run_study` in the orderings that doc's steps specify, confirming neither call is unexpectedly blocked or errors due to the other.

## 4. Definition of done

- [ ] `list_targets` run live against the real `fix/bouncing_dock` checkout, target confirmed rather than assumed (§3.1).
- [ ] `build_and_flash` succeeds against the real DUT, config-only (§3.2).
- [ ] DUT confirmed advertising post-flash (§3.3).
- [ ] The milestone's `Study` fixture submitted and run to completion via CLI (§3.4).
- [ ] Real `BleConnect`/`GattDiscover`/`GattMonitorAll` results confirmed correct (§3.5).
- [ ] The same run repeated and confirmed via MCP (§3.6).
- [ ] Concurrent DUT-flash + dev-bench-study behavior confirmed alongside `embarch-core/milestone-9.md` (§3.7).
- [ ] The milestone's actual Definition of Done — one successful end-to-end run, build→flash→connect→GATT-exchange→data forwarded into `events.json` — achieved and observed directly, not just inferred from individual steps passing.
- [ ] Any real gap found folded back into `design.md` per `DOC-PROTOCOL.md` §5.
- [ ] **`embarch-core/design.md` decision 22 implemented, and both real boards enrolled via `enroll_probe`/`enroll-probe`** — a new, unplanned prerequisite (§6) blocking §3.3 onward; see [embarch-core/milestone-9.md](../embarch-core/milestone-9.md) §4/§6 for the full narrative. Decision 22 and decision 34's `enroll_probe`/`enroll-probe` wrapper are both implemented and Linux-tested 2026-08-20; still needs a Windows deploy and both real boards actually enrolled before this checks off.

## 5. Open questions / risks carried into execution

- ~~**Whether `fix/bouncing_dock`'s current (empty) state is still current by the time this milestone executes**~~ — moot: the branch actually used turned out to be `bugfix/gpio-debounce-ppg-work-queue` (§2), not `fix/bouncing_dock` at all, with a real landed commit (`5ba862c`) — recorded here per this item's own reasoning.
- **Whether reference-dut's real advertising behavior (name, service UUIDs in the advertising/scan-response data) gives dev-bench's `target_address: None` central-role `BleConnect` enough to find it unambiguously**, especially if other BLE devices are active nearby during the live run — untested until §3.3/§3.4 actually run.
- **No convenience "flash the DUT and run the study in one call" wrapper exists or is planned** — matches this suite's existing minimal-viable posture (`embarch-study-designer/design.md` §6's own "no block-until-done wrapper" precedent); §3.7's ordering checks are manual, two separate tool calls, not a new bundled operation.

## 6. Changelog

- 2026-08-20 — **Decision 34's `enroll_probe`/`enroll-probe` implemented, closing this milestone's own blocking prerequisite in code — deploy and real-board enrollment still outstanding.** `core_client.rs`/`tools.rs`/`cli.rs`/`main.rs` all gained the new tool/subcommand, a thin wrapper over Core's new `POST /probes/enroll` (`embarch-core/design.md` decision 22, implemented the same pass — see that project's own `milestone-9.md` §6). `cargo build`/`cargo test` (59 passed)/`cargo clippy --all-targets -- -D warnings` clean on Linux. Not yet deployed to the live Windows Core; neither the DUT nor dev-bench is enrolled yet — §3.3 onward stays blocked until both are.
- 2026-08-20 — **§3.1/§3.2 ran for real against the corrected DUT branch, then a real hardware scare paused everything from §3.3 onward.** The originally-scoped `fix/bouncing_dock` had no commits past `main` (§2 corrected); switched to `bugfix/gpio-debounce-ppg-work-queue` (`5ba862c`, a real landed fix). First flash attempt failed on a real Kconfig bug in that branch's own new `lib/ppg_work_q` library (a missing/misresolved `PPG_WORK_Q` symbol) — traced to a west-workspace-level mismatch (the shared `.west/config` manifest path still pointing at the main checkout while building from a linked worktree of the branch), not a firmware bug at all; resolved by checking the branch out directly in the main checkout instead of using a worktree, sidestepping the mismatch entirely rather than reconfiguring the shared west workspace. `build_and_flash` then succeeded for real. Immediately after, real flash/reset activity across both boards this session surfaced a genuine hardware scare — the DUT needing a manual `west flash --recover`, dev-bench's native USB port going unresponsive — root-caused to real `probe-rs`/target quirks (not corruption) and partly fixed (`embarch-core/design.md` decision 21), but that investigation surfaced a deeper, unresolved vulnerability (decision 22: nothing today confirms a probe answering to a recorded serial is still wired to the board its config labels it as). §3.3 onward (boot confirmation, the Study fixture, CLI+MCP validation, concurrency checks) are blocked on decision 22 landing — full narrative in [embarch-core/milestone-9.md](../embarch-core/milestone-9.md) §6. New DoD item added (§4).
- 2026-08-20 — **A real, unplanned prerequisite surfaced and closed before any of §3's own steps could start: this milestone's design pass assumed dev-bench was "already connected and powered — no new board bring-up needed" (§2), but nothing in `embarch-api` could actually flash the *new* dev-bench firmware `embarch-dev-bench/milestone-9.md` produced — `list_projects` only ever configured the DUT.** New `build_dev_bench`/`flash_dev_bench`/`build_and_flash_dev_bench` (`embarch-api/design.md` §3 decision 32, per the user's explicit call that dev-bench must not share `[[projects]]` with DUT firmware) closes that gap. Building it surfaced two further real gaps, neither anticipated: `flash`/`build_and_flash` never actually exposed `base_address` despite `embarch-core` supporting it since Milestone 2; and `probe_serial` — needed the moment the DUT's own J-Link and dev-bench's ESP JTAG probe were attached simultaneously for the first time — was never threaded through from this side, and (found the same session) was never actually implemented in `embarch-core` either, despite that project's design doc saying otherwise. `cargo build`/`test`/`clippy` all clean; a real fresh dev-bench build succeeded. **§3's own steps (list_targets/build_and_flash against the DUT, the Study fixture, CLI+MCP validation) have not started** — blocked on a Windows-side rebuild+restart of the real, currently-running `embarch-core` with the `probe_serial` fix, which this WSL2 environment can't perform itself; the user is handling that directly. Resumes once confirmed back up.
- 2026-08-19 — Initial draft, scoping `embarch-api`'s half of Milestone 3 (Study Designer: Feature-Branch Iteration): drives `build_and_flash` and `run_study`/`study_status` together against two real, independent boards for the first time, using the same config-only/live-discovery/CLI-and-MCP discipline Milestones 1 and 2 each separately established.
