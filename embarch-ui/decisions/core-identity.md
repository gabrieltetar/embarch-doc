# embarch-ui decisions: Which Core the UI shows it is talking to

**Status:** active, 2026-11-26.

### 112 — One line under the top bar on every tab names the Core: mode, 16 hex of its fingerprint, and whether it is the installed one

A development Core must not pass for the attested one (HIL design, "The root of trust"), so the person sees which Core answers on every tab (EMB-336). **`snapshot::poll` adds `core.attestation()` to its join, and `CoreIdentity::from_attestation` builds the words once**; the page (`renderCoreIdentity`, `#core-identity`) only draws `snapshot.core_identity` with `textContent`. The client caches its attestation per connection, so the poll costs no extra challenge.

- **`Core: service, <16 hex>, matches the installed fingerprint`** when the client's `matches` is true; **`Core: development, <16 hex>, does not match`**, drawn as a warning (danger colour, bold), when false; **`Core: mode unknown, <16 hex>, no attested install on this machine`** when there is no installed fingerprint to compare.
- **No fingerprint at all** gives a line that says so: `no attested install on this machine` on a machine with no `core-fingerprint` (not a warning), and `did not report a mode or fingerprint (<why>)` as a warning when the challenge failed, as a Core too old for it does.
- **No act is blocked here.** The client's token rule (`embarch-api` 109) already decides what is sent; the line only shows it.

**The mode is derived, not read.** Core's `/status` carries `mode` and `keyid` (`embarch-core` 129) but `embarch-core-client`'s `StatusResponse` drops both and the UI holds no raw Core access (103), so `service` means "Core's key is the installed one" and `development` means "it is not". A development Core whose key was installed as the fingerprint would read `service`. When the client passes `mode` through, read it and drop the derivation (EMB-576) [assumed: not exercised against a live Core].
