# Module 4: Privacy-Preserving Wallet Development

> 3 sessions — Coin selection, compact block filters, CoinJoin, and the future of on-chain privacy.

---

## Session 1: Transaction Construction for Privacy

### Overview

Even without Silent Payments or Payjoin, the way a wallet constructs a transaction reveals enormous amounts of information. This session covers the subtle fingerprints that wallets leave in every transaction and how privacy-conscious wallet developers can eliminate them.

### Topics

**Coin Selection Algorithms**
- **Largest-first**: simple but creates obvious change outputs — bad for privacy
- **Branch and bound**: tries to find exact-match combinations (no change) — great for privacy
- **Random selection**: adds entropy but wastes fees
- **Privacy-optimized**: avoid combining UTXOs from different sources, prefer spending whole UTXOs
- The trade-off: fee efficiency vs privacy — you can't always optimize both
- BDK's coin selection module and how to extend it

**Change Output Handling**
- **Avoiding change entirely**: branch-and-bound to find exact-match input sets
- **Change output script type**: must match the payment output's script type (P2WPKH → P2WPKH)
- **Change output position**: randomize (don't always put change first or last)
- **Dust avoidance**: tiny change outputs are uneconomical and reveal information
- **Change avoidance strategies**: slightly overpay fees to eliminate change

**Fee Fingerprinting and Timing Analysis**
- Different wallets use different fee estimation methods
- Bitcoin Core uses `estimatesmartfee` — a recognizable fee curve
- Some wallets always use round fee rates (5 sat/vB, 10 sat/vB)
- Transaction broadcast timing can reveal timezone/geography
- Mempool snooping: observing which node first relays a transaction

**Wallet Fingerprints: nLockTime, nSequence, Version**
- `nLockTime`: Bitcoin Core sets this to current block height (anti-fee-sniping) — identifiable
- `nSequence`: different values reveal which wallet created the transaction
- `version`: most wallets use version 2, but some still use version 1
- Input ordering: BIP69 (deprecated) vs random vs deterministic
- Output ordering: random is best for privacy
- These fingerprints are invisible to users but obvious to chain analysts

### Exercise

**Wallet Fingerprint Analysis:**
1. Take 5 transactions from mempool.space (mainnet)
2. For each transaction, identify:
   - Likely wallet software (based on fingerprints above)
   - Change output (using heuristics from Module 1)
   - Fee estimation method
3. Compare a Bitcoin Core transaction vs an Electrum transaction vs a mobile wallet transaction
4. Document which fingerprints are most reliable for identification

### Discussion Questions

1. If you were building a new wallet from scratch, what transaction construction defaults would you choose for maximum privacy?
2. Should wallets sacrifice fee efficiency for privacy? How should this trade-off be presented to users?
3. Why is output ordering important? What information does a deterministic order leak?

### Reading

- [Bitcoin Wiki: Privacy — Wallet Fingerprinting](https://en.bitcoin.it/wiki/Privacy#Wallet_fingerprinting)
- [Bitcoin Optech: Coin Selection](https://bitcoinops.org/en/topics/coin-selection/)
- [Murch: Coin Selection with Leverage](https://murch.one/erhardt2016coinselection.pdf)

---

## Session 2: Compact Block Filters & Light Client Privacy

### Overview

Full nodes offer the best privacy but aren't practical for everyone. Light clients need to query the network for their transactions — but how do they do this without revealing which addresses they own? Compact block filters (BIP157/158) offer the best current solution. This session covers how they work and the projects building them.

### Topics

**BIP157/158 — How Compact Block Filters Work**
- The problem: SPV clients (BIP37) tell full nodes exactly which addresses they're watching — terrible for privacy
- The solution: full nodes create a small "filter" for each block containing all the scripts in that block
- The filter is a probabilistic data structure — it can tell you "this block MIGHT contain your transaction"
- Client downloads filters for every block (small: ~20KB per filter) and checks locally
- Only downloads the full block when the filter matches — no privacy leak to the serving node

**Golomb-Rice Coded Sets (GCS)**
- The compression algorithm used in BIP158 filters
- How it encodes a set of items with configurable false-positive rate
- The parameters chosen for BIP158: P=19 (false positive rate ~1/524,288), M=784,931
- Why GCS is more efficient than Bloom filters for this use case
- The bandwidth trade-off: filter size vs false positive rate

**Kyoto Light Client Project**
- [rustaceanrob/kyoto](https://github.com/rustaceanrob/kyoto) — Rust implementation
- Implements BIP157/158 compact block filter protocol
- Critical for Silent Payments: light clients need this to scan efficiently
- Integration with BDK for wallet development
- Current status and contribution opportunities

**Privacy Comparison: SPV vs Compact Block Filters vs Full Node**

| Property | SPV (BIP37) | Compact Filters (BIP157) | Full Node |
|----------|-------------|-------------------------|-----------|
| Privacy | Very poor — server knows your addresses | Good — server can't identify your addresses | Perfect — you validate everything locally |
| Bandwidth | Low | Medium (~20KB/block filter) | High (full blocks) |
| Computation | Minimal | Low (filter matching) | High (full validation) |
| Trust | Trusts server to provide correct data | Trusts server for filter, verifies blocks | Trustless |
| Suitable for mobile | Yes | Yes | No (usually) |

### Exercise

**Compact Block Filter Exploration:**
1. Using Bitcoin Core (`getblockfilter` RPC), retrieve the compact block filter for a recent block
2. Decode the filter and understand its structure
3. Check if a known address appears in the filter
4. Calculate the false positive rate: check 1000 random addresses against the filter
5. Compare the filter size to the full block size — what's the compression ratio?

### Discussion Questions

1. Why did BIP37 (Bloom filters) fail for privacy? What specific information does it leak?
2. If a compact block filter has a false positive rate of 1/524,288, how many false positives per day on mainnet?
3. Could a malicious node send you incorrect filters? How do you defend against this?
4. Why are compact block filters critical for Silent Payments adoption on mobile?

### Reading

- [BIP157: Client Side Block Filtering](https://bips.dev/157/)
- [BIP158: Compact Block Filters for Light Clients](https://bips.dev/158/)
- [Bitcoin Optech: Compact Block Filters](https://bitcoinops.org/en/topics/compact-block-filters/)
- [Kyoto Light Client](https://github.com/rustaceanrob/kyoto)

---

## Session 3: CoinJoin, CoinSwap, and Beyond

### Overview

The final session covers the most powerful privacy tools available today and the frontier of what's coming next. CoinJoin mixes your UTXOs with other users. CoinSwap swaps them atomically. And future protocol improvements like cross-input signature aggregation (CISA) could make privacy nearly free.

### Topics

**CoinJoin: Equal-Output Mixing**
- The original idea: multiple users contribute inputs and receive equal-value outputs
- No coordinator can steal funds (they only coordinate, never hold keys)
- WabiSabi protocol (used by Wasabi Wallet, Ginger Wallet):
  - Eliminates the fixed output size limitation
  - Keyed-verification anonymous credentials for input registration
  - Variable output amounts with privacy guarantees
- The anonymity set: how many equal outputs exist in the mix
- Limitations: equal outputs are recognizable as CoinJoin; requires other participants

**CoinSwap: Atomic Swaps for Privacy**
- Unlike CoinJoin, CoinSwap transactions look like normal payments on-chain
- Alice pays Bob, Bob pays Alice — two separate transactions, atomically linked via hash locks
- Chris Belcher's "Teleport Transactions" implementation
- Multi-hop CoinSwap: route through multiple intermediaries for stronger privacy
- The advantage over CoinJoin: no recognizable on-chain pattern

**JoinMarket NG and Its Approach**
- JoinMarket: decentralized CoinJoin marketplace with makers (liquidity providers) and takers
- JoinMarket NG: next generation, funded by OpenSats
- Fidelity bonds: makers lock bitcoin to prove they're not Sybil attackers
- How it differs from centralized coordinators (Wasabi, Ginger)

**The Future: Protocol-Level Privacy**
- **Cross-Input Signature Aggregation (CISA)**: aggregate all signatures in a transaction into one
  - Makes CoinJoin cheaper (fewer bytes = lower fees)
  - Economic incentive for privacy — mixing becomes the cheapest option
  - Requires a soft fork
- **Taproot-enabled privacy**: all spends (single-sig, multisig, HTLC, etc.) look identical
- **Schnorr signature aggregation**: enables MuSig2, threshold signatures
- **Ark**: off-chain payment protocol with on-chain settlement privacy
- The endgame: privacy by default, not privacy by choice

### Exercise

**Privacy Tool Comparison:**
1. Send 3 transactions on signet/regtest:
   - A normal P2WPKH transaction
   - A transaction with deliberately good privacy practices (no change, random output order, current-height nLockTime)
   - A CoinJoin-style transaction (simulate with multiple wallets)
2. Analyze all 3 using mempool.space or your own block explorer
3. For each transaction, rate: How much can a chain analyst learn? What is ambiguous?
4. Write a 1-page comparison of the three approaches

### Discussion Questions

1. CoinJoin creates equal outputs that are recognizable. Does this help or hurt privacy?
2. CoinSwap is invisible on-chain but requires a counterparty. What's the adoption bottleneck?
3. If CISA is activated, making CoinJoin cheaper than normal transactions, would privacy become the default? Why or why not?
4. What privacy improvements can be made today without any protocol changes?

### Assessment

**Final Project**: Write a 1,000-word report: **"A Privacy Roadmap for Bitcoin: What Exists, What's Missing, and Where I Want to Contribute."** Include specific projects and issues you plan to work on. This serves as your contribution plan for the post-track Contribution Sprint.

### Reading

- [Bitcoin Optech: CoinJoin](https://bitcoinops.org/en/topics/coinjoin/)
- [WabiSabi Paper](https://github.com/zkSNACKs/WabiSabi/blob/master/WabiSabi.pdf)
- [Chris Belcher: CoinSwap Design](https://gist.github.com/chris-belcher/9144bd57a91c194e332fb5ca371d0964)
- [Bitcoin Optech: CISA](https://bitcoinops.org/en/topics/cross-input-signature-aggregation/)

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
