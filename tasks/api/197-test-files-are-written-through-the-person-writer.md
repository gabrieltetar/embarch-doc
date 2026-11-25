# 197 — Test files are written through the person writer

**State:** done — hil_repo writes through person_writer kinds; 132 and 134 agree
**Source:** the reviewer of `api/196` (embarch-api `eb2f64d`, doc `44c88c7d`)
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Decision 132 (`decisions/person-mirror.md`) makes `person_writer` the one
writer into the person's `embarch/`: "any later writer into the person's
`embarch/` goes through this one", and "a struck kind is one enum arm". Its
guarantees are no link followed (`O_NOFOLLOW`), a hard-linked target refused,
and a write by temp file and rename. `api/196` added `src/hil_repo.rs`, which
writes `embarch/tests/suites/`, `embarch/tests/plans/` and
`embarch/topologies/` with its own writer: a `symlink_metadata` check before
the write, and none of 132's other guarantees. Decision 134
(`decisions/test-plans.md`) says 132's kinds (`tests/<name>.test.toml`)
disagree with the pinned layout, and leaves 132 standing, so the two now
contradict each other.

When this is done, every file `hil_repo` writes goes through `person_writer`,
with new kinds for the layout `api/196` pinned (a suite's `suite.json`, a test's
folder with its test and study files, a plan, a saved bench copied into
`embarch/topologies/`), and `hil_repo`'s own writer is gone. Retire or rewrite
132's `tests/<name>.test.toml` kind if nothing writes it. Decision 134's
sentence about the second writer is amended to say the writes go through 132,
and 132 gains the new kinds.

Keep the layout exactly as `api/196` wrote it: `embarch-ui` (`ui/120`) reads
it.

## Where to look

- `src/hil_repo.rs`, `src/person_writer.rs` (or wherever decision 132's
  writer lives)
- `embarch-doc/embarch-api/decisions/person-mirror.md` (132),
  `decisions/test-plans.md` (134), `interfaces/tools-tests.md`

## Where the doc goes

Amend 132 and 134. **Do not grow these decisions, which are at or over their
limit:** `ledger.md` 98 (15 B left), `lease.md` 90 (504 B over),
`bench-exchange.md` 89, `failure-reporting.md` 67. If your work pushes a file
into reserve, file `tasks/api/<NNN>-compact-api.md` in the same commit per
`tasks/README.md`.

## Done when

- [x] `hil_repo` has no file write of its own; every write is a
      `person_writer` kind.
- [x] A test plants a symbolic link at a suite folder and at a plan path, and
      each write is refused; a hard-linked target is refused.
- [x] `api/196`'s tests pass unchanged in what they assert.
- [x] Decisions 132 and 134 agree.
- [x] Gate green.
