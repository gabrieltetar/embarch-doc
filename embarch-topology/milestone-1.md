# embarch-topology: milestone 1 — first rollout

**Status:** in progress, 2026-08-21. The crate, the CLI/UI binary, and all three consumers'
wiring are code-complete and locally verified (`design.md` §4, §6) — this doc tracks what's
left to actually ship it, per `design.md` §5's "first-rollout migration" item.

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
2. **Merge and push the three `topology-integration` branches**, once the user has reviewed the
   diffs — deliberately left uncommitted-to-`main`/unpushed by this pass (general harness
   guidance: commit/push only when asked; this task's own scope was "implement," not "ship").
3. **Deploy to the live Windows Core.** This session ran entirely from Linux/WSL2 against a
   local git checkout — nothing here has touched the real Windows-hosted install
   `embarch-dev-workflow.md` §5 describes as daily-used. The real rollout needs, in order: build
   `embarch-core` on/for Windows with the new dependency, `embarch-core update <new-exe>`
   (self-elevating, per that repo's `service.rs`), then re-confirm `GET /status` and a real
   `flash`/`reset`/`run_study` cycle still work end to end.
4. **Live-validate against real hardware**, once deployed:
   - The nRF54L15 `FICR.INFO.DEVICEID` address (`embarch_topology::hardware::hardware_id`,
     `0xFFC304`/`0xFFC308`) — sourced from a DevZone report, never independently confirmed
     against this suite's own DUT (carried over unchanged from `embarch-core/design.md`'s prior
     open item on this exact address).
   - Re-enroll both real boards (DUT, dev-bench) via `POST /probes/enroll` /
     `embarch-topology enroll`, confirm `validate_role`/`validate_serial` both still pass.
   - Deliberately mismatch one (re-enroll a probe as a different chip, or physically swap
     boards without re-enrolling) and confirm: the alert lands in the durable log, the
     structured `topology-mismatch` error's `fix_it_url` is correct, and — with
     `embarch-topology ui` running — the live SSE push actually reaches a browser tab.
5. **Confirm `cross`'s Docker-based aarch64 release leg can actually see sibling path
   dependencies outside the crate root** — flagged as unverified in `embarch-core`'s (and now
   `embarch-api`'s/`embarch-umbrella`'s) `release.yml` comments; needs a real tagged release run
   to know either way.
6. **Everything `design.md` §5 still lists as open** — not blocking, but worth another pass once
   the above is live: web UI content/UX, an MCP tool surface for `validate`/alerts (and the
   caller-opens-the-UI question that depends on one existing), wiring
   `recommended_bind_address()` into `embarch-umbrella`'s `setup`, and whether a remote Core's
   declared host address should move into this crate's own storage.
