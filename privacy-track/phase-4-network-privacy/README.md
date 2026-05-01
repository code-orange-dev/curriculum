# Phase 4: Network & Protocol Privacy — Beyond Transactions

> Months 7-8 · Sessions 13-16 · Transactions aren't the only thing that leaks. Your node, your connections, and your script types tell a story too.

## Overview

Most Bitcoin privacy discussions focus on transaction-level privacy. But your node's network behavior — how it relays transactions, which peers it connects to, which blocks it requests — can reveal just as much. In this phase, you'll learn P2P network privacy (Dandelion++, Tor, I2P), build compact block filters from scratch, evaluate light client privacy tradeoffs, and understand how Taproot fundamentally improves Bitcoin's privacy properties.

## Session 13: P2P Network Privacy — Dandelion++, Tor, I2P

**Date:** Month 7, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- How transaction relay reveals your IP address to network observers
- Dandelion++ (BIP156): stem phase (private relay to one peer) → fluff phase (broadcast to network)
- Why the original Dandelion failed and how Dandelion++ fixes it
- Tor integration in Bitcoin Core: configuration, tradeoffs, Tor-only mode
- I2P integration: how it differs from Tor, advantages and limitations
- Eclipse attacks: how an adversary can isolate your node and what it reveals
- Anchor connections and block-relay-only connections as mitigations

### Exercise: Network Privacy Configuration
1. Configure Bitcoin Core in three modes: clearnet-only, Tor-only, hybrid (clearnet + Tor + I2P)
2. For each mode, analyze: which peers can see your transaction broadcasts? What's your anonymity set?
3. Use `bitcoin-cli getpeerinfo` to examine your peer connections — how many are Tor? I2P? Clearnet?
4. Simulate: if an adversary controls 10% of listening nodes, what's the probability they can link your transaction to your IP in each configuration?
5. Write up: recommended Bitcoin Core privacy configuration for different threat models

### Reading
- BIP156: Dandelion++ — **Required**
- Bitcoin Core Tor documentation
- Giulia Fanti et al.: "Dandelion++: Lightweight Cryptocurrency Networking with Formal Anonymity Guarantees"

---

## Session 14: Compact Block Filters — BIP157/158 Deep Dive

**Date:** Month 7, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- Why light clients need block filtering and why BIP37 Bloom filters failed (privacy disaster)
- BIP158: Golomb-Rice Coded Sets (GCS) — the data structure behind compact block filters
- BIP157: the client-server protocol for requesting and verifying filters
- False positive rates: tuning the M parameter for bandwidth vs privacy
- Filter construction: which data goes into a basic filter
- How compact block filters enable private light client syncing

### Exercise: Compact Block Filters from Scratch (Python)
File: `session-14-compact-block-filters/compact_block_filters.py`

1. Implement `BitWriter` and `BitReader` classes for bit-level I/O
2. Implement `golomb_rice_encode(value, P)` and `golomb_rice_decode(reader, P)`
3. Implement `build_gcs_filter(elements, N, M, P)` — build a complete GCS filter
4. Implement `query_gcs_filter(filter, query_elements, N, M, P)` — check membership
5. Build a filter for a real testnet block and query it for known addresses
6. Measure: false positive rate vs filter size for different M values

### Reading
- BIP158: Compact Block Filters for Light Clients — **Required**
- BIP157: Client Side Block Filtering — **Required**
- Golomb coding: Wikipedia entry for mathematical background
- Jim Posen's BIP157/158 presentation at Scaling Bitcoin

---

## Session 15: Light Client Privacy — Floresta, Kyoto, Neutrino

**Date:** Month 8, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- The light client privacy spectrum: SPV (worst) → CBF (good) → full node (best)
- Floresta: utreexo-based compact node — how utreexo proofs reduce storage while maintaining privacy
- Kyoto: a compact block filter light client in Rust — architecture and privacy properties
- Neutrino: the Go implementation of BIP157/158 used by LND
- Privacy comparison: what does each approach reveal to peers?
- The mobile wallet challenge: how to get full-node-like privacy on a phone

### Exercise: Light Client Privacy Evaluation
1. Set up Floresta and sync it to signet — measure resource usage (disk, bandwidth, time)
2. Read Kyoto's source code: how does it request filters? What does it reveal to the server?
3. Compare privacy properties of 5 light client approaches in a structured matrix: SPV (BIP37), Electrum (trusted server), Neutrino (CBF), Floresta (utreexo), full node
4. For each: what does the server learn? What does a network observer learn? What's the anonymity set?
5. Write up: which light client approach should a privacy-focused mobile wallet use, and why?

### Reading
- Floresta documentation: https://github.com/vinteumorg/Floresta
- Kyoto documentation: https://github.com/rustaceanrob/kyoto
- Tadge Dryja: "Utreexo: A dynamic hash-based accumulator optimized for the Bitcoin UTXO set"

---

## Session 16: Taproot Privacy — Schnorr, MAST & Key Path Spending

**Date:** Month 8, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- How Taproot (BIP340/341/342) improves Bitcoin privacy
- Key path spending: all Taproot outputs look identical on-chain regardless of the spending condition
- Why this matters: 2-of-3 multisig is indistinguishable from a single-sig payment
- MAST (Merkelized Abstract Syntax Trees): hiding unexecuted spending conditions
- MuSig2: n-of-n multisig that produces a single public key and single signature
- FROST: threshold signatures (t-of-n) that look like single-sig
- Cross-Input Signature Aggregation (CISA): future soft fork that would make CoinJoin nearly free
- Taproot adoption metrics: how much of the network uses P2TR?

### Exercise: Taproot Privacy Lab
File: `session-16-taproot-privacy/taproot_privacy_lab.py`

1. Create three Taproot transactions: single-sig key path, 2-of-2 MuSig key path, script path with timelock fallback
2. Compare the on-chain footprint: can an observer tell which is which when key path is used? (No)
3. Create a script-path spend and compare: what information is now revealed?
4. Analyze: what percentage of current Bitcoin transactions use Taproot? Use mempool.space data.
5. Calculate: if CISA were activated, how much would a 100-input CoinJoin save in fees compared to today?

### Reading
- BIP340: Schnorr Signatures — **Required**
- BIP341: Taproot — **Required**
- Pieter Wuille: "Taproot: Privacy Preserving Switchable Scripting"
- AJ Towns: "Cross-Input Signature Aggregation" proposal

---

## Phase 4 Contribution Target

By the end of Phase 4, every participant should submit at least one PR to Floresta, Kyoto, Bitcoin Core (P2P/privacy-related), or another network-layer privacy project.

### Key Repos
- [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta)
- [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto)
- [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) (P2P networking, Tor/I2P, compact block filters)

---

## What's Next

Phase 5 covers advanced privacy techniques: CoinJoin and the WabiSabi protocol, CoinSwap and Teleport Transactions, eCash privacy with Fedimint and Cashu, and Lightning network privacy including blinded paths.

---

*[Code Orange Dev School](https://codeorange.dev) · CC0 1.0 Universal*
