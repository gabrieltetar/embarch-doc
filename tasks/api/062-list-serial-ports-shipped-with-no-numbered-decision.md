# 062 — `list_serial_ports` shipped with no numbered decision, and the file it belongs in is 66 B from its cap

**State:** open
**Source:** `embarch-api/open.md` — *"`list_serial_ports`/`list-serial-ports` (task `041`) shipped
with no numbered decision, under that leg's burndown rule against new numbers"*
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`tasks/api/041` shipped the `list_serial_ports` MCP tool and its `list-serial-ports` CLI twin
during a burndown leg, whose standing rule forbade authoring a new numbered decision. The fleet is
not in burndown now, and `embarch-api/open.md` names exactly three things that decision owes:

1. **The no-parameter `GET /serial-ports` pair** — why the tool and the subcommand both take no
   arguments, and what that implies for a caller.
2. **Why `serial_log` has no automatic fallback onto it.** The reason is already written down in
   the `open.md` bullet and is a good one: several ports can enumerate, and only a human or the
   calling agent knows which is the DUT's console. An automatic fallback would pick a port on the
   caller's behalf and make a hardware inference the suite does not permit. Write it as a decision
   rather than as prose in an `open.md` bullet.
3. **The correction to `interfaces/tools-build-flash.md`'s stale `GET /dev-bench/port` claim** —
   moved there from `tools.md` on 2026-09-10 by `tasks/api/053`. Check whether that claim is still
   stale before correcting it; `053` may already have fixed it.

`open.md` also carries one thing that is explicitly **not this crate's to fix** and must survive
into whatever replaces the bullet: **`embarch init` never writes `serial_port` at all** —
`embarch-umbrella` decision 17's minimal discovery schema does not include it, so every config
reaches this surface without one. Do not fix that here and do not delete it; if the bullet is
rewritten, that half stays open and keeps naming `embarch-umbrella`.

## The file this belongs in is full, and that is part of the task

`open.md` says to file it in `decisions/tool-wrapping.md` *"once out of reserve (`tasks/api/047`),
or its successor"*. That file is at **12222/12288 B — 66 bytes left** and `tasks/api/047` is
**parked**. Sixty-six bytes is not a decision.

Per `DOC-COMPACTION.md` §2 and `DOC-BUDGET.md`'s split-first rule, you have two honest moves and
**a split is the default**:

- **Split** `decisions/tool-wrapping.md` by topic, verbatim, and write the new decision into
  whichever half it belongs to. `embarch-umbrella` decision 22's move into `bind.md` and
  `outpost/017`'s split of `decisions/testing.md` are both precedents; a verbatim split restates
  nothing, so a parked compaction task does not forbid one.
- **Or compact `tool-wrapping.md` as part of this unit**, carrying `tasks/api/047`'s
  `Must not delete:` list and closing only that file's item on it — you are the actor making the
  flux, so you are the one who can shorten what you are rewriting.

Say which you did and why in the commit message. **Do not put the decision in whichever `api`
decisions file happens to have room** — that exact failure is recorded in `embarch-api/open.md`'s
last bullet (leg 015, 96 B left) and is the reason this paragraph exists.

**Other `api` files in reserve:** `embarch-api/open.md` 4124/5120 B (996 B left, `tasks/api/060`,
parked), `decisions/core-link.md` 13164/12288 B (**over cap**, `tasks/api/061`, parked),
`decisions/zephyr.md` 14269/12288 B (**over cap**, `tasks/api/057`, parked). Do not grow any of
those three.

## Why now

The only thing that stopped this decision being written was a mode that is off. An owed decision
that lives in an `open.md` bullet is one a later reader re-derives from scratch, and this one's
substance — why a port list is never chosen automatically — is a safety property, not a
convenience.

## Done when

- [ ] A numbered `embarch-api` decision covers all three owed points, in a file that is not over
      cap after it lands.
- [ ] `embarch-api/open.md`'s `list_serial_ports` bullet is replaced by a pointer to it, keeping
      the `embarch init` / `serial_port` half open and still attributed to `embarch-umbrella`.
- [ ] `interfaces/tools-build-flash.md`'s `GET /dev-bench/port` claim is checked and corrected if
      still stale — or the task says plainly that `053` already fixed it.
- [ ] If you split or compacted `decisions/tool-wrapping.md`, `tasks/api/047` reflects it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) and a `changelog.d/` fragment dropped.
