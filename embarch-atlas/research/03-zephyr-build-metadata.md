# What a Zephyr build already computes

**Status:** draft, 2026-09-22.

Inventory of what is sitting in `build/` after a `west build`, and what of the
scoped capability set it answers for free. Verified end-to-end against a real
client firmware workspace — Zephyr **v4.3.0**, an nRF54L15 product board, one
snippet — rather than read from documentation.

**This note is generalized.** Examples below keep the real *shape* of each
artifact with the client's node paths, part names, pins and file names replaced
by placeholders (`<sensor>`, `<board>`, `<driver>.c`), because this repo is
public. The full-fidelity version is machine-local (see
[README.md](README.md), "Client data").

## The finding

**For a single built configuration, "build-config reality" and "hardware binding"
are roughly 85% free.** Everything needed is already on disk in machine-readable
form. The expensive parts are not extraction — they are **the cross-domain join**
and **the combinatorics of which build you indexed**.

This is the strongest argument found for this sub-project being small rather than
large, and it inverts the obvious plan: the work is not analysis, it is
correlation and identity.

## The inventory

Build dir total 102 MB, of which the *useful* subset is ~7 MB.

| Artifact | Size | Answers |
|---|---|---|
| `build_info.yml` | 4.3 KB | **The best single file in the tree.** Board + revision + qualifiers, every DTS/overlay in merge order, every Kconfig fragment in merge order, binding dirs, toolchain, Zephyr version, **the exact `west build` command line**, and the SoC vendor's SVD path |
| `zephyr/.config` | 95 KB | Final Kconfig — 1,251 symbols set, 1,238 explicitly not set |
| `zephyr/include/generated/zephyr/autoconf.h` | 49 KB | The same 1,251 as `#define`s — what the compiler actually saw |
| **`zephyr/.config-trace.json`** | 366 KB | **Provenance for all 2,489 symbols** — see below |
| `zephyr/edt.pickle` | 1.3 MB | Fully-resolved `edtlib.EDT`, 161 nodes, **loads in 47 ms** |
| `zephyr/zephyr.dts` | 101 KB | Final merged devicetree |
| `zephyr/zephyr.dts.d` | 4.1 KB | Every `.dts`/`.dtsi`/`.h` that fed the DT — a cache-invalidation key |
| `zephyr/include/generated/zephyr/devicetree_generated.h` | 1.5 MB | Macro form plus a node-path → dep-ordinal index |
| `compile_commands.json` | 3.4 MB | **490 entries = exactly the TUs compiled**, each with `-imacros …/autoconf.h` and the full `-I` set |
| `zephyr/zephyr.elf` / `.map` | 13 MB / 2.3 MB | Ground truth for what survived the linker |
| `zephyr/kconfig/sources.txt` | 4,241 lines | Every Kconfig file parsed — the second invalidation key |
| `zephyr_modules.txt` | 1.1 KB | Module name → path → CMake dir |
| `zephyr/snippets_generated.cmake` | 7.3 KB | **Every discoverable snippet** with paths — the snippet axis of the config space, enumerated free |
| `zephyr/runners.yaml` | 971 B | Flash/debug runners, device name, tool paths |

**Absent**: no `.cmake/api/` (Zephyr does not request the CMake file-API by
default — a query file would have to be written before configure), and no
`domains.yaml` (the measured build was not a sysbuild build).

## Build-config reality: solved, and better than expected

### `.config-trace.json` answers "what selected `CONFIG_X`"

**The find of the investigation.** Zephyr v4.3.0 ships value-origin tracing,
generated **unconditionally on every build** by `scripts/kconfig/kconfig.py` — not
gated on a target or a CONFIG.

Format: a list of 6-tuples `(name, visibility, type, value, kind, location)`.
Measured distribution over 2,489 entries:

| `kind` | count | `location` |
|---|---:|---|
| `unset` | 1,233 | `null` |
| `default` | 832 | `[abs_path, lineno]` — the Kconfig file with the default |
| `select` | 231 | `["<selecting expression>"]` |
| `assign` | 181 | `[abs_path, lineno]` — **the exact `.conf`/`_defconfig` line** |
| `imply` | 12 | as `select` |

The shape of real entries, with client paths replaced:

```
["CONFIG_SPI",     "y","bool","y","select", ["SPI_NOR && DT_HAS_JEDEC_SPI_NOR_ENABLED && FLASH"]]
["CONFIG_SPI_NOR", "y","bool","y","assign", [".../<board>_defconfig", <line>]]
["CONFIG_LOG",     "y","bool","y","assign", [".../<app>/prj.conf", <line>]]
```

