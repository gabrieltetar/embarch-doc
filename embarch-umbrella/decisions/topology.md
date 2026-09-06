# embarch-umbrella decisions: Finding Core

**Status:** active, 2026-09-02.

Detecting where Core is, and what may be done to it from here.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 6 — Topology is auto-detected by probing, not declared — and only the *class* is ever persisted, never an address

An ordered candidate list, each tried with a short-timeout status call: loopback first (which covers Core-local on every OS *and* WSL2 in mirrored-networking mode), then the WSL2 default gateway when running under WSL2, then a user-supplied host. First responder wins.

**A `401` counts as a hit, not a miss**, and is reported distinctly: **Core is there and the token does not match, which is a completely different fix from "Core isn't running."** A third outcome turned out to be worth distinguishing too — something answering HTTP with neither status **is not Core at all**, most likely another service squatting the port, and reporting that as "nothing there" would send someone to start a Core that cannot bind anyway.

**"Race" means ordered-sequential, not concurrent.** Ordering is the whole point, and the common miss is a connection refusal that returns immediately, so **a concurrent fan-out would buy nothing and lose the preference order.** The per-candidate budget is only ever paid where packets are silently dropped.

**Only the resolved class is written down** — `local`, `wsl-host` or `remote`, plus the host for `remote` only — **never the WSL2 gateway IP, which is dynamic and has already gone stale once in this suite's own records** (two different addresses recorded in two places). The address is re-resolved at every use instead (decision 9).

**Moved into `embarch-topology`, algorithm unchanged** — see decision 15. This repo's own modules are deleted; `status`, `setup` and `doctor` call the shared crate.

### 7 — Starting Core across the WSL2⟷Windows boundary is supported, because it is the same physical machine

WSL2 can invoke a Windows binary directly, so `up` from the WSL2 side is mechanically possible. **Controlling a *system* service needs elevation, and not only on Windows** — a systemd system unit wants root or a polkit prompt too, confirmed on Linux where an unprivileged start fails with "Interactive authentication required". This decision originally treated elevation as a Windows-only tax.

**Reversed on the never-self-elevate half.** It originally had umbrella and Core never self-elevate anywhere — print the exact command, exit nonzero, let a human paste it into a shell they open themselves — reasoned as acceptable *because* Core autostarts, making elevation rare. **That reasoning covered first-time install but not updating an already-installed Core's binary**, which has no reason to be rare once the suite is under active development, and which had **no supported path at all** beyond manual service-stop/copy/start surgery in a hand-opened elevated shell. Self-elevation now happens **in `embarch-core` itself, not as a second copy of the logic here**, since umbrella already reaches every privileged operation by shelling out to that CLI. The one case it does not cover — no GUI and no TTY — falls back to this decision's original behaviour, since **there is no one there to click through a prompt anyway.**

### 8 — A Core on a genuinely separate machine is detect-and-verify only

No SSH, no remote install, no remote start. `doctor` reports it reachable-or-not and tells the human to go start it there. **This topology also could not flash**, because the flash route reads a path from Core's own local disk and there was no shared filesystem to put an artifact on; `embarch-api`'s multipart upload closed that, so flashing works now — **via uploaded bytes rather than a shared path.**

### 9 — `base_url = "auto"` is implemented in `embarch-api`, not here

Umbrella could write a resolved URL into the config at setup time, **but that just relocates the staleness problem**: the WSL2 gateway IP changes on WSL restart, long after setup ran. So the config gets the literal string and `embarch-api` re-runs decision 6's candidate race itself, per process, at the point it first needs Core. **It belongs to the API because the API is the thing that has to be correct at 3pm on a Tuesday, not at install time.**

### 30 — Under WSL2, `up` probes for the installed Windows service before considering a guest-local Core

