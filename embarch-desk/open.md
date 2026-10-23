# embarch-desk: open

**Status:** active, 2026-10-22.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Slack is not connected, and no tile has reached Harvest.** Linear, Harvest and GitHub pass their connector checks [measured 2026-10-22]; the Harvest time-entry write, the Linear status move and Slack's `search.messages`/`conversations.*` reads have never run against a real account.
- **The polish prompt has never run against real Harvest targets.** Whether Claude picks the right project and task from assignments and recent entries is unmeasured.
- **Is 8 hours the right gap?** ([decision 23](decisions.md)) A guess; a week of real tiles says whether overnight sessions leak in or long afternoons drop out.
- **Umbrella does not install it yet.** `embarch-desk service install` and `claude plugin install embarch-desk@embarch` are run by hand; `embarch setup` should do both.
- **Slack app installs may need an admin.** A managed workspace — a client's — can require approval for any app, the user's own included; until then it has no feed.
- **Fleet's Slack app as the desk's** ([decision 16](decisions.md)) is possible and untried; the webhook rotation it costs is the thing to rehearse first.
- **If OAuth returns (v2):** does Slack's PKCE localhost redirect survive distribution, and what is Harvest's real implicit-grant `expires_in`? A probe script for both was written and never run.
