# Bitcoin Privacy Glossary

> Technical terms used throughout the Privacy Developer Track. Entries are ordered by when they first appear in the curriculum.

---

## Module 1: Chain Analysis

**Common-Input-Ownership Heuristic (CIOH):** The assumption that all inputs in a Bitcoin transaction belong to the same entity. This is the most powerful heuristic used by chain analysis firms and is correct for the vast majority of normal transactions. Payjoin specifically exploits this assumption by having both sender and receiver contribute inputs.

**Change output:** The output in a transaction that returns excess funds to the sender. If Alice has a 1 BTC UTXO and wants to send 0.3 BTC to Bob, the transaction creates two outputs: 0.3 BTC to Bob (payment) and ~0.7 BTC back to Alice (change, minus fee). Identifying the change output reveals which address belongs to the sender.

**Address reuse:** Using the same Bitcoin address to receive multiple payments. This links all payments together and to the same entity. HD wallets (BIP32) generate fresh addresses to avoid this, but reuse still occurs with donation addresses, invoices, and careless usage.

**Clustering:** The process of grouping Bitcoin addresses that belong to the same entity by combining CIOH with address reuse and other heuristics. Chain analysis firms maintain databases of clusters mapped to real-world identities.

**Wallet fingerprint:** Metadata in a transaction that reveals which wallet software created it. Includes nLockTime value, nSequence fields, transaction version, fee estimation pattern, input/output ordering, and script types used.

**Fee fingerprinting:** Identifying wallet software by its fee estimation behavior. Bitcoin Core uses `estimatesmartfee` which produces distinctive fee rates. Some wallets use round fee rates (5, 10, 20 sat/vB). Others use fixed rates regardless of mempool conditions.

**Unnecessary input heuristic:** If a transaction has multiple inputs and one input alone would cover the payment + fee, the smaller output is likely the payment (not change). This helps identify change outputs in multi-input transactions.

---

## Module 2: Silent Payments

**Silent Payments (BIP352):** A protocol that allows a receiver to publish a single static payment code from which senders can derive unique on-chain addresses for each payment. No interaction between sender and receiver is required. Each payment goes to a different address that only the receiver can detect.

**ECDH (Elliptic Curve Diffie-Hellman):** A key agreement protocol that allows two parties to derive a shared secret using their respective key pairs. In Silent Payments, the sender uses their private key + receiver's public key to compute the same shared secret that the receiver can compute using their private key + sender's public key.

**Scan key (b_scan / B_scan):** The receiver's key used to detect incoming Silent Payments. The private scan key can be on a hot/online device because it only detects payments — it cannot spend them. The public scan key is part of the Silent Payment address.

**Spend key (b_spend / B_spend):** The receiver's key used to spend received Silent Payments. The private spend key should be kept cold/offline. The public spend key is part of the Silent Payment address.

**Shared secret:** The point on the elliptic curve that both sender and receiver can independently compute via ECDH. In BIP352, this is derived from the sender's input keys and the receiver's scan key, then used to tweak the spend key to produce a unique output address.

**Tweak:** A scalar derived from the shared secret that is added to the receiver's spend key to produce the output public key. Different tweaks for different output indices allow multiple Silent Payment outputs in the same transaction.

**Tagged hash:** A domain-separated hash function defined in BIP340: `SHA256(SHA256(tag) || SHA256(tag) || data)`. Used throughout Silent Payments to prevent cross-protocol attacks. The tags "BIP0352/Inputs" and "BIP0352/SharedSecret" are used for input hashing and tweak derivation respectively.

**Input hash:** A hash of the smallest outpoint and the summed input public keys. This ensures that even if the same sender pays the same receiver twice, different transactions produce different shared secrets (because the outpoints differ).

**Label:** An optional extension in BIP352 that allows a receiver to have multiple "sub-addresses" from a single Silent Payment address. Useful for distinguishing between payment sources (e.g., one label for donations, another for invoice payments).

---

## Module 3: Payjoin

**Payjoin:** A collaborative transaction protocol where both sender and receiver contribute inputs. This breaks CIOH because a chain analyst cannot assume all inputs belong to the same entity. Defined in BIP78 (V1) and BIP77 (V2).

**PSBT (Partially Signed Bitcoin Transaction):** A standardized format (BIP174) for passing unsigned or partially signed transactions between parties. In Payjoin, the sender creates a PSBT, the receiver modifies it (adding their input), and both sign before broadcast.

**BIP78 (Payjoin V1):** The original Payjoin specification requiring the receiver to run an HTTP server. The sender sends a PSBT to the receiver's endpoint, the receiver adds their input and returns the modified PSBT. Limitation: receiver must be online.

**BIP77 (Payjoin V2):** The asynchronous version using a "Payjoin Directory" as an untrusted relay. The receiver posts an encrypted request to the directory; the sender picks it up later. Neither party needs to be simultaneously online. Uses OHTTP for privacy.

**Payjoin Directory:** An untrusted relay server in BIP77 that stores encrypted messages between Payjoin participants. The directory cannot read the messages (end-to-end encrypted) and learns only that a Payjoin is in progress, not the transaction details.

**OHTTP (Oblivious HTTP):** A protocol that hides the client's identity from the server by routing requests through a relay. Used in Payjoin V2 to prevent the directory from linking IP addresses to Payjoin transactions.

