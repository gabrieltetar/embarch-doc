# Repo comprehension for LLM agents: what the evidence says

**Status:** draft, 2026-09-22.

The research and evaluation literature, 2023–2026, on letting an agent understand
a repository without reading it. Run to settle the one method question left open
at scoping: **deterministic extraction vs a deterministic core plus LLM prose vs
embeddings/RAG.**

## The answer

**Deterministic core wins, and it should be compiler-backed rather than
tree-sitter-backed because the target is C with macros and `#ifdef`s. A thin,
tightly-scoped LLM prose layer is worth adding second. Embeddings are worth the
least and should be last or never.**

In one line: **deterministic structural + lexical core (must build) → short
role-level prose regenerated from it (should build, cheap, capped) → embeddings
(only over prose and docs, if at all).**

## Rank 1 — deterministic extraction. Strong evidence.

**The closest published analogue to this sub-project exists, and it is
deterministic.** "Repository Intelligence Graph: Deterministic Architectural Map
for LLM Code Assistants" (arXiv 2601.10112, https://arxiv.org/pdf/2601.10112)
builds its map from *build and test artifacts*, not source text — it runs CMake's
File API and instantiates nodes by explicit rule, stating "no non-deterministic
behavior is involved in building RIG." **Every node and edge carries an
`Evidence` pointer to a concrete location in a build file**, enforced as a schema
invariant.

Measured on 8 repos including C/C++ and a Meson-built **firmware** repo, driving
three real commercial agents (Claude Code, Cursor, Codex):

| Measure | Result |
|---|---|
| Mean relative accuracy | **+12.2%** |
| Completion time | **−53.9%** (−124.4 s/repo) |
| Seconds per correct answer | −57.8% |
| Low-complexity repos | +6.6% accuracy |
| **High-complexity repos** | **+17.7% accuracy, +69.5% efficiency** |
| Medium/hard questions | up to +28.6% |

**Map size: 20,692 bytes average ≈ 5,173 tokens**, ranging 494 tokens
(hello_world) to ~8,767 at high complexity, largest ~15,000. **That is the
empirical answer to how big the always-loaded map should be.**

