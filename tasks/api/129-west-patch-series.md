# 129 — Round-trip a west manifest's Zephyr patch series through one scratch tree

**State:** done on agent/api/129-west-patch-series, 2026-10-28 — awaiting land
**Dispatch note, 2026-10-28 leg — reserve in `embarch-api`:** `decisions/client-crate.md` 707 B left (filed: `tasks/api/140`), `open.md` 832 B left (filed: `tasks/api/144`). This task should need neither; put its decision in a topic file with room (or a new one) and keep `open.md` additions to a line, or compact that file in this unit and close its item in the filing task.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 32 scratch Zephyr worktrees (18 in one session), 8 hand-written regen, renumber and message scripts; about 20 manifest "Fix:" commits each split across 2–6 patch commits at curation; a 22→6 regroup by topic; patch regeneration 2.3 % of review-loop cost and 6 % in the manifest sessions
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Add an `embarch-api patches` command family for a west manifest that carries module patches (`patches.yml` plus patch files applied by `west patch`). **`patches export`** creates, or reuses, one scratch checkout of the module at the manifest's base revision. It holds one commit per patch file in `patches.yml` order, with the message taken from the patch header. **`patches import`** writes the patch files back from that commit range: stable headers, author and date kept, each entry's sha256 in `patches.yml` updated, and a list of which files changed. A fix made as a commit on top of the series is split by the patch each hunk belongs to and folded into that patch's commit, so a "Fix: correct patches 0013 and 0015" commit never needs splitting by hand at curation. **`patches regroup --map`** merges and renumbers patches (by topic, or upstream versus local directories). It proves that the applied module tree is byte-identical before and after, and rewrites patch-number references in commit messages, listing any it cannot rewrite. One scratch tree serves a whole review loop instead of one per round.

## Why now

Every review round that touched the carried Zephyr stack paid this cost again in the field. Each round made a new scratch tree, regenerated the patches with a hand-written script, and added a "Fix:" commit that later had to be split across the patch commits it touched. The engineer then asked for fewer patches, grouped by topic, and that regroup and its proof of tree identity were done by hand. The suite is about to become a second user: `dev-bench-pd-bench-own-west-manifest` (a sibling draft) gives pd-bench its own `west patch` set.

## Done when

- [x] On an unchanged 3-patch fixture series, an export/import round trip produces byte-identical patch files.
- [x] `patches.yml` sha256 fields are updated, and applying the series to a clean base gives the expected tree.
- [x] A fix commit touching two patches folds into both patch commits, and import rewrites both files.
- [x] `regroup` proves tree identity, renumbers files and `patches.yml`, and reports the message references it rewrote or could not rewrite.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Notes

Decision 92 (`embarch-api/decisions/patches.md`). CLI only, no MCP tool. The base revision is passed with `--base`, not read from `west.yml`; plain-diff patch entries (no mbox header) are unsupported. Verified on a throwaway fixture only; no hardware or real west workspace touched. Not done here: a `west.yml`-aware `--base`, and an MCP twin.
