# HIL notes: the trust model

**Status:** draft, 2026-11-15.

Written in review round 1 ([10-review.md](10-review.md)). **The owner answered every row of "What goes wrong" in that round** (2026-11-15); the rows say where each answer landed. **"The claim" opens the guide and the proposal** (owner, review round 1). "What already holds" is found in the suite's docs and cites them.

## Why this file exists

Files 01 to 08 design the mechanisms: three modes, a lease, verdicts decided by code, a report with an audit appendix. **None of them states the problem the mechanisms solve**, so nothing says whether they are enough, and an engineer deciding whether to let an agent near their bench has nothing to check them against. This file states it.

**An engineer lets an agent run hardware only if three things hold:**

1. **It does to the hardware only what the engineer allowed**, and the engineer can see what that is.
2. **What it reports is true.**
3. **Whoever reads the report later** — a colleague, a client, an auditor — **can check point 2 without trusting the agent.**

Point 3 is the one that decides whether EmbArch's output is worth anything outside the session that produced it. A test report is evidence, and evidence that rests on an LLM having told the truth is not evidence.

## The claim

Two sentences the guide and the proposal open with, and the design is held to (owner, review round 1):

- **No number, verdict or identity in a published report depends on the agent having told the truth; every sentence the agent wrote is labelled as its own.**
- **The agent does to the hardware only what the engineer allowed: a study or a test written in a file the engineer can read before it runs, and shown in a preview before a Test starts, or a Live action on the free list; every call is logged.** Hardware safety is an authoring concern, not a runtime limit (owner, review round 1): no envelope is enforced at execution. That is weaker than an enforced limit, by the owner's choice, and the guide says so.

**The agent is outside the evidence chain.** The chain is stimulus → measurement → record → verdict → report, and each link is produced by versioned code (Core, embarch-api, the bench firmware) or attested by a named person. The agent plans, authors, operates and interprets; it produces no link. A test of the claim: **the published zip would be byte-for-byte the same if a person had made the same tool calls**, apart from the prose labelled as the agent's.

This is the atlas's own rule carried to the bench. The atlas makes **the text layer the numeric oracle** — every number an LLM writes must be found on the page it cites, or be tagged (`embarch-atlas` repo, `DESIGN.md`, "Principles" 2) — and lists what an LLM step may and may not do ("What an LLM step may and may not do"). **Here, the run's files are the numeric oracle.**

## What the agent does, and does not

| The agent may | The agent never |
|---|---|
| **Plan**: pick the mode, select tests, propose a run and show it before it starts | Decide a verdict |
| **Author**: a study and the measurements it declares, a custom test, `report.typ` — each a file a person can read, hashed into the run | Widen what the engineer declared: a limit, an applicability input, a hook mapping |
| **Operate**: tool calls, inside the lease | Answer an operator prompt, enter a verdict or write the operator's notes, on its own |
| **Interpret**: prose, labelled as the agent's | Choose which runs of a test the reader sees |
| **Diagnose**: on a failure, propose causes and fixes; a fix is a new image and a new run, and both stay in the history | Edit a test so that a run passes |

## What goes wrong when an agent drives a bench

Each row is a failure an LLM at a bench is prone to, what stops it as answered in review round 1, and **which layer enforces that**:

