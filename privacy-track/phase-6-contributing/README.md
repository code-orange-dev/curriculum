# Phase 6: Building & Contributing — Ship Your Code

> Months 11-12 · Sessions 21-24 · Everything you've learned, applied. Every graduate ships a PR.

## Overview

This is where it all comes together. You've spent 10 months learning how Bitcoin privacy works, how it breaks, and how to fix it. Phase 6 is about applying that knowledge: building a privacy-preserving wallet, creating tools that measure privacy, and shipping your contributions to the Bitcoin ecosystem. Every participant graduates with at least one PR submitted to a real Bitcoin project.

## Session 21: Privacy-Preserving Wallet Development with BDK

**Date:** Month 11, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- Bitcoin Dev Kit (BDK): the Rust library for building Bitcoin wallets
- Privacy-by-default wallet design: what choices to make at the architecture level
- Implementing privacy-optimized coin selection in BDK
- Address reuse prevention: key management strategies
- Change output handling: matching script types, avoiding dust, randomizing position
- Adding Silent Payments or Payjoin support to a BDK wallet
- Descriptor wallets: how descriptors can encode privacy policies

### Exercise: Build a Privacy Wallet
1. Scaffold a BDK wallet in Rust with signet configuration
2. Implement privacy-optimized coin selection: prefer spending UTXOs that don't reveal payment amounts
3. Implement change output privacy: match script type to recipient, randomize position, avoid round amounts
4. Add address reuse detection: warn or refuse if a recipient address has been used before
5. (Stretch) Integrate basic Payjoin sender support using PDK
6. Test: construct 5 transactions and analyze each for privacy leaks using the criteria from Phase 1

### Reading
- BDK documentation: https://bitcoindevkit.org
- BDK source code: https://github.com/bitcoindevkit/bdk
- Bitcoin Dev Kit "Getting Started" guide
- Alekos Filini: "Building Bitcoin Wallets with BDK" (presentation)

---

## Session 22: Privacy Testing & Mempool Analysis

**Date:** Month 11, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- How to systematically evaluate a transaction's privacy
- Building a privacy scoring rubric: what to check and how to weight it
- Mempool analysis: using mempool.space API to examine real-time transaction privacy
- Automated privacy testing: building CI checks for wallet software
- How chain analysis firms score transactions (public research from Chainalysis, OXT)
- The "privacy budget" concept: every transaction leaks some information, minimize the total

### Exercise: Transaction Privacy Scorer
File: `session-22-privacy-testing/privacy_scorer.py`

Build a Python tool that takes a raw transaction (hex) and outputs a privacy score:

1. `check_address_reuse(tx)` — are any output addresses reused? (-20 points)
2. `check_script_type_mixing(tx)` — do inputs and outputs use different script types? (-15 points)
3. `check_round_amounts(tx)` — are any outputs suspiciously round? (-10 points)
4. `check_change_detection(tx)` — can the change output be identified? (-15 points)
5. `check_fee_fingerprint(tx)` — does the fee rate match a known wallet? (-5 points)
6. `check_timing(tx)` — was this broadcast at a predictable time? (-5 points)
7. `check_locktime(tx)` — does nLockTime reveal the wallet? (-5 points)
8. `check_input_count(tx)` — unnecessary UTXO consolidation? (-10 points)
9. `check_output_ordering(tx)` — BIP69 or random? (-5 points)
10. `privacy_score(tx)` — aggregate score from 0 (terrible) to 100 (excellent)

Test against 20 real mainnet transactions and calibrate the scoring weights.

### Reading
- OXT Research: "Understanding Bitcoin Privacy with OXT" (methodology)
- 0xB10C: "Tracking wallet fingerprints" (blog post)
- mempool.space API documentation

---

## Session 23: Contribution Sprint — Submit PRs to Privacy Projects

**Date:** Month 12, Week 1
**Duration:** 3 hours (extended session)

### What You'll Learn
- How to find Good First Issues across Bitcoin privacy repositories
- How to write a good PR: clear title, description, tests, rebased on latest main
- How to respond to code review feedback
- How to find a reviewer and get your PR merged

### The Sprint
This is a working session, not a lecture. Format:

1. **00:00 - 00:30** — Issue selection. Each participant picks a Good First Issue from the curated list below (or any Bitcoin privacy project). Facilitator helps match issues to skill levels.
2. **00:30 - 02:00** — Code. Participants work on their PRs. Facilitator circulates to help with build issues, test failures, and code questions.
3. **02:00 - 02:30** — Peer review. Each participant reviews one other participant's PR. Give constructive feedback.
4. **02:30 - 03:00** — Submit. Push your branch, open the PR, write a clear description. Celebrate.

### Curated Good First Issues (Updated Monthly)
The facilitator maintains a curated list of issues across these repos:

**Silent Payments:**
- bitcoin/bitcoin — SP-related issues
- cygnet3/rust-silentpayments — test coverage, documentation, edge cases

**Payjoin:**
- payjoin/rust-payjoin — open issues labeled "good first issue"
- BTCPay Server — Payjoin-related issues

**Light Clients:**
- vinteumorg/Floresta — issues labeled "good first issue"
- rustaceanrob/kyoto — early-stage project, many contribution opportunities

**eCash:**
- fedimint/fedimint — issues labeled "good first issue"
- cashubtc/nutshell — Python project, accessible entry point

**Wallets:**
- bitcoindevkit/bdk — issues related to coin selection, privacy
- any wallet repo where you've identified a privacy improvement

---

## Session 24: Capstone — Present Your Privacy Contribution

**Date:** Month 12, Week 3
**Duration:** 3 hours (extended session)

### What This Is
The final session. Each participant presents their contribution to the full Code Orange community — not just the privacy track participants, but Bitcoin Dojo, rawBit, and Decoding Bitcoin cohorts too. This is where we show what a year of focused privacy education produces.

### Presentation Format (10 minutes per person)
1. **The problem** (2 min) — What privacy issue did you work on? Why does it matter?
2. **What you built** (4 min) — Walk through your contribution. Show the code. Explain the tradeoffs.
3. **What you learned** (2 min) — What was harder than expected? What surprised you?
4. **What's next** (2 min) — If you had another 6 months, what would you build?

### Graduating
Participants who have:
- Attended 18+ of 24 sessions (75%)
- Submitted at least 1 PR to a Bitcoin privacy project
- Presented at the capstone session

...are eligible to apply for the **Code Orange Developer Fellowship** ($500/month for 6 months) to continue their privacy work full-time.

### Celebration
After presentations: community dinner at Bitcoin House Bali. We show the aggregate stats: total PRs submitted, total repos contributed to, total lines of code. This is the proof of work we send to grant reviewers.

---

## Phase 6 Contribution Target

**Every participant has at least 1 PR submitted to a Bitcoin privacy project.** This is the non-negotiable graduation requirement.

---

## The Full Picture

Over 12 months and 24 sessions, a privacy track graduate has:
- Traced transactions like a chain analysis firm (Phase 1)
- Built Silent Payments from the cryptography up (Phase 2)
- Deployed Payjoin in a production environment (Phase 3)
- Configured a privacy-hardened node and evaluated light client tradeoffs (Phase 4)
- Understood CoinJoin, CoinSwap, eCash, and Lightning privacy (Phase 5)
- Built a privacy-preserving wallet and shipped code to real projects (Phase 6)

They are now a Bitcoin privacy developer. The ecosystem has one more person who can review PRs, find bugs, implement features, and teach others. That's what this program is for.

---

*[Code Orange Dev School](https://codeorange.dev) · CC0 1.0 Universal*