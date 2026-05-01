# Phase 5: Advanced Privacy Techniques

> Months 9-10 · Sessions 17-20 · CoinJoin, CoinSwap, eCash, and Lightning — the full privacy toolkit.

## Overview

By now you understand chain analysis, can build Silent Payments and Payjoin from scratch, and know how network-layer privacy works. Phase 5 expands your toolkit to the full spectrum of Bitcoin privacy techniques: CoinJoin for mixing, CoinSwap for breaking the transaction graph, eCash for perfect payment privacy within federations, and Lightning for payment channel privacy. These are the tools that, combined with what you've already learned, give Bitcoin users a realistic path to financial privacy.

## Session 17: CoinJoin — Equal-Output Mixing & WabiSabi

**Date:** Month 9, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- CoinJoin fundamentals: multiple users create a single transaction with equal-value outputs
- Why equal outputs matter: unequal outputs allow "toxic change" linking
- Coordinator models: centralized (old Wasabi, JoinMarket), decentralized coordinator (WabiSabi)
- WabiSabi protocol deep dive: keyed verification anonymous credentials, registration, signing, blame rounds
- How Wasabi Wallet 2.0 implements WabiSabi
- CoinJoin weaknesses: timing analysis, amount correlation, Sybil attacks on coordinators
- Regulatory landscape: why Samourai was shut down and what it means for CoinJoin development

### Exercise: CoinJoin Analysis
File: `session-17-coinjoin/coinjoin_analysis.py`

1. Given 5 transactions, identify which are CoinJoins by analyzing output values and structure
2. For a known CoinJoin transaction, calculate the anonymity set (number of equal-value outputs)
3. Identify "toxic change" outputs that link back to specific inputs
4. Simulate: given 10 users with different UTXO amounts, construct an equal-output CoinJoin. What's the maximum equal output value? How much toxic change is produced?
5. Analyze: what would happen to the anonymity set if one user is a spy (Sybil)?

### Reading
- Greg Maxwell: CoinJoin original proposal (bitcointalk, 2013) — **Required**
- WabiSabi paper: "WabiSabi: Centrally Coordinated CoinJoins with Variable Amounts"
- Bitcoin Optech: CoinJoin topic page
- Adam Gibson: "From Coinjoin to Coinswap" (JoinMarket perspective)

---

## Session 18: CoinSwap & Atomic Swaps for Privacy

**Date:** Month 9, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- Why CoinSwap is fundamentally different from CoinJoin: swaps break the transaction graph entirely
- Atomic swap mechanics: hash time-locked contracts (HTLCs) for trustless exchange
- Chris Belcher's Teleport Transactions: the most active CoinSwap implementation
- Multi-hop CoinSwap: routing through multiple makers for stronger privacy (similar to Lightning)
- CoinSwap vs CoinJoin: privacy guarantees, tradeoffs, costs
- Cross-Input Signature Aggregation (CISA): how a future soft fork would make both CoinJoin and CoinSwap dramatically cheaper
- Submarine swaps: on-chain ↔ Lightning atomic swaps

### Exercise: CoinSwap Mechanics
1. Walk through a 2-party CoinSwap on paper: draw the HTLC contracts, timelocks, and hash preimages
2. Analyze: what does an on-chain observer see? What can they infer?
3. Extend to 3-party (routed) CoinSwap: draw the hop structure and analyze privacy at each point
4. Calculate: current cost of a 3-input CoinJoin vs a 2-party CoinSwap (in vbytes and sats). Then calculate with CISA.
5. Read through Teleport Transactions source code: identify the main modules and the swap state machine

### Reading
- Chris Belcher: "CoinSwap" design document — **Required**
- Teleport Transactions repository: https://github.com/nickhntv/teleport-transactions
- Bitcoin Optech: CoinSwap topic page
- CISA research: https://cisaresearch.org

---

## Session 19: eCash Privacy — Fedimint & Cashu

