# embarch-ui decisions: Tab folders

**Status:** active, 2026-11-04.

A tab the user's own config adds to the page, served at runtime with none of its code in this binary. Current truth: [../spec/tabs.md](../spec/tabs.md#tab-folders). Routes and the manifest: [../interfaces.md](../interfaces.md#tab-folders).

### 100 — A tab comes from a folder the config names, drawn into the page when it is served

The sidebar and panels were hard-coded in `index.html` and every asset was compiled in, so a tab holding private code had no way in except a fork or a second page. **Now `[[tabs]]` in the config names an id and a folder, and the folder holds `tab.toml`, a panel, an icon, scripts and styles.**

**Drawn on the server, not added by a script.** `app.js` binds the nav items and reads the fragment once, at start-up, so a tab must be in the page before that runs. Four comment marks in `index.html` say where its parts go. With no tab to draw, `/` serves the compiled page, byte for byte. The tab's nav item goes straight after Desk's, and its scripts after the built-in ones.

**The folder is read per request.** An edit to a tab shows on a reload, and only the `[[tabs]]` list needs a restart. A tab's page and files carry an `ETag` worked out from their bytes and revalidate on every load, as the compiled assets do, so a reload never shows a stale copy.

**Trust is the config file.** A tab's script runs on this UI's own origin and can call everything the page can. That is acceptable only because a tab comes from the user's own config, and nothing a page or a request does can add one. The panel and the icon go into the page unescaped for the same reason; only the label is escaped. No sandbox is claimed.

**A backend is a loopback service, and the rules are the desk proxy's plus three.** `/api/tab/<id>/<backend>/<rest>` generalises `/api/desk/{*rest}`: the token is added on the server and stays out of the page, and only this UI's own page gets through (`same_origin`). The three additions:

- **A backend's URL is `http://`, a literal loopback address and a port.** `localhost` is refused, because this server would be sending the token wherever the name resolves.
- **Redirects are not followed and no system proxy is used**, so a call and its token cannot leave the machine by either road.
- **A tab's files take the same origin check.** Without it, another site could load a private tab's script with a `<script>` tag and read what it defines.

The path goes on undecoded, so a `%2F` in a segment reaches the backend as sent. The answer's `Content-Type` comes back with it, unlike the desk proxy, which only ever answers JSON. No other header crosses in either direction, so no cookie reaches a backend.

**A broken tab is left out and logged** (the owner's call, 2026-11-04). A missing folder, a bad manifest, a non-loopback backend or an unreadable panel leaves that tab off the page, and the reason goes to the log at start-up and on each page load. Every other tab still works. A manifest's unknown key is an error, so a typo cannot quietly drop a script. *Rejected: refusing to start*, as a malformed config file does, because a private tab's typo would take down every tab. *Not chosen: showing the error in a panel under the tab's id.*

**A remembered tab that has gone lands on Desk.** The browser stores the last tab, and showing a tab with no panel would leave the page blank, which a tab leaving the config now makes possible.

**A tab's live data is polled here and pushed**, under the same rule as decision 6: `/api/tab-events/<id>/<backend>/<path>` polls that path every 10 s while a page listens and pushes it as a `view` event, or `view-error` with the reason. It shares its loop with `/api/desk-events`, whose failure event was renamed from `desk-error` to `view-error` so that one page script can read either stream. *Rejected: a streaming proxy and an event route on `embarch-desk`*, which is true push but adds a second repo and a new desk surface for a 10 s view. *Rejected: a timer in the tab's script*, which decision 6 rules out.

**Measured** in headless Firefox (`tests/browser/drive_tab.py`) with a sample tab and a stand-in backend, and against a real desk as the backend for the route and the event stream. No real tab has been built on it yet.
