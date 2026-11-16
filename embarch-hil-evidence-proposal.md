# Proposal: HIL evidence an agent cannot forge — Core-signed records, the agent in a boundary, and the open-source pieces they use

**Status:** proposal, 2026-11-15.

Spans `embarch-core`, `embarch-api`, `embarch-study-designer`, `embarch-ui`, `embarch-umbrella`, `embarch-chat` and this repo, which is why it sits at the root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). **The companion of [embarch-hil-proposal.md](embarch-hil-proposal.md)**: that one designs what an agent runs on a bench; this one designs **why a reader can believe what it reports, against an agent that deliberately subverts it**, and which existing open-source pieces it is built from. The research and every answer behind it are in [notes/hil/](notes/hil/README.md): the trust model ([09](notes/hil/09-trust-model.md)), the prior-art survey ([11](notes/hil/11-prior-art.md)) and the prevention design ([12](notes/hil/12-prevention.md)), gathered with the owner on 2026-11-15.

## Why

**The owner's call, review round 1: "plan for prevention. EmbArch is an HIL LLM tool mainly, we should know this type of issue very well."** An agent in a Claude Code session runs as the engineer's OS user: it can read Core's token, edit everything under `embarch/`, rewrite the user-owned UI and API binaries, edit Claude Code's own permission files, and flash firmware it wrote ([the adversary](notes/hil/12-prevention.md#the-adversary)). **Every check that lives in the engineer's account is therefore a check the agent can undo.**

**The survey found nothing that closes this** ([11](notes/hil/11-prior-art.md#what-is-new-in-embarch)): about twenty embedded MCP servers only drive hardware, the one project that keeps authority outside the agent's workspace (Agentic HIL, Apache-2.0) signs nothing and has no measurements, and no agent-driven USB PD work exists. Fabricated numbers, verdict ownership, cherry-picked runs and an agent speaking for the person are each documented failures ([11](notes/hil/11-prior-art.md#evidence-against-fabricated-numbers)).

## What it adopts

| Piece | Licence | Used for | As |
|---|---|---|---|
| **DSSE** envelope | Apache-2.0 | Signing Core's records and a zip's manifest, offline | Format, written in-house (small) |
| **in-toto Statement**, `test-result/v0.1` predicate | Apache-2.0 | The signed record's shape: subjects are file hashes; a custom predicate carries the verdicts, `test-result` the portable summary | Format |
| **Ed25519** (`ed25519-dalek`, from memory) | BSD-3-Clause, to confirm | Core's signing key | Dependency |
| **Claude Code's dev container** and its Dev Container Feature | To confirm | The agent's boundary, with a default-deny firewall | Reference setup |
| **WebAuthn** (`webauthn-rs`, from memory) | MPL-2.0, to confirm | One passkey touch per run, for an engineer who cannot run the agent in a container | Dependency, later |
| **OCP Test & Validation v2.0** (`ocptv` crate) | MIT | The lossless export of a run | Format, dependency to evaluate |
| **JUnit XML** | No formal spec | The CI summary export | Format |
| **Typst** crates, `typst-as-lib`, **lilaq** | Apache-2.0, MIT, MIT | The PDF, rendered offline; cetz (LGPL-3.0) avoided | Dependencies |
| OpenHTF's measurement model, OpenTAP's verdict order, ILAC-G8's guard bands, Agentic HIL's authority outside the workspace, Consent Integrity's mediator | — | Concepts | Ideas |

## The design in one screen

- **Core is the root of trust, under its own OS account** (decided): its binary where the engineer's account cannot write, and **a protected store** only Core's account reads or writes: its signing key, the run log, the confirmations, any registered passkey. **A Core run under the engineer's own account is unattested**, and every report from it says so on its first page ([12](notes/hil/12-prevention.md#the-root-of-trust-core-under-its-own-account)).
- **Scoped tokens**: an **agent** scope (hardware within the lease, runs, reads) and a **person** scope (the person's acts); **no route that speaks for the person, or rewrites evidence, accepts the agent's token.**
- **The agent runs in a dev container on every OS**, set up by `embarch init` (decided): the repo, the toolchain and the agent's token inside; **a firewall allowing Core's port and the model's API only**, embarch-ui's port above all; the person's token never mounted. **It works on every topology because the agent needs no hardware**: Core owns every probe and port, so no USB is passed through ([the table](notes/hil/12-prevention.md#a-persons-act-what-a-ui-card-can-prove-and-what-it-cannot)).
- **The person's acts** (a confirmation of a verdict-deciding input, the go of a Test run, an observation or clearance prompt's answer) **are made on a card in the UI, or the CLI in the person's own terminal, with the person's token** (decided). **Where the agent cannot be put in a container, one passkey touch per run** signs the card's list instead. **Every report says which held: boundary, passkey, or neither.**
- **Core signs what it measured**: when a test or a study ends, an in-toto Statement in a DSSE envelope over the SHA-256 of every capture, `events.json`, `measurements.json` and `run.json`, its predicate the verdicts, the image readback, the unit and bench identities and Core's build. **Measurements and verdicts are computed by Core** through the shared crate, so none can be rewritten without breaking the signature.
- **Core keeps a hash-chained run log**, one entry per run, never swept; **"every run of this test on this image" is read from it**, and the repo's ledger rows become its mirror. **Core logs every hardware call in the same chain**, Live included; the repo's live log becomes a mirror.
- **Confirmations bind hashes and are kept by Core** (decided); **Core refuses a run that rests on an unconfirmed input, and starts a Test only after a go for that `run.json`'s hash.**
- **Prompts declare their kind** (decided): Core refuses a relayed answer to an observation or a clearance prompt.
- **No hardware call but the run's own while a run is in flight**, Live reads included (decided).
- **Publish**: Core signs the zip's manifest; the zip carries JUnit XML and OCP T&V JSON Lines beside the PDF (decided). **`verify` checks Core's signature against the key fingerprint the engineer pinned and hands a client**, then recomputes every measurement and verdict.

**What stays outside, and is said so** ([12](notes/hil/12-prevention.md#what-stays-outside-prevention-and-is-said-so)): the DUT's own word (every measurement is marked `bench`, `dut` or `person`, and that mark is the rule); the hardware outside a run, within the lease; the person's judgement of what the card shows; the browser; an engineer who runs an unattested Core.

## The work, by sub-project

| Sub-project | Work |
|---|---|
| `embarch-core` | Its own account and protected store; key generation; scoped tokens; the DSSE signing of each test's and study's record and of a zip's manifest; the hash-chained run log and call log; confirmations bound to hashes and the refusal of a run on an unconfirmed input; the go; prompt kinds; refusing other hardware calls during a run; later, the passkey check |
| `embarch-study-designer` | A prompt's kind, and an action prompt's confirming measurement; a measurement's `by` |
| `embarch-api` | The agent scope; `verify` checking signatures against a pinned fingerprint; the JUnit and OCP T&V exports; the ledger and live log as mirrors of Core's logs |
| `embarch-ui` | The card, rendering a run's pending acts from Core's record, with the person's token; later, the passkey touch |
| `embarch-umbrella` | Core's own account on Linux and macOS; the dev container scaffold (`devcontainer.json`, the firewall's allow list per topology, the toolchain image, the agent's token); the key's fingerprint shown at setup |
| `embarch-chat` | Starting `claude` inside the container |
| `embarch-doc` | The HIL guide's trust section; [embarch-token.md](embarch-token.md)'s threat model, which today excludes anyone with access to the machine, rewritten for two scopes |

## Order

Recommended, not answered:

1. **Scoped tokens, Core's own account and its protected store**: the foundation every other piece rests on.
2. **Signing and the run log**, landing with the HIL proposal's Study publish, so the first published zip is already signed.
3. **The card, confirmations bound to hashes, and the go**, with the Test route.
4. **The dev container scaffold**, in the standalone pass the owner plans once the design is close to finished.
5. **The passkey alternative.**

## Open questions

- **Items "Core signs", "run log", "call log" and "Publish" above** are recommended and follow from the owner's answers; not yet answered one by one.
- **The boundary's details** ([12](notes/hil/12-prevention.md#open)): how a build's artifact reaches Core from inside the container, the toolchain image, the firewall's allow list on each topology.
- **Unverified**: WebAuthn on a page at `http://127.0.0.1`; whether WSL can reach a Windows service account's store; the licences marked "to confirm"; whether `typst-pdf` renders byte-identically across machines.
- **Key rotation, a lost key or passkey, a second engineer**: each a person's act.

**Fold:** each phase moves its part into the owning sub-project's docs as it is accepted and deletes it here. This file is deleted once nothing in it is still proposed.
