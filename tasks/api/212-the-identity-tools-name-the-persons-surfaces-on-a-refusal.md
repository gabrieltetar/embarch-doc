# 212 — The identity tools name the person's surfaces on a person-scope refusal

**State:** open
**Source:** EMB-335 — the identity tools give a bare refusal on an attested Core
**Issue:** EMB-335
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The identity tools (`enroll_probe`, `unenroll_probe`, `set_role_board`,
`declare_instrument`, `remove_instrument`, `declare_signal`, `remove_signal`,
`declare_bootload_ports`, `clear_bootload_ports`, `dev_bench_link`) call Core with
the agent's token only (api decision 109). The HIL evidence proposal has "the
identity tools leave the MCP surface for the CLI with the person's token on an
attested Core" (`embarch-doc/embarch-hil-evidence-proposal.md`, "The work, by
sub-project"). On an attested Core, Core refuses those acts to the agent's token
with a person-scope `403`, and today the tool returns that refusal bare. When this
is done:

- **On Core's person-scope `403`, each identity tool returns** the act it would
  have made, the CLI command the person can run in their own terminal to make it,
  and that `embarch-ui`'s Topology tab makes the same act.
- **The CLI gains `--as-person`** on those acts, which builds the client with the
  person's scope. Read api decision 141 (`embarch-api person`, a typed `yes`
  before sending) first, and either follow its confirmation rule for
  `--as-person` or say in the decision why an identity act does not need it.
- **The MCP server never sends the person's token.** A test fails if it builds a
  person-scope client.
- **Each tool's description says** it is the agent's only on an unattested Core.

The owner may strike this unit (HIL plan choice A.12). Build it on the issue's
default above.

## Where to look

- `src/tools.rs`: the identity tools; `src/cli.rs`; `src/person_cli.rs` (141)
- `crates/embarch-core-client/src/client.rs`: `new_with_scope`;
  `token_discovery.rs`: `TokenScope::Person`
- `embarch-doc/embarch-api/interfaces/tools-topology.md`,
  `tools-instruments.md`, `tools-bootload.md`, `tools-dev-bench.md`: the identity
  tool docs
- `embarch-doc/embarch-api/decisions/client-crate.md` (109),
  `decisions/person-verb.md` (141)

## Where the doc goes

A new api decision for the refusal text and `--as-person`. The interface docs say
who may make each act on each kind of Core. **Two files in reserve, each with its
compaction blocked on In flux: yes** (`scripts/check-doc-size.py --pressure`):

- `embarch-api/spec.md`, 1,110 B left, `tasks/api/201`. Do not write it unless
  the unit needs to; if it does, compact it out of reserve in the same commit,
  keeping `api/201`'s `Must not delete:` items.
- `embarch-api/decisions/client-crate.md`, 469 B left, `tasks/api/209`. 109 says
  the CLI sends only the agent's token outside `person`; if this unit amends it,
  compact that file out of reserve in the same commit, keeping `api/209`'s
  `Must not delete:` items. Never file a client decision in another topic file to
  avoid it.

## Done when

- [ ] On a fake person-scope `403`, each identity tool's text names the CLI
      command and the UI tab.
- [ ] `--as-person` sends the person's token, asserted on a fake Core.
- [ ] A test shows the MCP server never builds a person-scope client.
- [ ] The interface docs say who may make each act on each kind of Core.
- [ ] Gate green (`cargo build --workspace`, `test`, `clippy --workspace
      --all-targets -- -D warnings`).
