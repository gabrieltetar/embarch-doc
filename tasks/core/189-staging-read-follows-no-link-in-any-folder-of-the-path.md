# 189 — A staging read follows no link in any folder of the path

**State:** claimed by agent/core/189-staging-read-follows-no-link-in-any-folder-of-the-path, 2026-11-27 01:12
**Source:** EMB-593 — staging read still follows a parent swapped for a link after the check (reviewer finding on `core/185`)
**Issue:** EMB-593
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Decision 160 (`core/185`, merge `364cf99`) says a service Core reads `/flash`'s
`firmware_path` and `manifest_path` only through `staging::read`, and that "the
bytes are read from the handle that passed the check ... so a link swapped in
afterwards is never followed". That holds only for the last component.
`src/staging.rs` `read` checks each component with `symlink_metadata` in a
loop, then opens the joined path with `open_nofollow`; `O_NOFOLLOW` on Unix and
`FILE_FLAG_OPEN_REPARSE_POINT` on Windows cover the final component alone. A
folder under `staging/` replaced by a link between its check and the open is
followed, and the read leaves the folder. It needs a nested name and a writer
inside `staging/`. The hardlink and link-count checks run on the handle and
are sound.

When this is done, either:

- a nested name is resolved without a gap, for example by opening each folder
  with no-follow relative to the previous folder's handle (`openat` with
  `O_NOFOLLOW | O_DIRECTORY` on Unix; on Windows, a handle per folder opened
  with `FILE_FLAG_OPEN_REPARSE_POINT` and checked for a reparse point, or a
  check of the opened file's final path against the staging folder), and a
  test swaps a parent folder for a link between check and open; or
- if no sound resolution fits both platforms, nested names are refused
  outright (`400`, as for `..`), which makes the claim true by removing the
  case, and 160 says so.

Prefer the first only if both platforms get it; do not leave Windows on the
weaker guarantee without saying so in 160. Record which you chose and why.

**Not yours:** every other repo, and the multipart `/flash` path. You never
touch hardware.

## Where to look

- `src/staging.rs` (`read`, `open_nofollow`, the component loop, its module
  comment), its call site in `src/api.rs` `flash_handler`
- `embarch-doc/embarch-core/decisions/flashing.md` (10, 18, 160)
- the Windows arms cannot be built under WSL (hidapi blocks the crate); the
  `core/185` worker type-checked them in a throwaway crate, and so can you

## Where the doc goes

Amend decision 160 in place (`decisions/flashing.md`, 8,134 B, room) and the
`staging.rs` module comment. **`interfaces/hardware.md` is 11,055 of 12,288 B,
4 B under its reserve line**: if the `/flash` note there needs a word, keep it
net-neutral, or file `tasks/core/<NNN>-compact-core.md` in the same commit
(`tasks/README.md` has the shape; number from
`scripts/check-task-numbers.py --next core`). `open.md` is 3,916 B, 4 B under
its reserve line: net-neutral or smaller. `spec.md` is in reserve and filed
against `tasks/core/186`: do not grow it.

## Done when

- [ ] A parent folder swapped for a link between check and open is not
      followed (tested on Unix), or nested names are refused (tested).
- [ ] 160 and the `staging.rs` module comment state exactly the guarantee the
      code gives, on each platform.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
