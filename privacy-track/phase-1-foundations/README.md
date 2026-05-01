# Phase 1: Foundations — Why Privacy Matters & How It Breaks

> Months 1-2 · Sessions 1-4 · You can't build privacy tools if you don't understand how surveillance works.

## Overview

Phase 1 establishes the foundation every privacy developer needs: how chain analysis works, how transactions leak information, how coin selection affects privacy, and how wallet software leaves fingerprints. By the end of this phase, you'll see Bitcoin transactions the way a chain analysis firm does — and you'll know exactly what to fix.

## Session 1: Why Privacy Matters — Chain Analysis & Surveillance

**Date:** Month 1, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- How chain analysis companies (Chainalysis, Elliptic) cluster Bitcoin addresses
- The 5 primary heuristics: common-input-ownership (CIOH), change output detection, address reuse, timing analysis, amount correlation
- Why "I have nothing to hide" is wrong — privacy as a protocol-level requirement
- The difference between privacy, anonymity, and pseudonymity in Bitcoin

### Exercise: Chain Analysis Lab
1. Open mempool.space and OXT.me
2. Given a testnet transaction ID, trace the flow of funds through 5 hops
3. Apply CIOH to identify which inputs likely belong to the same entity
4. Identify the change output using amount analysis and script type matching
5. Write a 1-page report: "What can a chain analysis firm learn from this transaction chain?"

### Reading
- Bitcoin Wiki: Privacy (https://en.bitcoin.it/wiki/Privacy) — **Required**
- Greg Maxwell's 2013 CoinJoin post on bitcointalk — **Required**
- Bitcoin Optech: Privacy topic page

---

## Session 2: Transaction Anatomy for Privacy

**Date:** Month 1, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- Raw transaction structure byte-by-byte: version, inputs, outputs, locktime
- How nVersion, nLockTime, and nSequence values differ across wallet implementations
- Fee estimation patterns as wallet fingerprints
- Script types and their privacy implications (P2PKH, P2SH, P2WPKH, P2WSH, P2TR)
- Why mixing script types in a transaction destroys privacy

### Exercise: Transaction Dissection
1. Decode 5 raw testnet transactions using bitcoin-cli decoderawtransaction
2. For each transaction, identify: version, locktime, sequence values, script types used, fee rate
3. Research: which wallet software uses nLockTime for anti-fee-sniping? Which doesn't?
4. Given a transaction, determine if the sender and recipient are using the same or different wallets based on script types

### Reading
- BIP125: Opt-in Replace-by-Fee — understand nSequence signaling
- Bitcoin Optech: Transaction compatibility matrix
- Murch's coin selection presentation (2017 Scaling Bitcoin)

---

## Session 3: UTXO Management & Coin Selection

**Date:** Month 2, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- Why UTXO set management is fundamental to Bitcoin privacy
- 4 coin selection algorithms: largest-first, branch-and-bound, privacy-optimized, random/knapsack
- How each algorithm affects privacy differently (change output size, input count, UTXO consolidation)
- Dust attacks and how they break privacy through forced UTXO linking
- Coin control: manually selecting inputs for maximum privacy

### Exercise: Coin Selection Simulator (Python)
File: `session-03-utxo-management/coin_selection_simulator.py`

Implement all 4 algorithms from scratch:
- `select_largest_first(utxos, target)` — greedy selection, worst privacy
- `select_branch_and_bound(utxos, target)` — exact match search, avoids change
- `select_privacy_optimized(utxos, target)` — minimize information leakage
- `select_random(utxos, target)` — randomized selection with knapsack fallback

Then: run all 4 against the same UTXO set and target amount. Score each result for: number of inputs used, change output amount, whether change matches a round number, whether input amounts reveal the payment amount.

### Reading
- Murch: "An Evaluation of Coin Selection Strategies" (Master's thesis) — **Required**
- Bitcoin Core coin selection code: `src/wallet/coinselection.cpp`
- Erhardt & Shigeya: "Coin Selection with Leverage" (2017)

---

## Session 4: Wallet Fingerprinting & Transaction Construction

**Date:** Month 2, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- How wallet software creates unique fingerprints in every transaction
- Known fingerprints: Bitcoin Core (anti-fee-sniping locktime, BnB coin selection), Electrum (no locktime, round fee rates), BlueWallet, Wasabi, Sparrow
- How to construct a "privacy-clean" transaction that avoids all common fingerprints
- Transaction batching: privacy implications of combining multiple payments

### Exercise: Wallet Fingerprint Lab
File: `session-04-wallet-fingerprinting/wallet_fingerprint_lab.py`

Given 10 raw transactions (provided), identify which wallet created each one by analyzing:
- nVersion value
- nLockTime (0, current block height, or other)
- nSequence values (0xFFFFFFFE, 0xFFFFFFFF, or RBF-signaling)
- Output ordering (BIP69 lexicographic, or random)
- Script types used
- Fee rate patterns
- Change output position and amount

Then: construct a raw transaction using bitcoin-cli that avoids ALL known fingerprints.

### Reading
- 0xB10C: "Wallet Fingerprinting" (blog post)
- Ishaana Misra: "Deanonymization of Bitcoin Transactions" (analysis of wallet fingerprinting)
- BIP69: Lexicographic Indexing of Transaction Inputs and Outputs

---

## Phase 1 Contribution Target

By the end of Phase 1, every participant should file at least one issue or documentation PR on a Bitcoin wallet's privacy behavior. Examples:
- File an issue on a wallet repo documenting a privacy leak you discovered during the exercises
- Submit a docs PR to Bitcoin Optech adding clarity to a privacy topic
- Write up a wallet fingerprinting analysis and publish it

---

## What's Next

Phase 2 takes everything you learned about how privacy breaks and applies it to building the fix: Silent Payments (BIP352), the most important privacy improvement coming to Bitcoin wallets.

---

*[Code Orange Dev School](https://codeorange.dev) · CC0 1.0 Universal*
