# 017 — The gate's blind spot over in-repo sub-crates is described in two places, both partially

**State:** open
**Source:** `inbox/doc-gate-blindness-described-in-one-place.md`, dropped by `agent/api/024-clippy-reaches-the-path-dep-crate` 2026-09-06 as that task's last `Done when` item; `embarch-api` decision 56.
**Scope:** doc
**Hardware:** none
**Owner:** required — `../../embarch-fleet/protocol.md` §10 is the owner's alone. (`embarch.md` §5 is the supervisor's, so **that half alone is not blocked**; see "What is already done".)

## What

Two docs describe the same structural fact from opposite ends, and neither says
it is the same fact:

- `embarch.md` §5's `rustfmt` bullet works out at length that `cargo fmt --check`
  never descends into a local path-dependency crate, and that no single flag
  covers every crate inside a repo and nothing outside it.
- `../../embarch-fleet/protocol.md` §10 lists `cargo clippy --all-targets -- -D warnings`
  as *the* gate command, with no mention that `--all-targets` has exactly the same
  reach problem.

**The clippy half was not theoretical.** `api/024` found a red `unused_imports`
sitting in `crates/embarch-core-client/src/client.rs`, in a crate with 28 unit
tests that no gate command anyone typed had ever compiled, linted or run —
invisible to a root gate that had been green for weeks.

The underlying fact is one sentence: **a cargo command run at a repo root reaches
the packages it selects, and a path dependency that is not a workspace member is
not one of them** — for `fmt`, for `clippy --all-targets`, and for `test` alike.
Written once it is a thing a reader carries to the next crate. Written as an fmt
anecdote in one doc and an unqualified command list in another, it is two facts
that each look local.

## What is already done, so nobody re-derives it

**The drop's cheap, high-value item is closed. Leg 018 ran the sweep, 2026-09-06,
and the answer is that no other repo is behind this blind spot.**

Across all six Rust repos, **`embarch-api/crates/embarch-core-client` is the only
nested in-repo crate in the suite** — the only `Cargo.toml` below a repo root
(excluding `target/`), and the only `path =` dependency that points *inside* its
own repo. Every other `path =` in the suite points sideways into a sibling repo
(`../embarch-…`), which is the *over*-reach problem, not the missed-crate one.
`embarch-api` is also the only repo that declares a `[workspace]` at all, and
after `api/024` its one member is covered by `default-members`.

So the general remedy is documentation, not a second fix: **there is nothing else
currently hiding, and the value of writing it down is that the next in-repo crate
anyone adds does not hide either.**

## Why now

The reason is currently written down, in `embarch-api` decision 56 and in
`embarch.md` §5's bullet, both within two days. It gets more expensive to
reconstruct every week, and the next person to hit it will hit it the way
`api/024` did — by running a command from the wrong directory by accident.

## Done when

- [x] `cargo metadata`-equivalent sweep of every Rust repo, recording which
      contain an in-repo crate that is not a workspace member. **Answer: only
      `embarch-api`, and it is fixed.** Recorded above rather than only in a log
      entry, because a measurement that lives in one leg's entry is one nobody
      finds.
- [ ] `embarch.md` §5's `rustfmt` bullet says the reach problem is not specific to
      `fmt` and cites the clippy instance rather than repeating the argument.
      **Sequencing:** its `-p` sentence was separately wrong and was corrected in
      leg 018's `api/024` fold from `status.d/api-fmt-p-is-now-an-escape-hatch.md`;
      do not re-derive that. **And do not write this into the existing bullet
      without reading `tasks/suite/008` first** — that task exists because this
      bullet has already absorbed three rounds of decision text and should be
      moved to a home of its own rather than grown a fourth time.
- [ ] `../../embarch-fleet/protocol.md` §10 says what its `cargo` bullet actually
      covers — the packages it selects — or the fleet accepts that it does not and
      says so where a worker reads it. **Owner-only.**
- [ ] `changelog.d/` fragment if anything changed. Gate green.
