# 024 — `cargo clippy --all-targets` at the api root never lints `crates/embarch-core-client`'s tests, and one is already red

**State:** done, 2026-09-06 — `agent/api/024-clippy-reaches-the-path-dep-crate`
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

- [x] `crates/embarch-core-client/src/client.rs`'s unused `use super::*;` is
      gone, and `cargo clippy --all-targets -- -D warnings` is green **run from
      inside that crate** as well as from the repo root. **It was at 1713, not
      1721** — `api/022` moved it. It was a *second* `use super::*;` in the same
      `mod tests`, the first being at 1585, so removing it is a plain deletion;
      the block still needs the import.
- [x] A decision recorded in `embarch-api/decisions/` on which mechanism closes
      the blind spot: the sub-crate becomes a **workspace member** so one root
      command reaches it, or the gate grows a per-path-dep-crate leg. Argue both;
      the workspace-member route is the smaller standing cost and the larger
      one-time change. If you take the workspace-member route, make it — it is an
      `embarch-api` manifest change and it is in scope. Check what it does to
      `embarch-ui`, which path-depends on this crate: say in the decision whether
      a consumer outside the workspace is affected, and how you established that.
      Record the 28-unit-test blind spot as the evidence, and cite decision 46,
      which already names the `cargo test` half.
- [x] `embarch-api/open.md` no longer claims this is unexamined, if it does. It
      did not claim it either way; its smoke-harness bullet now records the blind
      spot as closed **and** that it was found by hand rather than reported, and
      that nothing yet says whether another crate sits behind the same one.
      `spec.md`'s "path dependency rather than a workspace member" sentence was
      outright false after this and is corrected.
- [x] **A drop in `inbox/`** naming what the suite-level docs owe once this lands:
      §10's gate command list and `embarch.md` §5's reversal condition should
      describe the fmt and clippy blind spots in one place rather than two.
      Neither file is yours; the drop is how that crosses.
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## What was done

**Decision 56, in `decisions/tests.md`** — not `decisions/build.md`, which had
125 B and would not have held it, and not `core-link.md`, which had 22. The
dispatch note guessed `tests.md` and the guess is right on the merits too: the
entry is about what the gate reaches, it amends decision 46 in place (46's stated
reason for putting the `CoreClient` tests in `embarch-api/tests/` expired with
this change), and 46 and 54 are the two entries it argues from.

**The route taken is workspace membership**, and the manifest change is
`members` **plus `default-members`**. `members` alone leaves `embarch-api` as the
sole `workspace_default_members` and a bare root `cargo clippy` still misses the
sub-crate — verified by planting an unused import and watching it stay green,
then go red once `default-members` was added. `default-members` is what lets the
**unamended** §10 command reach it, which matters because §10 is owner-only.

**`embarch-ui` is unaffected**, established by building a synthetic
out-of-workspace consumer with the identical `path =` line from a directory with
no `[workspace]` ancestor. Decision 56 records the limit of that method: it
reproduces the shape of `embarch-ui`'s dependency, not `embarch-ui`.

`crates/embarch-core-client/Cargo.lock` (43 KB, tracked) is deleted — a member's
lockfile is never read, and no consumer ever read it either.

**Two side effects worth a reader's attention.** `cargo test` at the root now
runs the sub-crate's 28 unit tests; all 28 pass. And `cargo fmt -p embarch-api -p
embarch-core-client --check` is now *accepted* — `embarch.md` §5 says that
spelling refuses — which rides `status.d/api-fmt-p-is-now-an-escape-hatch.md`.

This commit pushed `embarch-api/open.md` and `spec.md` into reserve (they were 6
and 3 bytes clear of it), so `tasks/api/028-compact-api.md` is filed here.

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
