# 039 — `embarch-ui/Cargo.toml` still cites a `design.md` that does not exist

**State:** done — leg 098, 2026-09-12.
**Doc-size reserve for `ui`:** nothing in reserve; no compaction debt expected from this unit.
**Source:** `ui/037`'s worker, found while re-grepping `embarch-ui` for stale-doc source-comment
citations (2026-09-12).
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`ui/033` repointed every `embarch-ui` source comment citing `embarch-doc/embarch-ui/design.md` (a
file that does not exist) at real decision numbers, but missed `Cargo.toml`'s own comments:

- `Cargo.toml:6` — the package `description` field itself: `"...embarch-doc/embarch-ui/design.md
  is the source of truth."`
- `Cargo.toml:14` — `# list, Study-building (embarch-ui/design.md §3 decision 5).`
- `Cargo.toml:19` — `# with embarch-api rather than duplicated (embarch-ui/design.md §3 decision`
  (continues onto line 20, which `ui/037` already fixed by dropping a co-located `milestone-1.md`
  clause — the `design.md §3 decision 5` part of that same comment is untouched and still stale)

`Cargo.toml:27` also cites `(embarch-api/design.md §11)` — a **cross-repo** citation into
`embarch-api`, not `embarch-ui`'s own `design.md`; whether `embarch-api/design.md` exists is outside
`ui`'s ownership and needs checking in that repo, not this one.

## Why now

Same defect class `ui/033` and `ui/034` already fixed everywhere else in this repo:
`check-decision-refs.py` only resolves decision numbers in `*.md` under the repo root, so a stale
citation living in a `Cargo.toml` comment (not a doc file) is invisible to any gate.

## Done when

- [x] `Cargo.toml:6`'s description no longer claims a nonexistent `design.md` is "the source of
      truth" — either repoint at `spec.md`/`decisions.md` (whichever is accurate today) or drop the
      clause. Repointed at `spec.md` (current truth) and `decisions.md` (why).
- [x] `Cargo.toml:14` and `Cargo.toml:19-20` cite the real decision (`decision 5`, per `ui/033`'s
      resolution for identical comments elsewhere) without the dead `design.md §3` prefix.
- [x] `Cargo.toml:27`'s `embarch-api/design.md §11` checked against `embarch-api`'s own repo — fixed
      here only if it's confirmed `ui`'s file to touch (it's a comment in `embarch-ui`'s own
      `Cargo.toml`, but the citation crosses repos so read `embarch-api/design.md` or whatever
      replaced it before repointing). `embarch-api/design.md` does not exist either (`embarch-api`
      also uses `decisions.md`/`decisions/`, no per-repo compaction into one file). Its "decision 11"
      turned out to be the wrong number too — `embarch-api/decisions/core-link.md`'s decision 11 is
      `base_url = "auto"` resolution, unrelated. The rule this comment actually describes ("this
      crate never links hardware", mirrored client wrappers instead of the real probe-rs-gated
      types) is `embarch-api/decisions/client-crate.md`'s decisions 37/38. Repointed the comment at
      `` `embarch-api` decisions 37/38 `` (bare, no file path — matches this repo's own convention,
      e.g. `src/main.rs`'s `` `embarch-topology` decision 5 ``).
- [x] `grep -rn "design.md" embarch-ui/` (all file types, not just `*.md`) comes back with only
      legitimate hits, if any remain. Zero hits after this unit.
