# embarch-umbrella decisions: the deleted-doc guard test

**Status:** active, 2026-11-27.

**Split out of [reporting.md](reporting.md) on 2026-11-27 (`tasks/umbrella/129`)** — that file was in reserve. Entry moved verbatim.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 52 — The deleted-doc guard test walks every tracked source file, and no longer skips comments

`doctor::tests::no_check_text_names_a_document_the_four_file_split_deleted` (decision 46's
`milestone-6.md` citation is exactly the failure mode it exists to catch) `include_str!`'d only
`doctor.rs` and `continue`d past every `//`/`///` line before checking for `design.md`/`milestone`.
Both narrowings defeated the point: the four-file split touched every sub-project, not just this
one file, and a stale citation sitting in a comment misroutes a reader reading the source exactly as
well as one sitting in a `Check.detail` misroutes an operator reading `doctor`'s output — so exempting
comments exempted the whole class this defect belongs to (task `umbrella/057`).

**Widened to every `src/*.rs`, comments included, with two exemptions and both by construction rather
than by pattern.** `doctor.rs` itself is skipped by file name, since this test necessarily quotes the
forbidden strings in its own body; a line naming `install.rs`'s `LEGACY_MARKER` identifier is skipped
by that name, since that constant's value must stay byte-for-byte equal to a marker real installs
already wrote into rc files, `design.md` and all (see `install.rs`). Nothing else is exempt — a
forbidden string in a comment anywhere else in `src/` now fails the build. **Rejected: keep skipping
`//` lines and add a denylist of exempt files instead** — a denylist is exactly the mechanism that let
this test re-exempt everything the moment a second file needed even one legitimate quote.
