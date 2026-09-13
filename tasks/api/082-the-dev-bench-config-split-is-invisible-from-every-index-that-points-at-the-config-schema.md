# 082 — `dev-bench-config.md` exists and nothing that points a reader at the config schema knows it

**State:** claimed by agent/api/082-dev-bench-config-index-pointers, 2026-09-13 14:26
**Source:** a supervisor sweep (leg 109, 2026-09-13) of the two verbatim splits that landed
yesterday alongside `study-designer/038`, hunting the same stale-citation class. `tasks/api/081`'s
split turned out to be clean on citations — 24 hits examined across all nine repos, every one naming
content that stayed in `config.md` — but the sweep found this instead, which is the opposite defect:
not a citation pointing at the wrong file, but **a file nothing points at.**
**Scope:** api
**Hardware:** none — four prose pointers and a fragment.
**Owner:** no

## What

`tasks/api/081` moved `config.md`'s whole `[dev_bench]` section verbatim into
`embarch-api/interfaces/dev-bench-config.md` on 2026-09-13. The forward link was written
(`interfaces/config.md:64` points at the new file), and the new file links back. **Every other
pointer in the suite still names `interfaces/config.md` alone**, so a reader arriving from any index
is told the config schema lives in one file, follows it, and finds a `[dev_bench]` section that is
a one-line referral:

- `embarch-api/spec.md:5` — `Config: [interfaces/config.md](interfaces/config.md).`
- `embarch-api/decisions.md:5` — `Config: [interfaces/config.md](interfaces/config.md).`
- `embarch-api/interfaces/tools-dev-bench.md` — describes all six dev-bench tools **entirely in
  terms of `[dev_bench]`'s fields** (`source_path`, chip, format, offset, probe serial) and links
  **no** config doc at all. It was never stale; it is now the single most obvious place a
  `dev-bench-config.md` link belongs, because it is the page whose whole subject is the tools those
  fields configure.

There is a fourth, and it is **not yours**: `embarch.md:115` lists this sub-project's interface files
and names three of the four. `embarch.md` is a shared suite-level doc — `never` for a worker in
[protocol.md](../../embarch-fleet/protocol.md) §3's table. **Drop a `status.d/` fragment** naming the
target doc and the fact that changed, per [status.d/README.md](../../status.d/README.md), and the
supervisor folds it when this unit lands. Do not edit `embarch.md`.

## Why now

A verbatim split is the one move `check-links.py` and `check-decision-refs.py` cannot see
(`tasks/doc/044`) — and this is the second face of that blindness. The first face is a citation that
still resolves to a file no longer holding what it cited; **this is an index that still resolves and
is now merely incomplete.** Both are green to every gate, both are invisible until a reader follows
one, and the cost is the same: a reader concludes the thing is not documented. The `[dev_bench]`
schema is the configuration a newcomer is most likely to get wrong — `dev-bench-config.md` opens by
saying **none of the five board-identifying fields is defaulted** and a missing one is a startup
error — so the page being unreachable from `spec.md`, `decisions.md` and the dev-bench tools page at
once is not a cosmetic gap.

## Done when

- [ ] `spec.md`'s and `decisions.md`'s `Config:` pointers name both files, in whatever form matches
      the surrounding line's existing convention — do not invent a new one, and do not restate what
      either file contains; a pointer is a pointer.
- [ ] `interfaces/tools-dev-bench.md` links the config doc its whole table depends on.
- [ ] A `status.d/` fragment filed for `embarch.md`'s interface list, naming the file and the line.
- [ ] `check-links.py` (inside `check-docs.py`) green — every link you add resolves.
- [ ] `changelog.d/` fragment **only if** something reader-visible changed; say which way you judged
      it. Making a shipped doc reachable is arguably reader-visible and arguably bookkeeping. Your
      call, stated.

## Dispatch note (supervisor, leg 109)

**In reserve for `api`** (last 10% of cap, still writable): `embarch-api/decisions/surface.md`
11258/12288 B (1,030 B left), filed as the blocked `tasks/api/069`. Nothing else. Your edits are
four pointer lines in `spec.md`, `decisions.md` and `interfaces/tools-dev-bench.md`, none of which
is anywhere near its cap — but if your work pushes an `api` doc into reserve or leaves one there
that nothing has filed, file `tasks/api/<NNN>-compact-api.md` in the same commit
(`tasks/README.md` has the shape). Recording the debt, not paying it.

**This is a pure code-free unit** — an `api` doc-only change with an empty code branch, which is
expected and correct. Push both branches anyway; the doc branch is the one that carries the work.
Run the `cargo` gate in the code worktree regardless, so a green is on the record.

**The `status.d/` fragment is a `Done when` item, not a nicety.** It is the only route a worker has
into a shared suite-level doc, and a unit that lands without it leaves `embarch.md` naming three of
four interface files with nothing recording why.

## Not in scope

- **Any change to `dev-bench-config.md`'s or `config.md`'s content.** The split was verbatim and it
  is correct; this task is about what points at them.
- `tasks/api/071`, the compaction task whose premise the split spent. The supervisor is closing it
  in this unit's fold — `config.md` is now 8,978/12,288 B (73.1%), out of reserve — so do not touch
  it, and do not file a replacement.
- The three size figures elsewhere in `tasks/` that the split made stale
  (`tasks/api/080:5` and two `umbrella` ones). They are records of what a closed unit measured at the
  time, not live claims, and rewriting a completed task's retrospective is how a ledger stops being
  evidence.
