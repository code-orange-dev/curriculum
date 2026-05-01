# Phase 3: Payjoin (BIP77/78) — Breaking the Common-Input-Ownership Heuristic

> Months 5-6 · Sessions 9-12 · The most practical privacy tool available to Bitcoin users today.

## Overview

The common-input-ownership heuristic (CIOH) is the single most powerful tool chain analysis firms use: if two inputs appear in the same transaction, they probably belong to the same person. Payjoin breaks this assumption by having the receiver contribute inputs to the payment transaction. The result looks like a normal transaction on-chain — but the ownership assumption is wrong. In this phase, you'll understand the protocol, build with Payjoin Dev Kit in Rust, deploy it in production via BTCPay Server, and contribute to the ecosystem.

## Session 9: BIP77/78 Theory — How Payjoin Defeats Chain Analysis

**Date:** Month 5, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- The common-input-ownership heuristic: why it exists, why it works, and why it matters
- Payjoin V1 (BIP78): synchronous flow, requires receiver to be online, HTTPS-based
- Payjoin V2 (BIP77): asynchronous flow via untrusted relay (Ohttp), no server required
- Step-by-step transaction flow: Original PSBT → receiver modifies → sender verifies & signs → broadcast
- Security model: what the sender must verify before signing the modified PSBT (5 critical checks)
- Privacy analysis: why a Payjoin transaction is indistinguishable from a normal transaction
- Output substitution attacks and how BIP78 prevents them

### Exercise: Payjoin Transaction Analysis
1. Given 10 testnet transactions, determine which ones are Payjoins and which are normal payments. (Hint: you can't tell — that's the point.)
2. Walk through the full Payjoin V2 flow on paper: draw each step, label each party's knowledge
3. Implement the 5 sender verification checks in pseudocode: amount check, input ownership proof, fee check, output substitution check, script type check
4. Analyze: what information does the relay server learn in BIP77? What can't it learn?

### Reading
- BIP78: Payjoin specification — **Required**
- BIP77: Payjoin Version 2 — **Required**
- Dan Gould: "Payjoin is Practical" (blog post)
- Bitcoin Optech: Payjoin topic page

---

## Session 10: Building with Payjoin Dev Kit (Rust)

**Date:** Month 5, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- Payjoin Dev Kit (PDK) architecture: sender, receiver, and relay components
- PSBT construction and modification: how the receiver adds inputs without breaking the transaction
- Rust implementation: integrating PDK into a wallet application
- Testing Payjoin flows on signet/testnet

### Exercise: PDK Integration
File: `session-10-payjoin-dev-kit/pdk_integration/`

Build a complete Payjoin flow in Rust:
1. `create_original_psbt(sender_wallet, amount, receiver_address)` — sender constructs the initial PSBT
2. `receiver_process_psbt(psbt, receiver_wallet)` — receiver adds their input and modifies outputs
3. `sender_verify_proposal(original_psbt, proposal_psbt)` — implement ALL 5 security checks
4. `sender_sign_and_broadcast(proposal_psbt, sender_wallet)` — finalize and broadcast
5. `analyze_broadcast_tx(txid)` — verify the on-chain transaction looks like a normal payment

Dependencies: payjoin 0.21, bitcoin 0.32, bitcoincore-rpc 0.19

### Reading
- Payjoin Dev Kit documentation: https://docs.rs/payjoin
- payjoin-rust source code walkthrough (focus on sender.rs and receiver.rs)

---

## Session 11: Payjoin in Production — BTCPay Server & Wallets

**Date:** Month 6, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- BTCPay Server's Payjoin implementation: how it works under the hood
- Bull Bitcoin's BIP77 integration: the first production wallet with async Payjoin
- The adoption challenge: why Payjoin needs more wallet support and what's blocking it
- Running a Payjoin-enabled payment server for a business
- UX considerations: how to make Payjoin invisible to users

### Exercise: BTCPay Payjoin Lab
File: `session-11-production-integration/btcpay_payjoin_lab.md`

1. Set up BTCPay Server locally (Docker) with Payjoin enabled
2. Make a Payjoin payment from a compatible wallet to your BTCPay instance
3. Trace the code path in BTCPay Server: from invoice creation → Payjoin negotiation → broadcast
4. Compare the on-chain footprint: Payjoin payment vs normal payment to the same BTCPay instance
5. Write up: what would it take to add Payjoin support to [wallet X]? (Each participant picks a different wallet)

### Reading
- BTCPay Server Payjoin documentation
- Bull Bitcoin BIP77 announcement and technical writeup
- Andrew Camilleri's BTCPay Payjoin implementation notes

---

## Session 12: Contributing to Payjoin

**Date:** Month 6, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- payjoin-rust codebase: architecture, modules, contribution workflow
- PDK open issues: what needs to be built
- How to add Payjoin support to an existing wallet
- Testing strategies for Payjoin implementations

### Exercise: Your First Payjoin Contribution
1. Clone payjoin/rust-payjoin and build locally
2. Run the test suite — understand what's covered and what isn't
3. Browse open issues — find one that matches your skill level
4. Either: submit a PR (bug fix, test, docs) OR write a detailed review of an open PR

### Contribution Targets
- Add test cases to rust-payjoin
- Improve PDK documentation
- File a well-described issue for an edge case
- Begin Payjoin integration in a wallet that doesn't support it yet
- Review an open PR on payjoin-rust

### Key Repos
- [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin)
- [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver)

---

## Phase 3 Contribution Target

By the end of Phase 3, every participant should submit at least one PR to payjoin-rust, Payjoin Dev Kit, BTCPay Server's Payjoin implementation, or begin a Payjoin integration in a new wallet.

---

## What's Next

Phase 4 moves beyond transactions to network and protocol privacy: Dandelion++ for P2P relay privacy, compact block filters for light client privacy, Floresta and Kyoto for private light nodes, and Taproot's privacy improvements.

---

*[Code Orange Dev School](https://codeorange.dev) · CC0 1.0 Universal*
