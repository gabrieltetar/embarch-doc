# embarch-ui: tab folders

**Status:** active, 2026-11-24.

Split verbatim from [tabs.md](tabs.md) (`tasks/ui/114`). Why: decision 100 ([../decisions/tab-folders.md](../decisions/tab-folders.md)).

## Tab folders

**The user's own config can add a tab** (100): `[[tabs]]` names an id and a folder, and the folder holds `tab.toml` and the tab's files, none of them in this binary. The nav item goes straight after Desk's and the panel joins the others, so a tab opens by click and by `#<id>` like a built-in one. The folder is read per request, so an edit shows on a reload.

**A tab's script runs on this UI's own origin and can call everything the page can.** That is acceptable only because a tab comes from the user's own config file, and nothing a page or a request can do adds one. Name only a folder you trust as you trust this binary.

A tab's calls go through this server to the loopback services its manifest names, with the token added there and kept out of the page. A tab that cannot be read is left off the page and logged, and the rest still work. With no tab configured, the page is the built-in one, byte for byte. Manifest and routes: [../interfaces.md](../interfaces.md#tab-folders).
