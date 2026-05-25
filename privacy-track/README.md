# Bitcoin Privacy Developer Track

**24 bi-weekly sessions. 12 months. Every session produces a contribution to Bitcoin base-layer privacy.**

---

## Why This Track Exists

> *"There are real privacy gaps on-chain today. Much of that sits in wallet behavior and transaction construction, which makes it a great area for open-source development."* — [OpenSats, Spring 2026 Call for Applications](https://opensats.org/blog/call-for-applications-spring-2026)

Bitcoin's base layer has privacy problems that affect every user: address reuse exposes payment history, the common-input-ownership heuristic lets chain analysis firms cluster wallets, wallet software creates identifiable fingerprints in every transaction, and light clients leak user addresses to third parties.

The solutions exist — [Silent Payments](https://opensats.org/topics/silent-payments), [Payjoin](https://opensats.org/topics/payjoin), [Coinswap](https://opensats.org/blog/developing-advancements-in-onchain-privacy#coinswap), compact block filters ([BIP157](https://opensats.org/topics/bip-157)/[BIP158](https://opensats.org/topics/bip-158)), [ASmap](https://opensats.org/blog/bitcoin-grants-september-2024-7th-wave#asmap), and privacy-aware transaction construction — but they need developers to build, integrate, and maintain them. The biggest bottleneck in Bitcoin privacy is not research. It is a shortage of developers who understand the problems deeply enough to write the code.

**This curriculum produces those developers.**

From session 1, participants read real Bitcoin source code and engage with real repos. By session 8, they've submitted their first PR. By session 24, they have 5-8 PRs across 3+ repos — to the same projects that [OpenSats](https://opensats.org/), [HRF](https://hrf.org/), and [Brink](https://brink.dev/) fund.

---

## Format

| | |
|---|---|
| **Structure** | 24 bi-weekly sessions (every 2 weeks), 2-2.5 hours each |
| **Duration** | 12 months |
| **Prerequisites** | Basic Bitcoin knowledge (completed Bitcoin Dojo or equivalent). Comfortable reading code. Python or Rust experience helpful. |
| **Outcome** | Every graduate has multiple merged PRs across Bitcoin privacy projects. Every graduate can articulate what base-layer privacy problems remain unsolved and how to fix them. |
| **License** | CC0 1.0 Universal (public domain) |

---

## What This Track Directly Addresses

This curriculum is built around the specific Layer 1 privacy gaps identified by the Bitcoin open-source funding ecosystem:

| Privacy Gap | Why It Matters | Where We Contribute | Sessions |
|---|---|---|---|
| **Address reuse** | Exposes full payment history to anyone who knows one address | [Silent Payments (BIP352)](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki), [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), wallet integrations | 5-8 |
| **Common-input-ownership heuristic** | Lets chain analysis cluster all UTXOs in a wallet from a single transaction | [Payjoin Dev Kit (BIP77/78)](https://github.com/payjoin/rust-payjoin), wallet integrations, [BTCPay Server](https://github.com/btcpayserver/btcpayserver) | 9-12 |
| **Wallet fingerprinting** | Transaction construction patterns reveal which wallet software you use | [Bitcoin Core](https://github.com/bitcoin/bitcoin) wallet, [BDK](https://github.com/bitcoindevkit/bdk), any wallet that constructs transactions | 2-4, 22 |
| **Light client privacy** | SPV and Electrum clients leak addresses to servers | [Kyoto (BIP157/158)](https://github.com/rustaceanrob/kyoto), [Floresta](https://github.com/vinteumorg/Floresta) | 7, 14-15 |
| **P2P network surveillance** | Transaction relay and peer connections reveal IP-to-transaction links | [Bitcoin Core P2P](https://github.com/bitcoin/bitcoin), Dandelion++, [ASmap](https://github.com/sipa/asmap), Tor/I2P integration | 13-14 |
| **Transaction graph analysis** | On-chain transaction chains can be followed across hops | [Coinswap/Teleport](https://github.com/nickhntv/teleport-transactions), [JoinMarket NG](https://github.com/nickhntv/joinmarket-ng), CoinJoin tooling | 17-18 |
| **Coin selection privacy leaks** | Poor UTXO selection reveals payment amounts and change outputs | [Bitcoin Core coin selection](https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp), [BDK](https://github.com/bitcoindevkit/bdk) | 3, 21 |
| **Taproot adoption gap** | Low Taproot usage means multisig, timelocks, and complex scripts remain distinguishable on-chain | Wallet integrations, [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin), BDK defaults | 16 |

---

## The Contribution Ladder

Contributions scale with knowledge. Nobody gets thrown into the deep end.

| Sessions | Contribution Level | Examples |
|---|---|---|
| 1-4 | **Engage** | Star repos, read source code, file issues, improve docs |
| 5-8 | **Submit** | Review PRs, add test cases, submit first PR |
| 9-12 | **Build** | Fix bugs, add features, submit PRs to multiple repos |
| 13-16 | **Lead** | Tackle harder issues, review others' PRs, mentor newcomers |
| 17-20 | **Research** | Identify gaps, propose improvements, build new tooling |
| 21-24 | **Ship** | Substantial contributions, present to community, join fellowship |

---

## Curriculum

### Phase 1: Foundations — How Privacy Breaks on Bitcoin's Base Layer
*Months 1-2 · Sessions 1-4*

> *"Traditional banking provides a fair amount of privacy by default... Poor privacy in Bitcoin can be a major practical disadvantage for both individuals and businesses."* — Greg Maxwell, 2013

Before building privacy solutions, developers must understand exactly how privacy fails today. This phase teaches the 5 primary chain analysis heuristics, how wallet software creates identifiable fingerprints, and why privacy must be solved at the protocol and wallet level — not bolted on as an afterthought.

---

#### Session 01: Chain Analysis & Surveillance — How Privacy Fails Today

**The problem:** Chain analysis firms like Chainalysis and Elliptic use 5 core heuristics to deanonymize Bitcoin users. Every on-chain transaction reveals information. Understanding what it reveals — and why — is the prerequisite for building solutions.

**Learn:**
- The 5 primary chain analysis heuristics: common-input-ownership (CIOH), change detection, address reuse, timing analysis, amount correlation
- How chain analysis firms cluster addresses into identity groups
- What the UTXO model reveals vs what an account model reveals
- Why privacy is a protocol-level requirement, not a user preference — with real-world examples of harm from poor financial privacy (targeted theft, business intelligence leaks, discrimination)
- The chain analysis arms race: what's detectable today that wasn't 3 years ago

**Build:**
- Trace a 5-hop transaction chain on [mempool.space](https://mempool.space) and [OXT.me](https://oxt.me)
- Apply CIOH to cluster addresses. Identify likely change outputs using 4 different heuristics
- Write a Python script that takes a transaction ID and returns: input count, output count, script types, likely change output, fee rate, and a "privacy score" (0-100)
- Analyze 10 real mainnet transactions and classify each by privacy quality

**Contribute this session:**
- Create a GitHub account if you don't have one
- Star and fork these 7 repos (the projects you'll contribute to over 12 months):
  - [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) — Bitcoin Core
  - [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) — Silent Payments library
  - [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) — Payjoin Dev Kit
  - [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta) — Privacy-preserving light client
  - [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) — BIP157/158 compact block filter client
  - [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk) — Bitcoin Dev Kit
  - [rust-bitcoin/rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) — Rust Bitcoin library
- Clone `bitcoin/bitcoin` and build it locally. Read `src/wallet/coinselection.cpp` — you won't understand all of it yet, but you start reading real Bitcoin code on day one
- Read the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy). Identify one section that's outdated or unclear — you'll file an issue or edit later

**Reading:**
- [Bitcoin Privacy Wiki](https://en.bitcoin.it/wiki/Privacy) (read fully)
- Greg Maxwell's [CoinJoin original post](https://bitcointalk.org/index.php?topic=279249.0) (2013)
- [An Empirical Analysis of Traceability in the Monero Blockchain](https://arxiv.org/abs/1704.04299) — read the methodology, not for Monero but to understand how academic deanonymization research works

---

#### Session 02: Transaction Anatomy for Privacy — What Every Byte Reveals

**The problem:** Every field in a raw Bitcoin transaction carries information. Version numbers, locktime values, sequence numbers, output ordering, script types, and fee rates create fingerprints that identify which wallet software created the transaction. A chain analyst doesn't even need heuristics — sometimes the transaction format alone tells them everything.

**Learn:**
- Raw transaction structure byte-by-byte: nVersion, vin[], vout[], nLockTime
- How nVersion, nLockTime, and nSequence differ across wallet implementations — and why those differences matter
- Script types and their privacy implications: P2PKH, P2SH, P2WPKH, P2WSH, P2TR
- Fee estimation patterns as wallet fingerprints
- Output ordering: BIP69 (deterministic) vs random vs amount-sorted — each is a tell
- How [0xB10C's wallet fingerprinting research](https://b10c.me/observations/03-blocktemplate-coinbase-transactions/) revealed identifiable patterns in production wallets
- Why transaction construction is the Layer 1 privacy problem OpenSats specifically wants solved

**Build:**
- Decode 5 raw testnet transactions manually. For each, extract: version, locktime, sequence values, script types, fee rate, output ordering
- Determine which wallet software likely created each transaction based on fingerprints alone
- Construct a raw transaction that avoids all known wallet fingerprints — use random output ordering, anti-fee-sniping locktime, minimal nSequence signaling, and consistent script types

**Contribute this session:**
- Pick one wallet (Sparrow, BlueWallet, Electrum, Green, Nunchuk). Test its current version against known fingerprint patterns. Document: wallet version, transaction version, locktime behavior, sequence behavior, output ordering, script type defaults, fee estimation pattern
- If the behavior differs from published research, this is an issue worth filing. Draft a GitHub issue (you'll submit it in Session 4 after review)
- Browse the [Bitcoin Optech Topics page](https://bitcoinops.org/en/topics/). Find the "Transaction compatibility" section. Note anything missing or outdated

**Reading:**
- 0xB10C's [wallet fingerprinting observations](https://b10c.me/)
- [Wallet fingerprinting and transaction construction](https://ishaana.com/blog/wallet_fingerprinting/) by Ishaana Misra
- Bitcoin Core source: `src/wallet/spend.cpp` — focus on `CreateTransaction()` and how it sets version, locktime, output ordering

---

#### Session 03: UTXO Management & Coin Selection — The Hidden Privacy Leak

**The problem:** How a wallet chooses which UTXOs to spend reveals enormous amounts of information. A wallet that always uses the largest UTXO creates different patterns than one using branch-and-bound. Change outputs can reveal payment amounts. Dust UTXOs can be used for tracking. This is where [Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp) and [BDK](https://github.com/bitcoindevkit/bdk) — two of the most important foundational libraries funded by OpenSats — directly affect every user's privacy.

**Learn:**
- 4 coin selection algorithms: largest-first, branch-and-bound (BnB), knapsack, and random
- How each algorithm affects privacy differently — and why BnB is preferred when it finds an exact match (no change output = no change detection heuristic)
- [Murch's coin selection research](https://murch.one/wp-content/uploads/2016/11/erhardt2016coinselection.pdf) and its influence on Bitcoin Core
- Dust attacks: how tiny UTXOs are used as tracking beacons
- Coin control: manual UTXO selection as a privacy tool
- How BDK exposes coin selection to wallet developers — and why privacy-aware defaults matter

**Build:**
- Implement all 4 coin selection algorithms in Python
- Run each against an identical UTXO set for the same payment amount
- Score each for privacy leakage: input count, change amount, whether change is detectable, total fees
- Identify which algorithm produces a changeless transaction (if any) for the given inputs and amount
- Build a "privacy-optimized" selector that prefers: changeless transactions > same-script-type change > minimal input count

**Contribute this session:**
- Read Bitcoin Core's coin selection: `src/wallet/coinselection.cpp` and `src/wallet/spend.cpp`. Find a comment that could be clearer, a variable name that's confusing, or an edge case that isn't tested. Even a 1-line documentation improvement counts
- Browse [BDK issues labeled "coin-selection"](https://github.com/bitcoindevkit/bdk/labels/coin-selection). Read through open issues. If you can reproduce one, comment with your findings
- Look at Murch's research. Are the algorithms described there fully implemented in Bitcoin Core today? If something's missing, that's a potential contribution

**Reading:**
- Murch's [coin selection thesis](https://murch.one/wp-content/uploads/2016/11/erhardt2016coinselection.pdf)
- Bitcoin Core source: `src/wallet/coinselection.cpp` (full file)
- BDK documentation on [coin selection](https://docs.rs/bdk_wallet/latest/bdk_wallet/)

---

#### Session 04: Wallet Fingerprinting & Privacy-Clean Transaction Construction

**The problem:** If every Bitcoin wallet constructed transactions identically, chain analysis would lose one of its most powerful tools. But they don't — each wallet makes different choices about version, locktime, sequence, output ordering, script types, and fees. Fixing this requires work in the foundational libraries ([rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin), [BDK](https://github.com/bitcoindevkit/bdk)) and in individual wallets that build on them. This is the "deeper integration of existing techniques into widely used wallets" that the privacy funding ecosystem wants to see.

**Learn:**
- Complete catalog of known wallet fingerprints: Bitcoin Core, Electrum, BlueWallet, Wasabi, Sparrow, Green, Nunchuk, Samourai (legacy)
- How to construct a "fingerprint-clean" transaction: randomized output ordering, anti-fee-sniping locktime, consistent script types, standard fee rates
- Transaction batching and its privacy implications — when it helps and when it hurts
- How rust-bitcoin's transaction builder API affects downstream wallet privacy
- The concept of "privacy by default" in wallet design — users shouldn't need to think about fingerprinting

**Build:**
- Given 10 raw transactions, identify which wallet created each by analyzing every available signal
- Construct a raw transaction that avoids all known fingerprints. Have another participant try to identify the wallet — if they can't, you succeeded
- Write a "transaction construction privacy checklist" that wallet developers can use as a reference

**Contribute this session — your first real contribution:**
- **Option A:** File an issue on a Bitcoin wallet repo documenting a privacy fingerprint you discovered. Include: wallet version, the specific fingerprint, and why it matters for privacy. Target: [BlueWallet](https://github.com/BlueWallet/BlueWallet), [Sparrow](https://github.com/sparrowwallet/sparrow), [Green](https://github.com/nickhntv/GreenBits), or any wallet you tested
- **Option B:** Submit a documentation PR to the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy) adding your fingerprint data
- **Option C:** Submit a PR to [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) or [BDK](https://github.com/bitcoindevkit/bdk) improving transaction construction documentation or adding a privacy-related test case
- **Option D:** Write up your wallet fingerprinting analysis as a structured report and publish it as a GitHub gist — share in Code Orange Discord for community review

> **Phase 1 checkpoint:** Every participant has starred 7 repos, read real Bitcoin Core source code, analyzed real transactions, and filed at least 1 issue or documentation PR. They understand the 5 chain analysis heuristics and how wallet behavior creates privacy leaks.

---

### Phase 2: Silent Payments (BIP352) — Solving Address Reuse at the Protocol Level
*Months 3-4 · Sessions 5-8*

> Silent Payments let anyone receive bitcoin to a unique address without the sender and receiver needing to interact first. Every on-chain transaction that uses Silent Payments instead of reusing addresses raises the baseline privacy of everyday users. — [OpenSats](https://opensats.org/topics/silent-payments)

Address reuse is the most common on-chain privacy failure. Static donation addresses, payment pages, and QR codes all reuse addresses — exposing the full payment history of the recipient to anyone who looks. [BIP352 Silent Payments](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) solves this by deriving unique addresses from a single public identifier using ECDH, without requiring any interaction between sender and receiver.

This phase builds the cryptography from scratch, contributes to [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), and tackles the scanning problem that makes SP adoption challenging for light clients — which is where [Kyoto](https://github.com/rustaceanrob/kyoto) and compact block filters ([BIP157/158](https://opensats.org/topics/bip-157)) become critical.

---

#### Session 05: BIP352 Deep Dive — How Silent Payments Work

**The problem:** Existing solutions to address reuse (HD wallets, BIP47 payment codes) require interaction — the receiver must give the sender a fresh address. This breaks down for donations, payment pages, and any scenario where the receiver can't be online. Silent Payments solve this using ECDH to derive unique outputs from a single static identifier.

**Learn:**
- The address reuse problem in depth: what exactly is revealed and to whom
- ECDH (Elliptic Curve Diffie-Hellman) shared secret derivation on secp256k1
- BIP352 specification walkthrough: scan keys vs spend keys, how the shared secret produces a unique output address, labeling for payment identification
- Why scanning is computationally expensive — the sender's public keys must be extracted from every transaction input, and ECDH computed for each
- How Silent Payments compare to BIP47 (payment codes) and stealth addresses — and why BIP352's design is superior for on-chain privacy
- Current implementation status: Bitcoin Core PR [#28122](https://github.com/bitcoin/bitcoin/pull/28122), [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), wallet integrations in progress

**Build:**
- Derive Silent Payment shared secrets by hand using pure Python secp256k1 math
- Given a sender's private key and an SP address, compute the output key step by step: extract scan key, compute ECDH shared secret, derive tweak, add to spend key
- Verify your result against the official [BIP352 test vectors](https://github.com/bitcoin/bips/tree/master/bip-0352)

**Contribute this session:**
- Read the [BIP352 specification](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) end to end. If anything is ambiguous or could be explained better, file an issue on [bitcoin/bips](https://github.com/bitcoin/bips) with a specific suggestion
- Clone [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments). Build it. Run the test suite. Read `sending.rs` — you just implemented this math by hand. Note any discrepancies between the code and the spec
- Browse [rust-silentpayments open issues](https://github.com/cygnet3/rust-silentpayments/issues). Comment on one with your understanding of the problem. Engaging with maintainers is how you build the relationships that lead to merged PRs

---

#### Session 06: Implement a Silent Payments Sender

**Learn:**
- Complete SP send flow: input selection, key aggregation for multiple inputs, shared secret computation, output key derivation, transaction construction
- Handling edge cases: single vs multiple inputs, Taproot vs SegWit inputs, multiple SP recipients in one transaction
- Testing against the full BIP352 test vector suite

**Build:**
- Implement the full SP sending pipeline in Python: parse SP address → aggregate sender input keys → compute ECDH shared secret → derive output key → construct transaction
- Handle all edge cases: single Taproot input, mixed input types (P2WPKH + P2TR), multiple SP recipients
- Run your implementation against every test vector in [BIP352's test suite](https://github.com/bitcoin/bips/tree/master/bip-0352). All must pass

**Contribute this session:**
- Check the BIP352 test vectors. Are any edge cases missing? (e.g., single P2PKH input, 3+ SP recipients, change output handling). If you find a gap, file an issue on [bitcoin/bips](https://github.com/bitcoin/bips) proposing the additional test vector
- Add a test case to [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) exercising an edge case you identified. Even if you're not confident in Rust, writing the test (data setup + assertion) is a great starting contribution
- If you're more comfortable in Python: clean up your sender implementation, add docstrings, and publish it as a reference tool on GitHub tagged `silent-payments` and `bitcoin`

---

#### Session 07: Scanning, Receiving & Compact Block Filters (BIP157/158)

**The problem:** Receiving Silent Payments requires scanning every transaction in every block — extracting sender public keys and computing ECDH for each. For a full node this is feasible but CPU-intensive. For a light client, it's the core challenge. This is where [compact block filters (BIP157/158)](https://opensats.org/topics/bip-157) and projects like [Kyoto](https://github.com/rustaceanrob/kyoto) become essential — they let light clients check whether a block *might* contain relevant transactions without downloading the full block or revealing their addresses to a server.

**Learn:**
- The SP scanning algorithm: for each transaction, extract input public keys → compute ECDH → check if any output matches
- Compact block filters: Golomb-Rice Coded Sets (GCS), false positive rates, how BIP157 client-server protocol works
- How CBFs optimize SP scanning: download filter → check if block might have SP outputs → download full block only if filter matches
- Bandwidth vs privacy tradeoffs: full node scanning vs CBF light client vs Electrum-style server query
- [Kyoto](https://github.com/rustaceanrob/kyoto) architecture — a BIP157/158 light client implementation in Rust that Silent Payments and other privacy tools rely on
- Tweak caching and other scanning optimizations

**Build:**
- Build a minimal SP scanner in Python: given a scan private key, iterate through blocks and find outputs addressed to you
- Implement Golomb-Rice encoding/decoding from scratch
- Build a compact block filter. Query it for a known output. Measure false positive rate
- Combine: use your CBF to skip blocks, then full-scan only matching blocks. Measure the speedup

**Contribute this session:**
- Review an open PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) related to Silent Payments or compact block filters. You don't need to ACK it — just leave a thoughtful review: "I tested this locally and it works" or "This section is unclear because..." Both are valuable
- Clone [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto). Build it. Run it. Browse issues — this is an early-stage project that needs contributors. Filing well-described bugs from testing is valuable
- If you found performance issues or bugs in your scanner, file them on the relevant repo with reproduction steps

---

#### Session 08: Contributing to Silent Payments — Your First PR

**Learn:**
- Bitcoin Core SP implementation walkthrough: code paths, test structure, review process
- [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) architecture deep dive
- Current wallet integration status: which wallets support SP, which are working on it, where the gaps are
- How to write a PR that gets reviewed and merged: commit messages, test coverage, description format

**Build:**
- Clone your target repo. Build locally. Run full test suite. Pick a Good First Issue. Write your fix. Submit your first PR.

**Contribute this session — submit a PR:**
- **Option A (Rust):** Add a test case, fix documentation, or implement a small feature in [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) or [Kyoto](https://github.com/rustaceanrob/kyoto)
- **Option B (C++):** Review and test a Silent Payments PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin). Leave a detailed review with test results
- **Option C (Any language):** Improve documentation for Silent Payments: BIP352, wallet integration guides, Bitcoin Optech
- **Option D (Ambitious):** Start integrating Silent Payments into a wallet that doesn't have it yet — even a proof-of-concept on a branch counts

The facilitator pairs each participant with a specific issue matching their skill level. **Nobody leaves this session without a PR submitted or a substantive review posted.**

> **Phase 2 checkpoint:** Every participant has submitted at least 1 PR or detailed code review to a Silent Payments or compact block filter project. They understand BIP352 cryptography, the scanning problem, and how CBFs enable light client privacy.

---

### Phase 3: Payjoin (BIP77/78) — Breaking the Most Powerful Chain Analysis Heuristic
*Months 5-6 · Sessions 9-12*

The common-input-ownership heuristic (CIOH) is the single most powerful tool in chain analysis. It assumes that all inputs in a transaction belong to the same entity. [Payjoin](https://opensats.org/topics/payjoin) breaks this assumption by having both sender and receiver contribute inputs to a collaborative transaction — making the on-chain result indistinguishable from a regular payment, but invalidating CIOH for that transaction and every transaction the analyst tries to cluster from it.

Unlike CoinJoin (which creates distinctive equal-output transactions), Payjoin transactions look like ordinary payments. This means Payjoin improves privacy for *all* Bitcoin users, not just Payjoin users — because analysts can no longer assume CIOH holds for any transaction.

[Payjoin Dev Kit](https://opensats.org/projects/pdk) and [Async Payjoin (BIP77)](https://opensats.org/projects/pdk) are actively funded by OpenSats. The [rust-payjoin](https://github.com/payjoin/rust-payjoin) library needs contributors for integration, testing, and adoption.

---

#### Session 09: BIP77/78 Theory — How Payjoin Defeats Chain Analysis

**Learn:**
- CIOH in depth: why it's chain analysis's most powerful tool, how many wallets it clusters, and what breaks when it fails
- Payjoin V1 (BIP78): the original interactive protocol — how it works, its limitations (receiver must be online)
- Payjoin V2 (BIP77, "Async Payjoin"): the serverless, asynchronous protocol — how it eliminates the online requirement using the Payjoin Directory
- The 5 critical sender verification checks that prevent output substitution attacks
- Why Payjoin is more powerful than CoinJoin for systemic privacy: it poisons the CIOH assumption for *all* transactions, not just participants'
- Current adoption: [BTCPay Server](https://github.com/btcpayserver/btcpayserver), [Bull Bitcoin](https://www.bullbitcoin.com/), [Mutiny Wallet](https://www.mutinywallet.com/)

**Build:**
- Analyze 10 testnet transactions — determine which are Payjoins (hint: it should be hard to tell)
- Walk through the full BIP77 async flow: sender creates original PSBT → posts to directory → receiver modifies PSBT (adds inputs, adjusts outputs) → sender validates 5 checks → sender signs and broadcasts
- Implement all 5 sender verification checks in pseudocode. Understand why each one is necessary to prevent theft

**Contribute this session:**
- Clone [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin). Build it. Run the test suite. Read `src/send.rs` and `src/receive.rs` — you just learned this flow
- Browse [rust-payjoin open issues](https://github.com/payjoin/rust-payjoin/issues). Issues labeled `good first issue` are your targets. Comment on one to claim it or ask clarifying questions
- Read the [BIP77 specification](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki) and Dan Gould's design documents. If you find inconsistencies, file an issue

---

#### Session 10: Building with Payjoin Dev Kit (Rust)

**Learn:**
- [PDK (Payjoin Dev Kit)](https://github.com/payjoin/rust-payjoin) architecture: send module, receive module, PSBT handling, the Payjoin Directory
- PSBT construction and modification: how PDK creates, modifies, and validates PSBTs
- Integrating PDK into a wallet application: the minimum code needed to add Payjoin support
- Testing Payjoin flows on signet

**Build:**
- Complete Payjoin flow in Rust using PDK:
  1. Sender creates original PSBT
  2. Receiver modifies it (adds input, adjusts change)
  3. Sender validates all 5 checks
  4. Sender signs and broadcasts
- Analyze the on-chain result — can you tell it was a Payjoin?
- Measure the size overhead vs a regular transaction

**Contribute this session:**
- Your PDK integration exercise surfaced rough edges. File issues on [rust-payjoin](https://github.com/payjoin/rust-payjoin) describing: unclear documentation, unhelpful error messages, missing examples, API friction
- Even better: fix the documentation yourself. Docs PRs are the fastest path to merged code in the Payjoin ecosystem
- If you wrote a clean integration example, submit it as a PR to the examples/ directory

---

#### Session 11: Payjoin in Production — Adoption Is the Privacy Multiplier

**The problem:** Payjoin only achieves its full privacy benefit with widespread adoption. Every wallet that supports Payjoin makes the CIOH weaker for all users. This session focuses on the integration work that OpenSats calls "deeper integration of existing techniques into widely used wallets."

**Learn:**
- BTCPay Server's Payjoin implementation — code walkthrough
- Bull Bitcoin's BIP77 integration — lessons from production
- UX considerations: how to make Payjoin invisible to users (it should "just work")
- The adoption curve: which wallets support Payjoin today, which are working on it, which should be next
- How to write a convincing "Payjoin support" feature request for a wallet that doesn't have it

**Build:**
- Set up BTCPay Server with Payjoin enabled. Make a Payjoin payment. Trace the code path from user action to on-chain result
- Compare on-chain footprints: Payjoin transaction vs regular payment. Document every observable difference (there should be none)

**Contribute this session:**
- Pick a Bitcoin wallet that doesn't support Payjoin. Research what it would take to add support. Write a detailed GitHub issue: "Payjoin (BIP77) Support — Feasibility Assessment" including which library to use (PDK), estimated effort, and the privacy benefit. **This is how adoption starts** — a well-researched issue that gives the wallet team a clear path
- Test BTCPay Server's Payjoin with different sender wallets. If something breaks or the UX is confusing, file a detailed issue on [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver)
- Review an open Payjoin-related PR on BTCPay Server or rust-payjoin

---

#### Session 12: Contributing to Payjoin — Ship Your Code

**Learn:**
- [rust-payjoin](https://github.com/payjoin/rust-payjoin) codebase deep dive: module architecture, testing strategy, CI pipeline
- How to get PRs merged: writing good commit messages, responding to review feedback, keeping PRs small and focused
- The Payjoin ecosystem roadmap: where help is needed most

**Build & Contribute — submit a PR:**
- Target repos: [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin), [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver), or any wallet where you're adding Payjoin support
- Bug fix, test case, documentation improvement, or feature — all count
- If your PR from Session 8 received review feedback, address it this session
- **Peer review:** every participant reviews at least one other participant's PR before next session

> **Phase 3 checkpoint:** Every participant has PRs in both the Silent Payments and Payjoin ecosystems. Most have 2-3 PRs open or merged. They can articulate how CIOH works and how Payjoin defeats it.

---

### Phase 4: Network & Protocol Privacy — Your Node Leaks Too
*Months 7-8 · Sessions 13-16*

Base-layer privacy isn't just about transactions. Your Bitcoin node's network connections, peer selection, transaction relay behavior, and light client queries all leak information. This phase covers P2P privacy, [ASmap](https://opensats.org/blog/bitcoin-grants-september-2024-7th-wave#asmap), compact block filters, light client privacy ([Floresta](https://github.com/vinteumorg/Floresta), [Kyoto](https://github.com/rustaceanrob/kyoto)), and Taproot's privacy benefits.

---

#### Session 13: P2P Network Privacy — Transaction Relay, ASmap & Eclipse Attacks

**The problem:** When your node broadcasts a transaction, the first node that sees it can associate your IP address with the transaction. Eclipse attacks isolate your node by filling all its peer slots with adversary-controlled nodes. And because Bitcoin nodes connect to peers without considering network topology, an adversary controlling a single ISP or AS (autonomous system) can see a disproportionate share of your traffic.

**Learn:**
- How transaction relay reveals your IP: first-spy attacks, timing analysis, relay topology inference
- Dandelion++ (stem-and-fluff): how it provides plausible deniability by routing transactions through a random stem path before broadcasting
- [ASmap](https://github.com/sipa/asmap): mapping IP addresses to autonomous systems so Bitcoin Core can diversify peer connections across network boundaries — preventing a single ISP/AS from eclipsing your node. **This is specifically funded by OpenSats and actively needs contributors**
- Tor and I2P integration in Bitcoin Core: configuration, tradeoffs, hybrid mode
- Eclipse attack mitigations: anchors, addrman bucketing, peer eviction logic
- [Naiyoma's P2P privacy and node-fingerprinting research](https://opensats.org/blog/five-grants-to-strengthen-bitcoin-development#naiyoma) — understanding how nodes themselves can be fingerprinted

**Build:**
- Configure Bitcoin Core in three modes: clearnet-only, Tor-only, and hybrid (clearnet + Tor). Analyze peer connections in each mode
- Map your node's current peers to autonomous systems. Calculate: how many distinct ASes? How many peers share an AS? What's the theoretical eclipse attack surface?
- Simulate adversary IP linking probability for each configuration: clearnet = high, hybrid = medium, Tor-only = low but with tradeoffs

**Contribute this session:**
- Bitcoin Core's Tor and I2P documentation (`doc/tor.md`, `doc/i2p.md`) can always be improved. Read both. If anything is outdated or unclear, submit a PR
- [ASmap](https://github.com/sipa/asmap) is an active project. Review the codebase, build the tools, and look for contribution opportunities — better AS data sources, testing improvements, or documentation
- Search Bitcoin Core issues for labels related to P2P or privacy. Find one you understand well enough to comment on with a test result or analysis

---

#### Session 14: Compact Block Filters (BIP157/158) — Privacy-Preserving Light Clients

**The problem:** [BIP37 Bloom filters were a privacy disaster](https://eprint.iacr.org/2014/763.pdf) — they leaked which addresses the client was interested in to whatever server it connected to. BIP157/158 compact block filters fix this by having the server provide a filter for each block, letting the client check locally whether the block might contain relevant transactions. The client never reveals its addresses.

**Learn:**
- Why BIP37 was broken: false positive rates, filter update attacks, server-side inference
- Golomb-Rice Coded Sets (GCS): the compression scheme behind compact block filters
- BIP157 client-server protocol: how clients request filters, verify them, and decide which full blocks to download
- False positive rates and parameter tuning: M and P values, bandwidth tradeoffs
- How [Kyoto](https://github.com/rustaceanrob/kyoto) implements BIP157/158 in Rust — and why it's critical infrastructure for Silent Payments light clients
- How [Floresta](https://github.com/vinteumorg/Floresta) uses utreexo for a different approach to light client privacy

**Build:**
- Implement Golomb-Rice encoding and decoding from scratch in Python
- Build a GCS filter from a set of scripts. Query it for matches. Calculate the actual false positive rate vs the theoretical rate
- Compare: for a given wallet with 100 addresses, how many false-positive blocks would BIP157/158 cause the client to download? What's the bandwidth overhead vs downloading all blocks?

**Contribute this session:**
- [Kyoto](https://github.com/rustaceanrob/kyoto) is early-stage and needs contributors. Clone, build, and run it. Browse issues. Even filing well-described bugs is valuable
- Compare your Golomb-Rice implementation against Kyoto's. If you find an optimization or cleaner approach, open a PR
- [Floresta](https://github.com/vinteumorg/Floresta) has issues related to block filter handling. Browse and comment with your analysis
- Test both Kyoto and Floresta on signet. Document setup instructions if they're missing or incomplete — submit as a docs PR

---

#### Session 15: Light Client Privacy — Floresta, Kyoto & the Privacy Spectrum

**Learn:**
- The light client privacy spectrum: SPV (worst) → Electrum (bad) → BIP157/158 (good) → full node (best)
- [Floresta](https://github.com/vinteumorg/Floresta): utreexo-based validation, privacy properties, what it can and can't verify
- [Kyoto](https://github.com/rustaceanrob/kyoto): BIP157/158 implementation, architecture, integration with wallet libraries
- How Silent Payments scanning works differently in each light client model
- Bandwidth, storage, and privacy comparison across 5 approaches: SPV, Electrum, Neutrino/Kyoto (CBF), Floresta (utreexo), full node

**Build:**
- Set up Floresta on signet. Connect a wallet. Monitor what information flows between client and network
- Build a structured privacy comparison matrix for all 5 light client approaches: what the server learns, what the network learns, bandwidth cost, storage cost, verification strength

**Contribute this session:**
- [Floresta is actively looking for contributors](https://github.com/vinteumorg/Floresta/issues). Check issues labeled "good first issue". Pick one and start working on it
- Your privacy comparison matrix is publishable content. Clean it up and submit it as a PR to Floresta or Kyoto docs, or as a post to [Bitcoin Optech](https://bitcoinops.org/)
- Test both Floresta and Kyoto against edge cases. File issues with detailed reproduction steps for anything unexpected

---

#### Session 16: Taproot Privacy — Making Complex Transactions Invisible

**Learn:**
- How Taproot makes multisig indistinguishable from single-sig on-chain (key path spending)
- MAST (Merklized Alternative Script Trees): complex spending conditions that only reveal the branch actually used
- MuSig2 for multi-party Taproot key aggregation — privacy-preserving multisig
- FROST: threshold signatures that look like single-sig on-chain
- CISA (Cross-Input Signature Aggregation): a future proposal that would make CoinJoin transactions cheaper, incentivizing privacy
- Why Taproot adoption matters for systemic privacy — and why it's still too low

**Build:**
- Create three Taproot transactions on signet: single-sig (key path), 2-of-2 MuSig (key path), and script path with 2 branches
- Compare on-chain footprints: the first two should be indistinguishable. The third reveals the script path
- Analyze current Taproot adoption metrics. Calculate: what percentage of transactions use P2TR? How does this compare to 6 months ago?
- Estimate CISA fee savings for a 5-input CoinJoin: how much cheaper would it be with signature aggregation?

**Contribute this session:**
- Research which wallets default to Taproot addresses and which don't. File issues on wallets that don't default to P2TR, explaining the privacy benefit of Taproot adoption
- Review a Taproot-related PR on Bitcoin Core, rust-bitcoin, or BDK — focus on privacy implications
- If you built the CISA fee analysis, publish it and share with the research community

> **Phase 4 checkpoint:** Participants have contributed to 3-4 different repos. Many have merged PRs. Everyone has reviewed multiple PRs. They understand P2P privacy, ASmap, compact block filters, light client tradeoffs, and Taproot's privacy benefits.

---

### Phase 5: Advanced Privacy Techniques — CoinJoin, CoinSwap, eCash & Lightning
*Months 9-10 · Sessions 17-20*

This phase covers the advanced privacy techniques that complement base-layer improvements: CoinJoin ([JoinMarket NG](https://opensats.org/blog/seventeenth-wave-of-bitcoin-grants#joinmarket-ng)), [Coinswap](https://opensats.org/blog/developing-advancements-in-onchain-privacy#coinswap), eCash ([Fedimint](https://github.com/fedimint/fedimint), [Cashu](https://github.com/cashubtc/nutshell)), and Lightning privacy (BOLT12). While OpenSats' Spring 2026 focus is Layer 1, these techniques interact with base-layer privacy in critical ways — and several are actively funded.

---

#### Session 17: CoinJoin & JoinMarket NG — Equal-Output Mixing

**Learn:**
- CoinJoin mechanics: how multiple users combine inputs into a single transaction with equal-value outputs
- Toxic change: why CoinJoin doesn't work if change outputs can be linked back to inputs
- WabiSabi protocol: the credential system used by Wasabi Wallet for flexible CoinJoin
- [JoinMarket NG](https://opensats.org/blog/seventeenth-wave-of-bitcoin-grants#joinmarket-ng): the next generation of the orderbook-based CoinJoin protocol — how it works, how it differs from centralized coordinators, and why OpenSats funds it
- CoinJoin weaknesses: Sybil attacks on coordinators, timing analysis, amount analysis of non-equal outputs
- CISA's potential impact on CoinJoin economics: if signature aggregation reduces CoinJoin fees, adoption increases

**Build:**
- Analyze 20 real mainnet transactions. Identify which are CoinJoins. For those that are: calculate the anonymity set, identify toxic change, and assess the actual privacy gain
- Simulate a 5-user CoinJoin construction: each user provides 2 inputs, all create equal-value outputs plus change. Analyze what a chain analyst can determine
- Compare CoinJoin vs Payjoin: privacy properties, on-chain footprint, detectability, cost

**Contribute this session:**
- Your CoinJoin analyzer is a useful tool. Publish it under CC0 as a standalone repo
- Research [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) (CoinSwap, next session). Clone, build, read the README. File issues for anything unclear
- Write a structured comparison of CoinJoin implementations: JoinMarket NG, Wasabi WabiSabi, legacy Whirlpool. Focus on privacy properties and trust assumptions

---

#### Session 18: CoinSwap & Teleport — Breaking the Transaction Graph Entirely

**The problem:** CoinJoin creates a single transaction with mixed outputs — but the on-chain footprint is still visible as a CoinJoin. [CoinSwap](https://opensats.org/blog/developing-advancements-in-onchain-privacy#coinswap) takes a radically different approach: two users make separate, normal-looking transactions that swap their coins. The on-chain result is two ordinary-looking payments — but the coins have swapped owners. There is no on-chain evidence that a swap occurred.

**Learn:**
- How CoinSwap breaks the transaction graph: the routing looks like two unrelated payments
- Hash time-locked contracts (HTLCs): the atomic mechanism that makes trustless swaps possible
- Multi-hop CoinSwap: adding intermediate hops for plausible deniability
- [Teleport Transactions](https://github.com/nickhntv/teleport-transactions): the active CoinSwap implementation — **OpenSats specifically wants to see work here**
- CoinSwap vs CoinJoin: privacy comparison. CoinSwap is invisible on-chain; CoinJoin is detectable but provides ambiguity
- CISA implications for CoinSwap economics

**Build:**
- Walk through a 2-party CoinSwap on paper. Diagram every on-chain transaction. Analyze what an observer sees vs what actually happened
- Walk through a 3-hop CoinSwap. How does each hop add plausible deniability?
- Calculate costs: CoinJoin (single transaction, many users) vs CoinSwap (multiple transactions, 2 users) — with and without CISA

**Contribute this session:**
- [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) is actively maintained and needs contributors. Browse issues. This is a **high-impact** project — early-stage, specifically mentioned by OpenSats
- File issues on Teleport for any bugs, documentation gaps, or UX problems you encountered while testing
- Start working on a Teleport issue. Even a documentation PR is very valuable — every contributor matters at this stage

---

#### Session 19: eCash Privacy — Fedimint & Cashu

**Learn:**
- Chaumian blind signatures: how the mint signs tokens without knowing which tokens it signed — providing perfect privacy from the mint operator
- [Cashu](https://github.com/cashubtc/nutshell) protocol: mint-receive-send-melt lifecycle, proof structure, how eCash achieves instant settlement with privacy
- [Fedimint](https://github.com/fedimint/fedimint) architecture: federated custody, threshold Chaumian minting, Lightning gateway integration
- How eCash complements on-chain privacy: eCash for small payments, on-chain for settlement
- Trust assumptions: eCash requires trusting the mint/federation. How does this compare to on-chain privacy tools?
- OpenSats has funded extensive eCash work — this is production infrastructure, not research

**Build:**
- Set up a Cashu mint on signet. Mint tokens, send them to another participant, redeem them. Walk through the blind signature math at each step
- Analyze what the mint learns at each stage: minting, sending, receiving, melting. Where does privacy hold? Where does it break?

**Contribute this session:**
- [cashubtc/nutshell](https://github.com/cashubtc/nutshell) is Python — accessible to everyone. Browse issues. The Cashu ecosystem is growing fast
- [fedimint/fedimint](https://github.com/fedimint/fedimint) has issues labeled "good first issue". The community is very welcoming
- If you set up a Cashu mint successfully, write a step-by-step setup guide and submit it as a PR to the nutshell docs. Real-world guides from actual users are incredibly valuable

---

#### Session 20: Lightning Privacy — BOLT12, Blinded Paths & Channel Privacy

**Learn:**
- Lightning's privacy model: onion-routed payments (good), but channel balances and graph structure leak information (bad)
- Channel balance probing: how an adversary can discover your channel balance by sending failing payments
- Blinded paths (BOLT12): how receiver privacy works — the last hops of the route are encrypted, so the sender doesn't know who they're paying
- BOLT12 offers: reusable payment requests that don't reveal the receiver's node identity
- Private vs public channels: tradeoffs for routing and privacy
- Trampoline routing: privacy through delegation

**Build:**
- Set up two LN nodes on signet. Open a channel. Probe your own channel balance using binary search
- Compare BOLT11 invoices vs BOLT12 offers: what information does each reveal to the sender?
- Design a maximum-privacy Lightning configuration: Tor, private channels, blinded paths, channel size selection

**Contribute this session:**
- [lightningdevkit/rust-lightning (LDK)](https://github.com/lightningdevkit/rust-lightning) has issues labeled "good first issue". LDK powers many Lightning wallets — contributions have enormous reach
- Your Lightning privacy analysis is publishable. Clean it up and share
- If you found privacy issues in a Lightning wallet during testing, file them with detailed reproduction steps

> **Phase 5 checkpoint:** Participants are contributing across 5+ different repos. Most have 3-5 PRs submitted. Several have merged PRs. They understand CoinJoin, CoinSwap, eCash, and Lightning privacy — and how each complements base-layer improvements.

---

### Phase 6: Building & Shipping — Substantial Work That Gets Merged
*Months 11-12 · Sessions 21-24*

Everything learned, applied. Every graduate ships real code.

---

#### Session 21: Privacy-Preserving Wallet Development with BDK

**The problem:** [BDK (Bitcoin Dev Kit)](https://opensats.org/projects/bdk) is the foundation for many Bitcoin wallets. Privacy improvements in BDK cascade to every wallet built on it. This session focuses on building privacy-by-default wallets using BDK — the kind of "deeper integration" work that OpenSats and the broader funding ecosystem want to see.

**Learn:**
- BDK architecture: descriptor wallets, coin selection API, PSBT building, chain data sources
- Privacy-by-default wallet design: what a wallet should do automatically without user intervention
- Privacy-optimized coin selection in BDK: configuring for privacy vs configuring for fees
- How to add Silent Payments or Payjoin support to a BDK wallet
- Privacy testing: how to systematically evaluate a wallet's privacy properties

**Build:**
- Scaffold a BDK wallet with: privacy-optimized coin selection, change output safety (same script type), address reuse detection (warn if an address is reused), anti-fee-sniping locktime
- Add basic Payjoin send support using PDK
- Run your wallet through your privacy scorer from Session 22 (preview)

**Contribute this session:**
- Submit a PR to [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk). Your wallet exercise surfaced gaps: missing privacy configuration options, documentation that could be clearer, coin selection edge cases
- File issues for privacy-related improvements: "add a privacy score to coin selection results", "warn when change output script type doesn't match inputs", "document privacy-optimal configuration"

---

#### Session 22: Privacy Testing, Scoring & Mempool Analysis

**Learn:**
- Systematic transaction privacy evaluation: what to check and how to score it
- Mempool analysis: how transaction timing, fee rates, and propagation patterns reveal information
- Building automated privacy testing for wallet software
- How wallet developers can use privacy scoring in CI to catch regressions

**Build:**
- Build a comprehensive transaction privacy scorer in Python. Check for:
  - Address reuse (critical)
  - Script type mixing between inputs and outputs (high)
  - Round payment amounts (medium)
  - Detectable change output (high)
  - Fee rate fingerprint (medium)
  - Locktime pattern (low-medium)
  - Sequence number pattern (low-medium)
  - UTXO consolidation without payment (medium)
  - Output ordering predictability (medium)
- Score 20 real mainnet transactions. Identify the worst offenders and why

**Contribute this session:**
- Your privacy scoring tool is a real contribution. Publish it under CC0 as a standalone repo. If it's good enough, submit it to [Bitcoin Dev Project](https://bitcoindevs.xyz/) as a community tool
- Run your scorer against transactions from popular wallets. If you find consistent privacy leaks, file issues on those wallets with your data
- Contribute your scoring methodology to [Bitcoin Optech](https://bitcoinops.org/) or the [Bitcoin Wiki](https://en.bitcoin.it/wiki/Privacy) as a reference for wallet developers

---

#### Session 23: Contribution Sprint — The Big Push

**This is a 3-hour working session. Code ships today.**

| Time | Activity |
|---|---|
| 00:00 - 00:30 | **Issue selection:** each participant picks a target from the curated list |
| 00:30 - 02:00 | **Code:** write your fix, test it, prepare the PR |
| 02:00 - 02:30 | **Peer review:** every participant reviews one other PR |
| 02:30 - 03:00 | **Submit:** push, open the PR, celebrate |

**Curated issue list (updated monthly by facilitator):**

| Repo | Language | What to Look For |
|---|---|---|
| [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) | C++ | Silent Payments, compact block filters, P2P privacy, ASmap, coin selection |
| [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) | Rust | Test coverage, edge cases, documentation |
| [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) | Rust | Good first issues, integration examples, docs |
| [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta) | Rust | Good first issues, testing, documentation |
| [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) | Rust | Early-stage — lots of opportunities |
| [nickhntv/teleport-transactions](https://github.com/nickhntv/teleport-transactions) | Rust | CoinSwap implementation, testing, docs |
| [fedimint/fedimint](https://github.com/fedimint/fedimint) | Rust | Good first issues, module development |
| [cashubtc/nutshell](https://github.com/cashubtc/nutshell) | Python | Testing, documentation, mint features |
| [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk) | Rust | Coin selection, privacy features |
| [lightningdevkit/rust-lightning](https://github.com/lightningdevkit/rust-lightning) | Rust | Good first issues, privacy features |
| [rust-bitcoin/rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) | Rust | Transaction construction, encoding |
| [sipa/asmap](https://github.com/sipa/asmap) | Python/C++ | AS mapping, peer diversity tooling |

---

#### Session 24: Capstone — Present Your Contributions

Each participant presents (10 minutes):

1. **What you contributed (4 min)** — Walk through your PRs. Show the code. Link to each one
2. **What impact it has (2 min)** — Who benefits? How does this make Bitcoin more private?
3. **What you learned (2 min)** — What was harder than expected? What changed how you think about privacy?
4. **What's next (2 min)** — If you had 6 more months of funded time, what would you build?

Open to the full Code Orange community — Bitcoin Dojo, rawBit, Decoding Bitcoin cohorts all attend.

**Graduation requirements:**
- Attended 18+ of 24 sessions (75%)
- Submitted 3+ PRs to Bitcoin privacy projects
- Presented at capstone

Graduates meeting these requirements are eligible for the **Code Orange Developer Fellowship** ($500/month, 6 months) to continue contributing to Bitcoin privacy open-source full-time.

---

## Expected Output

### Per participant (12 months):

| Metric | Target |
|---|---|
| PRs submitted | 5-8 |
| PRs merged | 3-5 |
| Distinct repos contributed to | 3+ |
| Code reviews posted | 10+ |
| Issues filed | 5+ |

### Per cohort (15 participants, 12 months):

| Metric | Target |
|---|---|
| PRs submitted | 75-120 |
| PRs merged | 45-75 |
| New privacy developers produced | 15 |
| Repos contributed to | 12+ |

---

## Session Format

Every session follows the same structure. The last 30 minutes are always about contributing.

| Time | Activity |
|---|---|
| 00:00 - 00:15 | **Review:** Show contributions since last session. What got merged? What feedback? What's blocking? |
| 00:15 - 00:45 | **Concept:** Theory and protocol walkthrough |
| 00:45 - 01:45 | **Build:** Hands-on coding exercise |
| 01:45 - 02:15 | **Contribute:** Open laptops. Find issues. File PRs. Review code. Facilitator matches participants to issues in real time. |
| 02:15 - 02:30 | **Plan:** Assigned reading + specific contribution goal for next 2 weeks |

The "Review" at the start creates accountability. When you know you'll be asked "what did you contribute since last time?" — you contribute.

---

## Contribution Tracker

Every participant maintains a public contribution log. This is what grant reviewers see.

| Session | Minimum Contribution | Target Repos |
|---|---|---|
| 01 | Star 7 repos. Clone bitcoin/bitcoin. Read coinselection.cpp | bitcoin/bitcoin, BDK, rust-silentpayments, rust-payjoin, Floresta, Kyoto, rust-bitcoin |
| 02 | Test a wallet's fingerprint. Draft issue for Session 4 | Any Bitcoin wallet repo, Bitcoin Optech |
| 03 | Comment on a BDK coin selection issue with analysis | bitcoindevkit/bdk, bitcoin/bitcoin |
| 04 | File your first issue or docs PR (wallet fingerprint or wiki) | Any wallet repo, Bitcoin Wiki, rust-bitcoin |
| 05 | Read BIP352. Comment on a rust-silentpayments issue | bitcoin/bips, rust-silentpayments |
| 06 | Add a test case or file issue on SP test vectors | bitcoin/bips, rust-silentpayments |
| 07 | Review a PR on bitcoin/bitcoin or Kyoto (CBF-related) | bitcoin/bitcoin, kyoto |
| 08 | **Submit your first PR** to an SP or CBF project | rust-silentpayments, kyoto, bitcoin/bitcoin |
| 09 | Clone rust-payjoin. Comment on an open issue | payjoin/rust-payjoin |
| 10 | File issues on PDK documentation or API rough edges | payjoin/rust-payjoin |
| 11 | File Payjoin feasibility issue on a wallet that lacks support | Any wallet repo, BTCPay |
| 12 | **Submit a PR** to Payjoin ecosystem | rust-payjoin, BTCPay |
| 13 | Improve Bitcoin Core P2P documentation or test ASmap | bitcoin/bitcoin, sipa/asmap |
| 14 | Test and file issues on Kyoto or Floresta | kyoto, Floresta |
| 15 | **Submit a PR** to Floresta or Kyoto | Floresta, kyoto |
| 16 | File Taproot adoption issues on wallets not defaulting to P2TR | Any wallet repo |
| 17 | Publish CoinJoin analysis tool. Research Teleport issues | teleport-transactions |
| 18 | **Submit a PR** to Teleport Transactions | teleport-transactions |
| 19 | Submit docs or test PR to Cashu or Fedimint | nutshell, fedimint |
| 20 | Submit a PR to LDK (privacy-related) | rust-lightning |
| 21 | **Submit a PR** to BDK (privacy feature or coin selection) | bdk |
| 22 | Publish privacy scoring tool. File issues on wallets tested | Any wallet repo |
| 23 | **Contribution sprint: submit a PR** | Any privacy-related repo |
| 24 | Present all contributions. Apply for fellowship if eligible | — |

---

## Exercises & Code

```
phase-1-foundations/
  session-01/  chain_analysis_lab.py      — Trace transactions, apply heuristics, privacy scoring
  session-02/  tx_anatomy_lab.py          — Decode raw transactions, identify wallet fingerprints
  session-03/  coin_selection_simulator.py — 4 algorithms, privacy scoring, BnB optimization
  session-04/  wallet_fingerprint_lab.py   — Identify wallets from raw transactions, build fingerprint-clean tx

phase-2-silent-payments/
  session-05/  sp_ecdh_derivation.py      — ECDH shared secret math from scratch
  session-06/  silent_payments_sender.py   — Full SP sender with test vector validation
  session-07/  sp_scanner_cbf.py          — SP scanner with compact block filter optimization

phase-3-payjoin/
  session-09/  payjoin_analysis.py        — Identify Payjoins from raw transactions
  session-10/  pdk_integration/           — Rust project using Payjoin Dev Kit
  session-11/  btcpay_payjoin_lab.md      — BTCPay Server Payjoin walkthrough

phase-4-network-privacy/
  session-13/  p2p_privacy_lab.py         — Peer analysis, AS mapping, relay timing
  session-14/  compact_block_filters.py   — Golomb-Rice coding from scratch, GCS construction
  session-16/  taproot_privacy_lab.py     — Key path vs script path analysis, CISA estimation

phase-5-advanced/
  session-17/  coinjoin_analysis.py       — CoinJoin detection, anonymity set calculation
  session-18/  coinswap_walkthrough.md    — CoinSwap flow analysis
  session-19/  cashu_mint_exercise.md     — Set up a Cashu mint on signet

phase-6-contributing/
  session-21/  bdk_privacy_wallet/        — Privacy-by-default BDK wallet scaffold
  session-22/  privacy_scorer.py          — Comprehensive transaction privacy scoring tool
```

---

## Resources

- **[Reading List](reading-list.md)** — 70+ resources organized by phase
- **[Glossary](glossary.md)** — 60+ terms covering all 6 phases
- **[Facilitator Guide](facilitator-guide.md)** — Session-by-session facilitation notes
- **[Capstone Projects](capstone-projects.md)** — 4 project tracks with rubrics
- **[Contributing](CONTRIBUTING.md)** — How to contribute to this curriculum

---

## For Grant Reviewers

**This is not a lecture series. This is a contribution pipeline specifically aligned with the base-layer privacy work that OpenSats, HRF, and Brink fund.**

The curriculum directly addresses every Layer 1 privacy area identified in [OpenSats' Spring 2026 Call for Applications](https://opensats.org/blog/call-for-applications-spring-2026):

| OpenSats Priority | Where We Address It | What Participants Build |
|---|---|---|
| Silent Payments (BIP352) | Phase 2 (Sessions 5-8) | SP sender/scanner from scratch, PRs to rust-silentpayments |
| Payjoin / collaborative transactions | Phase 3 (Sessions 9-12) | Full Payjoin flow with PDK, wallet integration assessments |
| Wallet behavior and transaction construction | Phases 1 + 6 (Sessions 2-4, 21-22) | Wallet fingerprint research, privacy-by-default BDK wallets, privacy scoring tools |
| Compact block filters (BIP157/158) | Sessions 7, 14 | CBF implementation, contributions to Kyoto |
| Floresta & light client privacy | Sessions 14-15 | Testing, issues, PRs to Floresta and Kyoto |
| ASmap & P2P privacy | Session 13 | AS mapping analysis, Bitcoin Core P2P docs, ASmap contributions |
| Coinswap | Session 18 | CoinSwap flow analysis, PRs to Teleport Transactions |
| JoinMarket NG / CoinJoin | Session 17 | CoinJoin analysis tooling, anonymity set calculation |
| rust-bitcoin and BDK (foundational libraries) | Throughout, especially Sessions 3-4, 21 | Coin selection improvements, transaction construction, privacy features |
| Deeper integration into widely used wallets | Sessions 4, 11, 16, 21 | Wallet fingerprint issues, Payjoin feasibility assessments, Taproot adoption issues |

From session 1, participants are reading real Bitcoin source code and engaging with real repos. By session 4, they've filed their first issue. By session 8, they've submitted their first PR. By session 24, they have 5-8 PRs across 3+ repos.

**Expected output for one cohort (15 participants, 12 months): 75-120 PRs submitted to Bitcoin privacy repos, 45-75 merged.**

Our track record proves this works. Code Orange has already produced **45+ merged PRs** across Bitcoin Core, rust-bitcoin, BDK, rust-payjoin, peer-observer, LDK, hex-conservative, kernel-node, and more. Our graduates — [Chaitika](https://github.com/chaitika) (Silent Payments), [Arowolo](https://github.com/Arowolokehinde) (Payjoin), [Peter](https://github.com/pzafonte) (Bitcoin Core), [Razor](https://github.com/RazorBest) (peer-observer), [Vaan](https://github.com/va-an) (BDK/rust-bitcoin) — are already contributing to the exact projects this curriculum targets.

**That's what your grant buys: more developers building the base-layer privacy tools that Bitcoin needs.**

---

*Code Orange Dev School · Bitcoin House Bali, Indonesia · [codeorange.dev](https://codeorange.dev) · CC0 1.0 Universal*
