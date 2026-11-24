**Target:** suite/hil-guide.md Study 1, the `steps` bullet (apply byte for byte; embarch-api's `guide/hil-guide.md` already carries it)
**Was:**

- **`steps`**: a `BleConnect` with `target_address` (six bytes, most significant first, and `Public` or `Random`) or `target_name`, never "the first one seen": on a real bench that reaches a neighbour. To find the DUT's address, run a `BleConnect` whose `target_name` nothing has, and read the census in its `fail_reason` and in `dev-bench.log`. Then a `GattMonitorSelected` naming the data characteristic, whose `timeout_ms` is the capture window.

**Now:**

- **`steps`**: a `BleConnect` with `target_address` (six bytes, most significant first, and `Public` or `Random`) or `target_name`, never "the first one seen": on a real bench that reaches a neighbour. To find the DUT's address, run a `BleConnect` whose `target_name` nothing has, and read the census in `dev-bench.log`, which lists every advertiser; `fail_reason` is capped and lists only those that sent a name, so one with no plausible DUT in it is not evidence the DUT is off the air. Then a `GattMonitorSelected` naming the data characteristic, whose `timeout_ms` is the capture window.
