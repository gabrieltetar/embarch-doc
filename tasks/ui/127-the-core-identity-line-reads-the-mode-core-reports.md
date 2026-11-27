# 127 — The Core identity line reads the mode Core reports

**State:** open
**Source:** EMB-580 — UI Core identity line reads the mode Core reports
**Issue:** EMB-580
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Ui decision 112's identity line (`decisions/core-identity.md`) derives `service`
or `development` from the attestation's match result, because the shared client
used to drop the `mode` Core reports. It no longer does: `StatusResponse` now
carries `mode` and `keyid`, each `Option<String>`, `None` for a Core that
predates them (api decision 139, `embarch-doc/embarch-api/decisions/client-crate.md`,
read only). So a development Core whose key happens to be the recorded installed
fingerprint reads `service` today. When this is done:

- **The line's mode is the mode Core reported.** `None` reads as unknown, never
  `service`. The match against the installed fingerprint still decides the
  verdict half of the line and the warning, as 112 says.
- **`src/snapshot.rs`'s comment that the client drops the field is corrected.**

## Where to look

- `src/snapshot.rs`: the identity derivation (`CoreIdentity`) and its tests
- `embarch-doc/embarch-ui/decisions/core-identity.md` (112)

## Where the doc goes

Decision 112 amended in `decisions/core-identity.md`, or a new decision beside
it. **`embarch-ui/spec/tabs.md` is in reserve** (906 B left; `tasks/ui/126` is
open against it): do not grow it. Its "Every tab" line already says "mode", so it
needs no edit.

## Done when

- [ ] The identity line reads `StatusResponse.mode`.
- [ ] A test covers a development Core whose key matches the installed
      fingerprint (reads `development`), and a Core that reports no `mode`
      (reads unknown, not `service`).
- [ ] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
