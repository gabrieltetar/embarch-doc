# Proposal: HIL evidence an agent cannot forge — Core-signed records, the agent in a boundary, and the open-source pieces they use

**Status:** proposal, 2026-11-15.

Spans `embarch-core`, `embarch-api`, `embarch-study-designer`, `embarch-ui`, `embarch-umbrella`, `embarch-chat` and this repo, which is why it sits at the root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). **The companion of [embarch-hil-proposal.md](embarch-hil-proposal.md)**: that one designs what an agent runs on a bench; this one designs **why a reader can believe what it reports, against an agent that deliberately subverts it**, and which existing open-source pieces it is built from. The research and every answer behind it are in [notes/hil/](notes/hil/README.md): the trust model ([09](notes/hil/09-trust-model.md)), the prior-art survey ([11](notes/hil/11-prior-art.md)) and the prevention design ([12](notes/hil/12-prevention.md)), gathered with the owner on 2026-11-15.

## Why

**The owner's call, review round 1: "plan for prevention. EmbArch is an HIL LLM tool mainly, we should know this type of issue very well."** An agent in a Claude Code session runs as the engineer's OS user: it can read Core's token, edit everything under `embarch/`, rewrite the user-owned UI and API binaries, edit Claude Code's own permission files, and flash firmware it wrote ([the adversary](notes/hil/12-prevention.md#the-adversary)). **Every check that lives in the engineer's account is therefore a check the agent can undo.**

**The survey found nothing that closes this** ([11](notes/hil/11-prior-art.md#what-is-new-in-embarch)): about twenty embedded MCP servers only drive hardware, and the one project that keeps authority outside the agent's workspace (Agentic HIL) signs nothing and has no measurements. Fabricated numbers, verdict ownership, cherry-picked runs and an agent speaking for the person are each documented failures ([11](notes/hil/11-prior-art.md#evidence-against-fabricated-numbers)).

## What it adopts

| Piece | Licence | Used for | As |
|---|---|---|---|
| **DSSE** envelope | Apache-2.0 | Signing Core's records and a zip's manifest, offline | Format, written in-house (small) |
| **in-toto Statement**, `test-result/v0.1` predicate | Apache-2.0 | The signed record's shape: subjects are file hashes; a custom predicate carries the verdicts, `test-result` the portable summary | Format |
| **Ed25519** (`ed25519-dalek`, from memory) | BSD-3-Clause, to confirm | Core's signing key | Dependency |
| **Claude Code's dev container** and its Dev Container Feature | To confirm | The agent's boundary, with a default-deny firewall | Reference setup |
| **WebAuthn** (`webauthn-rs`, from memory) | MPL-2.0, to confirm | One passkey touch per run, for an engineer who cannot run the agent in a container | Dependency, later |
| **OCP Test & Validation v2.0** (`ocptv` crate) | MIT | The structured export of a run | Format, dependency to evaluate |
| **JUnit XML** | No formal spec | The CI summary export | Format |
| **Typst** crates, `typst-as-lib`, **lilaq** | Apache-2.0, MIT, MIT | The PDF, rendered offline | Dependencies |
| OpenHTF's measurement model, OpenTAP's verdict order, ILAC-G8's guard bands, Agentic HIL's authority outside the workspace, Consent Integrity's mediator | — | Concepts | Ideas |

## The design in one screen

- **Core is the root of trust, under its own OS account** (decided): its binary where the engineer's account cannot write, and **a protected store** only Core's account reads or writes: its signing key, the run log, the confirmations, any registered passkey and, attested, the identity store. **A Core not installed from a signed release is unattested**, and its reports say so ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)). **An attested Core is installed only from a signed release artifact** (review round 3).
- **Scoped tokens**: an **agent** scope (hardware within the lease, runs, reads) and a **person** scope (the person's acts, and the identity routes that say which board, probe, instrument or signal is which); **no route that speaks for the person, declares an identity, or rewrites evidence accepts the agent's token** (unattested: identity routes excepted), and **whether an act was relayed is decided by the scope, never by a field the caller writes**, which amends embarch-core decision 105 (review round 2).
- **Two ways to use it**: **unattested**, Core in any account, every rule applied and every report saying so, enough for development runs; **attested**, Core under its own account plus the container or the passkey, for the run for record a client relies on (review rounds 2, 4).
- **The agent runs in a dev container on every OS**, set up by `embarch init` (decided): the repo, the toolchain and the agent's token inside; **a firewall allowing Core's port and the model's API only**, embarch-ui's port above all, set before the agent starts and out of its reach; the person's token never mounted; the agent's own clone waits for the standalone pass (owner, 2026-11-19). The boundary holds only while the agent's code is built and run inside it, and the guide says so (review round 2). **It works on every topology**: Core owns every probe and port, so no USB is passed through.
- **The person's acts** (a confirmation of a verdict-deciding input, the go of a Test run or of a host study with a prompt, an observation or clearance prompt's answer) **are made on a card in the UI, or the CLI in the person's own terminal, with the person's token** (decided). **The card escapes every string the agent wrote and takes an act only with a nonce Core issued.** **Where the agent cannot be put in a container, a passkey touch signs them**, since the agent can read the person's token there (its details deferred). **Every report says which held, as Core saw it: person-scoped token, passkey, or agent-scoped only** (review round 2).
- **Core signs what it measured**: when a test or a study ends, an in-toto Statement in a DSSE envelope over the SHA-256 of every capture, `events.json`, `measurements.json` and `run.json`, its predicate the verdicts, every image readback and identity, Core's build and the crate's behaviour versions, **with the build's commit and dirty state carried apart, as claims**. **Measurements and verdicts are computed by Core** through the shared crate, so none can be rewritten without breaking the signature.
- **Core keeps a hash-chained run log**, one entry per run with its manifest's hash once published, never swept; **"every run of this test on this unit" is read from it**, and the repo's ledger rows become its mirror, losing any disagreement. **Core logs every call to it in a chain of its own**, from Live on; the repo's live log becomes a mirror. **The zip carries the unit's segment of the run log and the run's of the call log**, so the list of runs is checked, not trusted; a full store fails closed once attested (review rounds 3, 4).
- **Core signs each Test run's record** (its selection, every test's status) **and, at publish, `report-data.json`**, every non-prose claim of the report; the PDF, the exports and `report.typ` rest on `verify` (review round 3).
- **Core takes firmware only as bytes**, uploaded or from a staging folder it owns, never from a path to a file its account reads (review round 3).
- **Confirmations bind hashes and are kept by Core** (decided). **Core re-expands `run.json` from the confirmed definitions and its own copy of the premade suite, refuses a run that rests on an unconfirmed input, and starts a Test only after a go bound to the run, its hash, a nonce and an expiry, used once** (review round 2).
- **Prompts declare their kind** (decided): Core refuses a relayed answer to an observation or a clearance prompt.
- **No hardware call but the run's own while a run is in flight**, Live reads included (decided).
- **Publish**: the zip carries JUnit XML and OCP T&V JSON Lines beside the PDF (decided); Core signs the zip's manifest. **`verify` checks Core's signatures against a key fingerprint from Core's elevated install, got from the engineer out of band**, then recomputes every measurement and verdict with the behaviour versions the records name, and checks every number in the PDF against the signed measurements (review round 2), **and runs the rest of [06's checks](notes/hil/06-report-and-publish.md#verify)** (review round 3; pictures checked at their source).

**What stays outside, and is said so** ([12](notes/hil/12-prevention.md#what-stays-outside-prevention-and-is-said-so)): the DUT's own word (every measurement is marked `bench`, `dut` or `person`, and that mark is the rule); the hardware outside a run, within the lease; the person's judgement; the browser; an engineer who runs an unattested Core.

## The work, by sub-project

| Sub-project | Work |
|---|---|
| `embarch-core` | Its own account and protected store; an elevated update path; key generation and the first passkey in the elevated install; scoped tokens, identity routes in the person's scope; the DSSE signing of each test's and study's record and of a zip's manifest; the hash-chained run log and call log; confirmations bound to hashes, each definition the agent submits kept by its hash, and the refusal of a run on an unconfirmed input; the go, a host study's included; prompt kinds; refusing other hardware calls during a run; the run record, `report-data.json` and both logs' segments; a route returning a publish's entry and the log head; firmware taken as bytes only, [decisions 10, 18](embarch-core/decisions/flashing.md) amended; the call log failing closed; installs only from a signed release; a fixed-frame challenge; outputs off at every stop and start; exclusive port handles under a lease; the identity store protected, [decision 53](embarch-core/decisions/auth.md) and [spec](embarch-core/spec.md) §3's `start` and `stop` amended; later, the passkey check |
| `embarch-topology` | The CLI refusing hardware under a service's lease or run, and refusing the identity store; [decision 23](embarch-topology/decisions/storage.md) amended |
| `embarch-study-designer` | A prompt's kind, and an action prompt's confirming measurement; a measurement's `by` |
| `embarch-api` | The agent scope, so **the identity tools ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)) leave the MCP surface for the CLI with the person's token** on an attested Core; `verify` checking signatures against a fingerprint from an elevated install, rescanning `report.typ` and the prose, and the checks of [06](notes/hil/06-report-and-publish.md#verify); the JUnit and OCP T&V exports with every qualifier; `run_test` preparing, never starting; the ledger and live log as mirrors of Core's logs |
| `embarch-ui` | The card, rendering a run's pending acts from Core's record, escaping the agent's strings, with the person's token and Core's nonce; later, the passkey touch. **Decision 90 amended**: Make live's declarations and enrolments go with the person's token |
| `embarch-umbrella` | Core's own account on Linux and macOS, and the install target's ACL; signed releases ([proposal](embarch-release-signing-proposal.md)); Core's copy of the premade suites in its store; the dev container scaffold, **kept outside the repo** (its definition, the firewall's allow list per topology, the toolchain image, the agent's token, the agent's own clone, no host forwards); the engineer's statement of where the agent runs; the key's fingerprint shown at setup and written to each registered repo's `embarch/core-fingerprint`; `deploy-core` installing a development Core beside the service, started and stopped without elevation in the container setup only ([decision 32](embarch-umbrella/decisions/deploy.md), dev workflow §4a) |
| `embarch-chat` | Starting `claude` inside the container |
| `embarch-doc` | The HIL guide's trust section; [agent-guide.md](suite/agent-guide.md) §1.1 without the identity tools, which become the person's on an attested Core; [Core decision 93](embarch-core/decisions/lease.md)'s gate amended for two scopes; [embarch-token.md](embarch-token.md)'s threat model rewritten for two scopes; [the user guide](suite/user-guide.md)'s setup, where Core's own account and the container add elevated steps; [embarch-core decision 105](embarch-core/decisions/host-prompt.md) and [embarch-ui decision 90](embarch-ui/decisions/bench-live.md), each amended; [embarch.md](embarch.md) §5's "no permission model" and "no special path", for the two scopes |

## Order

Dated items are the owner's; the rest recommended:

1. **Signing, the run log and scoped tokens**, with Study publish: the first zip signed and unattested (owner, 2026-11-19, 2026-11-20).
2. **The card, confirmations bound to hashes, and the go**, with the Test route.
3. **Core's own account and store with the identity store, signed-release installs, the development Core**: the attested phase, later (owner, 2026-11-19).
4. **The dev container scaffold**, in the owner's standalone pass.
5. **The passkey alternative.**

## Open questions

- **Deferred** ([12](notes/hil/12-prevention.md#open)): the passkey's details, to its phase; the agent's own clone and the boundary's details (a build's artifact reaching Core, the toolchain image, the firewall per topology), to the standalone pass.
- **Unverified**: WebAuthn on a page at `http://127.0.0.1`; whether WSL can reach a Windows service account's store; the licences marked "to confirm"; whether `typst-pdf` renders byte-identically across machines.
- **Key rotation, a lost key or passkey, a second engineer**: each a person's act.

**Fold:** each phase moves its part into the owning sub-project's docs as it is accepted and deletes it here. This file is deleted once nothing in it is still proposed.
