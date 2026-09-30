# embarch-ui decisions: Shape and stack

**Status:** active, 2026-09-02.

One consolidated process replacing three ad hoc UIs, with no build toolchain.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — One consolidated process, not a shared library three separate binaries keep depending on

The same "one implementation, many call sites" shape `embarch-topology` decision 8 established for topology detection — except **here the consolidation is the UI surface itself**, not just the logic behind it. `embarch-topology`'s and `embarch-study-designer`'s standalone UI binaries (413 and 812 lines) are retired outright, and Core's enroll page's HTML moves out of Core, which keeps the enroll endpoint it already had. Settled on the repo owner's own framing: "1 UI for the whole project, just like the topology project centralized all topology from the suite."

### 2 — Zero-build, Rust-served HTML — pushed to a real design system rather than replaced with a framework

The alternative was weighed on its actual merits: an SPA framework plus a bundler, with the built bundle vendored into the Rust binary so the *end user* still runs one binary — buying a real component/chart/table ecosystem and a faster path to polish, against **a second toolchain at build time, new CI legs, new supply-chain surface, and an explicit break of the suite's "Rust, one toolchain" principle.** Decided against, with the corollary that matters: **stop treating plain unstyled HTML as the ceiling** and actually invest in hand-rolled CSS, type and component design. Confirmed against real mockups (decision 8) before committing further.

### 9 — Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui), created empty

Matching how `embarch-umbrella`, `embarch-topology` and `embarch-dev-bench` each started: the path dependencies decision 5 requires **needed a real repo to exist before implementation could begin in earnest.**

The VS Code launcher (decisions 3, 28) is its own file: [decisions/launcher.md](launcher.md).
