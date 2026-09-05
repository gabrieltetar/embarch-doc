# embarch-api decisions: Running a build and what it produces

**Status:** active, 2026-09-05.

The generic per-project command, what its log keeps when it fails, where its output lands, and the one address a `bin` needs.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). What gets built — the Zephyr exception decision 5 scopes — is [zephyr.md](zephyr.md).

### 5 — A generic configurable command per project, not toolchain-specific logic
Originally motivated by an assumption that the two day-one projects used different toolchains. On inspection **both turned out to be Zephyr/west-based** — one reads as an Arduino board by name and its own `board.yml` confirms otherwise, confirmed by reading the real repo rather than assuming from the name. The generic design is kept regardless: it is the right call on its own merits, even though the two-toolchain premise did not hold.

### 18 — A truncated build log keeps the head *and* the tail
For a Zephyr build the **first** compiler error is usually the actionable one and everything after it is cascade, so an early failure followed by `cmake` and `ninja` grinding on can scroll the only useful line out of a tail-only cap entirely. What that produces — the split, the marker and the byte counts — is [spec.md](../spec.md) §3, with the number itself in §7.

**Written at the start and built 2026-09-04**, three months after `truncate_tail` shipped keeping the tail only — the gap [open.md](../open.md) carried as "an intent nobody built". It is built rather than retired, unlike decision 16, because nothing here was blocked on another repo: the whole cost is a second boundary walk. **Two calls this entry did not originally make:**

- **The cap bounds the retained bytes, not each half.** The marker sits on top of it exactly as the old one did, so this buys a head without doubling a response an MCP client has to carry. *Rejected: a cap per half* — one constant meaning two different things depending on whether a log overflowed.
- **The split is 1:3, and it is `[assumed]`** ([spec.md](../spec.md) §7). Nothing here has measured a real Zephyr failure's log; 16 KB is reasoned as far more than one diagnostic plus the Kconfig/`cmake` preamble it follows, while the tail keeps the failing recipe and the final summary a reader reaches for first. The **provenance is the load-bearing part**: if a real over-cap failure ever shows the first error past 16 KB, the number moves and this entry is where it says so.

**Both cuts must land on a UTF-8 boundary now, not one.** Slicing a `str` inside a codepoint panics, so a boundary walk is what stops a build log from taking the MCP server down rather than returning a truncated one — the head rounds **down** and the tail rounds **up**, which also makes "within the cap" hold by construction, since an adjustment can only ever drop bytes. The two constants are congruent differently (16384 ≡ 1 and 49152 ≡ 0, mod 3), so **a fixture of pure 3-byte characters exercises the head cut and not the tail one** — `tests/build_capture.rs` appends one ASCII byte specifically to shift the tail offset off a boundary. A both-ends test that does not actually straddle a character at both ends proves half of what it claims.

### 19 — A readable build-dir prefix, and a `target.json` beside the output
`extra_args` folds into the directory name via a hash, since an arbitrary flag can contain directory-unsafe characters — but **a bare hash makes a directory listing undebuggable to a human staring at it**. Two additions without touching the hash: every other axis spelled out ahead of it, and a `target.json` recording the full resolved selection, so `cat target.json` recovers exactly what produced that directory.

**The file is written as of 2026-09-05, and was stated as current truth for three months before that** — [../interfaces/config.md](../interfaces/config.md) described it as behaviour while a `target.json` grep over the whole crate matched nothing but the docs. Built rather than retired because something else was already deferred on it: [`embarch-umbrella` decisions](../../embarch-umbrella/decisions/projects.md) 26 has no other sound per-directory evidence of *which* target produced a directory, the name being unparseable back into one — board, app and snippet names all contain `-`. Three calls the entry above did not make:

- **The file is the descriptor value itself**, the same `serde_json::Value` a tool response echoes back, not a second serialization of the same facts — so a directory's provenance and the answer its caller was given cannot drift apart. It goes out through `json_out` like every other JSON object this crate emits, so it carries `schema_version` (decision 50) rather than becoming the one machine-read shape without it — and this file is read by a *different repo*, which is the case that promise was made for. *Rejected: a version counter of its own.*
- **Written after the build command, only into a directory that already exists, and it never creates one.** A manifest beside a directory no build produced is manufactured evidence, not evidence; and writing *before* the build would put this crate's correctness in front of `west build -d`'s, to gain a provenance file. A **failed** build's directory gets one too — that is the listing entry a reader most needs explained.
- **Absence means "unattributable", never "orphaned", and the write is best-effort.** Every directory built before this shipped has no `target.json`, so a consumer reading absence as "no valid target claims this" would delete exactly the directories it has no evidence about. That rule is also what makes losing the file to a write error the right trade against failing a build that would otherwise have succeeded. Only a `zephyr-west` target gets one: a `static` project resolves no selection (decision 51) and dev-bench builds into west's default `build/`.

### 42 — `base_address` is a per-project config field, not a per-call parameter
A `bin` artifact carries no address, so flashing one needs an offset, and this crate had no way to supply it. **The consequence was concrete rather than theoretical:** a validation flashed via a hand-written call straight to Core, bypassing this crate entirely for that step, because there was no config-driven path through it.

It wins the same argument `flash_format` already won: the offset is a fact about how the project builds, not something varying call to call, so **an agent should never have to know a hex number to flash a board**. *Rejected: a per-call parameter, and a config-default-with-override.* The override shape has a real precedent here — `--firmware-path` overrides the configured artifact — but that flag exists to flash *something other than what the project builds*, which is a genuinely per-call intent. An offset is not.

Opaque pass-through, like chip and format: this crate does not validate it against the target's memory map. Two shape details that were not free choices: the field is a **TOML integer** using TOML's own hex literal while Core takes a hex-or-decimal *string*, so the round trip lands a config-driven flash on byte-identical wire form to a dev-bench flash; and **a `bin` project that omits it is not a config-load failure**, despite being wrong in practice, because enforcing it is one step from validating the offset itself.

