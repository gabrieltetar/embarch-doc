# Give `doctor` check 2 tests, and make its Fail detail name the evidence it inferred the class from

**State:** claimed — leg 046
**Source:** `embarch-umbrella/open.md` — "`saved.host` is sticky, and `doctor` check 2 still reads it … check 17's fix line was fixed off it, **check 2 was not**"
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`src/doctor.rs:383-410` — `check_service` has four fix arms and **no test in the 121-test module
calls it**. `src/doctor.rs:2766` feeds it `config.core.host` *or* a sticky `saved.host`, so an old
`--host` makes it print "Core runs on another machine. On that machine: `embarch-core install`" on a
`wsl-host` bench, and its whole detail is the string `"not reachable"`.

Pin the four arms with tests. Make the Fail detail state *why* it concluded that class — "inferred
`remote` from a saved `--host` of `<x>`, recorded by an earlier `setup`" — so an operator sees the
input before following a remedy on another machine.

**The verdict does not change and nothing clears `saved.host`.** `open.md` records that the clearing
half was withheld deliberately, because it changes behaviour on real machines on a guess. Naming the
evidence is the half that costs nothing.

## Why now

`open.md` names this exactly and says the fix was withheld for the reason above. Check 17's fix line
was already corrected off the same defect; check 2 was left.

## Done when

- [x] Tests cover Pass and the Remote / WslHost / Local / no-binary fix arms (7 new tests in
      `src/doctor.rs`'s `check 2` section).
- [x] A test pins that a sticky `saved.host` with no `config.core.host` produces a detail naming
      that host as the reason (`check_2_names_a_sticky_saved_host_as_the_remote_evidence`).
- [x] No verdict or fix-command changes; `saved.host` handling is untouched — `check_service` still
      computes `host = config_host.or(saved_host)` and feeds it to `setup::infer_class` exactly as
      before; only `config_host`/`saved_host` now arrive un-merged, so the detail can say which one
      it read.
- [x] The `open.md` bullet is updated. **Correction to this task's own premise:** `open.md` is not
      actually near its cap — this leg's dispatch measured it "comfortable" at 4,440/5,120 B, and
      the file `tasks/umbrella/009` parks the compaction for is `decisions/bind.md`, not `open.md`.
      Rewrote the bullet anyway with growth in mind: net +54 bytes (4,440 → 4,494), well clear of
      `check-doc-size.py`'s reserve line.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build`, `cargo test` (223 passed,
      0 failed, including the 7 new check-2 tests), `cargo clippy --all-targets -- -D warnings`
      (clean) in the code repo; `scripts/check-docs.py` (10/10 green), `check-ownership.py` (both
      repos), `check-client-names.py` (both repos) in the doc repo.
- [x] `open.md` updated, `changelog.d/umbrella-doctor-check-2-evidence.fixed.md` dropped.
      `spec.md`/`decisions.md` deliberately left untouched: the check-2 row and every verdict are
      unchanged, and this is a mechanical evidence-naming fix rather than a new design call —
      nothing there is now false. No suite-level doc (`embarch.md`, `suite/*.md`,
      `embarch-decision-reversals.md`, `embarch-glossary.md`) names check 2's old bare-"not
      reachable" behaviour, so no `status.d/` fragment.
