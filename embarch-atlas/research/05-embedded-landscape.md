# The embedded landscape: who is already doing this

**Status:** draft, 2026-09-22.

The firmware-specific corner: vendor and startup activity, commercial architecture
tools as possible backends, hardware traceability prior art, and whether
static+runtime fusion is novel. Plus the honest answer to "what is actually
unclaimed."

## The finding

**The analysis primitives are commoditized; the joins are not.** Call graphs,
symbol search, callers/callees and dead-code detection for embedded C are already
free and firmware-specific (`fw-context-mcp`, MIT, 37 MCP tools) and already
commercial with an official MCP surface (SciTools Understand ships `undmcp`).
What nobody does — vendor, startup or research product — is join **build config →
code**, **code → physical hardware**, or **runtime trace → code structure**.

Those three joins are the white space. **The third is only buildable by someone
who already owns the probe.**

Supporting census: seven silicon vendors shipped MCP servers between Oct 2025 and
Aug 2026, and **zero of them analyse your codebase.** They do doc lookup (3),
toolchain control (3), live debug/capture (4), fleet data (2), runtime-fused
comprehension (**0**). Source, and the most useful single page found:
https://veecle.ai/blog/hardware-mcp-servers-2026

## Direct competitors

### Embedder — the serious one
https://embedder.com/, YC S25, founded 2025, ~6 employees, backed by CRV, Box
Group, Emerson Collective.

Claims 500+ MCUs / 3,000+ peripherals across 13 manufacturers (including Nordic);
C/C++/Rust; **Zephyr** and nRF Connect SDK among the supported stacks; EDA
ingestion from Altium/KiCad/Eagle/PADS. Features: "Datasheet Intelligence" (every
register value cited to the manual), schematic/netlist → board-specific drivers,
hardware debugging with logic-analyzer and scope captures analysed as structured
data, power profiling correlated to code, closed-loop build-flash-test-repair with
parallel test agents. VS Code extension plus CLI/daemon. Cloud-first, SOC 2 Type
II + ISO 27001, with customer VPC and **on-prem/air-gapped available**. Pricing
scoped case by case; claims 100+ paying customers in automotive, aerospace,
medical and IoT. v0.3.1 shown at embedded world; nominated for Embedded Award
2026 (Startup), 16 Mar 2026.

**10 Sep 2026: announced SEGGER J-Link/J-Trace integration** — flash, breakpoints,
register/memory inspection, RTT monitoring. **Not yet GA**, joint webinar 29 Sep
2026, no success rates or named deployments disclosed
(https://runtimewire.com/article/embedder-segger-ai-firmware-hardware-debugging).

**The structural gap in their model, and it is the defensible angle here**:
Embedder is grounded in *vendor documentation* and generates then verifies new
code. Every description of the product runs forward — datasheet to code. Its
analysis capability is "validates against documentation," not "comprehends your
existing proprietary codebase." **You cannot index a client's undocumented 200k-
line Zephyr tree from vendor reference manuals.**

### Embedd — the other one
https://embedd.it/, a different company (Ukrainian-founded, $2.7M pre-seed led by
Seedcamp, Aug 2026). AI datasheet → driver/devicetree/BSP generation, one HAL
architecture across a portfolio, every generated line traced back to a register
definition, MISRA-C/AUTOSAR output. Again generation with traceability, not
comprehension of existing code.

## Vendor MCP servers — all doc, control or debug

| Vendor | Product | Date | License | What it does |
|---|---|---|---|---|
| Arm | `arm/mcp` | Oct 2025 GA | Apache-2.0 | x86→Arm migration scan, `sysreport`, doc search, remote profiling |
| Arm | Performix Dynamic Insights | Aug 2026 | free/proprietary | profiling insights; needs a real-hardware run |
| Nordic | nRF Connect SDK MCP | May 2026 | proprietary, myNordic | semantic search over SDK docs + build/program/debug commands |
| Nordic | nRF Cloud MCP | May 2026 | proprietary, OAuth | 16 read-only fleet tools |
| Analog Devices | CodeFusion AI Debug Assistant | Mar 2026 | Apache-2.0 | 23 tools; live register/memory/stack, Cortex-M + RISC-V fault decode, ELF analysis; **local HTTPS** |
| Espressif | ESP-IDF Tools Local MCP | Apr 2026 | Apache-2.0 | build/flash/clean/configure |
| Microchip | MCP + MPLAB-DOCS | Nov 2025 | free | product/compliance + doc search |
| Silicon Labs | `mcp.silabs.com`, Network Analyzer | 2026 | proprietary | doc search; sniffer control |
| TI | CCS 21.0.0 bundled servers | 2026 | proprietary/local | needs CCS open + XDS110 |
| Golioth | `tinymcp` | Jul 2025 | Apache-2.0 | on-device RPCs via cloud; **no pushes since launch** |

