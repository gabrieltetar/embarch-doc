# embarch: Zephyr relationship

**Status:** active, 2026-08-15. Replaces the 3-line placeholder, closing item 59 of that day's design-improvement review (`.claude/design-improvements-2026-08-15.md`, local working notes — not committed): Zephyr is load-bearing across three design docs (`embarch-api/decisions.md` decision 12, `embarch-dev-bench/decisions.md`, `embarch-umbrella/design.md` §3 decision 17), and the board-qualifier grammar, revision semantics, snippets, and sysbuild behavior those docs assume were scattered across all three with no single home. This doc doesn't restate any of their decisions — per `DOC-PROTOCOL.md` §5, it's the concept-level reference those decisions link back to.

## 1. What this doc is for

`embarch-api`'s `discovery = "zephyr-west"` support (§2 below) and `embarch-dev-bench`'s own build (§3) both depend on understanding Zephyr's own conventions well enough to assemble a correct `west build` invocation and to tell a *real*, buildable target apart from one `board.yml` merely declares. This is where that conceptual grounding lives, so a design decision elsewhere in this suite can say "per the board-qualifier grammar" and mean something specific rather than re-explaining Zephyr from scratch each time.

## 2. Board-qualifier grammar

Zephyr identifies a buildable target with a qualifier string, passed to `west build -b`:

```
<board>@<revision>/<soc>/<cpucluster>/<variant>
```

- **`<board>`** — the board's own name (e.g. `roadrunner`, `nrf54l15dk`).
- **`@<revision>`** — optional. Omitted means the board's declared *default* revision, which is implicitly backed by the board's un-suffixed base `.dts`/`.overlay`/`.defconfig` files — no revision-specific file needs to exist for the default to work.
- **`/<soc>`** — required whenever a board's `board.yml` declares more than one SoC (common on multi-die or product-family boards); omittable when there's only one.
- **`/<cpucluster>`** — required for a multi-core SoC (e.g. `cpuapp`/`cpunet` on some Nordic parts); omitted for a single-core SoC.
- **`/<variant>`** — optional. A named product variant (e.g. `os`, `max_3led`) when `board.yml` declares one; a board with no declared variants, or a variant-less build of a board that *does* declare named variants (§2.2), omits this entirely.

`embarch-api/decisions.md` decision 12 assembles this string per call, from a live scan of `board.yml` and the app's own `CMakeLists.txt` — never stored, never hand-maintained, per that decision's core rationale (a repo's buildable surface is a property of its current files, not something safe to snapshot once).

### 2.1 Revisions: declared vs. real

Zephyr's board-revision mechanism auto-applies a revision-suffixed overlay/defconfig file — `<board>_<soc>_<cpucluster>[_<variant>]_<revision>.{overlay,defconfig}` — **if one exists on disk**, and silently falls through to the board's un-revisioned base files if it doesn't. `board.yml` can *declare* a revision without a real file backing it, and Zephyr won't error — it just quietly builds without the revision-specific override applied, which is a wrong-shape build, not a failed one. This is the exact gap `embarch-api/decisions.md` decision 12 exists to close for a `zephyr-west` project: a target is only ever reported as real if the default revision (backed by base files) or a matching revision-suffixed file actually exists, checked mechanically rather than trusted from `board.yml` alone.

A board can also opt out of this convention entirely (`board.yml`'s `revision: { format: custom }`), supplying its own `revision.cmake` with arbitrary logic — which can couple a specific variant to a specific revision (hard-error on any other combination) in a way the standard convention's file-existence check alone wouldn't catch. See [embarch-decision-reversals.md](embarch-decision-reversals.md) for the real bug this produced when first encountered.

### 2.2 Variants aren't mandatory just because they're declared

A SoC that declares named product variants (`os`, `max_3led`, `max_5led`, say) can *also* have a real, separately-buildable variant-less target for the same cpucluster — Zephyr's board-qualifier variant component is optional even when a board declares some. A scanner that only ever proposes declared variants can miss the variant-less build entirely, which is a real gap this suite hit against a real repo whose actual day-to-day build was exactly the variant-less form. See [embarch-decision-reversals.md](embarch-decision-reversals.md).

## 3. Snippets

A **snippet** (`west build -S <name>`) is a named, reusable devicetree-overlay/Kconfig-fragment bundle, discovered under `app/<app>/snippets/**/snippet.yml` (Zephyr's own scanner walks this recursively, not at one fixed depth — matched by `embarch-api`'s `available_snippets`, `embarch-api/decisions.md` decision 12). Snippets are **additive, not a narrowing axis**: choosing a snippet doesn't change which (board, soc, cpucluster, variant, revision, app) tuple exists, unlike every other qualifier component in §2 — it's an independent flag list layered on top of an already-resolved target. More than one snippet can be requested at once (`-S a -S b`).

## 4. Sysbuild

Recent Zephyr SDK releases (confirmed against NCS 3.4) wrap **every** application build in `sysbuild` regardless of whether one was explicitly requested — this is not opt-in behavior a project can avoid by not asking for it. The practical consequences:

- The build artifact lands under `build/<app>/zephyr/zephyr.hex` (or `.elf`/`.bin`/`.uf2`), **not** `build/zephyr/...` as a pre-sysbuild build would have produced.
- `build/domains.yaml` exists once sysbuild is active, naming each domain (image) in the build. A single-core, single-image application (this suite's dev-bench board, `embarch-dev-bench/decisions.md` decision 4) still has exactly one domain, named `app` — sysbuild's presence doesn't by itself imply a multi-image build to coordinate, only that the *mechanism* is active.
- A tool locating the build artifact (`embarch-api`'s `artifact_path` resolution, `embarch-umbrella`'s `init`) has to search for the real file rather than assume a fixed layout, since which of the two layouts applies depends on the SDK version in use, not on anything the project's own config declares.

## 5. Cross-references

- [embarch-api/decisions.md](embarch-api/decisions.md) decision 12 — the live target-discovery implementation that applies everything in this doc mechanically.
- [embarch-dev-bench/decisions.md](embarch-dev-bench/decisions.md) decision 4 — the sysbuild correction (§4 above) as it was actually found.
- [embarch-umbrella/design.md](embarch-umbrella/design.md) §3 decision 17 — `init`/`doctor`'s trimmed, detection-only application of this same grammar.
- [embarch-glossary.md](embarch-glossary.md) — one-line definitions of "board qualifier," "target," and "discovery kind."
- [embarch-decision-reversals.md](embarch-decision-reversals.md) — the real bugs §2.1/§2.2 above describe, as they were actually found.