**Deterministic graphs beat LLM-extracted ones head to head.** "Reliable
Graph-RAG for Codebases: AST-Derived Graphs vs LLM-Extracted Knowledge Graphs"
(arXiv 2601.08773, https://arxiv.org/pdf/2601.08773), on OpenMRS/ThingsBoard/
Shopizer with SWE-bench and RepoEval: AST-derived graphs achieve perfect relation
precision and byte-identical output across runs; **LLM extraction introduces
hallucinated edges — relationships not present in the code** — costs more API
calls, and is not reproducible. The conclusion is unambiguous.

**Structural indices produce the biggest measured agent lift in the localization
literature.** LocAgent (ACL 2025, https://aclanthology.org/2025.acl-long.426/),
SWE-bench-Lite:

| Method | File Acc@5 | Module Acc@10 | Function Acc@10 |
|---|---:|---:|---:|
| BM25 | 38.69% | 52.92% | 36.86% |
| E5-base-v2 (embed) | 49.64% | 72.26% | 51.09% |
| CodeRankEmbed (code embed) | 52.55% | 78.83% | 58.76% |
| Agentless | 72.63% | 68.98% | 58.76% |
| SWE-Agent | 77.37% | 78.10% | 64.60% |
| OpenHands | 76.28% | 83.58% | 70.07% |
| **LocAgent** | **77.74%** | **87.59%** | **77.37%** |

RepoGraph (ICLR 2025, https://arxiv.org/abs/2410.14684) plugged into four
existing frameworks: **+32.8% average relative** resolve-rate improvement
(+99.63% relative for a RAG baseline, +8.56% for Agentless).

**And the deterministic index is nearly free to build.** Codebase-Memory
(https://arxiv.org/html/2603.27277v1) indexes the **Linux kernel — 28M LOC, 75K
files — into 2.1M nodes / 4.9M edges in ~3 minutes**, with ~1.2 s incremental
re-index and <1 ms queries. **Scale is not an obstacle for a firmware tree.**

## Rank 2 — LLM prose, but only a thin "role" layer. Moderate evidence, with a C-shaped hole.

The cleanest experiment is "Retrieval-Oriented Code Representations in Agentic Bug
Localization" (arXiv 2607.11046, https://arxiv.org/html/2607.11046), comparing
five per-file representations. SWE-bench Verified, Hit@5:

| Representation | BM25 | Dense | Footprint |
|---|---:|---:|---:|
| STRUCT (file paths only) | 28.4% | 51.6% | 2.9M tok (1×) |
| **ROLESUM** (short "what this file is for") | **44.0%** | **72.4%** | 39.7M (13.7×) |
| TECSUM (detailed technical summary) | 37.8% | 67.0% | 245M (84.5×) |
| BUGSUM (synthetic bug reports) | **9.4%** | 37.4% | 33.6M (11.6×) |
| RAW source | 67.6% | 73.2% | 830M (286×) |

Four things fall out, and they are the whole guidance for a prose layer:

1. **Short role summaries beat path-only by a lot** — +55% relative on BM25, +40%
   on dense. Prose earns its place.
2. **Longer, more detailed summaries do not pay.** The paper's words: detailed
   summaries "are not worth the extra token volume." TECSUM is 6× ROLESUM's
   footprint and loses to it.
3. **The most generative representation actively destroys retrieval.** BUGSUM —
   where the model invents plausible failure narratives — scores **9.4% against
   the 28.4% path-only baseline, i.e. −67%.** This is the measured version of
   "LLM prose drifts and misleads," and it is the strongest quantitative warning
   in the corpus against prose that goes beyond role into behaviour.
4. **Raw code still wins on raw accuracy.** Summaries are a *compression* play,
   not an *accuracy* play.

Hierarchical summary trees do help routing at scale: on a real industrial system
(46 repos, 1.1M LOC, 87 bug tickets, arXiv 2512.05908) Pass@10 0.82 / MRR 0.50
against Copilot 0.61/0.25 and Cursor 0.57/0.27 — and **removing the
directory-level filtering tier costs −54% MRR and +44% tokens.** That is direct
support for the map-then-drill-down shape.

**But the C-shaped hole is large.** CodeWiki (arXiv 2510.24428,
https://arxiv.org/html/2510.24428v1), 21 repos across 7 languages, rubric-scored
against official docs: DeepWiki 64.06%, CodeWiki-sonnet-4 68.79% — and
**C/C++ 53.24% versus Python/JS/TS 79.14%, a 26-point gap.** Generated
architectural prose about C is measurably the least reliable kind. (The eval's own
rubrics reach only ~73% self-consistency, so read the scores as coarse.)

Hallucination in code summaries is an established, named phenomenon — PACMSE
https://doi.org/10.1145/3808139 and ETF https://arxiv.org/pdf/2410.14748,
motivated explicitly by production documentation tools.

## Rank 3 — embeddings/RAG. Weakest case, one counter-example that does not transfer.

**Zero-shot embeddings collapse at repository-scale localization.** CORE-Bench
(arXiv 2606.11864), NDCG@10 / Recall@100 for Qwen3-Embedding-8B:

| Level | NDCG@10 | Recall@100 |
|---|---:|---:|
| L1 code understanding | 71.7 | 96.9 |
| **L2 issue → edit localization** | **20.3** | **48.0** |
| L3 broader context | 34.4 | 41.5 |

L2/L3 is the task that matters here. In-domain fine-tuning on PR data lifts L2 to
32.8 — still poor, and it needs a training corpus. Per-language after SFT:
JS 39.8, Go 38.8, Python 33.7, **C++ 29.1**, Java 21.8.

**The one strong pro-embedding result is SweRank** (arXiv 2505.07849): a
fine-tuned code retriever plus reranker beating agentic localization outright —
SWE-bench-Lite file Acc@1 **83.21%** (vs LocAgent 77.74%), function Acc@10
**88.69%** (vs 77.37%), at **$0.011/instance against LocAgent's $0.66**, up to 6×
better accuracy-per-dollar. **Take it seriously, then discount it**: SweRank is
trained on a large mined GitHub-PR corpus that is Python-dominant, and its whole
advantage is in-domain supervision. **There is no equivalent corpus for
Zephyr-style embedded C**, and CORE-Bench shows the zero-shot version failing.

**Lexical search is not optional; semantic search mostly is.** LocAgent's
ablation is the sharpest evidence: removing `SearchEntity` (backed by a BM25
sparse index) costs **−19.34pp file accuracy — the single largest drop** — and
removing just the BM25 index inside it costs ~−11pp, **more than removing graph
traversal** (−2.19pp file / −5.47pp function). **The graph is the multiplier;
keyword search is the floor you cannot remove.**

"Is Grep All You Need?" (arXiv 2605.15184) finds grep beating vector retrieval on
every harness/model pair under inline tool-result delivery (93.1% vs 83.6% with
Claude Opus), with the ordering partly reversing under programmatic delivery.
**Caveat, and it matters: this is LongMemEval, a conversational-memory benchmark,
not code.** Directionally supportive, not decisive. The widely-circulated "grep
beat vector search" blog genre is hype with this kernel of truth.

Where dense retrieval does have an edge: CodeRAG-Bench (arXiv 2406.14497) finds
dense models often beating BM25 for code retrieval, split by domain — better at
tutorials and docs, worse at program solutions. **Read as: embeddings are for
prose (datasheets, app notes, commit messages), not for symbols.**

## Schema and queries that pay off

### Node types
Converged across LocAgent, Codebase-Memory, RepoGraph and RIG: structural
containment (project / package / folder / **file** / module); definitions
(**function**, method, class, interface, enum, **type**); **build-level** — RIG's
contribution and the one that matters most here — **Component** (buildable
artifact tagged with language and source files), **Aggregator**, **Runner**,
**TestDefinition**, **ExternalPackage**; derived **Community/cluster** from
modularity optimization, which is what powers a cheap architecture overview; and
an **Evidence** attribute on everything (file + line). **RIG enforces evidence
completeness as a schema invariant — that is the mechanism that makes "every
answer traceable" real rather than aspirational.**

### Edge types
**LocAgent uses exactly four and gets SOTA: contain, import, invoke, inherit.**
Codebase-Memory uses ~15 and attaches a **confidence score 0.0–1.0** to
framework-specific heuristic edges — a good pattern for sitting heuristics beside
exact facts. LocAgent's ablation says the semantic (non-containment) edges earn
the accuracy: containment-only drops function Acc@10 from 71.53% to 66.42%.

**For embedded C the edge set to add** (extrapolated, not measured by any paper):
`includes`, `defines_macro`/`expands_to`, `reads_global`/`writes_global`,
`registers_callback`/`implements_via_fn_ptr_struct` (**C's substitute for
inheritance — `inherit` is dead weight in C**), `guarded_by` (→ preprocessor
condition), `selected_by` (→ Kconfig symbol), `binds_devicetree_node`, `isr_for`,
`build_target_includes`.

### Queries with measured payoff
1. **Type-aware multi-hop traversal with direction, hop-count and relation
   filters.** Restricting to 1 hop costs −4.74pp function accuracy; removing it
   −5.47pp. Multi-hop is the point.
2. **Keyword/entity search over a hierarchical entity index with three detail
   levels — fold / preview / full code.** Largest single contributor (−19.34pp
   when removed). The tiering is the context-budget control.
3. **Exact entity retrieval returning file path + line numbers + code** — the
   traceability primitive.
4. **Callers-of / callees-of chains, hub detection, centrality ranking.** Aider's
   repo map does this cheaply with personalized PageRank, boosting identifiers
   mentioned in conversation 10× and in-chat files 50×, then binary-searching to
   a token budget.
5. **Change impact over a git diff**, and **build target → sources → tests**
   (RIG). **For firmware the second is the high-value one**: it answers "what
   actually ships in this build" rather than "what exists in the tree."
6. **Directory/module-level routing before file-level search** — −54% MRR and
   +44% tokens when removed.

### Context budget, with numbers
- **Always-loaded map: ~500–9,000 tokens, cap ~15K** (RIG, measured), buying
  +12.2% accuracy and −53.9% time.
- **Drill-down: ~1,000 tokens/question vs ~10,000** for file exploration (10×),
  2.3 vs 4.8 tool calls; for five structural queries, **~3,400 tokens vs ~412,000
  grepping file by file** (99.2% reduction).
- **Why compression matters at all**: Chroma's "Context Rot" (18 models, July
  2025) shows reliability falling with input length even on trivial retrieval;
  lost-in-the-middle shows **>30% degradation** when the relevant span sits
  mid-context. **A map that adds noise is worse than no map.**
- **Ceiling check**: on original SWE-bench, Claude 2 goes 1.96% (BM25) → 4.80%
  (oracle retrieval) → 5.93% (oracle collapsed to edited regions ±15 lines).
  **Perfect retrieval is worth ~2.4×, and then editing is the wall.** A map buys
  navigation and comprehension, not edit success — do not oversell it.

## What the literature says is NOT worth building

1. **An LLM-extracted knowledge graph.** Hallucinated edges, no reproducibility,
   more cost, worse precision than AST extraction. **If a fact can be parsed,
   parse it.**
2. **Long, detailed technical summaries.** 84.5× the footprint of a path index,
   6× ROLESUM, and it does not consistently beat ROLESUM. **Cap prose at one
   short role sentence per module.**
3. **Any generated content that speculates about behaviour or failures.** BUGSUM
   at 9.4% against a 28.4% baseline. Generated speculation is worse than nothing.
4. **Multi-agent documentation pipelines.** "The Illusion of Agentic Complexity in
   README.md Generation" (arXiv 2606.30524): single-agent ROUGE-L 0.2007 vs
   multi-agent 0.1964, at **7,840 vs 56,242 tokens (7.1×)** and 40 s vs 78 s. The
   multi-agent system wins only on structural formatting — **buy that with a
   template, not with agents.**
5. **A vector DB as the primary retrieval surface for one repo.** Zero-shot dense
   NDCG@10 of 20.3 at repo-scale localization; LocAgent's BM25 removal hurt more
   than its graph removal. A single firmware tree does not need one.
6. **Asking the graph to answer line-level or text-level questions.**
   Codebase-Memory's 9-point deficit concentrates in exhaustive grep patterns,
   line-granularity extraction, comments, string literals and macro-expansion
   behaviour. **Keep grep and keep file reads; the map routes, it does not
   replace reading.**
7. **Forcing the agent to consult the map.** In arXiv 2606.11976, a "nudged"
   variant that raised consultation from 8 to 22 calls **dropped micro-F1 from
   0.471 to 0.436** while pushing token cost to 25.1M. **Expose the surface, let
   the agent choose.**
8. **A graph with no natural-language → query translation layer.** CodexGraph
   drops from **27.9% to 8.3% EM** on CrossCodeEval-Lite when its translation
   agent is removed. A query surface with no ergonomic front door is worth about a
   third of its value.

## The embedded/C finding to design around

**LLMs are materially worse on C, across every task measured.** Multi-SWE-bench
(NeurIPS 2025 D&B, https://arxiv.org/html/2504.02605v1), best resolved rate:

| Python | Java | Rust | C++ | TS | **C** | Go | JS |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 48.20% | 23.44% | 15.90% | 14.73% | 11.61% | **8.59%** | 7.48% | 5.06% |

**C is ~5.6× worse than Python**, attributed to manual memory management,
**complex build systems**, and limited training exposure. CodeWiki adds the
documentation gap (53.24% vs 79.14%). EmbedAgent (arXiv 2506.11003) finds
specific weakness on hardware, peripheral and register knowledge across every
model tested.

**And tree-sitter graphs fail worst on exactly this code.** Codebase-Memory's
per-language table: the macro-heavy **C repo scores 0.58 against the file-
exploration agent's 1.00 — a 42-point gap, its worst of 31 languages.** Stated
cause: "macros lack AST representation in Tree-Sitter, so preprocessor-driven
call sites remain invisible to the graph." Contrast Haskell 0.97 vs 0.98.
**A naive tree-sitter atlas over Zephyr-style C would be the worst case in the
published data.**

**Implication — the single highest-value design decision: the extractor must be
compiler-backed, not text-backed.** `compile_commands.json` plus clangd/libclang
per build configuration gives post-preprocessor truth for the configuration that
actually ships, and Zephyr/CMake already emits it — which also hands you RIG's
Component/Test layer for free. Kconfig and devicetree become first-class node
types with `selected_by` and `binds` edges; **no paper covers that, and it is the
gap this sub-project would fill.**

On using an LLM for the `#ifdef` problem instead: arXiv 2601.16755 reports
GPT-OSS-20B at F1 0.93, beating TypeChef (0.70). **Discount heavily** — the corpus
is 5,000 *synthetic* systems of 4–25 LOC with 1–5 feature macros; on real commits
from Vim/BusyBox/OpenSSL/Linux/Glibc the same model drops to 0.64 accuracy, and
Gemini 3 Pro failed to produce complete output in 45.4% of cases. **Do not build
configuration reasoning on an LLM.**

## Evidence quality

**Strong** (peer-reviewed or large-N): LocAgent (ACL 2025), RepoGraph (ICLR
2025), CodexGraph (NAACL 2025), Multi-SWE-bench (NeurIPS 2025 D&B), SWE-bench
(ICLR 2024), CrossCodeEval (NeurIPS 2023), RepoBench (ICLR 2024), SuperC (PLDI
2012), lost-in-the-middle.

**Moderate** (credible preprints, unreplicated): RIG 2601.10112 — only 8 repos,
most build systems hand-constructed, **but the only study driving real commercial
agents with a deterministic map**. Retrieval-Oriented Code Representations
2607.11046 — the cleanest representation ablation in the corpus. CORE-Bench.
SweRank. CodeWiki (~73% rubric self-consistency). 2512.05908 (single industrial
system).

**Weak, directional only**: Codebase-Memory 2603.27277 — excellent schema and
token numbers, but one repo per language, LLM-graded answers, and it carries
marketing for its own MCP server; **the C=0.58 result is nonetheless the most
decision-relevant number in it, and it points against the authors' own tool.**
"Is Grep All You Need?" — wrong domain. 2601.16755 — toy-scale corpus.

**Genuine gaps, worth knowing:** no benchmark exists for RTOS, Zephyr, Kconfig or
devicetree comprehension. No published measurement of documentation-regeneration
drift for LLM-written module prose over time. **And nobody has published a
head-to-head of "deterministic map alone" vs "deterministic map + LLM prose" on
the same codebase — running that on a firmware tree would be a novel result.**

## The recommendation this note supports

Build the deterministic core from `compile_commands.json` plus clangd, with
Kconfig/devicetree/build-target nodes and an evidence pointer on every fact. Ship
the always-loaded map at **≤8K tokens**. Expose three tools, mirroring LocAgent's
set because its ablation proves each one's contribution: **keyword search over an
entity index with fold/preview/full detail levels** (backed by BM25 or ripgrep —
non-negotiable, biggest single contributor), **type-and-direction-filtered
multi-hop traversal**, and **exact entity retrieval returning path + line range.**
Add **one sentence of role prose per module**, regenerated on change, marked
non-authoritative, never extended into behaviour claims. **Add no embeddings until
something specifically fails without them** — and if ever, point them at prose,
not at symbols.

## Collection caveat

The agent that gathered this hit its WebSearch budget near the end. Two items it
wanted and did not get: exact hallucination rates from the PACMSE
code-summarization paper (ACM returned 403), and a dedicated search for published
evidence that summary indices actively mislead agents beyond the BUGSUM result.
