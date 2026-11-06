# 034 — A named build directory picks its sysbuild image the way `atlas build` does

**State:** claimed by agent/atlas/034-named-build-dir-picks-the-image-the-atlas-was-built-for, 2026-11-06 13:20
**Source:** a reviewer's finding on `atlas/027`, filed to Fleet Ready
**Issue:** EMB-77
**Scope:** atlas
**Hardware:** none — the image choice is a function of a build tree's layout and the atlas stamp, testable on a synthetic tree without running west.
**Owner:** no

## What

`atlas build` now picks the image of a multi-image sysbuild through `kconfig.image_dir(bdir, marker, app)`: `domains.yaml`'s `default:` first, then the target's application directory name, and an error naming every `zephyr/edt.pickle` it found when neither picks one (`atlas/027`). A build directory the caller *names* — `config --build`, `dt_node` — goes through `buildq.named()`, which still calls `KC.zephyr_dir(p)` with no `app`, so it gets only the `domains.yaml` step. On an application-plus-MCUboot build tree whose `domains.yaml` is missing or names no default, `named()` raises where `atlas build` on the same tree picks the application image.

When this is done, `named()` resolves the image the same way `atlas build` does: it passes the app the atlas was built for, read from the atlas stamp as `extract_kconfig` in `src/embarch_atlas/build.py` already does, so a named build and the atlas's own build never describe two different images.

## Why now

`atlas/027` fixed the build path and left this one on the old rule, so the two paths into the same build tree can now disagree about which image they describe. It is the residual its reviewer named.

## Done when

- [ ] `named()` on a synthetic two-image build tree with no `domains.yaml` picks the image named by the atlas's app and does not raise.
- [ ] A named single-image build resolves as before.
- [ ] When no image can be chosen, the error names the pickles it found, as `atlas build`'s does.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `embarch-atlas` docs updated where they describe how a named build dir picks its image; `changelog.d/` fragment dropped.

## Notes for the worker

`atlas/028` (open) also edits `build.py` and `kconfig.py`. Only one `atlas` worker runs at a time, so you will not collide with it, but rebase onto `main` before you start if it has landed.