**Date:** Month 10, Week 1
**Duration:** 2.5 hours

### What You'll Learn
- David Chaum's eCash: blind signatures and why they provide perfect sender privacy
- The trust model: eCash requires trusting the mint (unlike Bitcoin) — but the privacy guarantees are stronger
- Cashu protocol: simple eCash implementation for Bitcoin, using the Lightning Network for deposits/withdrawals
- Fedimint architecture: federated mint with BFT consensus, modules (mint, wallet, Lightning gateway), and guardians
- How eCash complements on-chain privacy: use eCash for small payments, on-chain for settlement
- Privacy analysis: what the mint knows, what it doesn't, what federation guardians can see

### Exercise: Cashu Mint Lab
File: `session-19-ecash/cashu_mint_exercise.md`

1. Set up a Cashu mint on signet using nutshell (Python reference implementation)
2. Mint tokens by paying a Lightning invoice
3. Send tokens to another participant (peer-to-peer, no mint interaction)
4. Redeem tokens back to Lightning
5. Analyze: at each step, what information does the mint have? Can it link sender to receiver?
6. Attempt a double-spend: what happens?
7. Examine the blind signature math: how does the blinding factor prevent the mint from linking issuance to redemption?

### Reading
- David Chaum: "Blind Signatures for Untraceable Payments" (1983) — **Required**
- Cashu NUT specifications: https://github.com/cashubtc/nuts
- Fedimint documentation: https://fedimint.org
- Calle: "eCash for Bitcoin" (blog post explaining Cashu)

---

## Session 20: Lightning Privacy — Blinded Paths, Probing & Route Privacy

**Date:** Month 10, Week 3
**Duration:** 2.5 hours

### What You'll Learn
- Lightning's privacy model: what senders know, what routing nodes know, what receivers know
- Channel balance probing: how an adversary can determine your channel balances
- Onion routing: how Lightning uses Sphinx to hide the payment path from intermediaries
- Blinded paths (BOLT12): how receivers hide their node identity and last-hop channel
- Trampoline routing: delegating route finding for better privacy
- Private channels vs public channels: when to use each
- BOLT12 offers: reusable payment codes for Lightning (similar to Silent Payments for on-chain)
- JIT (Just-In-Time) channel opening and its privacy implications

### Exercise: Lightning Privacy Analysis
1. Set up two LND or CLN nodes on signet with a channel between them
2. Probe your own channel: send payments of varying amounts to determine the balance distribution
3. Analyze: what information does a routing node learn about a payment it forwards?
4. Compare: create a BOLT11 invoice and a BOLT12 offer. What information does each reveal to the sender?
5. Write up: design a "maximum privacy" Lightning node configuration. What tradeoffs are you making?

### Reading
- BOLT4: Onion Routing Protocol — **Required**
- BOLT12: Offers specification
- Rene Pickhardt: "Channel balance probing" research
- Bitcoin Optech: Lightning privacy topic page

---

## Phase 5 Contribution Target

By the end of Phase 5, every participant should submit at least one PR to a CoinJoin, CoinSwap, eCash, or Lightning privacy project.

### Key Repos
- [nickhntv/teleport-transactions](https://github.com/nickhntv/teleport-transactions) (CoinSwap)
- [fedimint/fedimint](https://github.com/fedimint/fedimint) (eCash federation)
- [cashubtc/nutshell](https://github.com/cashubtc/nutshell) (Cashu mint)
- [lightningdevkit/rust-lightning](https://github.com/lightningdevkit/rust-lightning) (LDK)
- [ElementsProject/lightning](https://github.com/ElementsProject/lightning) (Core Lightning)

---

## What's Next

Phase 6 brings everything together: build a privacy-preserving wallet with BDK, create a transaction privacy scoring tool, sprint on open-source contributions, and present your work to the community.

---

*[Code Orange Dev School](https://codeorange.dev) · CC0 1.0 Universal*