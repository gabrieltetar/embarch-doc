# 009 — `interfaces/config.md` states two config fields as truth; neither exists

**State:** open
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "Decisions 20 and 21 describe config that does not exist — no `default_target`, no `["none"]` snippet, though `interfaces/config.md` states both as truth. **Build, or retire both.**"
**Scope:** api
**Hardware:** none

## What

`embarch-api` decisions 20 and 21 describe config that was never built: there is no
`default_target`, and no `["none"]` snippet. `interfaces/config.md` nonetheless
documents both as though they exist, so **anyone reading the interface doc and
writing that config gets an error the doc says cannot happen.**

Decide, per field, and do one of two things:

- **Build it** — implement the field, honour it, and test it.
- **Retire it** — remove it from `interfaces/config.md`, and amend decisions 20 and
  21 to say so with the reason. Do **not** leave a decision reading as settled and
  shipped: `embarch-decision-reversals.md`'s shape 1 is exactly this, and it records
  that "a decision recorded as settled — even one carrying its own note that it is
  unbuilt — is indistinguishable in a later reader's eyes from one that shipped."

Either answer is legitimate and it is yours to make within `api`
(`../../embarch-fleet/protocol.md` §5 rule 4). The one outcome that is not
acceptable is the current one, where the doc asserts something false.

## Why now

An interface doc that lies is worse than a missing feature, and this one is the file
a consumer configures from. It also sits next to a related live gap — task 010, the
`[[projects.targets]]` menu that cannot be picked from — so whichever way 020/021
go should be consistent with that, and this task should be worked first if both are
in the queue.

## Done when

- [ ] Each of `default_target` and the `["none"]` snippet is either built and tested,
      or removed from `interfaces/config.md` with its decision amended to say it was
      retired unbuilt and why.
- [ ] The `embarch-api/open.md` bullet is answered and removed, or narrowed to what
      is genuinely left.
- [ ] `changelog.d/` fragment dropped; `status.d/` fragment for any suite-level fact
      this makes false; `suite/user-guide.md` checked for either field (a
      `status.d/` fragment if it names one — you do not edit that file yourself).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
