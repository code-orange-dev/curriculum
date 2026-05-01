# Bitcoin Privacy Developer Track

> 24 bi-weekly sessions. 12 months. Every session ends with a contribution to Bitcoin open source.

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## What This Is

A contribution-first developer curriculum. We don't wait until the end to start contributing — participants engage with real Bitcoin privacy repos from session 1. Every session teaches a concept, builds something hands-on, and then points you at a specific open-source action: read this codebase, file this issue, review this PR, submit this fix.

By session 8, you've submitted your first PR. By session 24, you're a Bitcoin privacy developer with a track record that speaks for itself.

**Format:** Bi-weekly workshops (every 2 weeks), 2-2.5 hours each
**Duration:** 12 months (24 sessions)
**Prerequisites:** Basic Bitcoin knowledge (completed Bitcoin Dojo or equivalent). Comfortable reading code. Python or Rust experience helpful.
**Outcome:** Every participant contributes to Bitcoin open source from week 1. Every graduate has multiple PRs across privacy-related projects.

---

## The Contribution Ladder

We don't throw you into the deep end. Contributions scale with your knowledge:

```
Sessions 1-4:    Read code → Star repos → File issues → Improve docs
Sessions 5-8:    Review PRs → Add test cases → Submit your first PR
Sessions 9-12:   Fix bugs → Add features → Submit PRs to multiple repos
Sessions 13-16:  Tackle harder issues → Review others' PRs → Mentor newcomers
Sessions 17-20:  Identify gaps → Propose improvements → Lead contributions
Sessions 21-24:  Ship substantial work → Present to the community → Join the fellowship
```

---

## Curriculum Overview

```
Phase 1: Foundations                 (Sessions 1-4,   Months 1-2)
Phase 2: Silent Payments             (Sessions 5-8,   Months 3-4)
Phase 3: Payjoin                     (Sessions 9-12,  Months 5-6)
Phase 4: Network & Protocol Privacy  (Sessions 13-16, Months 7-8)
Phase 5: Advanced Techniques         (Sessions 17-20, Months 9-10)
Phase 6: Building & Contributing     (Sessions 21-24, Months 11-12)
```

---

## Phase 1: Foundations — Why Privacy Matters & How It Breaks

*Months 1-2 · Sessions 1-4 · Learn how surveillance works. Start engaging with real repos immediately.*

### Session 01: Why Privacy Matters — Chain Analysis & Surveillance

**Learn:** The 5 primary heuristics chain analysis firms use: common-input-ownership, change detection, address reuse, timing analysis, amount correlation. Why privacy is a protocol-level requirement, not a user preference.

**Build:** Trace a transaction chain on mempool.space and OXT.me. Apply CIOH to identify entity clusters. Write a 1-page analysis of what a chain analyst can learn from a 5-hop transaction chain.

**Contribute this week:**
- Create a GitHub account if you don't have one
- Star and fork these repos: [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin), [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments), [rust-payjoin](https://github.com/payjoin/rust-payjoin), [Floresta](https://github.com/vinteumorg/Floresta), [BDK](https://github.com/bitcoindevkit/bdk)
- Read the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy) and identify one section that's outdated or unclear — note it down, you'll file an issue or edit later
- Clone bitcoin/bitcoin and build it locally. Read `src/wallet/coinselection.cpp`. You won't understand all of it yet — that's fine. The goal is to start reading real Bitcoin code from day one.

---

### Session 02: Transaction Anatomy for Privacy

**Learn:** Raw transaction structure byte-by-byte. How nVersion, nLockTime, and nSequence differ across wallets. Fee estimation patterns as fingerprints. Script types and their privacy implications.

**Build:** Decode 5 raw testnet transactions. For each, identify version, locktime, sequence, script types, and fee rate. Determine which wallet software created each one.

