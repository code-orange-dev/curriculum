# Module 3: Payjoin — BIP77/78

> 3 sessions — Break the most powerful chain analysis heuristic, build with Payjoin Dev Kit, and contribute to payjoin-rust.

---

## Session 1: How Payjoin Breaks Chain Analysis

### Overview

The common-input-ownership heuristic is the backbone of chain analysis. Payjoin shatters it. In a Payjoin transaction, both sender and receiver contribute inputs — making it impossible to assume all inputs belong to one entity. This session covers how Payjoin works, its evolution from V1 to V2, and why it's one of the highest-leverage privacy improvements available today.

### Topics

**The Common-Input-Ownership Heuristic**
- Why it exists: wallets combine UTXOs automatically when spending
- How chain analysis firms use it: "all inputs in a transaction belong to the same wallet"
- Accuracy: extremely high for normal transactions — the foundation of clustering
- The weakness: it's an assumption, not a rule. Payjoin exploits this.

**Payjoin V1 (BIP78) — Synchronous**
- Original proposal: sender creates a PSBT, sends it to receiver's endpoint
- Receiver adds their own input(s) and adjusts outputs
- Sender verifies, signs, and broadcasts
- Limitation: receiver must run an always-on server (the `pj=` endpoint in BIP21 URI)
- This made V1 impractical for most users

**Payjoin V2 (BIP77) — Asynchronous**
- The breakthrough: outsource receiver's server to an untrusted "Payjoin Directory"
- Receiver posts an encrypted request to the directory
- Sender picks it up, adds their contribution, posts back
- Neither party needs to be online simultaneously
- The directory learns nothing (encrypted payloads)
- Bull Bitcoin: first production wallet to ship BIP77

**Walk Through a Payjoin Transaction Step by Step**
1. Receiver generates a BIP21 URI with `pj=` parameter pointing to their Payjoin endpoint
2. Sender constructs a standard transaction (the "original PSBT")
3. Sender sends the PSBT to the receiver's endpoint
4. Receiver adds one or more of their own inputs to the transaction
5. Receiver adjusts the outputs (receiver's output increases by the value of their added input)
6. Receiver signs their inputs and returns the modified PSBT
7. Sender verifies: their output values haven't decreased, no new outputs were added
8. Sender signs their inputs and broadcasts the final transaction
9. On-chain: looks like a normal multi-input transaction — but CIOH is broken

### Hands-On Exercise

**Analyze a Payjoin transaction:**

Given this transaction:
```
Inputs:
  - 0.5 BTC (address A)
  - 0.3 BTC (address B)
Outputs:
  - 0.7 BTC (address C)
  - 0.1 BTC (address D)
```

Questions:
1. If this is a normal transaction, who owns what? Apply CIOH.
2. If this is a Payjoin, what are the possible ownership combinations?
3. How many different interpretations exist? (This is the "ambiguity set")
4. Can a chain analysis firm tell if this is a Payjoin? Why or why not?

### Discussion Questions

1. Payjoin V1 required the receiver to run a server. Why did that kill adoption?
2. How does Payjoin V2's directory model solve the liveness problem without compromising privacy?
3. If every merchant used Payjoin for payments, what would happen to the CIOH across the entire blockchain?
4. Payjoin increases the receiver's UTXO set. Is this a feature or a bug?

### Reading

- [BIP78: Payjoin V1](https://bips.dev/78/)
- [BIP77: Payjoin V2](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki)
- [Bitcoin Optech: Payjoin](https://bitcoinops.org/en/topics/payjoin/)
- [The Payjoin Experience (Bitcoin Design)](https://bitcoin.design/guide/case-studies/payjoin/)
- [Bull Bitcoin BIP77 announcement](https://www.bullbitcoin.com/blog/bull-bitcoin-wallet-payjoin)

---

## Session 2: Building with Payjoin Dev Kit

### Overview

Payjoin Dev Kit (PDK) is a Rust library that makes it straightforward to integrate Payjoin into any wallet. This session walks through the PDK API and has you send your first Payjoin transaction on testnet.

### Topics

**Payjoin Dev Kit (PDK) — Rust Library Overview**
- Repository: [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin)
- Architecture: sender module, receiver module, directory client
- Key types: `Sender`, `Receiver`, `Request`, `Response`
- How PDK handles the BIP77 asynchronous flow

**Integrating Payjoin into a Wallet (Sender Side)**
- Detect `pj=` parameter in BIP21 payment URI
- Construct the original PSBT using wallet's normal coin selection
- Send the PSBT to the Payjoin endpoint via PDK
- Receive the modified PSBT, verify it, sign, broadcast
- Error handling: what if the receiver is offline? What if verification fails?

**Integrating Payjoin into a Receiver (Merchant/BTCPay)**
- Set up a Payjoin endpoint (V1: HTTP server, V2: directory)
- Receive the sender's PSBT
- Select own input(s) to contribute (UTXO consolidation opportunity)
- Modify outputs, sign, return the modified PSBT
- BTCPay Server's implementation as a reference

### Exercise

See [`exercises/payjoin_testnet.md`](exercises/payjoin_testnet.md)

**Your Task:**
1. Set up a regtest environment with 2 wallets
2. Install and configure the Payjoin Dev Kit
3. Wallet A (sender): construct an original PSBT paying Wallet B
4. Wallet B (receiver): add an input, modify outputs, sign, return
5. Wallet A: verify the modified PSBT, sign, broadcast
6. Inspect the final transaction: can you tell which inputs belong to which wallet?
7. Compare with a non-Payjoin transaction between the same wallets

### Discussion Questions

1. What coin selection strategy should the receiver use when adding inputs?
2. How does Payjoin help receivers consolidate UTXOs "for free"?
3. What checks must the sender perform on the receiver's modified PSBT to prevent attacks?

---

## Session 3: Contributing to Payjoin

### Overview

You've built with Payjoin. Now contribute to it. This session walks through the payjoin-rust codebase, BTCPay Server's implementation, and helps you find your first contribution opportunity.

### Topics

**payjoin-rust Codebase Walkthrough**
- Repository structure: `payjoin/`, `payjoin-cli/`, `payjoin-directory/`
- Key modules: `send/`, `receive/`, `ohttp/`, `directory/`
- The OHTTP (Oblivious HTTP) relay for V2 privacy
- Test suite: integration tests, test vectors
- Open issues and contribution areas

**BTCPay Server's Payjoin Implementation**
- How BTCPay integrates Payjoin for merchant payments
- The `PayjoinClient` and `PayjoinEndpointController` classes
- Configuration options and user experience
- Open issues related to Payjoin in BTCPay

**Bull Bitcoin's BIP77 Integration**
- First commercially available wallet with Payjoin V2
- Mobile wallet architecture considerations
- UX decisions: when to offer Payjoin, how to handle failures
- Lessons from production deployment

### Exercise

**Your First Payjoin PR:**
1. Pick one repository:
   - [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) — Rust
   - [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver) — C#
   - Any wallet integrating BIP77/78
2. Browse open issues — look for "good first issue", documentation improvements, or test coverage gaps
3. Fork, implement, write tests
4. Submit your PR

### Assessment

**Deliverable**: A submitted PR to a Payjoin-related project. Bring the PR link to the next session.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
