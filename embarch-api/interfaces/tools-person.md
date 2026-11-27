# embarch-api: the `person` verb

**Status:** active, 2026-11-26 ([decision 141](../decisions/person-verb.md)); see [tools.md](tools.md). **CLI only: the MCP server registers none of these**, because each is the engineer's own act and Core refuses the agent's token on its route.

Each subcommand sends the **person's token** (config `person_token`, `EMBARCH_PERSON_TOKEN`, the `person-token` file; [config.md](config.md)), prints Core's card on stderr with every string quoted, and reads one line from stdin: only `yes` sends. Anything else sends nothing and exits 1.

| Subcommand | Reads, then sends | Notes |
|---|---|---|
| `person confirm <hash>` | `GET /confirmations/{hash}/card`; `POST /confirmations` `{hash, nonce, surface: "cli"}` | No nonce on the card (nothing waits) is an error, nothing sent |
| `person go <run_id>` | `GET /test-runs/{id}/card`; `POST /test-runs/{id}/go` `{run_id, run_hash, nonce}` | The go of exactly the card shown |
| `person answer <run_id> <prompt_id> [value]` | `GET /test-runs/{id}` (the waiting prompt must be `prompt_id`); `POST /study/{id}/prompt` `{prompt_id, answer, answered_by: "cli", value?}` | `value` is a number when it parses as one, else text, sent with `confirmed`; `--cancel` sends `cancelled` and takes no value |
| `person unit <key> --serial <s> --revision <r>` | `PUT /units/{key}` `{serial, board_revision}` | Core decision 147 |
| `person name <name>` | `PUT /person` `{name}` | Core decision 147 |

`--json` prints `{success, sent, response | error}` (stamped like every verb) on stdout; the card and the question stay on stderr.
