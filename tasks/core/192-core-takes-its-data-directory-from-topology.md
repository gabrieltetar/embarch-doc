# 192 — Core takes its machine data directory from `embarch-topology`

**State:** open
**Source:** EMB-307 — the machine data directory is resolved five ways, with three unset behaviours
**Issue:** EMB-307
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/token_store.rs` computes the machine data directory itself
(`%ProgramData%\embarch`, an error when `ProgramData` is unset;
`/var/lib/embarch` elsewhere), and `embarch-topology/src/hardware/paths.rs`
was a copy of it. `tasks/topology/074` puts one public
`machine_data_dir(TopologyClass)` in `embarch-topology` with one unset policy.
When this is done, every place Core derives the default machine data directory
calls `embarch_topology::machine_data_dir(TopologyClass::Local)` (or whatever
name `topology/074`'s decision gives it — read that decision, not this task),
and Core's own copy is gone. Behaviour is unchanged unless `topology/074`'s
unset policy differs from Core's current error; if it does, the decision says
so and so does Core's.

Grep for every default-data-dir derivation, not only `token_store.rs`
(`ProgramData`, `/var/lib/embarch`), and keep `--data-dir` overrides exactly as
they are.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/token_store.rs` (the resolver near the top), any other
  `ProgramData` / `/var/lib/embarch` site in `src/`
- `embarch-doc/embarch-topology/decisions/storage.md` (the decision
  `topology/074` wrote), `embarch-doc/embarch-core/decisions/auth.md`

## Where the doc goes

`spec.md` and `decisions/platform.md` are in reserve under `tasks/core/186`:
do not grow them. Amend the core decision that names the path in place
(`decisions/auth.md` names `ProgramData`), net-neutral if you can.

## Done when

- [ ] Core has no data-directory resolver of its own; it calls topology's.
- [ ] Existing token-store tests pass unchanged, or changed only where the
      unset policy moved, and the decision says why.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment. The Windows arm cannot be built
      under WSL (hidapi blocks the crate): type-check it as `core/185` did, and
      say so.
