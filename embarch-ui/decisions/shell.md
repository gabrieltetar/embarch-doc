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

### 25 — The mark's red is a brand token, deliberately not the accent

The project has a real logo now (`embarch-ui/assets/brand/`, a GIMP master exported to the extension icon and the favicon), and the obvious move — make the UI's accent match it — is the one thing that cannot be done. **The mark's red is `oklch(63% 0.194 29)` and `--danger` is `oklch(66% 0.19 25)`: measured in the browser they sit at 1.12:1 against each other, which is to say they are the same colour.** A red accent would make every primary button read as destructive and stop failures standing out, so the accent stays cyan — the only wide band of hue the semantic ramp (red danger, amber warning, green success, blue info) leaves free, which is why decision 8 landed there and not by taste.

So identity and interaction get separate tokens. **`--brand` carries the mark's red and is worn by exactly two things** — the sidebar wordmark and the header glyph — while `--accent` keeps every interactive surface. One token, three call sites, no semantic collision.

**The header glyph is the mark itself, vectorised — not a bitmap.** `assets/brand/trace_mark.py` classifies the master's pixels into the two letters, walks the inside/outside boundary as unit edges, stitches the loops (the A's counter included) and Douglas-Peuckers the staircases back into the straight lines the art was drawn with: 16 vertices for the E, 15 plus a 4-vertex counter for the A, 657 B inline. **The point of tracing rather than embedding a PNG is that two fills can bind to `--text-secondary` and `--brand`, so the glyph follows the theme.** It is cropped to the ink — the master's 25px padding is right for an app icon in its own container and costs a fifth of the linear size at 22px — and drawn in "union" mode, the E as the whole silhouette with the A painted over it, so the letters cannot meet on the jagged interface a nearest-letter split of the dark outline produces. The script is committed, so a new master regenerates the glyph.

**The same tracer emits the whole mark as a standalone SVG, outline and all** (`assets/brand/embarch-mark.svg`, 693 B, 53 vertices). Its `layers` mode adds a third path — the dark stroke as the entire silhouette with each letter's own pixels over it, which is how the master is built — so this one reproduces the logo rather than approximating it, and keeps the master's box and padding because an app icon's breathing room is part of the artwork. It is served at `/favicon.svg` ahead of the PNG, which stays as the second `<link>`: an SVG icon is the one asset type a browser may decline. **Tolerance 1.6 is the glyph's number and the sweep says it is the right one** — against the master, 1.2 buys 0.04/255 for 8 more vertices and 0.8 buys 0.5 for 505, because those vertices trace the render's antialias wobble rather than the art.

**It is themed, because the sidebar is not a dark rail.** `.sidebar` is `--bg-surface`, which the light palette takes to 99% lightness, so the wordmark sits on near-white there and on `#0F141A` in dark. The mark's own red is 3.7:1 on the light surface, under AA for 15px bold, so light darkens it to `oklch(56% 0.19 29)`. Verified in a real headless Firefox rather than computed on paper: **4.84:1 dark, 4.98:1 light.**
