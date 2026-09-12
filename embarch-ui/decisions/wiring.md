# embarch-ui decisions: Backend wiring and real-time

**Status:** active, 2026-09-02.

Every hardware-adjacent call goes over HTTP to Core, and everything live is SSE.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 5 — Every hardware-adjacent call, read or write, goes over HTTP+Bearer to `embarch-core`

`embarch-ui` **never links `embarch-topology`'s hardware feature at all.** It depends on `embarch-study-designer` as a library and calls it in-process, but only for pure offline authoring logic that touches nothing but the firmware repo being edited: the merged action list, the custom-action registry, and turning table rows into a study. Everything involving a physical board or Core's own storage — probe and board enumeration, alert history, port detection, enrolling, running a study — goes through `embarch-core-client`.

**Originally split along a mutation/read-only line instead; reversed the same day**, prompted directly: "Instead of having the UI access hardware, can the UI use the Core to access it?" The original framing put only *mutating* operations behind Core, reasoning that reads were safe in-process because they do not race Core's hardware lock. **That reasoning missed a worse failure mode the lock framing never covered:** those reads still touch live USB enumeration or a local file **on whichever machine calls them** — correct only when `embarch-ui` happens to run on the same machine as Core, and **silently wrong the instant Core runs elsewhere**, giving missing probes and an empty enrollment file. That is a supported topology class and **the whole reason `embarch-topology` exists.** It is also the exact reasoning decision 7 already used to keep the Debug tab from reading Core's logfile — which turns out to apply to every hardware-adjacent read, not just logs. The rule `embarch-api` already follows and never violated now applies here identically, **verified with `cargo tree -e normal`: neither `probe-rs` nor `serialport` appears anywhere in the dependency graph.**

This still preserves the invariant `embarch-topology` decision 14 established when Core's own enroll page was built: **a second process calling a hardware-mutating function directly, without sharing Core's lock, is a real class of bug.**

**How it reaches that HTTP path: a shared library, not a duplicated client.** `embarch-api`'s Core client, plus the config and token-resolution chain it depends on, is extracted into `embarch-core-client` that both depend on — the same "one implementation, many call sites" shape, rather than **growing `embarch-ui` its own client and reintroducing the mirrored-copy risk that precedent exists to eliminate.** Doing it closed a real gap: the enrolled-probes and dev-bench-port reads **had no client wrapper in either crate** until this UI's Dashboard and Topology tabs needed one.

### 6 — SSE everywhere, not the mixed SSE/polling split the two source UIs have

`embarch-topology`'s UI already pushed alerts live over a broadcast-backed SSE endpoint; `embarch-study-designer`'s polled a JSON status endpoint once a second. Every section here updates by push — the Dashboard's study and alert cards, Topology's board list, the run log, and the Debug tab's live tail — with **no client-side interval polling anywhere.**

### 24 — A static id guard over `index.html` and `app.js`, not another rendered check

`tests/element_ids.rs` parses `assets/index.html` and `assets/app.js` (both `include_str!`-embedded) as text and asserts two things: no element id is declared twice, and every id looked up via `getElementById`/`sdEl`/`trEl`/`sigEl` is declared somewhere. It is a regression guard, not a live-defect finder — `embarch-ui/decisions/trace-chart.md` decision 10 (the Load button and the load table body once sharing an id, so the table never rendered while every Rust test passed) is the defect shape it exists to catch on the next occurrence, without needing a rendered check to see it.

**Id universe is the union of both assets, not `index.html` alone**: `app.js` builds three ids of its own (`tr-gap`, `tr-cross`, `tr-delay`, the trace chart's SVG pattern fills), and those count as declared for the duplicate check exactly like an `index.html` id would, so a collision between a dynamically-built id and a static one is still caught. They are never looked up via `getElementById`, so they cannot register as dangling.

**The parser resolves only a literal string argument**, so `sdEl`/`trEl`/`sigEl` (three one-line `getElementById` wrappers; `sigEl` is the same shape as the task-named `sdEl`/`trEl` pair) are seen through wherever the id is written at the call site, but a handful of `sd-req-*` requirement-field lookups that pass a variable instead are not traced back to their literal source — a known, disclosed gap in the test's own module doc, not a silent one.

### 26 — Core being unreachable is an expected, renderable state, not an error to surface as a crash

Every call decision 5 routes over HTTP+Bearer can fail because Core is not running, not reachable
from this machine, or not yet answering — and that failure is treated as ordinary, not exceptional.
`snapshot.rs::poll` runs its six Core calls independently (`tokio::join!`, no short-circuiting) and
folds a failed `status()` into `Snapshot::core_reachable = false` plus a human-readable `error`
string, the same shape `Snapshot::pending()` uses before the first poll ever completes. Nothing
downstream treats that as a panic, a 5xx, or a hidden log line: `core_reachable` is the one flag the
Dashboard tab reads to decide whether to render "Core unreachable" instead of live data, and it is
the only place that state is shown to a human at all.

`logs.rs::poll_loop` follows the same rule for a different call: a failed `logs_recent` poll is
logged once at `debug` level and the loop keeps ticking — it does **not** push an error onto the
client-visible SSE stream, and does **not** duplicate the Dashboard's own reachability signal. The
Debug tab simply keeps showing whatever it last had; `core_reachable` stays the single place this
information surfaces.

**What renders, and what does not:** a down Core renders as `core_reachable: false` plus one
human-readable cause on the Dashboard, and causes no other tab to show an error of its own — logs,
snapshot fields other than the ones above, and the trace/study views all either hold their last
good value or render their own independent empty/pending state. It never renders as a crash, a panic
screen, or a raw exception string outside that one field.

**Why this is a decision and not incidental error handling:** the `tokio::join!` shape in
`snapshot.rs` deliberately fails each call independently so one Core-down moment does not blank
fields that would otherwise still resolve; `Snapshot::pending()` exists specifically to give the same
shape a name before the first poll; and `logs.rs` explicitly withholds a second, redundant error
surface in favor of the one flag. Three separate places construct the same "down Core is data, not
an exception" shape on purpose — that is a standing design position, not a comment that happens to
describe what an unhandled `Result::Err` did.
