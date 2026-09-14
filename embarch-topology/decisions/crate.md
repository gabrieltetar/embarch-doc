# embarch-topology decisions: One crate, called live

**Status:** active, 2026-09-02.

Why topology is a linked library rather than a tool, a file, or a service.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — This is a resolution/abstraction layer, not just a checker

The rest of the suite should be able to say "give me dev-bench" or "what's my base URL" and **get a resolved answer**, rather than each independently re-implementing VID heuristics or a WSL2-gateway probe. **A deliberate step further than a read-only diagnostic: it is the thing that produces the answer, not just the thing that flags when the answer looks wrong.**

### 2 — A shared crate `embarch-core`, `embarch-api` and `embarch-umbrella` all link and call in-process

All detection, resolution, enrollment and validation lives in one crate; the three consumers call its functions directly, live, whenever they need an answer. Its own CLI is a thin wrapper over the same functions.

**Reversed from this session's own earlier decision**, which picked a doctor-style standalone tool specifically to avoid a shared library, **reasoning that the suite had deliberately kept mirrored copies of cross-repo logic instead of extracting crates.** That reasoning held right up until working through mismatch detection surfaced the actual cost of *not* sharing code: **Core still needed either a written-ahead file or a manual override to know the current answer — and a manual override left unmaintained is exactly what caused the motivating incident.** A shared crate Core calls live removes the need for either.

**This is not a reintroduction of the rejected standalone-service option.** That was rejected because **a network or IPC dependency in the hardware-operation path is a new thing that can be down**; a compiled-in library call carries no such risk, since it is just code running in Core's own process. There is already suite precedent for this shape of sharing — **`embarch-study-designer` extends it from shared *data types* to shared *logic*.**

### 3 — Live, in-process, on every call — no write-ahead file for anything auto-detectable

Per request for anything that can change while a process runs (dev-bench's port, on unplug/replug); once at startup for anything that cannot (a bind address, fixed for the life of the socket). **There is no resolve-then-write step and therefore nothing that can go stale between a write and a read.**

**Reversed**, same session, alongside decision 2: the earlier framing had this crate write resolved answers into files the consumers read. **That solved "the file might be missing" but did not remove the *incentive* for a manual override to exist in front of it** — which is what decision 9 was built to detect and is now retired to prevent instead. **The only state that still needs writing is a human's declared intent that detection cannot derive at all**, and it lives inside the crate's own storage, not as a file any consumer parses.

### 6 — `doctor`'s topology-relevant checks call the crate directly, in-process

They become thin wrappers translating a crate call into pass/fail/warn.

**Reversed**, same session: originally `doctor` was going to shell out to a CLI with its own JSON contract, **mirroring the precedent set for the target-count check.** That precedent fit when this was a separate process; **once it is a linked crate, calling it directly is simpler and consistent with how Core and the API consume it — no process spawn, no JSON boundary to keep in sync.**

### 13 — Started as a design-only doc with no repo

Matching how `embarch-umbrella` and `embarch-dev-bench` both started. Flagged at the time because **a shared crate needs *somewhere* for three consumers to depend on**, which pulls "when does a real repo need to exist" earlier than a design-only doc's usual timeline. The repo is real now: [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology), depended on as a **plain path dependency** — exactly `embarch-study-designer`'s precedent — with the hardware feature added only by Core.

**Release CI needed a real fix beyond the dependency line.** Each consumer's release workflow **only ever checked out itself**, so a relative path dependency could never resolve; fixed by checking out every path-dependency repo as a named sibling and building from inside the consumer's own subdirectory. **The same gap already existed for `embarch-study-designer`** — added days earlier and never exercised by a green release run — and was fixed in the same pass. Whether the Docker-based aarch64 cross build can see siblings outside the crate root was **researched against the tool's own history rather than assumed** (it auto-mounts any path dependency the metadata can see) and then **confirmed by a real tagged release run**, not by research alone.

### 32 — `enroll`'s probe selection duplicates `embarch-core::resolve_probe`, documented rather than de-duplicated

**Found by `core/053`'s worker while rewording `embarch-core`'s own doc comment, dropped to this crate's inbox because a `core` worker cannot write here.** `embarch_topology::hardware::validate::enroll` (`src/hardware/validate.rs`) carries its own inline probe-selection block — list every attached probe, find-by-serial if given, else bail unless exactly one is attached — structurally the same rule as `embarch-core::resolve_probe` (`src/hardware.rs`, `pub(crate)`, that crate's decision 9). **Before `embarch-core` decision 22 moved the board-identity gate wholesale into this crate, that was one implementation**: `board_gate.rs` lived inside `embarch-core`, so `resolve_probe` really was shared behind both the enforce path (flash/reset) and the enroll path. The move put `enroll` in a different crate than `resolve_probe`, and `pub(crate)` cannot cross that boundary — so the move silently turned one shared implementation into two independently maintained ones, without either side's tests or the gate noticing.

