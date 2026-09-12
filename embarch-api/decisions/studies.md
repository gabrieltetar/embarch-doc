# embarch-api decisions: Submitting and orchestrating studies (moved)

**Status:** active, 2026-09-11.

Split out of size reserve (`tasks/api/074`) into two files along its natural seam — reads vs
reflash. This file is a redirect kept so an old link (including one baked into `history/`, which
a compaction may not edit) still resolves; it carries no decision text of its own.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 27, 28 — moved to [study-reads.md](study-reads.md)
Validate capacities and fill the seals before the HTTP call.

### 31, 33 — moved to [study-reads.md](study-reads.md)
`run_study`'s schema declares an object, and the handler tolerates a stringified one.

### 39 — moved to [study-reads.md](study-reads.md)
The manifest rides the build, and one parameterised stream tool replaces three.

### 40 — moved to [study-reflash.md](study-reflash.md)
A reflash selector, and this crate will not move an engineer's tree.

### 44 — moved to [study-reflash.md](study-reflash.md)
Three gaps in `run_study`'s own contract, and the tool text was the defect.
