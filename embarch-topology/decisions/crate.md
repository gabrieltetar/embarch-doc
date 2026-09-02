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

### 4 — Both software and hardware topology, in one pass, not hardware-first

The board-identity gate, its storage, the dev-bench port heuristic, **and** the software-class detection then mirrored between `embarch-api` and `embarch-umbrella` all move here as the sole implementation. **The mirrored-copy CI diff job becomes obsolete: there is nothing left to mirror once everyone links the same crate.**

### 6 — `doctor`'s topology-relevant checks call the crate directly, in-process

They become thin wrappers translating a crate call into pass/fail/warn.

**Reversed**, same session: originally `doctor` was going to shell out to a CLI with its own JSON contract, **mirroring the precedent set for the target-count check.** That precedent fit when this was a separate process; **once it is a linked crate, calling it directly is simpler and consistent with how Core and the API consume it — no process spawn, no JSON boundary to keep in sync.**

### 8 — One implementation, multiple call sites — not two independent layers

A human running the CLI **sees precisely the validation Core enforces live, because it *is* that validation — there is no way for the two to disagree, since there is only one of them.** Concretely: whatever port or probe an operation is about to use, one shared `validate()` confirms the device is currently enumerated and still matches the identity recorded for its role, and **returns a specific error naming what is stale** if it does not.

**Reversed** from an earlier framing that described an ahead-of-time check and Core's live re-check as **two independent, separately-reasoned mechanisms that happened to agree.** They are not independent once both are calls into the same crate.

**A real gap this surfaced:** the live-identity recheck covered only JTAG-capable roles. **The dev-bench runtime *link* had no equivalent live check** — which is what absorbing that logic had to close here rather than leave behind in Core.

### 13 — Started as a design-only doc with no repo

Matching how `embarch-umbrella` and `embarch-dev-bench` both started. Flagged at the time because **a shared crate needs *somewhere* for three consumers to depend on**, which pulls "when does a real repo need to exist" earlier than a design-only doc's usual timeline. The repo is real now: [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology), depended on as a **plain path dependency** — exactly `embarch-study-designer`'s precedent — with the hardware feature added only by Core.

**Release CI needed a real fix beyond the dependency line.** Each consumer's release workflow **only ever checked out itself**, so a relative path dependency could never resolve; fixed by checking out every path-dependency repo as a named sibling and building from inside the consumer's own subdirectory. **The same gap already existed for `embarch-study-designer`** — added days earlier and never exercised by a green release run — and was fixed in the same pass. Whether the Docker-based aarch64 cross build can see siblings outside the crate root was **researched against the tool's own history rather than assumed** (it auto-mounts any path dependency the metadata can see) and then **confirmed by a real tagged release run**, not by research alone.
