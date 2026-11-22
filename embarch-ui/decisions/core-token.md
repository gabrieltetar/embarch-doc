# embarch-ui decisions: Which token the UI sends to Core

**Status:** active, 2026-11-21.

How the UI authenticates to embarch-core. The resolution and the files are `embarch-api` decision 109's; this is only what the UI does with them.

### 103 — The UI's Core client carries the person's token, and a missing one stops the UI rather than falling back to the agent's

The UI is the person's surface, so every request it makes to Core is the person's (EMB-219; HIL unit M1.4). **`config::core_client` builds the one `CoreClient` with `TokenScope::Person`**, resolved as `embarch-api` decision 109 left it: `[core] person_token_env`, then `person_token`, then `EMBARCH_PERSON_TOKEN`, then the `person-token` file beside Core's token file. A test asserts the client's scope is `Person`.

**No fallback to the agent's token.** A fallback would make every act made on the UI read as the agent's, which is exactly what the scope split exists to tell apart (notes and prose adoptions are attributed by the token's scope, M1.8). Its cost is real: a bench with Core's agent token but no person token cannot open the UI until the person token is created.

**A missing person token stops the UI at start**, the error naming the sources it looked in, as a missing agent token always has. *Rejected: starting anyway and showing the error in the Topology banner where "Core unreachable" shows* — every route holds one `CoreClient`, and one with no token to send is either absent (an `Option` through every handler) or sends an empty token Core rejects, which the banner would then report as a rejected token, not a missing one. The unit's journal and the launcher's failed-unit state carry the message instead [assumed: not exercised against the installed unit].
