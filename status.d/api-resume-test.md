**Target:** suite/agent-guide.md §1.1 — the **allow** list (line beginning "- **allow** — reads, host-side builds"), after `reset_dev_bench`, beside `run_test`
**Was:** the allow list names `run_test` and `test_status` among the Test tools, and no `resume_test`
**Now:** add `resume_test` (embarch-api decision 148): like `run_test` it only prepares a Test run from an interrupted one and never starts it, since the go is the engineer's on Core's card; and name it in the "`run_test` prepares a Test run and never starts one" sentence of the paragraph below.
