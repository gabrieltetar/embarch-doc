# milestone-6.md: changelog archive

Entries beyond the 8 most recent, moved here from [milestone-6.md](milestone-6.md)
by `scripts/archive-changelog.py`, per `DOC-PROTOCOL.md` §5. Newest-first,
same as the live doc's own Changelog.

- 2026-08-05 — §3.4's `init` done. Only `doctor` remains in §3.4, then §3.7 and §3.8.
- 2026-08-05 — §3.3 and §3.4's `up`/`down` done, with `locate.rs`/`state.rs` underneath them. Two refinements folded back into `design.md` decisions 3 and 4 (no `PATH` editing; opt-in foreground fallback). Remaining: §3.4's `init` and `doctor`, §3.7, §3.8.
- 2026-08-05 — §3.6 done: `embarch-core start`/`stop` shipped, unblocking `up`/`down`. Correction folded back into `design.md` §3 decision 7 and §10 — elevation is universal, not Windows-only. Remaining: §3.3, the rest of §3.4, §3.7, §3.8.
- 2026-08-05 — §3.5 done: `base_url = "auto"` shipped in `embarch-api`, `topology.rs` lifted verbatim with its tests intact, and the live stale-gateway-IP bug in the real config closed. Remaining: §3.3, the rest of §3.4, §3.6, §3.7, §3.8.
- 2026-08-05 — §3.2 done: topology detection implemented and verified against this machine and a mock, plus a partial §3.4 `status` so it isn't dead code. Two refinements and one new open item folded back into `design.md`. Remaining: §3.3, the rest of §3.4, §3.5, §3.6, §3.7, §3.8.
- 2026-08-05 — §5's shared-crate-vs-liftable-copy question resolved in favour of a liftable copy; §3.2 and §3.5 updated to say so, reasoning recorded as `design.md` §3 decision 15.
