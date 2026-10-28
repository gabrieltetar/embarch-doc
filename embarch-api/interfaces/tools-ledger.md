# embarch-api: ledger tools

**Status:** active, 2026-10-28. The hardware test ledger ([decisions](../decisions/ledger.md) 98); see [tools.md](tools.md) for the one-table premise. Each tool is also a kebab-case subcommand, `--project` defaulting to the open desk's.

Files, in `<project source_path>/embarch/ledger/`:

- `tests.toml`: `[[test]]` with `id`, `title`, `pass` (criterion, prose), `image`, `needs` (role, board-name or instrument names) and `notes`.
- `rows.jsonl`: append-only; per row `when`, `branch`, `commit`, `image_hash`, `roles`, `test`, `result`, `study_id`, `notes`.
- `bench.json`: `{ "attached": [..], "broken": [{ "what": "partner", "note": "port 2 dead" }] }`. Hand-editable; `attached` is the fallback when Core is unreachable.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `ledger_add` | `test`, `result` (pass/fail/skipped), `project?`, `notes?`, `image_path?` or `image_hash?`, `study_id?`, `commit?`, `branch?`, `roles?`, `broken?` | Appends a row. Branch and commit default to the tree's, roles to Core's attached set. `broken` replaces the header's list, empty clears it. Refuses an unknown test id when `tests.toml` has any |
| `ledger_show` | `project?`, `test?`, `limit?` (20) | The header (attached and its source, known broken) and the last rows, newest last. First settles `submitted` study rows whose study ended |
| `ledger_pending` | `project?`, `attached?`, `image_path?` or `image_hash?` | `runnable_now` and `by_missing_role`, each item with `reason` (`never-run`, last non-pass result, `commit-unreachable`, `image-changed`) and `missing`; `attached_source` says whether Core, `bench.json` or the argument answered |
| `run_study` (`--test`) | `test?` | Appends a `submitted` row for the project named or the open desk's; the result's `ledger` says `appended` or `skipped` and why |

**Not verified on a bench** ([open.md](../open.md)).
