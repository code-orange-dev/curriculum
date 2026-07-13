# Curated Issue Pool

**The single source of contribution targets for the Privacy Track.** Participants pick from here - never from random hunting across GitHub. This is the guardrail that lets us ship high volume without becoming noise to maintainers.

> **Rule:** If an issue isn't in this file (or just got verified by a curator), it is not a valid target for a session. No exceptions.

---

## How this pool stays healthy

A curator (a tutor or experienced participant) keeps this list fresh. An issue earns a spot only if it passes all four checks:

1. **Still open.** Verified open on GitHub within the last 7 days.
2. **Genuinely wanted.** Labeled `good-first-issue` / `help-wanted`, or explicitly confirmed welcome by a maintainer. Not a stale wishlist item, not something with an open PR already.
3. **Beginner-appropriate.** Scoped so someone could plausibly finish it in or shortly after a session. Docs, tests, examples, small fixes.
4. **Not already claimed.** Nobody else is mid-PR on it.

Re-verify the whole pool **weekly**. Mark anything that goes stale as `RETIRED` (don't delete - the history is useful). Aim for **5–10 live issues per repo** at any time.

---

## The maintainer-DM sourcing playbook

This is how we turn "we know a few maintainers" into the warmest possible issue pipeline - and into Code Orange's real long-term asset.

**The goal:** a handful of maintainers who think of Code Orange as *"the program that sends me prepared contributors,"* and who occasionally point us at issues they'd actually love help on.

**The opening DM (adapt per person):**
> Hey [name] - I run Code Orange's Bitcoin Privacy Track. We teach curious Bitcoiners and guide each one to a real, well-prepared PR (they run a build/test/CONTRIBUTING checklist before submitting - we're careful not to add noise). [repo] is one of the projects we contribute to. Are there a few issues you'd genuinely welcome outside help on - especially `good-first-issue`-type work? Happy to point our people only at things you actually want touched.

**Why this works:** it leads with respect for their time, signals we have a quality floor, and asks them to *pull* work toward us rather than us pushing PRs at them.

**After the first merge:** send a short thank-you and ask "anything else in this vein?" That loop is the whole game.

**Repos to open this conversation with first** (warmest, most beginner-friendly): **rust-bitcoin**, **Floresta**, then **BDK** and **Payjoin Dev Kit**.

**Sourcing checklist for each repo:**
- [ ] Identify 1–2 active maintainers (recent commits / review activity).
- [ ] Send the opening DM.
- [ ] Read their CONTRIBUTING.md and link it in the pool entry.
- [ ] Subscribe to their `good-first-issue` label.
- [ ] Log their response and any issues they flag, below.

---

## Live issues by repo

> Curators: fill `#`, title, link, label, difficulty, and the maps-to session. Keep entries one line where possible. `STATUS`: LIVE / CLAIMED / RETIRED.

### rust-bitcoin  🟢
CONTRIBUTING: _link here_ · Maintainer contact: _DM status here_

| # | Title | Link | Label | Maps to | Status |
|---|---|---|---|---|---|
| _tbd_ | _e.g. clarify docs on Transaction fields_ | _url_ | good-first-issue | F1, F2, T3 | LIVE |

### Floresta  🟢
CONTRIBUTING: _link here_ · Maintainer contact: _DM status here_

| # | Title | Link | Label | Maps to | Status |
|---|---|---|---|---|---|
| _tbd_ | _e.g. improve node setup docs_ | _url_ | good-first-issue | N2, N3 | LIVE |

### BDK (bdk_wallet)  🟡
CONTRIBUTING: _link here_ · Maintainer contact: _DM status here_

| # | Title | Link | Label | Maps to | Status |
|---|---|---|---|---|---|
| _tbd_ | _e.g. add tests for coin selection_ | _url_ | help-wanted | T1, T2 | LIVE |

### Payjoin Dev Kit (rust-payjoin)  🟡
CONTRIBUTING: _link here_ · Maintainer contact: _DM status here_

| # | Title | Link | Label | Maps to | Status |
|---|---|---|---|---|---|
| _tbd_ | _e.g. expand async example_ | _url_ | good-first-issue | C1, C2 | LIVE |

### Silent Payments tooling  🟡
CONTRIBUTING: _link here_ · Maintainer contact: _DM status here_

| # | Title | Link | Label | Maps to | Status |
|---|---|---|---|---|---|
| _tbd_ | _e.g. document address derivation_ | _url_ | good-first-issue | S1, S2 | LIVE |

### Kyoto  🟡
CONTRIBUTING: _link here_ · Maintainer contact: _DM status here_

| # | Title | Link | Label | Maps to | Status |
|---|---|---|---|---|---|
| _tbd_ | _e.g. clarify filter-sync docs_ | _url_ | good-first-issue | N1, S2 | LIVE |

---

## Retired / merged log

Keep a running record - it's how we report "merged PRs" and spot which repos are working.

| Date | Repo | # | Contributor | Outcome (MERGED/CLOSED) | Notes |
|---|---|---|---|---|---|
| _tbd_ | | | | | |
