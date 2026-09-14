# 040 — 103 source citations never swept, and `hardware/validate.rs` was rewritten yesterday

**State:** done — worker agent/topology/040-src-citation-sweep, 2026-09-13. All 103 citation lines
read; see Result below.
**Source:** the leg of 2026-09-13 18:3x, counting every repo's source citations while filling the
queue. `tasks/topology/036` fixed **three** dead citations in this repo's source comments, but it
was findings-driven — it fixed the three somebody happened to notice. **No systematic sweep of
`embarch-topology/src/` has ever been filed or run**, and there are 103 citation lines in it.
**Scope:** topology
**Hardware:** none — source comments only; no board, no probe, no live Core.
**Owner:** no

## What

```
21  src/hardware/validate.rs
19  src/hardware/port.rs
15  src/hardware/signal.rs
15  src/hardware/mod.rs
 8  src/hardware/hardware_id.rs
 7  src/hardware/alert.rs
 6  src/software.rs
 5  src/hardware/enrollment.rs
```
…plus `lib.rs` (3), `paths.rs` (3), `wsl2.rs` (1). **103 lines, eleven files.**

**`check-decision-refs.py` resolves decision numbers only inside `*.md`**, so a wrong number in a
source comment fails no gate and never has.

## Why `validate.rs` first, and why it is time-sensitive

**`tasks/topology/038` rewrote the probe-selection half of `hardware/validate.rs` on 2026-09-13**
(code `96e86c68cc3383a7dd491ff3dfb5394f5a93f547`): `enroll`'s inline selection block became a `pub`
`select_probe(probes, probe_serial, action)`, reconciling three behavioural differences the two
copies had already accumulated, and **decision 32 was amended with a dated note.** A comment in that
file that describes the *old* inline behaviour, or that cites decision 32 without the amendment, is
false now and was true two days ago. **That is the exact class four consecutive sweeps this week
found their real yield in: a citation whose number still resolves, inside a sentence that has gone
false.**

`tasks/core/055` is landing the `embarch-core` half of that same reconciliation in parallel. If its
worker files an `inbox/` drop saying the topology-side bullet in `open.md` and decision 32 need
closing, **that drop is the companion to this task, not a duplicate of it** — this one is about
comments in `src/`, that one is about the doc statement of the duplication being half-closed.

## What to do

Take `hardware/validate.rs` first for the reason above, then the rest in the order listed. Get as
far as you honestly can; **a partial sweep with an accurate boundary beats a rushed complete one** —
file `tasks/topology/<next>` for the remainder, naming exactly which files you reached.

For each citation:

1. **Resolve the number and say which repo's set it resolves against.** `embarch-topology` is a
   dependency of `embarch-core`, `embarch-api`, `embarch-ui` and `embarch-umbrella`, and its
   comments legitimately discuss `embarch-core`'s behaviour — so a bare `decision N` here can mean
   either set, and two decisions can wear the same number. Use the labelled form
   `embarch-core decision N` for a foreign referent; same-repo citations stay bare. Do not invent a
   new form — the general question is owner-reserved (`tasks/doc/055`).
2. **Read the decision body against the sentence around the citation, not just the number.**
3. **Do not manufacture findings.** "Twenty-one checked, twenty-one held" is a real and reportable
   outcome. Say how many you actually read versus how many you counted.

## Result

All 103 citation lines in all 11 files read against the decision body behind each number, not just
against whether the number resolves. Two classes of defect found, both the same class the task
predicted: a sentence true when written, made false by a later landing that never touched the
comment.

**`validate.rs`** (21 read): `enroll`'s doc comment said decision 32 was "amended, not closed" and
named `tasks/core/055` as "blocked on this landing" — both written by `topology/038` on
2026-09-13, true then. `topology/041` closed decision 32 in `decisions/crate.md` the same day
(`core/055` landed as `86345c01a451b0696af36f42c28bf6676478124c`) but never touched this comment.
Rewritten to say decision 32 is closed and name `embarch-core` decision 61. Second defect, same
file: a comment written 2026-08-23 (one day *before* `GET /enroll` was retired 2026-08-24) still
named that retired Core page as "the first caller" needing optional `probe_serial` — false since
the day after it was written, untouched when decision 15's citation was added on 2026-09-07.
Rewritten to name the retirement and `embarch-ui`'s Enroll surface without asserting whether the
new caller exercises the same disambiguation (unverifiable from this repo).

**`mod.rs`** (15 read): the same decision-32-staleness class, independently — `select_probe`'s
doc comment named `tasks/core/055` as future work for `embarch-core::resolve_probe` to adopt.
Fixed the same way.

**`hardware_id.rs`** (8 read): one cross-repo citation used "its decision 49" rather than the
labelled `embarch-core decision 49` form the Done-when box requires — number and claim both held,
relabelled for form only.

**port.rs (19), signal.rs (15), alert.rs (7), software.rs (6), enrollment.rs (5), lib.rs (3),
paths.rs (3), wsl2.rs (1)** — 59 citations read, all held: number and surrounding sentence both
checked against the cited decision's body (cross-repo citations verified against `embarch-core`,
`embarch-ui`, `embarch-study-designer` and `embarch-outpost`'s own decisions where labelled).
`enrollment.rs` is worth naming on its own: it correctly disambiguates two *different* decision 27s
(`embarch-core`'s and `embarch-topology`'s own) inside one file by labelling both, which is the
disambiguation this task's rule 2 asks for, already done right.

**Read 103 of 103 counted.** 3 false sentences fixed, 1 citation mislabelled and fixed, 0 wrong
numbers. No `tasks/topology/<next>` filed for a remainder — there is none.

## Done when

- [x] `hardware/validate.rs` is swept end to end and every comment describing probe selection
      matches what `select_probe` actually does after `topology/038`.
- [x] The remaining files are swept, or the boundary is stated exactly and the remainder filed.
- [x] Every cross-repo citation in the swept files carries the labelled `<repo> decision N` form.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment. A numbered decision only if something was actually *decided*.

## Reserve, for planning

`embarch-topology/decisions/crate.md` is **12,075/12,288 B — 213 B left, 98.3%**, re-measured at
dispatch on 2026-09-13 20:00 and now the **highest** pressure in the suite; the figures above
(612 B, 95.0%) were true when this task was filed and are not any more. It is filed against
`tasks/topology/039`, whose size debt is due **2026-09-20**, the soonest date on the whole ledger —
and note that `039` is **`open`, not blocked** as this task originally said, so the debt is payable
by a later unit and does not need paying here. **Do not write into `crate.md`:** 213 B is roughly
two sentences, and a unit that spends it turns an unrelated sweep into a compaction. If this unit
needs to record something, put it in another `embarch-topology` decisions file and check that file's
headroom first; if your work leaves any doc in this scope in the last 10% of its cap unfiled, file
`tasks/topology/<next>-compact-topology.md` in the same commit — **your own scope**, never
`tasks/doc/`.
