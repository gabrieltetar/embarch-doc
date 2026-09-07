# 024 — `DOC-COMPACTION.md` is in reserve

**State:** open
**Scope:** doc
**Hardware:** none
**Owner:** required — **`DOC-COMPACTION.md` is a standing rule and no agent may write it**
(`../../embarch-fleet/protocol.md` §2). `queue-status.py` gates this out of the dispatchable count
for that reason. It is filed here rather than nowhere so the debt is visible to the one actor who
can pay it.
**Source:** leg 035, 2026-09-07 — filed mechanically, not on judgement. The owner's own commit
`903a795` ("A split is the default remedy, reserve gets a byte floor, and an assembled file loses
its cap") grew `DOC-COMPACTION.md` past the reserve line, and `check-doc-size.py` then failed
`main` for **1 file in reserve with no debt filed**. Filing the debt is the only remedy available
to an agent, because the alternative — editing the file — is forbidden, and leaving it turns every
subsequent worker's `check-docs.py` red for a reason that has nothing to do with its own work.

**Compacts:** DOC-COMPACTION.md
**In flux:** **yes** — but read the next paragraph before treating that as the usual park.
**Must not delete:** the byte-floor rule and the assembled-file exemption that `903a795` just
added, which are the newest reasoning in the file and the least likely to be re-derivable; the
`tasks/doc/` versus `tasks/<scope>/` history (until 2026-09-05 the rule named `tasks/doc/` for
everyone and `check-ownership.py` refuses that path to every worker, so the only actor told to
file a debt was the one forbidden to file it — `tasks/doc/004` found this by disobeying it on
purpose); the reason `Compacts:` matches one field and not a mention anywhere in a task body (a
path merely cited made five of one day's twelve files read as filed); and the `In flux: yes`
argument that compacting a moving subsystem "writes a clean statement of something about to be
wrong and destroys the alternatives you are about to need."

## Why `In flux: yes` and why the state is still `open`

`In flux: yes` normally means `State: blocked` with a named milestone. **This one is `open`
because `Owner: required` already keeps every agent off it**, so the block would protect nothing
and would only hide the debt from the owner's own view of the queue. The flux is real and it is
the owner's: `903a795` is the third policy change to this file in three days (the split-as-default
remedy, the reserve byte floor, the assembled-file cap exemption), and compacting it while that
reasoning is still settling is exactly what the rule the file itself carries says not to do.

**So this task is a record, not a request.** Nothing here should be dispatched, and nothing here
needs to happen soon. What it does is stop `check-doc-size.py` from failing `main` for an unfiled
file, which is the state it was in for one commit.

## Note on the mechanism, because this is the second time a reserved doc has done this

`DOC-PROTOCOL.md` and `DOC-COMPACTION.md` are the standing case `tasks/README.md` §"Compaction
tasks" names: *"When the paths are reserved … the task still lives here, because `inbox/` is not
committed and a debt filed there would pass on the filer's machine and fail in CI."* That is
working as designed. **What is not obviously designed is the interaction with an owner commit
landing mid-leg**: the owner grows a reserved doc, the gate goes red on `main`, and the only actor
present is one that may neither edit the file nor leave the gate red. Filing an `Owner: required`
debt is the escape hatch and it is a good one — but a leg has to *know* to reach for it, and this
one reached for it only because the failure landed in the middle of its own fold. A successor that
meets a red `check-doc-size.py` naming a reserved doc should do this and carry on, not stop.

## Done when

- [ ] `DOC-COMPACTION.md` is out of reserve, or its cap is deliberately raised with the reason
      recorded — **the owner's call either way.** The file's own §2 now says a split is the default
      remedy, which would mean deciding what the second file is; that is a structural decision
      about the doc corpus and `DOC-PROTOCOL.md` reserves it.
- [ ] The human question is answered in the commit message, in the compactor's own words
      (`DOC-COMPACTION-PASS.md`): can this file alone answer what someone needs in order to decide
      whether a doc should be compacted today?
- [ ] The `Must not delete:` list above survives, or each dropped item is named and argued.
