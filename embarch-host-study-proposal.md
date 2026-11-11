# Proposal: host-run studies, operator prompts, bench instruments and a USB PD bench

**Status:** proposal, 2026-10-09.

Spans `embarch-topology`, `embarch-core`, `embarch-study-designer`, `embarch-api`, `embarch-ui` and `embarch-dev-bench`, which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). A USB Power Delivery DUT is tested with a PD partner, an electronic load and a person who plugs cables, none of which the dev bench can be; this is the study kind Core runs itself for that.

## What is built

Phases 1 to 3, each in its own sub-project's docs:

- **`embarch-study-designer`** — `HostStudy` and its four actions, the teardown and the refusal marker: [decision 80](embarch-study-designer/decisions/study.md).
- **`embarch-core`** — `POST /host-studies` and its taps: [decisions 95, 98](embarch-core/decisions/host-study.md); instrument commands: [104](embarch-core/decisions/instruments.md); the prompt: [105](embarch-core/decisions/host-prompt.md).
- **`embarch-topology`** — the `instruments` table: [decision 49](embarch-topology/decisions/instruments.md).
- **`embarch-api`** — the instrument tools: [decision 97](embarch-api/decisions/instruments.md); `run_host_study` and `answer_prompt`: [99](embarch-api/decisions/host-study.md).
- **`embarch-ui`** — the prompt modal: [decision 69](embarch-ui/decisions/operator-prompt.md).
- **`embarch-dev-bench`** — the PD bench app and its two shields, built from its own `workspaces/pd-bench/` (Zephyr v4.4.2 plus six carried USB-C patches): [decisions 48, 49, 58](embarch-dev-bench/decisions/pd-bench.md); its commands in [`pd-bench/README.md`](../embarch-dev-bench/pd-bench/README.md).

## What is left

1. **A first host study on a real bench.** Topology decision 49 and core decision 98 each state what is unverified.
2. **Numbers stay exact or absent:** v1 records an SCPI reply as text. A declared numeric parse can come later.
3. **Host-study rows in the Study Designer tab** come later.
4. **Fold:** this file is deleted as the rest is absorbed.

## Open questions

- Whether a host study may also drive the dev bench later (mixed studies). Out of scope here.
