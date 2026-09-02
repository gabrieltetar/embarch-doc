# embarch-ui decisions: The shell and the design system

**Status:** active, 2026-09-02.

One app behind a persistent sidebar, and a design system settled against real mockups.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 4 — One app, not linked-but-separate pages

A persistent left sidebar plus a top status bar, with **six** sections behind it: Dashboard, Topology, Study Designer, Enroll, Trace, Debug — the last two present in none of the three surfaces this replaces. Client-side navigation, one shared header throughout, **so it reads as one product rather than a pile of tools that happen to share a port.**

**Trace is its own section rather than a panel inside the Study Designer's run card**, for one reason: **a trace belongs to a *completed* study, which is not necessarily the one this tab currently has in its table** — a run from an hour ago, or one a terminal submitted, is exactly as valid a thing to open, and a per-run panel could only ever show the run you just did. The run card links into it, handing over the study id, so the common case costs no typing.

**Navigation is by URL fragment, and the fragment carries parameters where a section needs them** — `#topology` is already `embarch-topology`'s own fix-it destination. Parameters in the fragment rather than the query string, because **the fragment already selects the section, so an address is one mechanism rather than two**, and because **a fragment never reaches the server**: linking somebody to a trace costs no round trip and puts no study id in a log.

### 8 — A visual design system, settled against real mockups

Dark-first developer-console aesthetic, togglable to light: IBM Plex Sans for UI text and Plex Mono for data, parameters and log lines; an oklch token system with one cyan accent and green/amber/red semantics holding chroma and lightness across hues; and a real component set — stat cards, status badges, data tables, pill toggles, chip inputs, a terminal-styled console — **replacing the two source UIs' single inline `style=` attribute and bare `<style>` block respectively.** Hand-authored CSS throughout, no bundler (decision 2).

**Both palettes are lifted verbatim from the mockups rather than re-derived.** The light half looked unexercised until the saved mockup files were read directly and found to author a complete light token set alongside the dark one.
