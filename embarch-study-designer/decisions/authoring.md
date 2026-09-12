# embarch-study-designer decisions: Authoring surfaces

**Status:** active, 2026-09-02.

The table, the rows it can hold, and where a study is saved. The registry those rows resolve against, and what a hand-edited one is refused for: [registry.md](registry.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 6 — Symmetric human/agent access

The suite-wide principle applied here: **every capability is reachable both by an agent and directly by a human, converging on the same modules.** Study-running code means new MCP tools *and* CLI subcommands — **not one without the other.** Decision 26 exists **because decision 17's seal requirement would otherwise have broken the human half of this.**

### 34 — A Study Designer UI: an interactive, table-based `Study` builder

Motivated by a gap a milestone's own closing session hit directly: **a real monitor-everything run came back empty — nothing was captured because nothing in that study ever *wrote* anything, and there was no way for whoever authored it to know what to write, since that is DUT-specific knowledge no generic discovery can produce.** Closing it needed two things: an authoring UI, and **a place for that knowledge to live** (decision 35).

**Shape:** a table where each row is a step — an action from a dropdown, its parameters, a timeout, a continue-on-fail flag. **Sequencing is expressed purely by row order, not a separate precondition field**, matching how steps already work: **no state passes between steps.**

**The action list is merged from three sources, not one:** built-in variants, live discovery when a DUT happens to be connected, and static extraction — **the same dual-source cross-check decision 33 established, now feeding one UI instead of being two things a human diffs by hand.**

**Scope: author, run and watch — read-only outside the authoring table.** It submits what it just built and polls each step, **because a human should not need a second tool to try what they built.** It does **not** build or flash anything: **provisioning stays a separate step, done before the run button means anything.**

**This crate's own UI binary is retired.** `embarch-ui`'s tab is the successor — same merged list, same table model, same registry, **but calling this crate in-process rather than running a second local web server**, and submitting over HTTP rather than shelling out to a CLI. **The library modules are entirely unaffected; only the binary that wrapped them in a server is gone.**

### 37 — A free-text payload path alongside the registry: `RowAction::Raw`

The registry is the right home for a *named, reusable* action, **but it was the only way to send a payload at all — so a one-off, a value being tried once to see what happens, required editing the registry first.** A raw row takes a UUID pair typed directly and a payload as literal bytes.

**This does not weaken decision 35**, which forbids two specific things: **this crate inventing a *semantic description*, and this crate *encoding a number into bytes* on an engineer's behalf.** A raw payload **is already bytes when it reaches this crate**, parsed client-side by the same parser the registration form uses — **so nothing here interprets or encodes anything.** The registry remains how an action gets *named and re-used*; **this is how one gets *sent before it has a name*.**

UUID parsing arrives alongside it, accepting the hyphenated form, bare hex, **or the 16-bit shorthand expanded against the SIG base UUID. That expansion is a spec fact — a 16-bit UUID *means* that value by definition — not an inference about any DUT.**

### 38 — A saved-study library at `<firmware-repo>/embarch/studies/*.json`

Until this, **a study authored in the UI existed only as long as the browser tab did**; re-running one meant rebuilding the table by hand. Saved studies live beside the registry, **so a study travels with the firmware it was written against.**

**The file *is* a study** — the CLI re-runs it directly with no conversion step. The authoring rows ride along in **one extra key the study's own deserializer ignores.** That single-file choice is what makes a saved study **both re-runnable from the CLI *and* re-loadable into an editable table; a sidecar would have made one of the two lossy or the pair separable.** A study dropped into that directory by hand or by an agent is still listed and runnable — **it just has no rows to load back, and the UI says so rather than offering a Load that would silently produce an empty table.**

This is also what makes decision 39's `StreamSource::Signal` and decision 40's reflash-is-a-run-parameter rules load-bearing: a saved study has to survive a rewired bench and has to not reflash a board every time someone re-reads its results.

### 73 — One built-in action vocabulary, and the picker renders what it is served

The question *which built-in actions can a row pick* was answered in **three** places: `BuiltInAction` in `merged_actions.rs` (**seven**), `BuiltInActionKind` in `study_builder.rs` (**nine**), and a hand-written `SD_BUILT_INS` array of nine `{value, label}` pairs in `embarch-ui/assets/app.js`, whose label prose existed only there. The submit side was authoritative and right; the browser's copy was right by hand; **the crate's own served answer had been wrong since decision 53 added two variants, and nobody noticed — because the only consumer discarded it.** `merge_actions` built the built-ins, `embarch-ui` served the merged list, and `app.js` filtered it for `Registered`/`Unregistered` and rendered its own array instead. A list that is computed and thrown away cannot be wrong in a way anyone sees.

So: `BuiltInActionKind` is now the **only** definition, on both sides, and it carries `ALL` and a `label()`. `MergedAction::BuiltIn` changed from a bare string to `{which, label}` and the browser renders the served entries. Adding a built-in is one edit, and the compiler demands the variant, the `ALL` entry, the label and the `to_action` arm together.

**The labels moved to the server for the reason `embarch-ui` decision 17 already gave about `MAX_MONITOR_TARGETS`** — *a browser-side copy of a limit is a number that drifts silently the day the limit moves* — which is as true of a name as of a number, and `embarch-ui/spec.md`'s Invariants state it outright. This was the same shape one file over, and it had already drifted.

**A wire change with no stale consumer to break**, which is exactly why it was safe: the previously served built-ins reached the browser and were filtered out, so nothing rendered them before and nothing depended on their old shape. **Until the first actions response lands the picker's Built-in group is empty**, rather than falling back to a guess — the same posture the `max_stream_name_len` field takes, and for the same reason a wrong guess there would re-commit the defect being removed.

What replaced the old count-pinned test is `every_submittable_built_in_is_offered_with_a_label`: it asserts that every variant a row can submit is one a row can be offered, with a non-empty label. That is the property that was actually violated. A count could not have caught it, because both counts were internally consistent.

---
