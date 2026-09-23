# embarch-atlas: research intake

**Raw intake, not a doc tier.** These notes are the landscape survey that precedes
resuming `embarch-atlas` design work: what already exists, what it costs, what it
cannot do for firmware. They record what was *found*, not what was *decided*.

## What this folder is for

`embarch-atlas` has been paused since 2026-07-20 with no repo. Before writing a
design, the suite needs to know whether this capability should be adopted,
adapted, or built — and that question has a large, fast-moving answer surface
(agent code-intelligence tooling, C/C++ analysis substrates, Zephyr build
metadata, the repo-comprehension literature, the embedded vendor landscape).
Surveying it once and writing it down is cheaper than each future session
re-deriving a partial version of it from scratch.

## Rules

- **One file per research territory**, `NN-<slug>.md`, each carrying a
  `**Status:** draft, <date>` line and staying under the 25 KB `legacy` cap that
  `check-doc-size.py` applies to anything under a sub-project directory.
- **Findings, with sources.** A claim about an external tool carries a URL. A
  claim about this suite's own codebases carries a file path and a measurement
  date. An inference is marked as one.
- **Client data never lands here.** This repo is public. Anything derived from a
  client's firmware, schematics or build output — module and file names, net
  names, BOM, devicetree wiring, flow traces — is kept in a machine-local folder
  outside every repo (`~/Github/embarch/.atlas-local/`, beside `.fleet/`). A
  note here keeps the generalized finding and the numbers, with client specifics
  replaced by placeholders (`<sensor>`, `<board>`, `<driver>.c`). Scrubbing the
  client *name* is necessary and not sufficient: the pre-push hook catches names,
  nothing catches internals.
- **No decisions here.** A conclusion drawn from this material belongs in
  [`../design.md`](../design.md) (and, once the sub-project resumes, in its
  `decisions.md`). A verdict stated here is a note about what the evidence
  supports, not a commitment the suite has made.
- **This folder is temporary.** It follows the milestone-doc rule in
  [DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §3: once the design that consumes it
  is written, the folder folds into the design docs and is **deleted**. Git
  holds it. Research left standing beside a design competes with it for the
  reader who wants current truth — and this material ages fastest of anything
  in the corpus.

## Scope this survey was run under

Fixed 2026-09-22, before the research started, so a later reader knows what the
notes were and were not looking for:

| Question | Answer held |
|---|---|
| Consumer | A coding agent, mid-task, in a firmware repo |
| Capabilities in scope | Code structure; build-config reality (which code is *actually compiled in*); hardware binding (peripheral → driver → DT node → part) |
| Explicitly *not* in scope | Runtime/concurrency modelling as a first-class capability |
| Index scope | App + project libs, plus the parts of Zephyr the app actually reaches |
| Interface shape | A small always-loaded map, backed by a drill-down query surface |
| Method (deterministic vs LLM vs embeddings) | **Open** — the research is meant to settle it |
| Substrate | **Open** — whatever fits the analysis, suite-Rust consistency is not a constraint |
| Hard constraints | Fully local/offline (client IP never leaves the machine); must survive the real client firmware, not a toy |
| Runtime fusion (static map + EmbArch's own traces) | Kept as a later optional layer; design should not foreclose it |

## Index

| File | Territory |
|---|---|
| [`00-target-sizing.md`](00-target-sizing.md) | The codebase this has to work on, measured |
| [`01-agent-code-intelligence.md`](01-agent-code-intelligence.md) | Agent-facing code intelligence: Serena, repo maps, SCIP, the IDE vendors, code graphs, and the index-vs-grep evidence |
| `02-analysis-substrates.md` | C/C++ analysis engines: clang, tree-sitter, the commercial tools, and variability-aware parsing *(pending)* |
| [`03-zephyr-build-metadata.md`](03-zephyr-build-metadata.md) | What a Zephyr build already computes, verified against the real workspace |
| [`04-repo-comprehension-evidence.md`](04-repo-comprehension-evidence.md) | The research literature, and the deterministic-vs-LLM-vs-embeddings answer |
| [`05-embedded-landscape.md`](05-embedded-landscape.md) | Who is already doing this for firmware: vendors, startups, commercial backends, and the white space |
