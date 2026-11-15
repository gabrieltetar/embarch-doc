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

## Study

| Piece | Exists | Where |
|---|---|---|
| Dev-bench studies, taps, `events.json`, streams with truncation | yes | [studies guide](../../suite/studies-guide.md), [result layout](../../embarch-core/interfaces/result-layout.md) |
| Host studies: exchanges, instruments, prompts, `Repeat`, line counts | yes | [Core decisions 95, 98, 99](../../embarch-core/decisions/host-study.md) |
| Dev-bench studies saved in `embarch/studies/` | yes | [embarch-ui spec](../../embarch-ui/spec.md) |
| Host studies saved in a repo | **no** | [02-study.md](02-study.md#where-its-files-live) |
| `report.typ`, Typst in embarch-api, the PDF | **no** | [06-report-and-publish.md](06-report-and-publish.md) |
| `study_publish` and the zip | **no** | same |

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
| Premade suites on atlas requirement records | **no** | [04-premade-suites.md](04-premade-suites.md) |

## Live

| Piece | Exists | Where |
|---|---|---|
| Raw reads and actions: `mem_read`, `core_state`, `serial_log`, `reset`, `signal_exchange`, captures | yes | [agent-guide §1.1](../../suite/agent-guide.md) |
| Decoded reads: `reg_read`, `shell`, `shell_run`, `live_stacks`, `core_state` | yes | `embarch-atlas` repo, `DESIGN.md`, "Live" |
| `measured` as an atlas provenance level | yes | same, "records" |
| The live log | **no** | [05-live.md](05-live.md#the-live-log) |
| Writing a live finding back, with its receipt | **no** | [05-live.md](05-live.md#writing-a-finding-back) |
| Permission lists matching the Live mode | **no** | [07-procedure-doc.md](07-procedure-doc.md#gaps-it-closes) |

## Open

- **This inventory was taken from the docs, not from the code.** Each "yes" a phase relies on is checked against its repo when that phase starts (owner, 2026-11-15).