**Contribute this week:**
- Read [0xB10C's wallet fingerprinting research](https://b10c.me/blog/). Pick one wallet (Sparrow, BlueWallet, Electrum, etc.) and test whether its current version still has the fingerprints described. If the behavior has changed, this is an issue worth filing on the Bitcoin Wiki or the wallet's repo.
- Browse the [Bitcoin Optech Topics page](https://bitcoinops.org/en/topics/). Find the "Transaction compatibility" section. Is anything missing or outdated? If so, open an issue on [bitcoinops/bitcoinops.github.io](https://github.com/bitcoinops/bitcoinops.github.io).

---

### Session 03: UTXO Management & Coin Selection

**Learn:** 4 coin selection algorithms (largest-first, branch-and-bound, privacy-optimized, random). How each affects privacy. Dust attacks. Coin control.

**Build:** Implement all 4 algorithms in Python. Run them against the same UTXO set. Score each for privacy leakage: input count, change amount, whether change reveals the payment.

**Contribute this week:**
- Read Bitcoin Core's coin selection code: `src/wallet/coinselection.cpp` and `src/wallet/spend.cpp`. Find a comment that could be clearer or a variable name that's confusing. Even a 1-line documentation improvement counts.
- Browse [BDK issues labeled "coin-selection"](https://github.com/bitcoindevkit/bdk/labels). Read through open issues. If you can reproduce one, comment with your findings. If you have an idea for a fix, say so.
- Look at Murch's [coin selection research](https://murch.one/erhardt2016coinselection.pdf). Are the algorithms described there fully implemented in Bitcoin Core today? If something's missing, that's a potential contribution.

---

### Session 04: Wallet Fingerprinting & Transaction Construction

**Learn:** Known wallet fingerprints (Bitcoin Core, Electrum, BlueWallet, Wasabi, Sparrow). How to construct a "privacy-clean" transaction. Transaction batching and its privacy implications.

**Build:** Given 10 raw transactions, identify which wallet created each by analyzing version, locktime, sequence, output ordering, script types, and fee patterns. Then construct a raw transaction that avoids all known fingerprints.

**Contribute this week — your first real contribution:**
- File an issue on a Bitcoin wallet repo documenting a privacy fingerprint you discovered. Include: the wallet version, the specific fingerprint (e.g., "always uses nLockTime 0" or "outputs are always in BIP69 order"), and why it matters for privacy. Target repos: [AceBit/BlueWallet](https://github.com/AceBit/BlueWallet), [nickhntv/sparrow](https://github.com/nickhntv/sparrow), [nickhntv/GreenBits](https://github.com/nickhntv/GreenBits), or any wallet you tested.
- OR: Submit a documentation PR to the [Bitcoin Wiki Privacy page](https://en.bitcoin.it/wiki/Privacy) adding the fingerprint data you collected.
- OR: Write up your wallet fingerprinting analysis as a blog post or GitHub gist and share it in the Code Orange Discord for community review.

**Phase 1 running total: Every participant has starred 5+ repos, read real Bitcoin source code, and filed at least 1 issue or docs PR.**

---

## Phase 2: Silent Payments (BIP352) — Reusable Addresses Without Address Reuse

*Months 3-4 · Sessions 5-8 · Build the cryptography. Start reviewing and submitting PRs.*

### Session 05: BIP352 Deep Dive — How Silent Payments Work

**Learn:** The address reuse problem. ECDH shared secret derivation on secp256k1. Scan keys vs spend keys. Labeling. Why scanning is computationally expensive.

**Build:** Derive Silent Payment shared secrets by hand using pure Python secp256k1 math. Given a sender's private key and an SP address, compute the output key step by step.

**Contribute this week:**
- Read the [BIP352 specification](https://github.com/bitcoin/bips/blob/master/bip-0352.mediawiki) end to end. If anything is ambiguous or could be explained better, file an issue on [bitcoin/bips](https://github.com/bitcoin/bips) with a specific suggestion.
- Clone [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments). Build it. Run the test suite. Read the code for `sending.rs` — you just implemented this math by hand, so you'll recognize the flow. Note any discrepancies between the code and the spec.
- Browse [rust-silentpayments open issues](https://github.com/cygnet3/rust-silentpayments/issues). Comment on one with your understanding of the problem, even if you don't have a fix yet. Showing up and engaging is how you build a relationship with maintainers.

---

### Session 06: Implement a Silent Payments Sender in Python

**Learn:** Complete SP send flow: input selection, shared secret, tweak, output construction. Handling multiple inputs. Testing against BIP352 test vectors.

**Build:** Implement the full SP sending pipeline: parse address, aggregate input keys, compute shared secret, derive output key, create transaction. Verify against BIP352 test vectors.

**Contribute this week:**
- The BIP352 test vectors are at [bitcoin/bips/tree/master/bip-0352](https://github.com/bitcoin/bips/tree/master/bip-0352). Check if any edge cases are missing (e.g., single Taproot input, mixed input types, multiple SP recipients). If you find a gap, file an issue proposing the additional test vector.
- Add a test case to rust-silentpayments that exercises the edge case you identified. Even if you're not confident in Rust yet, writing the test (which is mostly data setup and assertion) is a great way to start.
- If you're more comfortable in Python: contribute your sender implementation as a reference tool. Clean it up, add docstrings, and publish it as a GitHub repo. Tag it with `silent-payments` and `bitcoin`.

---

### Session 07: Scanning, Receiving & Compact Block Filters

**Learn:** The scanning problem. Compact block filters (BIP157/158) as optimization. Tweak caching. Bandwidth vs privacy tradeoffs for SP light clients.

**Build:** Build a minimal SP scanner. Build a compact block filter. Measure how many blocks you can skip using CBF. Calculate false positive rates.

**Contribute this week:**
- Review an open PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) related to Silent Payments or compact block filters. You don't need to approve it — just leave a thoughtful review comment. "I tested this locally and it works" or "This section is unclear to me because..." are both valuable. Search for open PRs with labels like `silent-payments` or `block-filter`.
- Look at [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) — a compact block filter light client in Rust. It's an early-stage project with lots of room for contribution. Browse their issues, build the project, and identify something you can help with.
- If you found bugs or unexpected behavior while building your scanner, file them as issues on the relevant repo with reproduction steps.

---

### Session 08: Contributing to Silent Payments — Your First PR

**Learn:** Bitcoin Core PR #28122 code walkthrough. rust-silentpayments architecture. Wallet integration status. Where the gaps are.

**Build:** Clone your target repo. Build locally. Run tests. Pick a Good First Issue. Write and submit your first PR.

**Contribute this week — submit a PR:**
- **Option A (Rust):** Add a test case, fix a doc typo, or implement a small feature in [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) or [Kyoto](https://github.com/rustaceanrob/kyoto).
- **Option B (C++):** Review and test a Silent Payments PR on [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin/pull/28122). Leave a detailed review with test results.
- **Option C (Any language):** Improve documentation for Silent Payments anywhere: BIP352 wiki, Bitcoin Optech, wallet integration guides.
- **Option D:** Start integrating Silent Payments support into a wallet that doesn't have it yet. Even a proof-of-concept on a branch counts.

The facilitator will pair each participant with a specific issue matching their skill level. Nobody leaves this session without a PR submitted or a substantive review posted.

**Phase 2 running total: Every participant has submitted at least 1 PR or detailed code review to a Silent Payments project.**

---

## Phase 3: Payjoin (BIP77/78) — Breaking the Common-Input-Ownership Heuristic

*Months 5-6 · Sessions 9-12 · Build Payjoin in Rust. Contribute to the ecosystem that needs it most.*

### Session 09: BIP77/78 Theory — How Payjoin Defeats Chain Analysis

**Learn:** CIOH and why it's chain analysis's most powerful tool. Payjoin V1 (BIP78) vs V2 (BIP77). The 5 critical sender verification checks. Output substitution attacks.

**Build:** Analyze 10 testnet transactions — determine which are Payjoins. Walk through the full V2 flow. Implement sender verification checks in pseudocode.

**Contribute this week:**
- Clone [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin). Build it. Run the test suite. Read through `src/send.rs` and `src/receive.rs`. You just learned this flow — now see how it's implemented.
- Browse [rust-payjoin open issues](https://github.com/payjoin/rust-payjoin/issues). Issues labeled `good first issue` are your targets. Comment on one to claim it or ask clarifying questions.
- Read [Dan Gould's "Payjoin is Practical"](https://payjoindevkit.org/blog/payjoin-is-practical/) and the [BIP77 spec](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki). If you find inconsistencies between the blog post and the spec, that's an issue worth filing.

---

### Session 10: Building with Payjoin Dev Kit (Rust)

**Learn:** PDK architecture. PSBT construction and modification. Integrating PDK into a wallet application. Testing on signet.

**Build:** Complete Payjoin flow in Rust: create original PSBT, receiver modifies, sender verifies (all 5 checks), sign and broadcast. Analyze the on-chain result.

**Contribute this week:**
- Your PDK integration exercise probably surfaced rough edges in the documentation or API. File issues on [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) describing what was unclear, what error messages were unhelpful, or what's missing from the docs.
- Better yet: fix the documentation yourself. PDK docs PRs are the fastest way to get merged code in the Payjoin ecosystem. Submit a PR improving `README.md`, doc comments in the source, or the integration example.
- If you wrote a clean integration example that's better than what exists: submit it as a PR to the `examples/` directory.

---

### Session 11: Payjoin in Production — BTCPay Server & Wallets

**Learn:** BTCPay Server's Payjoin implementation. Bull Bitcoin's BIP77 integration. UX considerations. Running a Payjoin-enabled payment server.

**Build:** Set up BTCPay Server with Payjoin. Make a Payjoin payment. Trace the code path. Compare on-chain footprints.

**Contribute this week:**
- Pick a Bitcoin wallet that doesn't support Payjoin yet. Research what it would take to add support. Write up your findings as a GitHub issue on that wallet's repo: "Payjoin (BIP77) support — feasibility assessment." Include: which Payjoin library to use (PDK), estimated effort, and the privacy benefit for users. This is how adoption starts.
- Test BTCPay Server's Payjoin with different wallets. If something breaks or the UX is confusing, file a detailed issue on [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver) with steps to reproduce.
- Review an open Payjoin-related PR on BTCPay Server or rust-payjoin. Leave a review with test results.

---

### Session 12: Contributing to Payjoin — Ship Your Code

**Learn:** payjoin-rust codebase deep dive. Testing strategies. How to get PRs merged.

**Build:** Pick an open issue. Write the fix. Submit the PR. Get peer review from other participants.

**Contribute this week — submit a PR:**
- **Target repos:** [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin), [btcpayserver/btcpayserver](https://github.com/btcpayserver/btcpayserver), or any wallet where you're adding Payjoin support.
- Bug fix, test case, documentation improvement, or new feature — all count.
- If your PR from Session 8 received review feedback, address it and push updates this week.
- Peer review: every participant reviews at least one other participant's PR before the next session.

**Phase 3 running total: Every participant has PRs submitted to both SP and Payjoin ecosystems. Most have 2-3 PRs open or merged.**

---

## Phase 4: Network & Protocol Privacy — Beyond Transactions

*Months 7-8 · Sessions 13-16 · Your node and your connections leak too. Fix that, and help others fix it.*

### Session 13: P2P Network Privacy — Dandelion++, Tor, I2P

**Learn:** How transaction relay reveals your IP. Dandelion++ stem-and-fluff. Tor/I2P integration in Bitcoin Core. Eclipse attacks and mitigations.

**Build:** Configure Bitcoin Core in three modes (clearnet, Tor-only, hybrid). Analyze peer connections. Simulate adversary IP linking probability for each configuration.

**Contribute this week:**
- Bitcoin Core's Tor and I2P documentation could always be better. Read the current docs at `doc/tor.md` and `doc/i2p.md`. If anything is outdated or unclear, submit a PR improving it.
- Search Bitcoin Core issues for labels related to `P2P` or `privacy`. Find one you understand well enough to comment on with a test result or analysis.
- If you found that a specific Bitcoin Core privacy configuration is poorly documented, write it up and submit to [Bitcoin Optech](https://github.com/bitcoinops/bitcoinops.github.io) as a contribution to their Topics section.

---

### Session 14: Compact Block Filters — BIP157/158 Deep Dive

**Learn:** Why BIP37 Bloom filters were a privacy disaster. Golomb-Rice Coded Sets. BIP157 client-server protocol. False positive rates. Filter construction.

**Build:** Implement Golomb-Rice encoding/decoding from scratch. Build a GCS filter. Query it. Measure false positive rates for different parameters.

**Contribute this week:**
- [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) uses compact block filters. Clone, build, and run it. Browse issues — this is an early-stage project that needs contributors. Even filing well-described bugs from your testing is valuable.
- Compare your Golomb-Rice implementation against Kyoto's. If you find an optimization or a cleaner approach, open a PR.
- Check if [Floresta](https://github.com/vinteumorg/Floresta) has any open issues related to block filter handling. Comment on one with your analysis.

---

### Session 15: Light Client Privacy — Floresta, Kyoto, Neutrino

**Learn:** The light client privacy spectrum. Floresta's utreexo approach. Kyoto's CBF implementation. Privacy comparison of 5 light client approaches.

**Build:** Set up Floresta on signet. Read Kyoto source code. Build a structured privacy comparison matrix for SPV, Electrum, Neutrino, Floresta, and full node.

**Contribute this week:**
- Floresta is actively looking for contributors. Check [Floresta issues labeled "good first issue"](https://github.com/vinteumorg/Floresta/labels/good%20first%20issue). Pick one and start working on it.
- Your privacy comparison matrix from the exercise is publishable content. Clean it up and submit it as a PR to the Floresta or Kyoto docs, or as a blog post to Bitcoin Optech.
- Test Floresta and Kyoto against edge cases. File issues with detailed reproduction steps for anything unexpected.

---

### Session 16: Taproot Privacy — Schnorr, MAST & Key Path Spending

**Learn:** How Taproot makes multisig indistinguishable from single-sig. MuSig2 and FROST for multi-party privacy. CISA and future privacy improvements.

**Build:** Create three Taproot transactions (single-sig, 2-of-2 MuSig, script path). Compare on-chain footprints. Analyze Taproot adoption metrics. Calculate CISA fee savings for CoinJoin.

**Contribute this week:**
- Taproot adoption is still low. Research which wallets support Taproot by default and which don't. File issues on wallets that don't default to Taproot outputs, explaining the privacy benefit.
- Review a Taproot-related PR on Bitcoin Core or BDK. Focus on the privacy implications of the change.
- Check the [CISA research site](https://cisaresearch.org). If there are open questions or areas where analysis would help, write up your findings and share with the research community.

**Phase 4 running total: Participants have contributed to 3-4 different repos. Many have PRs merged. Everyone has reviewed multiple PRs.**

---

## Phase 5: Advanced Privacy Techniques

*Months 9-10 · Sessions 17-20 · CoinJoin, CoinSwap, eCash, Lightning — contribute to the cutting edge.*

### Session 17: CoinJoin — Equal-Output Mixing & WabiSabi

**Learn:** CoinJoin mechanics. Toxic change. WabiSabi protocol. CoinJoin weaknesses. Regulatory landscape and what it means for development.

**Build:** Identify CoinJoins from raw transactions. Calculate anonymity sets. Identify toxic change. Simulate a multi-user CoinJoin construction.

**Contribute this week:**
- CoinJoin tooling needs better analysis tools. If your CoinJoin analyzer from the exercise is useful, publish it as a standalone repo under CC0.
- Research [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) (CoinSwap, next session). Clone it, build it, read the README. File issues for anything unclear in the setup process.
- Write a short comparison of CoinJoin implementations (JoinMarket, Wasabi WabiSabi, Whirlpool). Publish as a blog post or submit to Bitcoin Optech.

---

### Session 18: CoinSwap & Atomic Swaps for Privacy

**Learn:** How CoinSwap breaks the transaction graph entirely. Hash time-locked contracts. Teleport Transactions. Multi-hop CoinSwap. CISA implications.

**Build:** Walk through a CoinSwap on paper. Analyze on-chain observer visibility. Calculate current CoinJoin vs CoinSwap costs, with and without CISA.

**Contribute this week:**
- [Teleport Transactions](https://github.com/nickhntv/teleport-transactions) is actively maintained and needs contributors. Browse issues. This is a high-impact project that OpenSats specifically wants to see work on.
- File issues on Teleport for any bugs, documentation gaps, or UX problems you encountered while building and testing.
- Start working on a Teleport issue. Even a documentation PR here is very valuable — the project is early-stage and every contributor matters.

---

### Session 19: eCash Privacy — Fedimint & Cashu

**Learn:** Chaumian blind signatures. Cashu protocol. Fedimint architecture. How eCash complements on-chain privacy.

**Build:** Set up a Cashu mint on signet. Mint, send, and redeem tokens. Analyze what the mint learns at each step. Walk through the blind signature math.

**Contribute this week:**
- [cashubtc/nutshell](https://github.com/cashubtc/nutshell) is Python — accessible to everyone. Browse issues. The Cashu ecosystem is growing fast and needs contributors for testing, documentation, and feature development.
- [fedimint/fedimint](https://github.com/fedimint/fedimint) has issues labeled ["good first issue"](https://github.com/fedimint/fedimint/labels/good%20first%20issue). Pick one. The Fedimint community is very welcoming to new contributors.
- If you set up a Cashu mint successfully, write a step-by-step guide and submit it as a PR to the nutshell docs. Real-world setup guides from actual users are incredibly valuable.

---

### Session 20: Lightning Privacy — Blinded Paths, Probing & Route Privacy

**Learn:** Lightning's privacy model. Channel balance probing. Blinded paths (BOLT12). Trampoline routing. Private vs public channels. BOLT12 offers.

**Build:** Set up two LN nodes on signet. Probe your own channel. Compare BOLT11 vs BOLT12 privacy. Design a maximum-privacy LN configuration.

**Contribute this week:**
- [lightningdevkit/rust-lightning](https://github.com/lightningdevkit/rust-lightning) (LDK) has issues labeled ["good first issue"](https://github.com/lightningdevkit/rust-lightning/labels/good%20first%20issue). LDK powers many Lightning wallets — contributions here have enormous reach.
- Your Lightning privacy analysis from the exercise is publishable. Clean it up and submit as a blog post or technical note.
- If you found privacy issues in a Lightning wallet during testing, file them with detailed reproduction steps.

**Phase 5 running total: Participants are contributing across 5+ different repos. Most have 3-5 PRs submitted. Several have merged PRs.**

---

## Phase 6: Building & Contributing — Ship Substantial Work

*Months 11-12 · Sessions 21-24 · Everything you've learned, applied. Every graduate ships real code.*

### Session 21: Privacy-Preserving Wallet Development with BDK

**Learn:** Bitcoin Dev Kit architecture. Privacy-by-default wallet design. Privacy-optimized coin selection in BDK. Descriptor wallets.

**Build:** Scaffold a BDK wallet with privacy-optimized coin selection, change output safety, and address reuse detection. Add basic Payjoin or SP support.

**Contribute this week:**
- Submit a PR to [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk). Your wallet exercise likely surfaced gaps in the coin selection API, missing privacy-related configuration options, or documentation that could be clearer.
- File issues on BDK for any privacy-related improvements you think the library should support (e.g., "add a privacy score to coin selection results" or "warn when change output script type doesn't match recipient").

---

### Session 22: Privacy Testing & Mempool Analysis

**Learn:** Systematic transaction privacy evaluation. Mempool analysis. Automated privacy testing for wallet software.

**Build:** Build a transaction privacy scorer in Python: checks for address reuse, script type mixing, round amounts, detectable change, fee fingerprints, locktime patterns, and UTXO consolidation. Score 20 real mainnet transactions.

**Contribute this week:**
- Your privacy scoring tool is a real contribution to the ecosystem. Publish it as a standalone repo under CC0. If it's good enough, submit it to [Bitcoin Dev Project](https://github.com/bitcoin-dev-project) as a community tool.
- Run your scorer against transactions from popular wallets. If you find consistent privacy leaks, file issues on those wallets with your data and methodology.
- Contribute your scoring methodology to Bitcoin Optech or the Bitcoin Wiki as a reference for wallet developers.

---

### Session 23: Contribution Sprint — The Big Push

**Learn:** How to find and claim Good First Issues. How to write a PR that gets merged. How to respond to review feedback.

**This is a 3-hour working session:**

```
00:00 - 00:30   Issue selection: each participant picks a target
00:30 - 02:00   Code: write your fix, test it, prepare the PR
02:00 - 02:30   Peer review: every participant reviews one other PR
02:30 - 03:00   Submit: push, open the PR, celebrate
```

**Curated issue list (updated monthly by the facilitator):**

| Repo | Language | What to Look For |
|------|----------|-----------------|
| [bitcoin/bitcoin](https://github.com/bitcoin/bitcoin) | C++ | Silent Payments, compact block filters, P2P privacy |
| [cygnet3/rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) | Rust | Test coverage, edge cases, documentation |
| [payjoin/rust-payjoin](https://github.com/payjoin/rust-payjoin) | Rust | Good first issues, integration examples, docs |
| [vinteumorg/Floresta](https://github.com/vinteumorg/Floresta) | Rust | Good first issues, testing, documentation |
| [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) | Rust | Early-stage — lots of opportunities |
| [fedimint/fedimint](https://github.com/fedimint/fedimint) | Rust | Good first issues, module development |
| [cashubtc/nutshell](https://github.com/cashubtc/nutshell) | Python | Testing, documentation, mint features |
| [bitcoindevkit/bdk](https://github.com/bitcoindevkit/bdk) | Rust | Coin selection, privacy features |
| [lightningdevkit/rust-lightning](https://github.com/lightningdevkit/rust-lightning) | Rust | Good first issues, privacy features |
| [nickhntv/teleport-transactions](https://github.com/nickhntv/teleport-transactions) | Rust | CoinSwap implementation, testing |

---

### Session 24: Capstone — Present Your Contributions

**Each participant presents (10 minutes):**
1. **What you contributed** (4 min) — Walk through your PRs. Show the code. Link to them.
2. **What impact it has** (2 min) — Who benefits? How does this make Bitcoin more private?
3. **What you learned** (2 min) — What was harder than expected? What changed how you think about privacy?
4. **What's next** (2 min) — If you had 6 more months of funded time, what would you build?

**Open to the full Code Orange community** — Bitcoin Dojo, rawBit, Decoding Bitcoin cohorts all attend.

**Graduating participants who have:**
- Attended 18+ of 24 sessions (75%)
- Submitted 3+ PRs to Bitcoin privacy projects
- Presented at the capstone

...are eligible for the **Code Orange Developer Fellowship** ($500/month, 6 months) to continue contributing full-time.

---

## Contribution Tracker

Every participant maintains a public contribution log. This is what grant reviewers see — proof that the program produces real output.

| Session | Minimum Contribution | Target Repos |
|---------|---------------------|--------------|
| 01 | Star 5 repos. Clone bitcoin/bitcoin. Read coinselection.cpp | bitcoin/bitcoin, BDK, rust-silentpayments, rust-payjoin, Floresta |
| 02 | Test a wallet's fingerprint. Note findings for future issue. | Any Bitcoin wallet repo, Bitcoin Optech |
| 03 | Comment on a BDK coin selection issue with analysis | bitcoindevkit/bdk, bitcoin/bitcoin |
| 04 | File your first issue or docs PR on a wallet's privacy | Any wallet repo, Bitcoin Wiki |
| 05 | Read BIP352. Comment on a rust-silentpayments issue | bitcoin/bips, rust-silentpayments |
| 06 | Add a test case or file an issue on SP test vectors | bitcoin/bips, rust-silentpayments |
| 07 | Review a PR on bitcoin/bitcoin or Kyoto (CBF-related) | bitcoin/bitcoin, kyoto |
| 08 | **Submit your first PR** to an SP or CBF project | rust-silentpayments, kyoto, bitcoin/bitcoin |
| 09 | Clone rust-payjoin. Comment on an open issue | payjoin/rust-payjoin |
| 10 | File issues on PDK documentation or API rough edges | payjoin/rust-payjoin |
| 11 | File a Payjoin feasibility issue on a wallet that lacks it | Any wallet repo, BTCPay |
| 12 | **Submit a PR** to Payjoin ecosystem | rust-payjoin, BTCPay |
| 13 | Improve Bitcoin Core Tor/I2P documentation | bitcoin/bitcoin (doc/) |
| 14 | Test and file issues on Kyoto or Floresta | kyoto, Floresta |
| 15 | **Submit a PR** to Floresta or Kyoto | Floresta, kyoto |
| 16 | File Taproot adoption issues on wallets not defaulting to P2TR | Any wallet repo |
| 17 | Publish CoinJoin analysis tool. Research Teleport issues | teleport-transactions |
| 18 | **Submit a PR** to Teleport Transactions | teleport-transactions |
| 19 | Submit docs or test PR to Cashu or Fedimint | nutshell, fedimint |
| 20 | **Submit a PR** to LDK or Core Lightning (privacy-related) | rust-lightning, lightning |
| 21 | **Submit a PR** to BDK (privacy feature or coin selection) | bdk |
| 22 | Publish privacy scoring tool. File issues on wallets tested | Any wallet repo |
| 23 | **Contribution sprint: submit a PR** | Any privacy-related repo |
| 24 | Present all contributions. Apply for fellowship if eligible | — |

**Expected output per participant over 12 months: 5-8 PRs submitted, 3-5 merged, across 3+ different repos.**

**Expected output for a cohort of 15 participants: 75-120 PRs submitted, 45-75 merged.**

---

## Session Format

Every session follows the same structure. The last 30 minutes are always about contributing.

```
00:00 - 00:15   Review: Show your contributions since last session. What got merged?
                 What feedback did you get? What's blocking you?
00:15 - 00:45   Concept: Theory and protocol walkthrough
00:45 - 01:45   Build: Hands-on coding exercise
01:45 - 02:15   Contribute: Open laptops. Find issues. File PRs. Review code.
                 The facilitator helps match participants to issues in real time.
02:15 - 02:30   Plan: Assigned reading + specific contribution goal for next 2 weeks
```

The "Review" at the start of each session creates accountability. When you know you'll be asked "what did you contribute since last time?" — you contribute.

---

## Exercises & Code

```
phase-1-foundations/
  session-01/chain_analysis_lab.py              — Trace transactions, apply heuristics
  session-03/coin_selection_simulator.py        — 4 algorithms, privacy scoring
  session-04/wallet_fingerprint_lab.py          — Identify wallets from raw transactions

phase-2-silent-payments/
  session-06/silent_payments_sender.py          — Build SP sender from scratch
  session-07/silent_payments_scanner.py         — Build SP scanner with CBF

phase-3-payjoin/
  session-10/pdk_integration/                   — Rust project using Payjoin Dev Kit
  session-11/btcpay_payjoin_lab.md              — BTCPay Server Payjoin walkthrough

phase-4-network-privacy/
  session-14/compact_block_filters.py           — Golomb-Rice coding from scratch
  session-16/taproot_privacy_lab.py             — Taproot key path vs script path analysis

phase-5-advanced/
  session-17/coinjoin_analysis.py               — CoinJoin detection and analysis
  session-19/cashu_mint_exercise.md             — Set up a Cashu mint on signet

phase-6-contributing/
  session-22/privacy_scorer.py                  — Transaction privacy scoring tool
```

---

## Resources

- [Reading List](resources/reading-list.md) — 60+ resources organized by phase
- [Glossary](resources/glossary.md) — 50+ terms covering all 6 phases
- [Facilitator Guide](FACILITATOR_GUIDE.md) — Session-by-session facilitation notes
- [Capstone Projects](capstone/README.md) — 4 project tracks with rubrics
- [Contributing](CONTRIBUTING.md) — How to contribute to this curriculum

---

## For Grant Reviewers

This is not a lecture series. This is a contribution pipeline.

From session 1, participants are reading real Bitcoin source code and engaging with real repos. By session 4, they've filed their first issue. By session 8, they've submitted their first PR. By session 24, they have 5-8 PRs across 3+ repos — Silent Payments, Payjoin, Floresta, Kyoto, Fedimint, Cashu, BDK, LDK, and Bitcoin Core itself.

The curriculum is already published (40 files, CC0-licensed). The exercises are real. The contribution targets are specific. Every session ends with laptops open and code being pushed to GitHub.

**Expected output for one cohort (15 participants, 12 months): 75-120 PRs submitted to Bitcoin privacy repos, 45-75 merged.**

That's what your grant buys.

---

*[Code Orange Dev School](https://codeorange.dev) · Bitcoin House Bali, Indonesia · CC0 1.0 Universal*
