# 229 — the person verb raises the call log's quota

**State:** claimed by agent/api/229-the-person-verb-raises-the-call-logs-quota, 2026-11-27 05:23
**Source:** embarch-core/open.md — "No client sends the quota route (161)."
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-core` decision 161 bounds the call log: past 90 % of its quota Core
refuses the agent's gated calls with `503`, past 100 % the person's too, and the
refusal's body names the way out, `PUT /call-log/quota {quota_bytes}` under the
person's token. Core answers the agent's token `403` on that route on every
Core. **No client sends it**, so today the way out is a hand-written HTTP
request.

When this is done, `embarch-api person` (decision 141, the one CLI verb that
sends the person's token) has a sixth subcommand that sets the call log's quota,
in the verb's shape: it reads `GET /call-log` first and prints the current
`size_bytes` and `quota_bytes` and the requested value on stderr, every string
quoted, reads one line from stdin, and sends the `PUT` only on `yes`. Pick the
name and the argument's unit (bytes, or a suffix such as `2GiB` parsed to
bytes) and write why into decision 141; `--json` follows the verb's existing
`{success, sent, response | error}` shape. A `400` (a quota of 0) and a `403`
come back as their own error text. No MCP tool, as for every person
subcommand.

Also make `embarch-api call-log` print `size_bytes` and `quota_bytes` if it
does not already, so an agent that hit the `503` can read how full the log is
and tell the person which command raises it. Check the client's `/call-log`
response type in `crates/embarch-core-client` carries the two fields
(`Option`, per decision 58, since an older Core does not serve them).

Amend decision 141 in place (five subcommands become six) and add the row to
`interfaces/tools-person.md`.

**Not yours:** every other repo, `embarch-core` included. You never touch
hardware; test against the mock Core the person verb's tests already use.

## Why now

Decision 161 landed with a way out that only an HTTP request reaches, and the
first person to meet a full log meets it with the agent's calls already
refused.

## Where to look

- `src/main.rs` (`Person` subcommands around line 1204; `CallLog` around 921),
  the person verb's module (`person_cli`) and its tests
- `crates/embarch-core-client` (the `/call-log` response type, `TokenScope::Person`)
- `embarch-doc/embarch-api/decisions/person-verb.md` (141),
  `interfaces/tools-person.md`
- `embarch-doc/embarch-core/decisions/call-log-quota.md` (161) and
  `interfaces/call-log.md` (the `PUT /call-log/quota` row; read only)
- **Size:** `decisions/client-crate.md` is in reserve (456 B left,
  `tasks/api/222`); if the response type's change needs a line there, keep it
  to one line, or put it in decision 141 instead.

## Done when

- [ ] The new person subcommand shows size, quota and the request, sends the
      `PUT` only on a typed `yes`, and its tests cover yes, anything else,
      `400` and `403`.
- [ ] `embarch-api call-log` shows `size_bytes` and `quota_bytes` when Core
      serves them.
- [ ] Decision 141 and `interfaces/tools-person.md` say so.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`);
      `changelog.d/` fragment.
