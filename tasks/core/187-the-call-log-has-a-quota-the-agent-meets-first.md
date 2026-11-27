# 187 — The call log has a quota, and the agent's calls meet it first

**State:** done — quota, 90 % agent and 100 % person refusals, person-only PUT, decision 161; gate green; no hardware
**Source:** EMB-329 — The call log has no quota, so the agent's calls can fill the store
**Issue:** EMB-329
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`call-log.jsonl` grows without limit. Decision 158 (`core/182`) gave Core a
cannot-log state and a reserved tail for the safe-off, but no quota, so an
agent filling the store turns the fail-closed refusal against the person. The
design this implements (`embarch-doc/notes/hil/12-prevention.md`, item 3): the
call log has a quota, past it the agent's calls are refused first, and recovery
is the person's, freeing the store or raising the quota with the person's
token.

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction, and says the values are chosen, not measured; follow it,
and record any deviation in the decision):

- A quota in bytes, kept in the store, default 1 GiB.
- At 90 % of the quota, gated calls carrying the agent's token answer `503`
  naming the quota and the person's way to raise it; at 100 %, the person's
  calls too. The cancel route stays open, as under 158.
- The reserved tail (158) lies beyond the quota, so the safe-off can always be
  logged.
- `PUT /call-log/quota` with the person's token raises or lowers it; with the
  agent's token, `403`. The change is itself a call-log entry.
- `GET /call-log` reports the size and the quota.

**Not yours:** `embarch-api`, `embarch-ui` and every other repo (a client that
should send the new route is a follow-up for its own scope: say so in
`open.md`). You never touch hardware.

## Where to look

- `src/call_log.rs` — the 158 gate (`cannot_log`, `Gate::Refused`, the `Store`
  trait and its free-space check), `GET /call-log`
- `src/api.rs` — the router and the scope extractor (`Scope::Person`,
  `Scope::Agent`); `src/lease.rs` lists the lease-open routes
- `embarch-doc/embarch-core/decisions/call-log.md` (122, 156, 158),
  `interfaces/call-log.md`; `embarch-doc/notes/hil/12-prevention.md`,
  `notes/hil/14-implementation-plan.md`

## Where the doc goes

**`decisions/call-log.md` is 10,990 of 12,288 B, so a new decision will not fit
there:** write it in a new topic file (`decisions/call-log-quota.md` or
similar) with an index row, and point 158's text at it only if a short
reference fits. Take the next free number by scanning the headings, as
`DOC-CONVENTIONS.md` says, and cite only that number in code comments.
`interfaces/call-log.md` gives the route, the `503` and `403` bodies and the
`GET` fields. **Over or near the per-decision cap, do not grow:**
`signing#110`, `analog-capture#127`, `host-study#95`, `definitions#133`,
`lease#93`, `stopping-a-study#128`.

**Reserve:** `spec.md` is in reserve (9,082 of 10,240 B; out at 9,039 B or
less) and filed against `tasks/core/186`; do not grow it. `open.md` is 3,916 B,
3 B under its reserve line: its call-log line ends "Quota: EMB-329."; replace
that with what is still open, net-neutral or smaller. If your edit leaves
either file in reserve beyond what 186 already names, file
`tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md` has
the shape; number from `scripts/check-task-numbers.py --next core`).

## Done when

- [x] With a tiny quota, the agent's gated calls are refused at 90 % and the
      person's still served; at 100 % both are refused.
- [x] The safe-off's entries still land past the quota.
- [x] `PUT /call-log/quota` with the agent's token is `403`; with the person's
      it changes the quota and is logged.
- [x] Decision and `interfaces/call-log.md` written.
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
