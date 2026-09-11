# 019 — The studies guide makes the UI a mandatory step, and nothing in the suite says how to obtain it, start it, or reach it

**State:** open — announced in #embarch-fleet by leg 082, `ts 1789114940.893289`, 2026-09-11, for the
**cheap half only** (README, guide paragraph, the five `EMBARCH_UI_*` variables written down), with
shipping the UI in the release archive recorded as a decision with a trigger rather than done. The
30-minute window under `../../embarch-fleet/ops.md` §4 runs from that message. **If leg 082 ends
before it closes, the next leg completes this window rather than restarting it** — read the thread
with `scripts/fleet-read.py --thread 1789114940.893289` and, if nothing objected and 30 minutes have
passed, run it. A reply saying "ship it" widens the unit to the expensive half.
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
