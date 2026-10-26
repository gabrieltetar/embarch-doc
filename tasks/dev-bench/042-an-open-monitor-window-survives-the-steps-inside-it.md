# 042 — An open monitor window is broken by the steps that run inside it

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-dev-bench findings 3, 4 and 12), verified by Opus against embarch-dev-bench@52822069
**Scope:** dev-bench
**Hardware:** toolchain — C in `app/src/ble_bridge_real.c`, built and tested in the **main checkout** (this repo's Zephyr trees are gitignored, so a worktree cannot build it). The window's behaviour across steps can only be observed against a real BLE peer, so the unit leaves a hardware-verification debt (`../../embarch-fleet/protocol.md` §7).
**Owner:** no

## What

`GattMonitorStart` opens a window that is meant to keep capturing while later steps run. That is its whole purpose (`embarch-study-designer` `src/study.rs:770-783`; decision 28). The state the window depends on is shared with those later steps, and they overwrite it. All Zephyr behaviour below was checked against the NCS v3.4.0 tree in `workspaces/nordic/zephyr`.

1. **A one-shot monitor step reuses the window's live params (finding 4).** Only `execute_gatt_monitor_window_start` checks `monitor_window_open` (`:2012-2016`). `GattMonitorAll`/`Selected` (`:1973-2002`) reset `monitor_subscribe_count` and `memset` the same `monitor_subscribe_params[]` (`:1823`, `:1865-1868`). Zephyr's subscription list is intrusive: each struct is linked through its own `node` (`gatt.c:5415`). Zeroing structs that are still linked truncates that list. Each re-subscribe then finds its own struct and returns `-EALREADY` (`gatt.c:5379-5391`), which the walk treats as success.

   Traced through: most of the window's characteristics are left with no host subscriber while their CCC stays enabled on the DUT. The one-shot captures little. The window flag stays set with a count of 0, so the window captures nothing more and its Stop is a no-op Pass.
2. **A later discovery relabels the window's rows (finding 3).** A window's notification is labelled by resolving a flat index (`monitor_char_index`, `:1905-1906`) through `discovered[]` (`:1753-1761`). Every later `RunProtocol`, `GattDiscover` or monitor step runs `run_gatt_discovery`, which zeroes that table and refills it (`:1656-1657`). Rows that arrive while it does resolve to no UUID or the wrong one. `main.c`'s GattNotify-tap fan-out (`:388-399`) matches on that UUID, so they miss their tap with no dropped count.

   If that discovery fails partway, the table stays partial for the rest of the window. Whether a completed re-walk returns a different table depends on the DUT and is not established here.
3. **`ble_bridge_reset` zeroes `subscribe_params` too early (finding 12).** It does so straight after starting the CCC-clear write (`:3284-3288`). That breaks the file's own rule at `:2228-2232`: "subscribe_params is never memset … zeroing it would be a NULL call". A successful CCC-clear response calls `params->notify(conn, params, NULL, 0)` unguarded (`gatt.c:5242-5245`). Whether that response can land before the disconnect that follows is timing, and has not been measured.
4. **Found while verifying finding 4, same root.** Zephyr skips the CCC write when another subscription on the same handle already covers it. It returns 0 with **no callback at all** (`gatt.c:5391-5415`). So a `DataExchange` subscribe (`ensure_subscribed`, `:2282`) or a `RunProtocol` source (`:2917`) on a characteristic the open window already holds waits on `ccc_sem` for its whole budget and reports `TimedOut`.

**Proposed direction**, which leaves room for the design:

- A window's subscriptions carry their own labels, copied at subscribe time as `protocol_subscribe_char_uuid` already does, rather than an index into a table other steps rebuild.
- A one-shot monitor inside an open window is either refused by name or explicitly closes and reopens it. Which one is a decision.
- No params struct is zeroed while Zephyr can still call through it.
- The "already covered on this handle" return is treated as subscribed rather than waited on.

## Why now

The crate allows any step inside a window, and stimulating the DUT from inside one is the reason the window exists. Each case above loses or mislabels capture without counting it, which contradicts spec §3, "Loss is counted and reported, never silent". The third case contradicts a rule written in the same file.

**Sequencing:** the inbox drop `dev-bench-monitor-step-fails-when-its-subscriptions-do.md`, filed the same day, also rewrites `monitor_subscribe_matching` in `ble_bridge_real.c`. Land them one after the other, not in parallel.

## Done when

- [ ] A one-shot monitor step run while a window is open leaves the host's subscription list intact, and the window still captures afterwards. If the chosen behaviour is a refusal, the step fails naming the open window.
- [ ] A notification arriving on an open window is labelled with the characteristic it was subscribed under, including while a later step re-runs discovery and after one that failed partway.
- [ ] `ble_bridge_reset` never leaves a struct zeroed while a CCC write that uses it can still be answered.
- [ ] A `DataExchange` subscribe or a `RunProtocol` source on a characteristic an open window already holds does not wait for a callback Zephyr never makes.
- [ ] Both bench images build: `nrf54l15dk/nrf54l15/cpuapp` from `workspaces/nordic` and `esp32c5_devkitc/esp32c5/hpcore` from `workspaces/espressif`. The `app/tests/serial_protocol` suite passes on `native_sim`. Run with `/home/gabriel/Github/embarch/.west-venv/bin/west` from the main checkout's workspace directories, per `README.md`'s build sections.
- [ ] The hardware-verification debt names which of the cases above were exercised against a real DUT.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. Decision 28 (`decisions/dispatch.md`) states what a window does with a monitor step inside it. `spec.md` and `open.md` are already inside their reserve.
