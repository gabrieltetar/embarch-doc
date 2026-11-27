# embarch-api: test ledger tools

**Status:** active, 2026-11-26 ([decisions 142](../decisions/test-ledger.md); replaces `ledger_*` of [98](../decisions/ledger.md)); see [tools.md](tools.md) for the one-table premise. Each tool is also a kebab-case subcommand (`test-show`, `test-pending`, `test-add`), `--project` defaulting to the session's desk's. Code: `src/test_ledger.rs`. Core's side: [run-log](../../embarch-core/interfaces/run-log.md), [manual-verdicts](../../embarch-core/interfaces/manual-verdicts.md).

Core's run log is the record: `GET /run-log`, its `test` entries (a Test run's) and `manual_verdict` entries. `embarch/tests/results.jsonl` mirrors them, one row per entry, and is rewritten from the log on every call (the log wins; a row's `branch` and `commit`, which the log lacks, are kept). `embarch/ledger/` is legacy: read, never written. `ledger_*` are gone, with no alias; `run_study` no longer takes `test` or appends a row.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `test_show` | `project?`, `test?`, `limit?` (20) | The last entries of the log, newest last, with `mirror` `{added, rewritten, removed}` and the log's `verified`/`head`. `legacy` lists the `embarch/ledger/` rows apart, "before Test, not in Core's log". A relayed entry is marked |
| `test_pending` | `project?`, `image_path?` or `image_hash?` | `by_bench`: bench name to items `{id, title, reason, relayed}`; `reason` is `never-run`, the latest counted verdict that was not a pass (`fail`, `inconclusive`), `not-reached`, `image-changed` or `commit-unreachable`. A test the log knows and no suite defines sits under `(unknown bench)` |
| `test_add` | `test`, `verdict` (pass/fail/inconclusive), `reason`, `unit_key`, `project?`, `definition_hash?`, `dut_image?`, `note?` | `POST /manual-verdicts`; `definition_hash` defaults to the hash of the test under `embarch/tests/suites/`. The answer carries `relayed` and `attribution`: with the agent's token, "relayed by the agent". Then the mirror follows the log |

**The rerun rule.** A test is done when its latest counted entry on the current image is a pass whose commit, from the mirror row, is still reachable from its branch. With an image named, only entries whose `dut_image.claim` matches it (or that have none) are runs on it. A relayed manual verdict never counts, not as a pass and not as a failure.

**Not verified on a bench or against a real Core** ([open.md](../open.md)). The tests are unit tests and a mock Core.