**Ambiguity set:** The number of possible interpretations of a transaction's input/output ownership. A normal 2-input, 2-output transaction has 1 interpretation (CIOH: both inputs are the sender's). A Payjoin with the same structure has multiple interpretations, making chain analysis unreliable.

**Payjoin Dev Kit (PDK):** A Rust library (`payjoin/rust-payjoin`) that implements both BIP77 and BIP78, providing sender and receiver APIs for wallet developers to integrate Payjoin support.

---

## Module 4: Wallet Privacy

**Coin selection:** The algorithm a wallet uses to choose which UTXOs to spend in a transaction. Different algorithms (largest-first, branch-and-bound, random) have different privacy and fee implications.

**Branch and bound:** A coin selection algorithm that searches for a combination of UTXOs whose total value exactly matches the target amount plus fees, eliminating the need for a change output. Used by Bitcoin Core as the preferred selection method.

**Waste metric:** A measure of the total cost of a coin selection result, including: fees paid in this transaction, cost of creating a change output, and future cost of spending the change. Minimizing waste optimizes for both fee efficiency and privacy.

**UTXO label:** A tag applied to a UTXO indicating its source or privacy level (e.g., "exchange", "coinjoin", "salary"). Privacy-conscious wallets refuse to combine UTXOs from different labels to prevent linking separate identities.

**Compact block filter (BIP158):** A probabilistic data structure that summarizes all the scriptPubKeys in a block. A light client downloads these small filters (~20KB each) and checks if any of their addresses might be in the block, without revealing which addresses they're watching to the serving node.

**Golomb-Rice coding:** The compression algorithm used in BIP158 filters. It efficiently encodes sorted lists of values where deltas between consecutive values follow a geometric distribution. The parameter P=19 gives a false positive rate of approximately 1/784,931.

**False positive:** When a compact block filter indicates a block might contain a relevant transaction when it actually doesn't. The client downloads the full block and discovers no match. BIP158's false positive rate is designed to be low enough that this wastes minimal bandwidth.

**BIP157 (Client Side Block Filtering):** The network protocol that defines how light clients request and verify compact block filters from full nodes. Includes filter headers (a chain of commitments) that allow clients to detect if a node sends incorrect filters.

**BIP37 (Bloom filter):** The older light client protocol where the client sends a Bloom filter of their addresses to a full node, and the node returns matching transactions. Privacy is poor because the node can determine which addresses the client is watching with high probability.

**CoinJoin:** A privacy technique where multiple users combine their inputs and outputs into a single transaction. The equal-value outputs cannot be linked to specific inputs, breaking the transaction graph. Coordinated by a central server (Wasabi/Ginger) or a decentralized market (JoinMarket).

**WabiSabi:** A cryptographic protocol used in modern CoinJoin implementations (Wasabi Wallet, Ginger Wallet) that allows variable-denomination outputs while maintaining anonymity. Uses keyed-verification anonymous credentials to prevent the coordinator from linking inputs to outputs.

**Anonymity set:** The number of equal-value outputs in a CoinJoin transaction. If 50 participants each create a 0.01 BTC output, each output has an anonymity set of 50 — an observer cannot distinguish between the 50 possible owners.

**CoinSwap:** A privacy technique where two parties atomically swap UTXOs. Unlike CoinJoin, the two transactions look like normal payments on-chain — there is no recognizable multi-party pattern. Uses hash time-locked contracts (HTLCs) or adaptor signatures for atomic execution.

**Teleport Transactions:** Chris Belcher's implementation of CoinSwap for Bitcoin. Supports multi-hop swaps through intermediaries for stronger privacy. Currently in development, funded by OpenSats.

**JoinMarket NG:** The next generation of JoinMarket, a decentralized CoinJoin marketplace where "makers" provide liquidity (UTXOs for mixing) and "takers" pay a fee to mix their coins. Uses fidelity bonds to prevent Sybil attacks.

**Fidelity bond:** Bitcoin locked in a time-locked output that proves a JoinMarket maker has "skin in the game." Larger and longer-locked bonds make Sybil attacks (where an adversary runs many maker nodes to de-anonymize takers) prohibitively expensive.

**CISA (Cross-Input Signature Aggregation):** A proposed soft fork that would allow all signatures in a transaction to be aggregated into a single signature. This makes CoinJoin transactions cheaper (fewer bytes = lower fees), creating an economic incentive for privacy. Currently in research/proposal stage.

**Taproot (BIP341):** A soft fork activated in November 2021 that makes all spend conditions (single-sig, multisig, HTLC, etc.) look identical on-chain when the cooperative path is used. This improves privacy by making complex spending conditions indistinguishable from simple payments.

**nLockTime:** A transaction field specifying the earliest block height or timestamp at which the transaction can be included in a block. Bitcoin Core sets this to the current block height as an anti-fee-sniping measure, which serves as a wallet fingerprint.

**nSequence:** A per-input field originally intended for transaction replacement. Its value varies by wallet software, serving as another fingerprint. Modern wallets use 0xFFFFFFFD (signals RBF) or 0xFFFFFFFE (final, no RBF).

**Dust limit:** The minimum value a transaction output must have to be considered "standard" by Bitcoin Core's relay policy (currently 546 satoshis for P2WPKH). Outputs below this limit are uneconomical to spend and may reveal information about the wallet's coin selection algorithm.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
