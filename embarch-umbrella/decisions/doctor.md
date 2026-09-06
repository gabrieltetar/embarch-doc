# embarch-umbrella decisions: What `doctor` checks

**Status:** active, 2026-09-06.

The checks, and why several of them distinguish states that look the same. Which are built and which are not is [../spec.md](../spec.md)'s table, not repeated per entry here. What a check *reports* — the `--json` contract, `code`, `path` — is [reporting.md](reporting.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Three checks are their own groups: what 11 and 15 compare is [schema-skew.md](schema-skew.md), check 10's MCP registration is [mcp.md](mcp.md), and check 17's bind address is [bind.md](bind.md).

### 18 — Check 5 distinguishes "no probe attached" from "a probe is attached but this user cannot open it"

Reporting zero probes as "warn — a probe can legitimately be unplugged" is true but **actively misleading for the most common Linux first-run failure:** a probe that *is* attached but unopenable because no udev rule grants this user permission, which enumeration silently under-reports. So on Linux only — **macOS and Windows have no such permission model** — `doctor` reads the USB device tree for a known debug-probe vendor ID the enumeration missed. **A hit means "attached but not permitted", a distinct fail rather than a warn**, with the udev-rules fix line; a miss on both stays the existing warn.

**Built 2026-09-05.** The tree is `/sys/bus/usb/devices/*/idVendor`, read with `std::fs` and no new dependency — and **sysfs attributes are world-readable while `/dev/bus/usb/...` is the node the udev rule grants**, which is exactly why this sees a probe the enumeration could not open. Codes, per decision 37: fail `probe-not-permitted`, pass `probes-present`, and **three warns, not two** — `no-probe-found` (bus read, nothing on it), `no-probe-unchecked` (nobody could look: not Linux, or Core enumerates elsewhere), `no-status` (check 4 obtained no count at all).

**"After zero probes are reported" describes the *verdict*, not the syscall:** the scan runs once in the driver and `check_probes` takes the finished result, which keeps the check pure and `cargo test` off a real `/sys`. The count gates only whether the scan can change the answer.

**One condition the decision did not name, and it is not optional: Core must be enumerating on *this* machine.** Check 5 reads its count off Core's `/status`, so on `wsl-host` or `remote` the count is about one computer and this host's bus another. Scanning anyway is check 14's mistake with a different peripheral (decision 31): a confident verdict about the wrong machine. The scan runs only on Linux **and** class `local`; every other case keeps the old warn and names the reason.

**`0403` (FTDI) is deliberately not a probe vendor ID**, though several JTAG adapters use it — so does every third USB-serial cable here — the outpost link and dev-bench console among them — and an ID meaning "probe" only sometimes would fail this check on machines with no probe at all, which is worse than the warn it replaces. The list is SEGGER, CMSIS-DAP, ST-Link, LPC-Link2, EDBG, Raspberry Pi Debug Probe, Black Magic, XDS110, ULINK.

**Never exercised against a real permission-denied probe** — that needs a Linux box with a probe attached and its udev rules removed. Until then the fail branch is unit-tested against a synthetic sysfs tree only ([../open.md](../open.md)).

### 19 — A stale-dev-bench-firmware check

It compares the bench's reported firmware version, over a handshake-only endpoint Core added for exactly this, against `git describe` in whichever local dev-bench checkout is configured — a machine-level state field, settable at setup or overridable per call. A mismatch fails with a fix line naming the reflash step, **whose exact command depends on which board, unlike this decision's original text assumed.**

**The configured path must name a path native to wherever `doctor` itself runs**, not a cross-filesystem view of one: Windows against a WSL2 checkout over a UNC path **spuriously reports the checkout as always-dirty, because Windows' git cannot read that repo's symlinks over that path.**

### 31 — Check 14: which program Core would flash each chip family with

Core refuses to flash an nRF54L part with probe-rs, because that family stores code in RRAM and probe-rs does not model it. **The vendor tool that replaces it cannot be bundled — licensing, not effort — so it might simply be absent.** Discovering that at the moment someone flashes is the worst available time, **and discovering it in `doctor` is what `doctor` is for.**

**It shells out to the located `embarch-core` rather than reasoning here**, which on this bench means running a Windows binary from WSL2. **That is the point rather than an accident: the tool has to exist on the machine running *Core*, not the machine running `doctor`, and only Core's own binary can answer about the right machine.** A second copy of the search logic here would be a mirror that drifts.

**Failure signature it found immediately, and the best argument for the check existing.** Run through WSL2 interop, the Windows Core reported a tool at a **Linux path — an ELF a Windows process cannot execute** — because interop merges WSL's `PATH` into the Windows process and the existence test resolves it through the filesystem redirector. **The *service*, whose environment is the system `PATH`, resolves a different tool.** So the check was reporting a backend the thing it checks would never choose, **which is worse than no check.** Fixed in Core.

**An older Core with no such subcommand is a Warn naming what it predates, not a Fail** — a real and recoverable state during a staged rollout, and the deployment procedure already assumes Core and the tooling around it move separately.

**Amended by [decision 38](topology.md), which is what made this check run on `wsl-host` at all.** Its skip arm said `see check 1` and pointed at a check that was itself wrong there; each class now names what is missing. And the exe it invokes is the right file but runs under the WSL user's environment, not the service account's — a narrower form of the failure above, and open.
