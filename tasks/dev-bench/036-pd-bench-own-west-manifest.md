# 036 — Give pd-bench its own west workspace that pins Zephyr v4.4.2 and carries its six USB-C patches

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — pd-bench builds only from a client's west workspace because it needs that workspace's patched USB-C stack (decision 48, "It builds outside `workspaces/`"); the owner decided 2026-10-20 that it gets its own manifest here, carrying the patches until they land upstream
**Scope:** dev-bench
**Hardware:** toolchain
**Owner:** no

## What

Add `workspaces/pd-bench/`, a west topdir laid out like the other three: a `manifest/` subdirectory and an app symlink. Its manifest pins Zephyr `v4.4.2` with only the modules pd-bench uses. It carries the Zephyr patches pd-bench needs as a `west patch` set at `manifest/zephyr/patches.yml` and `manifest/zephyr/patches/zephyr/{upstream,local}/`, where Zephyr's `west patch` looks by default. After this, pd-bench builds both shields from a clone of this repo alone.

**Six patches, in this order**, all written against v4.4.2:

1. **PDO enum bitfields** (backport, upstream PR 121386, commit 8a87e3bde92d). With short enums, `union pd_fixed_supply_pdo_sink` reads every field above `frs_required` one bit high. The stack decides DR_Swap support from that union's Dual-Role Data bit, so a sink bench never supports DR_Swap without this fix. Run time.
2. **STM32 UCPD fixes**: the shared IRQ, the prescaler shift and RX overrun. Not upstream; the prescaler part is fixed upstream another way in 9719cc9cbe4f (v4.5.0-rc1). Here the RX-overrun part matters at run time, and patch 5 does not apply without this one.
3. **VCONN `-ENOTSUP`.** In a source-capable build, ErrorRecovery never opened CC. Not upstream. Run time, DRP1M1 build only.
4. **The USB PD R3.2 stack patch.** It adds the DPM requests and callbacks pd-bench calls (`REQUEST_PE_GET_STATUS`, `_PR_SWAP`, `_SEND_SRC_CAPS`, `_SNK_REQUEST`, `usbc_set_policy_cb_set_status` and others) and the stack fixes its shell relies on. Not upstream. **Build time**, and it applies alone.
5. **UCPD Messages by DMA.** Byte-per-interrupt TX underruns sent zero bytes under a valid CRC. pd-bench's overlay already names the `dmas`. Not upstream. Run time; needs patch 2.
6. **UCPD late TXMSGDISC.** A collision left a Message without a result, and every later Message stayed queued until a Hard Reset. Not upstream. Run time; needs patch 5.

**Left out**, because pd-bench uses none of them: the two dead-battery backports (the Nucleo never boots from VBUS), the UDC shared-IRQ fix (pd-bench has no USB device stack), and the Discover Identity responder (pd-bench registers no identity callback).

The workspace is named for the app, not for a vendor family as decision 2 groups them, because its Zephyr is patched. Whether `app/` ever gets a vanilla STM32 workspace is a separate question.

## Why now

