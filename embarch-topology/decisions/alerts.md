# embarch-topology decisions: Alerts, and the UI that stopped existing

**Status:** active, 2026-09-02.

How a mismatch reaches a human, and the live-push mechanism that was retired.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 5 — A local web page served by this crate's own process, for the duration of one explicit run

Not a native app, not a TUI, not always-on. **A thin wrapper calling the same crate functions Core calls, so a human sees exactly what Core would compute, not a separate opinion.** Loopback-only by default: no TLS, no reason to expose past localhost.

**Retired outright** — [embarch-ui](../../embarch-ui/decisions.md)'s Topology tab covers the same ground now, over Core's own HTTP API, and **`embarch-ui` never links this crate at all.** The 413-line UI binary is deleted along with its subcommand; **every read-only function it called stays exactly where it was.** The HTTP dependencies went with it, since nothing left under that feature serves HTTP.

**The retirement surfaced a real orphan, which decision 19 then closed.** The live-push mechanism existed to reach *this* UI's own marker file and receiver, so with the binary gone it would **always silently find no marker — its designed-in fallback, unchanged — and the fix-it URL would always fall back to a port nothing serves any more.**

### 12 — Alert delivery is durable, and live-when-open; opening the UI and retrying are the caller's job

When the shared `validate()` catches a mismatch it **durably records it the instant it happens — nothing is lost to bad timing between the check and someone looking.** ~~And if the UI happened to be open, pushed it there instantly~~ — **the live-push half is retired (decision 19)**: the UI it pushed to no longer exists, and `embarch-ui` reaches the same durable log by polling Core. Whichever consumer called `validate()` gets back **a structured mismatch error carrying a fix-it URL**, and returns that same structured error to *its* caller unchanged.

**Opening or focusing the UI is deliberately not Core's job.** Core is typically a Windows service in Session 0 — the real primary deployment — or eventually a headless Pi with no desktop at all; **neither can reliably make a window appear on an interactive desktop.** Whatever is actually in the user's hands at the moment of failure opens the UI from the structured error, **since that tool runs in the user's own session with none of Core's platform restrictions.**

**Retry is just calling the operation again — no queue, no auto-resume.** `flash`, `reset` and `run_study` are already safely re-invocable.

**Revised**: the alert log, event stream and structured-error shape were originally scoped as three new surfaces **Core would have to build itself.** Under decision 2 they are crate-internal facilities instead.

### 19 — The live-push marker-file mechanism is retired; the fix-it URL becomes a plain deterministic `embarch-ui` URL

Both functions still *worked* exactly as designed — the push silently no-ops with no marker, the URL falls back to a default port — **and that is the problem: they were working-looking code whose live destination no longer existed anywhere in the suite**, and the URL now returned **a link guaranteed to be dead rather than one that is dead unless a human happened to start the UI.**

So the push and the marker dance go, and the URL **stays, reduced to what it can honestly be**: a deterministic link into `embarch-ui`'s Topology tab, no discovery, no marker. Alerts still land durably, and **the UI's existing five-second poll of Core's alert route is already the live path in practice and nobody has wanted it faster.**

*Rejected: restoring real push*, with `embarch-ui` writing the same marker and adding a receiver. **It adds an inbound loopback listener to the UI purely to beat a poll interval that has not been a complaint, and re-creates a discovery mechanism specifically so a second thing can rediscover what a fixed URL already knows.**

**It also lost its per-alert id, which is the part worth stating.** It used to point at a per-alert detail page **that only the deleted binary ever served**; `embarch-ui` has no such page, only the recent-alert list. **Keeping the id would have made the URL look more precise than the thing on the other end can act on.**

**One change fell outside this crate, and the decision as written did not anticipate it.** "A fixed URL into the Topology tab" **was not something a URL could express**: `embarch-ui` picked its tab from browser storage alone, so **every link landed on whichever tab that browser last had open.** It now reads a fragment first, with a listener so following the same link twice in an open tab still works. **Without that half, this fix would have been a *second* generation of the exact fault it exists to remove — a link that looks specific and isn't.**

**The honest limit, stated rather than papered over:** the host and port are duplicated constants, and `embarch-ui` honours overrides this crate cannot see. **Reading those env vars here would be worse than not** — they would be read in *this* process, usually Core's Windows service, **which has no reason to have them set and no way to learn what the UI process was actually started with.** A fixed URL that is wrong for a human who moved the UI's port **beats a discovery mechanism that is wrong for everyone.**
