# embarch-umbrella: the `doctor` chain

**Status:** active, 2026-09-10. Split verbatim out of [../spec.md](../spec.md) §"The
`doctor` chain" the same day, when that file reached its size cap
([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2) — a reference table, not cut, the same
way [embarch-core/interfaces/constants.md](../../embarch-core/interfaces/constants.md)
split out of that sub-project's `spec.md`. `tasks/umbrella/038` is the blocked compaction
task for this table; this split moved it, not rewrote it.

Index: [../decisions.md](../decisions.md). Current truth for the rest of `embarch-umbrella`:
[../spec.md](../spec.md).

Ordered; each emits pass/warn/fail plus a concrete fix line.

| # | Check |
|---|---|
| 1 | Both binaries found; versions match the suite manifest. **A missing `embarch-core` is a warn where none belongs** (`wsl-host`, `remote`). Each binary is found by a **reading** where one exists, never `PATH` alone (decisions 38, 42) |
| 2 | Core service installed, and running |
| 3 | Core reachable — reports **which candidate won** and the resolved class |
| 4 | Token resolves and matches (a `200`, not a `401`) |
| 5 | At least one probe visible — a count off `/status`. Zero is a warn, **except on Linux with Core on this machine**, where a known debug-probe vendor ID in `/sys/bus/usb/devices` is **Fail — attached but not permitted**, with the udev fix line (decision 18) |
| 6 | `embarch-api` itself accepts the config, via shell-out (decision 16); else a permissive warn-only read |
| 7 | Each project's build entrypoint resolves to an executable — branching on discovery kind |
| 8 | Chip is not still the placeholder (static); at least one real target exists (zephyr-west) — by shelling out to the located `embarch-api`'s own listing (decision 17) |
| 9 | Artifact paths name **the same file**; for zephyr-west, that the path translation itself succeeds |
| 10 | Registered **and answering**: reads the registration out of the agent CLI's own config by the binary it names rather than only the key `embarch`, spawns it, and completes one JSON-RPC `initialize` over stdio within 10 s. An entry with nothing to spawn is a warn, never a pass (decisions 23, 37, 40) |
| 11 | The study-designer schema versions: Core's served host version against the **located `embarch-api`**'s compiled one, plus **Core's own `compatible` verdict** on the bench's wire version, plus this binary's own constant as a mixed-install warn. The `/dev-bench/hello` fetch behind that verdict, and behind check 13, gets its own 10 s budget rather than the 500 ms the reads get (decision 44) |
| 12 | Dev-bench port detected — informational; absent is an expected state |
| 13 | Dev-bench firmware version matches the local checkout's `git describe` — no checkout configured, and a reported id no longer in that checkout's history, are each their own fail rather than a warn or an ordinary mismatch (decision 47) |
| 14 | Which program Core would flash each chip family with, by running the located binary — on `wsl-host`, the service's own exe, **measured** (decision 38). Unlocatable is one skip worded per class, not a flashing verdict — each wording is reachable only before *that* class's own `setup` finishes (decision 31) |
| 15 | The running Core's `core_version` is the located `embarch-core` binary's — a **cross-version** stale deploy, and blind to a same-version one |
| 16 | `study_results/` entries and their bytes **at the directory it names**, and build directories per project — informational (decisions 26, 39) |
| 17 | Core's bind address matches what this topology needs — the class `setup` recorded, against the address `/status` was reached at and against the service's own registered `--bind` (decision 22) |
| 18 | Tail of Core's log file, informational — **design-only** ([embarch-core](../../embarch-core/decisions/logging.md)'s daily-rolling log) |

Checks 12, 15 and 16 never fail the run outright; **5, 11, 13 and 17 do**, each only for the states its row names ([../decisions/schema-skew.md](../decisions/schema-skew.md) for why 11 is allowed to). A number a check simply could not obtain is a warn naming which one, never a pass.

**A row naming several arms says which have run, not only which were written.** `measured` above cites a live run (decision 38); prose alone, as check 14's per-class skip wording is, means reasoned but not observed — the convention this table now follows.

1-17 are what the code emits; **18 is designed and unbuilt, and it is not the only such item** — 26's `--prune` half sits *inside* a shipping command, marked above where it lives, and [../open.md](../open.md) carries whether it is still wanted. 18's number moves if something is built before it. `--json`'s per-check object — its fields, always present, and which carry a `code` (checks 1, 5, 10, 13, 14, 17) or a `path` (check 16) — is [../decisions/reporting.md](../decisions/reporting.md)'s contract.

Every `detail` and `fix` is **one line with no run of two or more spaces**; another program's raw output is normalised at the point it is interpolated, not exempted from the rule ([decision 43](../decisions/message-rendering.md)).
