# Make the dev-bench "not found" error name the declared fact that excluded every candidate

**State:** done
**Source:** owner's repo survey, 2026-09-06 — decision 20's own failure mode, with a remedy that preserves the cause
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`src/hardware/port.rs:136-142` tells any operator whose candidates were all filtered away to
"re-enroll dev-bench … with only its own probe attached". But the narrowing that emptied the list
may have been a declared `link_port_serial` (hard-narrows at `:316`) or a declared
`link_port_interface` (`:327-329`) — and `src/hardware/validate.rs:331-333` carries both of those
over on re-enrollment keyed by probe serial. **The advice the message gives cannot clear them**, and
`src/hardware/enrollment.rs:205-216` offers no way to unset either.

`NotFound` should carry which rule emptied the candidate list, and its `Display` should send the
operator to the fix that can actually work. That means a way to clear a declared link serial or
interface exists on the crate API and the CLI, rather than requiring a hand edit of a machine-wide
TOML.

**Host-side:** fixture tests over candidate lists, not a bench. Do not enroll anything.

## Why now

This is the exact failure decision 20 records — a stale declared link serial "hard-narrows detection
to a port that cannot exist" — and the message currently routes that operator to a command that
preserves the stale fact.

## Measured on the bench, 2026-09-06 (leg 020, `tasks/topology/006`)

There is a **fourth** case, and it is the one a fleet leg hits every time. Run from WSL with the
board attached and working, `embarch-topology dev-bench` printed:

    Error: no embarch-dev-bench serial port found (0 serial port(s) visible, 0 with a
    recognized link VID ...) — check dev-bench's USB connection

The USB connection was fine. The ports are on the **Windows host**, where the real Core runs;
this process was on neither. **`0 serial port(s) visible` is the tell and the message does not
use it** — zero ports on a developer machine means the enumerator is on the wrong host far more
often than it means every cable fell out.

**The same binary already knows this.** `embarch-topology status`, on that box, in the same
second, resolved Core as `http://172.22.128.1:4884 (wsl-host)` and reported
`Core { authorized: false }`. So the machine has established it is the remote half of a split
setup at the moment its sibling command blames the cable. The `usbipd attach` parenthetical is
in the message, but it trails a sentence that has already sent the reader to the hardware.

## Supervisor direction (leg 045)

**Verify the line numbers before you trust them.** Every site this task cites —
`port.rs:136-142`, `:316`, `:327-329`, `validate.rs:331-333`, `enrollment.rs:205-216`
— was read on 2026-09-06, and `embarch-topology` has landed units since
(`topology/003`, `007`, `009`, `015`, `016`). Find each site by what it *does*,
not by its line number, and if one of them no longer says what the task claims,
say so rather than working around it. That is a finding, not an obstacle.

**The fourth case is the one to get right, and it is the one you cannot
reproduce.** A leg running in WSL against a Core on the Windows host sees
`0 serial port(s) visible` and is told to check the USB cable. The claim in
"Measured on the bench" is that the same binary already has the evidence to know
better — `embarch-topology status` resolved a `wsl-host` Core in the same second.
**Establish for yourself that the enumerator and the resolver can actually reach
the same fact in the same process** before you write a message that promises it.
If the split-host conclusion is only computable in `status`'s code path and not
where `NotFound` is constructed, then the honest fix is smaller than the
Done-when asks — say which, and write down what plumbing the full version would
need, rather than reaching for it.

**Zero ports and no-matching-VID are different, and the message should not merge
them.** Zero visible ports on a developer machine is far more often "this process
is on the wrong host" than "every cable fell out". Ports visible but none with a
recognised VID is a genuinely different diagnosis. Keep them separate arms.

**The clearing affordance is a real API addition, not a message change**, and it
is the item most likely to grow. A way to unset a declared `link_port_serial` or
`link_port_interface` has to exist on the crate API and the CLI, because
re-enrolment carries both over keyed by probe serial — which is precisely why the
current advice cannot work. If you find this needs a numbered decision (how an
unset is represented, whether it round-trips through the TOML), write one; it is
within your sub-project and needs nobody's approval.

