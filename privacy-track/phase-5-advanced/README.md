# Phase 5: Advanced Techniques in Bitcoin Privacy
## Sessions 17-20

This phase moves beyond basics into production-grade privacy tools. You'll master CoinJoin, learn emerging techniques like CoinSwap, explore federated eCash, and build real-world Lightning privacy awareness. By the end, you'll understand every major privacy technique and be able to choose the right tool for the right scenario.

---

## Session 17: CoinJoin — WabiSabi, JoinMarket, Collaborative Transactions

### Real-World Scenario

You bought 0.5 BTC on Coinbase with full KYC. Your ID is linked to that Bitcoin address. Now you want to buy coffee at a merchant who doesn't trust chain analysis. If you spend your KYC Bitcoin directly, Coinbase will know you bought coffee. Their compliance team could even flag the merchant.

A CoinJoin transaction pools your coins with 50 other participants. The transaction has 51 identical 0.01 BTC outputs. Nobody — not Coinbase, not the chain analyst, not the merchant — can prove which output is "yours." The link between your identity and your future spending is broken.

**This is how real people reclaim their privacy.**

### Learning Objectives

- Understand the WabiSabi protocol and how it improves on Wasabi v1.0
- Analyze CoinJoin transactions to quantify anonymity (Anonset)
- Execute a practical CoinJoin in Wasabi Wallet
- Recognize the strengths and limitations of CoinJoin as a privacy tool
- Configure JoinMarket for yield farming while maintaining privacy

### Privacy Tools You'll Use

- **Wasabi Wallet** (WabiSabi CoinJoin coordinator)
- **Sparrow Wallet** (UTXO management, coin control, CoinJoin prep)
- **JoinMarket** (market-based mixing, liquidity provider)
- **OXT.me** (on-chain CoinJoin analysis)
- **Stratum mining pool analyzer** (to understand output clustering)

### Detailed Hands-On Exercise

#### Part 1: Execute a Real CoinJoin in Wasabi (60 minutes)

