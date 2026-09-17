# embarch-umbrella decisions: What `doctor` checks

**Status:** active, 2026-09-06.

The checks, and why several of them distinguish states that look the same. Which are built and which are not is [the table](../interfaces/doctor-chain.md)'s job. What a check *reports* — the `--json` contract, `code`, `path` — is [reporting.md](reporting.md).

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/doctor-chain.md](../interfaces/doctor-chain.md). Four checks are their own groups: what 11 and 15 compare is [schema-skew.md](schema-skew.md), check 10's MCP registration is [mcp.md](mcp.md), check 17's bind address is [bind.md](bind.md), and check 13's dev-bench-firmware comparison is [dev-bench-firmware.md](dev-bench-firmware.md). How `embarch-api` itself is located — a resolution mechanism, not a check — is [locate-api.md](locate-api.md).

### 18 — Check 5 distinguishes "no probe attached" from "a probe is attached but this user cannot open it"

Reporting zero probes as "warn — a probe can legitimately be unplugged" is true but **actively misleading for the most common Linux first-run failure:** a probe that *is* attached but unopenable because no udev rule grants this user permission, which enumeration silently under-reports. So on Linux only — **macOS and Windows have no such permission model** — `doctor` reads the USB device tree for a known debug-probe vendor ID the enumeration missed. **A hit means "attached but not permitted", a distinct fail rather than a warn**, with the udev-rules fix line; a miss on both stays the existing warn.

**Built 2026-09-05.** The tree is `/sys/bus/usb/devices/*/idVendor`, read with `std::fs` and no new dependency — and **sysfs attributes are world-readable while `/dev/bus/usb/...` is the node the udev rule grants**, which is exactly why this sees a probe the enumeration could not open. Codes, per decision 37: fail `probe-not-permitted`, pass `probes-present`, and **three warns, not two** — `no-probe-found` (bus read, nothing on it), `no-probe-unchecked` (nobody could look: not Linux, or Core enumerates elsewhere), `no-status` (check 4 obtained no count at all).

**"After zero probes are reported" describes the *verdict*, not the syscall:** the scan runs once in the driver and `check_probes` takes the finished result, which keeps the check pure and `cargo test` off a real `/sys`. The count gates only whether the scan can change the answer.

**One condition the decision did not name, and it is not optional: Core must be enumerating on *this* machine.** Check 5 reads its count off Core's `/status`, so on `wsl-host` or `remote` the count is about one computer and this host's bus another. Scanning anyway is check 14's mistake with a different peripheral (decision 31): a confident verdict about the wrong machine. The scan runs only on Linux **and** class `local`; every other case keeps the old warn and names the reason. **Amended by [decision 53](#53--check-5s-usb-scan-also-gates-on-the-located-binary-not-winner_class-alone-under-wsl2): class `local` is not enough under WSL2**, where mirrored networking makes a Windows-hosted Core answer at loopback exactly like a guest-hosted one, so the gate also weighs the located binary.

**`0403` (FTDI) is deliberately not a probe vendor ID**, though several JTAG adapters use it — so does every third USB-serial cable here — the outpost link and dev-bench console among them — and an ID meaning "probe" only sometimes would fail this check on machines with no probe at all, which is worse than the warn it replaces. The list is SEGGER, CMSIS-DAP, ST-Link, LPC-Link2, EDBG, Raspberry Pi Debug Probe, Black Magic, XDS110, ULINK.

**Never exercised against a real permission-denied probe** — that needs a Linux box with a probe attached and its udev rules removed. Until then the fail branch is unit-tested against a synthetic sysfs tree only ([../open.md](../open.md)).

### 31 — Check 14: which program Core would flash each chip family with

Core refuses to flash an nRF54L part with probe-rs, because that family stores code in RRAM and probe-rs does not model it. **The vendor tool that replaces it cannot be bundled — licensing, not effort — so it might simply be absent.** Discovering that at the moment someone flashes is the worst available time, **and discovering it in `doctor` is what `doctor` is for.**

**It shells out to the located `embarch-core` rather than reasoning here**, which on this bench means running a Windows binary from WSL2. **That is the point rather than an accident: the tool has to exist on the machine running *Core*, not the machine running `doctor`, and only Core's own binary can answer about the right machine.** A second copy of the search logic here would be a mirror that drifts.

**Failure signature it found immediately, and the best argument for the check existing.** Run through WSL2 interop, the Windows Core reported a tool at a **Linux path — an ELF a Windows process cannot execute** — because interop merges WSL's `PATH` into the Windows process and the existence test resolves it through the filesystem redirector. **The *service*, whose environment is the system `PATH`, resolves a different tool.** So the check was reporting a backend the thing it checks would never choose, **which is worse than no check.** Fixed in Core.

**An older Core with no such subcommand is a Warn naming what it predates, not a Fail** — a real and recoverable state during a staged rollout, and the deployment procedure already assumes Core and the tooling around it move separately.

**Amended by [decision 38](topology.md), which is what made this check run on `wsl-host` at all.** Its skip arm said `see check 1` and pointed at a check that was itself wrong there; each class now names what is missing. And the exe it invokes is the right file but runs under the WSL user's environment, not the service account's — a narrower form of the failure above, and open.

**The three arms are one skip worded per class, not flashing verdicts — reachable only before that class's own `setup` finishes (task 032).** A set-up `wsl-host` box hits `flash-backend` instead (decision 38). Kept distinct: each names its own next step. [interfaces/doctor-chain.md](../interfaces/doctor-chain.md) marks an arm `measured` only once a run has hit it.

### 53 — Check 5's USB scan also gates on the located binary, not `winner_class` alone, under WSL2

Decision 18 gated the scan on `class == Local`, reasoning "Core must be enumerating on **this** machine." Under WSL2, that reasoning has a hole [decision 30](topology.md) already named for a different pair of checks: mirrored networking makes a Windows-hosted Core answer at loopback exactly like a guest-hosted one, so `winner_class == Local` alone does not say *where* Core is. Left as it was, check 5 would scan this Linux guest's own bus on Core's behalf and could report `no-probe-found` — a confident verdict about the wrong machine, the exact failure mode decision 18 exists to avoid, just with a different peripheral (decision 31's phrase for check 14's version of the same mistake).

**`core_belongs_to` (decision 38) is *not* a drop-in fix here.** It is a pure function of `(winner_class, host, under_wsl2)`, and under WSL2 with no explicit `--host` it always resolves to `WslHost`, regardless of `winner_class` — its callers (checks 1 and 14) only ever consult it in the arm where `locate_core` already found no local binary, so that blindness is harmless there by construction. Check 5 has no such precondition: gating the scan on `core_belongs_to`'s answer directly would silently disable it on *every* WSL2 machine, including one with a real, located, native-Linux `embarch-core` — a real topology, not a hypothetical one, once a probe reaches the guest via `usbipd`.

**The fix folds in the evidence `core_belongs_to`'s callers already have and it does not: the located binary's own `windows_exe_from_wsl2` flag.** `usb_scan_for` now scans when `winner_class == Local` **and** (not under WSL2, **or** a located `embarch-core` is a native Linux binary rather than a Windows exe reached through interop). No located binary at all reduces to the same "assume the Windows host" call `core_belongs_to` already makes, for the same reason: a guest-local Core that `setup` installed would already be on `PATH`.

**Unexercised, like the rest of this check's fail branch** ([open.md](../open.md)) — there is no mirrored-networking bench. Tested only against synthetic `Located` values.
