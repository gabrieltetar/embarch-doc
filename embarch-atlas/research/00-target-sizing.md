# The target codebase, measured

**Status:** draft, 2026-09-22.

What `embarch-atlas` would actually have to index, measured on a real client
firmware west workspace rather than estimated. Every number here is
`[measured 2026-09-22]` on that tree at its then-current checkout. The point of
the exercise: the light-vs-heavy fork for this sub-project has to be argued with
real magnitudes, and "a firmware codebase is big" is not one.

**This note is generalized.** It keeps the numbers and drops the client's module,
driver and file names, because this repo is public; the full-fidelity version is
machine-local (see [README.md](README.md), "Client data").

## The headline

**The client-owned surface is small; the surface it depends on is not.** That
asymmetry, not raw volume, is the design problem.

| Layer | Files (`.c`/`.h`) | Lines |
|---|---:|---:|
| Application | 19 | 1,468 |
| Project libraries | 109 | 38,618 |
| Out-of-tree drivers | 114 | 59,981 |
| **Client-owned total** | **242** | **~100,067** |
| Whole repo, incl. vendored trees | 3,019 | ~1,275,635 |

100 K lines across 242 files is a tractable index by any measure — a single
machine, minutes not hours, and small enough that whole-file reads are viable for
a large fraction of queries. The 1.28 M-line figure includes vendored trees and is
a red herring for sizing the *owned* index; the genuine scale problem is the
Zephyr workspace underneath, which the repo does not own.

## Shape of the owned code

The project libraries are 31 modules. Their size is long-tailed: the largest is
~6.4 K lines, the top five sit between ~3.9 K and ~6.4 K, and most of the rest
are under 2 K — a vendored JSON library among them.

The out-of-tree drivers are ten, binding to external parts: two optical sensor
front-ends, an IMU and its auxiliary interface, a fuel gauge, a temperature
sensor, a battery abstraction, a power-enable switch and an interrupt-input
helper. **60% of the owned line count is driver code binding to physical
parts.** That is the single strongest argument that "hardware binding" is not a
nice-to-have capability for this codebase: it is where most of the code is.

## Conditional-compilation density

| Measure | Count |
|---|---:|
| `#if`/`#ifdef`/`#ifndef`/`#elif` in the repo's `.c`/`.h` | 556 |
| …of which reference a `CONFIG_` symbol | 333 |
| Distinct `CONFIG_*` symbols referenced in the owned code | 592 |
| `Kconfig*` files in the owned code and board definitions | 54 |
| `.dts`/`.dtsi`/`.overlay` in board definitions | 35 |
| `.conf` files in the application and boards | 20 |

**592 distinct `CONFIG_` symbols against 333 conditional directives.** The gap
matters: most `CONFIG_` references are not `#ifdef` guards at all — they are
values consumed in expressions (buffer sizes, priorities, timeouts, feature
parameters). A tool that only resolves `#ifdef` branches and ignores `CONFIG_`
*values* answers the smaller half of the question. Both halves need the same
input, so this is an argument about coverage, not cost.

35 devicetree/overlay files and 20 `.conf` files across a handful of boards is the
combinatorial space a "which build?" index has to pick a point in. It is small
enough to enumerate, which means indexing *several* concrete configurations is not
obviously out of reach — a fact worth holding before assuming a one-build-only
index.

## What this does not measure

- **Zephyr and the modules underneath** — the workspace also carries `zephyr/`,
  `nrfxlib/`, a bootloader and the HAL/module tree. Sizing that layer, and what the
  build tree already computes about it, belongs to the build-metadata note.
- **Anything post-build.** These are source-tree counts; what a `build/`
  directory hands you for free is a separate and more consequential question.
- **Semantics.** File and line counts say nothing about how many of those 242
  files an agent actually needs for a typical task — the number that would justify
  or sink this sub-project, and which nothing here measures.