pd-bench is the PD partner for host-run studies (`embarch-host-study-proposal.md`, phase 1), and today nobody can build it outside the client workspace, the fleet included. The set above applies cleanly to a v4.4.2 export and builds both shields with no warnings (measured 2026-10-20 with the fleet's west venv).

## Done when

- [ ] `workspaces/pd-bench/manifest/west.yml` pins `zephyr` at `v4.4.2` from `zephyrproject-rtos`, with `west-commands: scripts/west-commands.yml` and `import: name-allowlist: [cmsis_6, hal_stm32]`. A header comment says why, in the voice of the other three manifests.
- [ ] `workspaces/pd-bench/pd-bench` is a symlink to `../../pd-bench`, as `app` is in the other workspaces.
- [ ] `manifest/zephyr/patches.yml` lists the six in the order above. Each entry has `path`, `sha256sum`, `module: zephyr`, `upstreamable`, `merge-status` and `apply-command: git apply`; the backport also has `merge-pr`, `merge-commit` and `merge-date`. Each `comments:` says what the patch fixes for pd-bench and when to drop it.
- [ ] **No client name lands.** Two of the source patches name the client's product once each, in commit-message prose: the R3.2 stack patch's Power Role Swap part and the DMA patch's "Seen with DMA on..." paragraph. Reword both before the first commit, then recompute their `sha256sum`s. Run `check-client-names.py --repo embarch-dev-bench` green before committing. This repo works on `main`, and the checker scans only the commit messages on a branch since its merge-base.
- [ ] From a fresh `west init -l manifest && west update && west patch apply` in `workspaces/pd-bench/`, both builds succeed with no warnings, and `CONFIG_USBC_TCPC_STM32_DMA=y` in both `.config`s:
  - `west build -b nucleo_g0b1re -d build/pd-bench pd-bench`
  - `west build -b nucleo_g0b1re -d build/pd-bench-drp pd-bench -- -DSHIELD=x_nucleo_drp1m1`

  Reference, measured 2026-10-20: SNK1M1 128,368 B flash and 19,720 B RAM; DRP1M1 147,860 B and 21,648 B.
- [ ] `pd-bench/README.md` "Build and flash" describes this workspace instead of "a west workspace that has them". It gives one `embarch-api` `[[projects]]` block per shield: `build_command` is the workspace's `west build ... -s pd-bench` (plus `-DSHIELD=x_nucleo_drp1m1` for the DRP1M1), `chip = "STM32G0B1VE"`, `flash_format = "hex"`, `serial_baud = 115200` and `probe_serial = "<ST-LINK serial>"`. It keeps the note that the ST-LINK mass-storage drive refuses this image (it reports 32 KB). The repo README lists the new workspace.
- [ ] The repo README's License section says the carried patches modify Apache-2.0 Zephyr sources and keep that license.
- [ ] Decision 50, in `decisions/pd-bench.md`, supersedes decision 48's "It builds outside `workspaces/`". It records:
  - the pin and why v4.4.2;
  - the six patches and the four left out;
  - the drop rule: a patch leaves when the pin moves to a release that contains it. The backport goes after 8a87e3bde92d, and the prescaler part of patch 2 goes after 9719cc9cbe4f.
- [ ] **Ask the owner, do not pick:** which copy of a patch leads when it changes (this repo's or the one it came from), and how a fix reaches the other copy. Until it is answered, it is an `open.md` item.
- [ ] Run where (measured 2026-10-20):
  - west: `/home/gabriel/Github/embarch/.west-venv/bin/west` (v1.5.0). The system CMake 3.28.3 is enough, because v4.4.2 asks for 3.20.
  - SDK: `/home/gabriel/zephyr-sdk-1.0.0` (arm-zephyr-eabi).
  - Directory: `/home/gabriel/Github/embarch/embarch-dev-bench/workspaces/pd-bench`, in the main checkout. A worktree carries no Zephyr.
  - The first `west update` fetches Zephyr, hal_stm32 and cmsis_6: allow 10 to 20 minutes.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped. `spec.md` §1 and §2 stop saying pd-bench is "built from a workspace with the patched USB-C stack". `open.md` gains "the USB-C patch set is carried, not upstream", with what closes it.

## Evidence

### pd-bench: the Zephyr patches it needs

Pin: Zephyr **v4.4.2**. The client manifest carries 10 patches on that pin; pd-bench needs **6**.

Method (2026-10-20): every pd-bench identifier was checked against `git grep v4.4.2`, then subsets were applied with `git apply` to a v4.4.2 export, and both shields were built against the 6-patch tree with the fleet's west venv, system CMake 3.28.3 and Zephyr SDK 1.0.0. Both builds had no warnings. SNK1M1: 128,368 B flash, 19,720 B RAM. DRP1M1: 147,860 B flash, 21,648 B RAM. `CONFIG_USBC_TCPC_STM32_DMA=y` in both. A twister build-only run of the two scenarios passed (2 of 2 built). It used a venv that has Zephyr's `requirements-run-test.txt`, because the fleet venv lacks `natsort`. Run-time claims come from the patch headers and pd-bench's own commit history. None was re-measured on hardware for this table.

Upstream status comes from each patch's header and its `patches.yml` entry only. Nothing was checked on the web.

#### Needed (apply in this order)

| # | Patch file (client manifest name) | What it fixes or adds | Needed at | Depends on | Upstream status |
|---|---|---|---|---|---|
| 1 | `upstream/0003-usbc-pdo-enum-bitfields.patch` | With arm-zephyr-eabi's short enums, the 2-bit `frs_required` in `union pd_fixed_supply_pdo_sink` straddles a byte. It moves up a bit, so every field above it reads one bit high. | **Run time.** Patch 4 decides DR_Swap support from the Dual-Role Data bit of the port's first sink PDO, which it reads through this union. `pd dr accept\|nosupport` toggles that bit. Without the fix the stack reads bit 26 instead of bit 25, so a sink bench never supports DR_Swap. | none | **Merged upstream**: PR 121386, commit 8a87e3bde92d (2026-10-08). Backport from main. Drop it when the pin moves past that commit. |
| 2 | `local/0001-ucpd-stm32-fixes.patch` | Three STM32 UCPD fixes. (1) The shared IRQ picked the port from the raw status, so a UCPD2 interrupt went unserviced. (2) The clock prescaler went in unshifted. (3) A Message whose byte was overrun (RXOVR) got a GoodCRC a byte short. | **Patch order**, plus part 3 at run time. Patch 5 does not apply without it. Part 3 drops an overrun Message without a GoodCRC. Part 1 has no effect here, because only UCPD1 is enabled. Part 2 has none either, because the Nucleo overlay sets `psc-ucpdclk = <1>`, whose shift is zero. | none | **Not upstream.** Part 2 is fixed upstream another way: commit 9719cc9cbe4f (v4.5.0-rc1) drops `LL_UCPD_Init()`. Remove that part when the pin moves past it. Parts 1 and 3 are still open on main, per the header. |
| 3 | `local/0002-tc-vconn-enotsup.patch` | The Type-C CC-open entry and the Attached.SRC exit accepted only `-ENOSYS` from `tcpc_set_vconn(false)`. The STM32 UCPD returns `-ENOTSUP` without a VCONN callback. | **Run time, DRP1M1 build.** In a source-capable build, ErrorRecovery never opened CC. pd-bench requests ErrorRecovery on a TCPP03 fault and on a failed source turn-on. The SNK1M1 build is sink-only and is not affected. | none | **Not upstream.** |
| 4 | `local/0003-usbc-pd-r32.patch` | 16 changes to the USB-C stack: Policy Engine and Protocol Layer fixes, DPM requests and notifications, Get_Status / Alert / PPS_Status / Battery_Status, Power Role Swap, R3.2 timing, BIST, and the review fixes. Parts 11, 12 and 16 also touch the STM32 UCPD driver. | **Build time.** pd-bench uses `REQUEST_PE_GET_STATUS`, `_GET_PPS_STATUS`, `_GET_BATTERY_STATUS`, `_PR_SWAP`, `_SEND_SRC_CAPS`, `_SNK_REQUEST`, `usbc_set_policy_cb_set_status`, `_set_pps_status`, `_set_battery_status`, `union pd_sdb` / `pd_ppssdb` / `pd_bsdo` and `PD_V_SAFE_5V_MAX_MV`. None of them is in v4.4.2. It is also needed at run time for everything the README's shell section promises (PR_Swap, Wait handling, the PPS keep-alive, DR_Swap from the DRD bit). | applies alone on v4.4.2 | **Not upstream.** "zephyrproject main has none of it". |
| 5 | `local/0004-ucpd-stm32-dma.patch` | Moves UCPD Messages by DMA (`CONFIG_USBC_TCPC_STM32_DMA`, which defaults to y when the node has `dmas`). One interrupt per byte underran the transmitter. On an STM32G0B1 some underrun Messages left with a zero byte under a valid CRC. Reception checks the DMA count against RXPAYSZ. | **Run time.** pd-bench's own overlay names the `dmas` (commit 5282206). The header records the bug seen on a NUCLEO-G0B1RE partner: a PPS APDO read as 12.8 V, and Messages with MessageID 0. It builds without the patch, because `dmas` is in `base.yaml`, but then the DMA is silently unused. | 2 | **Not upstream.** |
| 6 | `local/0006-ucpd-stm32-tx-discard.patch` | The UCPD raised TXMSGDISC late, after the GoodCRC for the partner's Message had started. The handler took it as the end of the GoodCRC, so our Message never got a result. Every later Message stayed queued until a Hard Reset. | **Run time.** Any collision on CC triggers it, for a sink or a DRP. | 5 | **Not upstream.** |

#### Carried by the client, not needed by pd-bench

| Patch file | What it is | Why pd-bench does without it | Upstream status |
|---|---|---|---|
| `upstream/0001-tcpc-dead-battery-enabled.patch` | Adds the TCPC operation `dead_battery_enabled`. | Needed only by the next patch. | Merged: PR 118403, commit 7d8601056815 (v4.5.0-rc1). |
| `upstream/0002-tc-init-dead-battery-unattached-snk.patch` | `tc_init()` goes to Unattached.SNK when the UCPD still applies the dead-battery Rd. | The Nucleo runs from the ST-LINK USB and never boots from VBUS. The board DT sets no `dead-battery`, so the operation would report false and nothing would change. | Merged: PR 118403, commit a55d18501f47 (v4.5.0-rc1). |
| `local/0005-udc-stm32-shared-irq.patch` | Keeps IRQ 8 (USB, UCPD1 and UCPD2 on the G0) enabled while the USB device is disabled. | pd-bench builds no USB device stack. Its console is USART2 through the ST-LINK. | Not upstream. |
| `local/0007-usbc-discover-identity.patch` | Adds a DPM callback that ACKs Discover Identity. | pd-bench registers no `get_identity` callback, and the header says "without the callback nothing changes". A bench that should answer Discover Identity would need this patch and a callback. | Not upstream. |

#### Before these go into a public repo

- **Two patch messages name the client's product.** The denylist check hits the R3.2 stack patch once (its Power Role Swap part, a sentence about a PPC) and the DMA patch once (its "Seen with DMA on..." paragraph). Both are prose in the commit message, not code. Reword both before committing them, then recompute each `sha256sum`.
- The `patches.yml` entries themselves scan clean.
- The patches modify Apache-2.0 Zephyr sources. The repo is MIT, so the README's License section has to say that the patches keep Zephyr's license.