So `CONFIG_SPI=y` because `SPI_NOR` selected it, and `SPI_NOR=y` because a named
line of the board defconfig assigned it — **a two-hop lookup in one JSON file.**

**Atlas should not implement Kconfig provenance.** Two caveats:

- **Version gate.** `traceconfig` landed upstream 2025-09-19 and first shipped in
  **v4.3.0**. On Zephyr ≤4.2 / NCS ≤3.x the file does not exist and the fallback
  is kconfiglib.
- **Coverage.** The 2,489 entries are what appears in `.config`. A symbol whose
  menu node was never reached is absent, so "is `CONFIG_X` a thing at all, and why
  can't I enable it" still needs kconfiglib.

`kconfiglib` is vendored in every Zephyr tree and is scriptable enough for the
rest: `kconf.syms['SPI']` gives `.str_value`, `.visibility`, `.direct_dep`,
`.rev_dep` (the OR of everything that selects it) and node filename/linenr.
`menuconfig.py` and `guiconfig.py` are UIs over it, not APIs.

### Which files compiled, and which branches are live
`compile_commands.json` holds **exactly the 490 TUs that compiled** — a file absent
from it was not built, full stop, no inference. And because every entry carries
`-imacros …/autoconf.h` plus the full include path, **libclang and clangd resolve
inactive preprocessor regions correctly with zero analysis work.**

That is the single-configuration case, and it is solved. The all-configurations
case (kmax, TypeChef, SuperC) is a research project and effectively Linux-only —
skip it.

## Hardware binding: solved, and the DT↔ELF join is the good part

### edtlib on `edt.pickle` answers the hardware question completely

`pickle.load()` with `sys.path` pointed at
`zephyr/scripts/dts/python-devicetree/src` yields a live `edtlib.EDT` in **47 ms,
161 nodes**. Node API: `path, compats, matching_compat, binding_path, status,
labels, aliases, regs, interrupts, props, parent, children, bus_node, on_buses,
pinctrls, spi_cs_gpio, depends_on, required_by, dep_ordinal, flash_controller,
gpio_hogs, filename, lineno`. EDT API: `compat2okay, compat2nodes, compat2vendor,
label2node, chosen_nodes, dep_ord2node, scc_order`.

**"Which SPI instance drives this sensor" is answered exactly, in one query.** The
shape of the answer, placeholders for client specifics:

```
/soc/peripheral@50000000/spi@<addr>/<sensor>@1
  matching_compat  : <vendor>,<part>
  binding          : dts/bindings/<vendor>,<part>.yaml   (out-of-tree binding)
  on_buses         : ['spi']
  bus_node         : /soc/peripheral@50000000/spi@<addr>  (nordic,nrf-spim)
  bus reg          : <base>, 4 KiB   IRQ <n> prio <p>
  CS               : cs-gpios[1] -> gpio@<port> pin <n>
  spi-max-frequency: <hz>
  int-gpios        : gpio@<port> pin <n>, flags <f>
  power-domains    : /<power-enable node>
  pinctrl-0        : /pin-controller/<spim>_default
  dep_ordinal      : <N>
```

It also correctly shows a second part sharing the same SPI bus on another chip
select — a fact easy to get wrong reading DTS text.

**The one real gap is pin numbers.** `pinctrls[].conf_nodes[]…props['psels']`
gives raw encoded ints. Decoding needs the vendor macro at
`zephyr/include/zephyr/dt-bindings/pinctrl/nrf-pinctrl.h:274` —
`NRF_PSEL(fun, port, pin) = (fun<<24)|(port<<5)|pin` — plus the `NRF_FUN_*`
table, which turns each int into `Pport.pin (SPIM_SCK)` and so on. Atlas needs a
small per-vendor psel decoder, roughly 100 lines for Nordic. Everything else
about pins comes straight out of edtlib.

### The DT → driver instance → ELF join, and why `nm` is the key

**Source side, no build needed**: an out-of-tree driver carries
`#define DT_DRV_COMPAT <vendor>_<part>` and `DT_INST_FOREACH_STATUS_OKAY(...)`
wrapping `DEVICE_DT_INST_DEFINE(...)`. A plain grep for `DT_DRV_COMPAT` maps
compatible → implementing source file for **2,027 files in `zephyr/drivers/`
alone** — a static map, free, no build.

**Binary side, needs the build**: `DEVICE_DT_INST_DEFINE` emits a symbol named
`__device_dts_ord_<dep_ordinal>`, and `DEVICE_DT_GET(...)` in app code expands to
`&__device_dts_ord_<N>`. **So the linker symbol *is* the edge.** The shape of the
`nm` output:

