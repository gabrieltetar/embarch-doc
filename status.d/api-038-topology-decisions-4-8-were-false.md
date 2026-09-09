**Target:** embarch-topology/decisions/crate.md — decisions 4 and 8
**Was:** Decision 4: "the software-class detection then mirrored between
`embarch-api` and `embarch-umbrella` all move here as the sole implementation.
The mirrored-copy CI diff job becomes obsolete: there is nothing left to
mirror once everyone links the same crate." Decision 8: "there is no way for
the two to disagree, since there is only one of them."
**Now:** Both were false as written. `embarch-api/crates/embarch-core-client`
already linked `embarch-topology` and still ran its own second, narrower WSL2
predicate (`token_discovery::is_wsl2`) beside `detect_wsl2` — the same binary
carried two rules that could disagree, unit-tested only against each rule's
own expectations, so nothing compared them. Fixed on the `api` side
(`embarch-api` decision 62, `tasks/api/038`): `token_discovery::is_wsl2` now
delegates to `embarch_topology::software::detect_wsl2`. The general claim
still needs qualifying either way: linking the crate stops a mirrored *copy*
of the crate's own logic, it cannot stop a caller from writing a second,
unrelated predicate next to the call it never makes — worth a line in
`crate.md` saying so, since decision 8's "there is no way…since there is only
one of them" is true only inside the crate's own boundary.