1. **Install & fund Wasabi Wallet**
   - Download Wasabi Wallet from wasabiwallet.io
   - Verify GPG signature (learn why this matters for privacy software)
   - Create a new wallet with a 12-word seed
   - Fund it with 0.01 BTC from a public testnet faucet (we'll use testnet for safety)
   - Wait for 6 confirmations

2. **Prepare for CoinJoin**
   - In Wasabi's Coins tab, label your UTXO: "KYC input from exchange"
   - Enable coin control (Settings > Mix > Advanced)
   - Review the current Wasabi coordinator fee (typically 0.3%)
   - Check the current waiting queue (how many transactions ahead of you?)

3. **Initiate the CoinJoin**
   - Select your coin in the Coins tab
   - Click "Enqueue"
   - Wasabi begins searching for mixing partners
   - Watch the transaction build in real-time (or come back in 10-60 minutes)
   - **Key learning:** The mixing output is derived using Wasabi's output selection algorithm. This is intentional — round outputs (0.01, 0.03, 0.1) make it harder to fingerprint which output is "yours"

4. **Analyze the CoinJoin Output**
   - Once mixed, open the transaction on OXT.me
   - Count the total number of outputs
   - Identify the equal-denomination outputs (the anonymity set)
   - Calculate your anonset: How many outputs could yours be?
   - Check the change output (Wasabi sends change to a new address for privacy)
   - **Question to answer:** If outputs are 0.01 BTC and your input was 0.5 BTC, what does that tell a chain analyst?

5. **Document the Round**
   - Wasabi tracks your round in the transaction history
   - Screenshot: the round confirmation
   - Screenshot: the anonset achieved
   - Write a 200-word summary: "What privacy did this transaction give me?"

#### Part 2: Analyze a Real Mainnet CoinJoin (90 minutes)

1. **Pick a live Wasabi CoinJoin from mainnet**
   - Visit OXT.me > CoinJoin Coordinators
   - Find a recent Wasabi transaction (look for WabiSabi in the protocol field)
   - Example: Search txid on OXT.me (an actual Wasabi transaction)

2. **Trace the transaction**
   - Identify all inputs (who's mixing?)
   - Count outputs and find the equal-denomination cluster
   - Use OXT.me's "Merge Fields" detector to identify change outputs
   - **Challenge:** Can you identify which output might be the change? (Hint: Often slightly smaller or sent immediately to another address)

3. **Calculate Anonset**
   - Count equal-denomination outputs: `N`
   - This is your **forward anonset** — when you spend, how many outputs could yours be?
   - Now follow one of those outputs: if it was CoinJoined again, multiply the anonsets
   - This is your **heuristic anonset** — accounting for multiple rounds

4. **Identify Clustering Attacks**
   - Which outputs were spent within 24 hours? (suggests urgency, might leak timing info)
   - Which outputs were sent to the same merchant (identifies the requester)
   - Did outputs go to exchange deposit addresses? (leaked identity)
   - Write down: "This transaction leaked privacy because..."

#### Part 3: Set Up JoinMarket as a Yield Farmer (120 minutes)

1. **Install JoinMarket**
   - Clone the repo: `git clone https://github.com/joinmarket-org/joinmarket-clientserver.git`
   - Follow installation for your OS
   - Initialize the wallet: `python3 wallet-tool.py generate`
   - Save your seed phrase securely

2. **Fund and Configure**
   - Fund with 0.05 BTC (small amount for learning)
   - Wait for 6 confirmations
   - Create a new Yield Generator mode config
   - Set conservative fee: 0.0005 BTC per join
   - Set mix depth to 5 (changes address for each join)

3. **Start Yield Generating**
   - Launch the yield generator: `python3 yield-generator.py`
   - Monitor the logs as other users pay you to mix with them
   - **Learn:** You're being paid to provide liquidity. Earn sats while mixing others' coins
   - Run for at least 1 hour, monitor earnings

4. **Analyze Your Yields**
   - Export transaction history
   - Calculate: "How much sats did I earn? How many joins did I participate in?"
   - Calculate: "If I earn 10,000 sats/month, what's my effective hourly rate?"
   - **Trade-off analysis:** You earned privacy (your coins mixed) AND sats. But you locked capital. Was it worth it?

### Real-World Exercise: Read the WabiSabi Paper

1. Read the core sections of "WabiSabi: Centrally Coordinated CoinJoin with Variable Amounts" (arXiv:2202.12951)
2. Focus on: Protocol overview, Zero-Knowledge Proofs section, Input/output alignment
3. Answer: "Why does WabiSabi allow variable-amount inputs, unlike Wasabi v1.0?"
4. Answer: "What prevents the coordinator from stealing funds?"

### Open a PR This Week

**Choose one:**

1. **Wasabi Wallet Documentation**
   - Repo: `zkSNACKs/WalletWasabi`
   - Contribute: Add a "Privacy Tutorial: Your First CoinJoin" section to the docs
   - Target: Real-world guide for non-technical users

2. **OXT.me Analysis Tool**
   - Repo: `graymauser/opschain-ox` or similar chain analysis projects
   - Contribute: Add an "Anonset Calculator" tool that auto-computes forward/heuristic anonset
   - Target: Python script, or JavaScript widget

3. **JoinMarket Configuration Guide**
   - Repo: `joinmarket-org/joinmarket-clientserver`
   - Contribute: Add privacy-focused configuration examples (conservative fees, optimal mix depth)
   - Target: Wiki update with 5+ config scenarios for different user types

### Daily Life Privacy Tip

**If you have KYC Bitcoin, your first spending action should be a CoinJoin.**

Here's the minimal version:
1. Create a new Wasabi Wallet (or Sparrow with CoinJoin support)
2. Send your KYC Bitcoin to a fresh Wasabi address
3. Enqueue for CoinJoin (Wasabi handles the rest)
4. Once mixed, spend the output (the merchant has no link to your KYC identity)

Time investment: ~30 minutes. Cost: ~0.3% fee. Privacy gain: You broke the identity-to-spending link.

### Reading List

1. **WabiSabi Protocol** (Academic)
   - "WabiSabi: Centrally Coordinated CoinJoin with Variable Amounts"
   - arXiv: https://arxiv.org/pdf/2202.12951
   - Focus: Protocol mechanics, ZK proofs

2. **Wasabi Wallet Docs** (Practical)
   - https://docs.wasabiwallet.io/using-wasabi/CoinJoin.html
   - Real-world configuration and walkthrough

3. **JoinMarket Docs** (Advanced)
   - https://joinmarket.readthedocs.io/
   - Yield generation, market dynamics

4. **OXT.me Analysis Tool** (Data)
   - https://oxt.me/
   - Live CoinJoin observation, on-chain metrics

---

## Session 18: CoinSwap & Atomic Swaps for Privacy

### Real-World Scenario

You're a merchant who receives customer payments on-chain. But you don't want anyone knowing how much Bitcoin you have. CoinJoin shows a clear pattern: 51 identical outputs, obviously a mixing round.

CoinSwap is different. You swap coins with another Bitcoin user, 1-to-1, in a series of smart contract-like transactions. From the outside, it looks like a normal Bitcoin transaction. No obvious pattern. No anonymity set. The blockchain observer has no idea what happened.

**This is stealth privacy — it looks like nothing at all.**

### Learning Objectives

- Understand the CoinSwap protocol and how it differs from CoinJoin
- Learn why CoinSwap transactions are indistinguishable from normal payments
- Trace a CoinSwap step-by-step (theory)
- Understand Atomic Swaps and their privacy implications
- Recognize when CoinSwap or Atomic Swaps are the right tool

### Privacy Tools You'll Use

- **Teleport Transactions** (proposed CoinSwap implementation)
- **citadel-tech/coinswap** (experimental reference implementation)
- **atomic-swap-tools** (for cross-chain learning)
- **Paper and diagram tools** (to understand the protocol without executing)

### Detailed Hands-On Exercise

#### Part 1: Read & Understand the CoinSwap Specification (120 minutes)

1. **Read the CoinSwap BIP draft**
   - Original proposal: CoinSwap concept by Chris Belcher
   - Current repo: `citadel-tech/coinswap`
   - Read: The protocol overview and multi-transaction flow
   - **Key sections:** Why CoinSwap is better than CoinJoin for privacy, the maker/taker model, Hash time-locked contracts

2. **Draw a CoinSwap on Paper**
   - You and Alice want to swap coins
   - You have 1 BTC at address A
   - Alice has 1 BTC at address B
   - Draw the transaction sequence (setup, broadcast, settlement phases)
   - **Question:** Can a chain analyst tell that you and Alice swapped? What would they see?

3. **Compare: CoinJoin vs CoinSwap**
   - CoinJoin: 51 inputs, 51 equal outputs (obvious pattern)
   - CoinSwap: 1 input, 1 output each (looks normal)
   - Create a comparison table covering blockchain pattern, anonymity set, speed, coordination, capital required
   - **Conclusion:** When would YOU choose CoinSwap?

#### Part 2: Trace a Simulated CoinSwap (90 minutes)

1. **Build a theoretical CoinSwap scenario**
   - You: 0.5 BTC at address `1Alice...` (KYC from exchange)
   - Maker: 0.5 BTC at address `1Maker...` (unknown identity)
   - Create 4 addresses for yourself: setup, swap, redeem, final
   - Create 4 addresses for Maker

2. **Trace the transaction flow**
   - Tx1: You send 0.5 BTC to setup (locked contract, Maker can't spend)
   - Tx2: Maker sends 0.5 BTC to setup (locked contract, you can't spend)
   - Tx3: You spend Maker's output to redeem
   - Tx4: Maker spends your output to final
   - Result: You now control Maker's output, Maker controls your output
   - **Privacy consequence:** The address has no obvious connection to your redeemed output

3. **Attempt a clustering attack**
   - You're a chain analyst looking at the addresses
   - Can you connect them to one entity?
   - Check: Does any output get spent to a KYC exchange deposit?
   - Check: Do the addresses re-spend within 1 hour?
   - **Finding:** Even on paper, CoinSwap is much harder to trace than CoinJoin

#### Part 3: Understand Atomic Swaps (60 minutes)

1. **Read: How Atomic Swaps Work (Cross-Chain)**
   - Atomic Swap = CoinSwap across blockchains
   - Example: You swap Bitcoin for Monero 1-to-1
   - The same hash-timelock mechanism works

2. **Privacy Implications**
   - Atomic Swaps to Monero break the Bitcoin-to-identity link completely
   - Once you're in Monero, privacy is automatic
   - Downside: Requires trusted exchange infrastructure

3. **Security Analysis**
   - If an atomic swap partially completes, what happens?
   - Answer: Hash time-locked contracts force both parties to complete or both refund
   - This is the security property that makes CoinSwap work

### Real-World Exercise: Propose a CoinSwap Market

Design (on paper) a peer-to-peer CoinSwap market:
1. How do makers advertise their swap offers?
2. How do takers find matches?
3. What happens if one party doesn't complete?
4. How is pricing set?
5. Can it be done without a centralized coordinator?

Write a 500-word proposal.

### Open a PR This Week

**Choose one:**

1. **citadel-tech/coinswap**
   - Contribute: Improve documentation or add a "CoinSwap for Bitcoin Privacy" guide
   - Target: Make the protocol understandable to developers

2. **Bitcoin Privacy Research**
   - Contribute: Write a comparative analysis: "CoinSwap vs CoinJoin: When to Use Each"
   - Target: Published analysis document

3. **Atomic Swap Reference Implementation**
   - Contribute to: `comit-network/comit-rs` or similar atomic swap projects
   - Target: Documentation or example scenarios

### Daily Life Privacy Tip

**If you want invisible privacy, CoinSwap is better than CoinJoin — but you need a swap partner.**

Reality check: CoinSwap is still experimental. For today:
1. Use CoinJoin (Wasabi) for your routine privacy
2. Watch CoinSwap development (citadel-tech/coinswap on GitHub)
3. If a trusted CoinSwap service launches, try it for a second privacy layer

### Reading List

1. **CoinSwap Protocol**
   - Chris Belcher's original proposal: https://bitcointalk.org/index.php?topic=321228.0
   - citadel-tech coinswap repo: https://github.com/citadeltech/coinswap

2. **Scriptless Scripts & Hash Time-Locked Contracts**
   - "Scriptless Scripts via Discrete Log Contracts" — Poelstra
   - https://github.com/ElementsProject/scriptless-scripts

3. **Atomic Swaps**
   - "Atomic Swaps: Cross-Chain Transactions" — Tier Nolan, 2013

---

## Session 19: eCash — Fedimint & Cashu for Privacy-Preserving Communities

### Real-World Scenario

Bitcoin House Bali is a community hub where 50 people work and spend Bitcoin daily. But every transaction is public on-chain. They don't want the Indonesian government seeing exactly who paid whom for food, coworking, or events.

Solution: The community runs a Fedimint federation. Members deposit Bitcoin once. They receive eCash tokens (blind coins). When two members transact, they swap eCash tokens. The Bitcoin stays locked on-chain. The Fedimint federation cannot see who paid whom — the blind signatures ensure mathematical privacy.

**This is institutional privacy: Bitcoin goes in, perfect privacy comes out.**

### Learning Objectives

- Understand Fedimint architecture: guardians, federations, eCash protocols
- Learn blind signatures and why they provide mathematical privacy
- Execute a Cashu mint locally and issue/redeem tokens
- Understand the trade-offs: trust vs. privacy
- Design a real-world eCash federation for a community

### Privacy Tools You'll Use

- **Fedimint** (production federation framework)
- **Cashu** (lightweight eCash protocol, in development)
- **Fedi app** (mobile eCash wallet)
- **Blind Signature Libraries** (cryptographic primitives)
- **Docker** (to run a local test federation)

### Detailed Hands-On Exercise

#### Part 1: Understand Blind Signatures (90 minutes)

1. **Read the theory**
   - Blind Signature concept: Created by David Chaum (1983)
   - How it works: User blinds a message, server signs it blindly, user unblinds
   - Privacy property: Server learns nothing about the message it signed
   - Resource: Read "Blind Signatures for Untraceable Payments" — Chaum, 1983

2. **Implement a toy blind signature scheme**
   - Use Python or JavaScript
   - Create a simple example: RSA blind signatures
   - Code outline showing message blinding, blind signing, and unblinding
   - **Key insight:** The server signed something, but couldn't see what it signed

3. **Answer the privacy question**
   - If I deposit 1 BTC and receive blind-signed eCash tokens, can the server track my spending?
   - Answer: No. The server can verify the signature is valid, but doesn't know which token is yours
   - Compare: Bitcoin (all transactions public) vs eCash (all transactions private to federation)

#### Part 2: Deploy a Local Cashu Mint (120 minutes)

1. **Install Cashu (nutshell implementation)**
   - Clone: `git clone https://github.com/cashubtc/nutshell.git`
   - Install dependencies: `pip install -r requirements.txt`
   - Start a mint server: `python -m nutshell.mint`

2. **Create eCash Tokens**
   - Use a Cashu client to request tokens
   - Request: 0.01 BTC in eCash
   - The mint creates blind signatures for your tokens
   - You receive a token string

3. **Transfer Tokens (Peer-to-Peer)**
   - You and a partner use the same Cashu mint
   - You want to send them 0.005 BTC (eCash)
   - You: Send the token string to them
   - Partner: Redeem the token at the mint
   - Mint: Verifies and marks the token as spent
   - **Key privacy win:** No blockchain record. The mint can't tell who transferred to whom

4. **Redeem eCash Back to Bitcoin**
   - Redeem 0.005 BTC of eCash at the mint
   - The mint sends Bitcoin to your address
   - Check: The Bitcoin transaction is on-chain, but earlier privacy transactions were invisible

5. **Analyze the Privacy Leakage**
   - When you redeem eCash to Bitcoin, you provide an on-chain address
   - This reveals: "Someone redeemed X BTC"
   - But earlier transactions are private
   - **Design question:** How would you minimize this leakage?

#### Part 3: Design a Fedimint Federation for Your Community (120 minutes)

1. **Fedimint Architecture Overview**
   - Guardians: N trusted people
   - Consensus: Guardians must agree on Bitcoin deposits (3-of-5 multisig)
   - eCash: Users deposit Bitcoin, receive eCash tokens
   - Privacy: No guardian individually sees all transactions

2. **Design Your Federation**
   - Community: Choose 20-50 people
   - Guardians: Select 5-7 trusted leaders
   - Multisig: 3-of-5 consensus model
   - Deposit, spending, and redemption processes

3. **Governance Document**
   - Create a "Fedimint Governance Charter" for your community
   - Cover: Guardian selection, succession plan, multisig threshold, transaction limits, dispute resolution, mint expiration
   - Write 500-750 words

4. **Trust vs. Privacy Trade-off Analysis**
   - Create a comparison table: Bitcoin On-Chain vs Cashu vs Fedimint
   - Cover: Privacy, trust required, redemption risk, ease of use
   - Conclusion: Write 200 words on when each is appropriate

### Real-World Exercise: Interview a Fedimint Guardian

If possible, contact someone running a Fedimint federation. Ask:
1. How many users do you have?
2. What's the total Bitcoin in the federation?
3. How do you prevent double-spending of eCash?
4. What's the redemption process like?
5. Have you had any privacy breaches?

Synthesize their answers into a case study (500 words).

### Open a PR This Week

**Choose one:**

1. **Fedimint Documentation**
   - Repo: `fedimint/fedimint`
   - Contribute: Add "Setting Up Your First Federation: A Community Guide"
   - Target: Tutorial for non-technical communities

2. **Cashu Protocol Improvements**
   - Repo: `cashubtc/nutshell`
   - Contribute: Documentation, test cases, or privacy analysis
   - Target: Help stabilize the Cashu protocol

3. **eCash Privacy Analysis**
   - Publish a blog post analyzing: "Fedimint Privacy Properties"
   - Target: Compare to CoinJoin, CoinSwap, and native Bitcoin

### Daily Life Privacy Tip

**If your community is Bitcoin-native, run a Fedimint federation.**

Simple path:
1. Identify 5-7 trusted people in your community
2. Run Fedimint together
3. Members deposit Bitcoin, receive eCash
4. All internal transactions are invisible
5. Bitcoin stays locked on-chain, fully secured

Cost: Time to set up + server hosting
Privacy gain: Perfect privacy for community transactions

### Reading List

1. **Blind Signatures & eCash**
   - "Blind Signatures for Untraceable Payments" — David Chaum
   - https://chaum.com/blind-signatures/

2. **Fedimint Protocol**
   - https://github.com/fedimint/fedimint
   - https://fedimint.org/

3. **Cashu Protocol**
   - https://github.com/cashubtc/cashu
   - https://github.com/cashubtc/cashu/blob/main/docs/00-overview.md

4. **Fedi App (Mobile eCash Wallet)**
   - https://fedi.xyz/

---

## Session 20: Lightning Network Privacy — BOLT12, Blinded Paths & Channel Probing

### Real-World Scenario

You're a merchant using Lightning Network for instant payments. Every time a customer pays you, your node's public key appears in the transaction. Analyzing many Lightning payments, a chain analyst could map your payment graph and understand your transaction volume, which addresses you receive from, and even physical location.

BOLT12 (Offers with Blinded Paths) solves this: Instead of giving your node ID, you share a "blinded offer." The payer can't see your node's actual identity. They route through blinded paths. Result: Your node remains unknown.

**This is Lightning privacy: Instant payments, invisible sender and receiver.**

### Learning Objectives

- Understand BOLT12 offers and why they improve on BOLT11 invoices
- Learn blinded paths and how they hide node identities
- Execute a BOLT12 offer with blinded paths
- Analyze what information a payer can and cannot learn
- Recognize Lightning privacy risks (channel probing, flow analysis)
- Implement channel probing defenses

### Privacy Tools You'll Use

- **Core Lightning** (BOLT12 native support)
- **LDK** (Lightning Development Kit, BOLT12 in development)
- **Phoenix Wallet** (blinded paths support)
- **Eclair** (potential BOLT12 support)
- **Lightning Network Analyzer Tools** (to understand graph structure)

### Detailed Hands-On Exercise

#### Part 1: Understand BOLT12 vs BOLT11 (90 minutes)

1. **Review BOLT11 (Classic Invoices)**
   - Format: Static invoice with node ID, amount, expiry
   - Example: `lnbc100n1p0...` contains your node's identity
   - Privacy problem: Every invoice reveals your node ID
   - Reuse problem: Same invoice can be paid multiple times

2. **Learn BOLT12 (Offers with Privacy)**
   - Format: Non-specific offer with blinded path
   - Example: Offer encodes "I accept payments via blinded path X"
   - Privacy property: Payer doesn't see your actual node ID
   - Flexibility: Offers can be static (used many times) or one-time

3. **Compare in a Table**
   - Feature comparison: Node ID exposed, Multiple payments, Reusability, Payer knowledge, Implementation status
   - Clear privacy advantages of BOLT12

4. **Read the BOLT12 Specification**
   - https://github.com/lightning/bolts/blob/master/12-offer.md
   - Focus: Offer format, blinded path construction, privacy properties
   - Answer: Why can't a payer learn your node ID even if they want to?

#### Part 2: Create and Use a BOLT12 Offer (120 minutes)

**Note:** This exercise requires Core Lightning running. Use testnet or a local Lightning network simulator.

1. **Set Up Core Lightning**
   - Install: https://github.com/ElementsProject/lightning
   - Start a node: `lightningd --testnet --dev-fast-gossip`
   - Verify: `lightning-cli getinfo` shows your node ID

2. **Create a BOLT12 Offer**
   - Command: `lightning-cli offer <amount_in_msats> <description>`
   - Example: `lightning-cli offer 1000000msat "Coffee"`
   - Output: A `bolt12://` string with a blinded path embedded

3. **Share the Offer (Without Revealing Identity)**
   - Give the offer string to a friend (simulated payer)
   - Their Lightning wallet decodes the offer
   - They can pay without knowing your actual node ID

4. **Analyze What the Payer Sees**
   - Payer receives: `bolt12://...`
   - Payer learns: A way to send you money, amount, description
   - Payer does NOT learn: Your node ID, location, real identity
   - **Question:** How is this different from BOLT11?

5. **Send a Payment (Payer Perspective)**
   - Create a second node (payer)
   - Use the BOLT12 offer to create an invoice
   - Command: `lightning-cli pay <offer>`
   - The payment routes through blinded paths
   - Neither sender nor receiver knows each other's exact node identity

6. **Verify Privacy**
   - Check the payment in your node's database
   - Check the payer's node: `lightning-cli listinvoices`
   - Compare: What information is visible on each side?
   - **Finding:** The payment succeeded, but the graph structure remains private

#### Part 3: Understand Blinded Paths (90 minutes)

1. **Blinded Path Concept**
   - A path from a public node to your node, encrypted so intermediate nodes can't see the destination
   - Format: `[node1 (encrypted→2), node2 (encrypted→3), node3 (encrypted→4), you]`
   - Intermediate node 2 knows node 3, but not nodes 4 or 5
   - Result: Nobody except you knows the full path to you

2. **Trace a Blinded Path**
   - Create a 3-node blinded path manually:
     - Alice (public) → Bob (intermediate) → Charlie (intermediate) → You (recipient)
   - Alice sends payment using the blinded path
   - Bob sees: Payment destined for an encrypted value, forwards to Charlie
   - You see: Payment arrived, recognize the blinded path as yours
   - **Key insight:** No intermediate node sees the full path

3. **Compare to Source Routing**
   - Classic Lightning: Sender specifies the full path
   - Everyone on the path knows the full structure
   - Blinded paths: Sender only sees the first hop, rest is encrypted
   - Privacy improvement: Intermediate hops don't map the graph

#### Part 4: Detect and Defend Against Channel Probing (90 minutes)

1. **Understand Channel Probing Attack**
   - Attacker sends small test payments to map your network topology
   - Each test reveals: "Is this channel funded? How much? Who is the node?"
   - Attacker can identify: Your channels, capacity, balance (approximately)
   - **Risk:** An attacker could identify you as a merchant if your channel balances spike

2. **Implement Probing Detection**
   - Core Lightning has built-in defenses
   - Enable: Accept channel probes but don't leak balance information
   - Configure: `accept-htlc-underpaying-msat` to reject obviously fake payments

3. **Create a Probing Detection Script**
   - Monitor your Lightning node's failed HTLCs
   - Pattern: Many small failed payments from the same node = likely probing
   - Action: Block the probing node in your firewall rules

4. **Privacy Best Practices for Lightning**
   - Use BOLT12 instead of BOLT11 for merchant invoices
   - Rebalance channels over Tor to hide IP address
   - Don't advertise channel capacity
   - Rotate node aliases
   - Document and share: "Lightning Privacy Checklist"

### Real-World Exercise: Map a Lightning Network Community

1. Use a Lightning network analyzer (e.g., Amboss, 1ML)
2. Identify a merchant or hub in your region
3. Map their channels, capacity, and payment flow
4. Write: "Here's what privacy leaks I can identify"
5. Propose: "Here's how they could improve privacy with BOLT12"

### Open a PR This Week

**Choose one:**

1. **Core Lightning BOLT12 Documentation**
   - Repo: `ElementsProject/lightning`
   - Contribute: Tutorial on BOLT12 for merchants
   - Target: Step-by-step guide with examples

2. **LDK BOLT12 Implementation**
   - Repo: `lightningdevkit/rust-lightning`
   - Contribute: Documentation, test cases, or examples
   - Target: Help stabilize BOLT12 in LDK

3. **Lightning Privacy Scorecard**
   - Repo: Create new or contribute to `1ML` or Lightning analysis tools
   - Contribute: A privacy analysis tool that scores nodes on BOLT12 usage, IP privacy, etc.
   - Target: Help the Lightning community improve privacy

### Daily Life Privacy Tip

**If you receive Lightning payments as a merchant, use BOLT12 offers.**

Simple steps:
1. Update Core Lightning or switch to a BOLT12-supporting wallet
2. Create a BOLT12 offer: `lightning-cli offer <amount> "My Business"`
3. Share the offer code (not your node ID)
4. Customers pay the offer; their wallet handles blinded paths
5. You receive payments invisibly

Privacy gain: Customers can't map your Lightning topology.

### Reading List

1. **BOLT12 Specification**
   - https://github.com/lightning/bolts/blob/master/12-offer.md

2. **Core Lightning BOLT12 Guide**
   - https://docs.corelightning.org/docs/offers

3. **LDK BOLT12 Progress**
   - https://github.com/lightningdevkit/rust-lightning

4. **Blinded Paths Technical Details**
   - "Route Blinding" in Lightning Network documentation
   - https://github.com/lightning/bolts/pull/999

5. **Lightning Privacy Research**
   - "Echoes of Silence: Analyzing Light Client Privacy on Bitcoin"

6. **1ML Lightning Network Analysis**
   - https://1ml.com

---

## Phase 5 Capstone: Privacy Technique Comparison

By the end of Phase 5, you understand:
- **CoinJoin:** Obvious on-chain pattern, strong anonymity set, fast, centralized coordination
- **CoinSwap:** Invisible on-chain pattern, stealth, slow, P2P market-based
- **eCash (Fedimint/Cashu):** Perfect privacy with trusted federation, off-chain, requires deposit/redemption
- **Lightning (BOLT12):** Instant, on-chain settlement, node-level privacy, real-time

**Your challenge:** Design a full privacy architecture for a Bitcoin user's complete financial life:
- Accumulate Bitcoin (private initial purchase)
- Store Bitcoin (multisig, geographically distributed)
- Spend Bitcoin (at merchants, for privacy)
- Receive Bitcoin (payments from friends)
- Exchange Bitcoin (to fiat or other assets)

Write a 1000-word "Privacy Architecture" proposal that uses techniques from Sessions 17-20 appropriately. Explain your choices.

---

## How to Excel in Phase 5

1. **Read the specifications**, not just the summaries
2. **Run the tools** — hands-on execution teaches more than reading
3. **Contribute code** — you don't just learn; you ship
4. **Ask questions** — privacy is complex; engage with the community
5. **Think about trade-offs** — privacy is never free; understand what you're trading

Your future work in Bitcoin privacy depends on mastering these techniques. Make Phase 5 count.