```
$ nm -A --defined-only <all .a in build/> | grep __device_dts_ord_<N>
  .../lib…__<driver>.a : <driver>.c.obj : R __device_dts_ord_<N>

$ nm -A -u <all .a> | grep __device_dts_ord_<N>
  libzephyr.a : <app_module_a>.c.obj  U __device_dts_ord_<N>
  libzephyr.a : <app_module_b>.c.obj  U __device_dts_ord_<N>
  libzephyr.a : <selftest>.c.obj      U __device_dts_ord_<N>
```

One `nm` pass over the build's archives gives, **in 0.07 s**, a bidirectional
index: *defined* → the driver `.c` that instantiated the node (68 symbol families,
28 actual devices in the measured build); *undefined* → **every translation unit
holding a `struct device *` to that node.**

That resolves "which `struct device *` in app code traces back to which DTS node
and which compatible" **exactly — no source parsing, no macro heuristics, no false
positives.** Chained: app TU → ordinal → DT node → compatible → bus node and its
base address → decoded pins.

### What else the linker tells you
`ninja -C build initlevels` (`scripts/build/check_init_priorities.py`) runs in
**0.75 s** with no rebuild and prints the full boot order **with the init function
name per device** (`__init___device_dts_ord_<N>: <driver>_init(...)`, grouped by
`PRE_KERNEL_1` / `POST_KERNEL` / …).

`scripts/build/elf_parser.py` (`ZephyrElf`) is the reusable library behind that
and behind `gen_device_deps.py`, building a device object graph with
`devs_depends_on`/`devs_supports` and PM power-domain flags. **Caveat found in
practice**: its `edt_node`/`ordinal` linking needs the `__devicedeps_dts_ord_*`
handle arrays, which exist only with `CONFIG_DEVICE_DEPS=y`. The measured build
had it unset, so `ZephyrElf` parsed 28 devices and left `edt_node = None` on all
of them. **Use `nm` plus `edt.pickle` directly** — simpler, faster, and
independent of that CONFIG.

