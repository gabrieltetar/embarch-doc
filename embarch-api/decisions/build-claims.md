# embarch-api decisions: What a study tells Core about its build

**Status:** active, 2026-11-21.

Index: [../decisions.md](../decisions.md). Tools: [../interfaces/studies.md](../interfaces/studies.md). Core's side: [`embarch-core` decision 110](../../embarch-core/decisions.md) (`decisions/signing.md`).

### 111 — `run_study` sends the project checkout's commit, dirty state and `west` version, each only when read

**What.** Core's `POST /study` and `POST /host-studies` take `build_commit`, `build_dirty` and `build_toolchain` and record them under the signed run record's `claimed.build`, apart from what Core observed. `run_study`, as the MCP tool and as the CLI, sends them. They are claims: Core cannot check them, and neither can this crate beyond reading them off the machine.

**Where each comes from.** The project is the one the ledger row already uses (decision 98): the one named, else this session's desk's.
- `build_commit` is `git rev-parse HEAD` in the project's `source_path`, the full 40 characters.
- `build_dirty` is whether `git status --porcelain --untracked-files=no` prints anything: tracked files differ from `HEAD`. Untracked files do not count, the reading `build.rs` already stamps this binary with.
- `build_toolchain` is the first line of `west --version` for a `discovery = "zephyr-west"` project, run with that project's `west_binary`. "Toolchain" here is the build tool, not the compiler: it is the one version this crate can read without running a build, and the SDK or compiler behind it is not recorded. A `static` project's `build_command` is an arbitrary program this crate will not run a second time to ask its version, so it sends none.

**What is sent when only some are known.** Each parameter is sent only when read, so any subset goes out, in the order above. A directory that is not a git work tree, a failing `git`, or a project that does not resolve sends none of the three, never a placeholder: an absent parameter reads as "not claimed", a made-up one as a fact.

**The claim is the checkout, not the flash.** `--reflash none` runs against firmware already on the DUT, so the commit sent is what the project's tree is at, not proof it is what the board runs. That is why it is a claim; the ledger row (98) carries the same reading.

**A host study sends none.** `run_host_study` has no project and runs no build, so there is no build to claim; `post_host_study_claiming` exists on the client and the route accepts the parameters, and a caller that has one can send it. Not decided here: whether `run_host_study` should take an optional `project`.

**In `embarch-core-client`, additively.** `BuildClaims { commit, dirty, toolchain }`, `post_study_claiming` and `post_host_study_claiming`. `post_study(study, run)` and `post_host_study(study)` stay with their signatures and now delegate with `BuildClaims::default()`, byte-identical on the wire. The claims are not a field of `StudyRunOptions`: `embarch-ui` builds that with a struct literal, which a new field would break.

**Measured vs assumed.** Tested: the three parameters on the request through the CLI subprocess against a mock Core, none for a project with no git checkout, both routes at the client, and the urlencoding. **Not run:** against a real Core, and through an MCP subprocess (no harness drives one; the MCP call site is the same `build_claims::for_project` call the CLI makes).
