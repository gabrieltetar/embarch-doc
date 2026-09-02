# embarch-umbrella: open

**Status:** active, 2026-09-02.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **`doctor` check 11 never checks anything, and its stated reason is false.** It returns a hardcoded warn reading *"not available yet — `embarch-study-designer` isn't wired into `embarch-core`/`embarch-api` as a dependency yet"*. **It is a direct dependency of both**, Core has served the version on `/status` since 2026-08-25, and `embarch-api` compares its own compiled copy before every submit. **This is not cosmetic:** on 2026-08-26 the live pair sat at Core wire v13 against a bench flashed to **v14** — a state the handshake refuses correctly and loudly, **but only to whoever calls the handshake endpoint by hand.** `doctor` is the surface whose whole job is saying that without being asked, and it reported "not available yet" the entire time. **The three numbers worth comparing are Core's served host version, the version the located `embarch-api` was built against, and the wire version the bench reports** — all three already reachable from checks 3, 1 and 12. Not built in the pass that found it, because that pass had already moved the wire and **a check that gates deploys is worth its own.**

- **Several later decisions are recorded as designs with no implementation note, and whether each shipped is not established here.** Check 14 (bind address versus topology) is explicitly design-only. Also unconfirmed: `setup --dry-run` (21), the firewall and disk checks (22b, 22c), the MCP-handshake spawn (23), `doctor --prune` (26), and the release version assertion (27/29). Reading the code is the way to close this, not reading this repo.

- **Config fragments or includes**, so the Core section is not duplicated into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s config loader. **Deferred rather than rejected.**

- **The token and config mirrors still have nothing mechanical keeping them in step with `embarch-api`'s originals** (decisions 16, 20). The CI diff job that was supposed to guard them **was never implemented**, and decision 15's reversal removed only the third mirror. Extract them into a shared crate, or build the diff job — the question is open for these two specifically.

- **A user-level service would avoid needing any elevation at all on Linux and macOS** (systemd `--user`, a launch agent), **but would not start before login, which defeats decision 3's whole point.** Not yet weighed properly. Self-elevation also does not help the no-GUI/no-TTY case — CI, a headless remote session — which still needs decision 7's original print-the-command fallback.

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT mode has ever run here, so **what got live-validated is NAT mode.** The ambiguity decision 30 resolves is real either way; what is untested is the mode that creates it.

- **macOS is entirely unvalidated and has no machine to validate on.** Deliberately not blocking: ship it and have a Mac-only engineer walk the guide once the primary topology is proven. **Gatekeeper may also make the "just download and run" promise false there specifically**, since the aarch64 build is unsigned.

- **MCP registration has never been verified for real.** Every walk of the onboarding guide ran from an environment with no agent CLI present, so check 10 could not be exercised. Needs one run from an environment that has it.

- **Whether `init` should warn when a repo holds more than one recorded build** is undecided. It surfaced on a real repo: `init` read whichever recorded build it found first, **which was an ad hoc dev board's rather than the production board the prior config targeted**, and `init` has no way to know which of several past builds is the "real" one. Resolved that day by hand-adding a second project entry rather than picking one — the zephyr-west discovery of decision 17 is the structural answer for a repo shaped that way, but **a static-discovery repo with several recorded builds still silently gets one picked for it.**
