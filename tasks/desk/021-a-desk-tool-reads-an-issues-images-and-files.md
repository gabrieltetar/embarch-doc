# 021 — A desk tool reads an issue's images and files

**State:** done
**Source:** Linear issue EMB-14
**Issue:** EMB-14
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

`linear_get_issue` returns an issue's description and comment bodies as text. A screenshot, a schematic snippet or a file pasted into the issue is a link in that text that no desk tool can fetch: Linear's upload links need the workspace's credentials and are signed to expire within minutes. Decision 29 makes the desk the agents' one access point to Linear, so a session working such an issue reads the words and misses the rest.

Add the read, **with this direction (decided at the split):**

- **`linear_get_issue` lists what can be read.** Its answer gains a list of the issue's files: every Linear upload link in the description and in the comments it returns, and the issue's attachment records (title and URL), each saying where it was found. The worker names the field.
- **A new tool reads one of them, given the issue key and the link.** It fetches at call time with that workspace's credentials. **It reads only a link the issue itself lists**; any other URL is refused naming the issue, so the tool is never a general fetch through the owner's tokens.
- **What it returns:** an image as MCP image content; a text file as text; anything else (a PDF, an archive) written under the desk's own data folder and its path returned, so the session can open it. A size cap the worker picks, stated in the decision, and a refusal naming the size when it is over.
- **Both backends.** The API-key backend (`src/linear.rs`) fetches with the key. For a Linear-MCP workspace (`src/linear_mcp.rs`, decision 68) the worker finds what works: fetching with its token, or calling the Linear MCP server's own image or attachment tool. If neither works, the tool says so naming the backend; it never returns an empty success.

## Why now

EMB-14: an issue whose ask is partly in a screenshot is read incompletely by every agent, and the desk is the only route those agents may use.

## Where to look

- `src/linear.rs` `detail_from`, `get_issue` — the issue answer; the `Authorization` header the key backend sends
- `src/linear_mcp.rs` `detail_from`, `call_on_issue` — the MCP backend's issue read
- `src/server.rs` — the `/linear/...` routes `linear_get_issue` goes through
- `src/mcp.rs` `linear_get_issue` — where the new tool goes beside it
- `plugin/skills/desk/SKILL.md` — say when to use the tool
- `embarch-doc/embarch-desk/decisions/access-point.md` (29, 59, 79) and `decisions/agents.md` (68); `interfaces.md` for any new route

## Dispatch notes

- Normal mode: a new numbered `embarch-desk` decision is expected. Number it per `DOC-CONVENTIONS.md`; check `main` before you commit, since `desk/020` lands just before you.
- **`embarch-doc/LINEAR-PROTOCOL.md` §1 says "the desk cannot read attachments".** That file is the owner's; do not edit it. Say in this file which sentence your tool makes stale, and the supervisor files it for the owner.
- Tests use the existing fakes for both backends; nothing calls a real Linear workspace or a real upload link.
- No `embarch-desk` doc in `embarch-doc` is in doc-size reserve at the split.
- Edit files with your Edit and Write tools, not inline Python or shell redirects.

## Done when

- [x] `linear_get_issue` lists the issue's upload links and attachment records, each with where it was found.
- [x] A desk MCP tool returns an image or file the issue lists, given the issue key and the link, and refuses a link the issue does not list.
- [x] Images come back as image content, text as text, other files as a path under the desk's data folder; over the cap is a refusal naming the size.
- [x] Each backend has a test, the refusal of an unlisted link included; a backend that cannot fetch says so.
- [x] A new `embarch-desk` decision records the tool, and `interfaces.md` lists any new route.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.

## What landed

`embarch-desk` decision 81 (`decisions/access-point.md`): `linear_get_issue` gains `files` (`{url, title, found}`); new tool `linear_get_file(key, url)` over `POST /linear/issue/{key}/file`, new module `src/files.rs`. Picks: 10 MiB cap; text over 200 KB is written to a file, not returned; files go under `<data>/linear-files/<KEY>/`; the credential is sent only to `uploads.linear.app` and only `https` public hosts are fetched; the file list covers all comments read (500 cap), not only the 25 returned. API-key backend fetches with the bare key; the MCP backend fetches with its bearer, then falls back to the server's `extract_images`. Tests are pure plus one loopback download; no fake of either backend's HTTP exists, so the fetch calls themselves are not exercised.

**Debt (live workspace, not hardware):** nothing was run against a real Linear workspace. Unmeasured: the upload host accepts the bare key and the MCP bearer; `extract_images` takes `markdown`; the MCP `get_issue` returns `attachments` unasked. Verify with one issue holding an image, a PDF and an attachment, on each backend.

**Stale in `LINEAR-PROTOCOL.md` §1 (the owner's file, not edited):** "(the desk cannot read attachments)". It now can: `linear_get_issue` lists an issue's `files` and `linear_get_file` reads them, so a screenshot in an issue is readable by an agent; a reference to a screenshot is still worse than words in the body, but the parenthetical is false.
