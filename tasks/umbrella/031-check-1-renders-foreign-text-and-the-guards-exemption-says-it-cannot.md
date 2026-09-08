# 031 — Check 1 renders foreign text into `detail`, and the message-shape guard's pinned exemption says only check 6 can

**State:** closed (leg 045)
**Source:** supervisor bench unit `umbrella/027`, 2026-09-06 — live `embarch doctor --json` on the
primary bench; `embarch-umbrella/decisions/reporting.md` decision 43
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## `one_line()` now exists, and two things about it change this task — leg 026, from `umbrella/030`'s reviewer

**`umbrella/030` landed a `one_line()` helper in `src/doctor.rs`** (`embarch-umbrella` `d329842`),
collapsing every whitespace run to a single space and dropping control characters, applied at the
one interpolation point that unit owned. So this task no longer has to write the function. **But do
not simply call it and tick the box**, for two reasons the reviewer of that unit established:

1. **It drops the ESC byte as a control character and leaves the CSI body as literal text** — so an
   ANSI-coloured input becomes `[2m2026-09-07T00:24:33…[0m`, not clean text. That is harmless on the
   `reqwest` error chains `030` applied it to, and it is **not** what decision 43 means by escapes
   stripped. This task's whole premise is check 1 rendering raw ANSI, so **`one_line()` as it stands
   does not close this task's own case.**
