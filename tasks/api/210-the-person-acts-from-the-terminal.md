# 210 — The person acts from the terminal: a confirmation, the go, an observation

**State:** open
**Source:** EMB-378 — the person has no terminal path for a confirmation, the go or an observation
**Issue:** EMB-378
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Every `embarch-api` subcommand sends the agent's token. The person's token is
resolved by `embarch-core-client` (`TokenScope::Person`) but no subcommand uses
it, so an engineer with no UI open has no way to make a confirmation, give a Test
run's go, or answer an observation. The design: "a confirmation is made in the UI
only, or the CLI where there is no UI", and "the CLI covers every act the UI
does" (`embarch-doc/notes/hil/03-test.md`, "The DUT's inputs";
`notes/hil/12-prevention.md`, "The root of trust"). When this is done:

- **One `person` verb with five subcommands:**
  - `confirm <hash>`: shows the confirmation card's data, then confirms with its
    nonce (core decision 135);
  - `go <run id>`: shows the go card's data, then gives the go (core decision 112);
  - `answer <run id> <prompt id> [<choice or number>]`: an observation's value,
    else confirmed or cancelled (core decision 138, api decision 137);
  - `unit <key> --serial <s> --revision <r>` and `name <name>`: the declarations
    of core decision 147 (`PUT /units/{key}`, `PUT /person`).
- **Each prints the card's data as Core rendered it**, every string the agent
  supplied shown quoted, and asks for a typed `yes` before it sends. Anything
  else sends nothing.
- **They read the person's token only**, never the agent's, and **the MCP server
  registers none of them**. A test fails if it does.

The owner may strike this unit for subcommands of the `embarch` umbrella binary
(plan choice 15). Build it here, on the issue's default.

## Where to look

- `src/cli.rs`; `src/tools.rs` for what the MCP server registers
- `crates/embarch-core-client/src/lib.rs`, `token_discovery.rs`, `client.rs`:
  `TokenScope::Person`, `resolve_token_for`; the client methods the UI already
  calls for the go, a confirmation and a prompt answer
- `embarch-core` decisions 112, 135, 138, 147, read only, for the routes and
  their bodies
- `embarch-doc/embarch-api/interfaces/tools.md`

## Where the doc goes

A new api decision for the `person` verb, and the verb in `interfaces/tools.md`.
**Two files in reserve, each with its compaction blocked on In flux: yes**
(`scripts/check-doc-size.py --pressure`):

- `embarch-api/spec.md`, 1,110 B left, `tasks/api/201`. Do not write it unless
  the unit needs to. If it does, compact `spec.md` out of reserve in the same
  commit, keeping `api/201`'s `Must not delete:` items, and say so.
- `embarch-api/decisions/client-crate.md`, 480 B left, `tasks/api/209`. If this
  unit changes the client crate's public surface and so owes a decision there,
  compact that file out of reserve in the same commit, keeping `api/209`'s
  `Must not delete:` items. Never file a client decision in another topic file to
  avoid it.

Decisions already over or near their limit: `lease#90`, `test-plans#134`,
`ledger#98`. Write new ones rather than grow those.

## Done when

- [ ] Against a fake Core, each subcommand sends the person's token, and the
      card's nonce wherever Core's route takes one.
- [ ] A test fails if the MCP server registers any of them.
- [ ] With no typed `yes`, nothing is sent.
- [ ] `interfaces/tools.md` gives the verb.
- [ ] Gate green (`cargo build --workspace`, `test`, `clippy --workspace
      --all-targets -- -D warnings`).
