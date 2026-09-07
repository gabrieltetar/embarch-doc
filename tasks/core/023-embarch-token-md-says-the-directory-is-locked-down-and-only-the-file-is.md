# 023 — `embarch-token.md` says the directory is locked down, and only the file is

**State:** open
**Scope:** core
**Hardware:** none — reading `embarch-core`'s own `src/token_store.rs` settles this. **No live ACL
observation is needed and none should be attempted**: a WSL session cannot read a Windows ACL, and
this question does not require one.
**Source:** `embarch-worker` on `tasks/topology/013`, 2026-09-07, leg 035 — found while settling
whether `embarch-topology` decision 23's "unprivileged CLI" rationale was true. It was not, and
this doc is where the wrong idea came from. Drained from `inbox/` by leg 035.
**Owner:** no

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

- [ ] `embarch-token.md` §2's *"Core creates the directory and file with owner-restricted
      permissions"* says plainly that only the token **file** gets the `icacls` lockdown, and that
      the directory is left at the OS default.
- [ ] **Whether that is deliberate is the real question, and the answer belongs in a decision, not
      only in a corrected sentence.** If the shared directory's permissiveness is load-bearing —
      and `embarch-topology`'s `enrollment.toml` is evidence that it is — then it is a property
      another repo now depends on, and a future change that tightened the directory would break
      that repo silently. Record it as a numbered `embarch-core` decision with that consequence
      named, or say explicitly why it does not rise to one.
- [ ] `embarch-topology` decision 23 (`decisions/crate.md`) already describes the true state and
      points here. Check it still reads correctly against your wording; **do not edit it** — it is
      another sub-project's doc.
- [ ] Nothing asserts what `%ProgramData%\embarch`'s ACL concretely **is** on any real machine.
      What the code does is establishable from source; what Windows' default grant contains on a
      given box is not, and `embarch.md` §5 forbids stating the second as fact.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment only if this
      turns into a decision; a pure wording correction may not warrant one.

## Doc-size

`embarch-core/interfaces.md` is in reserve at **14,527 / 15,360 B (94.6%, 833 B left)**, filed
against `tasks/core/022-compact-core.md`, which is **`blocked` on `In flux: yes`**. `embarch-token.md`
itself is not in reserve. If a decision comes out of this and the natural home is a file in reserve,
say so rather than squeezing it in — and note that a blocked compaction task parks the *pass*, not
the reserve, so the supervisor dispatching this may tell you to compact that file as part of your
own unit.
