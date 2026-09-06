# 026 — `embarch-api/decisions/core-link.md` is 22 bytes from its cap

**State:** blocked
**Source:** `api/022` spent the reserve writing decision 55; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/core-link.md
**In flux:** yes — the event-stream half of this file (decisions 48, 49) has never
met a real `embarch-core`. `tasks/api/001-sse-client.md` is that run. Until it
happens, shortening 48/49 writes a clean statement of something a first live run
is expected to contradict, and throws away the fallback reasoning that run will
need to read. Unparked by `api/001` landing, either confirming those decisions or
replacing them.
**Must not delete:** decision 15's *failure signature* — the identical path
resolving from an interactive shell and failing with "the network name cannot be
found" from the service. It is a measurement, and it reads as an inference once
the A/B test is summarised away. Decision 36's **rejected** `Builder::thread_stack_size`
and the 64 MiB-insufficient/512 MiB-needed pair: both are empirical, and a
shortened form that keeps only "512 MiB" makes the number look chosen.
Decision 26's *correction* — that DUT-UART capture was never an intended use — is
the whole entry; the fallback chain it describes is the disposable half.
Decision 55's `default_headers` rejection, which is the second time that shortcut
has been proposed and rejected.

## What

`decisions/core-link.md` is **12,266 B against a 12,288 B cap** — 22 bytes. The
next `api` unit that writes this file cannot write anything into it.

**The move is a split, not a shortening, and the split is not blocked.** This
file already carries six unrelated missions: address resolution (11, 14, 17),
artifact transfer (15), the shared-client extraction (37, 38), the event stream
(48, 49), the per-machine logfile (43), `serial_log`'s port fallback (26), and
now the auth funnel (55). `api/023` did exactly this to `shape.md` — moved
entries **verbatim** into `decisions/tests.md` and updated the index — and a
verbatim move states nothing new, so `In flux: yes` does not forbid it. Splitting
the event stream (48, 49) out is the obvious cut: it is the flux, and it is the
half a live run will rewrite.

Actual compaction of the remaining entries waits for `api/001`.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md` §2).
This task is that filing.

`embarch-api`'s whole decision corpus is narrow — `zephyr.md` 11,056,
`interfaces/config.md` 11,008, `build.md` 10,934, `surface.md` 10,928, all a
paragraph short of the 11,059 B reserve line and therefore invisible to the
size check. [embarch-api/open.md](../../embarch-api/open.md) carries that as a
standing hazard, and leg 015 is what it is written from: with 96 bytes left, an
entry went into whichever file had room rather than the file whose topic it was.

## Done when

- [ ] `decisions/core-link.md` is clear of the 11,059 B reserve line.
- [ ] Whatever moved, moved **verbatim** unless `api/001` has landed; every
      `Must not delete:` item above is still readable at its new address.
- [ ] `decisions.md`'s index table names the new file, its decision numbers and
      both files' sizes, and `check-decision-refs.py` resolves every number.
- [ ] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *can `spec.md` alone answer what someone needs to
      work on reaching Core today?*
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
