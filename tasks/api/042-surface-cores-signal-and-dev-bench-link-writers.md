# 042 — Two of the suite's declared facts are settable only from a binary the suite does not ship

**State:** claimed — leg 074, `agent/api/042-signal-and-link-writers`

**Supervisor's dispatch note, leg 074, 2026-09-10.**
**Reserve in `api` for this dispatch, and one of these is load-bearing for your unit:**
`decisions/tool-wrapping.md` 12,222/12,288 B (**66 B left**, filed against the blocked
`tasks/api/047`) — do not put a new decision there, it cannot hold one;
`interfaces/tools.md` 11,280/12,288 B (1,008 B left, filed against the blocked `tasks/api/053`) —
**this is the file your second `Done when` box sends you into**; `open.md` 4,141/5,120 B (979 B
left, filed, `tasks/api/060`); `decisions/core-link.md` 13,164/12,288 B and `decisions/zephyr.md`
14,269/12,288 B are both already **over** cap — do not add to either.
**`interfaces/tools.md` is in reserve and its compaction task is blocked on `In flux: yes`, so
compacting it is part of your unit** (`../../embarch-fleet/leg` rule; `DOC-COMPACTION.md` §2). You
are the actor making the flux — you are adding rows to it — so you are the only one who can
shorten it without writing a clean statement of something about to be wrong. `tasks/api/053` names
its own preferred move and its own unpark clause: **a verbatim mission split by section**
(Config/discovery, Build/flash, Dev bench, Topology, Studies-pointer — already natural seams). A
verbatim split restates nothing, so `In flux: yes` does not forbid it. **Carry `api/053`'s
`Must not delete:` list intact** — the `erase` defaults-false callout and its decision-41 pointer,
the `dev_bench_schema_version`-vs-envelope-`schema_version` collision note under `dev_bench_hello`,
and the one-table premise sentence in the header. If you pay the file, delete it from `api/053`'s
`Compacts:` line (delete, never `~~strike~~` in place — the size gate parses that line) and say so
in the body. If you decide a split is not safe, say why in `tasks/api/053` and leave the debt.
**A new decision goes in a file that can hold it.** Pick the topic file by argument and write the
argument down; `tool-wrapping.md` is the topically obvious home and it has 66 bytes.
**Scope discipline:** you own `embarch-api` and `embarch-doc/embarch-api/` only. The third
`Done when` box names three docs in *other* sub-projects — `embarch-ui/decisions/topology-tab.md`,
`embarch-topology/decisions/links.md`, `suite/studies-guide.md` — and you may not edit any of
them. That box is satisfied by a `status.d/api-*` fragment naming them and what is now false; the
supervisor consumes it at the fold.
**Source:** suite review pass 2026-09-06, dimension 3 (one philosophy). Code-confirmed across 41 subcommands and 23 tools.
**Scope:** api
**Hardware:** none. The client wrappers already exist and are round-trip tested; this is surfacing, not new behaviour.
**Owner:** no

## What

`embarch.md` §5: *"Every hardware-facing capability is reachable both by an agent and directly by
a human, converging on the same underlying modules — **never a privileged or special code path for
either.**"* Two capabilities exempt themselves.

Counted across the suite: `embarch-api` has 23 `#[tool]` functions (`src/tools.rs`) and 23 CLI
subcommands (`src/main.rs:91-371`); `embarch-core` has 11; `embarch-umbrella` 7. **None of the 41
subcommands and none of the 23 tools reaches `POST/GET/DELETE /signals` or
`POST /dev-bench/link`.** `embarch-core/interfaces.md:12` names them as one class — *"the three
enrollment-file writers (`/dev-bench/link`, `POST /signals`, `DELETE /signals/{name}`)"* — and no
front end treats them as one.

**The wrappers already exist and nothing calls them.**
`embarch-api/crates/embarch-core-client/src/client.rs`: `declare_signal` (:1435), `list_signals`
(:1446), `remove_signal` (:1458), `list_serial_ports` (:1490), `list_enrolled` (:1121) — all
implemented, all round-trip tested, **zero front-end callers**.
`embarch-ui/decisions/topology-tab.md` decision 10 records why they were written there: *"The
shared Core client had no wrapper for any of them, so building this tab touched `embarch-api`'s
workspace as well."*

**The only surface is a GUI the suite does not release.**
`embarch-umbrella/.github/workflows/assemble-suite.yml:48-93` builds an archive containing
exactly `embarch`, `embarch-core`, `embarch-api`; `embarch-umbrella/decisions/release.md:48-51`
records that `embarch-ui` has no release workflow at all. So on a machine set up by
`embarch setup` there is no binary that can declare a signal — and
`embarch-dev-bench/spec.md:13` says the current bench requires
`link_port_interface = 2`, i.e. a `POST /dev-bench/link` nothing installed can send.

**The rejection on record does not cover this.** `embarch-topology/decisions/links.md` decision
18 rejected a signal-declaring CLI *in the topology crate*, on a reason entirely specific to that
binary — *"its CLI writes the store directly, and on the real deployment a plain-user run hits the
permission wall."* That does not transfer to `embarch-api`, which would `POST` to the elevated
service exactly as `embarch-ui` does. Two later docs generalised it into "no CLI at all"
(`embarch-ui/decisions/topology-tab.md` 10: *"there is deliberately no `embarch-topology` CLI
mirror, so this tab is the only human surface there is"*; `suite/studies-guide.md:114`) without
ever naming `embarch-api`. Meanwhile `embarch-api/decisions/tool-wrapping.md` decision 34 states this
repo's own rule and honoured it for the fourth writer: *"`enroll_probe`, wrapping Core's
enrollment endpoint. **The two-layer wrapping every other Core capability gets.**"*

Candidate direction: make it hold that every Core route in the enrollment / declared-fact class is
reachable from a binary `embarch setup` installs — MCP tool and CLI subcommand, per this repo's
own parity rule. The `list_serial_ports` wrapper is worth surfacing in the same pass; it is what
makes a declared signal's port findable at all.

## Why now

An agent cannot complete step 1 of using `embarch-outpost`, cannot diagnose the `400` a study gets
for naming an undeclared signal, and cannot even *read* what is declared. `embarch-ui` decision
10 already records the cost of the UI being the sole surface: *"The only human surface for
retracting or moving a wire had no working way in, and no Rust test could see it"* — a stray quote
in the markup, found only by headless Firefox. Every existing check is blind: `check-ownership.py`
is per-repo, `tasks/api/034`'s planned parity test compares MCP against CLI *within* this repo and
can never see a Core route neither reaches, and no gate reads Core's router against this repo's
surface.

## Done when

- [ ] `POST /signals`, `GET /signals`, `DELETE /signals/{name}` and `POST /dev-bench/link` are each
      reachable from both `embarch-api` front ends, or the reason one is not is written in
      `embarch-api`'s own decisions naming this repo.
- [ ] `embarch-api/interfaces/tools.md` lists whatever was added.
- [ ] `status.d/api-*` fragment for the three docs whose "only human surface" premise this makes
      false (`embarch-ui/decisions/topology-tab.md`, `embarch-topology/decisions/links.md`,
      `suite/studies-guide.md:114`).
- [ ] Gate green; `changelog.d/api-*` fragment.

**Adjacent, not the same:** `tasks/api/036` surfaces one read-only route (`GET /dev-bench/hello`).
This is the *write* surface for a class Core's own docs name as a class. If both are worked, they
should share the parity test.
