# embarch-umbrella decisions: What `doctor` checks

**Status:** active, 2026-09-03.

The checks, and why several of them distinguish states that look the same. Which are built and which are not is [../spec.md](../spec.md)'s table, not repeated per entry here.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). What checks 11 and 15 compare is its own group, [schema-skew.md](schema-skew.md).

### 11 — `doctor` and `status` are split by cost, and both carry `--json`

`status` is one Core call — **cheap enough for a UI or a shell prompt to poll.** `doctor` is the full chain including filesystem checks and a build-command resolution, **far too heavy to poll.** The JSON shape on both is the contract a UI consumes, **and it exists in v1 specifically so the UI does not arrive and find only human-formatted text to scrape.**

### 18 — Check 5 distinguishes "no probe attached" from "a probe is attached but this user cannot open it"

Reporting zero probes as "warn — a probe can legitimately be unplugged" is true but **actively misleading for the most common Linux first-run failure:** a probe that *is* physically attached but inaccessible because no udev rule grants the current user permission to open it, which probe enumeration can silently under-report. So on Linux only — **macOS and Windows do not have this permission model** — after zero probes are reported, `doctor` checks the USB device tree for a known debug-probe vendor ID the enumeration missed. **A hit means "attached but not permitted", reported as a distinct fail rather than a warn**, with the udev-rules fix line; a genuine miss on both stays the existing warn.

**Built 2026-09-05.** The tree is `/sys/bus/usb/devices/*/idVendor`, read with `std::fs` and no new dependency — and **sysfs attributes are world-readable while `/dev/bus/usb/...` is the node the udev rule grants**, which is exactly why this can see a probe the enumeration could not open. The fail carries `code` `probe-not-permitted`; the two warns are `no-probe-found` (the bus was read and holds nothing) and `no-probe-unchecked` (nobody could look), because decision 37's rule applies here the moment a second state shares a status.

**One condition the decision did not name, and it is not optional: Core must be enumerating on *this* machine.** Check 5 reads its probe count off Core's `/status`, so on `wsl-host` or `remote` the count is about one computer and this host's USB bus is about another. Scanning anyway is check 14's mistake with a different peripheral (decision 31): a confident verdict about the wrong machine. So the scan runs only on Linux **and** class `local`; every other case keeps the old warn and says which reason applies.

**`0403` (FTDI) is deliberately not a probe vendor ID**, though several JTAG adapters use it. So does every third USB-serial cable on this bench — the outpost link and the dev-bench console among them — and a vendor ID that means "probe" only sometimes would fail this check on machines with no probe at all, which is worse than the warn it replaces. The list is SEGGER, CMSIS-DAP, ST-Link, LPC-Link2, EDBG, Raspberry Pi Debug Probe, Black Magic, XDS110, ULINK.

**Never exercised against a real permission-denied probe** — that needs a Linux box with a probe attached and its udev rules removed. Until then the fail branch is unit-tested against a synthetic sysfs tree only ([../open.md](../open.md)).

### 19 — A stale-dev-bench-firmware check

It compares the bench's reported firmware version, over a handshake-only endpoint Core added for exactly this, against `git describe` run in whichever local dev-bench checkout is configured — a new machine-level state field, settable at setup or overridable per call. A mismatch fails with a fix line naming the reflash step, **whose exact command depends on which board, unlike this decision's original text assumed.**

**The configured path must name a path native to wherever `doctor` itself runs**, not a cross-filesystem view of one: Windows against a WSL2 checkout over a UNC path **spuriously reports the checkout as always-dirty, because Windows' git cannot read that repo's symlinks over that path.**

### 22 — Three more first-day checks: bind address versus topology, firewall state, and disk space

**(a) Bind address versus topology.** A Core that bound loopback under the new default **without `setup` having widened it** is exactly the "reachable from *this* interface but not the one WSL2 can actually use" failure **that default made possible for the first time.** The check reports the address `/status` was reached at versus what the detected topology needs, **failing when they disagree rather than reporting bare unreachability.** For whoever implements it: **`embarch-topology` already exposes a recommended-bind-address function for exactly this comparison**, and `setup` **already calls** it and bakes it into the `install` invocation — so the address does get widened, and what is missing is only the check that would notice when it hadn't been.

**(b) Firewall state**, best-effort and informational, because **firewall state cannot always be introspected without elevation itself** — it names a likely-active profile when a connectivity probe fails and Core cannot be ruled out as simply not running.

