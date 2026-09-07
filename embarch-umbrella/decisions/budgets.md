# embarch-umbrella decisions: How long `doctor` waits, and what it says when nothing came back

**Status:** active, 2026-09-06.

A new mission split off [doctor.md](doctor.md) rather than added to it, and **nothing was moved**: that file's mission is *what is checked*, and this one is *how long each remote call is given before it is written off, and how a call that did not come back is named*. A reader here is holding a stopwatch or an error string, not a checklist.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Which checks compare what: [schema-skew.md](schema-skew.md).

### 44 — Every remote call's budget is sized for what Core must do to answer *it*, and the constants are separate

`doctor` gave `GET /dev-bench/hello` the same **500 ms** it gives `GET /status`, through one constant every caller of `authed_get` inherited. That call is not a read: **Core opens the bench's serial link, completes the `Hello`/`HelloAck` handshake, takes the boot log the bench flushes only after that ack (`embarch-core` decision 37) and closes the link again** before it has anything to say.

**Three live runs said so** [measured 2026-09-06, primary `wsl-host` bench, both boards attached, enrolled and validated]: checks 11 and 13 reported *unavailable* while Core's own `dev-bench.log` recorded all three handshakes completing — one `--- link opened on COM17 (firmware 49958d34, wire schema v15) ---` per invocation. **The endpoint answered every time and `doctor` stopped waiting.** Since `/dev-bench/hello` is the only source of Core's `compatible` verdict ([decision 33](schema-skew.md)), checks 11 and 13 could not finish on *any* bench whose handshake outlasts half a second — which is why weeks of "needs a bench" was the wrong diagnosis, not a slow one.

**The ladder is what Core must do, not which endpoint it is:**

| what Core does before it can answer | calls | constant |
|---|---|---|
| enumerates devices; opens no link, takes no `hw_lock`, waits on no board | `/status` (`hardware::list_probes`), `/dev-bench/port` (`resolve_dev_bench_port`) | `DEVICE_SCAN_GET_TIMEOUT`, 500 ms |
| opens the bench's serial link and waits for a board to answer | `/dev-bench/hello` | `LINK_HANDSHAKE_GET_TIMEOUT`, 10 s |

**Two named constants, not one made bigger.** Widening the single one would buy the handshake its time by handing a device scan twenty times what it has ever needed, and `doctor`'s shortness on the cheap calls is [decision 11](reporting.md)'s split doing its job. Two names also make the ladder readable at the call site, where the defect actually was.

**Both budgets are now measured, and the ladder is the shape the measurement found** [measured 2026-09-07 ~01:52 MDT, primary `wsl-host` bench, both boards attached, enrolled and validated, three authenticated GETs per route one second apart]:

| route | three runs | budget | headroom |
|---|---|---|---|
| `/dev-bench/port` | 5.8, 12.5, 5.0 ms | 500 ms | ~40–100× |
| `/status` | 126.5, 99.6, 100.0 ms | 500 ms | ~4–5× |
| `/dev-bench/hello` | **719.7, 730.1, 746.9 ms** | 10 s | ~13× |

**The handshake costs about 0.73 s, so the 500 ms it used to inherit was short by roughly 230 ms — 1.4× under, not orders out.** That is the uncomfortable number in this table: a budget wrong by half a second is exactly the kind that reads as an intermittent bench rather than as a wrong constant, and it held checks 11 and 13 dark for weeks. Nothing about the fix depended on knowing it, and every one of the three runs above cleared 10 s by more than an order of magnitude, so the value stands unchanged — but it is now sized against something instead of against `MCP_HANDSHAKE_TIMEOUT`. `/dev-bench/port`'s place on the scan budget was an argument from what Core does for it and is now also a measurement; it is the cheapest call of the three.

**A budget is spent only by a call that does not answer**, so a generous one costs a healthy run nothing and a wrong one shows up as decision 45 below's named timeout rather than as a mystery.

**The budget is now a parameter of `authed_get`, not a constant read inside it.** The defect was inheritance: a third call site was added to a helper that had already chosen for it. A parameter makes the next one state which kind of call it is, and a caller that guesses wrong is at least visible in the diff.

**The durable rule, which outlives these two numbers:** a check whose remote call makes another process do real device work is not on the same clock as one that reads state, and a shared timeout constant will silently put it there. Reading its name is no defence — the constant this one inherited described itself accurately as "an authenticated request to an already-resolved `base_url`", which `/dev-bench/hello` *is*, and which says nothing about what answering it costs.

**Verified on a bench** [2026-09-07, `tasks/umbrella/034`]. `embarch doctor` on the primary `wsl-host` bench now prints check 11 as **PASS**, and its `compatible` verdict — the field this whole chain exists to read, never once read before — is *"dev-bench wire: bench reports v15, and Core accepts it"*, `{"schema_version":15,"compatible":true}` off the raw body. **Check 13 got its first real comparison too, and it is a `FAIL` whose fix line cannot clear it** — [../open.md](../open.md) carries what that turned out to be. No decision is amended for it: the budget half of this debt is closed, and what replaced it is a question about check 13's *baseline*, not about a clock.

### 45 — A call that did not come back says whether the clock ran out or the connection never came up

**Why this sits with the budgets and not with the check chain:** it is the only thing that can tell a wrong budget from an absent Core, and a wrong budget is invisible without it.

Every failed `authed_get` printed `request to <url> failed: error sending request for url (…)`. **`reqwest::Error`'s `Display` drops its source**, and a request that timed out and a connection that was refused render as *the same sentence apart from the URL* [measured host-side 2026-09-06 against a loopback socket, pinned by `reqwests_display_alone_does_not_say_which_failure_it_was`]. So the three runs above printed evidence that could not, by itself, say which had happened, and the diagnosis rested on two other facts: the same client, base URL and token got a `200` from `/status` in the same run, and the source has exactly one timeout on that path. **That inference is strong and it is still an inference** — no run has yet printed a message able to settle it.

What is printed now: a verb, then the chain *below* `reqwest`'s own layer. **A timeout names the budget it exceeded** (`timed out after 10000 ms`), because that number is this module's own and is the thing to change; **a refusal names the connection** (`could not connect: … tcp connect error: …`), because nothing here can widen its way past one. Where both predicates are set, the timeout wins and the number is kept. `reqwest`'s outer layer is skipped rather than repeated: it renders the URL this sentence already carries, and repeating it pushes the part that carries the diagnosis off the end of the line.

**Foreign text is flattened to one line where this module introduces it** — [decision 43](reporting.md)'s own prescription, applied at the interpolation point rather than widened into an exemption. This is that fix at one site and deliberately not the general one: check 1 still interpolates `embarch-core --version`'s stdout unnormalised (`tasks/umbrella/031`).

**What it does not do is re-read the past.** The three runs are gone; this changes what the *next* one prints. That is the point — the debt in [../open.md](../open.md) is now settleable by a single run either way, where before a failure and a timeout looked alike.
