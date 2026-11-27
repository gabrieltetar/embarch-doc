# embarch-api decisions: The test ledger reads Core's run log

**Status:** active, 2026-11-26.

Decision 142: `test_show`, `test_pending` and `test_add` replace `ledger_show`, `ledger_pending` and `ledger_add` (`tasks/api/211`, EMB-379), as [HIL 03](../../notes/hil/03-test.md) "It grows out of the ledger" says they will.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Tools: [../interfaces/tools-test-ledger.md](../interfaces/tools-test-ledger.md). Replaces the tools of [98](ledger.md).

### 142 - The ledger's record is Core's run log; `results.jsonl` mirrors it, `embarch/ledger/` is legacy, and a manual verdict is a route call

**The record is `GET /run-log`.** The `test` entries of Test runs and core decision 147's `manual_verdict` entries are the ledger; nothing else in the log is read. `embarch/tests/results.jsonl` holds one row per entry, keyed by the entry's hash, and **every `test_*` call rewrites it from the log**: a row that differs is replaced by the log's, a row whose entry is gone is dropped, a file already right is not written. The log has no commit, so a row's `branch` and `commit` are the tree's at the call that first wrote it and are kept on a rewrite; the rebased-away rule reads them there. Written atomically beside the other `embarch/tests/` files, refusing a link. When Core cannot be reached `test_show` and `test_pending` fail and say so, and the mirror is not touched: there is no fallback reading, unlike 98's `attached`.

**Pending is the HIL 03 rule, grouped by bench.** A test is pending when its latest counted entry on the current image is not a pass (`fail`, `inconclusive`, or `not-reached` for a null verdict), when it never ran on that image, or when the mirror's commit is no longer reachable from its branch (98's read-only `git merge-base --is-ancestor`). The image is the caller's `image_path`/`image_hash`; it is compared with the entry's `dut_image.claim`, and an entry without a claim counts on any image. **Assumed, not measured:** that `claim` is the image hash the run was made against; `holds` and `differs` are not read. Tests come from the repo's custom suites (their bench is the grouping) and from the log (grouped `(unknown bench)`); premade suites that live only in Core, `tests.toml`'s `needs` and the attached-roles split are not read, so there is no `runnable_now`. Test ids are matched across suites by id alone. The unit key is not matched.

**A relayed manual verdict is listed and never counted**, as a pass or a failure: it sits beside its test as `relayed`. A person's verdict counts as the latest entry. This is the rule Core's entry records and leaves to its reader (core 147).

**`test_add` is `POST /manual-verdicts`** with `{test_id, definition_hash, unit_key, verdict, reason, dut_image?, note?}`, `pass`, `fail` or `inconclusive`, refused here before Core if the verdict or the 64-hex hash is wrong. `definition_hash` defaults to the hash of the one test of that id under `embarch/tests/suites/`; none or two is a refusal naming it. The answer reads "relayed by the agent" when Core's entry says `relayed`, which it does for the agent's token, the only one this tool sends.

**`embarch/ledger/` is legacy and never written.** Its `rows.jsonl` rows are listed by `test_show` apart ("before Test, not in Core's log") and are not in pending; `tests.toml` and `bench.json` are not read. Nothing is moved, which is the issue's default; moving the folder on the first call or keeping aliases is the owner's to choose (plan choice 17). **So `run_study` stops appending `submitted` rows and loses its `test` param and `ledger` key**: a row there would feed a folder this unit calls closed, and a study outside a Test run has no `test` entry in Core's log.

**What of 98 stands:** the commit-reachability rule and the read-only git. Retired: the three files as the record, `submitted` rows and settling, `attached`, `broken`, `ambiguous_needs`.

**The client** gains `CoreClient::run_log` and `manual_verdict`, additive, each a `send` of one route; `tests/core_client_http.rs` sweeps both for the token.

**Not verified:** unit tests, and a mock Core for the three verbs; no real Core's log, no bench.
