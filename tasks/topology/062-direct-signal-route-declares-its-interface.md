# 062 — A direct signal route on a multi-interface USB device resolves to a declared interface or refuses by name, never a silent guess

**State:** claimed by agent/topology/062-direct-signal-route-declares-its-interface, 2026-10-26 06:43
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-topology findings 1, 4 and 8), verified by Opus against embarch-topology@93a83d9c
**Scope:** topology
**Hardware:** none — `port::select` is pure over an enumerated port list, and every case below is a fixture of `SerialPortInfo` rows, which is how the existing `port.rs`/`signal.rs` tests are built. Nothing needs a board to finish. Whether a direct route on a two-interface device exists on this bench today is not known (`open.md`), and this task does not need it to.
**Owner:** no

## Supervisor note, 2026-10-26 06:12 leg — not dispatched, and why

"Breaks them on their next topology bump" (Two costs, below) understates it. `embarch-api` (through `embarch-core-client`), `embarch-core` and `embarch-ui` all path-depend on the `embarch-topology` checkout, so there is no bump: a field added to `Route::Direct` breaks `embarch-api` `src/tools.rs:1342` and `embarch-ui` `src/topology.rs` the moment it lands on `main`, and a new error variant breaks any exhaustive match in `embarch-core`. So the declared-interface half is a cross-repo change (protocol §8), not a worker's. The half that changes no public shape is a worker's: refuse an ambiguous declared-serial match by name with a reason other than "not enumerable", drop the `set-dev-bench-link` advice from the signal path, and stop treating two serial-less same-VID ports as one device. A dispatcher should either send a worker with that narrower scope and an explicit "change no pub type that `embarch-api`, `embarch-core` or `embarch-ui` construct or match", or split the declared-interface half into a `suite` task.

## Dispatch note, 2026-10-26 06:43 leg — dispatched with the narrower scope

**Your scope is the half that changes no public shape**, per the note above: (1) on the declared-serial path, a match on several ports is refused by name (each candidate port and its interface) instead of guessed, with a reason distinct from "not enumerable", and Core's exchange port wait must not spend its budget on it; (2) no message on a signal's resolution path recommends `set-dev-bench-link`; (3) two same-VID ports that both report no USB serial are not treated as one device, or a decision records why they are. **Change no public type that `embarch-api`, `embarch-core` or `embarch-ui` construct or match**: no new field on `Route::Direct`/`SignalRoute`, no new variant in an enum any of them matches exhaustively, no changed signature they call. A new public *type* (for example an ambiguity error distinct from `SignalMismatch`, so Core's `downcast_ref::<SignalMismatch>` wait does not catch it) is additive and allowed; grep all three consumers before relying on that, and name what you checked in your report. If (1) cannot be done without a breaking change, stop at what can and file the rest as a drop. **The declared interface on a direct route is out of scope** (a §8 cross-repo pass): leave its `Done when` box unticked and drop `/home/gabriel/Github/embarch/embarch-doc/inbox/suite-direct-route-declared-interface.md` for it, naming the consumer sites. If Core needs a change so the exchange wait stops on the new error, that is a separate `core` drop, as the task already says.

**Doc reserve in your scope:** `embarch-topology/decisions/enrollment.md` 12,122 / 12,288 B (**166 B left**), parked under `tasks/topology/060` (blocked, `In flux: yes` for that file). Do not write into it; decision 18 lives in `decisions/links.md`, which is not in reserve, and so does `link-declares.md` (9,676 B). If your work pushes any other file into reserve, file `tasks/topology/<NNN>-compact-topology.md` in the same commit.

## What

`Route::Direct` declares only `port_serial` (`src/hardware/signal.rs:111`), and its resolution goes through `Filter::for_declared_serial`, which sets `interface: None` (`src/hardware/port.rs:391-400`). A USB device that exposes several serial interfaces under one serial narrows to all of them. Decision 20 records one such device: the onboard J-Link with two VCOMs. A dual-UART bridge and a firmware with two CDC ACM instances are others. `select` then takes its guess branch (`port.rs:517-558`): it returns the lowest interface with `guessed_among` set, plus a WARN that tells the reader to run `set-dev-bench-link --interface`, which cannot touch a signal. None of Core's signal callers reads `guessed_among`: the outpost preflight (`embarch-core/src/outpost_preflight.rs:207`), the study capture (`study.rs:2588`) and the console exchange (`exchange.rs:138`). A capture or an exchange can therefore run on the wrong port with no report that a port was chosen. No declaration can correct it, unlike the dev-bench link (decision 20) and the bootload ports (decision 36).

Two smaller faults sit in the same path:
- `resolve_link_port` maps every `select` error, including the "ambiguous" refusal, to a `SignalMismatch` that says the port "is not enumerable now … returns once it re-enumerates" (`signal.rs:261-267`). Core's exchange waits on exactly that mismatch (`exchange.rs:135-150`), so an ambiguity is waited out as if the device were resetting.
- `select`'s one-probe test compares `serial_number` with `==` (`port.rs:518-520`). Two distinct same-VID devices that both report no serial therefore count as one probe and are guessed between rather than refused.

One possible direction, not the only one: give a direct route an optional declared interface, the way decision 36 did for bootload ports (`bootload.rs:26-43`). On the declared-serial path, refuse a match on several ports by name the way `bootload::find_in` does (`bootload.rs:129-157`) instead of guessing. Give that ambiguity a reason of its own.

Two costs to weigh:
- `embarch-api`'s `src/tools.rs:751` and `embarch-ui`'s `src/topology.rs:1291` build or destructure `Route::Direct { port_serial }` without `..` (through the `SignalRoute` alias), so a new field breaks them on their next topology bump.
- Requiring a serial for "one probe" turns a guess into a refusal for any single device whose interfaces report no serial. Check that against decision 20's reason for keeping the guess on the dev-bench path.

## Why now

The guess and the WARN advice are at `port.rs:517-558`; the dropped ambiguity is at `signal.rs:261`. A search of embarch-core finds no reader of `guessed_among`. This contradicts three docs:
- spec/storage-and-roles.md: "a caller reports 'COM16, guessed among 2' rather than 'COM16'".
- Decision 18 assumes that "the declared serial already identifies exactly one device". That is true for a device, but not for a port.
- Decision 37 names a DUT console on a direct route as the case exchanges exist for.

A wrong pick here looks exactly like decision 20's expensive failure, a link that accepts bytes and never answers. It now lands on the console path that agents drive.

## Done when

- [ ] Fixture tests over a two-interface device's port list: a direct route with a declared interface resolves to that interface. Without one, the route never reaches a Core caller as an ordinary port. Either it is refused with an error naming each candidate port and its interface plus the declaration that fixes it, or `guessed_among` is set and a follow-up drop makes every Core signal caller report it.
- [ ] An ambiguous declared serial is reported with a reason distinct from "not enumerable", and Core's exchange port wait does not spend its budget on it. If that needs a Core change, file it as a separate `core` drop. A port that is absent is still waited for.
- [ ] No message on a signal's resolution path recommends `set-dev-bench-link`.
- [ ] Two same-VID ports that both report no USB serial are not treated as one device (fixture test), or a decision records why they are.
- [ ] An `enrollment.toml` written before this change, with signal rows lacking any new key, loads and is written back without that key.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (decision 18 amended or a new decision for what a direct route declares and what a match on several ports does), `changelog.d/` fragment dropped. Follow-up drops are filed for `embarch-api` (the `declare_signal` tool and CLI) and `embarch-ui` (the declare form, `topology.rs:1291`) if the route's shape changed.
