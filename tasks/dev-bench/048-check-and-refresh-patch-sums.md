# 048 — Check and refresh the sha256 sums in a patches.yml

**State:** claimed by agent/dev-bench/048-check-and-refresh-patch-sums, 2026-11-17 18:09
**Source:** EMB-146, filed by an audit after `tasks/dev-bench/036` reworded two carried Zephyr patches and recomputed their sums by hand
**Issue:** EMB-146
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

Every edit to a carried patch means recomputing its `sha256sum` by hand and
pasting it into `patches.yml`. `west patch` checks the sums only at `apply`
time, after a workspace is set up, and has no verb that rewrites them.

Add a small script to `embarch-dev-bench`, for example `scripts/patch-sums.py`:

- `--check <patches.yml>` lists every entry whose `sha256sum` does not match the
  file it names, and exits non-zero when any does.
- `--update <patches.yml>` rewrites only those `sha256sum` values in place,
  leaving every other field, the order and every comment byte-for-byte as they
  were. A YAML round-trip that reflows the file is not acceptable; edit the
  value on its line.
- Runs without a west workspace and without network, from the repo alone.
  Patch paths resolve the way `west patch` resolves them; read how before
  writing it, and say it in the script's help.

Start with `workspaces/pd-bench/manifest/zephyr/patches.yml`; any other
`patches.yml` in the repo should work the same. If the repo's gate has a natural
place for `--check`, add it there so a stale sum fails before `west patch apply`
does, and say in `spec.md` where.

**Public repo.** Tests use synthetic `patches.yml` and patch files in a temp
folder.

**Burndown leg: no new numbered decision.** A real design fork goes to
`scripts/fleet-linear.py file --from decision`.

**What you may change.** Only `embarch-dev-bench` and `embarch-doc/embarch-dev-bench/`.

**Doc reserve.** Nothing of `embarch-dev-bench`'s is in reserve, but several
decision entries are within 200 B of their limit (`logging` 38 and 39,
`ble` 34 and 37, `protocols` 41, `conventions` 47, `capture` 29). This unit
should not need to edit any of them.

## Why now

The owner moved EMB-146 to Fleet Ready.

## Done when

- [ ] One command reports every `patches.yml` entry whose `sha256sum` does not match its file, and exits non-zero when any does.
- [ ] One command rewrites those `sha256sum` fields in place, leaving every other field and comment untouched; a test compares the rest of the file byte for byte.
- [ ] `pd-bench/README.md` names the command where it says how to change a patch.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
