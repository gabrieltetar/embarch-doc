# embarch-desk: open

**Status:** active, 2026-10-22.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **No real Linear, Harvest or Slack account has been connected.** The GraphQL queries, Harvest's project assignments and time-entry write, and Slack's `search.messages`/`conversations.*` reads are written from the services' docs and unit-tested on their shapes only. Unblocked by the owner pasting one token of each.
- **The polish prompt has never run against real Harvest targets.** Whether Claude picks the right project and task from assignments and recent entries is unmeasured.
- **Is 8 hours the right gap?** ([decision 23](decisions.md)) A guess; a week of real tiles says whether overnight sessions leak in or long afternoons drop out.
- **The repo has no remote.** `../embarch-desk` is local; a public GitHub repo is the owner's call.
- **Umbrella does not install it yet.** `embarch-desk service install` and `claude plugin install embarch-desk@embarch` are run by hand; `embarch setup` should do both.
- **Slack app installs may need an admin.** A managed workspace — a client's — can require approval for any app, the user's own included; until then it has no feed.
- **Fleet's Slack app as the desk's** ([decision 16](decisions.md)) is possible and untried; the webhook rotation it costs is the thing to rehearse first.
- **If OAuth returns (v2):** does Slack's PKCE localhost redirect survive distribution, and what is Harvest's real implicit-grant `expires_in`? A probe script for both was written and never run.
