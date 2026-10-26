# 043 — A monitor step passes when its subscriptions failed or the link dropped mid-walk

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-dev-bench findings 1 and 8), verified by Opus against embarch-dev-bench@52822069
**Scope:** dev-bench
**Hardware:** toolchain — C in `app/src/ble_bridge_real.c`, built and tested in the **main checkout** (this repo's Zephyr trees are gitignored, so a worktree cannot build it). The changed paths run only against a real BLE peer, and no native_sim test reaches `ble_bridge_real.c`, so the unit leaves a hardware-verification debt (`../../embarch-fleet/protocol.md` §7) rather than claiming a bench result.
**Owner:** no

## What

The subscribe walk shared by all four monitor actions (`monitor_subscribe_matching`) does not check whether a subscription worked. The single-subscription path (`ensure_subscribed`) and the protocol path (`protocol_subscribe_sources`) both do. Four outcomes follow, all checked against the NCS v3.4.0 Zephyr tree in `workspaces/nordic/zephyr`:

- **A CCC write the DUT rejects is reported as a subscription.** Zephyr answers it through the `subscribe` callback with the ATT error (`gatt.c:5212-5250`). The walk never reads `ccc_att_err`, so it emits `SUBSCRIBED`, counts the characteristic, and the step passes.
- **A characteristic with no CCC uses up the step.** Zephyr reports a missing CCC only through `notify(NULL)`, with no `subscribe` callback (`gatt.c:5288-5297`). This file's own comment at `:138-141` says the same. `monitor_notify_cb`'s NULL arm (`:1748-1752`) wakes nothing, so `k_sem_take(&ccc_sem, …)` waits out the rest of the step budget. Every later characteristic then times out at once, and the step passes with a capture window of zero.
- **A disconnect during the walk is thrown away.** The walk never checks `link_lost`. It keeps calling `bt_gatt_subscribe(active_conn, …)` with `active_conn == NULL`; Zephyr only `__ASSERT`s `conn` and then reads `conn->state` (`gatt.c:5353-5364`). `execute_gatt_monitor_window` then runs `link_lost = false; k_sem_reset(&disconn_sem)` (`:1987-1988`), which discards that disconnect, waits out the deadline and returns Pass.
- **Teardown calls `bt_gatt_unsubscribe` with a NULL connection.** This is reached from the one-shot's `dropped` path (`:1995`), from Stop or the end-of-study close after a mid-window disconnect, and from `protocol_unsubscribe_all` after a RunProtocol whose link dropped (`:2951-2962`). Zephyr reads `conn->state` there too (`gatt.c:5455-5458`). What that read does on the bench is not established: the nRF54L15 build has `CONFIG_ASSERT` off and `NULL_POINTER_EXCEPTION_DETECTION_NONE`. Decision 28 says the window flag "is cleared on disconnect… or a later Stop would unsubscribe against a freed connection", but `disconnected_cb` (`:600-613`) never clears `monitor_window_open`.

The protocol path has a quieter relative of the same problem. `protocol_notify_cb`'s NULL arm (`:2774-2779`) neither sets `ccc_torn_down` nor gives `ccc_sem`, so the check `if (ccc_torn_down)` at `:2921` cannot fire. A protocol source with no CCC reports `TimedOut` after the full budget instead of "has no writable CCC".

**Proposed direction**, which leaves room for the design:

- Give the monitor walk the same per-characteristic verdict the other two paths already compute. Its NULL arm wakes the walk during the subscribe phase.
- Stop the walk on link loss and report `Disconnected`, instead of resetting the loss away.
- Never call into the GATT client with no live connection.
- A named Selected target whose subscription did not land fails the step and names it, as decision 40 already requires for a missing or non-notifying target.

Record as a decision whether an unfiltered `GattMonitorAll` that subscribed to **nothing** passes.

## Why now

The monitor family exists to refuse a capture that passes empty. The comment on `monitor_subscribe_matching` (`:1806-1810`) says so, and so do decisions 40 and 42. Today a CCC the DUT refuses produces exactly that: a Pass, a transcript that says `SUBSCRIBED`, and no rows. This contradicts:

- spec §3, "A named thing missing fails the step" and "Loss is counted and reported, never silent";
- decision 28's disconnect rule, quoted above.

**Sequencing:** the inbox drop `dev-bench-an-open-monitor-window-survives-the-steps-inside-it.md`, filed the same day, also rewrites `monitor_subscribe_matching` in `ble_bridge_real.c`. Land them one after the other, not in parallel.

## Done when

- [ ] A characteristic whose CCC write is answered with an ATT error, or whose CCC Zephyr cannot find, is never reported `SUBSCRIBED` and never counted as subscribed. The transcript names which case it was.
- [ ] A missing CCC costs that one characteristic, not the rest of the step budget.
- [ ] A Selected monitor step fails, naming the target, when a target's subscription did not land, whatever the reason.
- [ ] A disconnect at any point in a monitor step, the subscribe walk included, makes the step report `Disconnected`. No monitor step passes after one.
- [ ] No path in `ble_bridge_real.c` calls `bt_gatt_subscribe`/`bt_gatt_unsubscribe` with a NULL connection. Decision 28's "window flag cleared on disconnect" is true in code, or the decision is amended to say what happens instead.
- [ ] A protocol source with no CCC fails its step by name instead of timing out.
- [ ] Both bench images build: `nrf54l15dk/nrf54l15/cpuapp` from `workspaces/nordic` and `esp32c5_devkitc/esp32c5/hpcore` from `workspaces/espressif`. The `app/tests/serial_protocol` suite passes on `native_sim`. Run with `/home/gabriel/Github/embarch/.west-venv/bin/west` from the main checkout's workspace directories, per `README.md`'s build sections.
- [ ] The hardware-verification debt says which of the cases above were exercised against a real DUT and which were not.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. `spec.md` (9,632 of 10,240 B) and `open.md` (3,916 of 5,120 B) are already inside their reserve, so a new decision goes in `decisions/dispatch.md` or `decisions/capture.md`.
