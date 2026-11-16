# HIL notes: prevention against a subverting agent

**Status:** draft, 2026-11-15.

**The owner's answer, review round 1:** "Aim for prevention, I would even say plan for prevention. EmbArch is an HIL LLM tool mainly, we should know this type of issue very well and plan for it." So the trust model ([09](09-trust-model.md)) is held against **an agent that deliberately subverts it**, not only one that errs or chases the wrong goal. **Decided in round 1** (owner): **Core as the root of trust, under its own OS account; the agent in a dev container; the person's acts by a card the agent cannot reach, or a passkey touch where it can; prompts by kind; no hardware call but the run's own during a run; every measurement marked by who measured it.** What Core signs and logs (items 1 to 7 below) is recommended and follows from those; the remaining forks are under Open. It builds on the prior art ([11](11-prior-art.md)): Agentic HIL's authority outside the agent's workspace, the approval-integrity papers' channel the agent cannot reach, DSSE with Ed25519.

## The adversary

**What an agent in a Claude Code session can do on the engineer's machine** (facts from the suite's docs, inferences marked):

- **Run as the engineer's OS user**, with a shell, every file that user can read or write, and localhost.
- **Read Core's token**, so call every Core route with full authority. The token's own threat model excludes "anyone with access to the machines running Core or the API" ([embarch-token.md](../../embarch-token.md)), and the agent is such a one.
- **Write every file under `embarch/`**: studies, plans, custom suites, ledger rows, the live log; the publish folder and every zip in it; the binaries and config of the user-owned components, embarch-api and embarch-ui (a systemd user service); **Claude Code's own permission settings**, which are files in the repo and the home folder.
- **Write the DUT's firmware**, and flash it.
- **Start Windows processes as the Windows user** through WSL interop (inferred from how WSL works; not checked on this machine).
- **Ask the person** to approve something, in the chat, in its own words.

**What it cannot do** (inferred, each to check): act as another OS account without that account's password, so Core's own service account; pass a Windows elevation prompt or `sudo`'s password; touch an authenticator (a security key, Windows Hello, a phone's passkey); see the engineer's phone.

**So the harness and every user-owned component sit inside the adversary's reach.** The permission lists of [agent-guide.md §1.1](../../suite/agent-guide.md) are a guard against error and nothing against subversion; the guide says so. **The root of trust has to be a component the engineer's account cannot change: Core, under its own account.**

## The root of trust: Core, under its own account

**Decided** (owner, review round 1).

- **Core runs as a service under its own OS account**, as an installed Windows Core already does ("typically running as a different account than the interactive user", [embarch-token.md](../../embarch-token.md)); on Linux, a system service with a user of its own. **Its binary is installed where the engineer's account cannot write**, so **updating it is an elevated step** (a Windows elevation prompt, `sudo`), the person's act by construction; today's deploy, an rsync of a build into a folder the service runs from ([embarch-dev-workflow.md](../../embarch-dev-workflow.md) §4a), copies into a user-writable target and so yields an unattested Core until it does that copy elevated (review round 2, recommended).
- **Core's protected store** holds what only Core may write: its signing key, the run log, the confirmations, the registered passkeys. Readable and writable by Core's account alone. **The token file stays readable** (the API needs it), and **the token loses the power to speak for the person or to rewrite evidence**: no route reachable with the token alone does either.
- **A Core run under the engineer's own account is unattested**: a development Core ([embarch-dev-workflow.md](../../embarch-dev-workflow.md)) or one started by hand. It signs with nothing, or with a key marked development, and **every report from it says "unattested"** on its first page.
- **Two ways to use EmbArch, said plainly** (review round 2, recommended): **unattested**, which needs only Core (in any account), embarch-api and a bench, with every rule of the design applied in the engineer's own account and every report saying "unattested"; and **attested**, which adds Core under its own account and either the agent's container or the passkey. Live, a Study and a Test all run unattested; **attestation is what a client can rely on, not what a first result needs.**
- **Identity is the person's act too** (review round 2, recommended): the routes that say which board, probe, instrument or signal is which (`enroll_probe`, `unenroll_probe`, `set_role_board`, `declare_instrument`, `remove_instrument`, `declare_signal`, `remove_signal`, Make live's declarations) take the person's token, since the identity gate and the `bench` mark trust what they declare. The agent proposes them, as Make live already proposes each enrolment for a person to confirm ([embarch-ui decision 90](../../embarch-ui/decisions/bench-live.md)). So does registering or rotating a passkey, and **registering the first passkey is part of Core's elevated install**, so a token alone can never add an authenticator.

