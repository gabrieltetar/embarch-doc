# 019 — The studies guide makes the UI a mandatory step, and nothing in the suite says how to obtain it, start it, or reach it

**State:** claimed (leg 082) — announced in #embarch-fleet at 02:22:20 MDT, `ts 1789114940.893289`,
for the **cheap half only**; **window closed 02:52:20 with no objection**, so it runs.

## Reconciliation, 2026-09-11 — three of this task's premises are stale and one is newly false

Read this before the "What" section below, which was written on 2026-09-06 and has been overtaken:

- **`embarch-ui/README.md` exists** (6,917 B) and already covers how to build it
  (`cargo run --release`), the URL, the six tabs, the config file, and the VS Code launcher. The
  task says it does not exist. **That half is done and is not this unit's work.**
- **The signal CLI exists.** `studies-guide.md` §4 no longer says *"both done in the UI — there is
  deliberately no CLI for either"*; since `embarch-api` decision 67 it says "in the UI **or** from a
  terminal" and names `declare-signal`, `list-signals`, `remove-signal`, `dev-bench-link`. The
  quoted premise is gone from the source doc.
- **Port 4890 is no longer absent from the corpus** — `tasks/suite/009`, this leg's third unit, put
  it in `embarch.md` §4.
- **"Five `EMBARCH_UI_*` variables" is wrong in both directions.** There are **four** in the source
  (`HOST`, `PORT`, `CONFIG`, `STATE`), and the README's table documents **three** while asserting
  *"the whole surface is three environment variables"* — so the README is not merely incomplete, it
  makes a false completeness claim. `EMBARCH_UI_STATE` overrides the recent-projects path
  (`<per-user data dir>/embarch/ui/recent-projects.json`).

**What actually survived, and what this unit did:** the newcomer gap is real but narrower than
filed. `suite/user-guide.md` mentions the UI **zero times** and its §3 says the archive contains
*"all three binaries"*, while `suite/studies-guide.md` §4 still requires the **Topology**, **Study
Designer** and **Trace** tabs — and the release archive genuinely does not contain `embarch-ui`
(`assemble-suite.yml` pulls `embarch-core`, `embarch-api`, `embarch-umbrella` and nothing else).
So a reader who has only what `embarch setup` installed cannot reach the suite's flagship
capability and is told nothing about why.
**Source:** suite review pass 2026-09-06, dimensions 7 and 1. Code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`suite/studies-guide.md:114` — *"Two things have to be true first, **both done in the UI** — there
is deliberately no CLI for either."* Declaring a signal and adding a trace tap are UI-only, and
`embarch.md:27` says signal routing in the Topology tab is *"**the only human surface for it**"*.
A study whose tap names an undeclared signal *"is refused before it runs"* (`studies-guide.md:123`).

So the UI is the only door to a shipped feature, and:

- `suite/user-guide.md` mentions the UI **zero times** — `grep -in "\bUI\b\|topology tab\|study
  designer"` returns no hits — and §3 says the archive contains *"all three binaries."*
- `embarch-umbrella/decisions/release.md:48-50` records that `embarch-ui` has **no release
  workflow at all**, and `assemble-suite.yml:48-93` builds an archive of exactly `embarch`,
  `embarch-core`, `embarch-api`. **The UI is not in it.**
- `embarch-ui/` has **no `README.md`.**
- `embarch-umbrella` never mentions the UI: no `embarch ui` command in its command surface, none
  of `doctor`'s 18 checks, and `grep -rn "embarch-ui\|4890" embarch-umbrella/src/` returns nothing.
- Port **4890** (`embarch-ui/src/main.rs:40-41`: `BIND_ADDR = "127.0.0.1"`, `BIND_PORT = 4890`)
  appears **nowhere in the 3 MB doc corpus**, along with `EMBARCH_UI_CONFIG`, `EMBARCH_UI_HOST`,
  `EMBARCH_UI_PORT` and `EMBARCH_UI_STATE`.

The newcomer is reasonable here because everything else on the path is installed for them:
`setup` copies three binaries and edits `PATH`, `init` registers the MCP server. Nothing signals
that the fourth surface is a `cargo build` in a sibling repo.

Candidate direction: the property is that a reader of `studies-guide.md` §4 can get from "I have
the release archive" to a running Topology tab without reading a sub-project spec. The cheap end is
a `embarch-ui/README.md` plus a paragraph in the guide naming the build command and
`http://127.0.0.1:4890`; the real end is shipping it in the suite archive and giving umbrella a
way to start it. **That fork is worth putting to the owner before spending the unit on the wrong
half.**

## Why now

This blocks the suite's flagship capability — an outpost trace — for anyone who has only what
`embarch setup` installed. And it is invisible to every other dimension: each module is internally
consistent, the UI genuinely works, and there is no A-versus-B difference to report; the gap is a
uniform absence. It is also half of why the
`api-surface-cores-signal-and-dev-bench-link-writers` drop matters: the "only human surface"
premise was derived from a rejection that never named `embarch-api`, and the surface it names is
unshipped.

## Done when

- [ ] `embarch-ui` has a README stating how to build it, how to start it, and the URL it serves.
- [ ] `suite/studies-guide.md` §4 and `suite/user-guide.md` §3 agree on how many binaries a
      newcomer has and where the UI comes from.
- [ ] The UI's five `EMBARCH_UI_*` environment variables are documented somewhere a reader will
      find them, or the reason they are undocumented is recorded.
- [ ] Gate green.

**Adjacent:** the `suite-four-repos-cannot-be-built-from-a-fresh-clone` drop in this batch also
wants an `embarch-ui/README.md`. Let this one create it.
