# embarch: feature roadmap

**Status:** draft, 2026-07-20.

## Milestones

### 1 - Flash

Projects : API - Core
The goal is to use the EmbArch suite to flash the firmware to avoid having to forward the USB from windows to WSL2.
Ideally "west flash" can be used.
Steps : [embarch-api/milestone-1.md](embarch-api/milestone-1.md), [embarch-core/milestone-1.md](embarch-core/milestone-1.md)

### 2 - Token

Projects : API - Core
The goal is to replace the insecure `dev-token-change-me` fallback with an auto-generated, machine-wide token file Core persists and embarch-api discovers on its own — no more hand-copying `EMBARCH_TOKEN` between the two. Also folds in the already-diagnosed `sc.exe` Windows-service environment-variable fix. Full target design : [embarch-token.md](embarch-token.md).
Steps : [embarch-api/milestone-2.md](embarch-api/milestone-2.md), [embarch-core/milestone-2.md](embarch-core/milestone-2.md)

## Release

### 1 - Rochambeau
1.x.x
Date : ?
includes : 
Milestone 1
Milestone 2

## Changelog

- 2026-07-20 — Initial draft, Milestone 1 (Flash).
- 2026-07-21 — Added Milestone 2 (Token); added it to Rochambeau's includes list.
