# Build decision 14's `503` on `hw_lock` contention, or retire the decision

**State:** open
**Source:** `core/007` bench measurement, 2026-09-06 — three concurrent `/serial-log` calls all returned `200`, serialised, with no refusal and no holder named
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core` decision 14 says a second hardware request meeting a held `hw_lock` is refused with
`503` **naming the holder**, and gives the reason: without it "the second caller used to block
silently on the mutex, indistinguishable from Core being unresponsive". `spec.md` §2 and
`interfaces.md`'s status vocabulary both stated it as shipped.

**It was never built.** Every hardware handler is `state.hw_lock.lock().await` on a
`tokio::sync::Mutex`; `src/` contains no `try_lock`, no `503` and no `SERVICE_UNAVAILABLE` — in the
git checkout *and* in the rsync tree the Windows service is built from. Contention queues, with no
deadline and no message, which is the behaviour the decision named as the problem.

Decide one way and make the corpus say it:

- **Build it** — `try_lock` (or a short `timeout` on the acquire, which is friendlier to the common
  case of a 200 ms flash) and return `503` with a body naming what holds the lock. That needs
  `hw_lock` to carry *who* holds it, so `Arc<Mutex<()>>` becomes `Arc<Mutex<Option<HolderInfo>>>`
  or similar; the holder string is the whole point and a `503` without one is not decision 14.
- **Or retire decision 14** per `../../DOC-CONVENTIONS.md`, keeping the number, and say plainly that
  Core queues — which is a defensible design for a single-operator bench, and would then need
  `embarch-api`'s client timeouts documented as the *real* contention behaviour a caller sees.

Do **not** leave it as it is now, where three docs described a refusal and the code queued.

## Why now

The real behaviour — an unbounded silent wait, with no message and no deadline — is the one thing
an unattended agent cannot tell apart from Core being hung, which is exactly the reason decision 14
gives for existing. `tasks/core/009` compounds it: an unbounded `duration_ms` stalls every other
hardware caller for its whole span, and nothing tells them why.

Note for whoever picks this up: the fleet protocol's own "a `409` is a refusal, not a bug in your
change" instruction is about the **`study_lock`**, which Core genuinely does emit a `409` for
(`study.rs:869`, `:928`). It is not about `hw_lock` and it is not evidence either way here.

## Done when

- [ ] Either the `503`-naming-the-holder path exists with a test that observes it under real
      contention, or decision 14 is retired with a tombstone naming what replaced it.
- [ ] `spec.md` §2, `interfaces.md`'s status-code conventions and `decisions/platform.md` all say
      the same thing, and it is the thing the code does.
- [ ] If it is built: a caller that waits and a caller that is refused are distinguishable in
      `core.log`, so a stall can be diagnosed after the fact.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
