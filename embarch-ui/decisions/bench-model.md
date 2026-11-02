# embarch-ui decisions: The bench editor's model

**Status:** active, 2026-11-01.

What a part is, what a cable may join, and what the checks say: phase 1 of [embarch-bench-editor-proposal.md](../../embarch-bench-editor-proposal.md); what the vocabulary serves an editor, phase 3's (88). The file a bench is saved in, how it is written and how it is applied: [saved-benches.md](saved-benches.md) (73–75). What the canvas draws from it: [bench-canvas.md](bench-canvas.md) (76–78). Editing it: [bench-editing.md](bench-editing.md) (80–86) and [part-editor.md](part-editor.md) (87).

Index: [../decisions.md](../decisions.md). Current truth: [../spec/bench.md](../spec/bench.md).

### 71 — A part is a template of physical connectors; the built-ins ship in the binary and a repo adds its own

**Three fixed boxes could draw no bench but the BLE one.** A USB PD bench is a DUT, a partner with a shield, an analyzer in line, a load and a supply, so a part became data: a template naming **the physical connectors a human would cable** (owner, 2026-11-01), each with a kind that decides what it joins and, on a `usb-host`, the functions it carries to this machine. **A template carries no serial** (44): which unit is on the bench is the bench's binding, never the kind of device's.

**Built-ins plus a repo's own** (owner): the built-ins are TOML embedded in the binary and served by the same route as `embarch/parts/<id>.toml`, so a repo can add a part without a release. The repo half is written through `POST`/`PUT /api/bench/parts`, from the part editor (87). **Each built-in's connector list comes from that part's manual or this suite's own docs**, and a comment says where the source stopped short ([../open/bench.md](../open/bench.md)). **The CY4500 is generic** (owner): two USB-C in line on one bus, a USB link to this machine that declares nothing, a plain case — not the CY4500-EPR's layout or colours.

**A repo template reusing a built-in's id is refused** (owner): `409` on a write, an `errors` entry on a read, never a silent override. A repo cannot redefine the CY4500 every other repo draws, and one id would otherwise mean two connector lists depending on which checkout is open.

**The vocabulary is served, and it is the parser's own list.** Every word list is one Rust enum whose serde spelling is the word, and `GET /api/bench/vocabulary` serves exactly its variants, so a repo template using a word this build does not know fails its parse and is listed with the line, never half-drawn. The browser restates none of it — the spec's rule for every vocabulary — and derives even "never cabled" from it: a kind in no `joins` pair that is not the hub's.

**This machine is a hub** (owner): it has no connectors of its own, and a hub template declaring one is refused. Every cable reaching it is a port, because Core finds a device by its USB serial and interface, never by the physical port it is in. So a `usb-host` joins a hub and only a hub, and a stack socket or plug is never cabled: a shield joins its board through `mounted_on`.

### 72 — The checks read the description, and a save refuses only what makes a file unreadable

**Every check is a pure function over the bench as written** — no file, no Core, no hardware — so a finding is a statement about the description, never about what is plugged in. `POST /api/bench/check` takes a bench and a config and answers findings, each a level, a code, a sentence and the parts and cables it names. `POST /api/bench/candidates` takes the end a cable is being laid from and answers a verdict for every other end — `ok`, `refused` with why, or `hidden` for another kind — so the browser decides nothing while wiring (81 draws them). **Rule checks are in the first version** (owner, 2026-11-01).

**Three levels.** An `error` is a refusal the file already breaks: `kind-mismatch`, `connector-full`, `cable-same-part`, `unknown-end`, `bench-cable-not-to-hub`, `hub-cable-in-config`, `role-twice`, `usb-identity-twice`, `two-providers`, `config-name-twice`, `bad-part-id`, `part-id-twice`, `mount-cycle`, `mount-unknown`, `mount-no-plug`, `mount-no-socket`, `mount-full`, `binding-bad-connector`, `binding-bad-function`. A `warn`: `template-missing`, `shield-unmounted`, `binding-unresolved`, `no-source`, `drp-cn3-empty` (the X-NUCLEO-DRP1M1 sources only what CN3 gives it, `embarch-dev-bench` decision 49), `no-probe-path`, `signal-no-path`. An `info`: `drp-cn2-empty`, since sinking with nothing on CN2 is a legitimate state. **Warnings stay warnings: the picture must match the wiring "including when the wiring is deliberately unusual"** (10).

**A save refuses neither.** It refuses only what would make the file unreadable or ambiguous to address — a cap, a part id that cannot name a cable end or names two parts, a `usb` key that is no connector, two configs under one name, a name that slugs to nothing — so a legacy file with a problem can still be rewritten, and the problem is a finding on screen rather than a save that will not happen.

**Configs change only part-to-part cables** (owner): a cable to this machine is bench-level, shared by every config, so one inside a config is an error, and so is a bench-level one that misses this machine.

**The paths are defined, not guessed.** A bus is the usb-c, banana and terminal connectors joined by cables and passthrough pairs: two providers (`source`, `supply`, `out`) on one are refused, two consumers with nothing sourcing it warned. A probe path is a part's own probe cabled to this machine, or an SWD lead to a part whose probe is. A signal path is any part-to-part cable or a `mounted_on` stack, **never this machine**: a USB host carries nothing between two devices. Two USB identities on different parts clash when they share a serial, or when one has no serial and a port matching it would match the other by VID, PID and interface.

**Bounded, so a hostile file cannot make one request expensive**: 500 parts, 2,000 cables at the bench level or in one config, 100 configs, 32 USB bindings on one part, 64 connectors in one template — `400` past any — and everything a rule looks up is indexed once per request.

### 88 — The vocabulary serves the rules between fields and a template's limits, each held to the parser by a test

Extends 71 for the part editor (87), which may restate nothing. Beside the word lists, `GET /api/bench/vocabulary` serves `sides`, `roles`, the kinds that take a power role (`power_kinds`) and the functions that take an interface or line facts (`interface_functions`, `line_functions`) — the same predicates `PartTemplate::check` applies, and a function belongs to the hub's kind by `HUB_KIND`, not a second literal — and under `template` the limits a file is held to: `max_connectors`, each number field's `{min, max}` from its integer type (`max_cables`'s floor from `MIN_MAX_CABLES`), and the line facts as `{name, numeric}`. **A test holds each to what a parse accepts**: every range's ends parse and one past either does not; every rule matches per kind and per function; and the served line facts and number fields are compared with the structs' own serde field lists, so a field added and not served fails `cargo test` rather than vanishing from every file the editor saves.
