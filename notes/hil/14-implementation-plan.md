# HIL notes: the implementation plan

**Status:** draft, 2026-11-20.

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

## The later phases, in outline

Each gets its own unit list when it starts, with its rows of [08](08-existing-pieces.md) checked against the code first.

- **Live**: the call log (its chain, folded reads, receipts, described as Core's calls) and its half of check 8; the live log as its mirror; the 30-minute idle release enforced by Core; `instrument_exchange` refused outside a run; [agent-guide.md](../../suite/agent-guide.md) §1.1; the write-back once the atlas has its measured write-back.
- **Test**: the numeric parse at step time; a first host study on the real PD bench; the image readback and the released bench-firmware hash list; Core's Test route (`run.json` re-expanded, the go card and the go, prompts by kind, the run-held lease, the failure policy, the run record); the example shell suite, then the PD suite; the ledger grown into `test_*`.
- **The attested phase**: Core under its own account; its protected store, the identity store included; installs from a signed release only; `deploy-core`'s development Core beside the service, and the start and stop grant; outputs off at every stop and start; exclusive port handles; the topology CLI refusing under a lease; the call log failing closed, with its quota and reserved tail.
- **The standalone container pass**, then **the passkey phase**.

## Open

- **M1.3, the verdict rules, has no user in milestone 1**, since a Study has no verdict; the owner's order puts the shared crate in milestone 1 whole. To move to the Test phase if fleet capacity is short.
- **Where `suite/hil-guide.md` is embedded from** (M1.12): embarch-api would need the guide's text at build time, from a pinned copy of embarch-doc or a copy in its own repo. The unit's call.
- **How long milestone 1 takes**: unmeasured. Twelve fleet units at four per leg is at least three legs; M1.14 waits for all of them.
- **Where the attested phase falls** against Live and Test: the owner's order leaves it to this plan, and this plan leaves it until milestone 1 has run.
