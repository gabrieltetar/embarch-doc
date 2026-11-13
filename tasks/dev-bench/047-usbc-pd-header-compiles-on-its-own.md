# 047 — The carried R3.2 patch's `usbc_pd.h` compiles as a file's first include

**State:** claimed by agent/dev-bench/047-usbc-pd-header-compiles-on-its-own, 2026-11-13 13:51 (toolchain unit, run by the leg itself)
**Source:** EMB-147, found by `tasks/dev-bench/037` splitting pd-bench's pure logic into `pd_logic.c` and testing it on `native_sim`, 2026-11-10
**Issue:** EMB-147
**Scope:** dev-bench
**Hardware:** toolchain — needs pd-bench's own west workspace, which no worktree carries
**Owner:** no

## What

`workspaces/pd-bench/manifest/zephyr/patches/zephyr/local/usbc-pd-r32.patch`
adds structs ending in `} __packed;` (and one `} __packed manufacturer_info;`)
to `include/zephyr/drivers/usb_c/usbc_pd.h`, whose only include is
`<zephyr/types.h>`. A translation unit that includes `usbc_pd.h` before anything
that pulls in `<zephyr/toolchain.h>` fails on `native_sim`:
`conflicting types for '__packed'; have 'struct pd_skedb'`, then the same for
`pd_scedb`, `pd_midb` and `pd_bcdb`, then `expected ':', ... before
'manufacturer_info'`. Measured 2026-11-10 building `pd-bench/tests/logic`
against Zephyr v4.4.2 plus the six carried patches. The ARM builds of both
shields never hit it, because `main.c` includes other Zephyr headers first.

Fix:

- The patch's `usbc_pd.h` hunk adds `#include <zephyr/toolchain.h>` beside
  `<zephyr/types.h>`, and that entry's `sha256sum` in
  `workspaces/pd-bench/manifest/zephyr/patches.yml` matches the new file.
- `pd-bench/src/pd_logic.h` drops its workaround include of
  `<zephyr/toolchain.h>` and the comment explaining it.

**Only this repo's copy.** The same patch is carried in the workspace it was
copied from, which is not a suite repo; whether a fix reaches that copy is the
owner's open question in `embarch-dev-bench/open.md` (which copy of a carried
patch leads). Do not write outside `embarch-dev-bench`, and do not answer that
question here.

**Toolchain facts.** The fleet's west is
`/home/gabriel/Github/embarch/.west-venv/bin/west`. The workspace is
`workspaces/pd-bench/` in the `embarch-dev-bench` checkout, and on 2026-11-12 it
held only `manifest/` and `pd-bench/`: a first `west init -l manifest && west
update` downloads Zephyr v4.4.2 and its modules, several GB, and is the slow
step. The commands `tasks/dev-bench/037` ran are in its `decisions/pd-bench.md`
decision 59 and the workspace's README.

## Why now

It surfaces only in a new file or a host test, so the next person to add one
meets a compiler error that points at the wrong struct.

## Done when

- [ ] `usbc-pd-r32.patch` adds `#include <zephyr/toolchain.h>` to `usbc_pd.h`,
      and its `patches.yml` `sha256sum` matches the file.
- [ ] A fresh `west init -l manifest && west update && west patch apply` in
      `workspaces/pd-bench/` reports 6 patches applied, and both shields still
      build with no warnings.
- [ ] `pd_logic.h` no longer includes `<zephyr/toolchain.h>`, and
      `pd-bench/tests/logic` still builds and passes on `native_sim`.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
