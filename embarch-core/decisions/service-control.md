# embarch-core decisions: Starting and stopping the service

**Status:** active, 2026-11-27 (`tasks/core/190`, EMB-342). Index: [../decisions.md](../decisions.md). Sibling: [platform.md](platform.md) (decision 3, whose self-elevation this narrows for `start` and `stop`).

### 163 — `start` and `stop` ask the service manager unelevated first and elevate only on a rights refusal

`service::start` and `stop` used to call `elevate::ensure_elevated_or_fallback()` before anything, so every switch between the service and a development Core raised a UAC prompt or needed `sudo`, even where the elevated install had granted the engineer's account the right to start and stop the service (`tasks/umbrella/124`: a service-descriptor ACE on Windows, a polkit rule on Linux). Now `service::control` makes the `service-manager` call as the current user; only a refusal for lack of rights falls through to `ensure_elevated_or_fallback` and a retry, which behaves as before. Any other failure is returned as it was and does not elevate. An already elevated process calls once. With no grant the attempt is refused and the user sees the same prompt as before, plus one debug-level log line.

**The classifier is a pure function, `is_rights_refusal(&io::Error, windows: bool)`.** `service-manager` 0.11 wraps a failed `sc.exe` or `systemctl` as an `io::Error` of kind `Other` with the text `Command failed with exit code <n>: <stderr or stdout>`, so the text is all there is to match. Windows: exit code 5 or "Access is denied". systemd: "Interactive authentication required", "Access denied", "Permission denied" (case-insensitive). **Matched by reading, not constructed:** the real `sc.exe` and `systemctl` outputs. The tests build the `io::Error` shape from the crate's source and the message texts from the tools' documented wording; no real service was touched. **[assumed]:** that `systemctl` run with no terminal and no polkit agent prints one of these three texts for a refusal; hardware-verification debt in `tasks/core/190`. The launchd backend is not classified: a refusal there is reported as it is.

`install`, `uninstall` and `install --service` still elevate first, always: the grant never covers changing the service.

*Rejected:* checking the grant up front (`sc sdshow`, `pkaction`) — a second mechanism per platform to answer what the start itself answers; matching on the exit code alone for systemd (`systemctl` exits 1 for most failures).
