# Make `embarch status` report the probe count its spec promises, or correct the spec

**State:** claimed by agent/umbrella/028-status-does-not-report-the-probe-count-its-spec-promises, 2026-09-07 10:25
**Source:** owner's repo survey, 2026-09-06 — `embarch-umbrella/spec.md:58` advertises a field the binary never emits
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## Doc-size reserve — supervisor, leg start 2026-09-07 09:44

**Two of your decision files are in reserve and both are filed against `tasks/umbrella/009`, which
is `blocked` on `In flux: yes`:** `decisions/bind.md` at **879 B** left (92.8%) and
`decisions/doctor.md` at **942 B** left (92.3%). `embarch-umbrella/open.md` has come in and out of
reserve four times across the last several legs.

**This unit should land in `decisions/reporting.md`, which is *not* in reserve** — decision 11 there
is the `status --json` contract this task is about, so that is where the choice belongs on the
argument rather than on the byte count. **If your work does push a file into the last 10% of its
cap, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit** naming the file — it is
not your job to run the compaction, it is your job to record the debt while you still hold the one
piece of context nobody else will have.

**One suite-wide hazard: `suite/features.md` has 60 bytes of headroom** (20,420 of 20,480 B) and is
*assembled* from `features.d/` fragments, so **a new `features.d/` fragment turns the fold red.**
If this unit makes `status` report the probe count, that is arguably a feature row — **write the
row's text into this task file and do not create the fragment**, and say so in your report. I will
carry it.

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
