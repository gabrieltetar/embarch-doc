# embarch-umbrella decisions: What `doctor` checks

**Status:** active, 2026-09-05.

The checks, and why several of them distinguish states that look the same. Which are built and which are not is [../spec.md](../spec.md)'s table, not repeated per entry here. What a check *reports* — the `--json` contract, `code`, `path` — is [reporting.md](reporting.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Two checks are their own groups: what 11 and 15 compare is [schema-skew.md](schema-skew.md), and check 10's MCP registration is [mcp.md](mcp.md).

### 18 — Check 5 distinguishes "no probe attached" from "a probe is attached but this user cannot open it"

Reporting zero probes as "warn — a probe can legitimately be unplugged" is true but **actively misleading for the most common Linux first-run failure:** a probe that *is* attached but inaccessible because no udev rule grants this user permission to open it, which enumeration silently under-reports. So on Linux only — **macOS and Windows have no such permission model** — `doctor` reads the USB device tree for a known debug-probe vendor ID the enumeration missed. **A hit means "attached but not permitted", a distinct fail rather than a warn**, with the udev-rules fix line; a miss on both stays the existing warn.

**Built 2026-09-05.** The tree is `/sys/bus/usb/devices/*/idVendor`, read with `std::fs` and no new dependency — and **sysfs attributes are world-readable while `/dev/bus/usb/...` is the node the udev rule grants**, which is exactly why this sees a probe the enumeration could not open. Codes, since decision 37's rule applies the moment a second state shares a status: fail `probe-not-permitted`, pass `probes-present`, and **three warns, not two** — `no-probe-found` (bus read, nothing on it), `no-probe-unchecked` (nobody could look: not Linux, or Core enumerates elsewhere), `no-status` (check 4 got no authenticated status, so no count was ever obtained).

**"After zero probes are reported" describes the *verdict*, not the syscall.** The scan runs once in the driver before any check consults a count, and `check_probes` takes the finished result — which is what keeps the check pure and `cargo test` off a real `/sys`. The count gates only whether the scan can change the answer.

**One condition the decision did not name, and it is not optional: Core must be enumerating on *this* machine.** Check 5 reads its count off Core's `/status`, so on `wsl-host` or `remote` the count is about one computer and this host's bus about another. Scanning anyway is check 14's mistake with a different peripheral (decision 31): a confident verdict about the wrong machine. So the scan runs only on Linux **and** class `local`; every other case keeps the old warn and says which reason applies.

**`0403` (FTDI) is deliberately not a probe vendor ID**, though several JTAG adapters use it — so does every third USB-serial cable on this bench, the outpost link and dev-bench console among them, and an ID that means "probe" only sometimes would fail this check on machines with no probe at all, which is worse than the warn it replaces. The list is SEGGER, CMSIS-DAP, ST-Link, LPC-Link2, EDBG, Raspberry Pi Debug Probe, Black Magic, XDS110, ULINK.

**Never exercised against a real permission-denied probe** — that needs a Linux box with a probe attached and its udev rules removed. Until then the fail branch is unit-tested against a synthetic sysfs tree only ([../open.md](../open.md)).

### 19 — A stale-dev-bench-firmware check

It compares the bench's reported firmware version, over a handshake-only endpoint Core added for exactly this, against `git describe` run in whichever local dev-bench checkout is configured — a new machine-level state field, settable at setup or overridable per call. A mismatch fails with a fix line naming the reflash step, **whose exact command depends on which board, unlike this decision's original text assumed.**

**The configured path must name a path native to wherever `doctor` itself runs**, not a cross-filesystem view of one: Windows against a WSL2 checkout over a UNC path **spuriously reports the checkout as always-dirty, because Windows' git cannot read that repo's symlinks over that path.**

### 22 — Bind address versus topology, built 2026-09-05; firewall state and disk space, retired 2026-09-05

**(a) Bind address versus topology — check 17, built 2026-09-05.** A Core that bound loopback under the new default **without `setup` having widened it** is exactly the "reachable from *this* interface but not the one WSL2 can actually use" failure **that default made possible for the first time.** `embarch-topology`'s `recommended_bind_address` is the yardstick — the function `setup` already calls and bakes into the `install` invocation — and what was missing was only the check that notices when it hadn't been.

**The independent half is the class `setup` recorded**, not the class check 3 resolved. Check 3's class *is* derived from whichever candidate answered, so comparing the winner against it can only agree; with no recorded class the check warns `no-recorded-class` rather than passing vacuously.

