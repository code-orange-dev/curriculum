# Module 2: Silent Payments — BIP352

> 4 sessions — Understand, implement, and contribute to Bitcoin's reusable address protocol.

---

## Session 1: How Silent Payments Work

### Overview

Address reuse is one of Bitcoin's biggest privacy failures. Every time you post a donation address, every payment to it is linked. Silent Payments (BIP352) solve this by allowing a single static address to generate a unique on-chain address for every payment — without any interaction between sender and receiver.

### Topics

**The Problem: Address Reuse Destroys Privacy**
- Posting a Bitcoin address publicly links all payments to your identity
- Even "fresh address per payment" requires interaction (invoice model)
- The donation/tip use case: you need one static address, but reuse destroys privacy
- BIP47 reusable payment codes — the first attempt (requires a notification transaction)

**Static Payment Codes vs Fresh Addresses**
- Traditional: receiver generates a new address for each payment (requires online interaction)
- BIP47: sender sends a notification transaction first, then derives addresses (extra on-chain cost)
- BIP352 Silent Payments: sender derives a unique address from receiver's static code + sender's inputs (no notification, no interaction)

**ECDH Key Exchange for Payment Detection**
- Elliptic Curve Diffie-Hellman: two parties derive a shared secret without prior communication
- The sender uses their private key + receiver's public key → shared secret
- The receiver uses their private key + sender's public key → same shared secret
- This shared secret tweaks the receiver's spend key to produce a unique output address

**Scan Keys vs Spend Keys**
- Silent Payment address encodes two public keys: B_scan and B_spend
- B_scan: used by the receiver to detect incoming payments (can be on a hot/online device)
- B_spend: used to actually spend the received coins (kept cold/offline)
- This separation allows watch-only detection without exposing spending capability

**Walk Through the BIP352 Specification**
- Address format: `sp1q...` (bech32m encoded)
- Sending algorithm: sum input private keys → ECDH with B_scan → tweak B_spend
- Receiving algorithm: for each transaction, compute ECDH with summed input public keys → check outputs
- Label support: receiver can have multiple "sub-addresses" from one Silent Payment address

### Discussion Questions

1. Why doesn't BIP352 require a notification transaction like BIP47 does?
2. What is the privacy trade-off of the scan key being on a hot device?
3. If Silent Payments were in every wallet, how would the anonymity set change?
4. What are the computational costs of scanning? Why is this a challenge for light clients?

### Reading

