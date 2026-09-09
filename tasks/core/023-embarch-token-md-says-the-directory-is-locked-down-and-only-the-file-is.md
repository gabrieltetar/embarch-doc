# 023 — `embarch-token.md` says the directory is locked down, and only the file is

**State:** done — leg 059, 2026-09-09, burndown (a decision is still owed; see Done when box 2)
**Scope:** core
**Hardware:** none — reading `embarch-core`'s own `src/token_store.rs` settles this. **No live ACL
observation is needed and none should be attempted**: a WSL session cannot read a Windows ACL, and
this question does not require one.
**Source:** `embarch-worker` on `tasks/topology/013`, 2026-09-07, leg 035 — found while settling
whether `embarch-topology` decision 23's "unprivileged CLI" rationale was true. It was not, and
this doc is where the wrong idea came from. Drained from `inbox/` by leg 035.
**Owner:** no

## Supervisor note — leg 059, doc-size reserve in `core`

**`embarch-core/open.md` has 69 B left** (5051/5120) and its compaction task
`tasks/core/022-compact-core.md` is **blocked**. Treat `open.md` as effectively full: if this
unit needs to write there, compact that file as part of the unit, carrying `022`'s
`Must not delete:` list and closing only `open.md`'s item — prefer a split or a duplicate
deletion over a squeeze (`DOC-COMPACTION.md` §2). No other `core` doc is in reserve. If your
work pushes a different file into reserve, file `tasks/core/<NNN>-compact-core.md` in the same
commit.

**This leg runs in burndown, which forbids authoring a new numbered decision.** Correct the
prose, and if the finding looks like it deserves a decision, say so in your report instead.

## What

`embarch-token.md` §2 says: *"Core creates the directory and file with owner-restricted
permissions."*

Reading `token_store.rs` directly: `restrict_token_file_permissions(path)` is called with `path` =
the **token file** (`%ProgramData%\embarch\token`), and its `icacls /inheritance:r /grant:r …` call
names that file path, never the parent directory. The directory itself (`local_data_dir()`'s
`%ProgramData%\embarch`) is created by a plain `std::fs::create_dir_all(parent)` a few lines
earlier **with no ACL call at all** — it keeps whatever default ACL Windows gives a fresh
`ProgramData` subfolder.

So only the **file** is locked down to the creating account + `SYSTEM` + `Administrators`; the
**directory** is not. And as it happens that is structurally necessary — it is exactly what lets
`embarch-topology`'s own unrestricted `enrollment.toml`, one level down in the same tree, be
readable and writable by both the Core service account and an unprivileged CLI account.

## Why now

**A fact with no accurate home attracts wrong citations.** The "directory and file" phrasing reads
as if both were restricted, and that reading is what `embarch-topology` decision 23 copied into its
own rationale — which then argued, backwards, that an *admin-owned* directory is what lets an
unprivileged CLI read a file in it. Had the directory really been admin-owned, the unprivileged CLI
could not have used it at all. That decision was corrected on 2026-09-07 (`tasks/topology/013`, doc
`7008fdc`); **this is the source both consumers read, and it is still wrong.**

It is a small wording fix. It is filed because the same sentence has now produced one confirmed
reasoning error one repo over, days after it was written, and nothing stops a third consumer.

## Done when

- [x] `embarch-token.md` §2's *"Core creates the directory and file with owner-restricted
      permissions"* says plainly that only the token **file** gets the `icacls` lockdown, and that
      the directory is left at the OS default.
- [x] **Whether that is deliberate is the real question, and the answer belongs in a decision, not
      only in a corrected sentence.** Not recorded as a decision in this unit — **this leg runs in
      burndown, which forbids authoring a new numbered decision** (leg 059 note above). The prose
      now names the consequence inline (topology's `enrollment.toml` relies on the directory's
      default permissiveness) so the fact has an accurate home even without a decision number. **A
      numbered `embarch-core` decision is still owed**, with exactly the consequence this task
      names: a future change that tightened `%ProgramData%\embarch`'s directory ACL would silently
      break `embarch-topology`'s cross-account read/write of `enrollment.toml`. Recommend filing it
      as the next available `embarch-core` decision number once a leg is free to author one.
- [x] `embarch-topology` decision 23 (`decisions/storage.md`) already describes the true state and
      points here. Checked against the new wording — it still reads correctly; **not edited**.
- [x] Nothing asserts what `%ProgramData%\embarch`'s ACL concretely **is** on any real machine. The
      new wording says only that Core never restricts it, not what the default grant contains.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). No `changelog.d/` fragment — this stayed a
      pure wording correction, no decision was authored.

## Doc-size

`embarch-core/interfaces.md` is in reserve at **14,527 / 15,360 B (94.6%, 833 B left)**, filed
against `tasks/core/022-compact-core.md`, which is **`blocked` on `In flux: yes`**. `embarch-token.md`
itself is not in reserve. If a decision comes out of this and the natural home is a file in reserve,
say so rather than squeezing it in — and note that a blocked compaction task parks the *pass*, not
the reserve, so the supervisor dispatching this may tell you to compact that file as part of your
own unit.