**Do not enroll anything and do not touch hardware.** This is fixture tests over
candidate lists. `cargo test --no-default-features --features hardware` is in
your gate and compiles the hardware paths without needing a board.

**Reserve line for `topology`:** `spec.md` 9602/10240 B (**638 bytes**),
`open.md` 4322/5120 B (798 B), `decisions/validation.md` 11178/12288 B (1110 B).
Their compaction tasks `topology/014` and `topology/017` are both `open`, not
parked, so nothing blocks you — but if your work spends a reserve that nothing
has filed against, file `tasks/topology/<NNN>-compact-topology.md` in the same
commit per `tasks/README.md`. Decision numbers are global across `decisions/*.md`.

## Done when

- [x] The zero-ports-visible case names the split-host possibility **first**, not as a
      parenthetical, and says what `status` would show — it is already computable.
      **Landed narrower than asked, and here is why.** The literal ask — embed
      `status`'s live, network-probed resolution (`wsl-host`, `authorized: false`) inside
      `NotFound`'s own message — is not reachable at `NotFound`'s construction site for
      every consumer. `select`/`detect` (where `NotFound` is built) live in the `hardware`
      feature; the live probe needs `software`'s `reqwest`/`tokio`; and `embarch-core` —
      the consumer whose build actually hit this failure — links only `hardware` and
      deliberately never `software` (`src/lib.rs`'s own doc comment, avoiding `reqwest`'s
      transitive `aws-lc-sys` on Windows). `NotFound::Display` is also a plain formatting
      trait with no I/O of its own, so it could never make the live call itself regardless
      of feature wiring. What **is** reachable everywhere, synchronously, with zero new
      dependencies: whether this process is running inside a WSL2 guest at all (pulled out
      of `software::detect_wsl2` into a new unconditionally-compiled `wsl2` module).
      `NotFound` gains `likely_wsl2`, filled in only by `detect()` (the live wrapper,
      never by pure `select()`), and `Display` leads with the split-host possibility and
      names the command to run (`embarch-topology status`) rather than asserting a
      resolution this call never made. `embarch-topology decision 27` has the full
      argument; `open.md` records the remaining gap for `embarch-core` specifically.
- [x] `NotFound` gains a field naming the excluding rule, set at each narrowing site in `select`.
- [x] `Display` prints the matching remedy per rule; the existing wording stays for the
      role-fallback case.
- [x] Fixture tests cover: declared serial matches nothing, declared interface matches nothing, and
      no candidate VID at all — each asserting the message routes to a different fix.
- [x] A way to clear a declared link serial/interface exists on the crate API and the CLI, with a test.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features hardware`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
      (No suite-level doc was made false by this — nothing outside `topology` cites
      `NotFound`'s wording or shape, so no `status.d/` fragment was needed.)

## Line-number verification (leg 045)

Every cited site still does what the task said, but every line number had drifted —
`embarch-topology` landed `topology/003`, `007`, `009`, `015`, `016` since 2026-09-06, all
of which touched these same files:

- `port.rs:136-142`'s "re-enroll dev-bench ... with only its own probe attached" text was
  (pre-this-task) at lines 167-173, inside `NotFound`'s `Display` impl (which starts at 160,
  not 136 — line 136 is now inside `detected_by_for_vid`'s match arms).
- The declared-serial hard-narrow the task calls out at `:316` was at lines 358-360
  (`} else { candidates = narrowed; }`, the non-fallback branch of the serial filter).
- The declared-interface hard-narrow at `:327-329` was at lines 370-372
  (`if let Some(interface) = filter.interface { candidates.retain(...) }`).
- `validate.rs:331-333`'s "carries both over on re-enrollment keyed by probe serial" was at
  lines 364-373 (the `link_port_serial`/`link_port_interface` carry-over in `enroll`, with
  the doc comment explaining why it's keyed on probe serial rather than role).
- `enrollment.rs:205-216` is the one citation that still matched exactly:
  `set_link_port_serial`/`set_link_port_interface` were still at those lines, and there was
  still no `clear_*` counterpart before this task.

None of the drift changed the substance of the claim — every site still did what the task
said it does — so this is a finding about the task's own citations going stale under normal
landed work, not a defect in the sites themselves.
