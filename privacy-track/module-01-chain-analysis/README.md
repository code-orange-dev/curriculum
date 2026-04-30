# Module 1: Chain Analysis & Why Privacy Matters

> 2 sessions — Understand how Bitcoin surveillance works and why privacy is a protocol concern.

---

## Session 1: How Bitcoin Surveillance Works

### Overview

Before you can build privacy tools, you need to understand what you're defending against. This session covers the core heuristics that chain analysis firms use to de-anonymize Bitcoin users, and gives you hands-on experience tracing transactions yourself.

### Topics

**Common-Input-Ownership Heuristic (CIOH)**
- If a transaction has multiple inputs, they are assumed to belong to the same entity
- This is the single most powerful heuristic in chain analysis
- Why it works: wallets automatically combine UTXOs when spending
- How Payjoin (Module 3) specifically breaks this assumption

**Change Output Detection**
- Round amounts: sending 0.1 BTC means the other output is likely change
- Script type matching: if inputs are P2WPKH, the change is usually P2WPKH too
- Wallet-specific patterns: output ordering, fee estimation behavior
- Unnecessary input heuristic: if an input could be removed and the transaction still works, the smaller output is likely change

**Address Reuse and Clustering**
- Reusing an address links all transactions to the same entity
- Cluster analysis: combining CIOH + address reuse to build entity graphs
- Why HD wallets (BIP32) generate fresh addresses — and why that's not enough
- How Silent Payments (Module 2) solve this at the protocol level

**Timing Analysis and Fee Fingerprinting**
- Transaction broadcast timing can reveal geographic location
- Fee rate patterns identify wallet software
- nLockTime, nSequence, and version field differences between wallets
- Mempool observation and transaction relay timing

### Hands-On Exercise

**Trace a transaction chain on testnet/signet:**

1. Go to [mempool.space/signet](https://mempool.space/signet) or [OXT.me](https://oxt.me/)
2. Find a transaction with multiple inputs
3. Apply the common-input-ownership heuristic — which inputs belong to the same wallet?
4. Identify the change output — which heuristic did you use?
5. Follow the change output forward — can you trace the entity through 3+ transactions?
6. Document your analysis: which heuristics worked? Which were ambiguous?

### Discussion Questions

1. If you were building a wallet, which heuristic would you prioritize defeating first? Why?
2. Chain analysis firms claim 80-90% accuracy. What does that mean for the 10-20% of misidentified users?
3. Is it possible to make chain analysis completely impossible on a transparent ledger? Why or why not?

### Reading

- [Bitcoin Wiki: Privacy](https://en.bitcoin.it/wiki/Privacy) (comprehensive — read Sections 1-5)
- [Bitcoin Optech: Output Linking](https://bitcoinops.org/en/topics/output-linking/)

---

## Session 2: Privacy as a Protocol Property

### Overview

Privacy isn't a feature you bolt on — it's a property of the protocol. This session explores why privacy matters for Bitcoin's long-term viability, the difference between privacy and anonymity, and how privacy improvements at the base layer benefit all users, not just those who explicitly opt in.

### Topics

**Greg Maxwell's 2013 Post on Bitcoin Privacy**
- "Your inlaws don't see that you're buying birth control that deprives them of grandchildren"
- Traditional banking provides privacy by default — Bitcoin currently doesn't
- The practical consequences: theft targeting, competitive intelligence, discrimination
- Read the original: [bitcointalk.org/index.php?topic=279249.0](https://bitcointalk.org/index.php?topic=279249.0)

**Why "I Have Nothing to Hide" Is Wrong**
- Privacy is about power asymmetry, not guilt
- Fungibility: if coins can be traced and rejected, Bitcoin loses a core monetary property
- The merchant problem: accepting bitcoin exposes your revenue, suppliers, and customers
- The donation problem: supporting a cause reveals your political beliefs to anyone who checks
- The savings problem: your wealth is visible to anyone who knows one of your addresses

**Privacy vs Anonymity — What Bitcoin Actually Provides**
- Pseudonymous, not anonymous — your identity is one data leak away
- The privacy spectrum:
  - **Transparent**: all transactions visible, identity known (KYC exchange → your address)
  - **Pseudonymous**: transactions visible, identity unknown (fresh address, no KYC)
  - **Private**: transactions obscured, identity unknown (CoinJoin, Payjoin, eCash)
  - **Anonymous**: transactions and identity completely hidden (nearly impossible on-chain)
- Bitcoin's base layer is currently "pseudonymous" — the goal is "private by default"

**Privacy Improvements That Help Everyone**
- Silent Payments: every payment goes to a unique address (no more address reuse)
- Payjoin: breaks CIOH even for users who don't care about privacy
- Taproot: all spends look the same regardless of script complexity
- The "anonymity set" concept: privacy tools only work when many people use them
- Why base-layer privacy > application-layer privacy

### Discussion Questions

1. Greg Maxwell wrote his post in 2013. What has changed since then? What hasn't?
2. If Silent Payments were enabled by default in every wallet, how would that change chain analysis?
3. Taproot makes all spends look identical. Why isn't that enough for privacy?
4. What's the difference between "privacy by default" and "privacy as an option"? Why does it matter?

### Reading

- [Greg Maxwell: CoinJoin: Bitcoin privacy for the real world (2013)](https://bitcointalk.org/index.php?topic=279249.0)
- [Bitcoin Optech: Taproot](https://bitcoinops.org/en/topics/taproot/)
- [OpenSats: Advancements in On-Chain Privacy](https://opensats.org/blog/developing-advancements-in-onchain-privacy)

### Assessment

Write a 500-word essay: **"What is the most impactful privacy improvement that could be made to Bitcoin today, and why?"** Bring this to the next session for group discussion.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | CC0 1.0 Universal*
