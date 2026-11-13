# embarch-ui decisions: The UI's config file

**Status:** active, 2026-11-12.

Where `config::load()` finds the file. Routes and keys: [../interfaces.md](../interfaces.md#tab-folders).

### 102 — With `EMBARCH_UI_CONFIG` unset the UI reads a default file, and `service install` says which config it ends up with

Since 101 the unit is the only thing that sets `EMBARCH_UI_CONFIG`, and `service install` copies it only from the installing shell. A normal or Claude-session shell does not set it, so every reinstall silently dropped the tabs and per-repo settings (EMB-140). **`load()` now falls back to `embarch-ui/config.toml` under the user's config directory** (`$XDG_CONFIG_HOME`, else `~/.config`; `%APPDATA%` on Windows) **when that file exists.** The service finds it with no variable, so an install from any shell keeps the config, and the unit needs no path written into it.

**Order:** the variable, else the default file, else `Config::default()`. A variable that is set wins and a missing file it names is still an error, so a typo is not hidden by the fallback. With neither variable nor file nothing changes: the zero-config default, `base_url = "auto"`, still works.

**`service install` prints one line naming the config the unit will read** (the carried variable, the default path, or none), so the success line no longer looks the same when the UI will run on defaults. *Rejected: refusing to install without a config* — the zero-config bench is a supported case. *Rejected: writing the resolved path into the unit* — it would freeze a path the service can find itself, and an edit to the default file already takes effect on restart. The Windows path is written, not run: the UI is not deployed there [assumed].
