# embarch-api decisions: the identity acts on an attested Core

**Status:** active, 2026-11-26 (EMB-335, `tasks/api/212`).

Decision 143. Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/tools-topology.md](../interfaces/tools-topology.md), "Who makes an identity act". Design: [HIL evidence proposal](../../embarch-hil-evidence-proposal.md), "The work, by sub-project": the identity tools leave the MCP surface for the CLI with the person's token on an attested Core.

### 143 — An identity tool's person-scope `403` names the person's CLI command and the UI tab; `--as-person` makes the act with the person's token after a typed `yes`

**The ten acts.** `enroll_probe`, `unenroll_probe`, `set_role_board`, `declare_instrument`, `remove_instrument`, `declare_signal`, `remove_signal`, `declare_bootload_ports`, `clear_bootload_ports` and `dev_bench_link` send the agent's token ([109](client-crate.md)). On an **unattested** Core they are the agent's own acts, as before. On an **attested** Core, Core refuses them to that token with a person-scope `403`.

**The refusal text.** `identity_act::IdentityAct::error_text` appends to the tool's own error, only when it carries `403`: the act the tool would have made, `embarch-api <command> --as-person ...` with the same arguments, `embarch-ui`'s Topology tab as the surface that makes the same act, and "do not retry, do not ask for their token". Any other refusal is left as Core said it. The same sentence is in each tool's description ("Your own act only on an unattested Core"). A `403` from the read that precedes a re-declare (`declare_instrument` and `declare_signal` carry the stored `safe_off`) gets the note too.

**`--as-person`.** A global flag, accepted by those ten subcommands and **refused for every other**, before any request. `cli::run` hands the act to `run_as_person`, which builds `CoreClient::new_with_scope(.., Person)` (no fallback to the agent's token, [109](client-crate.md)), writes no live-log line and holds no agent client, as [141](person-verb.md) does. **It follows 141's confirmation rule**: an identity act has no Core card, so it shows the act (subcommand and its arguments, every string quoted, on stderr) and sends only on a typed `yes`; anything else exits 1 with `not sent`. The rule is kept rather than waived because the act is written from arguments an agent may have proposed, and the person should read exactly what will be sent.

**What this does not close.** A typed `yes` from a pipe is indistinguishable from a person's, as in 141 (its tests pipe it): the barrier is that the person's token is readable only where the person put it, not the prompt. This amends 109 and 141, which said no flag reaches the person's token; **`--as-person` is that flag**, narrowed to these ten acts.

**The MCP server never builds the person's client.** Pinned by `tests/identity_as_person.rs`: only `src/cli.rs` and `src/person_cli.rs` name `TokenScope::Person`, and a real MCP session against a mock Core answering `403` sends only the agent's bearer for all ten tools.

**Pinned by** the same file: each tool's text on a `403` names `embarch-api <command> --as-person` and the Topology tab and each description carries the rule; `--as-person` sends the person's bearer after `yes` and nothing for five wrong inputs; `status --as-person` sends nothing. **Client crate:** unchanged. **Owner may strike:** this unit (HIL plan choice A.12); built on the issue's default. **Not verified:** against an attested live Core (what Core's `403` body says), the Topology tab making all ten acts (the UI's own work), and the `yes` on a real terminal.
