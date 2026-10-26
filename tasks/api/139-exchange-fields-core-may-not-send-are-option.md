# 139 — The exchange fields an older Core does not send are `Option`, per decision 58

**State:** open
**Source:** the `api/138` reviewer's below-bar note, 2026-10-26, which the supervisor read as a real contradiction of decision 58 (`embarch-api/decisions/client-crate.md`) and filed rather than reverted.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`api/138` (code `dd49a1f`) added `bytes_read: usize`, `echo_seen: bool`, `written: bool` and `port_lost: bool` to `SignalExchangeResponse` in `crates/embarch-core-client/src/client.rs` as bare `#[serde(default)]` values. Decision 58 says every response field Core may not yet send is `Option<T>` with `#[serde(default)]`, "matching the existing fields in shape, not merely in having a default", so that a value Core did not report is never presented as a fabricated one. Against a Core older than `embarch-core` decision 85 — which is what the live Core on this machine is until the owner redeploys it — every exchange now reports `bytes_read: 0` beside non-empty text and `written: false` in the MCP and `--json` output, and `written: false` is the one value decision 85 exists to stop a caller misreading as "safe to resend".

When this is done those four fields are `Option`, absent stays absent in the serialized output, `wire_notes` and `exchange_problem` read `None` as "this Core did not say", and decision 82's amendment no longer needs the "false means unknown" caveat. Check `FlashResponse.erased` (`api/134`, a bare `Vec` default) against the same rule and either make it `Option` too or record in decision 58 why an empty list is not a fabricated answer.

## Why now

The fields shipped an hour ago and nothing reads them yet except the CLI and MCP text this crate owns, so the change is cheapest now. Decision 58 was written after `validated_at_utc_ms` broke the same rule once.

## Done when

- [ ] The four fields are `Option<_>` with `#[serde(default)]` (and skipped when `None` on serialize); the old-body test asserts `None`, not `false`/`0`.
- [ ] `wire_notes` and `exchange_problem` say nothing false against an old body; a test covers an old-shape reply with text.
- [ ] `FlashResponse.erased` is decided one way or the other, and the decision says which.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); decision 82's amendment and the `signal_exchange` row in `interfaces/tools-topology.md` updated; `changelog.d/` fragment dropped.
