# 041 — An unplugged board is reported as a `topology mismatch`, the one error whose whole meaning is "stop and get a human"

**State:** claimed — leg 085, 2026-09-11, `agent/core/041-not-attached-is-not-a-mismatch`
**Source:** leg 085, 2026-09-11. Hit live while selecting the bench unit `tasks/api/059`, with both
boards unplugged and `GET /status` reporting `"probes": []`.
**Scope:** core
**Hardware:** none — the two cases differ by whether `live` is `None` or a different ID, and both
are reachable from a unit test. Confirming the rendered text against a real detached probe is free
the next time one is unplugged, but nothing here needs a board.
**Owner:** no

## What

`POST /validate` for a role whose probe is simply **not plugged in** answers:

```
topology mismatch for role 'dev-bench' (probe 001057729826, chip 'nRF54L15'): probe '001057729826'
enrolled as role 'dev-bench' is not currently attached (recorded hardware_id 6fcddc36cb781b71,
live None) — fix it at http://127.0.0.1:4890/#topology
```

The sentence contradicts itself across its own two halves. The **lead** says `topology mismatch`.
The **body** says `is not currently attached` and `live None`. Those are two different conditions
with two different correct responses, and the lead names the wrong one.

## Why this is worth fixing rather than reading around

`embarch-topology` decision 20's failure is the reason enrolment exists at all, and the fleet's
own operating rules turn on telling these two apart — `.claude/leg.md` gives them opposite
handling, in consecutive bullets:

> - **A role that is not attached leaves the task `open`.** Not `blocked`. Say it once in the log
>   entry and move to the next unit. A board coming back is normal [...]
> - **A topology *mismatch* is different and you stop.** A probe that is attached but reports a
>   hardware ID other than the one enrolled means the board on the desk is not the board recorded.
>   **Never re-enrol to make it pass** [...] Leave the task `open`, name both IDs in the entry, and
>   **alert** — the owner re-enrols.

So the error's first two words route an unattended supervisor to **wake the owner up** for a cable
nobody has plugged in. An unplugged board at 3am is the single most ordinary state the bench is
ever in. A reader who parses the whole sentence gets it right; a reader who matches on the leading
phrase — which is exactly what the alert rule is written in terms of — gets it wrong, in the
direction that costs a person their sleep.

It also fails in the other direction and that half is worse: once `not currently attached` has been
seen rendered under a `topology mismatch` lead a few times, the lead stops carrying information,
and the **real** mismatch — attached, wrong hardware ID, the case decision 20 was written for —
arrives wearing a phrase that has been trained to mean "nothing is plugged in".

## Which is right

`live None` is not a mismatch. Nothing was compared: there was no live readback to compare the
recorded `hardware_id` against. A mismatch is `recorded X, live Y` with `Y` present and `Y != X`.

## Candidate direction

Give the not-attached case its own lead and its own error kind, so the two are distinguishable
before the body is read and without matching prose — e.g. `probe not attached for role 'dev-bench'`
— and keep `topology mismatch` for `live` present and different. `fix_it_url` is right for a real
mismatch (the owner re-enrols in the Topology tab) and is misleading for a detached probe, where
the fix is a USB cable; consider dropping it from the not-attached arm.

Check whether `flash`/`reset`/`run_study`'s mid-attach check renders the same conflated text, since
it is the same comparison — and whether `embarch-api`'s `validate` wrapper re-words either.

`embarch-core/open.md`'s "route sweep proves rejection, not reach" bullet is the neighbouring gap:
this is a per-route *success/failure-shape* fact that no per-route fixture asserts today.

## Done when

- [ ] A detached enrolled probe and an attached-but-wrong-ID probe produce errors distinguishable
      by their lead clause, not only by reading to the end.
- [ ] A numbered decision records which is which and why, and whether `fix_it_url` belongs on both.
- [ ] Both arms have a test that would fail if they were conflated again.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
