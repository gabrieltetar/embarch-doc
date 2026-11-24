# 012 — The folder-name decode finds a checkout however crowded the folders above it are

**State:** done — decode charges the budget only for fitting children; guard type and 3200-sibling test added
**Source:** found re-running the gate on `promptu/011` (2026-11-23): `cargo test` fails on a machine whose temp folder holds about 3,800 subfolders
**Issue:** EMB-286
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

`claude::tests::a_folder_name_decodes_back_to_the_checkout_on_disk` fails
whenever the temp folder is crowded: `decode_folder` returns `None` for a
scratch checkout that exists. `descend` (in `src/claude.rs`) spends one shared
budget of 2000 directory entries on every child it lists, sorted, whether or not
that child's encoded name fits the folder being decoded, so a parent folder with
more than about 2000 subfolders exhausts it before the walk reaches the match.
Measured on the gate machine: `/tmp` held 3,793 directories. The same test
passes with `TMPDIR` pointed at a near-empty folder.

The test also removes its scratch folder only after its asserts pass, so every
failed run leaves one more folder behind and the failure feeds itself.

When this is done:

- `decode_folder` finds an existing checkout whose encoded path matches, however
  many non-matching siblings sit in any folder above it. Keep a bound against a
  pathological walk, but charge it for the work that can actually match (the
  children whose encoded name fits), not for every entry listed. The design is
  yours. Keep the behaviour the existing tests pin down, including the
  ambiguity cases.
- The test cleans up on failure as well as on success. A guard type whose
  `Drop` removes the folder works.
- A test creates more than 3000 sibling folders beside the target under a
  scratch root, and the decode still finds the target.

## Why now

A red `cargo test` on `main` makes every later Promptu unit's gate read red for
a reason that is not that unit's, and step 4's units (`promptu week …`) are
queued behind it.

**Burndown leg: no new numbered decision.** If a decision or the contract
states the walk's bound, amend it in place.

## Done when

- [x] `decode_folder` finds the target with more than 3000 non-matching sibling folders, in a test.
- [x] A failed run of the decode test leaves no scratch folder behind.
- [x] `cargo test --all-targets` passes with the machine's own crowded `/tmp`, and `cargo clippy --all-targets -- -D warnings` is clean.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated where they describe the walk, and a `changelog.d/` fragment dropped.
