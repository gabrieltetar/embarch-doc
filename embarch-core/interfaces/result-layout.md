# embarch-core interfaces: Result layout on disk

**Status:** active, 2026-09-07. Split out of [../interfaces.md](../interfaces.md) on 2026-09-07 (`tasks/core/020`) when that file reached its size cap — a reference table, not cut, per [../DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3. (Itself moved here from `spec.md` §5 on 2026-09-05, [../DOC-COMPACTION.md](../../DOC-COMPACTION.md) §9: a reference table is loaded deliberately, not carried by everyone who opens the spec.)

Index: [../interfaces.md](../interfaces.md).

What the [studies routes](studies.md) are reading. Core owns these paths and this storage; `embarch-study-designer` owns every **row shape** inside them.

```
study_results/<study_id>/
├── events.json          the StudyResult: steps (with both time edges), provenance, streams
│                        written incrementally, `.partial` until StudyDone
└── streams/
    ├── index.json       per tap: id, name, files, encoding, alias, rendered, note
    ├── <tap>.bin        byte-for-byte what arrived — written first, always
    ├── <tap>.1.bin      the previous segment, after one rotation
    ├── <tap>.csv        the rendering, for Samples / GattTranscript / Struct
    ├── <tap>.txt        a Text tap: raw and rendering are the same bytes
    └── <tap>.arrival.csv  OutpostTrace only: frame_index,rx_utc_ms,frame_bytes
```

`named` and `timed` are two independent booleans in the index and on the wire — a trace can be named and untimed, or neither.

**Retention is bounded by count, not bytes**: `EMBARCH_STUDY_RESULTS_KEEP` (default 50, `0` disables) sweeps at `POST /study`. `embarch doctor` check 16 reports the count *and* the size, because the bytes behind those runs are still nobody's bound.
