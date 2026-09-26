# PR Quality Checklist

**Run this before every pull request goes upstream. No exceptions.**

This is the ten-minute step that turns a maybe-PR into a merge, and it's the reason maintainers welcome Code Orange instead of muting it. A facilitator should make sure every participant runs it before hitting "Create pull request" or "Comment".

---

## Before you start coding

- [ ] The issue is from [`ISSUE_POOL.md`](./ISSUE_POOL.md), marked LIVE and type BUILD (not random, not already claimed).
- [ ] You commented on the issue (or checked it's unassigned) so two people don't do the same work.
- [ ] You read the repo's **CONTRIBUTING.md**. Each repo has its own rules - follow theirs over any general habit.

## Before you submit

- [ ] **It builds.** The project compiles locally with no new errors (`cargo build`, `go build`, `cmake --build`, `flutter build`... whatever the repo uses).
- [ ] **Tests pass.** The existing test suite is green (`cargo test`, `go test ./...`, `ctest`...). If you changed behavior, you added or updated a test.
- [ ] **Formatted and linted.** You ran the repo's own formatter and linter (e.g. `cargo fmt` + `cargo clippy`, `gofmt`, `clang-format`) and fixed what they flagged.
- [ ] **Scope is tight.** The PR does *one thing* - the thing in the issue. No drive-by changes, no reformatting unrelated files.
- [ ] **It links the issue.** The PR description says `Closes #123` (or `Refs #123`).
- [ ] **Commits are clean.** Clear messages; follows the repo's commit-message style if it has one.
- [ ] **You can explain every line.** If a reviewer asks "why this?", you have an answer. If you can't explain it, it's not ready.

## After you submit

- [ ] Watch for review comments and respond promptly and politely.
- [ ] Expect change requests - that's normal and is part of contributing, not a rejection.
- [ ] When it merges (or closes), log it in the ISSUE_POOL outcomes log.

---

## Before you post a review or test report

Reviews and test reports are real contributions, and they're also the easiest way to add noise. Before you comment on someone else's PR:

- [ ] **You built and ran it**, or you're clear that your comment is conceptual only.
- [ ] **You read the whole thread.** Your point hasn't already been made or answered.
- [ ] **It's specific.** Platform, commit hash, exact commands, what you expected, what happened. "Tested ACK <hash>" plus the steps you ran beats a paragraph of praise.
- [ ] **It's yours.** You understand everything you're saying and could defend it in a follow-up. No pasted AI output, no comments written by a facilitator for you.
- [ ] **It's worth a maintainer's minute.** If you're unsure, discuss it in the Code Orange channel first. Not posting is a fine outcome.

### Test report template

```
Tested <commit hash> on <OS / arch>, <network: regtest/signet>.

Steps:
1. ...
2. ...

Result: <what happened; logs if relevant>
<optional: one question or observation the thread hasn't covered>
```

---

## PR description template

Copy this into the PR body and fill it in:

```
## What this does
<one or two plain sentences>

Closes #<issue number>

## Why
<the privacy or quality problem this addresses>

## How I tested it
- [ ] builds locally
- [ ] tests pass (which ones?)
- [ ] formatter / linter clean
<anything else you checked>

## Notes for the reviewer
<anything you're unsure about, or questions>
```

---

## The one-line standard

> **Would a tired, unpaid maintainer be glad to receive this PR?**

If yes, submit it. If you're not sure, run the checklist again or ask a peer to glance at it first. When in doubt, don't ship it - protecting the relationship is worth more than one extra PR in the count.