Decision 6 recorded the ambiguity and stopped: with mirrored networking **a Windows-hosted Core and a WSL2-guest-hosted Core both answer at loopback**, so a `local` classification does not say *where* Core is — and `up` has to know before deciding whether it can start Core itself or needs the Linux elevation path. **Detection already knew it was under WSL2; what `up` did with that was never designed.**

It checks for the installed Windows service first, and drives that Core when one is there. **Not a coin flip dressed as a heuristic:** the Windows service *is* the suite's actual deployment on the only machine this has ever run on, so the probe resolves the ambiguity in favour of the thing that is really there and degrades to the old behaviour otherwise. **It also fails safe — probing for a service is read-only, so a wrong guess costs a check, not a botched start.**

*Rejected: prompting once and recording the answer* — unambiguous by construction, but **adds an interactive prompt to a command meant to run unattended.** *Rejected: refusing without an explicit flag* — never guesses wrong, at the price of **making the single most common command on the suite's primary topology fail by default until a flag is typed.**

### 38 — `locate_core` reads the Windows service's own registration, and check 1 stops calling a healthy `wsl-host` machine broken

The first live `doctor` run opened on a red — `embarch-core: not found` — on a machine `setup` had just called correct **in the same session**: "not next to this binary, skipped", "already running — nothing to install". Two commands in one sub-project disagreeing about the same fact, and only one could be right. **The absence of a Linux `embarch-core` is the expected state on this topology, not a defect.** Check 14 then fell in behind check 1 with `skipped — see check 1`, so the failure cost two checks rather than one, and a run whose first line is a false red teaches its reader to skim the other fifteen.

**Two readings, and the first wins because check 14 needs a binary, not an excuse.** *(a)* Make check 1 topology-aware and actually **find** the Windows Core. *(b)* Keep check 1's shape and mark its `embarch-core` half not-applicable on this class. (b) alone clears the red and leaves check 14 permanently unanswerable on the suite's primary topology — [decision 31](doctor.md) has it shell out to Core's own binary precisely because nothing else can answer about the right machine. So (a) is built, **with (b) as the fallback when (a) genuinely finds nothing**: located, or an explicit not-applicable warn, never a fail where no local Core belongs. The warn covers `remote` too, which had the same false red for the same reason.

**What (a) reads is the service's own `BINARY_PATH_NAME`** — which [decision 32](deploy.md) has read since `deploy-core` existed, for the same reason: `locate_core`'s two Windows sources are guesses by design, and on this bench the live service runs out of a directory on neither list. It sits **after `PATH`**, because a binary this side of the boundary is cheaper for `doctor` to run, and **ahead of both guesses**, because a reading beats a guess. `sc.exe qc` is read-only, so a wrong answer costs a check rather than a botched anything, and a registration whose file is gone falls through. It carries **its own `FoundBy`**: check 1 prints provenance, and "the service's own registration" is a different claim from "a conventional directory".

**[Decision 31](doctor.md)'s rule governs, and it cuts both ways.** A path `sc.exe qc` names and `wslpath` translates is *the same file* the Windows service runs, so this is not a confident verdict about the wrong machine. **But the suite manifest next to `embarch` is one**: it describes the Linux archive this binary came from, while Core is a Windows build out of a different one. Check 1 no longer compares those two, says so, and names [check 15](schema-skew.md) — which compares the located Core against the *running* one and is the instrument that owns the question.

**The residual, stated rather than hidden.** Check 14 runs that exe through WSL2 interop as the WSL user, while the service runs under the system account, so a vendor flashing tool installed on a user `PATH` only is visible to one and not the other. Narrower than decision 31's original bug — a Linux ELF reported to a Windows process, fixed in Core — and **not closed**.

**Measured end to end 2026-09-05**, on the first run after the `deploy-core` that had never landed: check 1 located the service's own binary by `BINARY_PATH_NAME`, and **check 14 answered rather than skipping** — `nRF54L15=jlink, nRF52840=probe-rs, esp32c5=probe-rs`. That is (a) working on the topology it was built for, and it is the first evidence for it; the interop residual above is untouched by the run.
