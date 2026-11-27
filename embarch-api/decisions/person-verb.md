# embarch-api decisions: the `person` verb

**Status:** active, 2026-11-26 (EMB-378, `tasks/api/210`).

Decision 141. Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Interface: [../interfaces/tools-person.md](../interfaces/tools-person.md). Design: [HIL 03](../../notes/hil/03-test.md), "The DUT's inputs", and [HIL 12](../../notes/hil/12-prevention.md), "The root of trust": a confirmation is made in the UI, or on the CLI where there is no UI.

### 141 - `embarch-api person` is the one CLI verb that sends the person's token, has no MCP tool, and sends only after a typed `yes`

**Five subcommands, one verb.** `confirm <hash>` (`GET /confirmations/{hash}/card`, then `POST /confirmations` with the card's nonce and `surface: cli`, [core 135](../../embarch-core/decisions/test-run-go.md)); `go <run id>` (`GET /test-runs/{id}/card`, then the go with the card's `run_hash` and nonce); `answer <run id> <prompt id> [value]` (an observation's value, a number when it parses as one, else `confirmed`, or `--cancel` for `cancelled`; `POST /study/{run id}/prompt` with `answered_by: cli`, [core 138](../../embarch-core/decisions/host-prompt.md)); `unit <key> --serial --revision` and `name <name>` (`PUT /units/{key}`, `PUT /person`, core 147). `answer` first reads `GET /test-runs/{id}` and refuses, sending nothing, when the waiting prompt is not the one named. The study id of a Test run's prompt is the run id (Core publishes the slot under it).

**The token.** `person_cli::run` builds its own client with `TokenScope::Person`, from the existing person order ([109](client-crate.md): config, `EMBARCH_PERSON_TOKEN`, the `person-token` file), and never falls back to the agent's. `cli::run` hands the verb off before the agent's client or the live log is touched, so a person's act writes no live-log line. Decision 109's "no verb reaches the person's" is narrowed to this verb; **no MCP tool, no flag on another verb and no environment switch** reaches it.

**What the person sees.** The card as Core returned it, as indented lines on **stderr** (so `--json` keeps stdout), **every string quoted**: text an agent supplied cannot pass for Core's own words by being unquoted. The nonce is left out of the display. Then `<what>? Type yes to send:`. **Only the line `yes` sends**; an empty line, `y`, `YES` or a closed stdin sends nothing and exits 1 with `not sent`. Core's own refusal (spent or expired nonce, stale hash) comes back as the error text.

**Pinned by** `tests/person_verb.rs` against a mock Core: each subcommand sends the person's bearer and, where the route takes one, the card's nonce; no `yes` sends no write (six wrong inputs over five subcommands); `src/tools.rs` names none of the verb's client calls and registers no tool named for them. `tests/run_test_cli.rs` still fails if `src/cli.rs` or `src/hil_run.rs` names `test_run_go`, which is why the verb lives in `src/person_cli.rs`.

**Client crate, additive:** `CoreClient::declare_unit(key, serial, board_revision)` and `declare_person(name)`; nothing existing changed. **Owner may strike:** the verb as a subcommand of the `embarch` umbrella (plan choice 15); this is the issue's default. **Not verified:** against a live Core, and the interactive `yes` on a real terminal (tests pipe stdin).
