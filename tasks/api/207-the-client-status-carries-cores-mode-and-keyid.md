# 207 — The client's status carries Core's mode and keyid

**State:** open
**Source:** EMB-576 — StatusResponse drops Core's mode and keyid
**Issue:** EMB-576
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core's `/status` body carries `mode` and `keyid` (core decision 129), and
`embarch-core-client`'s `StatusResponse` has neither field. So the UI's Core
identity line (ui decision 112) derives `service` or `development` from the
attestation's match result rather than reading the mode Core reports: a
development Core whose key was recorded as the installed fingerprint reads
`service`. When this is done:

- **`StatusResponse` carries `mode` and `keyid`**, each `Option<String>` with
  `#[serde(default)]`, `None` for a Core that predates them.
- **A test parses a status body with both and one with neither.**

`embarch-core-client` is a shared crate. A new `pub` field breaks any consumer
that builds `StatusResponse` by struct literal. None did on 2026-11-26
(`embarch-ui`, `embarch-umbrella`, this repo), but check again, and say in your
report what you found. You do not write the consumers. Switching the UI's line to
the reported mode is ui's follow-up; file it with `scripts/fleet-linear.py file
--from worker --project embarch-ui` once this lands.

## Where to look

- `crates/embarch-core-client/src/client.rs`: `StatusResponse`
- `embarch-core/src/api.rs`: the status body, read only
- `embarch-doc/embarch-core/decisions/` (129), read only
- `embarch-doc/embarch-api/decisions/client-crate.md`

## Where the doc goes

A line in an existing client-crate decision, or a new one if none covers the
status type; the interface doc that lists the client's status. **`embarch-api/spec.md`
is in reserve** (1,110 B left; its compaction `tasks/api/201` is blocked): do not
grow it.

## Done when

- [ ] `StatusResponse` carries `mode` and `keyid`; a test parses both shapes.
- [ ] The decision and interface doc say so.
- [ ] Gate green (`cargo build --workspace`, `test`, `clippy --all-targets -- -D warnings`).
