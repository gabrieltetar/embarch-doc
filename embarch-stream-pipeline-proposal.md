# Proposal: the write direction of the stream pipeline

**Status:** proposal, 2026-09-02.

**The inbound half of this proposal was accepted and is built. The outbound half — sending bytes *to* a DUT and confirming what comes back — is still only proposed, and is what this file now is.**

Spans four repos plus the Study Designer tab, which is why it sits at this repo's root rather than in one sub-project's folder ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).

## What was accepted, and where it lives now

The read direction — one inbound pipeline whose source, sink and decoding are declared, with a bench that interprets no payload — is built and lives in [embarch-study-designer](embarch-study-designer/decisions.md) decision 39, [embarch-core](embarch-core/decisions.md) decision 30, [embarch-dev-bench](embarch-dev-bench/decisions.md) decision 29, [embarch-api](embarch-api/decisions.md) decision 39, [embarch-ui](embarch-ui/decisions.md) decision 10 and reversals rows 17, 18 and 25 (the last two: what this file got wrong about it).

**Since then, two decisions reach into the half below.** `embarch-study-designer` decision 58 (an engineer-written protocol manifest that dev-bench executes) records itself as closing decision 39's write direction by a different route, an authored state machine rather than a generic write step; and decision 37 built a free-text payload path. Nothing in a task, an `open.md` or the roadmap asks for the generic send step any more.

## The proposal: an authored write step

Nothing in the suite sends anything to a DUT this way yet, and the outpost is TX-only, so **adopting a step type nothing emits would be building an unused capability.** It stays proposed for that reason, not because the shape is in doubt.

**The write direction needs no new message and no new lifecycle.** A send step arrives inside the study dev-bench already receives and executes in order like every other step. **Core sends nothing mid-study; the receive-then-run loop is unchanged.**

**The sink is declared on the tap, not per step.** Most taps are read-only — a power trace and a PPG waveform have nothing to write back to — so the sink is optional. A console tap declares both directions, **and that pairing is the engineer's declaration, not something inferred from a service UUID.** Many send steps, one place that says what "the console" is. The tap also carries whether the write wants a response, **because which one a characteristic supports is visible in its discovered properties and picking wrong silently fails on some stacks**, and the line ending, **so a string authored once behaves identically from the UI, the CLI, or a JSON file — shells differ, and this suite does not get to assume.**

**A send step is: a tap that has a sink, a payload already line-terminated by whoever authored it, and an optional expectation.** Firmware stays dumb: it writes exactly those bytes and appends nothing.

**The expectation is what makes this a *test* rather than a fire-and-forget write.** The bench watches the named tap's inbound bytes for a **raw byte substring**, from the moment the write completes until a timeout: pass on a match, timed-out if it never arrives, fail if the write itself failed. **No new outcome vocabulary**, and it feeds the existing continue-on-fail rule like every other step — **which is the whole reason this is a real-time firmware-side check and not a post-hoc one: dev-bench cannot know a post-hoc result in time to decide whether to continue.**

**A byte-substring search is not an interpretation.** The bench does not need to know the payload is text, where a line ends, or what the DUT meant — only whether a given byte sequence appeared. It needs a rolling carry-over of one byte less than the pattern so **a match spanning two notifications is not missed. That is the entire algorithm**, and it keeps the never-infer-DUT-semantics line intact: the *string* comes from the engineer, the *matching* is mechanical.

Three details that are decisions rather than parameters:

- **The expectation's tap is separate from the write's**, so a study can write to a control characteristic and confirm on the log characteristic. It usually points at the same tap; **costing nothing to allow both is better than discovering the restriction later.**
- **It matches only what arrives after the write.** Bytes already in flight before the step started do not count, **which is what makes a sequence of send steps behave the way an author expects rather than matching a previous command's output.**
- **Nothing lands in the step result** — the transcript is in the stream file, the verdict is the existing outcome. This adds no bytes to the type two docs already carry crash reports against.