- [BIP352 Specification](https://bips.dev/352/)
- [Bitcoin Optech: Silent Payments](https://bitcoinops.org/en/topics/silent-payments/)
- [How Silent Payments Work (Otto)](https://medium.com/@ottosch/how-silent-payments-work-41bea907d6b0)

---

## Session 2: Implement a Minimal Silent Payments Sender (Python)

### Overview

You'll implement a simplified Silent Payments sender in Python. By the end of this session, you'll have code that takes a Silent Payment address and constructs a transaction with a unique output that only the receiver can detect.

### Topics

**Generate a Silent Payment Address**
- Derive B_scan and B_spend from a seed/xpub at path m/352h/0h/0h
- Encode as a bech32m `sp1q...` address
- Parse the address to extract the two public keys

**Derive the Shared Secret from Sender Inputs**
- Sum all input private keys (or use the input tweak for Taproot)
- Compute `input_hash = hash(outpoint || A_sum)` for deterministic tweaking
- ECDH: `shared_secret = input_hash * a_sum * B_scan`
- This ensures each transaction produces a different shared secret

**Calculate the Tweak and Output Key**
- `t_k = hash(shared_secret || k)` where k is the output index
- `output_key = B_spend + t_k * G`
- The output is a standard P2TR (Taproot) output paying to `output_key`

**Construct the Transaction**
- Build a transaction with your inputs and the Silent Payment output
- The output looks like any other Taproot output on-chain — no special markers
- Indistinguishable from normal Taproot transactions

### Exercise

See [`exercises/silent_payments_sender.py`](exercises/silent_payments_sender.py)

**Your Task:**
1. Implement the `generate_silent_payment_address()` function
2. Implement the `derive_shared_secret()` function
3. Implement the `compute_output_key()` function
4. Send a Silent Payment on signet using your implementation
5. Verify the output using the receiver's scan key

### Discussion Questions

1. Why do we sum all input private keys rather than using just one?
2. What happens if the sender has only Taproot inputs vs only SegWit inputs?
3. How does the `input_hash` prevent the same shared secret across transactions?

---

## Session 3: Scanning and Receiving Silent Payments

### Overview

Sending is the easy part. Receiving Silent Payments requires scanning every transaction in every block to check if any outputs belong to you. This session covers the computational challenge and the solutions being developed.

### Topics

**The Computational Cost of Scanning**
- For every transaction, the receiver must: extract input public keys → sum them → ECDH with scan key → check each output
- On mainnet: ~300,000 transactions per day = 300,000 ECDH operations
- This is orders of magnitude more expensive than standard address matching
- Why this makes Silent Payments challenging for mobile/light wallets

**Compact Block Filters (BIP157/158) for Efficient Scanning**
- Instead of downloading full blocks, download a compact filter per block
- Filter tells you "this block might contain a transaction for you" (probabilistic)
- Only download the full block when the filter matches
- Dramatically reduces bandwidth and computation for light clients

**Light Client Considerations**
- Kyoto: Rust implementation of BIP157/158 compact block filter client
- Neutrino: Go implementation used by LND
- The trade-off: privacy (compact filters) vs efficiency (trusted server)
- Hybrid approaches: use a trusted server for scanning, verify with your own node

### Exercise

See [`exercises/silent_payments_scanner.py`](exercises/silent_payments_scanner.py)

**Your Task:**
1. Implement `scan_transaction()` — check if a transaction contains a Silent Payment to you
2. Implement `scan_block()` — scan all transactions in a block
3. Benchmark: how long does it take to scan 100 blocks on signet?
4. Implement a basic compact block filter check to skip irrelevant blocks
5. Compare scanning time with and without the filter optimization

### Discussion Questions

1. Why can't Silent Payments use the same simple UTXO scanning as BIP32 wallets?
2. What is an acceptable scanning time for a mobile wallet? How far are we from that?
3. Could a third-party scanning service help without compromising privacy? How?

---

## Session 4: Contributing to Silent Payments

### Overview

You've implemented Silent Payments from scratch. Now it's time to contribute to the real implementations. This session walks through the active codebases and helps you find your first contribution.

### Topics

**Bitcoin Core PR #28122 — Code Walkthrough**
- Where Silent Payments lives in the Bitcoin Core codebase
- The `Sender` class and `GenerateRecipientScriptPubKeys()` method
- The `Recipient` class and `ScanTxOutputs()` method
- Test vectors and how to run the test suite
- Current status and open review comments

**rust-silentpayments Library**
- [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) — standalone Rust library
- API walkthrough: creating addresses, sending, scanning
- How it integrates with rust-bitcoin and BDK
- Open issues and areas needing contribution

**Wallet Integration Status**
- Which wallets are implementing Silent Payments (as of 2026)
- The UX challenges: scanning time, first-use experience, backup/recovery
- What needs to happen for mainstream adoption
- Where your contribution can have the most impact

### Exercise

**Your First PR:**
1. Pick one of these repositories:
   - Bitcoin Core (`bitcoin/bitcoin`) — C++
   - rust-silentpayments (`cygnet3/rust-silentpayments`) — Rust
   - Any wallet implementing BIP352
2. Find an open issue labeled "good first issue" or identify an improvement from the code walkthrough
3. Fork the repo, make your change, write tests
4. Submit your PR with a clear description of what you changed and why
5. Respond to review comments

### Assessment

**Deliverable**: A submitted (not necessarily merged) PR to a Silent Payments implementation. Bring the PR link to the next session for group code review.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
