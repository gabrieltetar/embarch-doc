# embarch-api: the live log

**Status:** active, 2026-11-23 (`tasks/api/180`). A readable mirror, in the firmware repo, of the calls `embarch-core` logged in its own call log (`embarch-core` decision 122). Core's log is the record; this file is for the engineer reading a Live session back, and is not signed. No decision of its own: it records what the design note for the live log fixed, and `embarch-atlas` ([EMB-266, EMB-267]) writes to the same file.

## When a line is written

One line per MCP tool call or CLI subcommand that **reached a lease-gated route** (`embarch-core`'s `LEASE_GATED`, a copy of which is `lease_gate.rs`), written **after Core answered**, a refusal included. A call that reached none (`list_projects`, `build`, `status`, `call_log`, a `lease_*` call) writes nothing. `run_study` and `run_host_study` write nothing either: a study is not Live, and its steps stay in its own `events.json`. A tool that makes several gated calls (`bench_exchange`) writes one line citing all of them.

The line is written by the process that made the call, from what its HTTP client saw: the route, the JSON body sent (kept when it is JSON of at most 4096 bytes, as Core keeps its own), the status, and `X-Embarch-Call-Seq` / `X-Embarch-Call-Hash` / `X-Embarch-Call-Repeat` off the answer. Only inside a `call_trace::scope`, so `embarch-ui` and the other users of `embarch-core-client` collect nothing.

## Where

`<repo>/embarch/live/<date>-<session>.jsonl`, untracked like the rest of `embarch/`.

- **`<repo>`** is the nearest directory from the working directory up to its git root that holds an `embarch/` folder; failing that the configured project's `source_path` (the call's `project`, else the only configured one). With neither there is **no line**: the CLI says `live log: no line written (...)` on stderr and an MCP result carries the same sentence as a second text block. A write that fails says so the same way. The call itself is unaffected.
- **`<date>-<session>`** is the live lease's start date, then its holder (every character that is not an ASCII letter or digit turned into `-`), then the start time as `HHMMSS`: `2026-11-23-claude-gabriel-210000`. The date and `HHMMSS` are sliced out of the lease's `started_at` text **as Core wrote it, with no zone conversion** (UTC when Core stamps in UTC; Core's is the authority). With no lease live it is `<today>-no-lease`, `<today>` being UTC `now`, the same clock as `t`. A second writer reads the lease's start the same way.
- **Append mode, one `write` of the whole line**, so `embarch-atlas` appends to the same file and a reader never sees half a line. The directory is created on the first write.

## The line

One JSON object, one line, UTF-8.

| Field | Meaning |
|---|---|
| `schema` | `"embarch-live/1"`. The atlas writes it too. Bumped by hand on a rename, removal or retype of a field. |
| `t` | UTC time the line was written, `YYYY-MM-DDTHH:MM:SSZ`: after Core answered, not when it was asked |
| `writer` | `"embarch-api"`. The atlas writes `"embarch-atlas"` |
| `via` | `"mcp"` or `"cli"` |
| `tool` | The MCP tool (`mem_read`) or the subcommand (`mem-read`) |
| `sent` | What was asked: the tool's arguments as an object (MCP), or the subcommand as the CLI parsed it, a string. embarch-api's CLI writes the Rust debug form of the parsed subcommand (`MemRead { ... }`), **not** a command line. The atlas writes a command line (`reg-read X --role y`) and the tool's arguments as an object over MCP. A reader may rely on the object-or-string split, not on a string's grammar: it differs by writer, so branch on `writer` |
| `board` | `{role, probe_serial, chip}`, each `null` when unknown: the first of each that any gated call's body named, else the tool's arguments, else the answer's |
| `image_sha256` | The sha256 `GET /status`'s `last_images` holds for the board (the entry for its probe serial, else its chip), or `"unknown"`. Unknown is not "nothing flashed": Core's record is in memory and a flash by another tool does not appear |
| `ok` | The tool succeeded (MCP: not an error result; CLI: exit 0) |
| `answer` | `{text, bytes, sha256, truncated}`: the answer as the caller got it (the human text for the CLI), cut on a character boundary past 4096 bytes, with the **full** answer's length and SHA-256 |
| `core` | One object per gated call, in order: `{seq, hash, repeat, method, path, status}`. `seq` and `hash` are Core's call-log entry (`null` against a Core that sent none); `repeat` is set when an identical read folded into entry `seq`; `status` is the HTTP status, so a refusal is a `409` here and `ok` false |
| `session` | `{holder, started_at}` of the live lease, or `null` |

**A writer's own fields.** The fields above are the contract every writer fills. A writer may add others, which is no `schema` bump, and records them in its own docs; a reader tells writers apart by `writer` and ignores a field it does not know. The atlas adds `outcome` (`answered`, `did-not-run`, `refused`, `no-reply`, `may-have-run`; [embarch-atlas design](../../embarch-atlas/design.md)). embarch-api writes none: its `ok` and `core[].status` carry the same fact.

The 4096-byte cap is chosen, not measured.

## Reading Core's entries

- **`--json`** adds `core_calls` (the `core` array above) to the object of any subcommand that reached a gated route, so a caller can cite the entries without reading the file. It is on a **failed** call too (a refusal, a non-zero exit) when the call reached a gated route, and absent when it reached none. Adding a field is not a `schema_version` bump.
- **`call_log`** (tool) and **`call-log`** (subcommand): `GET /call-log`, by `seq` (one entry; an entry's `seq` is its position) or `from` (inclusive) to `to` (exclusive), the whole log by default and at most Core's cap per answer (`truncated` says so). `verified` says whether the chain checks out. Not lease-gated, so it writes no line.

**Not verified on a bench** ([open.md](../open.md)): everything here ran against a mock Core.