## What Core then guarantees, in code

1. **Core signs what it measured.** When a test or a study ends, Core writes an **in-toto Statement in a DSSE envelope**, signed with its Ed25519 key: its subjects are the SHA-256 of every capture, `events.json`, `measurements.json` and `run.json`; its predicate holds the verdicts, the image readback, the unit's and every bench board's identity and image, Core's build, the shared crate's version, and the scope of every token that made a person's act. **The predicate separates what Core observed from what it was told**: the build's commit, dirty state and toolchain come from embarch-api and are carried as claims (review round 2, recommended). **Measurements and verdicts are computed by Core** through the shared crate ([02](02-study.md#measurements)), so the agent cannot rewrite `measurements.json` without breaking the signature.
2. **Core keeps the run log, hash-chained**: one entry per study and per test run, with its verdicts, its Statement's hash and, once published, its manifest's hash, the head held in the protected store. **Retention may delete captures, never an entry** ([03](03-test.md#a-run), item 7). "Every run of this test on this image" ([06](06-report-and-publish.md#publish)) **is read from Core's log**; the repo's `rows.jsonl` becomes a mirror of it.
3. **Core logs every hardware call** in the same chain, since every call passes through it, Live included. The repo's live log becomes a readable mirror, and an atlas write-back's receipt cites Core's entry ([05](05-live.md#the-live-log)).
4. **A person's act is made where the agent cannot reach** (decided, [below](#a-persons-act-what-a-ui-card-can-prove-and-what-it-cannot)): a confirmation of a verdict-deciding input, the go of a Test run, an observation or clearance prompt's answer. **A card in the UI, or the CLI in the person's own terminal, with the person-scoped token**, which the agent in its dev container never holds; the card renders the act from Core's own record, so **what the person approves is exactly what executes** (Consent Integrity, [11](11-prior-art.md#an-agent-speaking-for-the-person)). **The card treats every string the agent wrote as data**: a test's name, a prompt's text, a hook's command are escaped and shown quoted, never as markup; **an act is submitted with a nonce Core issued for that card's rendering**, checked with the request's `Origin`, so a page or link the agent controls cannot post one (cross-site request forgery) (review round 2, recommended). **Where the agent cannot be put in a container, one WebAuthn passkey touch per run** signs the card's list of acts made before the run (the confirmations and the go), and **each observation or clearance answer takes its own touch when it is given**, since it does not exist when the run starts (review round 2, recommended); on a page Core serves at `http://localhost:<port>`, the relying party `localhost` (WebAuthn takes no IP address as its ID) and the origin checked with its port (review round 2, recommended), **top-level and never framed** (`frame-ancestors 'none'`), since embarch-ui is user-owned and a frame inside a page the agent can rewrite could be covered with another act's text.
5. **A confirmation binds the hash of what was confirmed** (owner, round 1) **and Core refuses a run that rests on an unconfirmed input**: at the go, Core checks every verdict-deciding input in `run.json` against its confirmations, so a limit edited after it was confirmed stops the run instead of only showing in the preview.
6. **Core starts a Test only after a go for that run**: bound to the run's id, `run.json`'s hash, the card's nonce and an expiry, and used once ([03](03-test.md#selecting-and-rerunning)).
7. **Core signs the published zip's manifest**, so a zip's origin is Core's key; `verify` checks it against a fingerprint the client got from the engineer out of band; the one the report prints is for comparing by eye ([06](06-report-and-publish.md#verify)).
8. **Core decides "relayed" by the token's scope**, never by a field the caller writes: a prompt's `answered_by`, a manual verdict's surface, a note's author (review round 2, recommended). That amends [embarch-core decision 105](../../embarch-core/decisions/host-prompt.md), where `answered_by` is recorded and trusted for nothing.

## A person's act: what a UI card can prove, and what it cannot

The owner asked (round 1) whether **a UI card with a CLI fallback** could replace the passkey of item 4. **What decides it: against an agent that runs as the engineer's OS user, anything a click in a browser or a CLI command can do, the agent can do too.** A card's button calls an HTTP route; the agent can call the same route with the token, or drive the same CLI. A PIN typed into the card does not help either: a process of the same user can read another's memory (inferred, the general rule on Windows and Linux). **Only something outside the engineer's account separates the person from the agent**: a key held in hardware (a passkey: Windows Hello, a security key, a phone), another device, or another OS account.

So a card alone **covers an agent that errs or drifts** (it does not forge clicks, and every act it relays is marked), and **does not cover one that subverts**. Three shapes, lightest first:

| Shape | Covers error and drift | Covers subversion | Cost to the person |
|---|---|---|---|
| **A card in the UI, the CLI where there is none** | Yes | No | A click per act |
| **The same card, one passkey touch per run**: the card lists every pending act of a run (each confirmation and the go), rendered by Core, and one touch signs the hash of the whole list | Yes | Yes, for every act on the card | One touch per run (a fingerprint or a PIN on most laptops) |
| **A passkey per act** (item 4 as first written) | Yes | Yes | A touch per act |

**The owner's next question (round 1): "Should the agent not run at OS user level in this case?"** That is the other way to put the person outside the agent's reach: **move the agent out of the person's account, instead of adding a key the account cannot hold.**

- **The agent in its own boundary**: Claude Code runs in a dev container, or under an OS user of its own, holding the repo, embarch-api and **an agent-scoped Core token** only. The person's account keeps **a person-scoped token** the agent cannot read, and **a plain card in the UI, or the CLI run in the person's own terminal, then proves the person did it, with no passkey.**
- **It covers more than the person's acts**: the agent can no longer read a full-authority token, replace embarch-ui's binary, edit Claude Code's permission files, or touch published zips outside the repo. Core's signatures stay, since a client cannot see the boundary.
- **What it costs** (from memory, each to check): firmware builds run inside the boundary, so it needs the toolchain (Zephyr publishes container images); embarch-chat starts `claude` inside it; on WSL, **interop lets any Linux user start Windows processes as the Windows user**, so the boundary is a WSL distro of its own with interop off, or a container; Claude Code documents a dev-container setup. `embarch init` would set it up.
- **Core needs scoped tokens either way**: agent and person, so a route that speaks for the person refuses the agent's token.

| Shape | Covers subversion | Changes how the agent runs | Cost to the person |
|---|---|---|---|
| Card only | No | No | A click |
| **Card + one passkey touch per run** | Yes, for the card's acts | No | One touch per run |
| **The agent in its own boundary + card** | Yes, for the card's acts and the files above | Yes: container, account or distro | A click |

**Across the suite's topologies** (the owner asked whether it works on every OS combination). **What makes it work everywhere: the agent needs no hardware.** Core owns every probe and port ([embarch.md](../../embarch.md) §4), so the agent's boundary never needs USB passed through, which is what usually breaks containers on macOS and Windows. It needs the repo, the toolchain, the model's API and Core's port. Sources: Claude Code documents a dev container with a reference default-deny firewall and a Dev Container Feature ([code.claude.com/docs/en/devcontainer](https://code.claude.com/docs/en/devcontainer)); WSL's `[interop]` and `[automount]` are per-distribution settings in `/etc/wsl.conf` ([learn.microsoft.com/windows/wsl/wsl-config](https://learn.microsoft.com/windows/wsl/wsl-config)). The rest is inferred.

| Where the agent runs | The boundary | Holds |
|---|---|---|
| Linux | A dev container, or an OS user of its own | Yes; Core a system service under its own user |
| macOS | A dev container (in the Linux VM Docker Desktop, OrbStack or Colima runs) | Yes; a user of its own is awkward on a desktop Mac |
| Windows | A dev container (Docker Desktop's WSL2 backend) | Yes; Core is already a Windows service |
| **WSL2 with Core on Windows** (the owner's) | A dev container inside WSL, or a WSL distribution of its own with `[interop]` and `[automount]` off | Yes, with care: **a second Linux user is no boundary on WSL**, since interop starts Windows processes as the Windows user and `/mnt/c` reaches the Windows user's files |
| Core on another machine | Any of the above | Yes, the most natural split |

**Two rules every row needs**: **the boundary's network reaches Core's port and the model's API, nothing else**, embarch-ui's port above all, since the UI holds the person's token and a request through it would act as the person (the reference firewall is default-deny, so this is its allow list); and **the person's token is never mounted into it**. **Three more, from review round 2** (recommended):

- **The firewall is set where the agent cannot change it**: the agent runs as a non-root user without `NET_ADMIN`, and the rules are applied before it starts. On WSL2 with Core on Windows bound to loopback, "Core's port only" needs WSL's mirrored networking or Core listening on the WSL virtual interface; which one is the standalone pass's to measure.
- **The repo is the boundary's one door, and it opens both ways.** The agent must write the repo, and the person's own tools run files in it: git runs `.git/hooks` and reads `.git/config`, VS Code reads `.vscode/` and `.devcontainer/`. So **those are mounted read-only into the container**, and git's hooks path is set outside the repo. **What cannot be closed is the code itself**: firmware sources, build scripts and CMake files the agent wrote run as the person whenever the person builds or runs them on the host. **The boundary holds only while the agent's code is built and run inside the container**, through EmbArch's build, which runs there, and the guide says so.
- **The report says what Core saw, not where the agent ran**: "person's acts: person-scoped token", "passkey" or "agent-scoped only". That the agent ran in a container is the engineer's statement, labelled as such ([06](06-report-and-publish.md#the-audit-appendix)).

Costs: the firmware toolchain inside the container (Zephyr publishes images), how a build's artifact reaches Core (to check), and Docker Desktop's licence for larger companies, where Podman, Colima or Rancher Desktop serve (from memory).

**Decided** (owner, review round 1): **the agent in its own boundary, a dev container on every OS, set up by `embarch init`**, with a plain card in the UI (the CLI in the person's own terminal as the fallback) for the person's acts, and **one passkey touch per run as the alternative** for an engineer who cannot run the agent in a container. **Every report says which held**, as Core observed it (review round 2): "person-scoped token", "passkey", or "agent-scoped only". Core gets an agent scope and a person scope on its tokens.

## Operator prompts, by kind

**Decided** (owner, review round 1), after the owner asked for it to be thought through carefully:

**What a prompt's answer means decides who may give it.** A prompt answered by the agent relaying the person's words ([03](03-test.md#a-run), item 2) is as good as the agent's honesty, and as good as its paraphrase: the field log behind Core decision 105 had 25 confirmations typed into a chat in one session. Four kinds:

| Kind | Example | What the answer is | A false answer leads to | Who may answer |
|---|---|---|---|---|
| **Setup** | "Set up bench B: the partner on port 1" | A claim the setup is done | The smoke check fails: an **error**, never a forged pass | The person, or the agent relaying them |
| **Action** | "Plug the cable now"; a hook mapped to a prompt | A timing mark: the person acted | The measured consequence is missing (no attach seen on the wire): a **fail or an error** | Relayed, **if the test measures the consequence**; otherwise it is an observation |
| **Observation** | "Is the LED green?"; "read the meter" | **The measurement itself** | **A forged pass** | **The person's own hand only**: the card or the CLI, never a relay |
| **Clearance** | "Nobody is touching the bench; energise?" | A person's safety | **A person hurt** | **The person's own hand only** |

**The rule:** a prompt declares its kind; **an action prompt names the measurement that confirms it**, checked when the test is defined; **Core refuses an answer to an observation or a clearance prompt that comes with the agent's token**, deciding "relayed" by the token's scope, not by `answered_by` (item 8); **a prompt's kind is part of the test the engineer confirms**, so a study cannot relabel an observation as a setup to have it relayed (review round 2, recommended). An observation's answer is a measurement whose source is **`person`**, beside `bench` and `dut` (below), shown as such. With the passkey, an observation's and a clearance's answer each take a touch when given (item 4).

**A person at the bench, and what comes after** (review round 2, recommended): a setup or action prompt asks a person to handle the bench, and its relayed "done" could release the next step while they still are. So **a step that energises (an instrument's output on, a bench board's power request) after such a prompt needs a clearance prompt between them**, refused when the test is defined otherwise, which keeps the owner's "safety at authoring"; and **the card of every prompt shows what Core last switched on**, from its own record.

## What stays outside prevention, and is said so

- **The DUT's own word.** The agent writes the firmware it flashes, so a measurement the DUT reports about itself (a console line, a self-test result) is only as honest as that firmware. The image readback ties a run to a firmware and its commit, and the commit's diff shows what changed. **Each measurement is marked with its source, `bench` (measured by EmbArch's bench boards or instruments), `dut` (reported by the DUT) or `person` (an observation prompt), and the mark is the whole rule** (owner, review round 1): any test may rest on any source, and the report shows which.
- **The hardware, outside a run.** Safety is an authoring concern by the owner's answer ([03](03-test.md#benches)), and Live's shell commands are free ([05](05-live.md#reach-and-permission)). **While a study or a test runs, Core refuses every hardware call that is not the run's own**, Live reads included, since a halted debug read (`reg_read`, `core_state` with `halt`) disturbs the DUT the run is measuring (owner, review round 1). **No run holds its own lease today** ([08](08-existing-pieces.md#shared)): a run-held lease is planned for a Test and for a Study ([01](01-modes.md#the-lease)). **The rule does not wait on it**, since a run's steps run inside Core and use no HTTP route: during a run, Core refuses every hardware route whoever calls it, with the exceptions [03](03-test.md#a-run) item 4 names (review round 2). Outside a run, **a subverting agent can still put harm on the bench** within the lease, and the trust model says so.
- **The person's judgement.** The agent can still ask for an approval in persuasive words; the card shows the act as Core records it, and the person decides on that.
- **The browser and the authenticator** are trusted: a browser the agent has tampered with could show a page other than Core's (inferred residual risk).
- **The engineer's own choices**: running a development Core, or an account with elevation and no prompt. The report says unattested; nothing else can.
- **Prose**: labelled and its numbers checked ([02](02-study.md#the-report)); its meaning is not.

## What it costs

- **Core's install**: a service account on Linux, a protected store on both, a key generated at setup; for the passkey alternative, a passkey registered at setup.
- **The agent's install**: the dev container, its toolchain image and firewall, from `embarch init`.
- **Core grows**: token scopes, the signing, the chained logs, and for the alternative a small page and the WebAuthn check. Libraries, from memory and unverified: `ed25519-dalek` for the signature, `webauthn-rs` (MPL-2.0) for the passkeys; DSSE is small enough to write in-house ([11](11-prior-art.md#classical-hil-frameworks-formats-and-report-tooling)).
- **Unverified**: that a browser runs WebAuthn on a page at `http://127.0.0.1` (localhost is treated as a secure context; to test), and that WSL interop cannot reach a Windows service account's files.

## Open

- **Items 1 to 8**, Core's signatures, run log, call log and checks, as a whole: recommended, not yet answered one by one; [the evidence proposal](../../embarch-hil-evidence-proposal.md) carries them as its design.
- **Review round 2's additions** (marked so above): the two ways to use EmbArch, identity as the person's act, the card's escaping and nonce, a touch per observation or clearance, the read-only repo files, the clearance before energising, the attestation label. Recommended, the owner's to confirm.
- **The boundary's details**: how a build's artifact reaches Core, the toolchain image, embarch-chat starting `claude` inside it, a plain Claude Code user's way in, the firewall's allow list and networking per topology.
- **Where Core's page lives in the UI's flow**, and the CLI fallback's shape: the standalone pass the owner plans later.
- **Key rotation, a lost key or passkey, and a second engineer's passkey**: each elevated or a person's act, as above; the flows are to write.
