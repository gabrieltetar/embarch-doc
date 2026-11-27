# embarch-ui decisions: Which Core the UI shows it is talking to

**Status:** active, 2026-11-26.

### 112 — One line under the top bar on every tab names the Core: mode, 16 hex of its fingerprint, and whether it is the installed one

A development Core must not pass for the attested one (HIL design, "The root of trust"), so the person sees which Core answers on every tab (EMB-336). **`snapshot::poll` adds `core.attestation()` to its join, and `CoreIdentity::from_attestation` builds the words once**; the page (`renderCoreIdentity`, `#core-identity`) only draws `snapshot.core_identity` with `textContent`. The client caches its attestation per connection, so the poll costs no extra challenge.

- **`Core: service, <16 hex>, matches the installed fingerprint`** when the client's `matches` is true; **`Core: development, <16 hex>, does not match`**, drawn as a warning (danger colour, bold), when false; **`Core: mode unknown, <16 hex>, no attested install on this machine`** when there is no installed fingerprint to compare.
- **No fingerprint at all** gives a line that says so: `no attested install on this machine` on a machine with no `core-fingerprint` (not a warning), and `did not report a mode or fingerprint (<why>)` as a warning when the challenge failed, as a Core too old for it does.
- **No act is blocked here.** The client's token rule (`embarch-api` 109) already decides what is sent; the line only shows it.

**The mode is read, not derived (EMB-580, 2026-11-26).** `snapshot::poll` passes `StatusResponse.mode` (`embarch-core` 129, passed through by `embarch-api` 139) to `CoreIdentity::from_attestation`, and the line's `service`/`development` is that string. `None`, a Core that predates the field, reads `mode unknown`, never `service`. The match against the installed fingerprint decides only the verdict half and the warning, so a development Core whose key was installed as the fingerprint reads `Core: development, <16 hex>, matches the installed fingerprint` [assumed: not exercised against a live Core].
