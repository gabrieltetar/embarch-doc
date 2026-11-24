# HIL notes: the implementation plan

**Status:** draft, 2026-11-24.

The plan asked for once review round 4 closed ([10](10-review.md#round-4-2026-11-20)): the first milestone unit by unit, the later phases in outline. **The order and who builds it are the owner's (2026-11-19)** ([the proposal](../../embarch-hil-proposal.md#order)). **The units, their split and what each needs first are the plan's recommendation**; each milestone-1 unit is filed as a Linear issue in Backlog, for the owner to move to Fleet Ready (owner, 2026-11-20).

## Milestone 1: an unattested Study publish

**What it delivers**: the BLE GATT data-acquisition study, which already runs on hardware, published as a signed zip that `verify` checks offline. The Core is one not installed from a signed release, so every report reads "unattested" ([12](12-prevention.md#the-root-of-trust-core-under-its-own-account)).

**What it leaves out, by the owner's rulings** (review round 4, owner 2026-11-20): the image readback (the DUT image is a claim, every bench board `unverified`); the call log (the zip says "no call log"); Core's own account and protected store; the card and the go; every Test and Live piece.

**Checked against the code before planning** (review round 4's buildability reviewer, 2026-11-20), as [08](08-existing-pieces.md#open) asks of each phase:

- `embarch-study-designer` is a `no_std` types crate that Core (with `std`) and embarch-api (with `alloc`) already link, so the shared crate's host-only half has a home.
- Core has one token (`token_store.rs`), no hash chain, no DSSE or Ed25519, and no readback path from a DUT; `last_images` lives in memory since Core's start.
- embarch-api has no Typst.
- The lease, the ledger, prompts, `study_lock`, retention and `hardware_id` hold as 08 states.

| Unit | Repo | Who | Needs | What | Done when |
|---|---|---|---|---|---|
| **M1.1** File shapes | `embarch-study-designer` (its docs here) | fleet | — | The doc R24 asked for: verdicts; `measurements.json` with every field of [02](02-study.md#measurements), `declared_by`, `u_source` and `rate_check`; `run.json`; a Study's export and check shape; the PDF text extractor and number grammar; the plot helper's tick algorithm and the footer rule; a bench board's characterisation | The shapes sit in `embarch-study-designer/interfaces/`, and notes 02, 03 and 06 point at them |
| **M1.2** Reducers | `embarch-study-designer` | fleet | M1.1 | Count, rate, min, max, mean, percentile, the interval between two markers, the value at a marker: each with its contract, its fixture, its `U` rule with the type-A term, and how it reports incomplete input; versioned by behaviour | `cargo test` passes against the fixtures with no Core installed |
| **M1.3** Verdict rules | `embarch-study-designer` | fleet | M1.1 | The six verdicts, the step-outcome mapping, the guard band on both sides, the acceptance-width rule, the severity order, the requirement roll-up with its qualifiers and the gap rule | A fixture per verdict, per qualifier and per roll-up case |
| **M1.4** Two tokens | `embarch-core` | fleet | — | Core writes an agent token and a person token at first start; every route records the scope it was called with; embarch-api and embarch-ui read the pair | A call with each token records its scope; [Core decision 93](../../embarch-core/decisions/lease.md) and [embarch-token.md](../../embarch-token.md) amended |
| **M1.5** Signing | `embarch-core` | fleet | M1.1 | An Ed25519 key in Core's store under the engineer's account, its path per OS; a DSSE envelope over an in-toto Statement per study run, its subjects the captures, `events.json`, `measurements.json` and the study file Core keeps by hash; the predicate keeping what Core observed apart from what it was told; the fixed-frame challenge | A record verifies with a standard DSSE check, and the challenge route signs only its frame |
| **M1.6** Run log | `embarch-core` | fleet | M1.5 | The hash-chained run log, one entry per study run, the manifest hash added on publish, never swept; retention that sweeps no capture before publish and applies the discard rules of [13](13-research-phase.md#many-scans-few-reports); a route returning a publish's entry and the log head | The chain recomputes in a test, and a discard of a failing run's captures is refused with the agent's token |
| **M1.7** Measurements at a study's end | `embarch-core` | fleet | M1.2 | Core links the crate and writes `measurements.json` as each study ends: `by` and `instrument` from what the step addressed, resolution and `U` from the declaration or "U undeclared", `declared_by`, `bench_image: unverified`, the DUT image as a claim | A recorded capture yields the expected `measurements.json` |
| **M1.8** Core's side of publish | `embarch-core` | fleet | M1.4, M1.6, M1.7 | `report-data.json` written and signed at publish; notes and prose adoptions recorded with the token's scope and the text's hash; the manifest signed over the files Core produced | Publishing a fixture run yields a signed manifest and a signed `report-data.json` |
| **M1.9** The PDF | `embarch-api` | fleet | M1.1 | Typst built in (`typst`, `typst-pdf`, `typst-as-lib`), lilaq vendored, the plot helper drawing per-bin min and max, staging by content with links refused, Typst's root confined to the staged files, `PdfOptions.ident` and `timestamp` set | A fixture run renders offline, and a `report.typ` reading outside the staging root fails |
| **M1.10** The zip | `embarch-api` | fleet | M1.8, M1.9 | `publish <run id>`, an MCP tool and a subcommand: the numeric-oracle listing (citations, tags, unbound, hardcoded), authorship per block, the audit appendix, every capture raw and as CSV, the Study's exports, revisions built from the earlier zip, the publish folder setting, the `notes` parameter | A fixture run publishes, and publishing it again writes `-r2` |
| **M1.11** verify | `embarch-api` | fleet | M1.10 | `verify <zip>`: checks 0 to 8 as they apply to a Study and to a zip with no call log; check 9's syntax-tree whitelist, packages hashed against the checkout's list; the unattested result's wording | It passes a fixture zip and fails each tampered copy: a changed number, an embedded image, a forged label, a dropped run-log entry |
| **M1.12** The guide served | `embarch-api` | fleet | — | `embarch-api guide hil <mode>` serves the guide embedded at build, versioned with the tools; the `embarch-hil` skill points at it | The skill's pointer resolves on a machine with no embarch-doc checkout |
| **M1.13** The guide's Study and trust sections | `embarch-doc` (`suite/`) | interactive | M1.10, M1.11 | `suite/hil-guide.md`: the glossary, the claim and its exceptions, the rules that rest on procedure alone, choosing a mode, the Study section with the BLE GATT example ([07](07-procedure-doc.md#an-outline-of-the-guide)) | A first Study can be run and published from the guide alone |
| **M1.14** The first published Study | — | interactive, bench | every unit above | Run the BLE GATT study on the bench, publish it, run `verify` on the zip in a clean folder, read the report against the trust model ([09](09-trust-model.md)) | A zip that verifies, and every gap it shows filed |

**Filed as EMB-216 to EMB-229, in unit order, in Backlog** (2026-11-20).

**What can start at once**: M1.1, M1.4 and M1.12, which need nothing. M1.2, M1.3, M1.5 and M1.9 follow M1.1; M1.6 follows M1.5, M1.7 follows M1.2, M1.8 needs M1.4, M1.6 and M1.7, M1.10 needs M1.8 and M1.9, and M1.11 needs M1.10. **Each unit amends its own repo's decisions as it lands**, and moves its part of the two proposals into that repo's docs ([DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §3).

## The Live phase

**Planned 2026-11-23, with every row of [08](08-existing-pieces.md) Live touches checked against the code first; filed as these issues.** Fleet units first, then the owner's two.

| Unit | Issue | Repo | Who | Needs | What |
|---|---|---|---|---|---|
| **L.1** Call log | EMB-249 | `embarch-core` | fleet | — | `call-log.jsonl`: one chained entry per lease-gated call, refusals included; repeated reads folded; each answer names its entry |
| **L.2** Call log in record and zip | EMB-250 | `embarch-core` | fleet | L.1 | The signed record carries the head and the run's range; publish writes the segment |
| **L.3** Idle release | EMB-251 | `embarch-core` | fleet | — | A lease released after 30 min with no hardware call, whatever client renews; a run in flight is not idle |
| **L.4** `instrument_exchange` outside a run | EMB-252 | `embarch-core` | fleet | — | Refused outside a run, pointing to a host study's `Instrument` step |
| **L.5** Only the run's calls during a run | EMB-253 | `embarch-core` | fleet | — | Every lease-gated route refused while a study runs, but its cancel |
| **L.6** Check 8's call-log half | EMB-254 | `embarch-api` | fleet | L.2 | `verify` recomputes the segment the record names |
| **L.7** Live log, raw lines | EMB-255 | `embarch-api` | fleet | L.1 | One line per hardware call in `embarch/live/`, citing Core's entry; a `call-log` subcommand |
| **L.8** After an idle release | EMB-256 | `embarch-api` | fleet | L.3 | The token dropped; the next hardware call refused with the reason |
| **L.9** The instrument tool follows Core | EMB-257 | `embarch-api` | fleet | L.4 | The tool and CLI verb removed |
| **L.10** Call log in `report-data.json` | EMB-265 | `suite` | fleet | L.2, L.6 | The head, range and count, with check 6's recompute of them, in one unit |
| **L.11** Live log, decoded lines | EMB-266 | `embarch-atlas` | fleet | L.7 | Each atlas live tool's decoded line, citing Core's entries |
| **L.12** Measured write-back | EMB-267 | `embarch-atlas` | fleet | L.7, L.11 | A `measured` fact with its receipt from Core's entry |
| **L.13** Measured beside claimed | EMB-268 | `embarch-atlas` | fleet | L.12 | A disagreement with the datasheet becomes a check finding |
| **L.14** agent-guide.md §1.1 | EMB-269 | `embarch-doc` | fleet | L.9 | The permission lists per [05](05-live.md), with an atlas list |
| **L.15** The guide's Live section | EMB-270 | `embarch-doc`, `embarch-api` | interactive | L.1–L.11, L.14 | `suite/hil-guide.md` "Live" and its pinned copy |
| **L.16** The first Live session | EMB-271 | — | interactive, bench | every unit above | About 2 h on the bench, 30 min of it the idle wait |

**The owner's answers, 2026-11-23.** `instrument_exchange` stays a Core route that refuses outside a run with a pointer to the `Instrument` step, and its tool goes (Q1). The during-a-run refusal belongs to Live (Q2). The atlas's measured write-back is built in Live, ahead of the planes rework (Q3). A fold chains the first read at once and writes the repeats as one later entry (Q4). **The eleven smaller choices the issue bodies make were each kept by the owner the next day**: among them, a refused call is logged, Core keeps hashes and not answers, a run in flight is not idle, and a write-back citing an entry Core does not hold is refused.

## The Test and attested phases

**Planned 2026-11-24 the same way, every relevant row of [08](08-existing-pieces.md) checked against the code first, and filed with their blocker chains.** The unit tables, the code check and the choices sheets are in the planning drafts; each issue body carries its unit.

- **Test**: 46 units. Fleet: T.1–T.38 and T.41, EMB-352 to EMB-390; the crate's step-time parse, test, suite and plan types and run expansion; Core's definitions, prepare, go, run-held lease, executor, prompt kinds, smoke check, run record and Test publish; embarch-api's plans, `run_test`, ledger-to-`test_*` and Test `verify`; the UI's confirmation and go cards; `pd-bench`'s idle, hello and timing lines. Owner: create the `embarch-suites` repo (EMB-391; the example shell suite T.39 and the PD suite T.40 are filed after it, the PD suite being the owner's because its limits come from the specification), the guide's Test section (EMB-392), the first host study on the PD bench (EMB-393), `pd-bench`'s characterisation (EMB-394) and the first Test run (EMB-395).
- **Attested**: 32 units. Fleet: A.1–A.25, EMB-320 to EMB-344; topology's settable store and `safe_off` declarations, Core's service and development stores, install under its own account, safe-off at start and stop, exclusive handles, the call log failing closed with its quota, embarch-api's challenge before any token, the UI's Core identity, and `embarch-umbrella`'s install, deploy and release scripts. Owner: the docs (EMB-345), a rehearsal and a real signed release, the first elevated install on Windows, the development loop and first run for record on the bench, and the Linux install (EMB-346 to EMB-351).

**Choices the bodies carry on the drafts' recommendations**, for the owner to strike: 29 for Test (among them suites in a new repo, JSON definitions, a 10-minute go nonce, an image identified by its per-range hashes) and 25 for attested (among them the virtual `NT SERVICE` account, service mode from a `run --service` flag, a 1 GiB call-log quota, Linux in this phase).

## The container pass and the passkey phase

**Planned 2026-11-24 the same way, every relevant row of [08](08-existing-pieces.md) checked against the code first, and filed with their blocker chains.** Each leaves to the attested phase what that phase already planned: Core's own account and store, the start-and-stop grant behind an install flag, the fixed-frame challenge. **Each opens with a decision the owner makes before its first fleet unit can start**, since 12 leaves both "recommended": the agent's clone and the `embarch/` flow for the container pass, the WebAuthn check and its licence for the passkey.

- **The container pass**: 26 units. Owner first: the agent's clone and the `embarch/` flow decided (EMB-443). Fleet: C.2–C.22, EMB-444 to EMB-463 and EMB-468; `embarch-umbrella`'s rendered container definition with its hardening, the firewall at start, the toolchain image and west mounts, `embarch init --container`, `embarch agent up|down|status|shell`, the first-start seed of the agent's own clone, the fingerprint copies the elevated install writes, the statement and the grant tied to it; Core keeping the engineer's container statement, each record naming the statement in force, and listing what it keeps; the "agent in a container" label; embarch-api's container mode, `person statement`, the confined writer and `person mirror`, `verify` and `status` reading `embarch/core-fingerprint`; the statement on every UI card; a chat inside the container; the atlas taking a study or test result as a measured fact; [agent-guide.md](../../suite/agent-guide.md) for the container. Then the guides (EMB-464), a container runtime installed and the boundary measured (EMB-465), the first bench session from the container (EMB-466) and the first run for record with the container label (EMB-467).
- **The passkey phase**: 24 units, **on hold** (owner, 2026-11-24: not to be used for a long time). Every unit stays in Backlog with a comment saying so, whatever happens to its blockers, until the owner lifts the hold. Owner first: the library and its licence (EMB-418). Fleet: K.2–K.21, EMB-419 to EMB-438; the shared crate's assertion and registration checks; Core's page, its origin held on both loopback addresses, registered passkeys and the first registration, the touch ceremonies, every person-scoped act waiting for a touch (the Test's acts, the identity routes, the quota and the container statement among them), the stop by touch, later passkeys, revocation and a second engineer's, touches in the records and the label, a new log saying so and the key rotating; `embarch-umbrella`'s first passkey at the elevated install, stop and switch by touch, elevated recovery; the person's terminal taking a touch, `verify` rechecking each touch and the appendix naming them; the UI's cards. Then the guide's passkey section (EMB-439), real authenticators against the page (EMB-440) and the first run for record with the passkey (EMB-441).

**Choices the bodies carry on the drafts' recommendations**, for the owner to strike: 27 for the container pass (among them the firewall applied inside the container by an entrypoint that then drops every capability, the agent's `embarch/` copy in a read-write outbox the person's tools never build in, Claude Code's configuration a host folder so embarch-chat reads its transcripts, one machine-wide statement unchanged from a run's start to its publish) and 29 for the passkey (among them an in-house check over `p256`, `rsa` and `ed25519-dalek` rather than `webauthn-rs`, Core binding both loopback addresses so no other process can serve its origin, one middleware parking every person-scoped act until a touch, user presence required and user verification preferred, starting the service staying elevated).

## The later phases, in outline

Each gets its own unit list when it starts, with its rows of [08](08-existing-pieces.md) checked against the code first.

- **Live**, planned above: the call log (its chain, folded reads, receipts, described as Core's calls) and its half of check 8; the live log as its mirror; the 30-minute idle release enforced by Core; `instrument_exchange` refused outside a run; [agent-guide.md](../../suite/agent-guide.md) §1.1; the write-back once the atlas has its measured write-back.
- **Test**, planned above: the numeric parse at step time; a first host study on the real PD bench; the image readback and the released bench-firmware hash list; Core's Test route (`run.json` re-expanded, the go card and the go, prompts by kind, the run-held lease, the failure policy, the run record); the example shell suite, then the PD suite; the ledger grown into `test_*`.
- **The attested phase**, planned above: Core under its own account; its protected store, the identity store included; installs from a signed release only; `deploy-core`'s development Core beside the service, and the start and stop grant; outputs off at every stop and start; exclusive port handles; the topology CLI refusing under a lease; the call log failing closed, with its quota and reserved tail.
- **The standalone container pass**, planned above: the agent's dev container set up by `embarch init`, its own clone and its definition outside the repo, its hardening; the engineer's container statement as a person's act in Core's store, and the label it drives; the fingerprint copies.
- **The passkey phase**, planned above and on hold: the details 12 marks "recommended, its details wait for the passkey's phase", each decided in its units: a touch per run and per observation or clearance, the passkey as the whole person's scope where the agent is not contained, its page and relying party, the label listing which acts a touch signed, later passkeys needing a registered one.

## Open

- **M1.3, the verdict rules, has no user in milestone 1**, since a Study has no verdict; the owner's order puts the shared crate in milestone 1 whole. To move to the Test phase if fleet capacity is short.
- **Where `suite/hil-guide.md` is embedded from** (M1.12): embarch-api would need the guide's text at build time, from a pinned copy of embarch-doc or a copy in its own repo. The unit's call.
- **How long milestone 1 takes**: unmeasured. Twelve fleet units at four per leg is at least three legs; M1.14 waits for all of them.
- **Where the attested phase falls** against Live and Test: the owner's order leaves it to this plan, and this plan leaves it until milestone 1 has run.
