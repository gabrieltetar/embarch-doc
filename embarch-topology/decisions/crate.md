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

**Qualified 2026-09-08** (`tasks/topology/020`, from `api/038`'s finding): "the sole implementation" and "nothing left to mirror" describe the crate's own boundary, not its callers. `embarch-api/crates/embarch-core-client` already linked this crate and still ran a second, narrower predicate (`token_discovery::is_wsl2`) beside the call it never made to `detect_wsl2` — closed by `api/038` (`embarch-api` decision 62, `861f30f`), which made it delegate. Linking the crate stops a mirrored *copy* of its own logic; it does not stop a caller writing an unrelated second predicate next to a call it never makes. A third copy, `embarch-umbrella/src/token.rs`, is still live and is `umbrella/036`'s to close, not this decision's to claim closed.

### 6 — `doctor`'s topology-relevant checks call the crate directly, in-process

They become thin wrappers translating a crate call into pass/fail/warn.

**Reversed**, same session: originally `doctor` was going to shell out to a CLI with its own JSON contract, **mirroring the precedent set for the target-count check.** That precedent fit when this was a separate process; **once it is a linked crate, calling it directly is simpler and consistent with how Core and the API consume it — no process spawn, no JSON boundary to keep in sync.**

### 8 — One implementation, multiple call sites — not two independent layers

A human running the CLI **sees precisely the validation Core enforces live, because it *is* that validation — there is no way for the two to disagree, since there is only one of them.** Concretely: whatever port or probe an operation is about to use, one shared `validate()` confirms the device is currently enumerated and still matches the identity recorded for its role, and **returns a specific error naming what is stale** if it does not.

**Reversed** from an earlier framing that described an ahead-of-time check and Core's live re-check as **two independent, separately-reasoned mechanisms that happened to agree.** They are not independent once both are calls into the same crate.

**Qualified 2026-09-08** (`tasks/topology/020`): "there is no way for the two to disagree, since there is only one of them" holds only inside the crate's own boundary — a statement about the crate, not about whether a caller actually calls it. `api/038` found `embarch-api`'s own client still ran a second, narrower WSL2 predicate beside a call it never made to this crate's `detect_wsl2`, and closed that instance by making it delegate. Whether anything should detect a caller declining to call the crate at all: see `open.md`.

**A real gap this surfaced:** the live-identity recheck covered only JTAG-capable roles. **The dev-bench runtime *link* had no equivalent live check** — which is what absorbing that logic had to close here rather than leave behind in Core.

### 13 — Started as a design-only doc with no repo

Matching how `embarch-umbrella` and `embarch-dev-bench` both started. Flagged at the time because **a shared crate needs *somewhere* for three consumers to depend on**, which pulls "when does a real repo need to exist" earlier than a design-only doc's usual timeline. The repo is real now: [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology), depended on as a **plain path dependency** — exactly `embarch-study-designer`'s precedent — with the hardware feature added only by Core.

**Release CI needed a real fix beyond the dependency line.** Each consumer's release workflow **only ever checked out itself**, so a relative path dependency could never resolve; fixed by checking out every path-dependency repo as a named sibling and building from inside the consumer's own subdirectory. **The same gap already existed for `embarch-study-designer`** — added days earlier and never exercised by a green release run — and was fixed in the same pass. Whether the Docker-based aarch64 cross build can see siblings outside the crate root was **researched against the tool's own history rather than assumed** (it auto-mounts any path dependency the metadata can see) and then **confirmed by a real tagged release run**, not by research alone.

### 23 — Storage sits under the same machine-wide directory `embarch-core`'s token file already uses, one level down in a subdirectory this crate owns

`data_dir()` resolves to `/var/lib/embarch/topology` on Linux/macOS and `%ProgramData%\embarch\topology` on Windows. `embarch-core`'s `token_store.rs::local_data_dir()` resolves to the parent of that same path — `/var/lib/embarch` / `%ProgramData%\embarch` — and its own token file lives directly under it. **Confirmed by reading `token_store.rs`, not assumed**: the two functions compute byte-for-byte the same root by the same OS split, and this crate's `machine_data_dir()` is a straight copy of that logic with one `.join("topology")` added.

**Why the same directory, rather than a directory of this crate's own:** it has to be machine-wide — but **not admin-owned, which was the original wording's error, corrected 2026-09-07** (`tasks/topology/013`). `embarch-core`'s Windows lockdown ([embarch-token.md](../../embarch-token.md)) restricts its **token file** to the creating account, `SYSTEM` and Administrators, by an explicit `icacls` call in `token_store.rs::restrict_token_file_permissions` — and that call runs against the file, never the directory. Both `token_store.rs::local_data_dir()` and this crate's own `machine_data_dir()` just `create_dir_all` the shared root, so `%ProgramData%\embarch` keeps whatever ACL Windows gives a fresh `ProgramData` subfolder by default, never touched by `icacls`. **That default permissiveness, not an admin-only lockdown, is what actually lets a Windows service account and an unprivileged interactive CLI both create and read files there** — this crate's `enrollment.toml` gets no per-file lockdown of its own, so the directory's untouched default is the whole of its access story. Reusing Core's directory rather than inventing a sibling one is still continuity, not coincidence: it is the same directory `known_boards.toml` already used before this crate existed (decision 3), so a store from before this decision still loads without migration.

**Settled from both crates' source directly, not from either doc and not from a live ACL** — a WSL session cannot read a Windows ACL, and this did not turn out to need one: `token_store.rs`'s `icacls` call names its own argument (`path`, the file) unambiguously, and neither it nor `paths.rs` touches the directory. `embarch-token.md`'s "Core creates the directory and file with owner-restricted permissions" reads as if both were locked down, which is what this decision's original wording copied; only the file is, and that phrasing is embarch-core's to tighten, not this crate's — flagged to its owner rather than edited across the boundary.

**Not a new fact for detection to derive** — decision 3 already settled that the crate's own storage is unwritten by anything but a human's declared intent; this decision settles *where* that storage physically sits and *why* it has to agree with a sibling repo's, which decision 3 did not address. Picked over a named `spec.md` section because the interesting content here is the reasoning for *why this directory* and not a directory of the crate's own, not an added declared fact — `spec.md`'s "The declared facts" table already carries the one-line fact ("Storage is one file under a machine-wide directory this crate owns") and now cites this decision rather than restating the argument.

**embarch-core's own docs already state its half of this** ([spec.md line 85](../../embarch-core/spec.md), [embarch-token.md](../../embarch-token.md)) — including naming this crate's `enrollment.toml` as sharing the convention — so there is nothing to file back to that repo.