**Pre-flight rejects what would otherwise fail three hops away**, by name, at submit: the tap index in bounds, the write tap actually has a sink, and both taps' scope covers the step.

**On the bench**, a send step is one GATT write to a handle resolved when the tap armed — so no discovery round trip — plus an outbound record for the transcript and then the substring match. **No new inbound-serial handling, no concurrency with a running study, no change to the main loop's model.**

**One consequence worth stating: a dropped record can cost an expectation its match**, so a timeout is ambiguous between "never sent" and "dropped". The tap's own drop count is what disambiguates it after the fact, **and it belongs next to the step's outcome in the UI rather than only in the file.**

**Authoring is a step-table row**: choose the tap, type the string, optionally type the expected response and a timeout. Both the tap and the command persist as presets in the per-repo action registry, **so a characteristic's format and a repo's useful commands are declared once per firmware repo rather than retyped per study.**

## Why a live console was withdrawn

The proposal's third revision made this bidirectional with a live, mid-study console: write at any time, a POST endpoint per stream, a cancel endpoint, a terminal pane. **Withdrawn, and it was the actually-risky version.**

**A live console makes a study non-replayable** — its transcript depends on what somebody typed while it ran — and a study is *entirely static once submitted* for good reasons. **Authoring the string up front keeps every one of them:** the write is inside the sealed steps, re-runnable, diffable, and reviewable before it ever reaches hardware.

It was also strictly larger. The interactive version dragged in **a cancel endpoint, a mid-study Core→dev-bench message, and concurrent inbound serial handling in firmware** — all of which disappear here. The authored version **deletes the largest firmware change, the new HTTP surface, the cancel dependency, and the reproducibility problem at once, and needs no new message from Core to dev-bench at all.**

## Free text, and why it does not erode the never-infer rule

A one-off free-text payload is built: `RowAction::Raw`, [embarch-study-designer](embarch-study-designer/decisions.md) decision 37, which says why bytes an engineer typed are not an inference. **What stays proposed is a free-text field kind in the action registry** (decision 35 keeps it enumerated-values-only), so a shell command can persist as a preset.

**What stays forbidden is unchanged:** a value this suite generates, guesses, defaults, or labels with an invented description. **No "suggested commands", no parsing the DUT's source for a shell command table, no help text this crate writes about what a command does.**

## Left alone deliberately

**Monitor-everything looks foldable into N auto-armed taps** — discover, subscribe to everything, capture — **but its job is different: bounded reconnaissance whose result belongs *inline* beside the discovered GATT table**, answering "what does this DUT even emit?" **It is what you run *before* you know which characteristic deserves a tap, and its record ceiling is a feature for recon and a bug for capture.** Re-expressing it as taps is a plausible later simplification, not this change.

`serial_log` also stays as it is — dev-bench's link, an unrelated hop.

## Still open

- **The capacity constants** — how many taps per study, how long an expectation pattern may be, and the bench's buffer pool sizes. Needs the real link and real notification rates, **the same posture as every other hardware-unvalidated constant in these docs.** The bench's SRAM headroom is the binding check, and it is the first thing to measure: **the batch pool is shared across taps, not one buffer each.**
- **Whether richer matching than a substring is ever worth the firmware.** Resolved once as substring-only, on the grounds that **a richer check is already expressible post-hoc over the same stream, which is the cheap way to find out whether the real-time version is ever worth building.** Revisit only with a real case post-hoc validation genuinely cannot serve.
- **Whether the DUT premise holds at all.** Whether any specific DUT streams its console on subscribe, what it expects written, and what it prints back **is not established here, and by construction does not need to be** — the engineer names the characteristics, the command and the expected response. **The first real run against a real DUT is the validation, and it has not happened.**
- **Multi-value records for a genuinely multi-lead sensor** — the sample-grain question the shared crate already carries, unchanged. The declared layout is where it would eventually be expressed.
