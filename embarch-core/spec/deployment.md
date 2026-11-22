# embarch-core spec: Deployment details

**Status:** active, 2026-11-21. Moved verbatim out of [../spec.md](../spec.md) §3 on 2026-11-21 (`tasks/core/131`) when that file was in reserve — reference text, not cut, per [../../DOC-COMPACTION.md](../../DOC-COMPACTION.md) §3.

Index: [../spec.md](../spec.md) §3.

Runs natively on Windows, reachable from WSL2 at the session's dynamic host-gateway IP. Windows Firewall needs no inbound rule under the newer Hyper-V-firewall WSL networking mode. Building natively on Windows needs Visual Studio Build Tools' "Desktop development with C++" workload for `link.exe` — a bare `rustup` toolchain is not enough.

`install`/`uninstall`/`start`/`stop`/`update` **self-elevate** (UAC `runas` on Windows, `pkexec`→`sudo` on Linux, `osascript`→`sudo` on macOS); with no GUI and no TTY they print the command and exit nonzero. `update <new-exe>` must be invoked **from the installed binary's own path**, pointing at the new build — the reverse renames the source aside as its own backup and fails mid-way, leaving the service stopped.

`run` self-detects SCM versus a console and branches internally: an `sc create`-registered binary must call `StartServiceCtrlDispatcherW` and report `SERVICE_RUNNING` within 30 s or SCM kills the start (error 1053).

### Release assets

A `v*.*.*` tag runs `.github/workflows/release.yml`: four targets are built, and one `sign-and-publish` job (in the `release` GitHub environment, owner-approved, `id-token: write` on that job only) signs every archive with Sigstore keyless signing, cosign 3.0.4 or later, and publishes each archive with its `<archive>.sigstore.json` bundle. The signing step sits in `release.yml` itself, never a reusable workflow, so the certificate names this file. **Built 2026-11-17, not yet run: no tag has been pushed since.** Check an asset (cosign 3.0.4 or later):

```
cosign verify-blob embarch-core-<target>.<zip|tar.gz> \
  --bundle embarch-core-<target>.<zip|tar.gz>.sigstore.json \
  --certificate-identity https://github.com/gabrieltetar/embarch-core/.github/workflows/release.yml@refs/tags/v<version> \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

[The proposal](../../embarch-release-signing-proposal.md) holds the design; `embarch verify-release` ([embarch-umbrella](../../embarch-umbrella/spec.md)) checks the same identity for a suite release.
