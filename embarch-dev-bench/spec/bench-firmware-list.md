# embarch-dev-bench: the released bench-firmware list

**Status:** active, 2026-11-24 (EMB-389, `tasks/dev-bench/050`). No new decision: the design is `notes/hil/14-implementation-plan.md`'s, kept by the owner. Code: `scripts/bench-firmware-list.py`, tests `scripts/test_bench_firmware_list.py`.

A bench board's image reads as released only when its identity is in the list the release ships (`notes/hil/03-test.md`, "A run", item 3). This script writes that list; `embarch-dev-bench` has no release workflow beyond it (`embarch-release-signing-proposal.md`, "Bench firmware").

## Usage

`scripts/bench-firmware-list.py [--version V] [--commit C] [--out FILE] <release> <image>...`, each `<image>` being `app:board:path` (`path@base` for a raw bin, base decimal or `0x` hex).

- **Where the metadata comes from.** App and board are named on the command line, per image. Version defaults to `<release>` and commit to `git rev-parse HEAD` of this repo, both being the release's; `--version` and `--commit` override them once for every image.
- **Identity and segments** are `embarch-study-designer`'s (`interfaces/hil-image.md`): the script runs the crate's `image_segments` example through `cargo` in the sibling `../embarch-study-designer` (`--study-designer` overrides). The segment reduction is not reimplemented here.
- **Output** is `release/bench-firmware.json` at the repo root (`--out` overrides), the `BenchFirmwareList` shape, schema 1. Entries are sorted by `(app, board)`; two images for one app and board is an error. Exit 0 written, 2 error.
- **When it is written, and what ships.** Once per release, from the built images, and the list is committed with the release it names; the person flashes exactly those images. `release/characterisation/<board>.json` beside it belongs to the characterisation (`hil-characterisation.md`), not to this script.
