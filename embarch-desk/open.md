# embarch-desk: open

**Status:** active, 2026-10-22.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **The client's Linear workspace still goes through its hosted connector** ([decision 32](decisions.md)) until its API key is added to the desk; then that connector is removed too.
- **No draft has been sent and no tile has reached Harvest**; the comment, issue and status mutations were checked only with invalid ids, the reads against the real accounts [measured 2026-10-22]. **Slack is not connected**, so its reads have never run.
- **The polish prompt has never run against real Harvest targets.** Whether Claude picks the right project and task from assignments and recent entries is unmeasured.
- **Is 8 hours the right gap?** ([decision 23](decisions.md)) A guess; a week of real tiles says whether overnight sessions leak in or long afternoons drop out.
- **Umbrella does not install it yet.** `embarch-desk service install` and `claude plugin install embarch-desk@embarch` are run by hand; `embarch setup` should do both.
- **Slack app installs may need an admin.** A managed workspace — a client's — can require approval for any app, the user's own included; until then it has no feed.
- **Fleet's Slack app as the desk's** ([decision 16](decisions.md)) is possible and untried; the webhook rotation it costs is the thing to rehearse first.
- **If OAuth returns (v2):** does Slack's PKCE localhost redirect survive distribution, and what is Harvest's real implicit-grant `expires_in`? A probe script for both was written and never run.
