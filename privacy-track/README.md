# Code Orange · Bitcoin Privacy Track

**The Privacy Sessions: 12 biweekly, 90-minute, drop-in sessions. Season One opens with Silent Payments.** [Full session guide with facilitator prep →](./SESSIONS.md)

| Month | Sessions |
|---|---|
| 1 | **S1** Silent Payments I: One Address, No Trail · **S2** Silent Payments II: Finding Your Money |
| 2 | **S3** Silent Payments III: Review Club · **S4** Think Like the Adversary |
| 3 | **S5** Coin Selection & Change · **S6** Payjoin |
| 4 | **S7** Light Clients & Your Own Node · **S8** The Network Sees You (Tor, BIP324, private broadcast, ASmap) |
| 5 | **S9** CoinJoin & OpenSwap · **S10** Lightning Privacy |
| 6 | **S11** Ecash: Cashu & Fedimint · **S12** Contribution Sprint |

---

## Why this track exists

Bitcoin's base layer is public by default. Most of the privacy failures people actually hit aren't in the protocol. They're in **wallet behavior**, **how transactions get built**, and **how they get broadcast**: reusing an address, picking change badly, a wallet's fingerprint, a light client that tells a server every address you own, a broadcast that leaks your IP. Those are software problems, and open-source contributors can fix them.

This track teaches those problems one at a time, with the code open on screen, and connects every topic to a live project where the fix is being written.

## Why start with Silent Payments

Because it's landing right now. Bitcoin Core merged the BIP352 core logic in September 2026 ([#35301](https://github.com/bitcoin/bitcoin/pull/35301)), libsecp256k1 v0.8.0 ships a `silentpayments` module, and wallets like Dana, Cake, BlueWallet, Sparrow and our own community's [Shroud](https://github.com/CypherCommons/shroud) are shipping support. Sending and receiving in Core are in review. Participants can build the protocol from scratch (S1-S2) and then review the real implementation while it's still open (S3).

## How it works

- **Online, global, drop-in.** Every session stands alone. You'll never be lost because you missed last time
- **Hands-on every time.** You build or run something on your own machine: a Silent Payments sender graded against the official BIP352 vectors, a node, a payjoin, a swap
- **Review-first.** Every session reads a real open PR together. We learn to build, test and explain other people's work, which is how contributors earn trust
- **Proof of work, not attendance.** You leave with a concrete next step: a finished lab, a tested PR, a reproduced bug, a doc fix, or a PR from the [curated pool](./ISSUE_POOL.md)

## Where it fits

The Privacy Sessions are the open, drop-in layer of Code Orange's [Privacy Contributor Program](https://github.com/code-orange-dev/code-orange-dev/tree/main/privacy-contributor-program):

```
Workshops & meetups ──> The Privacy Sessions (this track) ──> Privacy Review Club ──> Rotations & residency ──> Fellowship / grant
   curious                 learn + build + first review        regular reviewer         one project, deep          independent
```

Anyone can join the sessions. People who keep coming back and produce proof of work get invited into the Review Club and the contributor pathway. See [fellowships](https://github.com/code-orange-dev/fellowships).

## Labs

All labs run offline with plain Python 3.8+. No installs.

| Lab | Session | What you build |
|---|---|---|
| [silent-payments](./labs/silent-payments/) | S1, S2 | A BIP352 sender and scanner graded against the 28 official test vectors, plus a scanning-cost benchmark |
| [chain-analysis](./labs/chain-analysis/) | S4 | The core heuristics (CIOH, change detection, clustering) on sample transactions |
| [coin-selection](./labs/coin-selection/) | S5 | Four selection algorithms, scored on fees vs privacy |
| [compact-block-filters](./labs/compact-block-filters/) | S7 | A simplified BIP158 filter: Golomb-Rice coding, matching, false positives |

```bash
git clone https://github.com/code-orange-dev/curriculum
cd curriculum/privacy-track/labs/silent-payments
python3 run_vectors.py send
```

## For facilitators

**You don't need to be a deep technical developer to host.** You need to be curious, one session ahead of the room, and honest when you don't know. "Let's find out together" models exactly what a good contributor does.

1. **Do the hands-on yourself first.** Every session in [SESSIONS.md](./SESSIONS.md) has a prep line. If you can do it, you can host it
2. **Teach the why, then show where it lives in code.** The repo's own docs handle the how
3. **Protect the relationship with maintainers.** Contributions come from the [curated pool](./ISSUE_POOL.md) and pass the [PR checklist](./PR_CHECKLIST.md). Review comments go upstream only when they're genuinely useful. The privacy world is small, and a reputation for noise closes doors for everyone after us

Full guide: [FACILITATOR_GUIDE.md](./FACILITATOR_GUIDE.md).

## The contribution ladder

Enter at any rung. There's no pressure to climb.

1. **Engage:** build a repo, read the code, join its chat
2. **Test:** build someone's PR, run it, report exactly what you did and saw
3. **Fix:** docs, error messages, small clarity improvements
4. **Cover:** add tests. Maintainers love it, and it teaches you the code
5. **Review:** explain a PR, challenge an assumption, find an edge case
6. **Build:** fix a real bug or implement a scoped feature, then see it through review
7. **Lead:** curate the pool, host a session, mentor newcomers

## What we measure

In the order that matters (details in the program's [MEASUREMENT.md](https://github.com/code-orange-dev/code-orange-dev/blob/main/privacy-contributor-program/MEASUREMENT.md)):

1. **Retention:** are people still contributing to a privacy project 3, 6 and 12 months later?
2. **Useful upstream activity:** reviews, test reports, reproduced bugs, tests, docs and merged code, counted separately
3. **Maintainer sentiment:** do maintainers want our contributors back? This is the asset that compounds
4. **Return attendance:** drop-in is the model, and coming back is the signal it works

## Files

| File | What it's for |
|---|---|
| [SESSIONS.md](./SESSIONS.md) | The 12 sessions: beats, prep, hands-on, PRs, follow-ups |
| [FACILITATOR_GUIDE.md](./FACILITATOR_GUIDE.md) | Running a session: checklist, Review Circle rules, troubleshooting |
| [ISSUE_POOL.md](./ISSUE_POOL.md) | Verified contribution targets, mapped to sessions |
| [PR_CHECKLIST.md](./PR_CHECKLIST.md) | Run before anything goes upstream |
| [resources/](./resources/) | Glossary and per-session reading list |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Improving this track |

CC0: fork it, translate it, run it in your city.

*Privacy isn't something you wait for. It's something you ship.* 🟠
