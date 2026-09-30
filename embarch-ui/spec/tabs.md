# embarch-ui: the five tabs

**Status:** active, 2026-09-29.

Split verbatim from [../spec.md](../spec.md) (`tasks/ui/069`), when decision 44's roles/topology growth put that file back over its cap. Nothing below is reworded from the version that moved. What each tab does. Current truth: [../spec.md](../spec.md).

One persistent left sidebar, one top status bar, client-side navigation by URL fragment (`#topology`, `#live-study`). **The open project is shell furniture, at the foot of the sidebar** (46): one firmware repo at a time, named there on every tab and changed from a dialog the Study Designer's own card also opens. A fragment names a tab and nothing else (31). **A retired fragment resolves to the tab that absorbed it**, never to the last one that browser had open: `#enroll` is `#topology` (43).

| Tab | What it does |
|---|---|
| **Dashboard** | Active study and alert cards, live |
| **Topology** | One diagram carrying both of a role's bindings (45): its **board type**, clicked to pick — as one **real scanned combination** of revision and variant (47) — and its **probe**, dropped on (43). Plus **signal routing** (the one human surface for declaring a wire), the project's **board-type catalog**, **saved benches**, and **Validate topology**, which replaced the alert list (44) |
| **Study Designer** | **Authoring and saving** a study; running it is Live Study's (31). Four panels (41): **project**, whose only field is the repo path (51), with the **Static firmware analysis** submenu that runs the GATT extractor — one ships, so there is a button and nothing to configure; the **study toolbar**, whose **Build options…** dialog holds the two `requires` fields, the dev-bench log level and the **Build card**; **steps**; and **Define the wire** — taps, `.eap` manifests and editor, the action registry, layouts. The Build card (38): app, an **ordered** snippet list, west flags and a three-state outpost mode per header flag — off by default, unavailable-with-a-reason off a configured project |
| **Live Study** | Runs a saved study and watches it land, or opens a past one and reads it back. Stacked cards: run/open with the studies list, the **build card** where this run builds its own firmware, status, steps filling in live, the event feed, one console per `Text` tap, the **Time chart** (every stream on one axis), the trace chart, and one data card per tap |
| **Debug** | Three sources: two live tails — Core and `embarch-api`'s rolling file, both reaching the browser as this UI's own `lines` SSE event — and **builds**, stored rather than tailed: every firmware build this UI ran, picked from a list (39) |
