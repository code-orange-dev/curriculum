# Bitcoin Privacy Developer Track: Phase 1 - Foundations (Sessions 1-4)

## Overview

Phase 1 establishes the technical and threat-modeling foundations for Bitcoin privacy. Developers learn how chain analysis works, understand transaction structure from a privacy lens, master UTXO management, and recognize wallet fingerprints. By the end of Phase 1, participants can analyze their own transactions for privacy leaks and make informed choices about wallet selection.

**Time Commitment:** 4 weeks, 8-10 hours per session  
**Target Audience:** Intermediate developers (familiar with Bitcoin basics and CLI tools)  
**Outcome:** Ability to recognize privacy vulnerabilities and implement privacy-preserving UTXO strategies

---

## Session 1: Chain Analysis & Surveillance

### Real-World Scenario

**Maria's Privacy Crisis**  
Maria runs a small organic coffee shop in Bali. She started accepting Bitcoin in 2023 and promoted her payment address on social media. Within months, a competitor used blockchain explorers to track her revenue: they saw every payment, calculated her sales volume, and could estimate her profit margins. One customer noticed their personal address was linked to Maria's shop address and felt exposed. Maria is now considering closing her Bitcoin payments or finding a private solution. But she still has 1.2 BTC sitting in that address—moving it would broadcast her entire transaction history to chain analysis firms that she suspects are already watching.

### Learning Objectives

By the end of Session 1, you will:
- Understand how chain analysis firms link addresses and identify behavioral patterns
- Use industry-standard tools (OXT.me, mempool.space) to perform analysis
- Recognize clustering heuristics (change address identification, transaction timing)
- Evaluate the threat model of different business use cases
- Articulate why privacy is not optional for business operations

### Privacy Tools You'll Use

- **OXT.me** — Advanced chain analysis and address clustering tool (Bitcoin-only, no KYC required to use)
- **mempool.space** — Real-time transaction explorer with privacy analysis features
- **Chainalysis Reactor (demo mode)** — Understanding enterprise surveillance capabilities (public demo)
- **bitcoin-cli** — Inspecting raw transaction data
- **Entropy** — Understanding address linking heuristics

### Hands-On Exercise: "Identify Yourself"

Your goal: analyze a public Bitcoin address to discover how much you can learn without additional context.

**Step 1:** Go to https://oxt.me  
**Step 2:** Search for address `1A1z7agoat4EvZ2D1V6v6ox6KSQqSWCVH5` (a famous early address)  
**Step 3:** Document in a local file:
- How many incoming transactions?
- How many UTXOs were created from this address?
- What does the "change address" pattern tell you?
- Can you identify likely sweep transactions vs. business-use payments?

**Step 4:** Go to https://mempool.space/address/1A1z7agoat4EvZ2D1V6v6ox6KSQqSWCVH5  
**Step 5:** Compare the data shown in mempool vs OXT:
- What additional metadata does mempool expose (timestamps, fee estimates)?
- How would a law enforcement agency use this to correlate payments across time?

**Step 6:** Open Terminal and run:
```bash
curl -s https://mempool.space/api/address/1A1z7agoat4EvZ2D1V6v6ox6KSQqSWCVH5 | jq '.chain_stats'
```
- Examine the JSON: total_tx_count, funded_txo_sum, spent_txo_sum
- Calculate the net movement of funds through this address over time

**Step 7:** Document a written threat assessment:
- If you were law enforcement, what would you conclude about this address's owner?
- What behavioral patterns indicate business vs. personal use?
- What additional information would you need to identify the owner?

**Step 8:** Write pseudocode for an automated clustering algorithm:
```
For each address in a transaction:
  IF (output[i] > output[j] for all j != i):
    LIKELY_CHANGE = output[i]
  CLUSTER(sender_address, all output addresses)
```

### Open a PR This Week

**Contribute to bitcoin-inquisition or mempool.space**

