# Bitcoin Privacy Developer Track

> 24 bi-weekly sessions. 12 months. From "why does privacy matter?" to "here's my merged PR to a privacy protocol."

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## What This Is

A hands-on developer curriculum that teaches Bitcoin privacy from the ground up — chain analysis, Silent Payments, Payjoin, compact block filters, CoinJoin, CoinSwap, Taproot privacy, eCash, Lightning privacy — and funnels every participant toward their first open-source contribution to a privacy-related Bitcoin project.

Every session has exercises. Every phase ends with a contribution target. All materials are CC0-licensed. Use them, fork them, translate them.

**Format:** Bi-weekly workshops (every 2 weeks), 2-2.5 hours each
**Duration:** 12 months (24 sessions)
**Prerequisites:** Basic Bitcoin knowledge (completed Bitcoin Dojo or equivalent). Comfortable reading code. Python or Rust experience helpful.
**Outcome:** Every graduate submits at least 1 PR to a Bitcoin privacy project.

---

## Curriculum Overview

```
Phase 1: Foundations                 (Sessions 1-4,   Months 1-2)
Phase 2: Silent Payments             (Sessions 5-8,   Months 3-4)
Phase 3: Payjoin                     (Sessions 9-12,  Months 5-6)
Phase 4: Network & Protocol Privacy  (Sessions 13-16, Months 7-8)
Phase 5: Advanced Techniques         (Sessions 17-20, Months 9-10)
Phase 6: Building & Contributing     (Sessions 21-24, Months 11-12)
```

---

## Phase 1: Foundations — Why Privacy Matters & How It Breaks

*Months 1-2 · Sessions 1-4 · You can't build privacy tools if you don't understand how surveillance works.*

| Session | Topic | What You Build |
|---------|-------|----------------|
| **01** | [Why Privacy Matters: Chain Analysis & Surveillance](phase-1-foundations/session-01-why-privacy-matters/) | Trace a transaction chain on mempool.space and OXT.me. Identify clustering heuristics applied to your own testnet transactions. |
| **02** | [Transaction Anatomy for Privacy](phase-1-foundations/session-02-transaction-anatomy/) | Dissect raw transactions byte-by-byte. Identify version, nLockTime, nSequence, and fee patterns that leak wallet identity. |
| **03** | [UTXO Management & Coin Selection](phase-1-foundations/session-03-utxo-management/) | Implement 4 coin selection algorithms in Python (largest-first, branch-and-bound, privacy-optimized, random). Score each for privacy leakage. |
| **04** | [Wallet Fingerprinting & Transaction Construction](phase-1-foundations/session-04-wallet-fingerprinting/) | Given 10 raw transactions, identify which wallet software created each one. Build a "privacy-clean" transaction that avoids all common fingerprints. |

**Phase 1 contribution target:** File an issue or documentation PR on a Bitcoin wallet's privacy behavior.

**Reading:** Bitcoin Wiki Privacy page, Greg Maxwell's 2013 privacy post, Bitcoin Optech Privacy topic.

---

## Phase 2: Silent Payments (BIP352) — Reusable Addresses Without Address Reuse

*Months 3-4 · Sessions 5-8 · The most important privacy improvement coming to Bitcoin wallets.*

| Session | Topic | What You Build |
|---------|-------|----------------|
| **05** | [BIP352 Deep Dive: How Silent Payments Work](phase-2-silent-payments/session-05-bip352-deep-dive/) | Walk through the full BIP352 specification. Derive shared secrets by hand using secp256k1 math. Understand scan keys vs spend keys and why the distinction matters. |
| **06** | [Implement a Silent Payments Sender in Python](phase-2-silent-payments/session-06-implement-sender/) | Build a minimal SP sender from scratch: generate a Silent Payment address, derive the ECDH shared secret, calculate the tweak, construct a transaction paying to an SP address on signet. |
| **07** | [Scanning, Receiving & Compact Block Filters](phase-2-silent-payments/session-07-scanning-and-cbf/) | Build a minimal SP scanner that detects incoming payments. Understand the computational cost of scanning and how BIP157/158 compact block filters make it practical for light clients. |
| **08** | [Contributing to Silent Payments](phase-2-silent-payments/session-08-contributing/) | Code walkthrough: Bitcoin Core PR #28122, rust-silentpayments library, and wallet integration status. Pick a Good First Issue and submit a PR. |

**Phase 2 contribution target:** Submit a PR to a Silent Payments implementation (Bitcoin Core, rust-silentpayments, or a wallet integrating SP support).

