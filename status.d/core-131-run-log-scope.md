**Target:** embarch-token.md §3 — the "Two secrets, two scopes" bullet ("refuses nothing by scope yet")
**Was:** "Core records whether a request carried the agent's token or the person's and refuses nothing by scope yet (decision 109)."
**Now:** Core refuses by scope on one route: the agent's token cannot discard (`POST /study/{id}/discard`) the captures of a run that failed, errored, was inconclusive or was published, `403`; the person's can (`embarch-core` decisions 111 and 112, 2026-11-21).
