# Phase 2: Silent Payments (BIP352) — Reusable Addresses Without Address Reuse

> Months 3-4 · Sessions 5-8 · The most important privacy improvement coming to Bitcoin wallets.

## Overview

Address reuse is one of the most common and damaging privacy failures in Bitcoin. Silent Payments (BIP352) solves this elegantly: a single static address that generates unique on-chain outputs for every payment, using ECDH key exchange. In this phase, you'll understand the cryptography, implement a sender and scanner from scratch, and contribute to a real Silent Payments implementation.

## Session 5: BIP352 Deep Dive — How Silent Payments Work

**Date:** Month 3, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- The address reuse problem: why it happens, how it destroys privacy
- How stealth addresses tried to solve this (BIP47 reusable payment codes) and their limitations
- BIP352 Silent Payments: the protocol design and its tradeoffs
- The cryptography: ECDH shared secret derivation on secp256k1
- Scan keys vs spend keys: why they're separated and what each does
- Labeling: how receivers can organize payments without revealing connections
- Why scanning is computationally expensive and how this affects light clients

### Exercise: Silent Payments by Hand
1. Given a sender's private key and a Silent Payment address (B_scan, B_spend), compute the shared secret using ECDH
2. Derive the tweak from the shared secret
3. Calculate the output public key: P_output = B_spend + tweak * G
4. Verify that the receiver (who knows b_scan and b_spend) can detect and spend this output
5. All math done in pure Python using secp256k1 field operations (no libraries)

### Reading
- BIP352 specification (https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) — **Required**
- Josie Baker: "Silent Payments: Light Client Protocol" (blog post)
- Ruben Somsen's original Silent Payments gist

---

## Session 6: Implement a Silent Payments Sender in Python

**Date:** Month 3, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- Complete SP send flow: input selection → shared secret → tweak → output construction
- Handling multiple inputs (input aggregation for shared secret derivation)
- Handling multiple SP recipients in a single transaction
- Edge cases: what happens with non-standard input types, taproot inputs
- Testing against the BIP352 test vectors

### Exercise: Build an SP Sender
File: `session-06-implement-sender/silent_payments_sender.py`

Implement the complete Silent Payments sending flow:
1. `parse_silent_payment_address(address)` → extract B_scan and B_spend
2. `aggregate_input_private_keys(input_keys)` → compute the aggregated key for multiple inputs
3. `compute_shared_secret(sender_key, B_scan)` → ECDH shared secret
4. `derive_output_key(shared_secret, B_spend, k)` → compute the kth output key
5. `create_sp_transaction(inputs, sp_recipients, change_address)` → construct the full transaction

Test against BIP352 test vectors to verify correctness.

### Reading
- BIP352 test vectors: https://github.com/bitcoin/bips/tree/master/bip-0352
- Bitcoin Core Silent Payments implementation PR #28122 — read the code
- secp256k1 library documentation

---

## Session 7: Scanning, Receiving & Compact Block Filters

**Date:** Month 4, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- The receiver's problem: scanning every transaction in every block
- Why full-node scanning is the simplest but most expensive approach
- Compact block filters (BIP157/158) as a privacy-preserving optimization for light clients
- The tweak cache: precomputing values to speed up scanning
- Bandwidth vs privacy tradeoffs for SP light clients
- How the Kyoto and Nakamoto light clients approach SP scanning

### Exercise: Build an SP Scanner
File: `session-07-scanning-and-cbf/silent_payments_scanner.py`

1. `scan_transaction(tx, b_scan, B_spend)` → check if any output belongs to us
2. `scan_block(block, b_scan, B_spend)` → scan all transactions in a block
3. `build_compact_filter(block)` → construct a BIP158 filter for a block
4. `query_filter(filter, elements)` → check if our elements might be in the block
5. `scan_with_filters(blocks, filters, b_scan, B_spend)` → full scanning pipeline using CBF to skip irrelevant blocks

Measure: how many blocks can you skip using compact block filters? What's the false positive rate?

### Reading
- BIP157: Client Side Block Filtering — **Required**
- BIP158: Compact Block Filters for Light Clients — **Required**
- Josie Baker's light client protocol proposal for Silent Payments

---

## Session 8: Contributing to Silent Payments

**Date:** Month 4, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- Current state of Silent Payments implementations across the ecosystem
- Bitcoin Core PR #28122: code walkthrough, what's merged, what's pending
- rust-silentpayments: library architecture, API design, open issues
- Cake Wallet: first wallet with SP support — how they integrated it
- Where the gaps are: what still needs to be built, tested, and reviewed

### Exercise: Your First SP Contribution
1. Clone rust-silentpayments or bitcoin/bitcoin (depending on your language preference)
2. Build the project locally and run the existing test suite
3. Browse open issues — find one that matches your skill level
4. Either: submit a PR (code fix, test addition, documentation improvement) OR write a detailed review of an open PR

The facilitator will help match each participant to an appropriate issue.

### Contribution Targets
- Add a test case to rust-silentpayments test suite
- Improve documentation in BIP352 or an SP implementation
- Review an open PR on Bitcoin Core #28122
- File an issue with a well-described bug or edge case
- Add SP support to a wallet that doesn't have it yet

### Key Repos
- [bitcoin/bitcoin #28122](https://github.com/bitcoin/bitcoin/pull/28122)
- [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments)
- [cake-tech/cake_wallet](https://github.com/cake-tech/cake_wallet)

---

## Phase 2 Contribution Target

By the end of Phase 2, every participant should submit at least one PR to a Silent Payments implementation. This can be code, tests, documentation, or a detailed PR review.

---

## What's Next

Phase 3 covers Payjoin (BIP77/78) — the most practical privacy tool available today. While Silent Payments prevent address reuse, Payjoin breaks the common-input-ownership heuristic that chain analysis firms rely on to cluster transactions.

---

*[Code Orange Dev School](https://codeorange.dev) · CC0 1.0 Universal*