1. Visit https://github.com/mempool/mempool  
2. Navigate to Issues tab, filter by `label: "good first issue"`
3. Pick one of:
   - Add a new privacy metric to address analysis (e.g., "change address confidence score")
   - Implement a clustering visualization (improve address graph display)
   - Write a test case for the Chainalysis-resistant address detection logic
4. Fork the repo, create a branch, submit a PR with clear documentation of the privacy metric or feature
5. Reference this PR in your final Phase 1 submission

**Alternative:** Contribute to OXT.me documentation:
1. Go to https://github.com/oxt-research/blockchain-analytics-research
2. Add a tutorial or documentation for the clustering heuristics you learned this week
3. Submit a markdown file with 500+ words of analysis and examples

### Daily Life Privacy Tip

**Use mempool.space's "Privacy Analysis" feature before every transaction.**

When you're about to send Bitcoin: go to mempool.space, paste your address, and review the "Cluster" analysis. You'll immediately see which of your previous addresses are linked by chain analysis. Before consolidating UTXOs or making large transfers, check whether you're about to merge outputs that chain analysis has already separated. This 30-second check prevents you from accidentally revealing hidden business relationships.

**Concrete example:** If you have KYC coins from a CoinBase deposit linked to address A, and non-KYC coins from a peer-to-peer trade linked to address B, do NOT merge them in a single transaction. Chain analysis will immediately correlate your KYC profile with your private activity. Mempool's clustering analysis shows this risk visually.

### Reading List with Links

1. **"How Chainalysis Made Me Paranoid" — Unchained Podcast**  
   https://podcasts.apple.com/us/podcast/how-chainalysis-made-me-paranoid/id1438148082
   - 45-min audio primer on how surveillance firms work

2. **"Heuristics for Bitcoin Address Clustering" — OXT Research**  
   https://github.com/oxt-research/blockchain-analytics-research/blob/master/clustering_heuristics.md
   - Technical reference for change address identification

3. **"Chain Analysis Fundamentals" — Bitcoin Privacy Institute**  
   https://bitcoinprivacyinstitute.org/fundamentals/
   - Interactive tutorial on linking addresses and pattern recognition

4. **Chainalysis Reactor Public Demo**  
   https://go.chainalysis.com/demo-reactor.html
   - See enterprise surveillance tools in action (no login required)

5. **"Transaction Fee Analysis: A Window Into Miner Behavior" — Jameson Lopp**  
   https://blog.lopp.net/transaction-fee-analysis/
   - How fee patterns leak timing information

6. **OXT.me User Guide**  
   https://oxt.me/guide
   - Complete documentation for the tools you're using

---

## Session 2: Transaction Anatomy for Privacy

### Real-World Scenario

**Developer's Dilemma**  
You're building a feature in your Bitcoin wallet that shows users whether their transaction is "private." But how do you analyze privacy at the transaction level? You find a transaction in mempool: multiple inputs, multiple outputs, mixed output values. One output is significantly larger—is it change or payment to the merchant? Is the change address on-chain reused? Does the wallet have a time-stamp of when the change address was created? Which heuristic breaks down? A user tests your feature and finds contradictory privacy scores. You realize: you can't evaluate transaction privacy without understanding exactly how that transaction's data structure leaks information.

### Learning Objectives

By the end of Session 2, you will:
- Understand the on-chain differences between privacy-leaking and privacy-preserving transactions
- Analyze transaction structure using bitcoin-cli and Sparrow Wallet
- Identify which outputs are likely change vs. payment
- Recognize timing and amount-based privacy leaks
- Design transaction patterns that resist common heuristics

### Privacy Tools You'll Use

- **bitcoin-cli** — Raw transaction inspection (`getrawtransaction`, `decoderawtransaction`)
- **Sparrow Wallet** — Transaction inspector with privacy scoring
- **mempool.space** — Visual transaction dissection
- **bitcoin-tx** — Transaction creation and inspection utility
- **mitmproxy** — Observing network-level leaks (optional advanced)

