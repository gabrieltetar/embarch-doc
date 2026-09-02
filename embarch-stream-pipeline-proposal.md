# Proposal: the write direction of the stream pipeline

**Status:** proposal, 2026-09-02.

**The inbound half of this proposal was accepted and is built. The outbound half — sending bytes *to* a DUT and confirming what comes back — is still only proposed, and is what this file now is.**

Spans four repos plus the Study Designer tab, which is why it sits at this repo's root rather than in one sub-project's folder ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).

## What was accepted, and where it lives now

The proposal's thesis was: **the suite is on its way to three near-identical capture pipelines that differ only in what the bytes mean — replace them with one, where the source, the sink and the decoding are declared parameters, and the firmware never interprets a payload.**

The read direction of that is now the suite's design. Do not read it here; read it in the living docs: [embarch-study-designer](embarch-study-designer/decisions.md) decision 39 (the tap types), [embarch-core](embarch-core/decisions.md) decision 30 (storage, retention, the parameterised route), [embarch-dev-bench](embarch-dev-bench/decisions.md) decision 29 (the bench stops interpreting payloads; decision 22 superseded), [embarch-api](embarch-api/decisions.md) decision 39 (the tools), [embarch-ui](embarch-ui/decisions.md) decision 10, and reversals row 17.

**Five things the accepted half got wrong here, worth keeping because each is a shape rather than a detail:**

- **The schema bump this file wrote as 5 → 6 landed as 7 → 8**, because two unrelated decisions were implemented first and took the numbers. **A *derived* value recorded ahead of the work that derives it is a fact with a shelf life, unlike the decision it sits inside** (reversals row 18). It went stale twice more before the work shipped.
- **The firmware half cost +654 bytes, not the shrink this file assumed.** The bench's decoder never walked the span a seal over it has to cover, so sealing needed a full variant walker (row 25).
- **`DataChannel` did not collapse to one stream-named variant.** A stream-named source **carries no step index at all**, because a tap's scope is declared rather than per-step — this file kept the field alongside the new variant, **which would have asked authors for a field with no meaning.**
- **A per-study stream index turned out to be *required*** for the deprecated aliases to work at all, because the handler serving one holds no study. And **a text-encoded tap gets one file rather than two**, since its decode is the identity: this file's proposed triple over-counts by one for that case.
- **This file imagined reading a capture by naming it and said nothing about how a caller *learns* the names.** The listing tool that answers that turned out to be about `truncated` rather than the names — **a capture that lost data must not read as a whole one, and the three per-channel aliases structurally cannot say.**

**Still not built from the accepted half:** dev-bench's payload-interpretation deletion — the piece this proposal opened with, **and the only one that removes the `f32` interpretation sitting in shipped firmware.**

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

The per-repo action registry is deliberately enumerated-values-only — a registered action's payload is named fields each with a small set of engineer-supplied label/value pairs, with **no free-text entry, precisely so nobody uses a value whose meaning nothing recorded.** A shell command is free text, so this wants a free-text field kind, **and that is worth stating carefully rather than slipping in.**

**The line that rule actually draws is *who authored the bytes*, not *whether they were enumerated*.** Its own point is that this knowledge only ever comes from the engineer, explicit and unambiguous, and that the failure it exists to prevent is **this suite inferring what something does and presenting the inference as fact.** An engineer typing a command they know into a study they are authoring **is that knowledge arriving by the most direct route there is.**

**What stays forbidden is unchanged:** a value this suite generates, guesses, defaults, or labels with an invented description. **No "suggested commands", no parsing the DUT's source for a shell command table, no help text this crate writes about what a command does.**

## Left alone deliberately

**Monitor-everything looks foldable into N auto-armed taps** — discover, subscribe to everything, capture — **but its job is different: bounded reconnaissance whose result belongs *inline* beside the discovered GATT table**, answering "what does this DUT even emit?" **It is what you run *before* you know which characteristic deserves a tap, and its record ceiling is a feature for recon and a bug for capture.** Re-expressing it as taps is a plausible later simplification, not this change.

`serial_log` also stays as it is — dev-bench's link, an unrelated hop.

## Still open

- **The capacity constants** — how many taps per study, how long an expectation pattern may be, and the bench's buffer pool sizes. Needs the real link and real notification rates, **the same posture as every other hardware-unvalidated constant in these docs.** The bench's SRAM headroom is the binding check, and it is the first thing to measure: **the batch pool is shared across taps, not one buffer each.**
- **Whether richer matching than a substring is ever worth the firmware.** Resolved once as substring-only, on the grounds that **a richer check is already expressible post-hoc over the same stream, which is the cheap way to find out whether the real-time version is ever worth building.** Revisit only with a real case post-hoc validation genuinely cannot serve.
- **Whether the DUT premise holds at all.** Whether any specific DUT streams its console on subscribe, what it expects written, and what it prints back **is not established here, and by construction does not need to be** — the engineer names the characteristics, the command and the expected response. **The first real run against a real DUT is the validation, and it has not happened.**
- **Multi-value records for a genuinely multi-lead sensor** — the sample-grain question the shared crate already carries, unchanged. The declared layout is where it would eventually be expressed.
