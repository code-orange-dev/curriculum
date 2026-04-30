# Reading List — Bitcoin Privacy Developer Track

> Organized by module. Required readings are marked with **(R)**. Everything else is recommended.

---

## Foundational

**(R)** [Bitcoin Wiki: Privacy](https://en.bitcoin.it/wiki/Privacy) — The single most comprehensive resource on Bitcoin privacy. Read Sections 1-7 before starting the track.

**(R)** [Bitcoin Optech Topics Index](https://bitcoinops.org/en/topics/) — Reference for every privacy-related topic. Use this as your starting point when researching any concept.

[Chainalysis 2024 Crypto Crime Report](https://www.chainalysis.com/blog/crypto-crime-midyear-2024-update/) — Understand what chain analysis firms actually do and what they claim they can do.

[An Incomplete Survey of Bitcoin's Privacy Technologies (Shymaa Arafat, 2023)](https://arxiv.org/abs/2307.16604) — Academic survey covering the full landscape of Bitcoin privacy research.

[OpenSats: Developing Advancements in On-Chain Privacy](https://opensats.org/blog/developing-advancements-in-onchain-privacy) — OpenSats' own statement on why they fund privacy work. Essential reading for understanding what grant givers value.

---

## Module 1: Chain Analysis

**(R)** [Greg Maxwell: CoinJoin — Bitcoin privacy for the real world (2013)](https://bitcointalk.org/index.php?topic=279249.0) — The post that launched modern Bitcoin privacy research.

**(R)** [Bitcoin Optech: Output Linking](https://bitcoinops.org/en/topics/output-linking/) — Technical overview of how outputs are linked across transactions.

[A Fistful of Bitcoins: Characterizing Payments Among Men with No Names (Meiklejohn et al., 2013)](https://cseweb.ucsd.edu/~smeir/papers/fistfulofbitcoins.pdf) — Foundational academic paper on Bitcoin transaction graph analysis. The techniques described here are still used by chain analysis firms today.

[An Analysis of Anonymity in the Bitcoin System (Reid & Harrigan, 2012)](https://arxiv.org/abs/1107.4524) — One of the earliest academic analyses of Bitcoin privacy.

[Tracking Bitcoin Users Activity Using Community Detection on a Network of Weak Signals (Ermilov et al., 2017)](https://arxiv.org/abs/1710.08158) — Shows how even weak signals (timing, amounts, fee patterns) can be combined to de-anonymize users.

---

## Module 2: Silent Payments

**(R)** [BIP352: Silent Payments](https://bips.dev/352/) — The specification. Read it end to end.

**(R)** [Bitcoin Optech: Silent Payments](https://bitcoinops.org/en/topics/silent-payments/) — Overview with links to all related newsletter entries and podcast discussions.

**(R)** [How Silent Payments Work (Otto)](https://medium.com/@ottosch/how-silent-payments-work-41bea907d6b0) — Clear, accessible explanation with diagrams.

[BIP47: Reusable Payment Codes for Hierarchical Deterministic Wallets](https://bips.dev/47/) — The predecessor to Silent Payments. Understanding why BIP47's notification transaction was a problem helps you appreciate BIP352's design.

[Ruben Somsen: Silent Payments — Bitcoin Seoul 2024](https://www.youtube.com/results?search_query=ruben+somsen+silent+payments) — Talk by the BIP352 co-author explaining design decisions.

[Bitcoin Core PR #28122](https://github.com/bitcoin/bitcoin/pull/28122) — The implementation PR. Read the description and review comments for deep technical context.

[Silent Payments Test Vectors](https://github.com/bitcoin/bips/blob/master/bip-0352/send_and_receive_test_vectors.json) — Official test vectors for validating your implementation.

---

## Module 3: Payjoin

**(R)** [BIP78: Payjoin (V1)](https://bips.dev/78/) — Original synchronous protocol.

**(R)** [BIP77: Payjoin (V2)](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki) — Asynchronous protocol with directory relay.

**(R)** [Bitcoin Optech: Payjoin](https://bitcoinops.org/en/topics/payjoin/) — Overview with all newsletter references.

**(R)** [The Payjoin Experience (Bitcoin Design)](https://bitcoin.design/guide/case-studies/payjoin/) — UX case study on implementing Payjoin in wallets.

[Dan Gould: Payjoin Dev Kit (PDK)](https://payjoindevkit.org/) — Official documentation for the Rust library.

[Bull Bitcoin: BIP77 Announcement](https://www.bullbitcoin.com/blog/bull-bitcoin-wallet-payjoin) — First production wallet to ship Payjoin V2. Discusses implementation decisions and lessons learned.

[Pay to Endpoint (P2EP, 2018)](https://blockstream.com/2018/08/08/en-improving-privacy-using-pay-to-endpoint/) — Blockstream's early proposal that evolved into BIP78. Historical context.

[Bustapay (2018)](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-August/016340.html) — Another early Payjoin variant. Shows the evolution of the idea.

---

## Module 4: Wallet Privacy

### Coin Selection

**(R)** [Bitcoin Optech: Coin Selection](https://bitcoinops.org/en/topics/coin-selection/) — Overview of algorithms and trade-offs.

**(R)** [Murch: An Evaluation of Coin Selection Strategies (2016)](https://murch.one/erhardt2016coinselection.pdf) — The thesis that led to Bitcoin Core's branch-and-bound implementation. Essential reading for understanding the waste metric.

[Bitcoin Core: coinselection.cpp](https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp) — The actual implementation. Read the comments.

### Compact Block Filters

**(R)** [BIP157: Client Side Block Filtering](https://bips.dev/157/) — The network protocol.

**(R)** [BIP158: Compact Block Filters for Light Clients](https://bips.dev/158/) — The filter construction (Golomb-Rice coding).

[Bitcoin Optech: Compact Block Filters](https://bitcoinops.org/en/topics/compact-block-filters/) — Overview with newsletter references.

[Kyoto Light Client](https://github.com/rustaceanrob/kyoto) — Rust implementation. Read the README and examples.

[Neutrino: Privacy-Preserving Bitcoin Light Client (Lightning Labs)](https://github.com/lightninglabs/neutrino) — Go implementation used by LND.

### CoinJoin and CoinSwap

**(R)** [Bitcoin Optech: CoinJoin](https://bitcoinops.org/en/topics/coinjoin/) — Overview.

[WabiSabi Paper](https://github.com/zkSNACKs/WabiSabi/blob/master/WabiSabi.pdf) — The cryptographic protocol behind modern CoinJoin. Technically dense but important for understanding how variable-denomination mixing works.

[Chris Belcher: CoinSwap Design](https://gist.github.com/chris-belcher/9144bd57a91c194e332fb5ca371d0964) — Comprehensive design document for Teleport Transactions.

**(R)** [Bitcoin Optech: CISA](https://bitcoinops.org/en/topics/cross-input-signature-aggregation/) — The proposed soft fork that would make CoinJoin economically incentivized.

[Ark Protocol](https://ark-protocol.org/) — Off-chain payment protocol with privacy properties. Still early but worth understanding.

---

## Advanced / Post-Track

[Dandelion++ (BIP156 draft)](https://arxiv.org/abs/1805.11060) — Transaction relay privacy. Prevents mempool snooping attacks.

[Erlay: Efficient Transaction Relay (BIP330)](https://arxiv.org/abs/1905.10518) — Bandwidth-efficient transaction relay that also improves privacy.

[Bitcoin Optech: Adaptor Signatures](https://bitcoinops.org/en/topics/adaptor-signatures/) — Scriptless scripts that enable private atomic swaps.

[Bitcoin Optech: MuSig2](https://bitcoinops.org/en/topics/musig/) — Multi-signature scheme where the combined signature is indistinguishable from a single signature.

[Blockchain Privacy and Regulatory Compliance: Towards a Practical Equilibrium (Buterin, 2023)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4563364) — Vitalik's paper on balancing privacy and compliance. Different chain, but the framework is applicable.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
