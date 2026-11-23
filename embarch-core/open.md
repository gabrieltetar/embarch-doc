# embarch-core: open questions

**Status:** active, 2026-09-02.

What is unresolved and what would close it. Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Never exercised

- **Seven paths have never met their real counterpart** (`POST /bootload`, signal tap, decisions 35, 106, 89, 92, 93), each with its owner-run step: [open/never-exercised.md](open/never-exercised.md).

- **Decision 108's rename has not reached the installed service.** Built natively on Windows in a scratch copy on 2026-11-10, never deployed, so the bench's Core still serves `firmware_version`, and a caller built after the rename reports the bench's build as unknown against it. Owner-run: deploy (`embarch-dev-workflow.md` §4a), then `embarch-api dev-bench-hello` prints `dev_bench_version`.

## Scope is carried, and enforced on one route

- **Decision 109's scope is enforced by the discard alone** (decision 112) and recorded in the signed run record (decision 110: each declaration's scope), and by the run log's publish and discard entries. The lease holder, `hw_holder` and the logs carry none; `measurements.json` carries it (decision 113); the publish's `report-data.json` carries it (decisions 117, 119). The person token file's `icacls` lockdown on Windows is unrun, and `embarch-ui` is the one client sending the person's token (its decision 103), and nothing in it calls the discard yet.

- **Decision 110's declarations ledger is in memory**, so a declaration made before this Core started is not in a run's record (`witnessed_since_utc_ms`). **Windows ACL debt, owner-run:** `icacls` on `signing-key` and `run-log.jsonl` (steps and the expected output in [open/scope-and-ledger.md](open/scope-and-ledger.md)); a worktree cannot build it.

- **The run log's tail is anchored only from a publish on** (decisions 111, 118): a publish records the head it ended at beside the manifest hash, so a tail cut *before* that head is detectable, one after the last publish is not. `verify` check 8 (api decision 121) checks a zip's segment against the signed head; the publish's own entry is not checkable offline. A run a crash cut off mid-way has no entry and is swept like any run; an entry that fails to write is logged at `error` and leaves the run unprotected.

- **"A pending requirement" has no store** (milestone 1 has no Test phase): `RunLog::discard`'s `clean` test is where a requirement holding a run would refuse the agent too. Not built.

## Unverified, and moved elsewhere

- **Whether probe-rs writes killed the nRF54L15** (decision 36) and **the stale bytes a signal port's open cannot discard** (decision 30, `embarch-ui` decision 19): [open/unverified-and-moved.md](open/unverified-and-moved.md).

## Designed, not built

- `core.toml` (decision 11), the `{code, message, cause}` error body (12), an `Alert` subject discriminator (30), a `dev-bench.log` surface (37), a `truncated` byte count (58, rejected): [open/designed-not-built.md](open/designed-not-built.md).

## Publish, not yet complete

- **A republish after the retention sweep needs the caller to resend the earlier zip's files** (decision 120): Core takes them back checked against its own logged manifest, so what stays open is embarch-api sending them (`tasks/api/172`). The run log's segment is the whole log to the head, not one unit's.

## Structural limits

- **Espressif-family dev-bench port selection has no current story.** Decision 23's removed env overrides had no replacement: `link_port_interface` answers an ambiguous-VCOM board, and the ESP32-C5-WROOM-1 DK is **[assumed]** to enumerate as one USB-Serial/JTAG interface with no VCOM to name (`tasks/core/028`). Confirming needs the board; the missing knob outlives it.
- **A separate-machine deployment has no artifact transfer.** Multipart (decision 10) closed WSL2; a LAN Pi cannot flash.
- **macOS is reasoned-only.** Nothing here has run on a Mac.
