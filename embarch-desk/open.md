# embarch-desk: open

**Status:** active, 2026-10-22.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **One client's own Linear workspace still goes through its hosted connector** ([decision 32](decisions.md)), until that client gets a desk with its key; then the connector is removed.
- **No draft has been sent and no tile has reached Harvest**; the comment, issue and status mutations were checked only with invalid ids, the reads against the real accounts [measured 2026-10-22]. **Slack is not connected**, so its reads have never run.
- **The polish prompt has never run against real Harvest targets.** Whether Claude picks the right project and task from assignments and recent entries is unmeasured.
- **Is 8 hours the right gap?** ([decision 23](decisions.md)) A guess; a week of real tiles says whether overnight sessions leak in or long afternoons drop out.
- **Umbrella does not install it yet.** `embarch-desk service install` and `claude plugin install embarch-desk@embarch` are run by hand; `embarch setup` should do both.
- **Slack app installs may need an admin.** A managed workspace — a client's — can require approval for any app, the user's own included; until then it has no feed.
- **Fleet's Slack app as the desk's** ([decision 16](decisions.md)) is possible and untried; the webhook rotation it costs is the thing to rehearse first.
- **If OAuth returns (v2):** does Slack's PKCE localhost redirect survive distribution, and what is Harvest's real implicit-grant `expires_in`? A probe script for both was written and never run.
- **"Is the bench busy?" sees studies only.** The bench proposal names a study Core lists as running; a flash or bootload in progress is not in that list ([decision 37](decisions.md)).
- **A repo with several `embarch-api` projects** answers an unnamed build with the list (`embarch-api` decision 85). Whether a desk should name its default build project is unasked.
- **Several desks open at once** ([decision 33](decisions.md)) is deliberately later.
- **Is `claude.ai/code/<id>` the local session id?** Remote Control's docs call the URL's id the session id without saying which; Answer assumes the local one ([decision 44](decisions.md)). The first real session settles it.
- **A worktree of a repo built inside a west workspace** — does it need its own `west update`, or can it share the main clone's modules? The first real Start work settles it.

