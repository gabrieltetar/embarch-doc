# 033 — Settle check 17's two Fail arms against a real narrow-bound Core

**State:** open
**Source:** moved verbatim in substance out of `embarch-umbrella/open.md` by the supervisor at
`umbrella/027`'s fold, 2026-09-06 — it is an experiment protocol, and `tasks/` is where those live.
`open.md` keeps the one-line question and points here.
**Scope:** umbrella
**Hardware:** **bench** — supervisor's own hands, and it needs a service reinstall, so read
"Before you start" first
**Owner:** **required** — see below. Do not dispatch, and do not run it as an ordinary bench unit.

## The question

Check 17 compares Core's bind address against what this topology needs
([decision 22](../../embarch-umbrella/decisions/bind.md)). **Its two Fail arms have never met a
real narrow-bound Core.** This bench registers `--bind 0.0.0.0`, and every live run has been the
Pass. **The loopback hit discriminates nothing** — a run that sees only it settles neither arm.

## The protocol, each arm its own half

One Core installed `--bind 127.0.0.1` on a `wsl-host` machine settles both:

1. **Stopped:** `bound-narrow` must Fail where a wide registration does not.
2. **Running:** `bind-too-narrow` must Fail where a wide one Passes `bind-matches-registered`.
3. **Same machine, third step:** does `embarch-core install --bind 0.0.0.0` **rewrite** an
   already-registered narrow service, or refuse it? It has never been run against one, **and it is
   the assumption under *both* of check 17's fix lines** — if it errors, the diagnosis is right and
   the whole remedy is wrong.

## Why `Owner: required`

Every step reinstalls or re-registers the Windows service that the entire fleet, the MCP surface and
`embarch-ui` reach at `172.22.128.1:4884`. A supervisor's bench grant is *exercising EmbArch against
real hardware* — flash and study over an existing artifact — not re-registering the machine's Core
service, and step 3 is explicitly an experiment about whether a reinstall does the right thing.
A failed step 3 could leave the machine with a narrow-bound or unregistered Core and the fleet with
no Core at all, unattended.

## Done when

- [ ] All three steps run, and each records **what was observed**, not just the verdict — the
      registered `--bind` string, the address `/status` answered on, and the `code` each arm emitted.
- [ ] `open.md`'s check-17 bullet is closed or rewritten to whatever is left unknown.
- [ ] Step 3's answer lands in [decision 22](../../embarch-umbrella/decisions/bind.md), because both
      fix lines depend on it.
- [ ] Core is left registered `--bind 0.0.0.0` and answering, verified.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
