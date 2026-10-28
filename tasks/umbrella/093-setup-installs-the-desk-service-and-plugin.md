# 093 — `embarch setup` installs `embarch-desk`'s service and Claude plugin, which are run by hand today

**State:** open
**Source:** refill sweep, 2026-10-28 leg — `embarch-desk/open.md`: "Umbrella does not install it yet.
`embarch-desk service install` and `claude plugin install embarch-desk@embarch` are run by hand;
`embarch setup` should do both."
**Scope:** umbrella
**Hardware:** verify-only — host-side code and tests with the two commands mocked; one real `embarch setup`
on the owner's machine confirming both steps is the owner's or an attended leg's.
**Owner:** no

## What

`setup` installs Core's service and copies three binaries (decisions 3, 28); the desk's service and its
plugin are separate manual steps. Have `setup` run `embarch-desk service install` and
`claude plugin install embarch-desk@embarch` when `embarch-desk` is found by the same locate rules the
other binaries use, skip both by name when it is not, and report each step's outcome. `setup --uninstall`
reverses what it installed. Read `embarch-desk`'s own `spec.md` and `interfaces.md` for the exact commands
and what they need first; do not infer a flag. Record the choice as an umbrella decision, including what
happens when `claude` is not on `PATH`.

## Why now

Every machine that gets the suite needs both steps, and nothing reminds anyone of them; `doctor` cannot
see a desk that was never installed.

## Done when

- [ ] `setup` runs both steps when `embarch-desk` is located and skips them by name when it is not; tested
      with both commands mocked.
- [ ] `setup --uninstall` reverses them, tested the same way.
- [ ] An umbrella decision records it; `embarch-desk/open.md`'s bullet is a status fragment for the
      supervisor (an `embarch-desk` doc is not an umbrella worker's to edit).
- [ ] Gate green (`../../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
