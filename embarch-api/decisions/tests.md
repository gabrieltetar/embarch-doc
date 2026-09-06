# embarch-api decisions: How far the tests reach

**Status:** active, 2026-09-06.

The named smoke-harness tier that the live-run methodology became, the one-module `lib` target that lets the mocked suite reach anything at all, and where the bearer sweep's exhaustiveness comes from. Split out of [shape.md](shape.md) on 2026-09-06, verbatim: that file carried scope-and-boundaries and test-reach in one 12,281 B body against a 12,288 B cap.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Scope and boundaries: [shape.md](shape.md).

### 30 — A named smoke-harness tier, because the real methodology was unnamed
**Every real bug found in this project to date came from a live run** against a real Core or a real repo, not from the still-unwritten unit-test suite. That is a real, working methodology, just an unnamed and unrepeatable one. So it gets a name and a script: a throwaway Core instance plus a synthetic fixture repo, re-running a fixed sequence of calls. Not a substitute for the mocked unit tests, which remain the acceptance criteria below the process boundary.

### 46 — A one-module `lib` target, so the mocked suite can reach anything at all
`open.md` carried six recorded acceptance criteria as "specified and unwritten" for weeks. Three of them — the two-pipe drain invariant, truncation on a UTF-8 character boundary, an untouched artifact not counting as fresh — are properties of `build.rs`, and `build.rs` lived in a **binary** crate. Each file under `tests/` compiles as its own crate and can reach a package's `lib` and nothing else, so those three were not merely untested, they were **untestable from an integration test**. The suite was unwritten partly because writing it was blocked and nobody had said so.

`build` therefore moves behind a `lib` target and `main.rs` imports it rather than declaring it a second time — one compiled copy, exercised by the bin and the tests alike. Deliberately **one module wide**: the rest of `main.rs` stays where it is. A whole-crate lib/bin split would have meant moving `Cli`/`Commands`/`TargetSelection` too, which is a refactor of the front end bought for nothing the tests need.

The other three criteria are properties of `CoreClient`, and their tests live in **`embarch-api/tests/`, not `crates/embarch-core-client/tests/`**, deliberately: the core-client crate is a plain path dependency rather than a workspace member, so `cargo test` at the repo root — the command the gate runs and the only one anybody types — would never execute them there.

The mock Core is **hand-rolled on `tokio::net`, not `wiremock`/`httpmock`**. Two of the three invariants cannot be expressed against a well-behaved mock anyway: per-endpoint timeout independence needs a socket that accepts and then goes silent, and the plain-text-on-non-2xx rule needs a response that is deliberately not JSON. Both are a few dozen lines against a dependency this crate already has. **The suite adds no dependency at all**, dev- or otherwise.

Six mutations — one per criterion, each reverted — confirmed every test goes red when its invariant is broken. Two limits worth stating: the four end-to-end tests need a POSIX shell and are `#[cfg(unix)]`, so **Windows runs the direct tests only and covers the two-pipe invariant not at all**, and the bearer sweep's exhaustiveness was a comment rather than a mechanism, which decision 54 below closes.

### 54 — The bearer sweep's exhaustiveness is derived from the source
Decision 46 shipped recording its own gap: an endpoint added without `.bearer_auth(…)` was caught only if the sweep was extended to call it. **A comment describing a gap is not a mechanism that closes one**, and this one had already fired twice — `post_study` and `open_study_events` both reach the network and neither was swept. The second escapes such a list by construction: the one route that bypasses `send`, building its request through a `pub(crate)` `http()` accessor because it streams a body and sets no timeout.

So it is derived. `the_sweep_calls_every_networked_method` reads the client's source, taking the method enclosing every `self.client.<verb>(…)`/`self.http().<verb>(…)` call site as the networked surface — a private builder (`get_study_csv`) expanding to its public callers — reads the sweep's own `client.<method>(…)` calls the same way, and requires the two sets to match. **There is no list**: the sweep's real calls are the declaration. Verified by mutation per decision 46's standard: an unauthenticated networked method turns the new test red naming it, and adding the call it demands turns the sweep red on the missing header.

*Rejected: coverage-by-observation*, diffing the `(METHOD, path)` pairs the mock recorded against a route inventory the client exposes. Cheaper, but only as exhaustive as the inventory — the hand-kept list renamed — and it makes the client grow a public route table nothing wants.

**Not covered.** A lexical scan is not a Rust parse, so a request born some third way is invisible; the two that exist are asserted shut instead — one `reqwest::Client` in the crate, and `http()` only ever used to build a request in the same expression. Whether a call carries the token stays the sweep's job, and its `(METHOD, path)` list is still hand-written — now pinned **both** ways, so a call added without its route fails rather than passing quietly.

**Amended 2026-09-06.** The sweep proved the header on all 25 routes and, doing so, found that 9 of them applied it by hand — so it was auditing a convention, not observing a mechanism. [Decision 55](core-link.md) folded those nine into one funnel and added the structural guard beside this one; the sweep is unchanged and now measures what the funnel emits.
