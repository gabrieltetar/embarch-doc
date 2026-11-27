**Target:** embarch-token.md §2 — the WSL2 token discovery and the relocated-`ProgramData` gap
**Was:** the client falls back silently to `C:\ProgramData` when `ProgramData` is unset
**Now:** core-client token discovery calls `embarch_topology::machine_data_dir`; an unset `ProgramData` is an error naming it, with no literal fallback (api 221).
