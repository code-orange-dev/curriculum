# PR Quality Checklist

**Run this before every pull request goes upstream. No exceptions.**

This is the ten-minute step that turns a maybe-PR into a merge - and the reason maintainers welcome Code Orange instead of muting it. We ship volume; this is how we keep that volume *respected*. A tutor should make sure every participant runs it before hitting "Create pull request."

---

## Before you start coding

- [ ] The issue is from [`ISSUE_POOL.md`](./ISSUE_POOL.md) and marked LIVE (not random, not already claimed).
- [ ] You commented on the issue (or checked it's unassigned) so two people don't do the same work.
- [ ] You read the repo's **CONTRIBUTING.md**. Each repo has its own rules - follow theirs over any general habit.

## Before you submit

- [ ] **It builds.** The project compiles locally with no new errors (`cargo build`).
- [ ] **Tests pass.** The existing test suite is green (`cargo test`). If you changed behavior, you added or updated a test.
- [ ] **Formatted and linted.** You ran the repo's formatter and linter (usually `cargo fmt` and `cargo clippy`) and fixed what they flagged.
- [ ] **Scope is tight.** The PR does *one thing* - the thing in the issue. No drive-by changes, no reformatting unrelated files.
- [ ] **It links the issue.** The PR description says `Closes #123` (or `Refs #123`).
- [ ] **Commits are clean.** Clear messages; follows the repo's commit-message style if it has one.
- [ ] **You can explain every line.** If a reviewer asks "why this?", you have an answer. If you can't explain it, it's not ready.

## After you submit

- [ ] Watch for review comments and respond promptly and politely.
- [ ] Expect change requests - that's normal and is part of contributing, not a rejection.
- [ ] When it merges (or closes), log it in the ISSUE_POOL merged log.

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
- [ ] `cargo build` passes
- [ ] `cargo test` passes
- [ ] `cargo fmt` / `cargo clippy` clean
<anything else you checked>

## Notes for the reviewer
<anything you're unsure about, or questions>
```

---

## The one-line standard

> **Would a tired, unpaid maintainer be glad to receive this PR?**

If yes, submit it. If you're not sure, run the checklist again or ask a peer to glance at it first. When in doubt, don't ship it - protecting the relationship is worth more than one extra PR in the count.
