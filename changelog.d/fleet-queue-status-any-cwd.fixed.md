`queue-status.py` reads `fleet.toml`'s instance when the cwd has no `tasks/`, and exits 2 naming the paths it tried instead of reporting an empty queue.
