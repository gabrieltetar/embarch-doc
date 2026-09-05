# embarch-umbrella decisions: Version and schema skew

**Status:** active, 2026-09-04.

What checks 11 and 15 compare, where each number comes from, and why a mismatch between two halves of an install warns rather than refuses. Which checks are built and which are not is [../spec.md](../spec.md)'s table, not repeated per entry here.

Index: [../decisions.md](../decisions.md). The rest of the chain: [doctor.md](doctor.md).

### 24 — Version skew between Core and the API stays a warning, not a refusal

Kept deliberately rather than escalated: **refusing to run a mismatched pair would obstruct the exact in-development, fast-iterating state this suite is still in**, with independent per-repo releases and a warn-not-refuse precedent already set elsewhere. **Revisit only once a mismatch is more likely an operator mistake than an expected in-progress state.**

### 33 — Check 11 compares real numbers, and says which one it could not get

The check returned a hardcoded warn — *"not available yet, `embarch-study-designer` isn't wired into `embarch-core`/`embarch-api` as a dependency yet"* — after that had stopped being true. **It is a direct dependency of both**, and a live pair once sat at Core wire v13 against a bench flashed to v14 while this check reported "not available yet" the whole time. The handshake refused that state correctly and loudly, **but only to whoever called it by hand**; saying it unasked is the entire job of the surface that was silent.

**Two comparisons, and they are not two of a kind** (decision 36 adds a fourth number that is neither).

- **Core's served `study_designer_schema_version`** versus **the `HOST_TYPE_SCHEMA_VERSION` the located `embarch-api` compiled** (decision 35) — the `embarch-api`⟷`embarch-core` hop, the one `embarch-api` itself refuses to submit a `Study` across. A difference is a **fail**: the pair cannot run a study at all.
- **The bench's wire version** cannot be compared against either of those. `DEV_BENCH_WIRE_SCHEMA_VERSION` counts its own sequence and is only guaranteed `<=` the host one, so equality means nothing and inequality means less. What *is* comparable is `/dev-bench/hello`'s `compatible` — **Core's own verdict**, Core comparing the bench's number against the wire constant Core compiled. Core's wire constant is served nowhere, so recomputing the verdict here would be a mirror with nothing to mirror.

**The stand-in is gone.** This binary's own constant stood in for the located `embarch-api`'s until 2026-09-04, exact only where check 1's manifest agreed: decisions 35 and 36 replace it and say what became of it.

**A missing number is a skip that names it, never a pass.** Core unreachable, no token, no bench, a `409` mid-study, a Core predating the field: each is a distinct `Warn` carrying its own reason, and the numbers that *were* obtained are still printed. A `Fail` always outranks a skip, so an absent bench cannot mask a host disagreement.

**`/dev-bench/hello` is fetched once for checks 11 and 13.** It is not a read — it opens the serial link long enough to handshake — so two checks asking separately would be two link opens for one answer. The visible consequence: the handshake now runs even when no dev-bench checkout is configured, where check 13 alone used to skip before calling it.

**The comparison is a pure function over injected numbers**, which is what lets the whole matrix be tested with no Core, no bench, no network and no `embarch-api` on disk — the check that gates deploys being untestable without the hardware it gates was most of why it stayed a stub.

### 34 — Check 15: `core_version` is a different question, so it is a different check

`GET /status` also serves `core_version` (`embarch-core` decision 13). **It is deliberately not one of check 11's three numbers.** Schema skew asks whether the pieces agree on a wire contract; this asks whether the Core answering on the network is the binary that was last built and deployed — and folding it into check 11 would present one verdict over two unrelated questions.

It compares `/status`'s `core_version` against the located `embarch-core` binary's own `--version`, both of which `doctor` already has. **`deploy-core` has printed `landed` twice in one session with nothing installed**, when the elevated child was cancelled ([embarch-dev-workflow.md](../../embarch-dev-workflow.md) §4a), and its own check compares byte *length*, which cannot discriminate a release rebuild of one constant.

**The limit is stated in the check's own output, not only here:** `core_version` is `CARGO_PKG_VERSION`, so it moves only when the crate version does. This catches a **cross-version** stale deploy and is blind to a same-version one. Strictly better than nothing, and not a hash comparison — a test asserts the blind spot rather than leaving it to the prose.

**Warn, never fail**, following `embarch-core` decision 13's "consumers warn, never refuse" and decision 24 above: independent per-repo versions are an expected state in a suite iterating this fast.

### 35 — Check 11 asks the located `embarch-api` for the host number, and a number it cannot get is its own verdict

The number the study hop turns on is the one **`embarch-api`** compiled, not the one `embarch` did, and `embarch-api --json versions` now states it while loading no config and contacting no Core ([embarch-api](../../embarch-api/decisions/surface.md) 52). Check 11 shells out for it, on decision 31's reasoning: it is a fact about a *different binary*, and only that binary can state it. **`--json` goes before the subcommand** — it is a top-level flag and not `global`, so `embarch-api versions --json` exits 2 [verified 2026-09-04]. The *installed* binary answers with `host_type_schema_version` v17, debug and release alike, and Core's `/status` carries `study_designer_schema_version` — check 11 read all three and agreed [measured 2026-09-05, owner's machine].

The number is therefore fallible where it used to be a compile-time constant: `embarch-api` not located, too old to know `versions` (clap exits 2, reported as what it predates, as check 14 does for an older Core), not executable, or an object without the field. **Each is a `Warn` naming which — never a fall back to this binary's own copy.** A fallback would report a clean pass on exactly the hand-built mixed install the check exists to catch, and **"could not ask `embarch-api`" is a different fact from "they disagree"**; a test pins that the two reach different verdicts on the same numbers.

### 36 — `embarch`'s own constant survives as a fourth number, and can only warn

Kept rather than dropped. It is free — a compile-time constant of the binary already running — and an `embarch` that disagrees with the `embarch-api` it has just located **is itself a mixed install**, which nothing else here notices on a machine with no suite manifest for check 1 to read, which is the hand-built case.

**It can never fail the check.** `embarch` submits no studies, so its number blocks nothing that works; the fix line is check 1's reinstall, not a redeploy. Where `api_host` could not be read at all it is still printed, labelled context and explicitly not a stand-in (decision 35).
