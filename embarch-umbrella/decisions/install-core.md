# embarch-umbrella: decisions — `install-core`

**Status:** active, 2026-11-25. Index: [../decisions.md](../decisions.md). Verb: [../spec/commands.md](../spec/commands.md); record: [../interfaces/install-core.md](../interfaces/install-core.md).

### 61 — `install-core` verifies a signed release in an admin-only staging folder before anything is recorded (EMB-338)

Step 4 of [the release-signing proposal](../../embarch-release-signing-proposal.md), unit A.19 of the HIL attested phase. `setup` copies per-user (decision 28) and trusts the folder it runs from; a release that must be trusted by an elevated step cannot be checked where the engineer's account can still write it, so the check moves **after the copy into a folder only Administrators or root can write**. The proposal's design is not reopened: `verify_release` (decision 14, [verify-release](../interfaces/verify-release.md)) is the check, unchanged.

**Shape.** `embarch install-core <release dir or archive> [--allow-downgrade] [--dry-run]` builds a plan, prints it, and, unless `--dry-run`, runs the elevated half, a function that takes its data dir, a verifier and the time. `<data dir>/release-staging/<n>/` is created `0700` on Unix and, on Windows, with inheritance removed and Administrators and SYSTEM granted (`icacls`); the engineer-writable firmware `staging/` is a different folder. The release is copied there (an archive is unpacked there with `tar`, which reads tar.gz everywhere and zip on Windows 10 or later), the manifest's folder is found (the staging folder, or its one subfolder), `verify_release` runs **on that copy**, the suite version is compared with `installed-release.json`, and the record is written by temp file and rename.

**A failed check writes nothing.** The staging folder the run made is removed and an existing record is not touched. A passing run keeps its staging folder: it is the verified copy the later steps install from.

**Downgrade.** An older suite than the installed one is refused unless `--allow-downgrade`; then it installs and the record says `allow_downgrade` and `downgraded`, with the version it replaced. Versions order as `major.minor.patch[-pre]`, a pre-release before its release; **a version that does not parse has no order, so it is refused too unless the flag is passed** (fail closed; the suite's tags are all that shape).

**Seams.** The verifier is a `&dyn Fn(&Path)`, so tests use a fake and need no signature; the folders are arguments, so tests run as an ordinary user in temp dirs. `--data-dir` overrides the default (`/var/lib/embarch`, `%ProgramData%\embarch`). The trust-root flags are `verify-release`'s.

**Later units, named so they are not assumed done:** re-launching itself elevated (today the caller must already hold the privilege, and without it the staging folder fails to create); installing the verified binaries from staging; registering the service under its own account (Windows and Linux), which is Core's `install --service`; `setup` calling this instead of copying; WSL2 hosts (the data dir is the Windows one); and pruning old staging folders. **Measured vs assumed:** the `icacls` grant type-checks for the Windows target but has never run, and the real signature path is the one `verify-release` already tests; here it is a fake. The command's name is the plan's recommendation; the owner may strike it.

**Reversal:** the owner renames or folds the verb into `setup`, or the proposal's order changes.
