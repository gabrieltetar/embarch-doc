# embarch-study-designer decisions: Authoring surfaces

**Status:** active, 2026-09-02.

The UI, the registry, and where engineer knowledge enters the system.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 6 — Symmetric human/agent access

The suite-wide principle applied here: **every capability is reachable both by an agent and directly by a human, converging on the same modules.** Study-running code means new MCP tools *and* CLI subcommands — **not one without the other.** Decision 26 exists **because decision 17's seal requirement would otherwise have broken the human half of this.**

### 34 — A Study Designer UI: an interactive, table-based `Study` builder

Motivated by a gap a milestone's own closing session hit directly: **a real monitor-everything run came back empty — nothing was captured because nothing in that study ever *wrote* anything, and there was no way for whoever authored it to know what to write, since that is DUT-specific knowledge no generic discovery can produce.** Closing it needed two things: an authoring UI, and **a place for that knowledge to live** (decision 35).

**Shape:** a table where each row is a step — an action from a dropdown, its parameters, a timeout, a continue-on-fail flag. **Sequencing is expressed purely by row order, not a separate precondition field**, matching how steps already work: **no state passes between steps.**

**The action list is merged from three sources, not one:** built-in variants, live discovery when a DUT happens to be connected, and static extraction — **the same dual-source cross-check decision 33 established, now feeding one UI instead of being two things a human diffs by hand.**

**Scope: author, run and watch — read-only outside the authoring table.** It submits what it just built and polls each step, **because a human should not need a second tool to try what they built.** It does **not** build or flash anything: **provisioning stays a separate step, done before the run button means anything.**

**This crate's own UI binary is retired.** `embarch-ui`'s tab is the successor — same merged list, same table model, same registry, **but calling this crate in-process rather than running a second local web server**, and submitting over HTTP rather than shelling out to a CLI. **The library modules are entirely unaffected; only the binary that wrapped them in a server is gone.**

### 35 — A user-authored custom-action registry: names and enumerated parameter choices only, never a semantic description

The actual fix for what motivated decision 34. An attempt to figure out what a custom GATT write "does" **by reading the DUT firmware's own source and asserting a conclusion from it was flagged directly as destructive to the dev process** — **reading code and inferring behaviour from it is not the same as knowing it, and presenting that inference as fact is worse than not answering at all.** The fix is not a smarter inference; **it is removing inference from the loop entirely.**

**What the engineer provides — mechanical, not documentary:** a freely-chosen name, which characteristic it targets, its operation, and — for a write — a payload described as named fields, **each with a small enumerated set of engineer-supplied label/value pairs.** Building a step means clicking a name and clicking a value; **nothing is typed as raw hex, and nothing describes *why* a value does what it does — there is deliberately no "what this does" field at all, since that would be this crate inventing a place to write down another guess.**

A value's bytes are **the engineer's own literal bytes, never a numeric type this crate encodes itself** — **which would require assuming a width and endianness nobody here is in a position to know.**

**Persisted in the firmware repo's own folder**, so **it travels with the firmware and is versioned in that repo's history** — not a catalog this tool owns separately, and not re-entered per study.

**The durable principle, stated plainly since it generalises past this crate:** *no EmbArch component should ever present an inference about what a specific piece of hardware or firmware does — derived from reading its source, its comments, or any heuristic — as established fact.* Where that knowledge is needed, **the answer is a pipeline for the engineer who actually knows to supply it explicitly, built once, generically.** Decisions 41, 45, 52, 56 and 58 are each that rule applied somewhere else.

### 37 — A free-text payload path alongside the registry: `RowAction::Raw`

The registry is the right home for a *named, reusable* action, **but it was the only way to send a payload at all — so a one-off, a value being tried once to see what happens, required editing the registry first.** A raw row takes a UUID pair typed directly and a payload as literal bytes.

**This does not weaken decision 35**, which forbids two specific things: **this crate inventing a *semantic description*, and this crate *encoding a number into bytes* on an engineer's behalf.** A raw payload **is already bytes when it reaches this crate**, parsed client-side by the same parser the registration form uses — **so nothing here interprets or encodes anything.** The registry remains how an action gets *named and re-used*; **this is how one gets *sent before it has a name*.**

UUID parsing arrives alongside it, accepting the hyphenated form, bare hex, **or the 16-bit shorthand expanded against the SIG base UUID. That expansion is a spec fact — a 16-bit UUID *means* that value by definition — not an inference about any DUT.**

### 38 — A saved-study library at `<firmware-repo>/embarch/studies/*.json`

Until this, **a study authored in the UI existed only as long as the browser tab did**; re-running one meant rebuilding the table by hand. Saved studies live beside the registry, **so a study travels with the firmware it was written against.**

**The file *is* a study** — the CLI re-runs it directly with no conversion step. The authoring rows ride along in **one extra key the study's own deserializer ignores.** That single-file choice is what makes a saved study **both re-runnable from the CLI *and* re-loadable into an editable table; a sidecar would have made one of the two lossy or the pair separable.** A study dropped into that directory by hand or by an agent is still listed and runnable — **it just has no rows to load back, and the UI says so rather than offering a Load that would silently produce an empty table.**

This is also what makes decision 39's `StreamSource::Signal` and decision 40's reflash-is-a-run-parameter rules load-bearing: a saved study has to survive a rewired bench and has to not reflash a board every time someone re-reads its results.

---

