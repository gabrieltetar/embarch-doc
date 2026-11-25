# embarch-core decisions: The bench lease

**Status:** active, 2026-10-26.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). HTTP surface: [../interfaces/hardware.md](../interfaces/hardware.md). Siblings: [platform.md](platform.md) (decisions 4, 14, 15: `hw_lock`, which this sits above), [signal-capture.md](signal-capture.md) (decision 92).

### 93 — `/lease`: one session holds the whole bench across calls, and a hardware request without its token is refused `409` by name

`hw_lock` serialises single requests only, but a session's work is a sequence: between two calls another session can flash its own image, and every later reply silently describes the wrong firmware. The field's `mkdir` lock directory (two sessions, one DUT, one bench board, from 2026-10-08) saw 62 holds by 8 sessions, one collision, and a reflash after every take, since nobody knew what the other left; it held only while every session remembered it, and never saw `embarch-atlas`'s live tool calls.

**The shape** ([interfaces](../interfaces/hardware.md)): `POST /lease` returns a token, once; `PUT` renews (its own TTL if `ttl_s` is omitted) and `DELETE` releases, both with it in `X-Embarch-Lease`. A second `POST` while one is live is `409` naming the first. The holder is the name a caller gives, never the token scope (decision 109).

**The whole bench, not one board.** Field sessions always used both boards; a per-board lease needs a board vocabulary Core lacks (a chip is not a role, a signal is neither), and two leases bring a lock-order problem for nothing. Leasing one board is a new decision.

**While a lease is live, a gated route without its token is `409`**, plain text, naming holder, purpose, start and expiry; with none live nothing changes. Middleware in `auth_middleware`, keyed on the registered path pattern: no handler changes. `lease::LEASE_GATED`: `/flash`, `/reset`, `/bootload`, `PUT`/`DELETE /bootload/ports`, `/serial-log`, `/dev-bench/hello`, `/probes/enroll`, the three enrollment writers, `/dev-bench/link`, `POST`/`DELETE /signals*` (registry writes: they take `hw_lock` and change what an exchange reaches), `/signals/{name}/exchange`, `/live/mem-read`, `/validate` and `POST /study`. All else (`lease::LEASE_OPEN`) is reads, a capture's or study's `GET` included, and `/lease`. **A test puts every route in exactly one list**, so a new route cannot skip the question.

**Capture start and stop are gated; reading is not.** `POST /signals/{name}/capture` records the DUT for up to 600 s, so an unleased session could start one the holder never asked for, and `POST /bootload` is then refused by name against its port; `DELETE` ends the holder's recording. The lease gates only who starts the sequence: decision 92's capture still takes no `hw_lock`, and outlives its lease (bounded by `max_s`). `GET .../capture` stays open: it returns held bytes and moves no board.

**A study in flight refuses every gated call but its cancel**, the lease's token too ([95](host-study.md), `core/143`); a lease taken mid-study succeeds and does not stop it.

**Expiry is lazy**: no timer, live iff `now < expires` at each check, so a crashed holder frees the bench at its TTL with no sweep to fail. `ttl_s` is `1..=14400` (four hours), else `400`. **[assumed]**: the cap is reasoned from the field's longest hold, 1.4 h (6.3 h across 62 holds), not measured. In memory: a Core restart frees the bench (the safe direction); the holder sees `404` on its next renew.

**`GET /status` adds `lease` and `last_images`**: per chip, the last image Core flashed or bootloaded, recorded only on success in `flashed-images.jsonl` with its load segments, scope and call-log entry ([interfaces](../interfaces/hardware.md)), so a restart keeps it. `sha256` hashes the bytes read just before flashing; `path` is `(uploaded)` for a multipart flash, `(bootload image)` for `POST /bootload`. **An absent entry means unknown, not "nothing flashed"**: another tool's flash never appears, and an old entry is what Core flashed, not what the chip holds (decision 12). A session taking the bench compares `sha256` with its image to decide on a reflash.

**An idle lease is released too** (decision 123, [lease-idle.md](lease-idle.md)): 30 min with no hardware call. **2026-11-25:** the lease holds the serial ports ([port-hold.md](port-hold.md), 130). **2026-11-25:** a Test run's go moves it to the run ([test-run-go.md](test-run-go.md), 135).

**The client half is `embarch-api`'s** (inbox drop, `tasks/core/099`): the token rides an environment variable so `embarch-atlas`'s live calls inherit it.
