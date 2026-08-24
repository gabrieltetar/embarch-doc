# embarch-topology: milestone 1 — first rollout

**Status:** first rollout closed except one deferred sub-check, 2026-08-24. The crate, the
CLI/UI binary, and all three consumers' wiring are code-complete, merged to each repo's `main`,
and pushed (§2 items 1-2, done). The live Windows Core is deployed, both real boards are
enrolled and validated, and a real `build_and_flash` + `run_study` cycle has completed clean
end-to-end (§2 items 3-4's enroll/validate/regression parts, done) — a real bug found running
that first study (dev-bench's link-port serial needing its own declared fact,
`design.md` decision 17) was fixed and redeployed live along the way. What's left: item 4's
deliberate-mismatch/alert/SSE sub-check (explicitly skipped this session, see its own note) and
the non-blocking §5 items (§2 item 6).

## 1. What's already done

- `embarch-topology` repo scaffolded locally (`git init`, committed) — lib crate (`software`
  always on, `hardware` feature-gated) + `embarch-topology` CLI/UI binary (`bin` feature).
  `cargo test`/`cargo test --features hardware`/`cargo test --features bin` and
  `cargo clippy --features bin --all-targets -- -D warnings` all clean on Linux.
- `embarch-core`, `embarch-api`, `embarch-umbrella` all wired to depend on it, each on its own
  local `topology-integration` branch (not merged to `main`). Each repo's own
  `cargo build`/`cargo test`/`cargo clippy --all-targets -- -D warnings` passes against the real
  dependency; `cargo tree` confirms `embarch-api`/`embarch-umbrella` never pull in
  `probe-rs`/`serialport`.
- `release.yml` fixed in all three consumer repos (a real, latent gap: none of them checked out
  a path dependency's sibling repo at all) plus a new `release.yml`/`test.yml` for
  `embarch-topology` itself.
- `embarch-topology/design.md` §4/§5 updated to reflect what shipped vs. what's still open;
  `embarch-core/design.md`, `embarch-api/design.md`, `embarch-umbrella/design.md` updated in the
  same pass (new decisions/updates, per-doc changelog entries).

## 2. What's left

1. ~~**Push `embarch-topology` to GitHub.**~~ Done, 2026-08-21 — the user created
   [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology) themselves
   after this session's own `gh repo create` attempt was blocked (an outward-facing action);
   pushed to `main`. CI (`test.yml`: default/`+hardware`/`+bin` tests, `clippy --features bin`)
   ran on the push and passed clean in 3m36s
   ([run 32529687422](https://github.com/gabrieltetar/embarch-topology/actions/runs/32529687422)) —
   the first confirmation this builds on a real GitHub-hosted runner, not just this session's
   own Linux/WSL2 sandbox.
2. ~~**Merge and push the three `topology-integration` branches.**~~ Done, 2026-08-23 —
   the user asked directly, closing the "commit/push only when asked" gate this item was
   waiting on. All three (`embarch-core`, `embarch-api`, `embarch-umbrella`) merged to `main`
   and pushed to `origin/main`; each is in sync with its remote (no divergence either
   direction). Same pass also found and closed a real gap: the unpowered-target diagnosis
   (`design.md` §3 decision 16, `embarch-core/design.md` §3 decision 26) existed only as
   uncommitted working-tree changes in both repos — despite an earlier session believing it
   already shipped — now committed and pushed too.
3. ~~**Deploy to the live Windows Core.**~~ Done, 2026-08-23 (re-deployed again 2026-08-24 with
   decision 17's fix, see item 4) — `embarch-core update <new-exe>` self-elevated (UAC
   approved), the installed binary now matches the merged `main` build byte-for-byte,
   `com.embarch.core` restarted and confirmed `Running`, `GET /status`/`GET /enroll` both
   reachable from WSL2 over the gateway IP. `embarch-api` has no persistent service to deploy —
   its locally-run debug binary (the exact path Claude Code's MCP config spawns) is rebuilt
   against the merged dependency instead. `embarch-umbrella` has no live install anywhere on
   this machine to update (`which embarch` finds nothing) — nothing to deploy until `setup` is
   actually run again. A real `flash`/`reset`/`run_study` cycle end-to-end against the
   redeployed Core is confirmed — see item 4.
4. **Live-validate against real hardware.** Done, except one deliberately-deferred sub-check:
   - ~~Re-enroll both real boards (DUT, dev-bench) via `POST /probes/enroll`, confirm
     `validate_role`/`validate_serial` both still pass.~~ Done, 2026-08-24 — DUT (nRF54L15,
     J-Link `000852006107`) enrolled now that it's powered (`check_target_powered`, decision 16,
     didn't fire — clean attach); dev-bench (esp32c5, ESP JTAG) re-confirmed. Re-enrolling
     dev-bench a second time produced the identical `hardware_id`, confirming the live-identity
     recheck is consistent.
   - ~~A real `flash`/`reset`/`run_study` cycle end-to-end against the redeployed Core.~~ Done,
     2026-08-24 — real `reset`, then a real `build_and_flash` (`reference-dut-fw`,
     `dut_dev@7`/`reference-dut`) succeeded. The first real `run_study` attempt surfaced a genuine
     bug: dev-bench's link-port detection was ambiguous against the DUT's own separate J-Link
     VCOM interface (`design.md` decision 17) — fixed, tested, redeployed live (both
     `embarch-topology` and `embarch-core` rebuilt and the running Windows service updated via
     its own `update` self-elevation), then `run_study` completed both steps (`BleConnect`,
     `GattDiscover`) `Pass` — a real BLE connection and full GATT-table discovery against the
     freshly-flashed DUT.
   - **Still open, explicitly deferred:** deliberately induce a mismatch and confirm the alert
     lands in the durable log, the structured `topology-mismatch` error's `fix_it_url` is
     correct, and — with `embarch-topology ui` running — the live SSE push reaches a browser
     tab. `enroll`'s own API can't be used to fake this (it always writes a fresh, correct
     live-read `hardware_id`, by design); the two remaining routes — writing `enrollment.toml`
     directly, or physically swapping a probe without re-enrolling — were respectively blocked
     (a Claude Code permission classifier correctly denied the direct file write to a live
     production file) and declined by the user this session ("skip this sub-check"). Closed
     2026-08-24 by design decision, not a documentation deep-dive: the nRF54L15
     `FICR.INFO.DEVICEID` address (`embarch_topology::hardware::hardware_id`,
     `0xFFC304`/`0xFFC308`) is still sourced from a DevZone report, not Nordic's own Product
     Specification — a rigorous datasheet cross-check was considered and deliberately not
     pursued, not worth the depth. Accepted instead on this session's real, repeated,
     successful use against the real DUT: `enroll`/`reset`/`build_and_flash`/`run_study` all
     read a stable, plausible value at this address across multiple calls. Revisit only if a
     real symptom (e.g. a `hardware_id` collision) ever points back at it.
5. **`cross`'s Docker-based aarch64 release leg seeing sibling path dependencies — theoretical
   doubt resolved 2026-08-24 by research, real-run confirmation still open.** No Docker was
   available in this dev sandbox to run `cross` for real, so this was checked against
   `cross-rs/cross`'s own history instead: [PR #684](https://github.com/cross-rs/cross/pull/684)
   (merged, shipped `v0.2.2`+, well below what `taiki-e/install-action@v2` installs today)
   auto-mounts any path dependency `cargo metadata` can see, no formal `[workspace]` required —
   exactly `embarch-core`'s plain `path = "../embarch-topology"` shape. `embarch-core`'s
   `release.yml` comment updated with the citation (`embarch-api`/`embarch-umbrella` don't hit
   this at all — they only need a plain aarch64 cross-linker, not `cross`'s Docker build). What's
   left is mechanical: an actual tagged-release CI run to confirm it for real.
6. **Everything `design.md` §5 still lists as open** — not blocking, but worth another pass once
   the above is live: web UI content/UX, an MCP tool surface for `validate`/alerts (and the
   caller-opens-the-UI question that depends on one existing), wiring
   `recommended_bind_address()` into `embarch-umbrella`'s `setup`, and whether a remote Core's
   declared host address should move into this crate's own storage.
