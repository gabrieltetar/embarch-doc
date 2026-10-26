Core: `/signals/{name}/capture` records a declared signal in the background, no `hw_lock`; exchanges on it use its port ([decision 92](../embarch-core/decisions/signal-capture.md)).
