# Agent-facing code intelligence: what already exists

**Status:** draft, 2026-09-22.

Survey of the tooling built to let a coding agent navigate a codebase without
reading it: LSP-bridging MCP servers, repo maps, repo flatteners, SCIP/LSIF, the
IDE vendors' indexers, and the code-knowledge-graph family. Plus the published
evidence on whether an index beats agentic grep at all.

## The finding that reorders everything

**The market has solved the wrong half of the problem.** Nearly every tool
surveyed answers "what calls Y" adequately. **None answers "is this file even
compiled in"** — because each is either a tree-sitter AST walker (preprocessor-
blind by construction) or an embedding model (preprocessor-oblivious). The
exceptions are the ones that run a real compiler: clangd, Serena-via-clangd, and
`scip-clang`.

The measured consequence, and it is the number that should govern this
sub-project's design: in the Codebase-Memory evaluation, a tree-sitter knowledge
graph scored **0.58 on macro-heavy C against 1.00 for a plain grep/read agent** —
the authors' stated cause being "macros are not represented in the AST"
(https://arxiv.org/html/2603.27277v1). **Firmware is the worst case for the
entire AST-graph family.** A naive code graph is not merely unhelpful on this
codebase; it is worse than the baseline it would replace.

## What a Zephyr build already knows

The corollary, and the strongest argument found for this sub-project existing at
all: **Zephyr's build already computes what the market cannot, and writes it to
disk.**

- `build/compile_commands.json` — Zephyr sets `CMAKE_EXPORT_COMPILE_COMMANDS`,
  so a `west build` emits the definitive list of which translation units are
  compiled at all, with exact flags.
  (https://github.com/zephyrproject-rtos/zephyr/issues/23618)
- `build/zephyr/.config` and `build/zephyr/include/generated/autoconf.h` — every
  `CONFIG_*` symbol's resolved value for this build.
- The resolved devicetree — the hardware half. Zephyr splits the two
  deliberately: Kconfig controls what gets compiled, devicetree describes what
  hardware exists.

So `is_compiled_in(file)` is a lookup against `compile_commands.json`, and
`is_active(CONFIG_X)` a lookup against `autoconf.h`. Both exact, both offline,
both essentially free — **and nothing in the surveyed market does either.** The
one existing west-workspace MCP server
(https://lobehub.com/mcp/leog25-mcp-zephyr-west) catalogues modules, boards and
manifest but resolves no configuration and answers no compiled-in query.

This note records that claim as *found*; the build-metadata note is where it gets
verified against the real tree.

## Verdicts

| Tool | Preproc. correct | Local | Verdict |
|---|---|---|---|
| Serena | yes (via clangd) | yes | adapt vocabulary only — GPL-3.0 |
| Claude Code native LSP | yes | yes | **assume free baseline; do not rebuild** |
| aider repo-map | no | yes | adapt algorithm, reject C query |
| repomix / gitingest / code2prompt | no | yes | ignore as architecture |
| `scip-clang` + SCIP | **yes** | yes | **preferred substrate, gated on a spike** |
| `scipq` | inherits SCIP | yes | **read end to end; do not depend on** |
| Cursor / Copilot / Windsurf / Cody | no | **no** | disqualified by the offline constraint |
| tree-sitter graph family | no | mixed | ignore — the 0.58-vs-1.00 result ends it |

### Serena — https://github.com/oraios/serena
MCP server exposing symbol-level tools (`find_symbol`,
`find_referencing_symbols`, `get_symbols_overview`, symbol-body replace, rename)
over language servers through its own `SolidLSP` layer. ~24–30k stars, very
active.

- **Needs a build for C/C++.** Both clangd and ccls require a
  `compile_commands.json` at the repo root with `-std=` and all `-I` flags, or
  cross-file reference finding does not work; Serena rewrites relative paths to
  absolute into `.serena/compile_commands.json` because clangd mishandles
  relative ones.
  (https://oraios.github.io/serena/03-special-guides/cpp_setup.html)
- **License is split and it matters**: `src/solidlsp` is MIT, **everything else
  GPL-3.0-or-later**. Do not vendor code.
- **The token-saving claim is one anecdote**, not a benchmark — 38K→4K on a
  TypeScript rename (https://andrew.ooo/posts/serena-mcp-coding-agent-ide-review/).
  Counter-pressure is well documented: MCP tool schemas load into *every*
  message, and Serena's default context duplicates tools Claude Code now has
  natively, causing net context *bloat*
  (https://github.com/anthropics/claude-plugins-official/issues/121).
- **Why it still cannot answer the question**: clangd gives the active branch and
  says nothing about inactive ones. Serena silently answers for whichever variant
  the compile DB picked — a dangerous half-truth in firmware, because it looks
  like an answer.

### Claude Code's native LSP — the baseline moved
Claude Code shipped built-in LSP support around v2.0.74 (Jan 2026), off by
default, via the official plugin marketplace; C/C++ is among the plugins.
Practitioner reports are mixed (permission prompts, no refactoring commands), but
the scoping consequence is sharp: **Clangaroo's own README declares itself
obsolete for this reason** (https://github.com/jasondk/clangaroo).

**Assume go-to-definition and find-references are solved and free. Build what LSP
cannot express.** That also retires Clangaroo, `clangd-mcp-server` and
`mcp-language-server` as candidates — though `clangd-mcp-server`'s nine tools are
worth reading as compact prior art
(https://github.com/felipeerias/clangd-mcp-server).

### aider's repo-map — the algorithm is right, the C support is not
(https://aider.chat/docs/repomap.html, https://aider.chat/2023/10/22/repomap.html)

Three stages: tree-sitter extracts `def`/`ref` tags; a graph of **files** gets
**personalized PageRank** with the restart vector biased toward files in the
chat and files mentioned by name; then a binary search fits the top-ranked tags
into `--map-tokens` (default **1024**), emitting an indented signature sketch
with `⋮` for elided bodies. Cache is `.aider.tags.cache.v{N}`, diskcache over
SQLite, mtime-validated. The map **expands by a multiplier when no files are in
the chat** (default 8 → ~8k tokens).

**The disqualifying detail, read directly from source**: aider's C tag query
(`aider/queries/tree-sitter-language-pack/c-tags.scm`) captures struct, union,
function, typedef and enum *definitions* and has **no `name.reference.call`
captures at all**, and no `#define` or `#ifdef` handling. In a C repo aider's
PageRank graph has almost no edges, so the ranking degenerates to "files with the
most definitions" rather than "files that matter."

**Steal**: task-biased personalized PageRank, binary search to a hard token
budget, mtime-keyed cache, the `⋮` sketch, the 1k-hot/8k-cold sizing.
**Reject**: file-level nodes (useless at Zephyr driver granularity), tree-sitter
as the edge source for C, and that C query.

### The repo-flattening family — wrong shape
repomix (~28.3k stars, MIT, active), gitingest (~14k, dormant ~13 months),
code2prompt (~7k, Rust), files-to-prompt (~2.6k). Output is 50k–500k tokens for a
real repo; repomix's `--compress` claims ~70% reduction, i.e. still 15k–150k.

These are human-in-the-loop one-shot tools and **anti-patterns for a mid-task
agent**: they blow the context they were meant to save and go stale the moment
the agent edits anything. One narrow steal: repomix's `--compress` is a clean
implementation of "signature skeleton of one file," which is the `skeleton`
drill-down verb.

### SCIP and `scip-clang` — the only preprocessor-honest substrate
**SCIP** (https://scip-code.org/) is LSIF's successor: protobuf, per-document,
incrementally composable. LSIF itself is superseded — ignore.

**`scip-clang`** (https://github.com/sourcegraph/scip-clang), Apache-2.0, on
Clang 21, ~329 commits. Takes `--compdb-path=compile_commands.json` and must be
invoked from the project root. **It is the only tool in the survey that is
natively preprocessor-correct at index level**: Sourcegraph's own copy describes
navigation "aware of build configurations, macros, and type information," with
find-references for **macros** and for **`#include`** as first-class features. It
is fault-tolerant — one failing translation unit does not poison the others.

Costs and hazards: ~2 MB temp disk per TU and ~2 MB of `/dev/shm` per core on
Linux; binaries only for x86_64 Linux (glibc ≥2.16) and arm64 macOS; documented
failures from wrong invocation directory, path mismatches, a 5-minute per-TU
timeout, and `/dev/shm` exhaustion in Docker
(https://github.com/sourcegraph/scip-clang/blob/main/docs/Troubleshooting.md).

**Two risks, both load-bearing:**
1. **Still Beta**, three years after the May 2023 announcement
   (https://sourcegraph.com/blog/announcing-scip-clang).
2. **The Zephyr-shaped risk, unquantified.** `scip-clang` parses with Clang, but
   a Zephyr `compile_commands.json` records `arm-none-eabi-gcc` invocations with
   GCC-only flags. Zephyr's own docs note clangd does not understand Zephyr's GCC
   arguments and the database needs post-processing
   (https://docs.zephyrproject.org/latest/develop/tools/vscode.html,
   https://holgerschurig.github.io/en/zephyr-fixing-lsp-issues/). `scip-clang`'s
   troubleshooting doc says nothing about cross-compilation, GCC-only flags,
   `--extra-arg`, or bare-metal sysroots.

**This is the single biggest unknown in the whole plan**, and it is cheap to
settle: run `scip-clang --compdb-path=build/compile_commands.json` against a real
nRF Zephyr build, and measure `clangd --background-index` on the same tree as the
fallback. The same spike de-risks Serena, since it hits the identical wall.

### `scipq` — the desired shape, already written
https://github.com/elodhorvath/scipq — MIT, Go, static binary, no LLM, no
telemetry, queries over a SCIP index. **Its five verbs map onto the scoped
questions almost exactly:**

| Verb | What it answers |
|---|---|
| `map` | repo structure, hub symbols by reference in-degree, hotspots — **under ~800 tokens for a 300-file repo** |
| `callers` | exact reference sites, resolves implementors |
| `blast` | diff impact, transitive dependents, broken-reference detection |
| `skeleton` | a file's API surface without bodies |
| `dead` | unreferenced defs, test-only symbols, entry points |

All verbs take `--json`. Index load ~100 ms; queries sub-millisecond; a 4.1 MB
index built in 15 s on a production C# codebase. Its stated motivation is a
measured session: **221 read-only exploration shell calls in one task, ~200k
tokens of tool-result content** — the cost this sub-project exists to remove,
quantified by someone else.

It ships an agent skill embedded in the binary with a rule worth taking verbatim:
**if no index exists and one cannot be built, say so and ask — never silently
fall back to grep and present it as a graph answer.**

**Maturity: ~0 stars, 93 commits, pre-v1, single author, v0.4.0, and no C/C++
indexer among those it has been exercised against.** Read it end to end; do not
take a dependency on it.

### What the IDE vendors do, and why it does not apply

| Vendor | Mechanism | Offline? |
|---|---|---|
| Cursor | Merkle tree of file hashes → AST chunking → custom embedding model → remote Turbopuffer vector DB; server stores embeddings + obfuscated paths, never raw source | **No** |
| Windsurf | "M-Query" generative retrieval + 768-dim embeddings + `SWE-grep` models; repo cloned to index, source deleted, embeddings persisted; assembles 10k–50k tokens | Partially, proprietary |
| GitHub Copilot | Remote semantic index per repo (instant since Mar 2025); local folders get a locally-built index | **Mostly no** |
| Sourcegraph Cody | **Deprecated embeddings** for keyword + code-graph (SCIP) search; Free/Pro discontinued 2025-07-23 | Self-hosted only |
| Claude Code | **No index** — Glob → Grep → Read, plus an Explore sub-agent | Yes |

Two consequences. First, **the offline constraint deletes the entire embedding-
vendor path outright** — a scoping gift, not an obstacle. Second, and more
telling: **Sourcegraph, the company with the most code-intelligence experience
anywhere, abandoned embeddings for code and moved to the code graph**, on the
stated grounds that it "doesn't require sending code to an embedding processor,
requires zero additional config, scales to massive codebases"
(https://sourcegraph.com/blog/how-cody-understands-your-codebase). That is the
strongest available endorsement of the structural direction over the RAG one,
from someone who ran both at scale.

### The code-knowledge-graph family

**Findings worth keeping, code worth ignoring.**

- **LocAgent** (ACL 2025, https://arxiv.org/abs/2503.09089) — directed
  heterogeneous graphs, multi-hop agent search. **Up to 92.7% file-level
  localization; +10.5% accuracy from graph guidance over an agent with no graph,
  rising to +19.2% on complex samples;** +13.4% on HumanEval-Bugs; **+12%
  Pass@10** downstream; 4.2 interaction rounds average; a fine-tuned
  Qwen-2.5-Coder-32B matches proprietary SOTA at ~86% lower cost. Python only.
  **The cleanest causal evidence that structure beats unguided agentic search for
  localization — and that the gain concentrates on hard cases.**
- **RepoGraph** (ICLR 2025) — drop-in graph module, **+32.8% relative on
  SWE-bench**. Python only.
- **CodexGraph** (NAACL 2025, https://aclanthology.org/2025.naacl-long.7/) — the
  agent writes Cypher against a Neo4j graph of the repo. **Adapt the idea** (let
  the agent express a structural query rather than pick from fixed verbs);
  **reject the dependency** — a graph database is a non-starter for a local
  firmware tool.
- **Codebase-Memory** (arXiv 2603.27277, Mar 2026) — 31 languages × 1 repo each,
  12 question categories, MCP graph agent vs a grep/read Explorer, both on Claude
  Opus 4.6:

  | Metric | Graph (MCP) | Explorer (grep/read) |
  |---|---|---|
  | Quality | 0.83 | **0.92** |
  | Tool calls/question | **2.3** | 4.8 |
  | Tokens/question | **~1,000** | ~10,000 |
  | Latency | **<1 ms** | 10–30 s |

  Graph wins hub detection and caller ranking on 19/31 languages; Explorer wins
  full source context (16/31) and exhaustive call-site grep (10/31). **Macro-heavy
  C: 0.58 vs 1.00**, even after they bolted on LSP-style type resolution for Go, C
  and C++.
  **Caveats, stated plainly**: answers graded by the first author; one repo per
  language; one LLM; thresholds "chosen pragmatically"; it is a vendor paper —
  `codebase-memory-mcp` is their product. **Ignore the tool. The evidence is
  load-bearing anyway**: 10× token reduction at ~90% quality is the right
  expectation, *except in C, where the naive version loses to grep.*
- **treeloom** (https://github.com/treeloom/treeloom) — MIT, runs fully local in
  "simple mode." Self-run Sept 2026 benchmark, ~1,900-file C#/TS repo: **11–47%
  cheaper per query than a grep agent, quality tied, fewer turns.** The sentence
  that matters most for scoping: **largest savings (25–47%) on symbol-free
  questions; when the identifier is already in the question, grep finds it
  directly and the advantage collapses to 11–20% cost alone.** That tells you
  exactly when an index pays. 2 stars, C/C++ untested, raw rows not shipped.
- **blarify** (https://github.com/blarApp/blarify) — **supports SCIP and claims
  up to 330× faster reference resolution than LSP.** Corroborates the SCIP path;
  a C++ fork exists (`tomorrowCoder/blarify_cpp`).
- **potpie**, **code-graph-rag** — ignore; graph-DB dependencies and tree-sitter
  blindness. `code-graph-rag` is the most mature multi-language tree-sitter graph
  MCP if the SCIP path dies.

## Index versus grep: what the evidence actually says

Ranked by methodological strength.

1. **Agent Retrieval Bench** (arXiv 2607.24882, Jul 2026,
   https://arxiv.org/html/2607.24882) — **the strongest source.** Isolates the
   context-acquisition step. From 287 logged real trajectories: an OpenAI
   strict-context agent reads 3.2 files/sample and **never touches the gold file
   on 35.2%** of samples; Codex CLI reads 6.2 files/sample and **misses gold on
   27–29%**. Seeding the agent with retrieval results, on a 45-sample pilot:
   random non-gold seed **+0.0215** File F1, lexical **+0.0759**, RRF hybrid
   **+0.0744**, oracle gold **+0.3115** (upper bound) — with fewer post-seed
   tokens and tool calls. No single retriever dominates (best MRR 0.2379,
   Recall@20 0.7029; RRF fusion lifts to 0.2713 / 0.7331).
   **The result that should shape this design**: on *trace2code* (failure trace →
   root-cause implementation), **a repo-map-style structural ranker beats every
   embedding model** (MRR 0.2742), because agentic relevance is *structural, not
   semantic* — the file you need is often not textually similar to the query.
   Structure also wins context-packing outright (RepoMap BCY@8k 0.3788).
2. **LocAgent** — +10.5% / +19.2% / +12% Pass@10, as above.
3. **RepoGraph** — +32.8% relative on SWE-bench.
4. **Codebase-Memory** — 10× fewer tokens at 0.83 vs 0.92; **0.58 vs 1.00 on C**.
5. **treeloom** — 11–47% cheaper, quality tied, savings only without the identifier.
6. **CORE-Bench** (EMNLP 2026, https://arxiv.org/abs/2606.11864) — 180K+ queries;
   headline is "a sharp drop from traditional code search to code retrieval in
   agentic coding settings," i.e. **off-the-shelf embedding retrievers are much
   worse at agent-relevance than their code-search scores suggest.**
7. **Anthropic's and Cline's claims — assertion only.** Boris Cherny: *"Early
   versions of Claude Code used RAG + a local vector db, but we found pretty
   quickly that agentic search generally works better"*
   (https://vadim.blog/claude-code-no-indexing/). **Never published with a number,
   a benchmark, or a methodology** — the most-cited claim in this space and the
   least-evidenced. It also describes *RAG with a vector DB*, not a structural
   index; nobody at Anthropic has publicly claimed grep beats a code graph. Cline
   names three failure modes without numbers: chunking tears logic apart, the
   index decays against a live tree, embeddings double the IP security surface
   (https://cline.bot/blog/why-cline-doesnt-index-your-codebase-and-why-thats-a-good-thing).

**The honest synthesis:**

- **Embeddings for code: the evidence is genuinely against them.** Sourcegraph
  dropped them, Anthropic and Cline never shipped them, CORE-Bench shows they
  degrade in agentic settings, and the offline constraint kills them regardless.
  Treat as settled.
- **Structural index vs grep is not a competition.** The index wins on cost and
  on structural questions; grep wins on exhaustive and full-context questions.
  Every quantified source agrees on roughly 10× tokens and 2× tool calls at ~90%
  of the quality, **concentrated on questions where the agent does not already
  know the identifier.**
- **So the architecture is a seed, not a replacement.** Fire before grep, cut the
  search space, leave Grep and Read fully intact.

## Design constraints this survey imposes

1. **Seed, don't replace.** +0.076 File F1 from a good seed; 27–35% of pure
   agentic runs never reach the right file.
2. **Budget the always-loaded map at ~1k tokens, with a ~8k cold expansion.**
   aider and `scipq` converged on this independently.
3. **Watch the MCP tool-schema tax.** Schemas load into every message; duplicating
   Claude Code's native tools is a net context *loss*. Keep to ~5 verbs; do not
   re-expose file reads or shell.
4. **One index = one build configuration.** Unsolved across the whole market.
   Either scope to the active build, or make cross-config diff ("which `CONFIG`
   flips this file in") a deliberate, novel feature — what undertaker did for
   Linux in 2014 and nobody has done for Zephyr or for an agent.
5. **Never present a grep result as a graph answer.** `scipq`'s rule, verbatim.
   It is the difference between a tool an agent can trust and one that launders
   guesses.

## Variability-aware prior art (right ideas, wrong code)

- **TypeChef** (https://github.com/ckaestne/TypeChef) — variability-aware parser
  for unpreprocessed C keeping all `#ifdef` branches, built for kernel-scale
  feature counts. Research-grade Scala, effectively unmaintained.
- **undertaker** — parses Kconfig, emits SAT problems, finds **dead** blocks (no
  valid config selects them) and **undead** blocks (present in every config).
- **KernelHaven** (https://arxiv.org/pdf/2110.09758) — infrastructure composing
  these extractors.

All 2012–2018 era, none MCP-shaped, none Zephyr-aware. The relevant point is that
**Zephyr does not need them**, because its build resolves the configuration and
writes the answer down.

## Open, for later notes to close

- **Does `scip-clang` survive an `arm-none-eabi-gcc` Zephyr compile DB?** Nothing
  found answers this. It gates the preferred architecture.
- Whether one index per build configuration is acceptable, or whether cross-config
  diff is the differentiating feature.
- Whether the `scipq` verb set survives contact with C, where it has never run.
