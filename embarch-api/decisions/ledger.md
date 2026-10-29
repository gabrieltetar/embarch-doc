# embarch-api decisions: The hardware test ledger

**Status:** active, 2026-10-28.

Decision 98: what ran, on what, and what waits for which hardware, kept per project and computed rather than hand-written. Landed as `tasks/api/128`, from a field engineer who kept the log and the pending list by hand across 5-6 sessions in 8 days.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Tools: [../interfaces/tools-ledger.md](../interfaces/tools-ledger.md).

### 98 - A per-project ledger under `embarch/ledger/`, a pending view that is computed, and a study row that settles when read

**Three files in `<project source_path>/embarch/ledger/`, untracked like the rest of `embarch/`.** `tests.toml` holds the hand-written test definitions (`id`, `title`, `pass`, `image`, `needs`, `notes`); `rows.jsonl` is append-only; `bench.json` is the header (`attached`, `broken`). Plain files, not a Core table: the ledger is about a firmware repo's work and travels with it, and this crate keeps no state of its own. The roles a test `needs` are matched, case-insensitively, against what Core's topology lists: an enrolled board by **role and by board name** and a declared instrument by name. **Confirmed against `embarch-topology`'s types (`tasks/api/149`, 2026-10-28):** a role-less bench board (topology decisions 41, 48) is stored with `role == NO_ROLE` (`""`) and a `name`; the ledger skips the empty role, so the board is needed by its `name`, never by probe serial (a serial is a probe's, not a need's). Nothing in topology makes `name` unique (rows are keyed by probe), so `ledger_pending` also returns `ambiguous_needs`, the names a test needs that two attached things answer to (two boards, or a board and an instrument); such a need still counts as met, and the view says it cannot tell which. Unit tests cover a role-less board attached, absent, and ambiguous, and an instrument attached and absent.

**The pending view is computed on every call and never stored** (`ledger_pending`). A test is done when its latest row is a pass whose commit is still reachable from its branch (`git merge-base --is-ancestor`, read-only) and whose image hash matches the rebuild the caller names. Otherwise it is listed with its reason: `never-run`, the last non-pass result, `commit-unreachable` (folded or rebased away) or `image-changed`. Listed tests split into `runnable_now` and `by_missing_role`; a test missing two roles appears under each, with `missing` saying so. Hardware named in the header's `broken` list counts as missing though attached. **An image hash is compared only when both sides are known**: a caller that names no current image never gets a rerun from the hash alone. The hash is SHA-256 of the artifact file the caller points at.

**Attached comes from Core, and the answer says so.** When Core cannot be reached the view falls back to `bench.json`'s `attached` and reports `attached_source: "bench.json"` and Core's error, never presenting the fallback as a reading.

**`run_study` returns when the study is submitted, not when it ends, so its row is appended `submitted` and closed later.** A new `test` param (`--test`) names the ledger test; the project is the one named, else the open desk's, and with neither the row is skipped and the result says why. `ledger_show` and `ledger_pending` first close every `submitted` row whose study has ended by appending a second row for the same study: `pass` only if Core says `completed` **and** every step's own outcome was a pass, `fail` for `failed` or any other step outcome, `interrupted` kept as itself. A study Core no longer knows or still runs stays `submitted`, which the pending view treats as not done. This reads a verdict off the result Core already holds and infers nothing about the DUT. The cost is that a finished study lands only when someone next looks.

**`ledger_add` refuses a test id absent from a non-empty `tests.toml`**, so a typo cannot start a second history, and accepts `pass`, `fail` or `skipped`; `submitted` and `interrupted` are the system's. Branch and commit default to the tree's own; roles to Core's. `broken` replaces the header's list.

**Flat names, `ledger-add` / `ledger-show` / `ledger-pending`**, so the tool-subcommand parity rule holds with no documented asymmetry.

**Not verified:** unit-tested (the pending logic against a stub reach, the files, a real throwaway git repo) and run against a mock Core only. No study has landed a row on a bench and the pending view has not been compared with a real topology; see `open.md`.
