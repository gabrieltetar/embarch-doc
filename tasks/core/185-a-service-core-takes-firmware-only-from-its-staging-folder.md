# 185 — A service Core takes firmware only as bytes or from its own staging folder

**State:** open
**Source:** EMB-330 — A service Core would flash any file its own account can read
**Issue:** EMB-330
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`POST /flash` takes `firmware_path` and `manifest_path` in its JSON body and
reads them as given (`src/api.rs`, around lines 530 to 660). No staging folder
exists and no link is checked. The client already sends bytes to a WSL-host or
remote Core. Under its own account, Core could be asked to flash its own
signing key onto a DUT through `firmware_path`, and the agent could read it
back. The design this implements (`embarch-doc/notes/hil/12-prevention.md`,
item 9): Core "refuses `firmware_path` and `manifest_path` pointing anywhere
else, since Core under its own account would read any file its account can, its
own signing key included"; a staging folder Core owns and the engineer may
write into, "which Core opens without following links"; "every Core route that
takes a path follows the same rule".

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction; follow it, and record any deviation in the decision):

- With `--service`, both paths are refused unless they resolve inside
  `<data dir>/staging/`. Each component is resolved against the folder; a
  symlink, a hardlink (link count above one), a junction or any other reparse
  point is refused; `..` and absolute paths outside are refused.
- The multipart upload is unchanged.
- A development Core keeps `firmware_path`, since it reads nothing the engineer
  cannot.
- One helper, so a later route that takes a path uses the same check.
- The elevated install creates the staging folder (a later task); Core refuses,
  not creates, when it is missing.

**Not yours:** `embarch-api` (its client is unchanged: it already sends bytes
where it must), and every other repo. You never touch hardware: use the fake
flash backend.

## Where to look

- `src/api.rs` — `FlashRequest`, the JSON branch of `/flash`
- `src/flash_backend.rs` — the vendor staging copy
- `run --service` (`src/main.rs`, the attested Core whose store is
  `<data dir>/store/`) is what "service mode" means here; key the check on it
- `embarch-doc/embarch-core/decisions/flashing.md` (10, 18; 6.8 KB of 12 KB);
  `embarch-doc/notes/hil/12-prevention.md` item 9

## Where the doc goes

Amend decisions 10 and 18 in `decisions/flashing.md`, or write a new decision
there with an index row (take the next free number when you write it, by
scanning the headings as `DOC-CONVENTIONS.md` says, and cite only that number
in code comments). `interfaces/` gives the refusal. **Over or near the
per-decision cap, do not grow:** `signing#110`, `analog-capture#127`,
`host-study#95`, `definitions#133`, `lease#93`, `stopping-a-study#128`.
**`open.md` is 3,917 B, 2 B under its reserve line, and `spec.md` 9,011 B, 28 B
under it.** If your edit puts either into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md` has the
shape; number from `scripts/check-task-numbers.py --next core`).

## Done when

- [ ] In service mode on Linux: a symlink, a hardlink, a `..` path and an
      absolute path outside staging are each refused before the file is
      opened; a plain file inside is flashed (fake backend).
- [ ] In development mode, `firmware_path` behaves as today.
- [ ] The Windows reparse-point check type-checks for `x86_64-pc-windows-msvc`
      (`cargo check --target x86_64-pc-windows-msvc` where the target is
      installed; say if it is not); a hardware-verification debt is written
      into this file for a junction test on Windows.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`).
- [ ] Decisions 10 and 18 amended (or a new decision written); `changelog.d/`
      fragment.
