# 027 — Decision 55 rejects `default_headers` on a reason that does not hold, and the funnel guard has three blind spots

**State:** open
**Source:** `api/022`'s reviewer, 2026-09-06, verifying decision 55 from source. It found all of this and left the filing to me; I filed rather than fixed because `decisions/core-link.md` has 22 bytes.
**Scope:** api
**Hardware:** none. Two sentences of decision text, one test file, no board and no live Core.
**Owner:** no

## What

Three findings from one review, all in `crates/embarch-core-client` and its decision record.

### 1. Decision 55's second rejection reason is false, and `026` will preserve it

Decision 55 rejects `default_headers` on the `reqwest::ClientBuilder` on two grounds. The first
holds prospectively: `http()` hands the client handle out, so "every request the `reqwest::Client`
makes" and "every request this client's *routes* make" are not the same set **once anything else
is built on that handle**. Today `http()` has exactly one call site and that site goes through
`dispatch`, so the two sets are identical — the code comment hedges this correctly and the
decision text does not.

The second does not hold at all. Decision 55 says a builder default would leave
`api/020`'s sweep nothing per-route to assert. **It would not.**
`every_outbound_call_carries_the_bearer_token` asserts `request.header("authorization")` **on the
wire at `MockCore`**. Under `default_headers` the header is on the wire identically, and the
sweep would pass and fail exactly as it does now. The code comment's narrower phrasing —
"invisible at every call site" — is defensible; the decision's compressed form is not.

**This is urgent in a way it does not look.** `tasks/api/026-compact-api.md` lists this rejection
under `Must not delete:`, so a verbatim split of `core-link.md` carries the wrong sentence
forward into a new file, where it reads as freshly asserted. Fix the sentence before, or as part
of, whatever runs `026`.

Note also that `api/020`'s reviewer and `tasks/api/022` **both** stated a *third* reason that is
also false — that `base_url = "auto"` probing would leak the token to a non-Core host. Probing is
`embarch_topology::software::resolve_software_topology`, which builds its own `reqwest` client
(`embarch-topology/src/software.rs:286-289`); `CoreClient`'s client is used only after
`base_url()` resolves and never touches a candidate. `api/022`'s worker established that and
correctly kept it out of decision 55. Do not put it back.

### 2. The funnel guard is weaker than decision 55 reads

`every_outbound_request_is_sent_through_the_one_funnel` is a lexical scan and says so in its own
"What this does not cover" paragraph, so this is not a contradiction — but two decision texts read
stronger than the test delivers. Three shapes put an unauthenticated request on the wire with all
three tests green:

- **`reqwest::get(url)`** inside a public method. No `.send()`, no `.execute(`, and no
  `reqwest::Client::builder(` / `::new(` in source, so it defeats the funnel guard **and**
  decision 54's "one `reqwest::Client` in the crate" assertion. Pre-existing.
- **Any function *named* `dispatch`.** The guard matches the funnel by enclosing-function name
  only — `site.ends_with("(in \`dispatch\`)")` — not by file, module or type. A free
  `async fn dispatch(client: &reqwest::Client, url: String)` that sends unauthenticated is
  licensed by the guard. **New with `api/022`**, and the cheap fix is to match on file *and*
  function, or to assert `client.rs` as the funnel's file.
- **Any file in a subdirectory of `src/`.** `client_sources()` uses non-recursive
  `std::fs::read_dir(CLIENT_SRC)`, so a route in `src/routes/mod.rs` is invisible to both scans.
  Pre-existing.

### 3. Nothing tests that the SSE subscription gets no request timeout

`open_study_events` passes `dispatch(_, None)`, and decisions 48 and 49 depend on no `reqwest`
per-request timeout reaching the stream — one covers the body, so a healthy stream would be cut
off. The reviewer mutated that call site to `Some(Duration::from_millis(500))` and then
`Some(Duration::from_secs(30))`; **all 16 tests in `tests/study_events_sse.rs` passed under both.**

The property was equally untested before `api/022`, but it used to be an absent line and is now a
wrong argument away — **the cheapest regression in that diff**, and one that would surface only
against a real Core, which nothing in this suite has run. A test that holds a slow mock stream
open past 500 ms and asserts it survives would close it.

## Why now

Finding 1 has a deadline that is not obvious: `026`'s `Must not delete:` list is what a future
compactor obeys, and it currently instructs one to preserve a sentence known to be wrong. Findings
2 and 3 are cheap and are in the file a future unit will already have open.

## Done when

- [ ] Decision 55's `default_headers` rejection states only reasons that hold, and says which of
      them is prospective rather than current. Net bytes matter — see the reserve note below.
- [ ] `tasks/api/026`'s `Must not delete:` entry for that rejection is updated in the same commit,
      so a verbatim split cannot carry the old text.
- [ ] The funnel guard matches the funnel by file and function rather than by name alone, and its
      "What this does not cover" paragraph names the `reqwest::get` and subdirectory shapes
      explicitly — **or** the scan is widened to catch them and the paragraph shortened. Argue the
      choice; widening a lexical scan has its own cost.
- [ ] A test asserting `open_study_events` survives past any timeout a mutation would introduce,
      or a written statement of why that cannot be tested without a real Core.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Doc-size reserve for `api` — read this before you plan

**`embarch-api/decisions/core-link.md` is at 12,266 B against a 12,288 B hard cap. You have 22
bytes.** `tasks/api/026-compact-api.md` is filed against it, `blocked` on `In flux: yes`
(`tasks/api/001-sse-client.md` — decisions 48/49 have never met a real Core).

A blocked compaction task parks the *pass*, not the reserve. `026` names the move that is **not**
blocked and that you should take: a **verbatim split** of the event-stream half out of
`core-link.md`, the way `api/023` split `shape.md` — a split moves entries unchanged, so
`DOC-COMPACTION.md` §2's in-flux objection does not apply to it. Do that first, then write.
Editing a moved entry means you have wandered into the parked pass; do not.

Finding 1 is a *rewrite* of two clauses, so aim to come out net shorter. `decisions/tests.md` is
the roomy file (5,434 B) and is the right home for anything about finding 2 or 3 — those are about
how far the tests reach, which is that file's mission. Finding 1 belongs in `core-link.md`, which
is why the split comes first.
