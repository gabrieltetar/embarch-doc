# embarch-chat interfaces: what it asks the desk

**Status:** active, 2026-11-17.

Split verbatim from [../interfaces.md](../interfaces.md) on 2026-11-17, under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: the file was in reserve, and these are calls, not settings. Current truth: [../spec.md](../spec.md).

## What it asks the desk

From the Node side only, bearer token from `deskTokenPath` (20). Shapes and status codes: [`embarch-desk`'s interfaces](../../embarch-desk/interfaces.md).

| Call | Why |
|---|---|
| `GET /view`, `GET /view?desk=<id>` | The thread list and the waiting count: every 3 s while the list is visible, 15 s while hidden; `?desk=` for a window on another desk than the open one, plain `/view` again once that desk is gone (9, 20) |
| `POST /sessions/{sid}/assign` with `"client": "embarch-chat"` | A new chat on its item before `claude` starts (10); a resume sends the mark alone and never `untracked` (48) |
| `GET /sessions/{sid}` | A resumed chat's item, and whether the desk kept the mark |
| `POST /sessions/{sid}/line` | Keep, kind `finding` or `decision` (84) |
| `GET /items/{id}/states`, `POST /items/{id}/status` | The header's status dropdown (18) |
| `GET /items/{id}/brief` | A chat's work item for Promptu's pass, as its `desk` source (96) |
| `GET /mailbox?folder=`, `POST /mailbox/{id}/take` | Start work and Open chat, polled every 3 s per window folder (60 s back-off while the desk is unreachable or lacks the route), each entry taken once; a `start` runs Promptu's pass, its `prompt` the draft's fallback (11, 96) |
| `GET /mailbox` entry `{"kind":"end"}` (`item_id`, `issue_key`, `outcome` `done`/`canceled`) | The issue is Done or Canceled and every check passed: its chat shows the message and one Close window button and takes no input, waiting for a running turn (104). Written by the desk only; never expires on the launch clock |
| `GET /mailbox` entry `{"kind":"unfinished"}` (as `end`, plus `blockers: [{repo, reason}]`) | A check failed: nothing closes; each blocker shows over the live chat with Finish (104) |
| `POST /items/{id}/finish` | Finish: the desk re-checks and posts a fresh `end` or `unfinished`; answers `{"ended":true}` or `{"ended":false,"blockers":[…]}`, which the chat ignores — it acts on the entry. 404 from an older desk: one plain error (104) |
| `POST /mailbox` `{"kind":"focus"}` | Jump to a chat another window runs: that window takes the entry and shows it (31) |
| `GET /mailbox` entry `{"kind":"open"}` | Starts an untracked chat in the entry's folder, with no prompt (desk decision 70) |
| `GET /refs`, `GET /refs?desk=<id>` | The reference index of the desk `/view` is asked for (88): read once, then again only when `/view`'s `refs_ms` or the desk moves. Its `projects` (`id`, `name`, `state`, `url`) and `documents` (`id`, `title`, `url`, `project_id`, `project_name`) feed the linker's project and document kinds (117); a desk that omits them reads as none |

**A desk older than b722b3b** ignores `/view?desk=` and does not keep the mark: the list says "Update embarch-desk" and shows only chats in the window's repos. **One older than 8f06ba0** has no `refs_ms` in `/view`, so `/refs` is never asked: no reference cards, no prose links, and a step shows only what it carries.
