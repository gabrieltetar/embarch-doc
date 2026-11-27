# embarch-core decisions: The call log's quota

**Status:** active, 2026-11-27 (`tasks/core/187`, `notes/hil/12-prevention.md`, "What Core then guarantees, in code", item 3). Index: [../decisions.md](../decisions.md). Surface: [../interfaces/call-log.md](../interfaces/call-log.md). Sibling: [call-log.md](call-log.md) (decision 158, whose fail-closed state and reserved tail this sits beside).

### 161 — The call log has a quota; past it the agent's calls are refused first, and only the person raises it

Decision 158 refused every gated call while Core could not log, but nothing bounded the log, so an agent filling the store would have turned that refusal against the person. **The quota** is a size in bytes for `call-log.jsonl`, kept in `call-log-quota.json` beside it and read at the start; with no readable file it is **1 GiB**. **At 90 % of it, a gated call carrying the agent's token answers `503`; at 100 %, the person's too.** The body names the size, the quota and the person's way out: `PUT /call-log/quota` under the person's token, or freeing the store. `POST /study/{study_id}/cancel` is served at any size, as under 158. A refusal for the quota is **not entered**, so a refused agent cannot go on growing the file (the same rule as a refusal for want of space).

**The reserved tail lies beyond the quota:** the `start`, `stop` and `safe_off` entries do not ask the gate, so the safe-off lands at any size. The 90 % mark is about the agent's token, not the study that token started: a host study in flight asks the 100 % mark before each step (`cannot_log` uses the person's), so a study the agent started is not cut at 90 %.

**`PUT /call-log/quota {quota_bytes}`** raises or lowers it, at least 1; the agent's token is `403` on every Core, development included (the middleware, like a declaration). It is lease-open and not a gated route, so a full log's person can still reach it; the handler enters a `quota` entry (`from_bytes`, `to_bytes`, `scope`) first, past the quota like the tail, and only then keeps the new value (written to a temporary file and renamed). A quota set below the current size refuses everything but a cancel until the store is freed or the quota raised. **`GET /call-log`** reports `size_bytes` and `quota_bytes`.

**The values are the owner's, chosen, not measured:** 1 GiB, 90 % and 100 %. The size is the file's length on disk; the free-space check of 158 is independent of it and stays.

**Measured:** unit tests: with the quota set so the log is at 90 %, the agent's call is `503` and not entered while the person's is served; at the quota both are `503`; a cancel is served throughout; the `safe_off`, `start` and `stop` entries land at a quota of 1 B; the agent's `PUT` is `403` and changes nothing; the person's changes the quota, enters it, keeps it across a reopen and `GET` reports it; a full log's person raises it and the agent is served again. Nothing was run on a board.
