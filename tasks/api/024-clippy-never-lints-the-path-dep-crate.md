# 024 — `cargo clippy --all-targets` at the api root never lints `crates/embarch-core-client`'s tests, and one is already red

**State:** claimed by agent/api/024-clippy-reaches-the-path-dep-crate, 2026-09-06 04:25
**Source:** `inbox/api-clippy-skips-the-path-dep-crates-tests.md`, dropped by `agent/api/020-bearer-sweep-exhaustive` 2026-09-06 while running the §10 gate.
**Scope:** api
**Hardware:** none. One lint fix, one manifest-or-gate decision, no board and no live Core.
**Owner:** no

## What

`cargo clippy --all-targets -- -D warnings` at the `embarch-api` repo root is
green and has been. Run the identical command from inside
`crates/embarch-core-client` and it fails:

    error: unused import: `super::*`
        --> src/client.rs:1721:9
    error: could not compile `embarch-core-client` (lib test) due to 1 previous error

Not a regression from `api/020` — the drop reproduced it on `embarch-api` `main`
at `943419b`, and that branch touched only `tests/core_client_http.rs`.

The cause is structural and is the same one `tasks/suite/007` recorded for
`cargo fmt`: `crates/embarch-core-client` is a **plain path dependency, not a
workspace member** (`cargo metadata` reports `embarch-api` as the sole package).
`--all-targets` expands the *root package's* targets; a dependency is built as a
lib only, so the sub-crate's `#[cfg(test)] mod tests` is never compiled and never
linted. `cargo test` at the root has the same blind spot — decision 46 already
records that for tests, which is exactly why the `CoreClient` tests were put in
`embarch-api/tests/` rather than in the sub-crate.

So the suite has a crate with 28 unit tests that no gate command anyone types
ever lints, in the one crate `embarch-ui` also path-depends on.

## Why now

The lint is red today, in a shared crate, and nothing reports it. `tasks/suite/007`
has just corrected `embarch.md` §5's rustfmt reversal condition for the same
blindness, so the reason is currently written down in one place and this is the
cheap moment to close the clippy half beside it.

## Scope boundary — read this before you plan

Two of the drop's three acceptance items are **not yours**, and this task is
narrowed accordingly:

- Amending `embarch-fleet/protocol.md` §10's gate is **owner-only**. Do not edit it.
- Amending `embarch.md` §5 is **supervisor-only** (`protocol.md` §3). Do not edit it.

What *is* yours: the lint, the repo-side mechanism you choose, the decision
record for it, and a drop describing what the suite-level docs then owe.

## Done when

- [ ] `crates/embarch-core-client/src/client.rs:1721`'s unused `use super::*;` is
      gone (or the `mod tests` block that no longer needs it is), and
      `cargo clippy --all-targets -- -D warnings` is green **run from inside that
      crate** as well as from the repo root.
- [ ] A decision recorded in `embarch-api/decisions/` on which mechanism closes
      the blind spot: the sub-crate becomes a **workspace member** so one root
      command reaches it, or the gate grows a per-path-dep-crate leg. Argue both;
      the workspace-member route is the smaller standing cost and the larger
      one-time change. If you take the workspace-member route, make it — it is an
      `embarch-api` manifest change and it is in scope. Check what it does to
      `embarch-ui`, which path-depends on this crate: say in the decision whether
      a consumer outside the workspace is affected, and how you established that.
      Record the 28-unit-test blind spot as the evidence, and cite decision 46,
      which already names the `cargo test` half.
- [ ] `embarch-api/open.md` no longer claims this is unexamined, if it does.
- [ ] **A drop in `inbox/`** naming what the suite-level docs owe once this lands:
      §10's gate command list and `embarch.md` §5's reversal condition should
      describe the fmt and clippy blind spots in one place rather than two.
      Neither file is yours; the drop is how that crosses.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Doc-size reserve for `api` at dispatch time

Nothing in `embarch-api/` is in reserve — `api/023`'s split paid `decisions/shape.md`
down to 7,654 B. **But the corpus is one paragraph from the wall in five places**,
and the reserve line for a `decisions/*.md` is 11,059 B:

| file | bytes | headroom to reserve |
|---|---|---|
| `decisions/zephyr.md` | 11,056 | **3 B** |
| `interfaces/config.md` | 11,008 | 51 B |
| `decisions/build.md` | 10,934 | 125 B |
| `decisions/surface.md` | 10,928 | 131 B |
| `decisions/core-link.md` | 10,879 | 180 B |
| `open.md` | 4,521 | 87 B (cap 5,120) |

Your decision is about the build/gate wiring, so `decisions/build.md` (125 B) is
its natural home and **it will not fit**. `decisions/tests.md` is new, 5,434 B,
and holds decisions 30, 46 and 54 — the test-reach mission. A gate that does not
reach a crate's tests is that mission, so **write it there** unless you can argue
better. Say in your report which file you chose and why.

If your work pushes any file into reserve, file
`tasks/api/<NNN>-compact-api.md` in the same commit per `tasks/README.md` —
**`tasks/api/`, not `tasks/doc/`**, which `check-ownership.py` refuses to you.
