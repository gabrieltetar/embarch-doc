# embarch-umbrella decisions: What `doctor` checks

**Status:** active, 2026-09-03.

The checks, and why several of them distinguish states that look the same. Which are built and which are not is [../spec.md](../spec.md)'s table, not repeated per entry here.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 11 — `doctor` and `status` are split by cost, and both carry `--json`

`status` is one Core call — **cheap enough for a UI or a shell prompt to poll.** `doctor` is the full chain including filesystem checks and a build-command resolution, **far too heavy to poll.** The JSON shape on both is the contract a UI consumes, **and it exists in v1 specifically so the UI does not arrive and find only human-formatted text to scrape.**

### 18 — Check 5 distinguishes "no probe attached" from "a probe is attached but this user cannot open it"

Reporting zero probes as "warn — a probe can legitimately be unplugged" is true but **actively misleading for the most common Linux first-run failure:** a probe that *is* physically attached but inaccessible because no udev rule grants the current user permission to open it, which probe enumeration can silently under-report. So on Linux only — **macOS and Windows do not have this permission model** — after zero probes are reported, `doctor` checks the USB device tree for a known debug-probe vendor ID the enumeration missed. **A hit means "attached but not permitted", reported as a distinct fail rather than a warn**, with the udev-rules fix line; a genuine miss on both stays the existing warn.

**Unbuilt:** check 5 has no `Fail` branch at all, so the state this decision exists to separate is still reported as exactly the warn it calls misleading.

### 19 — A stale-dev-bench-firmware check

It compares the bench's reported firmware version, over a handshake-only endpoint Core added for exactly this, against `git describe` run in whichever local dev-bench checkout is configured — a new machine-level state field, settable at setup or overridable per call. A mismatch fails with a fix line naming the reflash step, **whose exact command depends on which board, unlike this decision's original text assumed.**

**The configured path must name a path native to wherever `doctor` itself runs**, not a cross-filesystem view of one: Windows against a WSL2 checkout over a UNC path **spuriously reports the checkout as always-dirty, because Windows' git cannot read that repo's symlinks over that path.**

### 22 — Three more first-day checks: bind address versus topology, firewall state, and disk space

**(a) Bind address versus topology.** A Core that bound loopback under the new default **without `setup` having widened it** is exactly the "reachable from *this* interface but not the one WSL2 can actually use" failure **that default made possible for the first time.** The check reports the address `/status` was reached at versus what the detected topology needs, **failing when they disagree rather than reporting bare unreachability.** For whoever implements it: **`embarch-topology` already exposes a recommended-bind-address function for exactly this comparison**, and `setup` **already calls** it and bakes it into the `install` invocation — so the address does get widened, and what is missing is only the check that would notice when it hadn't been.

**(b) Firewall state**, best-effort and informational, because **firewall state cannot always be introspected without elevation itself** — it names a likely-active profile when a connectivity probe fails and Core cannot be ruled out as simply not running.

**(c) Disk space** on the filesystem backing the build and results directories — warn below a generous threshold, **since a build failing from a full disk reads as a mystifying compiler error otherwise.**

**All three unbuilt:** `doctor` assembles exactly checks 1-15, and *firewall* and *disk* appear nowhere in the crate.

### 23 — Check 10 spawns `embarch-api` and confirms the MCP handshake completes, not just that a registration entry exists

**The failure mode the check exists to catch — registered but broken — is exactly the one it cannot detect:** adding a registration says nothing about whether the registered command actually starts and speaks the protocol. It would spawn the exact registered command with a short timeout and send a minimal initialize handshake, **reporting success, failure and timeout distinctly.** A hand-rolled one-shot JSON-RPC exchange is sufficient; a full client is not needed for one round trip.

**Unbuilt:** check 10 runs `claude mcp get embarch` and passes on a zero exit — the registration-entry test this decision was written to replace.

### 24 — Version skew between Core and the API stays a warning, not a refusal

Kept deliberately rather than escalated: **refusing to run a mismatched pair would obstruct the exact in-development, fast-iterating state this suite is still in**, with independent per-repo releases and a warn-not-refuse precedent already set elsewhere. **Revisit only once a mismatch is more likely an operator mistake than an expected in-progress state.**

### 31 — Check 14: which program Core would flash each chip family with

Core refuses to flash an nRF54L part with probe-rs, because that family stores code in RRAM and probe-rs does not model it. **The vendor tool that replaces it cannot be bundled — licensing, not effort — so it might simply be absent.** Discovering that at the moment someone flashes is the worst available time, **and discovering it in `doctor` is what `doctor` is for.**

