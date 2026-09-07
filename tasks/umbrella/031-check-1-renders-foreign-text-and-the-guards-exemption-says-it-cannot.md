# 031 — Check 1 renders foreign text into `detail`, and the message-shape guard's pinned exemption says only check 6 can

**State:** open
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

## Done when

- [ ] Text interpolated from another program is **normalised at the point of interpolation** —
      collapsed to one line, whitespace runs squeezed, ANSI escapes stripped — so it satisfies the
      rule rather than being exempted from it. `check_handshake`'s existing
      `stderr.replace('\n', " / ")` (`src/doctor.rs:1421`) is the pattern already in this file.
- [ ] The guard's comment and its `assert_eq!(verbatim, vec![6])` say what they actually pin.
      **Note the trigger is a `'\n'`, not "foreign text"** (`src/doctor.rs:5015`) — so the set is
      *checks whose fixtures contain a newline*, and **foreign text with a multi-space run and no
      newline is an offender today**, exempted by nothing and caught by nothing. Widening the
      exemption is the wrong fix and the entry in `decisions/reporting.md` says why.
- [ ] Something covers the runtime case — a test that hands check 1's judge a version string with
      a newline and a multi-space run and asserts the rendered `detail` is still one line.
- [ ] `--json` carries no ANSI escapes from any check, verified rather than argued.
- [ ] `open.md`'s guard bullet and `decisions/reporting.md` decision 43 are updated to whatever the
      fix makes true.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
