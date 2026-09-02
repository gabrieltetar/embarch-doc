# embarch-api: milestone 9 — Study Designer: Feature-Branch Iteration

**Status:** done, 2026-08-24 — §3.1–3.7 all closed for real; see §6's final entries. A real, previously-unknown production bug (a stack-overflow crash in `study_status` on any GATT-sized result, `embarch-api/design.md` decision 36) had to be found and fixed before §3.4 onward could even return a result rather than crash the MCP server. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 3 ("Study Designer: Feature-Branch Iteration" — filed on disk as `milestone-9`). Companion to [embarch-study-designer/milestone-9.md](../embarch-study-designer/milestone-9.md) (new wire types), [embarch-dev-bench/milestone-9.md](../embarch-dev-bench/milestone-9.md) (dispatching them on real firmware), and [embarch-core/milestone-9.md](../embarch-core/milestone-9.md) (the concurrent DUT-flash + dev-bench-study validation). See [design.md](design.md) §5/§5a for the `build_and_flash`/`run_study`/`study_status` surface this milestone drives, all already implemented and validated separately (Milestone 1, Milestone 2) — the new thing here is running both together against two real, independent boards in one session.

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

- [x] `list_targets` run live against the real checkout, target confirmed rather than assumed (§3.1) — `dut_dev@7`/`reference-dut` confirmed live 2026-08-24, on the branch actually checked out (`bugfix/gpio-debounce-ppg-work-queue`, per §2's own correction).
- [x] `build_and_flash` succeeds against the real DUT, config-only (§3.2) — succeeded repeatedly across every real run this milestone, including mid-concurrency-check (§3.7).
- [x] DUT confirmed advertising post-flash (§3.3) — confirmed indirectly but conclusively: a real `BleConnect` from dev-bench succeeded, which is only possible if the DUT was advertising.
- [x] The milestone's `Study` fixture submitted and run to completion via CLI (§3.4) — confirmed 2026-08-24 via `run-study --study-file`/`study-status`, both on the debug and `--release` binaries.
- [x] Real `BleConnect`/`GattDiscover`/`GattMonitorAll` results confirmed correct (§3.5) — `BleConnect` `Pass`, `GattDiscover` `Pass` with 8 real GATT services/characteristics (real UUIDs, real ATT properties bytes), `GattMonitorAll` `Pass` with a clean (empty, nothing dropped) `gatt_activity`.
- [x] The same run repeated and confirmed via MCP (§3.6) — confirmed 2026-08-24 via `run_study`/`study_status` MCP tools, same real result shape as the CLI path.
- [x] Concurrent DUT-flash + dev-bench-study behavior confirmed alongside `embarch-core/milestone-9.md` (§3.7) — confirmed 2026-08-24: a `build_and_flash` against the DUT issued while a 25s dev-bench `BleAdvertise` study was in flight; both completed successfully, unaffected by each other.
- [x] The milestone's actual Definition of Done — one successful end-to-end run, build→flash→connect→GATT-exchange→data forwarded into `events.json` — achieved and observed directly, not just inferred from individual steps passing. Achieved twice for real (once via MCP, once via CLI), plus a third clean CLI run — `GET /study/{id}` confirms the full result round-trips through `events.json` correctly.
- [x] Any real gap found folded back into `design.md` per `DOC-PROTOCOL.md` §5 — done (§6): the production stack-overflow fix (new decision 36) and a real, unresolved ~50% DUT-connect flake rate.
- [x] **`embarch-core/design.md` decision 22 implemented, and both real boards enrolled via `enroll_probe`/`enroll-probe`** — implemented, deployed, and both boards enrolled as of 2026-08-20/21. **Superseded 2026-08-21**: this table/gate moved into the new shared `embarch-topology` crate (`embarch-topology/design.md` §3 decisions 2/3) — the capability is live and was exercised throughout this milestone's real runs, just no longer as this repo's own code.

## 5. Open questions / risks carried into execution

- ~~**Whether `fix/bouncing_dock`'s current (empty) state is still current by the time this milestone executes**~~ — moot: the branch actually used turned out to be `bugfix/gpio-debounce-ppg-work-queue` (§2), not `fix/bouncing_dock` at all, with a real landed commit (`5ba862c`) — recorded here per this item's own reasoning.
- **Whether reference-dut's real advertising behavior (name, service UUIDs in the advertising/scan-response data) gives dev-bench's `target_address: None` central-role `BleConnect` enough to find it unambiguously**, especially if other BLE devices are active nearby during the live run — untested until §3.3/§3.4 actually run.
- **No convenience "flash the DUT and run the study in one call" wrapper exists or is planned** — matches this suite's existing minimal-viable posture (`embarch-study-designer/design.md` §6's own "no block-until-done wrapper" precedent); §3.7's ordering checks are manual, two separate tool calls, not a new bundled operation.
