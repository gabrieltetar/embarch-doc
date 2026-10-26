# 084 — A saved study is never written into another repo, stripped of its taps, or orphaned by an `.eap` delete

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui findings 1, 9 and 11), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Three paths in `src/study_designer.rs` damage a saved study, or remove what it depends on, without refusing.

1. **The `firmware_version` write-back goes to whichever project is open when the build finishes.** `submit_run` builds from the repo it captured at submit time (`:1953`). `update_saved_firmware_version` instead resolves `sd.project()` again after the build (`:2144`). The write-back runs only on decision 40's waved-mismatch path. If the open project changed during the build and the new repo has a study with the same slug, the first repo's flashed version is written into the second repo's file, and the build stream says "the saved file was updated".
2. **A taps sidecar that will not parse loads as no taps.** `_embarch_ui_rows` refuses with a 400 when it cannot be read back (`:3398-3401`), but `_embarch_ui_taps` falls back to `unwrap_or_default()` (`:3410`). The next Save rebuilds `Study.streams` from the empty table and returns 200, so the taps and their record checks are gone from the runnable file.
3. **`.eap` delete checks only the blocks that resolved.** `api_protocol_delete` scans for references under each name in `file.resolved()`, and under the stem only when the file did not parse (`:3061-3075`). A block that parses but does not resolve is never checked. When no block resolves at all, no scan runs, so a study the scan could not read never blocks the delete. A saved study embeds its `ProtocolDef` and still runs without the file, but deleting the file deletes the source its author would fix.

Suggested direction: the write-back uses the repo the run started from; an unreadable taps sidecar is refused the way the rows sidecar is, or else recovered with `taps_from_streams`; the delete scans every block name the file declares and always reports unscannable studies. The worker decides how.

## Why now

spec.md:54: "A destructive edit that would break a saved study is refused, naming the studies … a directory it cannot fully read is not permission to delete." Decision 14 is about not mixing one repo's state with another's. Item 1 writes one repo's build result into another repo's tracked file. Each fix is a few lines with a unit test beside the existing ones.

## Done when

- [ ] A test opens repo A, starts a waved-mismatch run of a saved study, switches to repo B (which holds a study with the same slug) before the write-back, and finds A's file updated and B's file byte-identical.
- [ ] Loading a study whose `_embarch_ui_taps` does not parse either refuses with a message naming the file, or returns the taps recovered from `Study.streams`. In neither case does it return an empty tap list that Save would write.
- [ ] Deleting an `.eap` file whose block parses but does not resolve is refused while a saved study names that block. A study file the scan cannot read blocks the delete even when no block in the file resolved.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` and `open.md` are in reserve with parked compaction debts (`tasks/ui/078`, `tasks/ui/074`).