**It shells out to the located `embarch-core` rather than reasoning here**, which on this bench means running a Windows binary from WSL2. **That is the point rather than an accident: the tool has to exist on the machine running *Core*, not the machine running `doctor`, and only Core's own binary can answer about the right machine.** A second copy of the search logic here would be a mirror that drifts.

**Failure signature it found immediately, and the best argument for the check existing.** Run through WSL2 interop, the Windows Core reported a tool at a **Linux path — an ELF a Windows process cannot execute** — because interop merges WSL's `PATH` into the Windows process and the existence test resolves it through the filesystem redirector. **The *service*, whose environment is the system `PATH`, resolves a different tool.** So the check was reporting a backend the thing it checks would never choose, **which is worse than no check.** Fixed in Core.

**An older Core with no such subcommand is a Warn naming what it predates, not a Fail** — a real and recoverable state during a staged rollout, and the deployment procedure already assumes Core and the tooling around it move separately.

### 33 — Check 11 compares three real numbers, and says which one it could not get

The check returned a hardcoded warn — *"not available yet, `embarch-study-designer` isn't wired into `embarch-core`/`embarch-api` as a dependency yet"* — after that had stopped being true. **It is a direct dependency of both**, and a live pair once sat at Core wire v13 against a bench flashed to v14 while this check reported "not available yet" the whole time. The handshake refused that state correctly and loudly, **but only to whoever called it by hand**; saying it unasked is the entire job of the surface that was silent.

**Three numbers, and they are not three of a kind.**

- **Core's served `study_designer_schema_version`** versus **the `HOST_TYPE_SCHEMA_VERSION` this `embarch` binary compiled** — the `embarch-api`⟷`embarch-core` hop, the one `embarch-api` itself refuses to submit a `Study` across. A difference is a **fail**: the pair cannot run a study at all.
- **The bench's wire version** cannot be compared against either of those. `DEV_BENCH_WIRE_SCHEMA_VERSION` counts its own sequence and is only guaranteed `<=` the host one, so equality means nothing and inequality means less. What *is* comparable is `/dev-bench/hello`'s `compatible` — **Core's own verdict**, Core comparing the bench's number against the wire constant Core compiled. Core's wire constant is served nowhere, so recomputing the verdict here would be a mirror with nothing to mirror.

**This binary's constant stands in for the located `embarch-api`'s, and the check is not pretending otherwise.** All three binaries ship from one suite archive, so the stand-in is exact whenever check 1's manifest agrees, and check 1 is the check that says so. The gap is filed in [../open.md](../open.md) rather than papered over.

**A missing number is a skip that names it, never a pass.** Core unreachable, no token, no bench, a `409` mid-study, a Core predating the field: each is a distinct `Warn` carrying its own reason, and the numbers that *were* obtained are still printed. A `Fail` always outranks a skip, so an absent bench cannot mask a host disagreement.

**`/dev-bench/hello` is fetched once for checks 11 and 13.** It is not a read — it opens the serial link long enough to handshake — so two checks asking separately would be two link opens for one answer. The visible consequence: the handshake now runs even when no dev-bench checkout is configured, where check 13 alone used to skip before calling it.

**The comparison is a pure function over injected numbers**, which is what lets the whole matrix be tested with no Core, no bench and no network — the check that gates deploys being untestable without the hardware it gates was most of why it stayed a stub.

### 34 — Check 15: `core_version` is a different question, so it is a different check

`GET /status` also serves `core_version` (`embarch-core` decision 13). **It is deliberately not one of check 11's three numbers.** Schema skew asks whether the pieces agree on a wire contract; this asks whether the Core answering on the network is the binary that was last built and deployed — and folding it into check 11 would present one verdict over two unrelated questions.

It compares `/status`'s `core_version` against the located `embarch-core` binary's own `--version`, both of which `doctor` already has. **`deploy-core` has printed `landed` twice in one session with nothing installed**, when the elevated child was cancelled ([embarch-dev-workflow.md](../../embarch-dev-workflow.md) §4a), and its own check compares byte *length*, which cannot discriminate a release rebuild of one constant.

**The limit is stated in the check's own output, not only here:** `core_version` is `CARGO_PKG_VERSION`, so it moves only when the crate version does. This catches a **cross-version** stale deploy and is blind to a same-version one. Strictly better than nothing, and not a hash comparison — a test asserts the blind spot rather than leaving it to the prose.

**Warn, never fail**, following `embarch-core` decision 13's "consumers warn, never refuse" and decision 24 above: independent per-repo versions are an expected state in a suite iterating this fast.
