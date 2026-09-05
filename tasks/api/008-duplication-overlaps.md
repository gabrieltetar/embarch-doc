# 008 — `embarch-api` holds fifteen claims in two files each

**State:** claimed by agent/api/008-duplication-overlaps, 2026-09-04 21:15
**Source:** tasks/api/007-compact-docs.md, closed 2026-09-04 when its reserve debt was paid — this is the half of it that was never about size
**Scope:** api
**Hardware:** none
**In reserve for this sub-project:** none. `open.md` (89.1%) and
`decisions/surface.md` (88.9%) both came **out** of reserve under `api/005`, and
`spec.md` came out under the 2026-09-04 compaction pass. This task has room.

## What

`scripts/check-duplication.py embarch-api` reports **15 overlaps of 12+ words**.
The two worth naming, because they are the largest and the most load-bearing:

- A **37-word run** between `interfaces/modules.md` and `spec.md` §5 — the
  512 MiB runtime-thread-stack paragraph, kept in both when the module map was
  split out of `spec.md`.
- **Four** between `decisions/surface.md` and `interfaces/tools.md`, all about
  `erase`.

**Every one of these is a `DOC-PROTOCOL.md` §3 question — which file owns the
claim — and not a `DOC-COMPACTION.md` §9 hot/cold one.** That distinction is why
this is filed separately rather than folded into a compaction pass: a §9 pass
asks whether a sentence still earns its place, and answering it about a sentence
that exists twice will delete the wrong copy about half the time.

## Why now

Not urgent, and deliberately not a size task. It was discovered while `api/007`
was looking for bytes, and it survived that task's closure because the bytes
turned out not to be needed — `api/005` freed both files by closing an `open.md`
bullet and moving decision 18 out of `surface.md`. The finding is real
independently of whether anything is in reserve, and `check-duplication.py` is
advisory and in nobody's gate, so nothing else will re-surface it.

`api/007`'s original `Must not delete:` still applies to any pass over these
files and is carried here verbatim rather than lost:

> `open.md`'s *do not derive a kind from the HTTP status* clause and its
> ordering (Core emits codes, the shared client carries one typed, this crate
> passes it on) — decision 50 exists because that shortcut was proposed and it
> is coarser than `embarch-core` decision 12's enum; decision 52's rejection of
> a `status --json` field, whose reason is that a diagnostic's input has to
> survive a broken machine.

## Done when

- [ ] Each of the 15 overlaps is either resolved by assigning the claim to one
      file per `DOC-PROTOCOL.md` §3, or named here as a deliberate restatement
      with the reason. **Both are real answers**; a pointer in the losing file
      is usually better than silence where the claim used to be.
- [ ] `check-duplication.py embarch-api` reports what you intended, and the
      commit message says which overlaps were kept on purpose.
- [ ] No file pushed into reserve; if one is, file the debt in the same commit
      per `tasks/README.md` § "Compaction tasks".
- [ ] Gate green, `changelog.d/api-*` fragment dropped.
