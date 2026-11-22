# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **Seven paths have never met their real counterpart** (`POST /bootload`, signal tap, decisions 35, 106, 89, 92, 93), each with its owner-run step: [open/never-exercised.md](open/never-exercised.md).

- **Decision 108's rename has not reached the installed service.** Built natively on Windows in a scratch copy on 2026-11-10, never deployed, so the bench's Core still serves `firmware_version`, and a caller built after the rename reports the bench's build as unknown against it. Owner-run: deploy (`embarch-dev-workflow.md` §4a), then `embarch-api dev-bench-hello` prints `dev_bench_version`.

## Scope is carried, and enforced on one route

- **Decision 109's scope is enforced by the discard alone** (decision 112) and recorded in the signed run record (decision 110: each declaration's scope), and by the run log's publish and discard entries. The lease holder, `hw_holder` and the logs carry none; `measurements.json` carries it (decision 113); M1.8 adds it where it needs it. The person token file's `icacls` lockdown on Windows is unrun, and `embarch-ui` is the one client sending the person's token (its decision 103), and nothing in it calls the discard yet.

- **Decision 110's declarations ledger is in memory.** A declaration made before this Core started is not in a run's record, which says so (`witnessed_since_utc_ms`). **The run log is a natural home for it** (an append-only, chained file Core already writes), as `declared` entries replayed at start; not built here, since Core's protected store is the attested phase's. A declaration outside the five the ledger watches (a tap's declared origin) is not stamped yet; a study value takes the submitting token's scope (decision 113). **Windows ACL debt:** the `signing-key` file's `icacls` lockdown is unrun, as `person-token`'s is, and `run-log.jsonl`'s now too. From the main checkout in a Windows session, start Core natively, then `icacls %ProgramData%\embarch\signing-key` (and `run-log.jsonl`, after a run) must list only the running account, `SYSTEM` and `Administrators`, and a second start must print `reusing the existing signing key` with the same `keyid` in `core.log`. A worktree cannot build it.

- **The run log's tail is not anchored** (decision 111): cutting its last lines leaves a valid chain. M1.8's publish must record the head from `GET /study/{id}/log` beside the manifest hash, and `verify` check 8 compare it; until then a tail cut is undetectable. A run a crash cut off mid-way has no entry and is swept like any run, and an entry that fails to write is logged at `error` and leaves the run unprotected.

- **"A pending requirement" has no store** (milestone 1 has no Test phase): `RunLog::discard`'s `clean` test is where a requirement holding a run would refuse the agent too. Not built.

## Unverified diagnoses

- **Whether probe-rs writes killed the nRF54L15 is evidence, not proof** (decision 36): a J-Link erase-and-program recovered the board, but a full reprogram may have cleared something else.

## Designed, not built

- **`core.toml`** (decision 11), narrowed to `bind`/`port`.
- **A `{code, message, cause}` JSON error body** — deferred, cross-repo: the `code` enum is a wire contract three consumers branch on (decision 12).
- **A subject discriminator on `Alert`** so a signal mismatch reaches `/alerts` (decision 30); not needed until a direct route is physically possible.
- **An HTTP surface, SSE stream, or `embarch-api` tool for `dev-bench.log`** (decision 37); nothing has asked.
- **A byte count alongside `GET /serial-log`'s `truncated: bool`** — rejected (decision 58) until a caller must tell 1 byte lost from 900 KB.


## Structural limits

- **Espressif-family dev-bench port selection has no current story.** Decision 23's removed env overrides had no replacement: `link_port_interface` answers an ambiguous-VCOM board, and the ESP32-C5-WROOM-1 DK is **[assumed]** to enumerate as one USB-Serial/JTAG interface with no VCOM to name (`tasks/core/028`). Confirming needs the board; the missing knob outlives it.
- **A separate-machine deployment has no artifact transfer.** Multipart (decision 10) closed WSL2; a LAN Pi cannot flash.
- **macOS is reasoned-only.** Nothing here has run on a Mac.

## Moved elsewhere, not resolved

- **Discarding a signal port's buffered input on open is not sufficient; the defence is now `embarch-ui`'s** (decision 30). A capture began with **18 stale records** seconds off — those bytes sit inside the USB-UART bridge, past an OS-level purge. Fix built as `embarch-ui` decision 19; unresolved is that it has never met the real prefix ([embarch-ui/open.md](../embarch-ui/open.md)).
