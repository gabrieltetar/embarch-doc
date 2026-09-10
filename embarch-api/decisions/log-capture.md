# embarch-api decisions: What a build log keeps

**Status:** active, 2026-09-08.

What a truncated build log keeps, and how the drain that fills it reads a child stream.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The command this log comes from: [build.md](build.md).

### 18 — A truncated build log keeps the head *and* the tail
For a Zephyr build the **first** compiler error is usually the actionable one and everything after it is cascade, so an early failure followed by `cmake` and `ninja` grinding on can scroll the only useful line out of a tail-only cap entirely. What that produces — the split and its marker — is [spec.md](../spec.md) §3, with the numbers in §7.

**Written at the start and built 2026-09-04**, three months after `truncate_tail` shipped keeping the tail only — the gap [open.md](../open.md) carried as "an intent nobody built". It is built rather than retired, unlike decision 16, because nothing here was blocked on another repo: the whole cost is a second boundary walk. **Two calls this entry did not originally make:**

- **The cap bounds the retained bytes, not each half.** The marker sits on top of it exactly as the old one did, so this buys a head without doubling a response an MCP client has to carry. *Rejected: a cap per half* — one constant meaning two different things depending on whether a log overflowed.
- **The split is 1:3, and it is `[assumed]`** ([spec.md](../spec.md) §7). Nothing here has measured a real Zephyr failure's log; 16 KB is reasoned as far more than one diagnostic plus the Kconfig/`cmake` preamble it follows, while the tail keeps the failing recipe and the final summary a reader reaches for first. The **provenance is the load-bearing part**: if a real over-cap failure ever shows the first error past 16 KB, the number moves and this entry is where it says so.

**Both cuts must land on a UTF-8 boundary now, not one.** Slicing a `str` inside a codepoint panics, so a boundary walk is what stops a build log from taking the MCP server down rather than returning a truncated one — the head rounds **down** and the tail rounds **up**, which also makes "within the cap" hold by construction, since an adjustment can only ever drop bytes. The two constants are congruent differently (16384 ≡ 1 and 49152 ≡ 0, mod 3), so **a fixture of pure 3-byte characters exercises the head cut and not the tail one** — `tests/build_capture.rs` appends one ASCII byte specifically to shift the tail offset off a boundary. A both-ends test that does not actually straddle a character at both ends proves half of what it claims.

### 65 — The drain decodes per line, falling back to lossy decoding only for the failing line
`drain_stream` used to read lines via `next_line()`, which treats a non-UTF-8 byte as an error — and that error was read as EOF, silently dropping the rest of the log. **That is the defect this closes, not a polish**: a build failing past the bad byte would have gone entirely unreported. It now reads raw bytes with `read_until`, decoding each line as UTF-8 and falling back to `from_utf8_lossy` for only the one line that fails, naming the substitution in a marker so a reader can tell where the log was altered.

This is a decision about how the drain reads a child stream, upstream of and orthogonal to decision 18's truncation: it fires on every line the drain reads, whether or not the log ever nears `OUTPUT_CAP_BYTES`.

*Rejected: decoding the whole buffer lossily.* That would substitute replacement characters wherever they fall across the entire log rather than isolating the cost to the one line that actually failed to decode, leaving a reader no way to tell how much of the log was affected.
*Rejected: failing the build on bad bytes.* A non-UTF-8 byte in a child process's stdout or stderr is not evidence the build itself failed, and turning a decode failure into a build failure would report the wrong result for a reason that has nothing to do with the build.
