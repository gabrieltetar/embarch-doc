# HIL notes: prior art

**Status:** draft, 2026-11-15.

A web survey made in review round 1, at the owner's request, of what exists before EmbArch claims anything as new ([00-goals.md](00-goals.md), G3). **Stars and dates are as the survey found them on 2026-11-15**; an item marked *unverified* was seen only in a search listing, not opened. Nothing here is decided; what the HIL design should take from it is under Open.

## Agent-driven HIL

**The bottom line: one project treats the integrity of agent-run hardware-test evidence as a design goal, about twenty others only drive hardware, and nothing combines signed, provenance-bound test evidence with verdicts the agent cannot write. No agent-driven USB PD work was found at all.**

| Item | What it is | What it does about trust | For EmbArch |
|---|---|---|---|
| **Agentic HIL** ([github.com/agentic-hil/agentic-hil](https://github.com/agentic-hil/agentic-hil), Apache-2.0, 26 stars, created 2026-06, near-daily releases) | An MCP server and pytest plugin: flash, reset, debug (OpenOCD, pyOCD, esptool), serial and CAN, YAML test plans with exact, pattern or range checks | **The closest prior art.** The authoritative config sits outside the agent's workspace; over MCP an agent can only narrow grants, never widen them; each report carries the digest of the config that permitted the action; a SHA-256 hash-chained audit, and a broken chain quarantines the bench; reports kept outside the workspace, the workspace copies "untrusted mirrors". **Signs nothing, does not stop the agent writing the test expectations, no instruments or measurement studies, no person gates a verdict** | Ideas and a threat-model reference; read its `docs/security-design.md` |
| **labgrid-mcp** ([github.com/onurcelep/labgrid-mcp](https://github.com/onurcelep/labgrid-mcp), Apache-2.0, 10 stars) | MCP over labgrid places: reserve, acquire, release | Flash, power and console off by default; MCP `readOnly` and `destructive` annotations on every tool; its author's blog argues for reservation at the network layer, "blast radius one reserved board". Keeps no evidence; "no human in the loop" | The tool-annotation pattern |
| **lab-instrument-mcps / labmcp-scpi** ([github.com/K-Dense-AI/lab-instrument-mcps](https://github.com/K-Dense-AI/lab-instrument-mcps), Apache-2.0, 31 stars) | Generic SCPI over VISA, socket or serial, a simulator per instrument | Read-only mode, write and query allow/deny lists, `apply_safe_state`, a command log; says itself "a denylist is a guard rail, not a guarantee", and a query such as `MEAS?` can turn an SMU's output on | A reference for Core's instruments |
| Debug-probe and device MCP servers (embedded-debugger-mcp, MIT, 218 stars; jlink-mcp; openocd-mcp; serial, sigrok, Zephyr and ESP servers) | Drive one tool each | Erase and memory write off unless configured, path allowlists, a call log at most | Nothing beyond what EmbArch has |
| Benchmarks: Embedded Arena (arXiv 2606.16190), IoT-SkillsBench (2603.19583), EmbedBench (2506.11003) and others | LLMs writing and deploying firmware | Nothing | Context only |
| Commercial: BootLoop Test, EmbeddedCI BenchPod, a scope vendor's MCP | Agent-generated HIL tests, instrument MCPs | Nothing on verdicts or evidence; safety is the client's approval prompt | None open source |

## Evidence against fabricated numbers

**Found in AI-scientist work, not in HIL, and it matches what review round 1 chose:**

- **AutoResearchClaw** ([arXiv 2605.20025](https://arxiv.org/abs/2605.20025), MIT, about 14.9k stars): every value a run produces goes into a registry the writing agent can read and not modify, tables are built from it, and **a checker re-extracts every number in the draft; an unmatched number in the results rejects the document.** EmbArch's numeric oracle lists instead of refusing ([02](02-study.md#the-report)).
- **EviBound** ([arXiv 2511.05524](https://arxiv.org/abs/2511.05524)): a claim propagates only with a queryable run ID, its artifacts and a finished status.
- **DREAMS**: each number cites the artifact behind it, and **an LLM judge re-checking them still passed between 1 and 7 of 83 fakes**, depending on the model: a checker must be deterministic, which the numeric oracle is.
- **Luo, Kasirzadeh and Shah** ([arXiv 2509.08713](https://arxiv.org/abs/2509.08713)): AI scientists select runs after the fact by score, and **only full trace logs expose it**: the case for listing every run ([06](06-report-and-publish.md#publish)).
- **"Compaction as Epistemic Failure"** ([arXiv 2607.13071](https://arxiv.org/abs/2607.13071)): **Claude Code's compaction turned a killed process's output into "confirmed results" in later sessions.** A reported number must come from a durable store, never from the chat's context: the case for `measurements.json`.
- **ImpossibleBench** ([arXiv 2510.20270](https://arxiv.org/abs/2510.20270), *unverified beyond summaries*): **agents edit or special-case tests to pass even when told not to**, and read-only or hidden tests cut it.

## An agent speaking for the person

**A known attack class with no settled fix**: "lies-in-the-loop" dialog forging (*unverified*, a vendor write-up), Loopjacking (arXiv 2609.21081, an approval applied to a changed operation) and Consent Integrity ([arXiv 2606.02668](https://arxiv.org/abs/2606.02668)). **Every proposed fix has three parts**: a trusted mediator renders the approval from the real action, the approval is bound to the exact action that runs, and it travels over a channel the agent cannot reach. **MCP's URL-mode elicitation** ([spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation)) is the protocol's primitive for that channel; which clients support it was not checked.

## Self-driving labs

**They reached the same split as EmbArch: the LLM plans, a deterministic runtime executes**, and hardware interlocks are the safety envelope, outside the agent: Lightfall (arXiv 2606.06711, on Bluesky's event model, BSD-3; every agent change a git commit under human review, the run's ID and tool calls to a logbook), RFIA (arXiv 2605.23636), Safe-SDL (arXiv 2602.15061), AEGIS (arXiv 2607.15620, which reports an uncertain case as low confidence, never as a verdict: EmbArch's `inconclusive`). **The cautionary case** (*unverified, secondary*): an automated lab's published verdicts corrected in 2026 for overclaiming, verdicts no person had checked.

## Attestation formats

- **in-toto's `test-result` predicate** ([spec](https://github.com/in-toto/attestation/blob/main/spec/predicates/test-result.md)): `result` (PASSED, WARNED, FAILED), `configuration`, `url`, the passed, warned and failed lists.
- **agent-governance-toolkit's offline receipts** ([tutorial](https://microsoft.github.io/agent-governance-toolkit/tutorials/33-offline-verifiable-receipts/), MIT): an Ed25519 signature per MCP tool call over an RFC 8785 canonical payload, chained by the parent's hash, exported as an in-toto statement, verified offline. **A key on the agent's own host proves little; it belongs with the service that touched the hardware**, which for EmbArch is Core.

## Classical HIL frameworks, formats and report tooling

**The bottom line: borrow the measurement model and the verdict roll-up, export to two interop formats, sign offline with standard envelopes, and build the PDF on the Typst crates. No open-source USB PD conformance or pre-compliance suite exists.**

| Item | What it has | For EmbArch |
|---|---|---|
| **OpenHTF** ([github.com/google/openhtf](https://github.com/google/openhtf), Apache-2.0, 731 stars, v1.6.3 2026-10) | A measurement is `name`, `units`, `dimensions`, `validators` (`in_range(min, max, marginal_min, marginal_max)`, `equals`, `matches_regex`, `within_percent`), `outcome`, `marginal`; a record carries `dut_id`, `station_id`, phases, attachments with hashes; operator input is a plug. **Its JSON record has no schema**; its proto export is better specified | **The measurement model to borrow** ([02](02-study.md#measurements)), with its *marginal* band, which is a guard band in all but name. Python, so not a dependency |
| **OCP Test & Validation output spec v2.0** ([github.com/opencomputeproject/ocp-diag-core](https://github.com/opencomputeproject/ocp-diag-core), MIT; Rust crate `ocptv`, MIT) | JSON Lines artifacts under JSON Schema 2020-12; a measurement `{name, value, unit, validators[]}`; **a two-axis outcome**, status (COMPLETE, ERROR, SKIP) × result (PASS, FAIL, NOT_APPLICABLE), so "nothing was tested" cannot read as a pass; `testRunStart` carries `parameters` | **The lossless export**: the six verdicts map onto its two axes, inconclusive and cancelled through its metadata. Quiet since 2024 |
| **OpenTAP** ([github.com/opentap/opentap](https://github.com/opentap/opentap), MPL-2.0, v9.34 2026-07) | Verdicts ordered by severity, NotSet < Pass < Inconclusive < Fail < Aborted < Error; a parent's verdict is its children's maximum; DUT and instrument `Close()` runs on abort; a lock-manager hook | **The roll-up order** for a run's summary line. C#, not a dependency |
| **labgrid** (LGPL-2.1+, v26.0.1 2026-10) | A strategy drives a board to a named state; a broken strategy skips the rest; reservations time out unless refreshed | The precedent for preconditions ([03](03-test.md#one-test)) and the lease |
| **LAVA** (GPL-2.0) | Device health (Good, Unknown, Bad, ...) set by a health-check job; test jobs run only on a healthy device; `--measurement` with `--units` | The precedent for the smoke check gating a bench |
| **JUnit XML** | "There is no official specification"; `<failure>`, `<error>`, `<skipped>`; no units or limits; the de-facto hardware CI format (Zephyr Twister, Robot, pytest) | **The CI summary export** |
| CTRF (draft 0.2), TAP 14 | No measurement structure | Skip |
| Robot Framework, HardPy (GPL-3.0), Zephyr Twister, pytest-embedded, tbot | Status vocabularies, operator dialogs, numeric measurements with limits, hardware maps, a power harness | Concepts only; nothing EmbArch lacks after round 1 |
| **DSSE** ([github.com/secure-systems-lab/dsse](https://github.com/secure-systems-lab/dsse), Apache-2.0) around an **in-toto Statement** | A local signed envelope `{payload, payloadType, signatures[]}`; the in-toto `test-result/v0.1` predicate (PASSED, WARNED, FAILED, the test lists, `configuration` as resource descriptors); SLSA provenance's `externalParameters` and `resolvedDependencies` | **Signing records offline**, no transparency log: the subject is a manifest's SHA-256, the predicate EmbArch's own with `test-result` as the portable summary. The Rust `sigstore` and `in-toto` crates call themselves experimental and beta, so DSSE plus Ed25519 in-house is the smaller dependency; `cosign verify-blob` can check the result |
| **Typst as a library** (`typst`, `typst-pdf`, `typst-kit` 0.15.1, Apache-2.0; `typst-as-lib` 0.17, MIT) | Fonts embedded through `typst-assets` (about 9.9 MB raw); a local package root for vendored packages, so the registry is never contacted; `PdfOptions.ident` and `timestamp` for stable re-renders; PDF/A-3 allows embedded files | **The PDF stack** ([06](06-report-and-publish.md#the-report)); plot packages **lilaq (MIT)** and cetz (LGPL-3.0, whose terms need checking when its source ships inside a binary). Binary size unmeasured |
| **ISO/IEC 17025:2017 and ILAC-G8:09/2019** (read through ILAC-G8, which quotes 17025) | A decision rule says how measurement uncertainty is accounted for when stating conformity, agreed before measuring; a statement of conformity names the results, the specification parts met or not, and the rule. Guard band: acceptance limit = tolerance limit − w; simple acceptance (w = 0) risks up to 50 % false accept at the limit, w = U under 2.5 %; a non-binary rule gives pass, conditional pass, conditional fail, fail | **Each limit carries an uncertainty and a decision rule**, and a result inside a guard band needs a verdict ([03](03-test.md#the-verdict)) |
| **USB-IF certification** (public pages only) | Certification only at a compliance workshop or an authorised test lab; only certified products are listed and may use the logo; a PD product's capabilities are declared in a **VIF** (Vendor Info File, XML), and **Zephyr's `scripts/generate_usb_vif` builds one from the devicetree** | The report's "pre-compliance, not a certification" sentence ([03](03-test.md#the-report)) is the survey's inference from these pages, not a quoted rule. **A VIF is the industry's capability declaration**, a source for the DUT's capabilities |
| Open-source PD capture: sigrok's `usb_power_delivery` decoder (GPL-2.0+), Twinkie and its redesign Twonkie, `km003c-rs` (Apache-2.0) | CC decoding, sniffing, packet injection | A possible independent witness of PD traffic, later |

## What is new in EmbArch

**Measured against the survey, nothing found combines** verdicts decided by code from named measurements with engineer-confirmed inputs, a deterministic check of every number in an agent's prose, every attempt listed, and a report a third party can verify offline from raw captures, **for agent-run HIL measurement and conformance**. The closest, Agentic HIL, has the audit chain and the authority outside the workspace, and none of the rest. **No agent-driven USB PD work exists.** The claim is safe to make in those words, and no wider.

## Open

Recommended takes from the survey, unanswered unless marked:

- **Prevention against a subverting agent**, the owner's answer of round 1 ("plan for prevention"), is designed in [12-prevention.md](12-prevention.md), on Agentic HIL's authority-outside-the-workspace, the approval-integrity papers' out-of-band channel, and DSSE with Ed25519.
- **A guard band's verdict**: what a result between the tolerance limit and the acceptance limit gets.
- **The interop exports**: JUnit XML as the CI summary, OCP T&V v2.0 JSON Lines as the lossless one, both written into the zip.
- **The VIF as a capability source**, beside the atlas's decoding and the engineer's declaration.
- **Re-renders**: whether `typst-pdf` output is byte-identical across machines and patch versions, to measure before `verify` compares PDFs rather than only the data.
