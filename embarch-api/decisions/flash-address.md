# embarch-api decisions: The flash offset a `bin` needs

**Status:** active, 2026-09-05.

The one address a `bin` artifact needs, and why it is config rather than a call parameter.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The command this address flashes: [build.md](build.md).

### 42 — `base_address` is a per-project config field, not a per-call parameter
A `bin` artifact carries no address, so flashing one needs an offset, and this crate had no way to supply it. **The consequence was concrete rather than theoretical:** a validation flashed via a hand-written call straight to Core, bypassing this crate entirely for that step, because there was no config-driven path through it.

It wins the same argument `flash_format` already won: the offset is a fact about how the project builds, not something varying call to call, so **an agent should never have to know a hex number to flash a board**. *Rejected: a per-call parameter, and a config-default-with-override.* The override shape has a real precedent here — `--firmware-path` overrides the configured artifact — but that flag exists to flash *something other than what the project builds*, which is a genuinely per-call intent. An offset is not.

Opaque pass-through, like chip and format: this crate does not validate it against the target's memory map. Two shape details that were not free choices: the field is a **TOML integer** using TOML's own hex literal while Core takes a hex-or-decimal *string*, so the round trip lands a config-driven flash on byte-identical wire form to a dev-bench flash; and **a `bin` project that omits it is not a config-load failure**, despite being wrong in practice, because enforcing it is one step from validating the offset itself.
