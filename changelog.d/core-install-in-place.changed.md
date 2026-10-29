Windows `install` over a registered service rewrites it in place, keeps its `Environment`, and applies the restart policy via `sc failure` ([decision 106](../embarch-core/decisions/platform.md)).
