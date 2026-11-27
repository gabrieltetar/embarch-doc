# embarch-core: open questions

**Status:** active, 2026-11-23.

What is unresolved and what closes it. Truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

## Never exercised

- **Seven paths never met their real counterpart** (`POST /bootload`, signal tap, 35, 106, 89, 92, 93), each with an owner step: [open/never-exercised.md](open/never-exercised.md).

- **Decision 108's rename has not reached the installed service.** Built on Windows in a scratch copy 2026-11-10, never deployed: the bench's Core serves `firmware_version`, so a caller built after the rename sees the build as unknown. Owner-run: deploy (`embarch-dev-workflow.md` §4a); `embarch-api dev-bench-hello` prints `dev_bench_version`.

## Scope is carried, and enforced on one route

- **Decision 109's scope is enforced by the discard alone** (112), recorded in the signed run record (110) and the run log's publish and discard entries. The lease holder, `hw_holder` and the logs carry none; `measurements.json` (113) and `report-data.json` (117, 119) carry it. The person token file's Windows `icacls` lockdown is unrun; `embarch-ui` alone sends the person's token (its decision 103) and does not call the discard yet.

- **Decision 110's declarations ledger is in memory,** so a declaration from before this Core started is not in a run's record (`witnessed_since_utc_ms`). **Windows ACL debt, owner-run:** `icacls` on `signing-key` and `run-log.jsonl` (steps and expected output: [open/scope-and-ledger.md](open/scope-and-ledger.md)); a worktree cannot build it.

- **The run log's tail is anchored only from a publish on** (111, 118): a publish records its head beside the manifest hash, so a tail cut before it shows, one after the last publish does not. `verify` check 8 (api 121) checks a zip's segment against the signed head; the publish's own entry is not checkable offline. A run a crash cut off has no entry and is swept like any run; an entry that fails to write is logged and leaves the run unprotected.

- **"A pending requirement" has no store** (no Test phase): `RunLog::discard`'s `clean` test is where a requirement would hold a run. Not built.

- **The call log's `board` is named by four handlers only** (`/flash`, `/reset`, the two live reads; 122): `/bootload`, `/validate`, exchange and capture leave it null. An expired lease leaves a fold pending till the next call. No client sends the quota route (161). A device study is not stopped on a full log (158).

## Unverified, and moved elsewhere

- **Whether probe-rs writes killed the nRF54L15** (36); **the stale bytes a signal port's open cannot discard** (30, `embarch-ui` 19): [open/unverified-and-moved.md](open/unverified-and-moved.md).

## Designed, not built

- `core.toml` (11), the `{code, message, cause}` error body (12), an `Alert` subject discriminator (30), a `dev-bench.log` surface (37), a `truncated` byte count (58, rejected): [open/designed-not-built.md](open/designed-not-built.md).

## Publish, not yet complete

- **A republish after the retention sweep needs the caller to resend the earlier zip's files** (decision 120): Core checks them against its logged manifest; open is embarch-api sending them (`tasks/api/172`). The segment is the whole run log.

- **A Test run's captures are held until it is published** (144, 149): a `published` entry naming its `run_id` releases them. A resumed pair is not published as one zip (153).

## Structural limits

- **Espressif dev-bench port selection has no story.** Decision 23's removed env overrides had no replacement: `link_port_interface` answers an ambiguous VCOM, and the ESP32-C5-WROOM-1 DK is **[assumed]** one USB-Serial/JTAG interface, no VCOM to name (`tasks/core/028`). Confirming needs the board; the knob stays missing.
- **A separate machine has no artifact transfer.** Multipart (10) closed WSL2; a LAN Pi cannot flash.
- **macOS is reasoned-only.** Nothing has run on a Mac.
