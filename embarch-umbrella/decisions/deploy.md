# embarch-umbrella decisions: `deploy-core`

**Status:** active, 2026-09-02.

The WSL2-to-Windows-service deploy, and the verification that is the point of it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 32 — `embarch deploy-core`: the WSL2-to-Windows-service deploy becomes a command, and its silent failure mode becomes a check

**A documented five-step manual procedure with a silent failure mode in the middle is a command waiting to be written.** Writing the procedure down fixed the forgetting; **it did not fix the re-typing** — every deploy since had been a hand-assembled sync loop, a hand-typed absolute compiler path, and a from-scratch elevated script, **re-derived, un-reviewed, and different each time.** The session that said this out loud had already written that script from scratch one more time first.

**What it does unelevated:** sync the three crates — **shared first, Core last, because Core has path dependencies on both, so a run that copied it first and died leaves a tree that builds cleanly and is wrong** — then build with the Windows compiler. Then one elevation around stop → copy → start. Then **verify the binary on disk actually changed.**

**That verification is the point of the whole command.** Core's own self-elevating update **exits `0`, prints nothing, and does nothing** when the consent dialog is never answered — which once left the live Core down for several minutes. **A deploy that cannot distinguish success from that is not a deploy.**

**Nothing is guessed.** The install target comes from the service's own registered binary path — **read-only, and the authoritative answer, where the conventional-location list is a guess by design and on this bench would miss entirely**, since the live service runs out of a directory on no such list. **The Windows source root is never probed:** nothing distinguishes a directory holding this suite's source copies from any other directory, and **building the wrong tree and deploying it is worse than refusing** — so an unset value is an error naming the flag, remembered afterwards. Paths are saved only **after a deploy that landed**, so a wrong one is not inherited by the next run.

**Decision 7 is narrowed here, not abandoned, and the distinction is that umbrella still never elevates silently.** `--print-script` is decision 7's posture verbatim — do everything unelevated, write the script, print the one command — and is what runs when not under WSL2 at all. **The default merely saves the human a copy-paste, through one prompt they see and can decline.** The script logs each step from *inside* the elevated context, **because the relaunch gives the child its own console and a redirect around the unelevated launcher captures nothing**; it waits for the service to actually reach `STOPPED` rather than trusting the stop command's own return, **which reports the request and not its completion**; and **it rolls the old binary back on failure** rather than leaving the service pointed at a half-copied file.

It also prints the dev-bench wire schema version, **read out of `embarch-study-designer`'s own source at deploy time** — the same trick that crate's firmware build uses, and for the same reason: **umbrella links none of the binaries it orchestrates, so reading the source is the only honest way to state the number.** A wire bump means reflashing the bench in the same sitting, and **the command gives that reminder rather than a human having to remember it.**

**Amended — the check did not catch the failure it was written for, and the command reported success through it.** Deploying a real fix, the elevated child was cancelled, `deploy-core` **printed its own correct diagnosis** and then printed **"landed, and the service is running"** immediately after it. Twice, on two consecutive invocations. The installed binary never changed, confirmed by hash. Two separate defects:

- **The verification compares a byte count, and the two builds were the same size.** The command even said so — *"the installed binary is already N bytes — this deploy may be a no-op, and the verification below cannot tell the difference"* — and reported landing anyway. **A length check cannot discriminate a release rebuild of one constant, which is the *most common* thing a development deploy carries.** It has to hash. Dogfooding had recorded "one of them a rename-only change where the length check correctly reported that it could not discriminate" — **which shows this was known and read as a corner case rather than as the normal case.**
- **The success line does not depend on the elevated half having run.** What it keys off — the service being `RUNNING`, which it was, **because it was never stopped** — is true of a deploy that did nothing at all. **An explicit cancellation is a hard failure and must exit non-zero.**

**What is *not* wrong with it: self-elevation from WSL works fine.** Both cancellations were the repo owner simply not being at the machine when the dialog rendered, and a third invocation with them watching installed and restarted cleanly, **verified by hash on both sides.** The reading that the prompt "never rendered" came from the command's own diagnostic line, **which cannot distinguish a dialog nobody answered from a dialog that never appeared** — worth narrowing, because **the two have completely different fixes and the wrong one was believed for an hour.**
