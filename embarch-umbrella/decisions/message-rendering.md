# embarch-umbrella decisions: rendering another program's text into a check's message

**Status:** active, 2026-09-07.

**Split out of [reporting.md](reporting.md) on 2026-09-07** — that file's reserve was tipped to
94% by decision 46's amendment (`tasks/umbrella/040`), which is a *different* decision, still in
flux, and not to be touched by this split. This entry is a verbatim move plus its own amendment,
not a restatement of anything else in `reporting.md`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 43 — The one-line message rule is a runtime property, and normalisation happens at the point of interpolation, not by widening the guard's exemption

Every `detail` and `fix` is **one line with no run of two or more spaces.** The rule exists because
of what Rust does to a long string literal wrapped without a trailing `\`: the continuation's
indentation stays *inside* the sentence, so the defect renders as a run of spaces mid-word and
compiles, tests and ships. A `contains` assertion reading one side of the wrap does not catch it,
which is how check 14 shipped it twice.

`no_check_renders_a_run_of_two_or_more_spaces` holds every **pure judge**'s verdict to a fixture
corpus. **Its pinned exemption is a statement about the fixtures, not the program**: the trigger is
a literal `'\n'`, so what it exempts is *checks whose fixtures contain a newline* — check 6's `{e:#}`
of a `toml` parse error, whose caret diagram is not ours to police. A live run on 2026-09-06 showed
the gap this leaves: check 1's `binary_version` interpolated `embarch-core --version`'s **stdout**
into `detail` verbatim, and the deployed Core's multi-line `Caused by:` chain on a log-directory
permission failure carried newlines, multi-space runs and **raw ANSI escape sequences** into
`--json` with the guard green — because the corpus hands check 1 a version string that is a version
string.

**Chosen (`tasks/umbrella/031`): normalise at every point that interpolates another program's raw
output, not by widening the exemption** — a wider exemption is how a green test comes to be believed
to cover more than it does. `one_line()` (added by `umbrella/030`) collapses whitespace runs and
drops control characters; `031` extended it to consume a whole ANSI CSI sequence (`ESC [ … `
through its final byte) rather than leaving the sequence's body behind as literal text, which is
what "escapes stripped" means here. Applied at every site found by re-grepping the module rather
than trusting an earlier comment: check 1's `--version` output (`check_binaries`, including the
values `manifest_mismatches` echoes into a mismatch message), check 4's and check 12's HTTP
response bodies, and the two `/dev-bench/hello` failure-body sites that feed checks 11 and 13 —
plus check 13's own `unexpected /dev-bench/hello response` arm, which echoes the full raw body and
was not named by the reading `031`'s task file started from.

**`embarch-core`'s stdout half is a separate, already-landed decision** (`tasks/core/015`,
2026-09-07): `--version` now writes only its version line to stdout, because its fallback tracing
init picked stdout as the default writer. That closes the one symptom this entry's live run
observed. **It does not close this entry** — the defect is the interpolation, not the one program
caught doing it, and the next foreign string a check meets would do the same thing.

**`open.md`'s statement of the checks-4-and-12 gap is a different gap and stays true**: those two
`async` checks have no pure judge, so their text is never tested at all, where check 1's is tested
against text it does not carry in the field. This entry's guard fix does not touch that gap.
