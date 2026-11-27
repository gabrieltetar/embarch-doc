# 196 — every route that touches a board names it in the call log

**State:** open
**Source:** embarch-core/open.md — "The call log's `board` is named by four handlers only (`/flash`, `/reset`, the two live reads; 122): `/bootload`, `/validate`, exchange and capture leave it null."
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A call-log entry's `board` (`{role, probe_serial, chip, image_sha256}`,
decision 122) is filled only where a handler calls
`call_log::board_note().set(...)`: `/flash`, `/reset` and the two live reads.
When this is done, every gated route that acts on one board names it too:

- `POST /bootload` — the DUT role, its enrolled probe serial and chip, and
  the uploaded image's hash. Today it calls only `note.flashed(&chip)` (around
  `src/api.rs` line 1096), so the entry's `board` stays null.
- `POST /validate` — the role (or probe serial) it was asked about, and the
  chip once the enrolled row is read.
- `POST /signals/{name}/exchange` (and `POST /instruments/{name}/exchange`, if an instrument's
  route can name a board at all; if not, say so in the decision rather than
  inventing a shape) — the board the signal leaves from.
- `/signals/{name}/capture` (start, read, stop) — the board the captured signal
  belongs to.

Use the existing `board_note()` (`src/call_log.rs`, clone it into a
`spawn_blocking` closure as its doc comment says). Where a route cannot know
the board before it fails (an undeclared signal, an unknown role), the entry
keeps `board: null`, and the decision says which cases those are. Each route
gets a test in the style of the existing ones in `src/call_log.rs` (around line
1070) that reads back the entry and checks `board`.

Amend decision 122 in place (its "the two live reads today" clause) and the
`board` row of `interfaces/call-log.md`, and delete the open item from
`open.md`, or narrow it to whatever is still left.

**Size:** `decisions/call-log.md` is 10,986 B with its reserve line at about
11,059 B. Replace the "today" list with the rule rather than a longer list, so
the file does not grow into reserve; if it must, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.
`spec.md` sits 31 B under its reserve line; you should not need it.

**Not yours:** every other repo, `embarch-api`'s call-log reader included. No
wire schema bump: `board` already exists and is nullable. You never touch
hardware.

## Why now

The call log is the record of what an agent did to which board (decision 122),
and today a bootload, a validate, an exchange or a capture is recorded with no
board at all, which is the half of the record a reader needs most after a
board misbehaves.

## Where to look

- `src/call_log.rs` (`board_note`, `BoardNote::set` and `flashed`, the tests
  around line 1070)
- `src/api.rs`: `flash_handler` and `reset_handler` (around 832 and 1017, the
  shape to copy), `bootload_handler` (around 1043), `signal_exchange_handler`
  (around 1906), `instrument_exchange_handler` (around 2046), the capture
  handlers (around 2135 to 2210), `validate_handler` (around 2490), and the
  live-read handlers (around 2241 and 2290)
- `embarch-doc/embarch-core/decisions/call-log.md` (122),
  `interfaces/call-log.md` (the `board` row)

## Done when

- [ ] `/bootload`, `/validate`, the signal exchange and the capture routes
      fill `board` when the board is known, each with a test reading the entry
      back.
- [ ] Decision 122, `interfaces/call-log.md` and `open.md` say which routes
      name a board and which cases stay null.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`,
      `cargo clippy --workspace --all-targets -- -D warnings`);
      `changelog.d/` fragment.