**Key repos:** [bitcoin/bitcoin #28122](https://github.com/bitcoin/bitcoin/pull/28122) · [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) · [cake-tech/cake_wallet](https://github.com/cake-tech/cake_wallet) (first wallet with SP support)

---

## Phase 3: Payjoin (BIP77/78) — Breaking the Common-Input-Ownership Heuristic

*Months 5-6 · Sessions 9-12 · The most practical privacy tool available to Bitcoin users today.*

| Session | Topic | What You Build |
|---------|-------|----------------|
| **09** | [BIP77/78 Theory: How Payjoin Defeats Chain Analysis](phase-3-payjoin/session-09-bip77-78-theory/) | Walk through a Payjoin transaction step by step. Understand V1 (BIP78, synchronous) vs V2 (BIP77, asynchronous via relay). Analyze real Payjoin transactions on-chain — can you tell them apart from normal transactions? |
| **10** | [Building with Payjoin Dev Kit](phase-3-payjoin/session-10-payjoin-dev-kit/) | Integrate PDK into a Rust application. Build a sender that constructs an original PSBT and a receiver that modifies it. Send a Payjoin on testnet/signet. |
| **11** | [Payjoin in Production: BTCPay Server & Wallets](phase-3-payjoin/session-11-production-integration/) | Set up BTCPay Server with Payjoin enabled. Trace the code path from payment request to broadcast. Understand Bull Bitcoin's BIP77 integration — the first production wallet with async Payjoin. |
| **12** | [Contributing to Payjoin](phase-3-payjoin/session-12-contributing/) | Code walkthrough: payjoin-rust, PDK architecture, BTCPay's Payjoin implementation. Pick an open issue and submit a PR. |

**Phase 3 contribution target:** Submit a PR to payjoin-rust, Payjoin Dev Kit, or a wallet's Payjoin integration.

**Key repos:** [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) · [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver)

---

## Phase 4: Network & Protocol Privacy — Beyond Transactions

*Months 7-8 · Sessions 13-16 · Transactions aren't the only thing that leaks. Your node, your connections, and your script types tell a story too.*

| Session | Topic | What You Build |
|---------|-------|----------------|
| **13** | [P2P Network Privacy: Dandelion++, Tor, I2P](phase-4-network-privacy/session-13-p2p-privacy/) | Understand how transaction relay reveals your IP address. Study Dandelion++ (BIP156) stem-and-fluff propagation. Configure Bitcoin Core with Tor and I2P. Measure the anonymity set difference. |
| **14** | [Compact Block Filters: BIP157/158 Deep Dive](phase-4-network-privacy/session-14-compact-block-filters/) | Implement a Golomb-Rice Coded Set from scratch. Build a compact block filter, query it, and understand false positive rates. Compare the privacy of BIP37 Bloom filters vs BIP157/158 compact block filters vs running a full node. |
| **15** | [Light Client Privacy: Floresta, Kyoto, Neutrino](phase-4-network-privacy/session-15-light-clients/) | Set up Floresta (utreexo-based node) and understand how it improves light client privacy. Study Kyoto's compact block filter implementation in Rust. Evaluate privacy tradeoffs of each light client approach. |
| **16** | [Taproot Privacy: Schnorr, MAST & Key Path Spending](phase-4-network-privacy/session-16-taproot-privacy/) | Understand how Taproot makes multisig transactions indistinguishable from single-sig. Build a Taproot transaction using key path spending. Analyze how MuSig2 and FROST improve privacy for multi-party setups. Study how Taproot enables future privacy improvements (CISA, cross-input signature aggregation). |

**Phase 4 contribution target:** Submit a PR to Floresta, Kyoto, or a Bitcoin Core P2P privacy improvement.

**Key repos:** [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta) · [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) · [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) (P2P/net PRs)

---

## Phase 5: Advanced Privacy Techniques

*Months 9-10 · Sessions 17-20 · CoinJoin, CoinSwap, eCash, and Lightning — the full privacy toolkit.*

| Session | Topic | What You Build |
|---------|-------|----------------|
| **17** | [CoinJoin: Equal-Output Mixing & WabiSabi](phase-5-advanced/session-17-coinjoin/) | Understand CoinJoin mechanics: equal-output mixing, toxic change, coordinator trust. Study the WabiSabi protocol (used by Wasabi Wallet 2.0): keyed verification anonymous credentials, registration, and blame rounds. Analyze a real CoinJoin transaction on-chain. |
| **18** | [CoinSwap & Atomic Swaps for Privacy](phase-5-advanced/session-18-coinswap/) | Understand how CoinSwap breaks transaction graph analysis using atomic swaps. Study Teleport Transactions (Chris Belcher's CoinSwap implementation). Understand how CISA (cross-input signature aggregation) would make CoinJoin and CoinSwap dramatically cheaper. |
| **19** | [eCash Privacy: Fedimint & Cashu](phase-5-advanced/session-19-ecash/) | Understand Chaumian eCash: blind signatures, mint trust model, and perfect transaction privacy within a federation. Set up a Cashu mint on signet. Build a simple eCash wallet interaction. Study Fedimint's architecture: consensus, modules, Lightning gateway. |
| **20** | [Lightning Privacy: Blinded Paths, Probing & Route Privacy](phase-5-advanced/session-20-lightning-privacy/) | Understand Lightning's privacy model: what's visible to whom. Study channel balance probing attacks. Understand blinded paths (BOLT12) and how they improve receiver privacy. Analyze trampoline routing and its privacy properties. |

**Phase 5 contribution target:** Submit a PR to a CoinJoin, CoinSwap, eCash, or Lightning privacy project.

**Key repos:** [nickhntv/teleport-transactions](https://github.com/nickhntv/teleport-transactions) · [fedimint/fedimint](https://github.com/fedimint/fedimint) · [cashubtc/nutshell](https://github.com/cashubtc/nutshell) · [lightningdevkit/rust-lightning](https://github.com/lightningdevkit/rust-lightning)

---

## Phase 6: Building & Contributing — Ship Your Code

*Months 11-12 · Sessions 21-24 · Everything you've learned, applied. Every graduate ships a PR.*

| Session | Topic | What You Build |
|---------|-------|----------------|
| **21** | [Privacy-Preserving Wallet Development with BDK](phase-6-contributing/session-21-wallet-dev-bdk/) | Build a privacy-focused wallet using Bitcoin Dev Kit. Implement privacy-optimized coin selection, avoid address reuse, handle change outputs safely, and add Silent Payments or Payjoin support. |
| **22** | [Privacy Testing & Mempool Analysis](phase-6-contributing/session-22-privacy-testing/) | Build a privacy scoring tool that takes a raw transaction and identifies privacy leaks: round amounts, address reuse, script type mismatches, timing patterns, fee fingerprints. Test it against real mempool data. |
| **23** | [Contribution Sprint: Submit PRs to Privacy Projects](phase-6-contributing/session-23-contribution-sprint/) | Guided sprint: pick a Good First Issue from any privacy-related Bitcoin project, get mentorship from the facilitator and community, and submit a PR by end of session. Group code review of each other's PRs. |
| **24** | [Capstone: Present Your Privacy Contribution](phase-6-contributing/session-24-capstone/) | Each participant presents their contribution: what they built, what they learned, and what they'd work on next. Open to the full Code Orange community. Graduating participants are eligible for the Developer Fellowship ($500/mo) to continue contributing. |

**Phase 6 contribution target:** Every participant has at least 1 PR submitted to a Bitcoin privacy project.

---

## Contribution Targets by Phase

| Phase | Target | Key Repos |
|-------|--------|-----------|
| 1. Foundations | File an issue or docs PR on wallet privacy | Any Bitcoin wallet repo |
| 2. Silent Payments | PR to an SP implementation | bitcoin/bitcoin, rust-silentpayments |
| 3. Payjoin | PR to Payjoin ecosystem | rust-payjoin, PDK, BTCPay |
| 4. Network Privacy | PR to node/light client privacy | Floresta, Kyoto, Bitcoin Core P2P |
| 5. Advanced | PR to CoinJoin/eCash/Lightning | Fedimint, Cashu, LDK, Teleport |
| 6. Building | Ship your own privacy contribution | Any privacy-related Bitcoin project |

**12-month target: 30+ merged PRs from track participants across these repos.**

---

## Session Format

Each bi-weekly session follows the same structure:

```
00:00 - 00:15   Review: What happened since last session? Any PRs submitted?
00:15 - 00:45   Concept: Theory and protocol walkthrough with diagrams
00:45 - 01:45   Build: Hands-on coding exercise (the core of every session)
01:45 - 02:00   Contribute: Identify Good First Issues, discuss contribution paths
02:00 - 02:15   Reading: Assigned reading + prep for next session
```

Sessions are designed for in-person delivery at Bitcoin House Bali, but all materials work for remote/self-study. Session notes, exercises, and reading lists are in each session folder.

---

## Schedule

| Week | Date | Session | Phase |
|------|------|---------|-------|
| 1 | Month 1, Week 1 | Session 01: Why Privacy Matters | Foundations |
| 3 | Month 1, Week 3 | Session 02: Transaction Anatomy | Foundations |
| 5 | Month 2, Week 1 | Session 03: UTXO Management | Foundations |
| 7 | Month 2, Week 3 | Session 04: Wallet Fingerprinting | Foundations |
| 9 | Month 3, Week 1 | Session 05: BIP352 Deep Dive | Silent Payments |
| 11 | Month 3, Week 3 | Session 06: Implement SP Sender | Silent Payments |
| 13 | Month 4, Week 1 | Session 07: Scanning & CBF | Silent Payments |
| 15 | Month 4, Week 3 | Session 08: Contributing to SP | Silent Payments |
| 17 | Month 5, Week 1 | Session 09: BIP77/78 Theory | Payjoin |
| 19 | Month 5, Week 3 | Session 10: Payjoin Dev Kit | Payjoin |
| 21 | Month 6, Week 1 | Session 11: Production Integration | Payjoin |
| 23 | Month 6, Week 3 | Session 12: Contributing to PJ | Payjoin |
| 25 | Month 7, Week 1 | Session 13: P2P Privacy | Network Privacy |
| 27 | Month 7, Week 3 | Session 14: Compact Block Filters | Network Privacy |
| 29 | Month 8, Week 1 | Session 15: Light Clients | Network Privacy |
| 31 | Month 8, Week 3 | Session 16: Taproot Privacy | Network Privacy |
| 33 | Month 9, Week 1 | Session 17: CoinJoin | Advanced |
| 35 | Month 9, Week 3 | Session 18: CoinSwap | Advanced |
| 37 | Month 10, Week 1 | Session 19: eCash | Advanced |
| 39 | Month 10, Week 3 | Session 20: Lightning Privacy | Advanced |
| 41 | Month 11, Week 1 | Session 21: Wallet Dev with BDK | Contributing |
| 43 | Month 11, Week 3 | Session 22: Privacy Testing | Contributing |
| 45 | Month 12, Week 1 | Session 23: Contribution Sprint | Contributing |
| 47 | Month 12, Week 3 | Session 24: Capstone Presentations | Contributing |

---

## Exercises & Code

Each session includes hands-on exercises. Key exercise files:

```
phase-1-foundations/
  session-03-utxo-management/coin_selection_simulator.py     — 4 coin selection algorithms
  session-04-wallet-fingerprinting/wallet_fingerprint_lab.py — Identify wallet software from raw txs

phase-2-silent-payments/
  session-06-implement-sender/silent_payments_sender.py      — Build SP sender from scratch
  session-07-scanning-and-cbf/silent_payments_scanner.py     — Build SP scanner with CBF

phase-3-payjoin/
  session-10-payjoin-dev-kit/pdk_integration/                — Rust project using Payjoin Dev Kit
  session-11-production-integration/btcpay_payjoin_lab.md    — BTCPay Server Payjoin walkthrough

phase-4-network-privacy/
  session-14-compact-block-filters/compact_block_filters.py  — Golomb-Rice coding from scratch
  session-16-taproot-privacy/taproot_privacy_lab.py          — Taproot key path vs script path analysis

phase-5-advanced/
  session-17-coinjoin/coinjoin_analysis.py                   — CoinJoin detection and analysis
  session-19-ecash/cashu_mint_exercise.md                    — Set up a Cashu mint on signet

phase-6-contributing/
  session-22-privacy-testing/privacy_scorer.py               — Transaction privacy scoring tool
```

---

## Resources

- [Reading List](resources/reading-list.md) — 50+ resources organized by phase, required readings marked
- [Glossary](resources/glossary.md) — 50+ terms covering all 6 phases
- [Facilitator Guide](FACILITATOR_GUIDE.md) — Session-by-session facilitation notes, timing, tips
- [Capstone Projects](capstone/README.md) — 4 project tracks with rubrics
- [Contributing](CONTRIBUTING.md) — How to contribute to this curriculum

---

## For Grant Reviewers

This curriculum exists because Bitcoin's privacy infrastructure needs more developers — and those developers need to come from more places. Code Orange's privacy track is the only structured, open-source, CC0-licensed program that teaches developers to understand, implement, and contribute to Silent Payments, Payjoin, compact block filters, CoinJoin, CoinSwap, and privacy-preserving wallet development.

Every session leads to code. Every phase leads to contributions. Every graduate is a permanent addition to Bitcoin's privacy developer pool.

**Repos our graduates will contribute to:** [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) · [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) · [rust-payjoin](https://github.com/payjoin/rust-payjoin) · [Floresta](https://github.com/vinteumorg/Floresta) · [Kyoto](https://github.com/rustaceanrob/kyoto) · [Fedimint](https://github.com/fedimint/fedimint) · [Cashu](https://github.com/cashubtc/nutshell) · [BDK](https://github.com/bitcoindevkit/bdk) · [LDK](https://github.com/lightningdevkit/rust-lightning)

---

*[Code Orange Dev School](https://codeorange.dev) · Bitcoin House Bali, Indonesia · CC0 1.0 Universal*
