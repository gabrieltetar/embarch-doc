# 017 — `soc_chip_overrides` is decided and never built: build it or retire decision 13

**State:** open
**Source:** `embarch-api/open.md` — "`soc_chip_overrides` is decided and unbuilt", and
`embarch-api/decisions/zephyr.md` 13's own amendment. Found 2026-09-05 by `api/016` while
closing decisions 20/21's loose ends: `open.md` listed the field among those "equally
unhonourable on a `static` project", and it turned out to be unhonourable on **both** kinds.
**Scope:** api
**Hardware:** none to decide; **verify-only** if built (see below)
**Owner:** no

## What

`embarch-api` decision 13 and `embarch-api/interfaces/config.md` describe a per-project
`soc_chip_overrides` table: an `{ soc, chip }` list consulted **before** Core's
`POST /resolve-chip`, so an operator who resolved an unmapped SoC by hand with
`probe-rs chip list` has somewhere to write the answer and a hit skips the HTTP call.

**None of it exists.** `ProjectConfig` has no such field, `resolve.rs` calls
`core.resolve_chip(&target.soc)` unconditionally, and the crate sets no
`deny_unknown_fields`, so a config declaring the key is parsed and dropped in silence on a
`zephyr-west` project as much as on a `static` one. This is
`embarch-decision-reversals.md` shape 1 — config the interface doc states as truth and
nothing implements — the same shape decision 20 was built to close for `default_target`.

**Resolve it one way or the other.** Both are legitimate:

- **Build it.** Small: one `Vec<SocChipOverride>` on `ProjectConfig`, consulted in
  `resolve.rs` before `resolve_chip`, plus the load-time refusal on a `static` project that
  decision 20 now applies to the whole zephyr-west-only class (so it joins the five, and
  `interfaces/config.md`'s "five fields" sentence becomes six). The reason to: the dead end
  decision 13 names is real — Core's resolver 404s and the operator has nowhere to put the
  answer they already have.
- **Retire decision 13** per `DOC-CONVENTIONS.md`'s tombstone shape, and say plainly that a
  404 naming the unmapped SoC is where an unmapped SoC stops — the fix belongs in Core's
  chip table, not in a per-project override that makes one machine's config disagree with
  every other machine's. Then delete the `soc_chip_overrides` row from
  `interfaces/config.md` and the `open.md` bullet with it.

**Do not close this by quietly deleting the doc text**, and do not close it by building the
field without saying why the "fix it in Core" alternative was rejected. The entry has to
carry the argument against whichever half is not taken.

## Why now

`embarch-api/open.md` states it, and it is the one remaining half of the loose-ends bullet
`api/016` closed. It is cheap either way and it removes a doc that lies.

**What would sharpen the choice, and is not required to make it:** a real SoC Core has no
mapping for. Nobody has hit one recently, which is itself evidence for the retire half —
an escape hatch nothing has needed in three months is a hatch, not a door.

## Done when

- [ ] Decision 13 either loses its "**decided, never built**" amendment because it is now
      built, or becomes a tombstone naming what replaced it. Amend in place; do not append
      a correction under a body that then contradicts it.
- [ ] `embarch-api/interfaces/config.md`'s `soc_chip_overrides` row states the built
      behaviour, or is gone.
- [ ] If built: a test that a configured override short-circuits `/resolve-chip` (no HTTP
      call made), one that a miss still calls it, and one that a `static` project setting it
      fails at load with the rest of the class (decision 20).
- [ ] `embarch-api/open.md`'s bullet is deleted.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/api-*` fragment
      dropped.
