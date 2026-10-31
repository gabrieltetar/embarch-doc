# embarch-desk: open

**Status:** active, 2026-10-22.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **One client's own Linear workspace still goes through its hosted connector** ([decision 32](decisions.md)). Its desk exists, with no key to be had: it signs in through Linear's MCP server (68), and the hosted connector goes once that sign-in has run for real.
- **Linear through its MCP server is checked only by a probe and unit tests** (68): no desk sign-in has completed. `save_issue`'s and `save_comment`'s answers are read for a key and a link without ever having been seen, and whether a tool call needs `initialize` first is untested. The first status move, comment and issue on that desk settle it. How long the refresh token lives is unknown; the connector check renews the day-long token, so it never sits idle.
- **No draft has been sent and no tile has reached Harvest**; the comment, issue and status mutations were checked only with invalid ids, the reads against the real accounts [measured 2026-10-22].
- **The polish prompt has never run against real Harvest targets.** Whether Claude picks the right project and task from assignments and recent entries is unmeasured.
- **Is 8 hours the right gap?** ([decision 23](decisions.md)) A guess; a week of real tiles says whether overnight sessions leak in or long afternoons drop out.
- **`embarch setup` installs it, and has never run for real** ([`embarch-umbrella` decision 58](../embarch-umbrella/decisions/setup-reversal.md)): the service and the plugin, both mocked in tests. Adding the `embarch` marketplace, now in `embarch-umbrella` (`embarch-promptu` decision 20), stays by hand.
- **If OAuth returns (v2):** what is Harvest's real implicit-grant `expires_in`? A probe script was written and never run.
- **"Is the bench busy?" sees studies only.** The bench proposal names a study Core lists as running; a flash or bootload in progress is not in that list ([decision 37](decisions.md)).
- **A repo with several `embarch-api` projects** answers an unnamed build with the list (`embarch-api` decision 85). Whether a desk should name its default build project is unasked.
- **Several desks open at once** ([decision 33](decisions.md)) is deliberately later.
- **A mark alone answers 400.** A resumed `embarch-chat` chat sends only `client` to `POST /sessions/{sid}/assign`; the desk records it, then refuses for the missing item, so the panel reads the mark back from `GET /sessions/{sid}` ([interfaces.md](interfaces.md)). Whether a mark alone should be a 200 is the owner's call.
- **Keep archived issues in the reference index?** ([decision 56](decisions.md)) They are in it — 69 of 178 on the first desk [measured 2026-10-25] — because a reference to old finished work is the point, and that is the recommendation; the owner has not said.
- **A worktree of a repo built inside a west workspace** — does it need its own `west update`, or can it share the main clone's modules? The first real Start work settles it.

