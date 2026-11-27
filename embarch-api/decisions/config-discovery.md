# embarch-api decisions: Finding `embarch.toml`

**Status:** active, 2026-11-27 (`tasks/api/224`, EMB-306).

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/config.md](../interfaces/config.md).

### 152 — One function in `embarch-core-client` says which `embarch.toml` a process reads

Three binaries found the file three ways: this one took `--config`, then `EMBARCH_API_CONFIG`, then walked up from the working directory; the umbrella walked up only to the first `.git` ancestor and read neither flag nor variable; the ui took `[build].config_path`, then the variable, then the open repo, with no walk. With a flag or the variable set, `embarch doctor` could pass on one file while the API ran from another.

**`embarch_core_client::config_discovery::find_config_path(explicit, start)`** returns the path: the explicit path (`--config`), else `EMBARCH_API_CONFIG`, else the nearest `embarch/embarch.toml` in `start` or any ancestor. `find_config_path_with` takes the variable's value as an argument, so tests inject it and never touch the process environment. `main.rs` calls it and `find_config_upward` is gone.

**The walk is every ancestor, not a stop at `.git`.** It is this binary's present behaviour (decision 25), and the stop is not clearly better: a config kept above a repo (a workspace holding several firmware repos) is found by the walk and missed by the stop. The umbrella's stop only ever guarded against reading a stranger's config; the explicit path covers that case.

**A named file that does not exist is an error naming it**, from either the flag or the variable (`--config names X, which is not a file`), never a fall-through to the walk. Before, the API failed later with "failed to load config from X", so nothing relied on a fall-through. **An empty variable reads as unset**, as the desk's paths do; before, it was taken as a path and failed to load.

**The umbrella follows in `tasks/umbrella/128`** (`doctor` and `status` gain `--config` and the variable), **the ui in `tasks/ui/132`.** Neither is changed here.

**Rejected:** a per-binary rule (the drift this closes); the umbrella's `.git` stop as the shared walk.
