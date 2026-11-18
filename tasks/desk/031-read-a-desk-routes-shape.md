# 031 — Read a desk route's shape from a shell

**State:** open
**Source:** EMB-137, filed by an audit after a session building a desk sub-tab piped `curl` into throwaway Python three times to learn what routes returned
**Issue:** EMB-137
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A session building on the desk's HTTP routes first has to learn what a route
returns on the running instance. Today it reads the token file by hand, calls
the route with `curl` and pipes the JSON into an inline script. The MCP tools
answer specific questions and do not expose a raw route.

Add a subcommand beside `serve`, `hook` and `mcp` in `src/main.rs`, for example
`embarch-desk get <route> [--post <json>] [--count-by <field>] [--raw]`:

- It finds its instance's port and token the way `serve` and `hook` already do
  (the config dir, `EMBARCH_DESK_CONFIG_DIR` and whatever else they read), so the
  caller never handles the token. A named instance, such as a dev desk on its own
  config dir and port, is reached the same way.
- By default it prints the answer's shape: the top-level keys, each list's
  length, one sample row, and with `--count-by` a count of rows by that field.
  `--raw` prints the JSON as returned.
- It prints no secret. A route that returns one is printed with that value
  masked, or refused; say in `spec.md` which.

**Public repo.** Tests start the desk against a temp config dir, the way the
existing tests do.

**Burndown leg: no new numbered decision.** Record the subcommand in `spec.md`
and `interfaces.md`. A real design fork goes to `scripts/fleet-linear.py file
--from decision`.

**What you may change.** Only `embarch-desk` and `embarch-doc/embarch-desk/`.

**Doc reserve.** Nothing of `embarch-desk`'s is in reserve.

## Why now

The owner moved EMB-137 to Fleet Ready.

## Done when

- [ ] One command prints a route's top-level keys, list lengths and one sample row, without the caller handling the token.
- [ ] It reaches a named instance, such as a dev desk on its own config dir and port, and not only the default one; a test covers it.
- [ ] No token or connector secret reaches its output; a test covers it.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
