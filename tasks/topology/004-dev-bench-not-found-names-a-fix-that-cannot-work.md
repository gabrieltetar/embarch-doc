# Make the dev-bench "not found" error name the declared fact that excluded every candidate

**State:** open
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

## Done when

- [ ] `NotFound` gains a field naming the excluding rule, set at each narrowing site in `select`.
- [ ] `Display` prints the matching remedy per rule; the existing wording stays for the
      role-fallback case.
- [ ] Fixture tests cover: declared serial matches nothing, declared interface matches nothing, and
      no candidate VID at all — each asserting the message routes to a different fix.
- [ ] A way to clear a declared link serial/interface exists on the crate API and the CLI, with a test.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features hardware`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
