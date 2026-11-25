# embarch-desk: desks, the work item's knowledge and the interface overview, continued

**Status:** active, 2026-11-25. Split out of [../spec.md](../spec.md) §1 and §3 on 2026-11-25, verbatim, when that file reached its reserve line. Interface links are relative to `spec.md`'s folder in the original; [interfaces.md](../interfaces.md) is the reference.

## From §1

**Desks** (decisions 33–40, 77): one per project — a Linear project or team, a Harvest project and task, GitHub and firmware repos, a saved bench. **Each session works on its own desk**, its folder's else its work item's: its agents' Linear scope and `embarch-api`'s default build follow it (`embarch-api` decision 85), whatever the UI shows. **The UI selects one desk**, which picks only the Desk tab's cards and the repo its tabs open (`embarch-ui` decision 57). Every desk is published as `~/.local/share/embarch-desk/desks.json` for `embarch-api` to read while the service is stopped. A desk keeps **standing notes**, which every session in its repos hears at its start (74).

**The work item gathers the work's knowledge** (decisions 48–55): sessions write notes unasked, a tile line being a note of kind `done`; the hook turns every memory file a session writes into a note on its item; `desk_work_item` returns the whole brief, and a day's notes are what the tile's note summarises. **For `embarch-chat`** (46, 47) the desk is a mailbox each VS Code window polls, and the Desk shows each session as one line with Open chat or Jump. It also holds each desk's **reference index** (56) — every issue in its Linear scope, archived included, and every PR in its repos — which the chat mirrors from `GET /refs`.

## From §3

**HTTP on `127.0.0.1:4891`**, bearer `~/.config/embarch-desk/desk-token` (generated on first run) on every route but `GET /health` and `/oauth/linear/callback`; the plugin's hooks, `desk` skill and MCP server — agents' one access point to Linear and Harvest ([decision 29](../decisions.md)); connectors on pasted tokens or Linear's MCP sign-in (68); a CLI; `github_pr_threads` reads a pull request's review threads (EMB-176) and `github_draft_review_replies` drafts replies to them for one Send (EMB-173). `desk_restack` restacks a branch onto its moved base, hunk by hunk (EMB-142). A draft keeps the agent's version beside the owner's edits: `desk_revise_draft` revises both safely, `desk_get_draft` gives the owner-only diff (EMB-165). Reference: [interfaces.md](../interfaces.md).