No official server from ST, Infineon, Renesas or NXP. **Memfault** is cloud-hosted
only, 18 read-only tools, explicitly a fleet-data query interface and **not a code
repository connector** (https://docs.memfault.com/docs/platform/mcp-server).
**Percepio** has no AI/LLM/MCP story at all in any 2026 material. **SEGGER** has
no server of its own; its only AI exposure is the unshipped Embedder integration.

**Consequence for positioning**: Nordic, Memfault, Silicon Labs, Microchip and
Arm's doc servers are all cloud or account-gated. Only ADI, Espressif and TI run
locally, and all three are vendor-locked to their own silicon. **A genuinely
local, vendor-neutral module operating on proprietary client firmware is a real
differentiator** in defense, medical and automotive.

## `fw-context-mcp` — the closest analog, and it should be read first

https://github.com/turbyho/fw-context-mcp — MIT, on PyPI at 0.32.0. Its own
pitch: *"C/C++ semantic index for AI coding assistants — powered by your
compile_commands.json. Query the program your compiler actually builds, not just
the source files."*

Persistent index from libclang AST; FTS5 full-text plus vector embeddings plus
optional local Ollama for natural-language query translation. Local-first, no
external services. Supports Zephyr, PlatformIO, Mbed OS, Arduino, ESP-IDF, generic
CMake and Makefile, with documented setup for Keil, IAR, STM32CubeIDE and TI CCS.

37 tools, including the firmware-shaped ones: `find_callers` (direct **and
indirect through function pointers**), `find_indirect_call_sites`,
`find_indirect_targets`, `find_call_path`, `find_all_callers_recursive`,
`find_callees_recursive`, `find_dead_code`, `find_hotspots`, `trace_data_flow`
(experimental), `read_file` with **ifdef-filtered content for the current build**,
`list_variants` ("every indexed build with variant, image, and board identity"),
`get_symbol_context`, `explain_symbol`, `semantic_search`.

**Maturity: 10 stars, 898 commits**; the author says interfaces and indexing
behaviour are still evolving. **Critically, from its own `docs/tools.md`: no tools
for devicetree, SVD, Kconfig, or runtime traces.**

So it has independently arrived at the same premise — index what the compiler
actually builds — and stopped exactly where the firmware-specific value starts.
That is simultaneously the strongest validation of the direction and the clearest
statement of what is left to own.

Others in the same space: `mcp-cpp` (Rust, clangd LSP), `clangd-mcp` (impact
analysis), Serena, codebase-memory-mcp, CodeLogic MCP. Zephyr-specific MCPs are
toys: `hakehuang/zephyr_mcp` (6 stars, west build/flash/twister plus git,
explicitly not a code analyzer) and `leog25/zephyr-west-mcp` (workspace and
Kconfig-presence introspection).

## Static + runtime fusion: novel in this framing

**Nobody ships it for MCUs, agent-facing.** The four closest:

1. **Arm Performix Dynamic Insights** (Aug 2026) — explicitly "connecting source
   code with runtime behavior across the system," exposed through Arm's MCP
   server. But it targets **Neoverse servers and Linux**, not Cortex-M.
2. **Qt Coco MCP Server (preview)** — "exact code coverage data from real test
   runs directly into your AI coding agent workflow," per-instrumentation-point
   execution data as agent context, with a feedback loop driving test generation
   (https://www.qt.io/blog/introducing-the-coco-mcp-server-preview). **The best
   existing proof that static+runtime fusion for an agent works** — and it is a
   preview, in a non-embedded-first product.
3. **ADI CodeFusion AI Debug Assistant** — live register/memory/stack plus ELF
   symbols over MCP, but halt-state inspection rather than a trace over time.
4. **Vector VectorCAST** — the one commercial product that genuinely fuses static
   and runtime for embedded: source instrumentation for statement/branch/
   condition/**MC/DC** coverage on the real target, TRACE32 integration for
   non-intrusive coverage, and a complete Python data API. But framed and priced
   as *certification evidence*, not comprehension. Quote-only.

**Percepio Tracealyzer** is task-and-event level (tasks, ISRs, queues, user
events), not function-level structure tied to source; no scriptable API, no MCP.
**$2,395/yr single-user node-locked** on reseller list; Percepio View is free for
Zephyr. **SEGGER SystemView** added loading the firmware ELF directly into a
project in March 2026 — a small step toward symbol resolution. Ozone is ~$750/seat
commercial, free with J-Link PLUS and above.

**A constraint worth knowing**: Zephyr's gcov coverage collects into RAM, not a
filesystem, and the docs state support is "currently enabled only for QEMU
emulation of embedded targets" because of RAM size
(https://docs.zephyrproject.org/latest/develop/test/coverage.html). On-target
coverage on a real MCU means the VectorCAST source-instrumentation route or
TRACE32 hardware.

ETM/ITM dynamic call-graph reconstruction is academically well-established (e.g.
FrankenTrace, https://dl.acm.org/doi/fullHtml/10.1145/3576914.3587521) but **no
product turns an ETM stream into a code-structure-annotated comprehension
artifact.** The 2026 LLM+trace papers are aimed at repair and vulnerability
localization, not comprehension, and none are embedded.

**Verdict: novel in the embedded agent-facing framing, moderately hard.** Zephyr
already emits SystemView/CTF traces with task and ISR identity, and this suite
already owns capture. The hard part is the **join key** — mapping trace events to
source symbols across a build with heavy `#ifdef` and devicetree-driven
instantiation. `fw-context-mcp`'s `list_variants` shows the build-variant problem
is recognized; nobody has solved it *together with* runtime.

## Hardware traceability: the most under-served area, with free ingredients

**CMSIS-SVD is the only broadly-covering machine-readable hardware truth**:
device → peripherals → registers → fields, with reset values, access policies and
descriptions comparable to the reference manual. Aggregated free at
https://github.com/cmsis-svd/cmsis-svd-data. Tooling: `svd2rust`, `svdtools` (YAML
patches for the endemic vendor errors), `svd2pac`, SVDSuite.

**The asymmetry to exploit**: the Rust embedded ecosystem has the strongest
code↔hardware chain that exists — SVD → PAC → HAL → BSP, compile-time checked.
**That chain does not exist in C**, where the same information is a wall of
`#define` and vendor HAL structs with no link back to the SVD. Rust solved it by
*regenerating* code from the hardware model; C never can, so the only route in C
is *recovering* the link analytically — which is precisely a static-analysis
problem.

Agent-facing SVD today, both shallow, and neither says anything about code:
- `mcp-svd` (pkt-lab, MIT) — 4 tools, bundled SVDs including nRF52840. Purely a
  hallucination guard.
- `jlink-mcp` (Klievan) — 47 tools: halt/resume/step, memory and register access,
  flash, Cortex-M fault decode, RTT streaming, GDB source-level debugging, and
  **SVD-decoded peripheral registers**. HIL-tested with 58 tests against a real
  nRF52840-DK. **This overlaps the probe surface this suite already owns — read it
  as a reference to that, not to atlas.**

**Datasheet + LLM research is real, recent and unproductized:**
- **SpecMap** — "Hierarchical LLM Agent for Datasheet-to-Code Traceability Link
  Recovery in Systems Engineering," arXiv **2601.11688** (16 Jan 2026),
  https://arxiv.org/abs/2601.11688. Hierarchical narrowing: repo-level inference →
  file-level relevance → symbol-level alignment, explicitly covering **macros,
  structs, constants, configuration parameters and register definitions** in
  systems-level C/C++. **73.3% file-mapping accuracy, 84% fewer LLM tokens, ~80%
  faster** than IR baselines. This is almost exactly "which datasheet section
  explains this code," published as research with **no product behind it.**
- arXiv **2608.25217** (2026) — datasheet-aware hardware compatibility
  verification, 97.5% accuracy, 8.6× input context reduction.

On devicetree: Zephyr adopted Linux pinctrl in 3.0, and **no tool resolves
devicetree + pinctrl + Kconfig into "this driver instance drives these physical
pins on this peripheral instance."** The best public guidance
(https://www.beningo.com/zephyr-devicetree-with-ai/) concludes AI "still makes
binding, bus, and pin mistakes" and its output must be treated as a draft verified
by a build.

**So: yes, a tool could answer "which physical peripheral does this code touch,
and what does its datasheet say" — and nothing does.** Every ingredient is local
and offline-capable: SVD (free, aggregated), the resolved devicetree from the
build, `.config`/`autoconf.h`, `compile_commands.json`, and the ELF/map.
**Zephyr uniquely makes this tractable because the build already emits a resolved
hardware model on disk** — a moat a generic C tool cannot copy.

This also fits an existing standing rule in this suite: cite the register field,
do not infer the behaviour.

## Commercial architecture tools as a backend

**SciTools Understand is the only real candidate.** Python 3 API (Perl deprecated
2026), `und` CLI, and an **official MCP server, `undmcp`**, shipping in its `bin`
directory (https://docs.scitools.com/support/solutions/articles/70000680031-setting-up-an-mcp-server)
exposing entity search, call-graph traversal, reference walking, file dependency
tracing, source browsing and CodeCheck violations.

- **Price: $100–$120/user/month, 12-month minimum**, with offline/secure-lab
  licensing at the same cost (https://scitools.com/pricing).
- **The trap**: the developer license **excludes** `und` command-line automation,
  **API access**, and exporting dependencies/graphs/metrics — i.e. exactly what an
  agent backend needs. "Contact sales" for the tier that has them. Budget
  >$1,440/seat/yr.
- **Weakness for this use case**: a C/C++ parser with no notion of Kconfig,
  devicetree, SVD, linker maps or build variants. Its `#ifdef` handling is
  configuration-driven, not build-truth-driven.

Others: **Lattix** 2026.0 (28 Jul 2026) added an MCP server, an Ada module and a
VS Code extension; price not public; good for architecture conformance, poor for
explaining code to an agent. **Imagix 4D** — no API or MCP story at all;
Verifysoft lists company-wide floating licenses from **€4,100–€9,800** for the
first license. **Axivion Suite** (Qt-owned) — TÜV-certified to ASIL-D / SIL 4;
architecture *conformance checking*, not comprehension; no MCP. **Klocwork** and
**CodeSonar** find defects, do not explain code, and publish no pricing.

**Backend verdict: libclang/clangd as the primary substrate.** Requiring a
$1.4k+/seat/yr proprietary backend to analyse *client-proprietary* firmware is a
hard commercial sell, libclang is free and local, and `fw-context-mcp` is a
working firmware-specific proof that it suffices. Treat Understand as an optional
backend for customers who already own seats, never a dependency.

## The white space, named honestly

**Genuinely unclaimed:**

1. **The build-truth model as first-class agent context.** Nobody joins
   `compile_commands.json` + `.config`/`autoconf.h` + resolved devicetree + linker
   map + ELF into one queryable model. `fw-context-mcp` does the first and flirts
   with variants; the Zephyr MCPs verify Kconfig presence but never relate it to
   code; Understand has no concept of any of it. *"In this build, which driver
   instance is compiled in, on which bus, on which pins, and who calls it"* is
   unowned — **and it is the question that silently wrecks generated firmware
   today.**
2. **Code → hardware reverse traceability.** SpecMap proves feasibility as
   research. Embedder and Embedd commercialize the **forward** direction. Nobody
   does the reverse on existing proprietary code.
3. **Trace-to-structure fusion for MCUs.** Zero vendors. Arm does it for servers,
   Qt Coco for coverage in preview, VectorCAST as certification evidence. The join
   — trace event → symbol → call path → devicetree node → peripheral — **is the
   one differentiator no competitor is positioned to build: silicon vendors have
   the hardware but not your codebase; code-analysis vendors have your codebase
   but no probe. This suite has both.** That argues for designing the schema with
   the runtime join in mind from day one, even shipping static-only first.
4. **Fully local, vendor-neutral, proprietary-firmware posture**, per the vendor
   table above.

**Mostly a packaging problem — do not rebuild:** call graphs, callers/callees,
function-pointer resolution, dead code, symbol and semantic search (solved, free,
firmware-specific in `fw-context-mcp`); doc and SDK lookup (every vendor shipped
it in twelve months); flash/probe/RTT/register inspection (`jlink-mcp` gives 47
free tools, and this suite already owns the capability).

**Risk to name: Embedder is converging on this suite's territory from the
generation side** — well funded, 100+ paying customers, VS Code plus CLI, on-prem
option, and a probe integration announced 10 Sep 2026. The defensible angle is
comprehension of existing proprietary firmware, which their documentation-grounded
architecture structurally does not address.

## Sourcing caveat

Several search results were SEO content farms quoting invented statistics
("34% faster," "42% of embedded teams fine-tune their assistant"). Those numbers
were excluded. Everything cited here traces to a vendor page, a docs page, a
GitHub repo, an arXiv paper or a dated press item.