### In-tree helpers worth knowing
- **`scripts/dts/dtdoctor_analyzer.py`** (new in 4.3) — takes `--edt-pickle` and
  `--symbol __device_dts_ord_<N>` and root-causes it ("node disabled" / "driver
  Kconfig off"). **It already loads both edtlib and kconfiglib and joins them.
  Read this before writing atlas's explainer — it is a working prototype of
  exactly the join atlas needs.**
- `gen_device_deps.py`, `gen_isr_tables.py`, `gen_kobject_list.py`,
  `gen_symtab.py` — all take `--edt-pickle` and/or the ELF.
- `list_boards.py`, `list_hardware.py`, `list_shields.py`, `snippets.py` —
  enumerate the configuration space **without building**.
- `west build -t ram_report | rom_report` → `--json`, attributing every symbol to
  a source file with size and address. **Measured 27.5 s** (DWARF/addr2line
  bound). `puncover`, `hardenconfig`, `traceconfig`, `usage`, `footprint` are all
  present as phony ninja targets.
- `west manifest --resolve` — the pins, offline, instant.

## Cost: what "atlas requires a build" actually means

### Build time — cheap, and not a blocker
Two pristine builds of the measured app, on a 14-core machine with ccache:

| Run | Wall | CPU |
|---|---:|---|
| 1st (partly warm ccache) | **28.0 s** | 2m51s user |
| 2nd (warm ccache) | **30.2 s** | 3m30s user |

ccache barely moves it — **~30 s is the honest number** for a full pristine build
of a ~100 K-line app on Zephyr; an incremental rebuild after a source edit is
seconds. If atlas needs only config and DT and not the ELF, stopping after CMake
configure is a few seconds.

### Reproducibility — good enough, with two known wrinkles
Same command into two directories, compared:

| Artifact | Result | Cause |
|---|---|---|
| `zephyr/.config` | **byte-identical** | — |
| `zephyr/zephyr.dts` | **byte-identical** | — |
| `devicetree_generated.h` | 4 diff lines | a comment embedding the absolute path to `zephyr.dts.pre` |
| `edt.pickle` | differs | embeds absolute `dts_path` and per-node `filename` |
| `zephyr.bin` | **exactly 2 bytes** | a build counter/timestamp |

**So atlas can safely content-hash `.config` + `zephyr.dts` as its cache key**,
and must treat `edt.pickle` as path-tainted. Against a two-week-old checked-in
build, `zephyr.dts` was identical and `.config` differed only by symbols added to
the app since — config drift is real and visible.

### Combinatorics — the actual cost
The measured repo alone has several boards; one board has **three revisions**
declared `exact: true`, and **its optical sensor front-end is a different part
from one revision to the next — different DT, different drivers, different ELF**;
several apps; and **~50 discoverable snippets**, about a dozen app-local and
clearly meant to be combined, plus stacked `.overlay` files.

Naïvely that is hundreds of configurations. **In practice the team's own working
set is 4–7 live configs** — the repo already keeps that many named build
directories, some already named `<board>-<variant>-<rev>-<app>`.

**So: atlas should index *named configurations*, not "the codebase."** One index
per build dir, keyed on `build_info.yml` plus a hash of `.config`+`zephyr.dts`. At
~30 s per build and ~7 MB of useful artifacts per config, **indexing 6 configs is 3
minutes and 45 MB.** And **every answer atlas returns must be stamped with which
configuration it is true for** — two revisions of the same board genuinely
disagree about what one of its sensors *is*.

**Hard constraint**: anything needing the ELF (device instantiation, init order,
"did this link in") needs a **successful link**. `.config`, `edt.pickle` and
`compile_commands.json` survive a failed *compile* as long as CMake configure
succeeded — a useful degraded mode worth designing for.

**Not covered here: sysbuild.** Under sysbuild each image gets its own
`build/<image>/zephyr/` with its own `.config`, `edt.pickle` and ELF, plus a
top-level `domains.yaml`. **Atlas's model must be N configs per build dir, not
one.**

## Zephyr-adjacent prior art

- **No MCP server targets Zephyr/Kconfig/devicetree.** Two independent surveys say
  so explicitly (https://github.com/beriberikix/awesome-mcp-hardware,
  https://veecle.ai/blog/hardware-mcp-servers-reviewed). The two Zephyr-named ones
  are 0★ and 6★ and index nothing.
- **Nordic nRF Connect for VS Code**: the core is closed, but both language
  servers are MIT and open — `vscode-nrf-devicetree` (its own TypeScript DTS
  parser, **not** edtlib; has an `api.d.ts`) and `vscode-nrf-kconfig` (Python LS
  over kconfiglib, one Kconfig context per build). **No CLI on either — LSP only,
  not consumable headless.** Nordic also shipped a local MCP server inside the
  extension in 2026, closed, with an undocumented tool list.
- **DTSh** (Apache-2.0, 74★) — shell-like devicetree browser over `zephyr.dts`,
  once proposed for in-tree. Interactive-first; a reference for query semantics,
  not a library.
- **`nrf-regtool`** — parses devicetree with Zephyr's own bindings plus CMSIS-SVD
  to emit register blobs. Precedent for "DT → structured hardware facts" offline.

## What this leaves as genuinely new work

Free, already in `build/`: Kconfig values **and provenance**; the full resolved
devicetree with bindings, buses, regs, interrupts, GPIOs and power domains; which
files compiled; which `#ifdef` branches are live; which devices instantiated,
their init functions and boot order; which TUs hold a `struct device *` to which
node; full build provenance; and the configuration space itself.

The remaining ~15%:

1. **The join.** `Kconfig symbol → driver → compatible → DT node → dep ordinal →
   ELF symbol → app call sites → vendor part.` Every artifact above holds one
   link; **nothing joins them.** This is the differentiator.
2. **Vendor psel decoding** — raw pinctrl ints → `Pport.pin (function)`. One table
   per SoC family.
3. **Configuration identity and drift** — naming, hashing, invalidating
   (`zephyr.dts.d` and `kconfig/sources.txt` are the dependency sets), and
   **refusing to answer without saying which config the answer is for.**
4. **Degraded mode** when configure succeeded but the link failed.
5. **Compatible → datasheet part.** `compat2vendor` gives the vendor string and
   the binding YAML a description, but the actual part and datasheet is a
   **human-supplied mapping** — explicit engineer-supplied knowledge, never
   inferred from source, per this suite's existing standing rule.

**The rule worth writing into the spec: atlas parses no DTS and no Kconfig.** It
reads `edt.pickle` and `.config-trace.json`, shells `nm`, and spends all its
effort on the join and on configuration identity.

## Sources

Zephyr docs: devicetree build outputs
(https://docs.zephyrproject.org/latest/build/dts/intro-input-output.html),
sysbuild (https://docs.zephyrproject.org/latest/build/sysbuild/index.html),
optimization tools
(https://docs.zephyrproject.org/latest/develop/optimizations/tools.html),
dtdoctor (https://docs.zephyrproject.org/latest/develop/sca/dtdoctor.html).
Verified locally against upstream `scripts/kconfig/kconfig.py` (lines 140–144,
300–335), `scripts/dts/dtdoctor_analyzer.py`, `scripts/build/elf_parser.py`,
`scripts/build/check_init_priorities.py`, and
`include/zephyr/dt-bindings/pinctrl/nrf-pinctrl.h:274`.
