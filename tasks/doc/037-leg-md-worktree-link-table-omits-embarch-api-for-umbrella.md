# `.claude/leg.md`'s worktree link table omits `embarch-api` for `embarch-umbrella`

**State:** done — the template's link table re-derived from every manifest in the suite, umbrella row gains `embarch-api` (fleet `039bd66`, owner/dispatch); lands by `deploy.py`
**Source:** supervisor leg 072, landing `umbrella/049` on 2026-09-10
**Scope:** doc
**Hardware:** none — a documentation/template fix plus, optionally, a check.
**Owner:** required — `.claude/` is owner-reserved and generated from
`embarch-fleet/scripts/install.py`'s template, so no agent may edit it.

## What

`.claude/leg.md`'s "link every sibling in the dependency *closure*" table says:

| worktree repo | link into its parent |
|---|---|
| `embarch-umbrella` | `embarch-topology`, `embarch-study-designer` |

`embarch-umbrella/Cargo.toml` line 47 has path-depended on
`embarch-core-client = { path = "../embarch-api/crates/embarch-core-client" }` for some time, so
the closure includes **`embarch-api`** and the table is already one link short.

`umbrella/049` (landed 2026-09-10, code `46ec5c0`) makes that omission bite harder than a build
failure. Its new drift-guard test in `src/config.rs` reads
`PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../embarch-api/config.example.toml")` — so an
`embarch-umbrella` worktree created strictly to the table fails `cargo test` with a panic naming a
path inside `.worktrees/`, which reads like a broken worktree rather than a missing symlink. That
is exactly the failure mode the table's own `embarch-ui` note calls "the trap".

It did not bite on leg 072 only because an earlier leg had made the `embarch-api` link by hand at
15:35 that day.

## Why now

The table is what a supervisor follows when it sets a worktree up, and the next umbrella unit
dispatched into a fresh worktree will hit it. The bolded-trap paragraph directly under the table
exists because this has already cost two legs.

## Done when

- [x] `embarch-umbrella`'s row in the template's table reads
      `embarch-topology`, `embarch-study-designer`, `embarch-api` — unbolded, because the table's
      bold means "transitive, not in the crate's own manifest" and this one is in it.
- [ ] Landed through `embarch-fleet/scripts/deploy.py` (not `install.py` by hand), so the instance
      gate stays green. **The owner's session, at landing.**
- [x] Consider whether the table should be generated from
      `grep -rn 'path *= *"\.\.' --include=Cargo.toml embarch-*/` rather than hand-kept — the
      file already names that grep as the source of truth when the table is wrong, which is an
      admission the table drifts.
      **Considered, not generated.** A rendered table would make `install.py` read sibling repos,
      which are not render inputs and sit outside the SHA `deploy.py --queue` pins — a queued
      deploy could then render something nobody committed. The drift is caught instead where it
      bites: `tasks/doc/046`'s `check-dispatch.py --created` resolves every relative Cargo
      path-dep from the worktree as created. The re-derivation also found what a Cargo grep
      cannot: `embarch-outpost`'s cross-decoder test and `embarch-dev-bench`'s CMake read siblings
      too, so the table carries both, and `embarch-core` gains `embarch-smp` (`tasks/doc/090`).
