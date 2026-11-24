# embarch-umbrella: `scripts/cut-release.py`

**Status:** active, 2026-11-24 (EMB-344, `tasks/umbrella/109`). Step 4 of
[the release-signing proposal](../../embarch-release-signing-proposal.md). Index:
[../decisions.md](../decisions.md); the flow it drives is
[decision 14](../decisions/install.md) and [verify-release.md](verify-release.md).

`python3 scripts/cut-release.py <suite-version> [--go] [--root DIR] [--dest DIR]`

Python 3.11+, standard library only. **A dry run by default**: it reads each component's
`Cargo.toml` version and latest `v*.*.*` tag (newest by number) and prints every tag it would
create, the `suite.toml` change, and every command `--go` would run. `--root` is the folder
holding the `embarch-core` and `embarch-api` checkouts (default: this repo's parent); `--dest`
is where the release downloads (default `dist/suite-v<version>`).

**`--go`, first run.** For each component whose version differs from its latest tag, in the
order core, api, umbrella: `git tag`, `git push origin <tag>`, then `gh run watch --exit-status`
on its `release.yml` run. A component whose version equals its tag is skipped. A failed run
stops the script before anything later is tagged. It then rewrites `suite.toml` (comments
kept) and stops, for the owner to commit it.

**`--go`, second run** (versions and `suite.toml` agree, and `suite.toml` is committed): tag
`suite-v<version>`, watch `assemble-suite.yml`, `gh release download`, `embarch verify-release`
on the download. A failed verification stops with `VERIFICATION FAILED` and prints no install
line; otherwise it prints `embarch install-core <dest>`, the verb as the issue gives it.

**The owner approves the `release` environment, never the script.** Wherever it waits it says
so. Every `git` and `gh` call goes through one `Runner` (`query` read-only, `act` mutating, a
dry run only prints `act`), which `scripts/test_cut_release.py` fakes: no test touches the
network or a real tag. Run them with
`python3 -m unittest discover -s scripts -p 'test_*.py'` in `embarch-umbrella`.

**Unbuilt, not run live.** Written against the fake runner only; the first real cut is the
test of the `gh` argument shapes.
