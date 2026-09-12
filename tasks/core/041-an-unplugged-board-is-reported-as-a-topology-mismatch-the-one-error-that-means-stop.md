# 041 — An unplugged board is reported as a `topology mismatch`, the one error whose whole meaning is "stop and get a human"

**State:** done — leg 085, 2026-09-11, `agent/core/041-not-attached-is-not-a-mismatch`
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

- [x] A detached enrolled probe and an attached-but-wrong-ID probe produce errors distinguishable
      by their lead clause, not only by reading to the end. — `/validate`'s JSON gets a `kind`
      field (`"not_attached"` vs `"mismatch"`) and a different status (503 vs 409); `flash`/`reset`/
      `run_study`'s plain-text paths get a differently-led sentence ("probe not attached for role
      ..." vs "topology mismatch for role ...").
- [x] A numbered decision records which is which and why, and whether `fix_it_url` belongs on both.
      — `embarch-core` decision 59 (`decisions/surfaces.md`): `fix_it_url` is `None`/omitted on the
      not-attached arm (a USB cable, not the Topology tab, is the fix).
- [x] Both arms have a test that would fail if they were conflated again. — `api::tests::
      a_detached_probe_is_not_attached_not_a_mismatch`, `a_wrong_live_id_is_a_mismatch`,
      `flash_reset_path_leads_differ_between_not_attached_and_mismatch`, and `study::tests::
      dev_bench_gate_not_attached_lead_differs_from_mismatch`.
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Resolution

`embarch_topology::hardware::TopologyMismatch` already carried `live_hardware_id: Option<String>`
— `None` exactly when nothing was compared (the probe couldn't be opened). Core was the one
collapsing both conditions under one lead; `embarch-topology` needed no change at all.

**`POST /validate`** (`src/api.rs`): `ValidateMismatchResponse` gains `kind: &'static str`
(`"not_attached"` | `"mismatch"`), `fix_it_url` becomes `Option<String>` (`None` on the
not-attached arm), and status is `503` for not-attached, `409` (unchanged) for a real mismatch.
Classification lives in `classify_topology_mismatch`, a pure function, tested directly.

**`flash`/`reset`** (`src/api.rs`, called via `hardware::flash`/`reset`): both used to fold every
failure — including a genuine mismatch and a merely-unplugged probe alike — into one `500` via
`internal_err`'s `{e:?}`. Now go through `describe_topology_error`, which renders a distinguishing
lead ("probe not attached for role ..." vs "topology mismatch for role ...") and a different status
(503 vs 409) for a `TopologyMismatch`, falling back to the unchanged `internal_err` shape for
anything else.

**`run_study`'s dev-bench handshake gate** (`src/study.rs`'s `enforce_dev_bench_gate`): same
conflation, found on inspection per the task's "check the other call sites" instruction — it
folded both conditions into `{e:?}` before this, then handed the resulting string to two callers
that both wrap it as one `BAD_GATEWAY` regardless of kind. Fixed with a text-only
`describe_gate_error` (no status split available at this call site, since both callers already
discard it) that gives the same two distinguishable leads.

**Not changed:** `embarch-api`'s MCP `validate` wrapper — the text the source incident actually
showed (`"topology mismatch for role 'dev-bench' (probe ..., chip ...): ... — fix it at ..."`)
further re-wraps `/validate`'s JSON with its own lead, in a different repo this task cannot write.
That wrapper now receives a `kind` field it did not have before and can branch on it instead of
`reason`'s wording — filed to `embarch-doc/inbox/` as a finding for `embarch-api` to pick up.

**Reserve:** `embarch-core/decisions/surfaces.md` was 12,019/12,288 B (269 B left), parked by
`tasks/core/038` on `In flux: yes`. Decision 59 belongs there topically, so per `DOC-COMPACTION.md`
§2 this unit compacted it — as a **split**, not a squeeze: `## The human enrollment surface`
(decisions 25, 27, 28, 50, 54, 57) moved verbatim to a new `decisions/enrollment.md`, a real
topical seam that was already a section boundary in the file. Nothing was deleted, so there is no
hunk to quote the first dozen words of. `surfaces.md` dropped to 7,025 B before decision 59 was
even added (7,969 B in flat text, landing at that size after formatting); `enrollment.md` is
8,239 B. `tasks/core/038` is closed (its own unpark condition named exactly this: "a compaction
pass finds a genuine verbatim split/squeeze that does not touch either decision's checkable
claims" — decisions 12 and 55 are unmoved). `decisions.md`'s index table updated for both files.

**Hardware-verification debt:** none of this needed hardware — both arms are pure functions of
`TopologyMismatch`'s own fields, exercised by unit test. Confirming the rendered text against a
real detached probe (as the task's own `Hardware:` line says) is free the next time either board
is unplugged and a caller runs `/validate` against it.

**Native Windows build:** not attempted here, per protocol §10 — this change joins the existing
outstanding `embarch-core` Windows-build queue (no `cargo build --target
x86_64-pc-windows-msvc`/no worktree-side Windows build was run).

**Gate:** `cargo build`, `cargo test` (197 passed, 2 ignored, 0 failed — includes the four new
tests above), `cargo clippy --all-targets -- -D warnings` all green in the code worktree.