**(c) Disk space** on the filesystem backing the build and results directories — warn below a generous threshold, **since a build failing from a full disk reads as a mystifying compiler error otherwise.**

**All three unbuilt:** `doctor` assembles exactly checks 1-16, and *firewall* and *disk* appear nowhere in the crate.

### 23 — Check 10 spawns `embarch-api` and confirms the MCP handshake completes, not just that a registration entry exists

**The failure mode the check exists to catch — registered but broken — is exactly the one it cannot detect:** adding a registration says nothing about whether the registered command actually starts and speaks the protocol. It would spawn the exact registered command with a short timeout and send a minimal initialize handshake, **reporting success, failure and timeout distinctly.** A hand-rolled one-shot JSON-RPC exchange is sufficient; a full client is not needed for one round trip.

**Built 2026-09-04.** Check 10 reads the command line out of `claude mcp get embarch`, spawns it with piped stdio, writes one `initialize` request and waits 10 s for a matching JSON-RPC response — no session, no client, no second request. The three outcomes carry distinct `code` values into `--json` (decision 37).

**Two states the decision did not name, and both are warns rather than either verdict.** No `claude` on `PATH` at all was already a warn and stays one. New is a registration whose output this cannot read a command out of: **`claude mcp get`'s human output is a format nothing in this suite has ever seen for real** ([../open.md](../open.md)), so the parse is an assumption, and an assumption that guessed wrong must not be able to invent a verdict about the server. It says it could not read the entry, and names that as the reason.

**Timeout is Fail, not Warn, and stays its own code.** A server that takes longer than 10 s to say hello is a finding either way; the separate code is what makes a badly chosen budget visible as itself rather than as a mystery failure. The 10 s is assumed, not measured.

### 31 — Check 14: which program Core would flash each chip family with

Core refuses to flash an nRF54L part with probe-rs, because that family stores code in RRAM and probe-rs does not model it. **The vendor tool that replaces it cannot be bundled — licensing, not effort — so it might simply be absent.** Discovering that at the moment someone flashes is the worst available time, **and discovering it in `doctor` is what `doctor` is for.**

**It shells out to the located `embarch-core` rather than reasoning here**, which on this bench means running a Windows binary from WSL2. **That is the point rather than an accident: the tool has to exist on the machine running *Core*, not the machine running `doctor`, and only Core's own binary can answer about the right machine.** A second copy of the search logic here would be a mirror that drifts.

**Failure signature it found immediately, and the best argument for the check existing.** Run through WSL2 interop, the Windows Core reported a tool at a **Linux path — an ELF a Windows process cannot execute** — because interop merges WSL's `PATH` into the Windows process and the existence test resolves it through the filesystem redirector. **The *service*, whose environment is the system `PATH`, resolves a different tool.** So the check was reporting a backend the thing it checks would never choose, **which is worse than no check.** Fixed in Core.

**An older Core with no such subcommand is a Warn naming what it predates, not a Fail** — a real and recoverable state during a staged rollout, and the deployment procedure already assumes Core and the tooling around it move separately.

**Amended by [decision 38](topology.md), which is what made this check run on `wsl-host` at all.** Its skip arm said `see check 1` and pointed at a check that was itself wrong there; each class now names what is missing. And the exe it invokes is the right file but runs under the WSL user's environment, not the service account's — a narrower form of the failure above, and open.

### 37 — A check may carry a machine-readable `code`, because `status` cannot hold every state a check distinguishes

Decision 23 asks check 10 to report success, failure and timeout **distinctly**, and decision 11 makes `--json` the contract a UI consumes. Those two together do not fit in three statuses: registered-but-broken and registered-but-hanging are both Fail, and the only thing separating them was an English sentence in `detail`.

So `Check` grows an optional `code` — a short stable identifier, `null` for every check that has nothing to add. **Never derived from `detail`**, which is written for a human and is free to be rephrased; a consumer that had to match on it would break on a wording change. Check 10 is the only user today (`handshake-ok`, `handshake-failed`, `handshake-timeout`, `not-registered`, `no-cli`, `unreadable-entry`); checks 5 and 22 are the obvious next ones, since both exist to split states that share a status.

**Additive on the wire**: the key is always present, so nothing has to tell "absent" apart from "no code", and every existing consumer of `--json` keeps working.