**Exactly `embarch-core` decision 9's own drift class**, restated one repo over: a rule described as centralized quietly stops being that, and nothing fails until the copies disagree — there, "single-probe-only" survived months until a real second probe exposed it.

**Documented, not de-duplicated, because the direction that would close it is not available from here.** `embarch-topology` is a dependency of `embarch-core`, not the other way round, so this crate cannot depend on or re-export `embarch-core`'s helper. The only real de-dup path is the other direction — this crate exposing a `pub` selection helper and `embarch-core`'s own `resolve_probe` calling it instead of keeping its private copy — and that requires an edit inside `embarch-core`, which is out of reach for a topology-scoped change. Recorded as open work (`open.md`) rather than actioned here.

**Amended 2026-09-13 — the topology half of the close is landed; `embarch-core` still holds its copy.** `tasks/topology/038` did the half that was in reach: `enroll`'s inline block is now a call to [`select_probe`](https://github.com/gabrieltetar/embarch-topology/blob/main/src/hardware/validate.rs), a `pub` function in `embarch_topology::hardware`. This decision stays open, not closed — `embarch-core::resolve_probe` is still its own copy until `tasks/core/055` (blocked on this landing) makes it call `select_probe` instead. See decision 33 for the reconciliation that made one shared function possible: the two copies had **already drifted** by the time `038` looked, past what a mechanical extraction could paper over.

### 33 — `select_probe` reconciles three real divergences between the two probe-selection copies, not just their shape

**Filed alongside decision 32's amendment above, same landing.** `038`'s worker verified both copies live on `main` before extracting anything and found the drift was real, not assumed: `embarch-core::resolve_probe` special-cased `probes.is_empty()` first, with a usbipd hint (*"check the USB connection (and usbipd attach, if Core is on a Pi and the probe is elsewhere)"*); `enroll`'s inline block had no such case, falling through a `len() != 1` bail whose message named enrollment specifically (*"plug in only the board you mean to enroll"*). Every error string differed. A shared function had to pick, not just relocate code.

**Zero probes is now checked first, unconditionally, keeping the usbipd hint** — the one piece of genuinely diagnostic content either copy had, and the strongest available diagnosis regardless of whether a serial was given. Where a serial *was* given, the message now names it too (*"no debug probe found (looking for serial 'S1') — check the USB connection…"*), so nothing that `enroll`'s old serial-first order used to convey is lost — it is folded into the stronger message rather than kept as a separate branch. **This changes `enroll`'s own observable behavior** for the zero-probes-with-a-serial case, from *"no attached probe with serial 'S1' — is it still plugged in?"* to the usbipd-hinted message above; the two callers agreed this case is rare enough (a probe present with the wrong serial is common, zero probes at all attached to a machine already running enrollment is not) that a better diagnosis wins over a narrower one that happened to be `enroll`'s original wording.

**The `len() > 1` vs. `len() != 1` divergence closes for free.** Once zero probes is handled first and unconditionally, checking `len() > 1` afterward is exactly `!= 1` restricted to the surviving case — not a second policy choice, just the one order that makes the two predicates provably the same rule instead of accidentally-equivalent ones that stop matching the moment either copy is edited alone (exactly the failure decision 32 named).

**The multi-probe and serial-miss wordings are reconciled differently, deliberately.** Serial-miss keeps `enroll`'s phrasing (*"no attached probe with serial 'X' — is it still plugged in?"*) outright — friendlier than `resolve_probe`'s bare *"no attached probe has serial_number 'X'"*, and there is no caller-identity reason to want the plainer one. Multi-probe keeps neither wording whole: it takes a caller-supplied `action` verb (`"enroll"`, `"flash"`, `"reset"`, …) so the refusal reads *"{action} requires exactly one debug probe attached (N seen) — plug in only the board you mean to {action}, or specify which probe by serial"* — `enroll`'s own phrasing, generalized rather than replaced — and additionally lists every attached probe's identifier and serial, which `resolve_probe` did and `enroll` never had. **A caller-supplied noun over a single fixed wording**, because `enroll`'s enrolment-flavored phrasing is worth keeping for its own caller and a flash/reset caller reads just as naturally with its own verb substituted — collapsing to one wording would have meant arguing the enrollment flavor away rather than keeping it for free.

**Testable over hardware-reaching, and it took a signature change to get there.** Neither original copy had a unit test; both called `Lister::list_all()` internally, which needs a real probe-rs enumeration to exercise at all. `select_probe(probes: Vec<DebugProbeInfo>, probe_serial: Option<&str>, action: &str)` takes the list instead — `enroll` now calls `Lister::new().list_all()` itself and hands the result in, which is the only change needed to make five cases (zero / one / two probes, serial-hit, serial-miss) run with no hardware attached, using a fake `DebugProbeInfo` built from a real `ProbeFactory` (`JLinkFactory`, never opened) rather than a mock trait.