### Hands-On Exercise: "Decode the Privacy Leak"

**Step 1:** Set up a local Bitcoin testnet node (or use a public testnet):
```bash
bitcoind -testnet -server
bitcoin-cli -testnet getblockcount
```

**Step 2:** Create a transaction with multiple inputs and outputs:
```bash
bitcoin-cli -testnet createrawtransaction \
  '[{"txid":"TXID1","vout":0},{"txid":"TXID2","vout":1}]' \
  '{"address1":0.5,"address2":0.3}'
```
(Use testnet addresses from a faucet if needed)

**Step 3:** Sign and broadcast:
```bash
bitcoin-cli -testnet signrawtransactionwithkey <hex> '[]'
bitcoin-cli -testnet sendrawtransaction <signed_hex>
```

**Step 4:** Inspect your own transaction:
```bash
bitcoin-cli -testnet getrawtransaction <txid> true
```

**Step 5:** Analyze the JSON output. Document:
- Which output is likely change? (Hint: check address reuse, value size, position)
- What does the version field (`vin[0].sequence`) tell you about locktime usage?
- Are you using RBF (Opt-In Replace-By-Fee)? How does this leak timing?

**Step 6:** Open **Sparrow Wallet** (https://sparrowwallet.com):
- Go to Tools → Transaction and paste your transaction hex
- Read Sparrow's privacy assessment
- Does it agree with your analysis? Where do you disagree?

**Step 7:** Create a comparison spreadsheet:

| Transaction Property | Leaks Information? | Why / Why Not |
|---|---|---|
| Number of inputs | ? | More inputs = higher UTXO consolidation |
| Sequence numbers | ? | Indicates RBF capability, locktime |
| Output amounts | ? | Round numbers vs. random amounts |
| Output ordering | ? | Change address patterns |
| Script type (P2PKH vs P2WPKH) | ? | Wallet fingerprinting |

**Step 8:** Read the Sparrow analysis feature documentation and write pseudocode for a privacy scoring algorithm:
```
transaction_privacy_score = 100
IF (num_inputs > 1):
  score -= 10  // Input merging reveals owned addresses
IF (output[largest].index == last):
  score -= 15  // Change address at end (predictable)
IF (output[i].is_round_number):
  score -= 5   // Round numbers = likely payment (not change)
RETURN score
```

### Open a PR This Week

**Contribute to Sparrow Wallet or BTCPay Server**

1. Visit https://github.com/sparrowwallet/sparrow or https://github.com/btcpayserver/btcpayserver
2. Look for issues tagged `privacy` or `enhancement`
3. Choose one of:
   - Improve transaction privacy scoring (add new heuristics)
   - Implement fee-amount randomization (reduce timing leaks)
   - Add a "Privacy Report" feature that explains each output's role
   - Create educational tooltips explaining privacy implications of transaction structure
4. Fork, code, and submit PR with test cases
5. Link your PR in Phase 1 final submission

**Alternative:** Contribute to Sparrow documentation:
1. Go to https://github.com/sparrowwallet/sparrow/tree/master/docs
2. Write a "Transaction Privacy Analysis Guide" (1000+ words)
3. Include real transaction examples and explanations
4. Submit as a Markdown file PR

### Daily Life Privacy Tip

**Check the "Privacy" tab in Sparrow before signing any transaction.**

Every time you're about to broadcast a payment:
1. In Sparrow, click the transaction you're about to send
2. Click the "Privacy" tab (or hover over the privacy icon)
3. Read the warnings
4. If you see "Change address pattern detected" or "Address reuse," stop and adjust:
   - Use a new change address (generate fresh)
   - Consider breaking the payment into smaller transactions
   - Or accept the privacy leak consciously (sometimes necessary for small payments)

This 10-second review prevents you from accidentally merging addresses or creating obvious change patterns that chain analysis expects.

### Reading List with Links

1. **"The Privacy Implications of Bitcoin Transaction Structure" — Bitcoin Optech**  
   https://bitcoinops.org/en/newsletters/2022/04/06/#spend-patterns-and-privacy
   - Technical deep-dive on input/output analysis

2. **Sparrow Wallet Privacy Features Documentation**  
   https://www.sparrowwallet.com/docs/transactions.html
   - Complete guide to transaction inspection and privacy scoring

3. **"UTXO Management: A Practical Guide" — Bitcoin Magazine**  
   https://bitcoinmagazine.com/articles/utxo-management-a-practical-guide
   - Real-world examples of privacy-preserving transaction patterns

4. **mempool.space Transaction Explorer Guide**  
   https://mempool.space/docs/faq
   - Learn to read transaction data from the block explorer

5. **"Coin Mixing Explained" — Wasabi Wallet Blog**  
   https://blog.wasabiwallet.io/coinjoin/
   - Context for why alternative transaction patterns exist

6. **Bitcoin Core Transaction API Reference**  
   https://developer.bitcoin.org/reference/rpc/getrawtransaction.html
   - Complete reference for decoderawtransaction and related commands

---

## Session 3: UTXO Management & Coin Selection

### Real-World Scenario

**The Consolidation Problem**  
You've received Bitcoin from three different sources: $100 from a friend, $200 from a CoinBase withdrawal, $150 from a client payment. You're storing them separately because you know that merging them creates a transaction that says "one person owns all three." But now you want to buy a $300 laptop. If you select all three UTXOs for the payment, you've just linked your friend, your exchange, and your business income in a single transaction. If you select only the friend and client coins, you leave a separate CoinBase UTXO that makes you a target for exchange surveillance. There's no perfect move. The answer is understanding **coin selection**: which UTXOs minimize privacy leaks for this specific transaction?

### Learning Objectives

By the end of Session 3, you will:
- Understand how coin selection strategies affect privacy
- Use Sparrow Wallet's coin control feature to manually select UTXOs
- Implement Bitcoin Core's coin selection algorithm (BnB, Knapsack, First-Fit)
- Recognize the privacy trade-offs of different selection strategies
- Build a UTXO management strategy for your personal or business Bitcoin use

### Privacy Tools You'll Use

- **Sparrow Wallet** — Coin control interface with visual UTXO management
- **Bitcoin Core** — Coin selection algorithms (`selectcoins`, `fundrawtransaction`)
- **BTCPay Server** — UTXO selection for merchant payments
- **OXT.me** — Analyzing historical coin selection patterns
- **bitcoin-cli** — Programmatic coin selection

### Hands-On Exercise: "Engineer the Optimal Spend"

**Step 1:** Open Sparrow Wallet and create a test wallet (testnet or mainnet view-only):
- Go to Wallet → Settings → Advanced
- Enable "Coin Control" mode
- You'll now see individual UTXOs instead of a combined balance

**Step 2:** Simulate three UTXOs (you can use real ones if testing on testnet):
- Create fictional labels: "Friend Gift (0.05 BTC)", "Exchange (0.2 BTC)", "Client Payment (0.15 BTC)"
- Document their addresses and age

**Step 3:** Scenario: You need to send 0.22 BTC to a merchant. Choose your coin selection:

**Option A: Select Friend + Client (0.2 BTC)**  
- Need to add more to cover 0.22 BTC requirement—force selection of Exchange UTXO too
- Privacy cost: Links all three sources
- Fee benefit: Single transaction, lower total fees

**Option B: Select only Exchange (0.2 BTC) + Friend (0.05 BTC)**  
- Exactly covers 0.22 BTC, minimal change
- Privacy benefit: Keeps client payment separate
- Cost: Merchant learns you've linked exchange + friend

**Option C: Send two separate transactions**  
- First: 0.2 BTC from Exchange
- Second: 0.02 BTC from Client, 0.0 BTC change = exact amount
- Privacy benefit: No linking in a single transaction
- Cost: Double fees (2 transactions instead of 1)

**Step 4:** In Sparrow, select each UTXO and observe:
```
Right-click UTXO → "Select for Send" or "Deselect"
```

**Step 5:** For each option above, simulate the transaction:
- Check Sparrow's privacy score for the resulting transaction
- Record: fee impact, privacy score, UTXO links created

**Step 6:** Read the Bitcoin Core documentation:
```bash
bitcoin-cli help selectcoins
bitcoin-cli help fundrawtransaction
```

**Step 7:** Understand BnB (Branch-and-Bound) coin selection:
```
Goal: Select UTXOs that minimize "change" 
Algorithm:
  1. Sort UTXOs by size
  2. Try combinations that sum as close as possible to target
  3. Minimize change = less on-chain evidence of coin selection
```

Write pseudocode for BnB:
```
target = payment_amount + estimated_fee
best_combination = None
best_waste = INFINITY

FOR each combination of UTXOs:
  sum = total_of_combination
  IF (sum >= target):
    waste = sum - target
    IF (waste < best_waste):
      best_waste = waste
      best_combination = combination

RETURN best_combination
```

**Step 8:** Create a UTXO Management Policy spreadsheet for yourself:

| Source | Address | Amount | Age | Privacy Risk | Selection Rule |
|---|---|---|---|---|---|
| Friend Gift | addr1 | 0.05 | 3 mo | Low | Only merge with other gift sources |
| Exchange (KYC) | addr2 | 0.2 | 6 mo | High | Isolate, minimize merge |
| Client Payment | addr3 | 0.15 | 1 mo | Medium | Separate from Exchange |

**Rule Set:** "For any spend under 0.1 BTC, use only Friend UTXOs. For larger spends, use Client + Friend if sum is sufficient, only merge with Exchange if unavoidable and spend amount is already de-anonymized."

### Open a PR This Week

**Contribute to Bitcoin Core or BTCPay Server**

1. Visit https://github.com/bitcoin/bitcoin (coin selection) or https://github.com/btcpayserver/btcpayserver (merchant coin selection)
2. Look for coin selection issues or enhancements tagged `privacy`
3. Choose one of:
   - Implement a privacy-aware coin selection algorithm (prefer older UTXOs to avoid timing leaks)
   - Add documentation to coin selection logic with privacy implications
   - Create test cases for coin selection with mixed UTXO ages
   - Implement "privacy mode" in BTCPay that minimizes UTXO merging
4. Submit PR with tests and documentation
5. Link in Phase 1 final submission

**Alternative:** Contribute to Sparrow:
1. Go to https://github.com/sparrowwallet/sparrow
2. File or pick an issue related to coin control UI improvements
3. Implement: "Privacy warning when merging KYC + non-KYC UTXOs"
4. Submit PR

### Daily Life Privacy Tip

**Label every UTXO in Sparrow with its source and risk level.**

In Sparrow Wallet, every UTXO you receive should be immediately labeled:
- "KYC: CoinBase" (high risk, minimize merging)
- "Peer: Alice" (low risk, safe to merge)
- "Inherited: Unknown" (medium risk, keep isolated)

When you spend, look at your UTXO list and consciously select coins that minimize linking. This takes 30 seconds per transaction and prevents you from accidentally revealing your entire financial graph.

### Reading List with Links

1. **"Coin Selection and Wallet Fingerprinting" — Bitcoin Optech**  
   https://bitcoinops.org/en/newsletters/2022/10/05/#coin-selection-for-privacy
   - Technical analysis of coin selection privacy implications

2. **Bitcoin Core Coin Selection Implementation**  
   https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.cpp
   - Source code comments explaining the algorithms

3. **"UTXO Consolidation: When and Why" — Blockstream Blog**  
   https://blockstream.com/2017/12/12/utxo-consolidation/
   - Strategic guide to managing UTXO sets

4. **Sparrow Coin Control Guide**  
   https://www.sparrowwallet.com/docs/wallets.html#coin-control
   - Complete visual walkthrough of coin selection

5. **"Branch-and-Bound Coin Selection" — Bitcoin Core Docs**  
   https://github.com/bitcoin/bitcoin/blob/master/src/wallet/coinselection.h
   - Algorithm documentation and rationale

6. **BTCPay Server UTXO Selection**  
   https://docs.btcpayserver.org/features/payouts/#coin-selection
   - Merchant-focused coin selection strategies

---

## Session 4: Wallet Fingerprinting

### Real-World Scenario

**The Fingerprint That Revealed Everything**  
A Bitcoin analyst notices a pattern: transactions from a podcast host always use P2WPKH-nested-in-P2SH outputs (SegWit v0), always have exactly 3 inputs and 2 outputs, and always pay to Blockstream's BTCPay Server address (which is public). The analyst cross-references transaction patterns with podcast sponsors, donation amounts, and announcement timing. Within weeks, they've mapped the host's entire funding structure without ever knowing the hosting wallet's seed phrase. The host thought they were using multiple wallets, but each one had a unique fingerprint. The lesson: **every wallet implementation leaks information through its transaction structure**. Different wallets default to different script types, fee strategies, and output ordering. This is "wallet fingerprinting."

### Learning Objectives

By the end of Session 4, you will:
- Recognize wallet fingerprints from transaction patterns
- Understand why different wallets produce different signatures
- Compare privacy characteristics of major wallet implementations
- Choose a wallet based on privacy criteria, not just features
- Analyze a transaction and identify the likely wallet software that created it

### Privacy Tools You'll Use

- **Sparrow Wallet** — View-only wallet inspector with script type analysis
- **Electrum** — Check legacy vs. modern output formats
- **Bitcoin Core** — Full node with raw transaction inspection
- **BlueWallet** — Mobile wallet with different fingerprints
- **Cake Wallet** — Privacy-focused mobile option
- **mempool.space** — Visualizing transaction patterns
- **OXT.me** — Clustering and fingerprinting analysis

### Hands-On Exercise: "Identify the Wallet"

**Part 1: Understand Script Types (and Why They Matter)**

Different wallets default to different address types:
- P2PKH (1...) — Legacy, most obvious script type, high fingerprinting risk
- P2SH (3...) — Can hide script type, but SegWit-in-P2SH has unique signatures
- P2WPKH (bc1q...) — Native SegWit, most common modern format
- P2TR (bc1p...) — Taproot, newest, becomes more common yearly

**Step 1:** Go to mempool.space and find a recent transaction with mixed input/output script types:
- Example: a transaction with both P2PKH and P2WPKH inputs
- Screenshot it and annotate: which input type is legacy? which is modern?

**Step 2:** Search https://bitcoin.stackexchange.com for "wallet fingerprint" and read 2-3 top answers:
- Understand why Electrum has a recognizable fingerprint
- Note: "coin selection algorithm differences create patterns"

**Part 2: Hands-On Wallet Comparison**

**Step 3:** Collect transaction examples from four wallets (use testnet or view transactions from analysis):

| Wallet | Example Tx | Input Type | Output Type | Fee Strategy | Change Pattern |
|---|---|---|---|---|---|
| Bitcoin Core | ? | ? | ? | ? | ? |
| Sparrow | ? | ? | ? | ? | ? |
| Electrum | ? | ? | ? | ? | ? |
| BlueWallet | ? | ? | ? | ? | ? |

**Step 4:** Analyze each wallet's characteristics:

For **Bitcoin Core** transactions:
```bash
bitcoin-cli getrawtransaction <txid> true
```
- Look at `vin[].scriptSig` lengths
- Note `vout[].scriptPubKey.type` values
- Observe fee calculation: do outputs have specific patterns?

For **Sparrow** transactions:
- Check address descriptor format
- Note: Sparrow can intentionally randomize output order to obscure change
- Check if all inputs are same script type (characteristic fingerprint)

For **Electrum** transactions:
- Older versions have predictable change address patterns
- Search for Electrum's coin selection algorithm on GitHub
- Note: Electrum's specific fee behavior

For **BlueWallet / Cake Wallet** transactions:
- Mobile wallets often have less randomization
- Check if transaction structure is consistent wallet-to-wallet

**Step 5:** Create a fingerprinting checklist:

```
WALLET FINGERPRINTING CHECKLIST:

Transaction observed: <txid>

Input analysis:
  [ ] All same script type? (Bitcoin Core often does this)
  [ ] Coin selection follows age pattern? (Electrum sometimes does)
  [ ] Inputs ordered in specific way? (Some wallets sort, others don't)

Output analysis:
  [ ] Change address is largest output? (Legacy fingerprint)
  [ ] Change address is last output? (Common default)
  [ ] Outputs in sorted order? (Bech32 sorting indicates Bitcoin Core)

Fee analysis:
  [ ] Is fee round number (0.0001 BTC)? (Indicates simple strategy)
  [ ] Fee proportional to size? (Indicates rate-based calculation)

Script type analysis:
  [ ] P2PKH only (very old wallet)
  [ ] P2SH mixed (potentially modern Electrum)
  [ ] P2WPKH (native SegWit, most common)
  [ ] P2TR (Taproot, Bitcoin Core 24+, Sparrow 1.7+)

Confidence: ___/10 (How confident are you this is [Wallet X]?)
```

**Step 6:** Find three real Bitcoin transactions (mainnet, public addresses):
1. One you believe is Bitcoin Core
2. One you believe is Electrum or Sparrow
3. One you believe is a mobile wallet (BlueWallet, Cake, etc.)

Document your analysis for each. Include:
- Screenshot of the transaction
- Fingerprinting analysis (check list above)
- Your conclusion and confidence level

**Step 7:** Write a brief "Privacy Ranking" of the four wallets you studied:

```
PRIVACY SCORE (1-10):

Bitcoin Core: ___ 
  Pros: Can customize everything, randomizes output order
  Cons: Large fee variance = timing leak, script type flexibility
  Ideal for: Power users who want full control

Sparrow: ___
  Pros: Excellent coin control, output order randomization, full transparency
  Cons: Desktop-only, requires setup
  Ideal for: Privacy-conscious developers

Electrum: ___
  Pros: Established, recoverable seed phrases
  Cons: Older versions have predictable patterns, legacy fingerprint
  Ideal for: Users who prioritize recovery, willing to accept some fingerprinting

BlueWallet / Cake: ___
  Pros: Mobile convenience, some support for newer features
  Cons: Less control, less randomization, cloud connectivity risks
  Ideal for: Mobile-first users, accepting some privacy trade-offs
```

### Open a PR This Week

**Contribute to Wallet Fingerprinting Research or Implementation**

1. Visit https://github.com/bitcoin/bitcoin (wallet fingerprinting in output sorting)
   OR https://github.com/sparrowwallet/sparrow (output randomization features)
2. Pick one of:
   - Improve output sorting randomization in Bitcoin Core (reduce fingerprinting)
   - Add wallet fingerprinting documentation to Bitcoin Core
   - Implement "Anonymity Score" feature in Sparrow that warns of wallet-specific patterns
   - Create test cases that verify output randomization is working correctly
3. Research existing PRs:
   - Bitcoin Core #24308 (output randomization)
   - Sparrow (look for "privacy" or "fingerprint" labels)
4. Submit your PR with clear privacy rationale

**Alternative:** Contribute to wallet fingerprinting research:
1. Fork https://github.com/bitcoinops/bitcoinops.github.io
2. Add a new entry to the "Wallet Privacy Comparison" section
3. Document real transaction examples for each wallet type
4. Submit PR with anonymized transaction analysis

### Daily Life Privacy Tip

**Use Sparrow Wallet and enable output randomization for all transactions.**

Sparrow Wallet intentionally randomizes the order of transaction outputs to prevent analysts from assuming "last output is change." Additionally:

1. In Sparrow, go to Preferences → Transactions
2. Enable "Randomize outputs" (if available in your version)
3. Set script type preference to the newest you support (P2WPKH or P2TR)
4. For critical privacy transactions, use Bitcoin Core directly with `bitcoind` so you control every detail

This prevents your wallet software from creating a recognizable fingerprint that ties together your transactions over time.

### Reading List with Links

1. **"Wallet Fingerprinting: Identifying Software from Blockchain Transactions"**  
   https://en.bitcoin.it/wiki/Weaknesses#Wallet_fingerprinting
   - Bitcoin wiki reference on fingerprinting techniques

2. **Bitcoin Core Output Sorting (BIP69)**  
   https://github.com/bitcoin/bitcoin/pull/24308
   - Discussion of output randomization in Bitcoin Core

3. **"The Privacy Implications of Wallet Software" — Bitcoin Optech**  
   https://bitcoinops.org/en/newsletters/2022/06/15/#analyzing-wallet-privacy
   - Analysis of different wallet implementations

4. **Sparrow Wallet Privacy Documentation**  
   https://www.sparrowwallet.com/docs/privacy.html
   - Complete guide to Sparrow's privacy features

5. **Electrum Blockchain Transaction Patterns**  
   https://github.com/spesmilo/electrum/blob/master/electrum/coinselection.py
   - Source code for Electrum's coin selection (affects fingerprinting)

6. **"Linkability Attacks in Bitcoin" — Monero Research Lab**  
   https://www.monerooutreach.org/
   - Cross-chain analysis techniques relevant to wallet fingerprinting

7. **BlueWallet and Cake Wallet Comparison**  
   https://www.sparrowwallet.com/docs/wallets.html#wallet-comparison
   - Feature and privacy matrix comparing wallet implementations

---

## Phase 1 Capstone Project

### Your Mission

Submit a **privacy audit** of your own Bitcoin wallet or a publicly documented transaction:

1. **Identify the UTXO sources** (KYC exchange, peer-to-peer trade, inheritance, etc.)
2. **Analyze the transaction structure** (inputs, outputs, script types, fees)
3. **Determine the likely wallet** (fingerprinting analysis)
4. **Rate the privacy leaks** (1-10 scale, with justification)
5. **Propose improvements** (alternative transaction structure, wallet selection, coin selection strategy)
6. **Submit as a GitHub PR** to the Bitcoin Privacy Institute curriculum repo

### Deliverables

- [ ] Write a 1500+ word privacy audit document
- [ ] Include at least 5 screenshots (transactions, analysis tools, fingerprinting evidence)
- [ ] Reference Session 1-4 concepts explicitly
- [ ] Propose 3 specific changes to improve privacy
- [ ] Create a PR to a Bitcoin wallet or analysis tool repository (link in your submission)
- [ ] Be honest: if there are privacy leaks in your own wallet, acknowledge them and explain why you accept the trade-off

---

## Getting Help

- **Bitcoin Privacy Institute Discord:** [link]
- **Bitcoin Optech Newsletter:** https://bitcoinops.org/en/newsletters/
- **Sparrow Wallet Documentation:** https://www.sparrowwallet.com/docs/
- **Bitcoin Core RPC Reference:** https://developer.bitcoin.org/reference/rpc/
- **OXT.me Tutorials:** https://oxt.me/guide

---

## What's Next?

After completing Phase 1 (Foundations), advance to **Phase 2: Silent Payments** where you'll implement BIP352 senders, understand scanning algorithms, and contribute to production Bitcoin privacy infrastructure.

**Phase 2 Preview:** Building a Silent Payments address generator, implementing the sender protocol, and deploying privacy solutions for real-world use cases (donations, merchant payments, client invoicing).
