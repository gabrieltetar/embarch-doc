# embarch-ui decisions: What a page may say about itself

**Status:** active, 2026-09-20.

One rule, applied across every tab: the prose a surface carries about its own model. Kept out of the per-tab groups because it is not a fact about any one of them.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 50 — A page stops explaining itself; a path or a state is the only note that stays

Under almost every title in this UI sat a paragraph of prose: what a board *type* is, that a wire between two headers is invisible to software, that a snippet list is ordered and not a set, that a gap band is a bound and not a measurement. **Forty of them**, across three tabs and a dozen dialogs. Each was true and each was written while the decision behind it was being made — which is the tell. **A design note addressed to the person who just built the surface is not documentation for the person using it**, and eight of them stacked down one tab turn a working surface into a reading task; the reader who wants the reasoning is served better by these files than by a `<p>` they cannot skip.

So a page keeps two kinds of note and no third:

- **A path** — `embarch/topologies/`, `embarch/boards.toml`, `<firmware-repo>/embarch/studies/`, `<firmware-repo>/embarch/protocols/` — because where a fact is written down cannot be inferred from the screen. A paragraph that carried one was cut down *to* it rather than deleted.
- **A state**: a repo whose targets could not be scanned, a study not yet run, no taps declared, waiting for Core. A refusal is a state and stays; a count is not — "3 combinations in this repo's scan", printed beside a list of three, is the list read aloud.

**Everything else went, including the caveats about how to read a chart** — the gap band's bound, the repartition's coverage line, the lane-edge counts, the trace that is not live. *Rejected: keeping those.* They read as a third category, and a third category is how the first forty got there; what a drawn value means is [spec/capture-rendering.md](../spec/capture-rendering.md)'s subject, loaded deliberately by whoever is about to trust the number. **A control legend is not prose about the model and stays**: `wheel over the plot zooms at the pointer, drag pans, double-click fits` is the only place that gesture is written down.