**Two Fails on different evidence.** Reached at loopback while the recorded class needs `0.0.0.0` — `bind-too-narrow`. And **nothing reachable at all, with the Windows service's registration naming `--bind 127.0.0.1`** — `bound-narrow`, which is what "failing when they disagree **rather than reporting bare unreachability**" buys: check 3 sends someone to restart a service that is already running. The registration comes off the same `sc.exe qc` line `locate_core` and `deploy-core` already parse, read **only when nothing answered** — a Core that answered has proved its bind covers that route. A wide registration with nothing reachable is `bind-not-the-cause`, a useful negative rather than a duplicate red.

**Bound *wider* than needed warns and does not fail**, and the losing case is real: "disagreement fails" reads more cleanly, and a laptop needing only loopback that listens on every interface is exposure. It loses because **that machine works**, and a red `doctor` where nothing is broken is the failure this chain exists to avoid.

**The argument against building (a), which lost:** it duplicates check 3, since an unreachable Core already fails and a reachable one is by construction bound wide enough for the route that reached it. True, and it is why the check took this shape rather than the one this entry first described — the value is entirely in the **unreachable** case and in the cross-interface case where `doctor` runs somewhere the guest does not. **Never yet met a real narrow-bound Core** (the bench registers `--bind 0.0.0.0`), so both Fail branches are unit-tested against synthetic evidence only ([../open.md](../open.md)).

**(b) Firewall state (retired unbuilt 2026-09-05, see (a)).** It would have named a likely-active profile when a connectivity probe fails and Core cannot be ruled out as simply not running. Retired for the reason its own text named: **firewall state cannot always be introspected without elevation**, so here it would be a permanent warn — and decision 37's rule says a number a check could not obtain warns, never passes. A check that is always amber trains people to stop reading amber. Nor could it produce a fix line: naming a profile does not name a rule, and the real Windows first-day event is an interactive prompt at Core's first bind, already answered by the time `doctor` runs. **(a) now answers the same question with a cause rather than a suspicion**, which is what made the guess redundant rather than merely weak.

**(c) Disk space (retired unbuilt 2026-09-05, see check 16).** It would have warned below a generous threshold behind the build and results directories, a full disk otherwise reading as a mystifying compiler error. Retired on cost against a check that already exists: **`std` has no free-space API**, so it needs a new dependency or a per-platform shell-out (`df`, `GetDiskFreeSpaceExW`) in a crate whose Cargo.toml is explicit about what it refuses to link, and the payoff is a guessed threshold. **Check 16 already measures what grows here** — `study_results/` at 809 MiB across 50 entries — making growth the signal and decision 26's `--prune` the fix. The losing argument: free space catches a disk filled by something that is not EmbArch, which 16 structurally cannot see. Real, but that is machine health wearing an EmbArch badge, and 16's numbers land in the same report.

### 31 — Check 14: which program Core would flash each chip family with

Core refuses to flash an nRF54L part with probe-rs, because that family stores code in RRAM and probe-rs does not model it. **The vendor tool that replaces it cannot be bundled — licensing, not effort — so it might simply be absent.** Discovering that at the moment someone flashes is the worst available time, **and discovering it in `doctor` is what `doctor` is for.**

**It shells out to the located `embarch-core` rather than reasoning here**, which on this bench means running a Windows binary from WSL2. **That is the point rather than an accident: the tool has to exist on the machine running *Core*, not the machine running `doctor`, and only Core's own binary can answer about the right machine.** A second copy of the search logic here would be a mirror that drifts.

**Failure signature it found immediately, and the best argument for the check existing.** Run through WSL2 interop, the Windows Core reported a tool at a **Linux path — an ELF a Windows process cannot execute** — because interop merges WSL's `PATH` into the Windows process and the existence test resolves it through the filesystem redirector. **The *service*, whose environment is the system `PATH`, resolves a different tool.** So the check was reporting a backend the thing it checks would never choose, **which is worse than no check.** Fixed in Core.

**An older Core with no such subcommand is a Warn naming what it predates, not a Fail** — a real and recoverable state during a staged rollout, and the deployment procedure already assumes Core and the tooling around it move separately.

**Amended by [decision 38](topology.md), which is what made this check run on `wsl-host` at all.** Its skip arm said `see check 1` and pointed at a check that was itself wrong there; each class now names what is missing. And the exe it invokes is the right file but runs under the WSL user's environment, not the service account's — a narrower form of the failure above, and open.
