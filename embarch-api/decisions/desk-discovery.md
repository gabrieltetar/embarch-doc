# embarch-api decisions: Finding the desk

**Status:** active, 2026-11-27 (`tasks/api/223`, EMB-305).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 151 — The clients' copy of where the desk lives is one module in `embarch-core-client`

`embarch-desk`'s `paths.rs` owns where the desk lives: its config dir (`EMBARCH_DESK_CONFIG_DIR` taken as the folder itself, else `$XDG_CONFIG_HOME/embarch-desk` with an empty value read as unset, else `$HOME/.config/embarch-desk`), its data dir (the same three steps over `EMBARCH_DESK_DATA_DIR`, `XDG_DATA_HOME`, `.local/share`), its port (`EMBARCH_DESK_PORT` as a `u16`, else 4891) and its token file (`desk-token` in the config dir). Until now `session_desk.rs` here and `embarch-ui`'s `desk.rs` each spelled that out again, and one copy had drifted.

**`embarch_core_client::desk_discovery`** returns the config dir, data dir, token path, port and base URL with exactly that precedence, in the mold of `token_discovery`: the desk keeps its rule, the clients share one copy of it. `session_desk.rs` calls it and its own `home`, `desk_dir`, `data_dir`, `config_dir` and `desk_port` are gone. `embarch-ui` moves onto it in `tasks/ui/130`. An empty `HOME` reads as unset, as in the desk (the old copy here accepted it). **It reads and never creates**: the token stays the desk's to generate, and a client that finds no file treats the desk as not running. The rule is tested through an injected environment lookup, so no test touches the process's.

**Why the desk does not take the crate:** it has no path dependency today, and this crate would bring `embarch-topology` and `embarch-study-designer` into it. The rule therefore stays written twice, in the desk and here, and a change to one is a change to both. **Chat keeps its one TypeScript copy** (`tasks/chat/053`): a different language cannot share a Rust module. **Out of scope:** the generic XDG base-dir helpers (`user_dirs.rs` among them), which resolve `embarch`'s own directory, not the desk's; `user_dirs.rs` is unchanged and this module does not call it, because the desk's rule differs (an override taken as the folder itself, `embarch-desk` as the suffix).

**Rejected:** a copy per client (the drift this closes); moving the rule into `embarch-topology`, which holds no paths.
