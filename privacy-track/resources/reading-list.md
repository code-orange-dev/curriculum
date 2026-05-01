# Reading List

> Resources organized by phase covering all 24 sessions of the Code Orange Bitcoin Privacy Curriculum. Items marked **(R)** are required reading for that session.

## Phase 1: Foundations (Sessions 1-4)

### Bitcoin Privacy Fundamentals

- **(R)** [Bitcoin Wiki: Privacy](https://en.bitcoin.it/wiki/Privacy) - Comprehensive overview of privacy on Bitcoin
- **(R)** [Greg Maxwell CoinJoin proposal (2013)](https://bitcointalk.org/index.php?topic=279249.0) - Original CoinJoin design and rationale
- [Bitcoin Optech: Privacy Topic](https://bitcoinops.org/en/topics/privacy-terminology/) - Privacy terminology and concepts
- [Bitcoin Optech: Coin selection](https://bitcoinops.org/en/topics/coin-selection/) - Wallet algorithms affecting privacy
- [BIP 125: Opt-in Full Replace-by-Fee (RBF)](https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki) - Transaction replacement mechanics

### Coin Selection & Wallet Fingerprinting

- **(R)** [Murch: "Evaluation of Coin Selection Strategies"](https://github.com/murchandamus/thesis) - Thesis on wallet fingerprinting via UTXO selection
- **(R)** [0xB10C: Wallet fingerprinting via change output analysis](https://b10c.me/blog/) - Change pattern detection techniques
- [BIP 69: Lexicographic Indexing of Transaction Inputs and Outputs](https://github.com/bitcoin/bips/blob/master/bip-0069.mediawiki) - Deterministic ordering to prevent fingerprinting
- [Murch: UTXO selection algorithms](https://github.com/murchandamus/bitscripts/tree/master/coinselection) - Reference implementations

### UTXO Model & Privacy

- [Jameson Lopp: "The Ultimate Guide to Bitcoin"](https://www.lopp.net/bitcoin-information.html) - Privacy section covers UTXO model
- [Bitcoin Core reference: Output script types](https://developer.bitcoin.org/reference/transactions.html) - Script types and their identifiability

## Phase 2: Silent Payments (Sessions 5-8)

### BIP 352 Silent Payments Specification

- **(R)** [BIP 352: Silent Payments](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) - Full specification with test vectors
- [BIP 352 GitHub Discussion](https://github.com/bitcoin/bips/issues/1458) - Design rationale and alternatives considered
- [Josie Baker: "Light client support for Silent Payments"](https://github.com/josibake/bitcoin-articles/blob/main/silent_payments_light_client_support.md) - Privacy in SPV clients

### Silent Payments Research & Design

- **(R)** [Ruben Somsen: Silent Payments gist (original design)](https://gist.github.com/RubenSomsen/c43b79517e7cb701ebf77ebc6231d35e) - Original proposal and discussion
- [Silent Payments: Light Client Protocol](https://github.com/bitcoindevkit/bdk/discussions/941) - Client implementation considerations
- [Kixunil: Silent Payments analysis](https://github.com/Kixunil/bips/blob/silent_payments_analysis/bip_0352_analysis.md) - Security analysis

### Implementation & Libraries

- [BDK Silent Payments module](https://github.com/bitcoindevkit/bdk/tree/master/crates/bdk_wallet) - Rust implementation
- [secp256k1 library](https://github.com/bitcoin-core/secp256k1) - Underlying elliptic curve math
- [Rust Secp256k1 bindings](https://docs.rs/secp256k1/latest/secp256k1/) - API documentation
- [Silent Payments test vectors](https://github.com/bitcoin/bips/blob/master/bip-0352/test-vectors.json) - Interoperability testing

## Phase 3: Payjoin (Sessions 9-12)

### Payjoin Specification (BIP 77/78)

- **(R)** [BIP 78: Payjoin (Pay-to-contract Protocol)](https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki) - Full specification
- **(R)** [BIP 77: Payjoin URI scheme](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki) - URI format for initiating payjoin
- [Payjoin Specification](https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki#specification) - Detailed protocol flow

### Payjoin Research & Design

- **(R)** [Dan Gould: "Payjoin is Practical"](https://gist.github.com/dgould/e9bab83f8a89de22babe3e31ef937eee) - Privacy analysis and practical considerations
- [Stonehedge Labs: Payjoin privacy](https://medium.com/coinmonks/payjoin-privacy-analysis-c9e7e7d9a4c0) - Real-world privacy evaluation
- [Dan Gould: Payjoin for PaymentPointers](https://github.com/royalpay/payjoin-paymentpointers) - Extended payjoin protocols

### Implementation & Tools

- [Payjoin Dev Kit (PDK)](https://github.com/payjoin/payjoin) - Reference Rust implementation
- [Payjoin specification reference](https://payjoin.org/) - Payjoin.org resource hub
- [Bluewallet Payjoin support](https://bluewallet.io/payjoin/) - Mobile wallet implementation
- [Sparrow Wallet Payjoin](https://www.sparrowwallet.com/) - Desktop wallet with Payjoin
- [Zeus Payjoin module](https://github.com/ZeusLN/zeus) - Lightning wallet with Payjoin

## Phase 4: Network & Protocol Privacy (Sessions 13-16)

### Dandelion Protocol (BIP 156)

- **(R)** [BIP 156: Dandelion++ (Anonymity in the Bitcoin P2P Network)](https://github.com/bitcoin/bips/blob/master/bip-0156.mediawiki) - Full specification
- [Dandelion++ paper](https://arxiv.org/abs/1805.11060) - Academic research on P2P anonymity
- [Bitcoin Core Dandelion++ PR discussions](https://github.com/bitcoin/bitcoin/pulls?q=dandelion) - Implementation discussion

### Compact Block Filters (BIP 157/158)

- **(R)** [BIP 157: Client Side Block Filtering](https://github.com/bitcoin/bips/blob/master/bip-0157.mediawiki) - Compact block filter specification
- **(R)** [BIP 158: Compact Block Filters for Segregated Witness](https://github.com/bitcoin/bips/blob/master/bip-0158.mediawiki) - Extension for SegWit
- [Oxt.me: BIP 157 analysis](https://oxt.me/blog/) - Privacy analysis of block filters
- [Bitcoin Core BIP 157 PR](https://github.com/bitcoin/bitcoin/pull/18876) - Implementation notes

### Light Client & SPV Privacy

- [Floresta: Stateless Bitcoin validation](https://github.com/bitcoin-dev-kit/floresta) - Light client library
- [Kyoto: BIP 324 transport layer](https://github.com/lexe-app/kyoto) - Privacy-focused light client
- [Electrum: SPV implementation](https://electrum.org/) - Traditional SPV wallet
- [BDK Light Client](https://github.com/bitcoindevkit/bdk/tree/master/crates/bdk_sqlite) - BDK light client support

### Taproot & Tapscript (BIP 340/341/342)

- **(R)** [BIP 340: Schnorr Signatures for secp256k1](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) - Schnorr signature specification
- **(R)** [BIP 341: Taproot: SegWit version 1 spending rules](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) - Taproot specification
- **(R)** [BIP 342: Validation of Taproot Scripts](https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki) - Script validation rules
- [Taproot privacy benefits](https://bitcoinops.org/en/topics/taproot/) - Optech Taproot topic

### Script Privacy & CISA

- [Cross-Input Signature Aggregation (CISA) research](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2024-February/) - Proposed enhancement for privacy
- [CISA design document](https://github.com/sipa/bips/blob/bip-cross-input-aggregation/bip-cross-input-aggregation.mediawiki) - Specification draft

## Phase 5: Advanced (Sessions 17-20)

### CoinJoin & Mixing

- **(R)** [Greg Maxwell: CoinJoin proposal (2013)](https://bitcointalk.org/index.php?topic=279249.0) - Original design
- [WabiSabi: Mixing protocol paper](https://arxiv.org/abs/2106.04253) - Privacy-preserving mixing
- [Whirlpool: Samourai implementation](https://samouraiwallet.com/whirlpool) - Practical mixing service
- [WabiSabi GitHub](https://github.com/zkSNACKs/WabiSabi) - Reference implementation

### Teleport Transactions

- **(R)** [Teleport Transactions: design document](https://github.com/RubenSomsen/teleport-transactions) - Design and motivation
- [Ruben Somsen: Teleport Transactions blog](https://ruben.somsen.com/2020/04/20/teleport-transactions/) - Explanation and privacy analysis

### eCash & Blind Signatures

- **(R)** [David Chaum: "Blind Signatures for Untraceable Payments" (1983)](https://chaum.com/publications/Chaum-blind-signatures.PDF) - Foundational paper
- [Cashu: eCash protocol](https://github.com/cashubtc/cashu) - Bitcoin-backed eCash implementation
- [Cashu NUT (Notation, Usage, and Test vectors)](https://github.com/cashubtc/nuts) - Cashu specification
- [Fedimint: Federated eCash](https://fedimint.org/) - Threshold-signature eCash
- [Fedimint whitepaper](https://docs.fedimint.org/) - Architecture and security

### Lightning Network Privacy

- **(R)** [BOLT 4: Onion Routing](https://github.com/lightning/bolts/blob/master/04-onion-routing.md) - Encrypted routing specification
- [BOLT 11: Invoice Protocol](https://github.com/lightning/bolts/blob/master/11-payment-encoding.md) - Invoice format
- [BOLT 12: Offers](https://github.com/lightning/bolts/blob/master/12-offer-encoding.md) - Upgraded offer protocol
- [Rusty Russell: Lightning privacy analysis](https://rusty.ozlabs.org/) - Expert analysis
- [LND Privacy considerations](https://github.com/lightningnetwork/lnd/blob/master/docs/SAFETY.md) - Node implementation notes

## Phase 6: Building & Contributing (Sessions 21-24)

### Bitcoin Development Kit (BDK)

- **(R)** [BDK Documentation](https://docs.rs/bdk/latest/bdk/) - Complete API reference
- [BDK GitHub](https://github.com/bitcoindevkit/bdk) - Source code
- [BDK tutorial: Building a wallet](https://github.com/bitcoindevkit/bdk/tree/master/examples) - Example code
- [BDK discussions](https://github.com/bitcoindevkit/bdk/discussions) - Community Q&A

### Bitcoin Core & Network

- [Bitcoin Core GitHub](https://github.com/bitcoin/bitcoin) - Main repository
- [Bitcoin Core contributing guide](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md) - Contribution process
- [Bitcoin Core P2P documentation](https://developer.bitcoin.org/reference/p2p_networking.html) - Network protocol
- [Bitcoin Core RPC reference](https://developer.bitcoin.org/reference/rpc/) - API documentation

### Research & Analysis Tools

- **(R)** [OXT Research: Blockchain analysis methodology](https://oxt.me/) - Analysis frameworks and tools
- [Glassnode: On-chain analytics](https://glassnode.com/) - Data and research
- [Chainalysis: Transaction analysis](https://www.chainalysis.com/) - Commercial tool (for defensive knowledge)
- [Elliptic: Privacy risk assessment](https://www.elliptic.co/) - Enterprise tool
- [CoinJoin tracker tools](https://github.com/nopara73/CoinJoinWatch) - Monitoring and detection

### Privacy Tool Development

- [Wasabi Wallet](https://www.wasabiwallet.io/) - Privacy-focused desktop wallet
- [Samourai Wallet](https://samouraiwallet.com/) - Mobile privacy wallet
- [BTCPay Server](https://btcpayserver.org/) - Self-hosted payment processor
- [Electrum Server (ElectrumX)](https://electrumx-spesmilo.readthedocs.io/) - SPV server implementation

## Reference Materials

### Cryptographic Foundations

- [Elliptic Curve Cryptography (ECC) introduction](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography) - Mathematical foundations
- [secp256k1 curve specification](https://en.wikipedia.org/wiki/Secp256k1) - Bitcoin's curve
- [Schnorr signature scheme](https://en.wikipedia.org/wiki/Schnorr_signature) - Signature scheme background
- [Hash functions in Bitcoin](https://en.bitcoin.it/wiki/Hash_functions) - SHA-256, RIPEMD-160, etc.

### Bitcoin Protocol

- [Bitcoin: A Peer-to-Peer Electronic Cash System (Whitepaper)](https://bitcoin.org/bitcoin.pdf) - Original design
- [Bitcoin Script reference](https://en.bitcoin.it/wiki/Script) - Scripting language documentation
- [Bitcoin Transactions](https://developer.bitcoin.org/reference/transactions.html) - Transaction structure
- [Bitcoin Blocks](https://developer.bitcoin.org/reference/block_chain.html) - Block structure and consensus

### Standards & RFCs

- [BIP Index](https://github.com/bitcoin/bips) - All Bitcoin Improvement Proposals
- [BOLT Specification](https://github.com/lightning/bolts) - Lightning Network standards
- [RFC 2104: HMAC](https://tools.ietf.org/html/rfc2104) - Keyed hashing
- [RFC 3394: AES Key Wrap](https://tools.ietf.org/html/rfc3394) - Key encryption

### Learning Resources

- [Mastering Bitcoin by Andreas M. Antonopoulos](https://github.com/bitcoinbook/bitcoinbook) - Technical introduction (free online)
- [Programming Bitcoin by Jimmy Song](https://jimmysong.io/programmingbitcoin/) - Practical coding guide
- [Learning Bitcoin from the Command Line](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line) - Hands-on tutorial
- [Bitcoin Optech](https://bitcoinops.org/) - Technical resources and education

## Session-to-Resource Mapping

| Session | Topic | Key Resources |
|---------|-------|---|
| 1 | Privacy Foundations | Bitcoin Wiki Privacy, Maxwell CoinJoin |
| 2 | UTXO Model | Optech Coin Selection, Lopp guide |
| 3 | Change Analysis | Murch thesis, 0xB10C fingerprinting |
| 4 | Wallet Fingerprinting | BIP 69, wallet implementations |
| 5 | Silent Payments Intro | BIP 352, Somsen gist |
| 6 | SP Key Derivation | BIP 352 spec, secp256k1 docs |
| 7 | SP Light Clients | Josie Baker protocol, BDK |
| 8 | SP in Practice | ENuts, implementation guides |
| 9 | Payjoin Protocol | BIP 77/78, Gould analysis |
| 10 | Payjoin Implementation | PDK, Bluewallet, Sparrow |
| 11 | Receiver Privacy | BIP 78 spec, Gould practical guide |
| 12 | Payjoin + SP | Combined protocols, design docs |
| 13 | P2P Anonymity | BIP 156, Dandelion++ paper |
| 14 | Light Client Privacy | BIP 157/158, Floresta, Kyoto |
| 15 | Transaction Relay | Bitcoin Core P2P, protocol docs |
| 16 | Taproot Privacy | BIP 340/341/342, Optech |
| 17 | CoinJoin Basics | Maxwell proposal, WabiSabi paper |
| 18 | Teleport Txs | Somsen design doc, analysis |
| 19 | eCash & Blind Sigs | Chaum 1983, Cashu/Fedimint docs |
| 20 | Lightning Privacy | BOLT 4, Russell analysis |
| 21 | Wallet Development | BDK docs, examples |
| 22 | Privacy Analysis | OXT methodology, analysis tools |
| 23 | Bitcoin Core Contrib | Contributing guide, source code |
| 24 | Capstone Project | All previous resources |

---

**Last Updated:** May 2026

**Note:** This reading list is maintained as a living document. Resources are curated for accuracy and relevance to Bitcoin privacy. Links may change; GitHub repositories and academic papers are most stable sources.
