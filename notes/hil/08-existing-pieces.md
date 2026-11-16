# HIL notes: what exists, and what each mode still needs

**Status:** draft, 2026-11-15.

The options were weighed by simplicity and by reuse. This is the reuse side: what each mode stands on, and the gap left. **"Exists" means built; it does not mean verified on a bench** — each linked doc says how far that goes.

## Shared

| Piece | Exists | Where |
|---|---|---|
| Bench lease, held by a session | yes | [embarch-api lease tools](../../embarch-api/interfaces/tools-lease.md), Core decision 93 |
| Saved benches, Make live, configs | yes | [embarch-ui decisions 73, 90, 96–98](../../embarch-ui/decisions.md) |
| Board identity gate, `validate` | yes | [embarch-topology spec](../../embarch-topology/spec.md) |
| `last_images`: what Core last flashed, with its SHA-256 | yes | [lease tools](../../embarch-api/interfaces/tools-lease.md) |
| A lease held by a run instead of a session | **no** | Test |
| The `embarch-hil` skill and `suite/hil-guide.md` | **no** | [07-procedure-doc.md](07-procedure-doc.md) |
| Measurements: `measurements.json`, the reducers and verdict rules as one crate Core and embarch-api link | **no** | [02-study.md](02-study.md#measurements) |
| The numeric-oracle listing and per-block authorship at publish | **no**; the atlas has the numeric rule for its own records | [02-study.md](02-study.md#the-report) |
| Revisions on republish, the manifest hash in the ledger row, every run listed | **no**; the ledger's rows are append-only | [06-report-and-publish.md](06-report-and-publish.md#publish) |
| `verify <zip>` | **no** | [06-report-and-publish.md](06-report-and-publish.md#verify) |

## Study

| Piece | Exists | Where |
|---|---|---|
| Dev-bench studies, taps, `events.json`, streams with truncation | yes | [studies guide](../../suite/studies-guide.md), [result layout](../../embarch-core/interfaces/result-layout.md) |
| Host studies: exchanges, instruments, prompts, `Repeat`, line counts | yes | [Core decisions 95, 98, 99](../../embarch-core/decisions/host-study.md) |
| Dev-bench studies saved in `embarch/studies/` | yes | [embarch-ui spec](../../embarch-ui/spec.md) |
| Host studies saved in a repo | **no** | [02-study.md](02-study.md#where-its-files-live) |
| `report.typ`, Typst in embarch-api, the PDF | **no** | [06-report-and-publish.md](06-report-and-publish.md) |
| `publish` and the zip | **no** | same |

## Test

| Piece | Exists | Where |
|---|---|---|
| Ledger: test definitions, result rows, computed pending view, image-hash rerun rule | yes, **not verified on a bench** | [embarch-api decision 98](../../embarch-api/decisions/ledger.md) |
| Operator prompt, answered in the UI or relayed by `answer_prompt` | yes | [embarch-core decision 105](../../embarch-core/decisions/host-prompt.md), [embarch-ui decision 69](../../embarch-ui/decisions/operator-prompt.md) |
| A prompt naming a bench config | yes | [embarch-study-designer decision 88](../../embarch-study-designer/decisions/host-prompt.md) |
| Bench instruments over SCPI | yes | [embarch-topology decision 49](../../embarch-topology/decisions/instruments.md), [Core 104](../../embarch-core/decisions/instruments.md) |
| The PD partner bench app | yes | [embarch-dev-bench pd-bench decisions](../../embarch-dev-bench/decisions/pd-bench.md) |
| Teardown on every way out of a host study | yes, over a fake port only | [Core decision 95](../../embarch-core/decisions/host-study.md) |
| A first host study on a real bench | **no** | [host-study proposal](../../embarch-host-study-proposal.md), "What is left" item 1 |
| A number parsed out of a reply at step time | **no** | same, item 2 |
| Suites, tests with verdict rules, test plans, DUT hooks | **no** | [03-test.md](03-test.md) |
| A Core route that runs a resolved Test across benches | **no** | same |
| Six verdicts, a failure charged by what the step addressed | **no**; a lost port is `Fail` today | [Core decision 95](../../embarch-core/decisions/host-study.md), [03-test.md](03-test.md#the-verdict) |
| Preconditions, `requires`, `stop_on_fail` | **no** | [03-test.md](03-test.md#one-test) |
| `run.json`, templates, the preview | **no** | [03-test.md](03-test.md#selecting-and-rerunning) |
| The image read back through the probe | **no**; the atlas's `image_check` reads 16 words at three places | `embarch-atlas` repo, `DESIGN.md`, "Live" |
| A resolution per measurement source, refused limits | **no** | [03-test.md](03-test.md#the-verdict) |
| An interrupted run resumed, the host kept awake | **no**; an `interrupted` record exists | [embarch-api studies](../../embarch-api/interfaces/studies.md) |
| Capability provenance, confirmation of every verdict-deciding input | **no** | [03-test.md](03-test.md#the-duts-inputs) |
| Premade tests validated against injected faults | **no** | [04-premade-suites.md](04-premade-suites.md#decided) |
| Premade suites on atlas requirement records | **no** | [04-premade-suites.md](04-premade-suites.md) |

## Prevention

| Piece | Exists | Where |
|---|---|---|
| Core as an installed Windows service, typically under another account | yes | [embarch-token.md](../../embarch-token.md) |
| Core's own account on Linux and macOS, a protected store, a signing key | **no** | [12-prevention.md](12-prevention.md#the-root-of-trust-core-under-its-own-account) |
| Token scopes (agent, person) | **no**; one token, full authority | [embarch-token.md](../../embarch-token.md) |
| Signed records, the hash-chained run log and call log | **no** | [12-prevention.md](12-prevention.md#what-core-then-guarantees-in-code) |
| The card for a person's acts; confirmations kept by Core | **no**; the UI's prompt modal exists | [embarch-ui decision 69](../../embarch-ui/decisions/operator-prompt.md) |
| The agent's dev container, set up by `embarch init` | **no** | [12-prevention.md](12-prevention.md#a-persons-act-what-a-ui-card-can-prove-and-what-it-cannot) |
| Prompt kinds; no other hardware call during a run | **no**; `study_lock` refuses some routes during a study | [Core decision 95](../../embarch-core/decisions/host-study.md) |

## Live

| Piece | Exists | Where |
|---|---|---|
| Raw reads and actions: `mem_read`, `core_state`, `serial_log`, `reset`, `signal_exchange`, captures | yes | [agent-guide §1.1](../../suite/agent-guide.md) |
| Decoded reads: `reg_read`, `shell`, `shell_run`, `live_stacks`, `core_state` | yes | `embarch-atlas` repo, `DESIGN.md`, "Live" |
| `measured` as an atlas provenance level | yes | same, "records" |
| The live log | **no** | [05-live.md](05-live.md#the-live-log) |
| Writing a live finding back, with its receipt and `via` | **no** | [05-live.md](05-live.md#writing-a-finding-back) |
| Permission lists matching the Live mode | **no** | [07-procedure-doc.md](07-procedure-doc.md#gaps-it-closes) |

## Open

- **This inventory was taken from the docs, not from the code.** Each "yes" a phase relies on is checked against its repo when that phase starts (owner, 2026-11-15).