2. **`030`'s doc comment names check 1 as the one remaining unnormalised site, and the honest list is
   longer.** Four other `detail`s interpolate Core's raw HTTP body verbatim: `unexpected HTTP
   {status}: {body}` (check 4), `dev-bench is busy: {body}` and `HTTP {status}: {body}` (checks 11
   and 13), and `detected: {body}` / `HTTP {status}: {body}` (check 12). Decision 43 already records
   the check-4-and-12 gap as separate and open and `open.md` carries it as its own bullet, so nothing
   contradicts anything — but a fix here that trusts that comment will miss four sites. **Re-derive
   the list from the source rather than from the comment**, and correct the comment while you are in
   the file.

## What was observed

`doctor --json`'s `checks[0].detail` — check 1, *binaries found* — came back containing **newlines,
runs of two or more spaces, and raw ANSI escape sequences**:

```
"embarch-core: …\\embarch-core.exe (\x1b[2m2026-09-07T00:24:33.426655Z\x1b[0m \x1b[33m WARN\x1b[0m
 \x1b[2membarch_core\x1b[0m\x1b[2m:\x1b[0m failed to set up daily-rolling log file, … \n\nCaused by:\n
    0: failed to create log file: Access is denied. (os error 5)\n    1: …\nembarch-core 0.1.4); …"
```

Every other check's `detail` and `fix` was clean; a scan of all 17 found exactly this one offender.

**The guard was green the whole time.** `no_check_renders_a_run_of_two_or_more_spaces`
(`src/doctor.rs:4999`) asserts its corpus covers checks
`[1,2,3,5,6,7,8,9,10,11,13,14,15,16,17]` — **check 1 included** — and then pins its exemption with
`assert_eq!(verbatim, vec![6])`, above a comment reading *"check 6 is the only check that renders
foreign text"*.

**That sentence is false at runtime.** `binary_version` (`src/doctor.rs:161`) runs
`<binary> --version` and interpolates `output.stdout` into `detail` verbatim. The deployed
`embarch-core.exe` writes a multi-line tracing warning to **stdout** when it cannot open
`C:\ProgramData\embarch\logs` as a non-elevated caller. The guard never sees it because the fixture
corpus hands check 1 a version string that is a version string.

## The shape, which is the reason this is worth a task rather than a line

The guard tests *fixtures*, so its exemption list is "checks whose fixtures contain foreign text" —
not "checks that render foreign text". Any check interpolating another program's output can break
the rule in the field with the test green. `open.md` has been stating this gap as *"cannot reach
checks 4 and 12"*, which is true, a **different** gap (those two have no pure judge at all), and
narrower than the real one.

**The stdout half is `embarch-core`'s** and is filed separately as `tasks/core/015` — a `--version`
that prints diagnostics on stdout is unparseable by anything. Fixing that would hide this defect
without closing it: the next foreign string does the same thing.

## Supervisor direction (leg 045)

**The stdout half landed twenty minutes ago and it does not close this task.**
`tasks/core/015` merged this leg (`embarch-core` `1c1224e`): `--version` now
prints exactly one clean line, because `init_tracing()`'s fallback arm was
calling bare `tracing_subscriber::fmt::init()`, whose default writer is stdout
rather than stderr. **So the specific string quoted in "What was observed" can no
longer be produced by that binary.** That is exactly the hazard this task's own
line 64 names: the observed symptom is gone and the defect is not. Do not
reproduce-then-declare-fixed. The defect is that `binary_version` interpolates
another program's stdout verbatim, and the next foreign string does the same
thing — you are fixing the interpolation, not the one program that happened to
be caught doing it. Say so plainly in whatever you write, because a later reader
who diffs the two units will otherwise think one of them was redundant.

**Re-derive the offender list from the source, not from any comment — including
this task file's.** The task names four other sites (checks 4, 11, 12, 13) from
a reading taken on 2026-09-06, and `embarch-umbrella` has landed several units
since. Grep the file yourself and report the list you actually find; if it
differs from the four named above, your list is the one that is right and saying
so is part of the unit.

**`one_line()` does not strip ANSI and you must not pretend it does.** It drops
the ESC byte as a control character and leaves the CSI body as literal text, so
a coloured input becomes `[2m…[0m`. Decision 43's "escapes stripped" means the
whole sequence. Either extend `one_line()` to consume the full CSI sequence or
add a sibling that does — and if you extend it, check every existing caller
still gets what it expects.

**Reserve line for `umbrella`, and this one needs a decision from you before you
start writing.** `embarch-umbrella/decisions/reporting.md` is **11,589 / 12,288 B,
699 bytes of headroom**, and decision 43 — which this task requires you to amend
— lives in it. Its compaction task `tasks/umbrella/040` is `blocked` on
`In flux: yes`. **Read that park before you assume it binds you**: the flux it
names is *decision 46* (the `ProbeReport` states, five to six), not decision 43.
`DOC-COMPACTION.md` §2's split-first rule applies — **a verbatim split restates
nothing, so `In flux: yes` cannot forbid one**, and §2 names a mission split as
the cheaper move where one fits. If 699 bytes will not hold your amendment,
split the file along a topic seam that leaves decision 46's prose untouched and
byte-for-byte unchanged, carry `umbrella/040`'s `Must not delete:` list forward
verbatim, and tick only the item for the file you actually split. Do not shorten
decision 46. Do not squeeze to fit. Also in reserve for this sub-project:
`spec.md` (413 B left), `open.md` (850 B), `decisions/bind.md` (879 B, parked).
If your work spends a reserve nothing has filed against, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.

**Decision numbers are global across `decisions/*.md`, not per file.**

**Out of scope:** `embarch-core`. The stdout half is done and is not yours to
revisit.

## Done when

- [x] Text interpolated from another program is **normalised at the point of interpolation** —
      collapsed to one line, whitespace runs squeezed, ANSI escapes stripped — so it satisfies the
      rule rather than being exempted from it. `check_handshake`'s existing
      `stderr.replace('\n', " / ")` (`src/doctor.rs:1421`) is the pattern already in this file.
      **`one_line()` extended** (`src/doctor.rs`) to consume a whole ANSI CSI sequence rather than
      dropping only the `ESC` byte. **Re-derived offender list** (grepped fresh, not read off the
      comment or this task file's own line 22-25 reading): check 1's `--version` output
      (`check_binaries`, normalised once at the top of the function so both the plain display and
      `manifest_mismatches`' echoed values get it), check 4's unexpected-status body, the two
      `/dev-bench/hello` failure-body sites that feed checks 11 and 13
      (`fetch_dev_bench_hello`), check 12's detected/HTTP-status bodies, **and one site the task's
      own reading missed**: check 13's `unexpected /dev-bench/hello response: {ack.raw}` arm,
      which echoes the whole raw body when a successful response is missing `firmware_version`.
      Checks 4 and 12 are `async` with no pure judge, so this closes their *rendering*, not their
      *test coverage* — that gap is still open, see `open.md`. `firmware_version`/`core_version`
      (short structured JSON scalar fields already extracted by `serde`, not free-form dumps) were
      deliberately left alone — a different, narrower category than the raw-body/stdout sites this
      task closes; check 15's `version_from_output` already parses rather than echoing verbatim.
- [x] The guard's comment and its `assert_eq!(verbatim, vec![6])` say what they actually pin.
      **Note the trigger is a `'\n'`, not "foreign text"** (`src/doctor.rs:5015`) — so the set is
      *checks whose fixtures contain a newline*, and **foreign text with a multi-space run and no
      newline is an offender today**, exempted by nothing and caught by nothing. Widening the
      exemption is the wrong fix and the entry in `decisions/message-rendering.md` says why.
      Comment rewritten in place.
- [x] Something covers the runtime case — `doctor::tests::check_1_normalises_a_foreign_version_string`
      hands `check_binaries` (check 1's judge) a version string shaped like the exact stdout quoted
      in "What was observed" — newline, multi-space run, ANSI colour codes — and asserts the
      rendered `detail` is one line, has no `"  "` run and no `ESC` byte.
- [x] `--json` carries no ANSI escapes from any check, verified rather than argued — a new
      assertion inside `no_check_renders_a_run_of_two_or_more_spaces` scans every pure-judge
      verdict's `detail`/`fix` for `'\u{1b}'`.
- [x] `open.md`'s guard bullet and the decision 43 entry are updated to whatever the fix makes true.
      **Decision 43 moved**: `decisions/reporting.md` was 11,589/12,288 B (699 B headroom) and
      decision 43 needed real new prose (the runtime fix, the re-derived offender list, the
      "does not close umbrella/031" note against `tasks/core/015`), too much for 699 B without
      trimming decision 46's untouched prose. Per `DOC-COMPACTION.md` §2's split-first rule, split
      decision 43 out **verbatim, then amended in its new home** —
      `decisions/message-rendering.md` — leaving decisions 11, 37, 39 and 46 in `reporting.md`
      byte-for-byte unchanged (`reporting.md` is now 9,064 B, 73.8% of cap, out of reserve).
      `decisions.md`'s index row split accordingly. `tasks/umbrella/040` (blocked on decision 46's
      own flux, untouched by this split) got one Done-when item ticked incidentally — see that
      file for why the rest stays open. `decisions/budgets.md`'s decision 45 entry, which pointed
      at decision 43 and asserted check 1 was still unnormalised, updated to match. `spec.md`'s
      pointer updated **net negative** (270 B → 227 B) — it was itself 413 B from its own cap.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What this does not close

**`tasks/core/015` landed twenty minutes before this task started** and fixed `embarch-core`'s
`--version` to stop writing its tracing fallback to stdout — so the exact byte string quoted in
"What was observed" above can no longer be produced by that binary. **That is not why this task is
closed.** This task closes because `binary_version`'s interpolation of *any* program's raw stdout,
and the equivalent raw-HTTP-body sites, are now normalised at the point of interpolation — the next
foreign string a check meets (a different binary's warning, a proxy's error page, anything) is
caught the same way. A reader diffing `core/015` against this unit should not read either as having
made the other redundant: `core/015` closed one symptom in one binary; this task closed the
defect class in `doctor`.
