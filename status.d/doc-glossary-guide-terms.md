**Target:** embarch-glossary.md (table: Study row replaced, eleven rows appended after the last row) and suite/studies-guide.md §1 (one sentence)
**Was:** the Study row says "run against a DUT through dev-bench"; the glossary has no row for bench lease, host study, instrument, bench board, role, enrolment, bootload, ledger, publish, saved bench or live bench
**Now:** the Study row names both runners and the eleven terms have link-only rows, each pointing at the doc that owns it; studies-guide §1 points at the Study row instead of restating it. Glossary size after the edit set: 9,222 B (was 8,199 B, +1,023 B, inside the 1,024 B headroom above the reserve line).

Task: [tasks/doc/102](../tasks/doc/102-glossary-rows-for-the-guides-terms.md) (EMB-317). Apply each edit as old text to new text; the supervisor writes any prose around it.

## Edit 1: `embarch-glossary.md`, the Study row

Old:

```
| **Study** | A scripted sequence of BLE stimulus and interaction steps plus measurement, run against a DUT through dev-bench. **Entirely static once submitted** | [study-designer](embarch-study-designer/spec.md) |
```

New:

```
| **Study** | A scripted sequence of steps plus measurement, run on the dev bench or Core's own host runner (`run_host_study`). **Entirely static once submitted** | [study-designer](embarch-study-designer/spec.md) |
```

## Edit 2: `embarch-glossary.md`, append after the `dev-bench debug log` row (the last row)

```
| **host study** | Run by Core itself | [core](embarch-core/decisions/host-study.md) 95 |
| **bench lease** | Session holds the bench | [core](embarch-core/decisions/lease.md) 93 |
| **instrument** | A declared bench device | [topology](embarch-topology/decisions/instruments.md) 49 |
| **bench board** | A board with no role | [topology](embarch-topology/decisions/enrollment-bench.md) 41 |
| **role** | `dut` or `dev-bench` | [topology](embarch-topology/decisions/enrollment.md) 35 |
| **enrolment** | A human binds probe to board | [topology](embarch-topology/decisions/enrollment.md) 14 |
| **bootload** | Image via the DUT's bootloader | [core](embarch-core/decisions/bootload.md) 77 |
| **ledger** | What ran on hardware | [api](embarch-api/decisions/ledger.md) 98 |
| **publish** | A run as one zip | [api](embarch-api/spec.md) |
| **saved bench** | A bench file in the repo | [ui](embarch-ui/decisions/saved-benches.md) 44 |
| **live bench** | A saved bench applied | [ui](embarch-ui/decisions/bench-live.md) 90 |
```

## Edit 3: `suite/studies-guide.md` §1, the study sentence

Old:

```
The unit of work is a **study**: an ordered list of steps, each a BLE action, with pass/fail checks. A **step is never
```

(the line is one paragraph line; match from `The unit of work is a **study**:` to `with pass/fail checks.`)

New:

```
The unit of work is a **study** ([glossary](../embarch-glossary.md): it runs on this bench or on Core's own host runner), an ordered list of steps with pass/fail checks. A **step is never
```