- **Core**: refuses, whoever calls.
- **embarch-api**: refuses or records, for the MCP server and the CLI alike.
- **Bench firmware**: refuses at the hardware, whatever Core sent.
- **Harness**: a Claude Code permission that asks. The engineer's own setting, and it can be loosened; **against an agent that subverts, it is nothing**, since its files are the agent's to edit ([12](12-prevention.md#the-adversary)).
- **Boundary**: the agent's dev container, which keeps the person's token, embarch-ui and every user-owned file out of its reach ([12](12-prevention.md#a-persons-act-what-a-ui-card-can-prove-and-what-it-cannot)).
- **Procedure**: the guide tells the agent; nothing checks.

| # | What goes wrong | On a bench | What stops it | Layer | Where |
|---|---|---|---|---|---|
| F1 | A number in the report that the run never produced | The agent writes "sustained 1,180 B/s" from an earlier run it remembers | Every number is a **measurement** computed by built-in code from the run's files; prose cites measurements by name, and a number in prose that matches none is listed in the appendix | embarch-api, at publish | [02](02-study.md#measurements) |
| F2 | The agent bends the test until it passes | Widens a limit, edits a custom test, marks a requirement not applicable, reruns until a pass and publishes that one | Verdict-deciding inputs are **confirmed by the engineer**; the report lists **every run** of the test on that unit, from Core's run log, grouped by image and definition; a test copied from a premade one shows its diff; the guide forbids editing a test to pass | embarch-api; procedure for the last | [03](03-test.md#the-duts-inputs), [06](06-report-and-publish.md#publish) |
| F3 | An action damages the DUT, the bench or the person | An agent-written host study sets the load to 5 A on a 3 A port; a shell command erases a calibration partition; a prompt asks a person to re-cable a live 20 V bus | **Authoring**: what a study puts on the DUT is checked against its ratings when written; the Test preview shows it before the go. A runtime envelope and a list of DUT shell commands that ask were both declined | The engineer's review; harness asks on `run_host_study` | [03](03-test.md#benches), [05](05-live.md#reach-and-permission) |
| F4 | The run measured something other than what the report names | The board was reflashed by hand after the build; the tree was dirty; another unit was plugged in on bench B | The identity gate per bench; the same-unit check; **the image read back through the probe** before each bench, bench boards' images included; the commit and dirty state recorded **as the build's claim**, apart from what Core observed | Core | [03](03-test.md#a-run), [06](06-report-and-publish.md#the-audit-appendix) |
| F5 | Incomplete evidence read as complete | A truncated capture, a reply cut at 4,096 bytes, a dropped-record gap | A verdict resting on incomplete evidence is **inconclusive**, never a pass | Core, embarch-api | [03](03-test.md#the-verdict) |
| F6 | The agent speaks for the person | It answers a prompt, enters a verdict by hand, confirms its own limit, gives the go | **Confirmations and the go on a card the agent cannot reach** (its container, or a passkey touch); **an observation or clearance prompt refuses a relayed answer**; every surface recorded. A manual verdict stays reachable over MCP (owner) | Boundary, Core | [12](12-prevention.md#a-persons-act-what-a-ui-card-can-prove-and-what-it-cannot), [03](03-test.md#a-run) |
| F7 | A bench fault blamed on the DUT | A cable falls out; the partner's port is lost; the load does not acknowledge | **Error** is a verdict apart from **fail**: a step on a bench board or an instrument that fails is the setup's, not the DUT's; an error ends its bench, a fail only its test; the smoke check | Core | [03](03-test.md#the-verdict) |
| F8 | Data too large for the agent's context, misread | It reads 200 lines of a 32 MiB capture and generalises | The agent concludes from `measurements.json` and stream summaries, never from a raw capture | Procedure, on measurements computed by code | [02](02-study.md#how-a-study-runs-as-the-procedure-would-say-it) |
| F9 | An inference about the DUT presented as fact | It reads the source, decides the DUT cannot PR_Swap, and the swap tests drop out as not applicable | Every DUT input carries its **provenance** (measured, decoded, confirmed, declared); an agent's proposal is not used until confirmed; a measurable capability is checked on the wire | embarch-api | [03](03-test.md#the-duts-inputs) |
| F10 | The run cannot be reproduced or checked | The test plan was an untracked file since edited; a reader cannot rederive a verdict | **`run.json`**, hashed, kept by Core and in the zip; definition files pinned by hash; publishes never overwritten; `verify <zip>` recomputes every measurement and verdict from the raw captures | embarch-api | [03](03-test.md#selecting-and-rerunning), [06](06-report-and-publish.md#verify) |
| F11 | Hardware driven with nobody there | A fleet leg starts a run at 3 a.m. | Interactive sessions only | Procedure | [01](01-modes.md#who-may-run-them); [CLAUDE.md](../../CLAUDE.md), "Parallel agent work" |

**The rule the table follows: a guarantee that protects the evidence is enforced by code, held by Core under its own account**, and the harness and the procedure are a second line, never the only one. **The table assumes an agent that errs; [12-prevention.md](12-prevention.md) holds it against one that subverts** (owner: "plan for prevention"). **Hardware safety is the owner's exception** (F3): it rests on authoring and the engineer's review. **The guide lists every rule that is procedure-only, as such** (owner, review round 1), so an engineer knows exactly which ones rest on the agent behaving: today F2's last clause (never edit a test to pass), F6's relayed setup and action answers being the person's true words, F8 and F11. An observation's or a clearance's answer is not among them: Core refuses one that comes with the agent's token ([12](12-prevention.md#operator-prompts-by-kind)).

## What already holds

Found in the suite's docs; each is a mechanism the claim stands on, and each says how far it is verified.

- **Board identity**: an enrolled board is checked by hardware ID before use (`validate`; [embarch-topology spec](../../embarch-topology/spec.md)).
- **The lease**: every other session's hardware call is refused `409`, naming holder and purpose ([lease tools](../../embarch-api/interfaces/tools-lease.md)).
- **Teardown on every way out** of a host study, ignoring cancel; proven over a fake port only ([Core decision 95](../../embarch-core/decisions/host-study.md)).
- **An unacknowledged instrument set fails the step**: a load that never switched is not measured as if it had ([Core decision 104](../../embarch-core/decisions/instruments.md)); not run against an instrument.
- **Truncation is reported per capture** ([studies guide §1](../../suite/studies-guide.md)); a reply over 4,096 bytes sets `reply_truncated` (Core 95).
- **An override is written into the result** (`--allow-version-mismatch`), and **EmbArch never runs `git checkout`** ([studies guide §2](../../suite/studies-guide.md)).
- **A prompt answer names its prompt id**, is taken once, and records `answered_by` (`ui`, `mcp`, `cli`) ([Core decision 105](../../embarch-core/decisions/host-prompt.md)).
- **The bench's version is a measurement; the DUT's is a claim** ([studies guide §2](../../suite/studies-guide.md)). The atlas's `image_check` compares 16 words at three places of the image through the probe before it names a symbol (`embarch-atlas` repo, `DESIGN.md`, "Live").
- **The atlas refuses a read-to-clear register by name and a read on the wrong chip** (same section).
- **The ledger's rows are append-only** ([embarch-api decision 98](../../embarch-api/decisions/ledger.md)); not yet verified on a bench.

## Prior art

**From memory, not checked online in this round.** Each borrows a piece; **none models an agent as the operator**, which is the part EmbArch adds.

- **OpenHTF**: measurements as named values with units and validators; outcomes that separate a failed DUT from an error in the station.
- **LabGrid**: strategies that drive a board to a known state before a test; reservations, which the lease already is.
- **LAVA**: a health check of the device before a job, which the smoke check is.
- **NI TestStand**: a step status vocabulary (passed, failed, error, skipped, terminated) and limits with units on every numeric step.
- **ISO/IEC 17025:2017**: a statement of conformity states its decision rule; a measurement is traceable to a calibration; a record carries enough to repeat the test.

## Open

- **Prior art**: "Prior art" above was written from memory; the web survey is [11-prior-art.md](11-prior-art.md).
- **Against a deliberately subverting agent**, the owner asks for prevention, not only detection: [12-prevention.md](12-prevention.md). The layers above assume the agent errs; that note moves the evidence and the person's acts out of its reach.
