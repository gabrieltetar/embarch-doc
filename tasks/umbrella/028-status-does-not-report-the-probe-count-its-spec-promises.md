# Make `embarch status` report the probe count its spec promises, or correct the spec

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-umbrella/spec.md:58` advertises a field the binary never emits
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-umbrella/spec.md:58` says "`embarch status` … One status call: is Core up,
which class, **how many probes**. `--json`". `src/main.rs:254-255` prints "auth: not checked (this
probe is unauthenticated)" under a comment saying probe listing "arrive[s] with milestone-6.md
§3.3/§3.4", and `status_json` (`main.rs:264-284`) carries `reachable`/`base_url`/`topology`/
`authorized`/`attempts` and no probe count.

**Either direction closes this, and the unit picks one.** Making the authenticated `GET /status`
the spec describes is cheap — token resolution already exists in `token.rs` and the identical call
is in `doctor.rs` (`authed_get`, `AuthedStatus`) — and both the human and `--json` forms then carry
the count, with a distinguishable value when the token could not be resolved. If the cheap
unauthenticated shape is judged correct instead, edit the spec row **and** the stale `milestone-6.md`
comment rather than leaving them contradicting each other.

## Why now

`decisions/reporting.md` 11 makes `status --json` "the contract a UI consumes … so the UI does not
arrive and find only human-formatted text to scrape". A field the spec advertises and the binary
never emits is that contract being wrong in the one place a consumer reads it.

## Done when

- [ ] `embarch status` and `status --json` agree with `spec.md`'s row, whichever direction the unit
      resolves it, and `decisions.md` records the choice.
- [ ] Unauthenticated / no-token is its own reported state, never a silent `0`.
- [ ] Tests cover the JSON shape for reachable-with-probes, reachable-without-token, and unreachable.
- [ ] The `milestone-6.md` comment at `main.rs:254` is gone.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
