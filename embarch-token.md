# EMBARCH_TOKEN

**Status:** active, 2026-09-02.

The single shared secret authenticating every caller of Core's HTTP API. **The source of truth for its full lifecycle** — generation, storage, transport, security model, rotation, known gaps. Component docs link here rather than restate it.

## 1. What it is

**A single opaque string, shared across every caller.** Not a JWT, not signed, not structured — Core does a plain exact-string comparison against every request's bearer header. **No expiry, no issued-at, no claims:** it is valid until the token file is deleted and Core regenerates one, or an explicit override changes it.

**Two ways a value gets chosen, in strict precedence order:**

1. **An explicit override** — the env var on Core, or an inline value or env-var name in the API's config. **If set it is used as-is; no file is read or written.**
2. **Auto-generated and persisted**, when nothing explicit is set: **Core generates a random value on first startup and persists it to a machine-wide file**, so the same value survives a restart. The API reads that same file when nothing is configured.

**That replaced a hardcoded insecure default entirely.** An unset token used to fall back to a literal `dev-token-change-me` with a warning — **a known-insecure value baked into the binary.** It is gone, and Core logs loudly either way — on generating a new token *and* on reusing an existing one — **so which happened is never silent.**

## 2. Where it lives

| Component | How it holds the token |
|---|---|
| **Core**, HTTP server and foreground CLI alike | The env var if set; otherwise the token file if present, or generate one and write it there. **Local CLI operation is not a separate credential** |
| **`embarch-api`** | Its config's inline value or env-var name (the latter wins if both are set); **otherwise the same token file Core uses.** If neither resolves it **fails to start with a clear error** rather than proceeding unauthenticated |

**Beyond process memory, the API's own config file and the token file are the only two places the token is ever written to disk.** Stored inline in a config, that file wants owner-only permissions and exclusion from version control — identical treatment to any other local secret.

### The auto-generated token file

**A canonical, machine-wide path per OS, independent of which account runs Core or the API** — `%ProgramData%\embarch\token` on Windows, `/var/lib/embarch/token` on Linux and macOS. **That is what lets an installed Windows service, typically running as a different account than the interactive user, still find the same file.**

Core creates the directory and file with **owner-restricted permissions**. On Windows that means **explicitly granting only the creating account, `SYSTEM` and Administrators rather than relying on `ProgramData`'s default inheritance, which is more permissive than a user-profile directory** — done by shelling out to `icacls` rather than through an ACL crate, **a thin and infrequently-updated wrapper worth avoiding for a security-relevant, Windows-unvalidated operation.**

**WSL2⟷Windows discovery**, since that is this suite's primary split: the API under WSL2 **resolves the real `%ProgramData%` value by shelling out to the Windows side rather than hardcoding `C:\ProgramData`, which could be wrong on a machine that customized it**, then maps the result through WSL2's mount convention to read the same file.

**Scope limit, and it is structural.** This bridges same-machine deployments only — **including the WSL2 split, since both sides are really one physical machine** — not a genuinely separate host. A Core on a real LAN box **has no local file for the API to discover at all**, so that case needs explicit config. **No filesystem convention can bridge two actual machines.**

## 3. Transport and security model

Every request carries the token as a bearer header, checked by exact-string comparison. **There is no TLS anywhere in this path** — Core's server is plain HTTP — **so the token crosses the network in cleartext on every call.**

- **Single shared secret, no per-caller identity.** The same token authenticates Core's own local process and any remote API caller: **Core can tell "authorized" from "not", never "which caller."** Adequate for the suite's single-engineer scope.
- **The token's confidentiality in transit relies entirely on the trustworthiness of the network segment it crosses** — localhost, a WSL2 loopback, or eventually a LAN.
- **The threat model, explicitly:** this protects against **an unauthenticated stranger on the same network hitting Core's endpoints directly.** It does **not** protect against anyone with access to the machines running Core or the API — env vars, config files and process memory are all readable at that level — **nor against network-level eavesdropping. An appropriate trade-off for a single-engineer local tool, not an oversight, but worth stating plainly rather than leaving implicit.**

## 4. Rotation

**No hot-reload on either side** — both read the token once at startup, **so rotation always requires restarting both.** Accepted rather than designed around: no dual-token grace window, no config-reload mechanism.

**To rotate an explicit override:** pick a new value, update wherever Core reads it from — the shell environment for a foreground run, or **the service's own registration for an installed service** — restart Core, update every API config to match, then restart or reconnect each API instance.

**To rotate an auto-generated token:** delete the file, restart Core — **it regenerates one on next startup since the file is now absent** — then restart or reconnect every API instance. Simpler, since there is no value to pick or copy between two places.

**Because there is no grace window, any call made after Core's restart but before every API instance re-reads the new value will fail authentication until they agree.** Acceptable downtime for one engineer rotating their own token, **but worth knowing before doing it mid-session.**

**This doc does not prescribe *when* to rotate** — no expiry, no cadence. That judgment is the engineer's: suspected exposure, a machine change.

## 5. Known gaps and open questions

**Every item below was re-examined in a suite-wide design pass and every one was deliberately kept open rather than answered — the repo owner's explicit call.** Worth stating at the top, because **a list of open security questions reads as neglect when it is in fact a posture**: today every byte of this token stays on one machine's loopback, where **TLS buys nothing, per-caller identity distinguishes one caller from itself, and a rotation cadence protects against nothing that is happening.**

- **No TLS in transit.** Not yet assessed against the anticipated LAN deployment; **may need revisiting before Core is reachable over a real, less-trusted network rather than a loopback.**
- **No per-caller identity.** Revisit if Core ever needs to tell *which* caller, not just authorized or not.
- **No rotation grace window or hot-reload.** An accepted low-frequency cost; **revisit only if rotation ever needs to happen without a stop-the-world restart.**
- **No rotation trigger or cadence policy.** Mechanics only, above.
- **Cross-machine token distribution remains unsolved.** The file mechanism bridges same-machine deployments only; **a genuinely separate host needs explicit config, with no auto-discovery.** Revisit once a real remote deployment needs it.
- **The native Linux and macOS path ships as code and is not service-validated.** Hardware validation was deliberately scoped to the Windows+WSL2 topology actually in use, **so that path has not had the same real-world confirmation the Windows one gets.**
- **The Windows path assumes `%ProgramData%` resolves to something WSL2 can reach** through its mount convention. Mitigated by resolving the real value rather than hardcoding it, **but a relocated `ProgramData` on a drive WSL2 does not mount is not an exercised edge case.**
