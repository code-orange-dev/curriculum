# Phase 6: Building & Contributing to Bitcoin Privacy
## Sessions 21-24

This phase shifts from learning to shipping. You'll build production-grade tools, contribute real code to major Bitcoin privacy projects, and deliver a capstone that demonstrates mastery. By the end, you'll have shipped code, contributed to the privacy ecosystem, and be ready for advanced fellowship work.

---

## Session 21: Privacy-Preserving Wallet Development with BDK

### Real-World Scenario

You're building a wallet app for Bitcoin users who care about privacy. BDK (Bitcoin Development Kit) handles the hard parts: blockchain communication, UTXO selection, transaction building. But BDK is just a library. YOU must design it for privacy:

- No address reuse (each payment gets a fresh address)
- Taproot-only (P2TR outputs hide script details)
- Coin control mandatory (users choose which coins to spend)
- No coin consolidation (don't merge UTXOs unless necessary)

Your wallet is the difference between private and exposed Bitcoin.

**This is wallet-level privacy engineering.**

### Learning Objectives

- Understand BDK's coin selection algorithm and how to customize it for privacy
- Design a wallet architecture that enforces privacy best practices
- Implement Taproot-only outputs (P2TR)
- Build a functional coin control UI
- Integrate change management for privacy
- Contribute production-grade code to BDK ecosystem

### Privacy Tools You'll Use

- **BDK** (Rust Bitcoin Development Kit)
- **bdk-cli** (command-line testing)
- **Sparrow Wallet** (reference implementation to study)
- **Test networks** (signet, testnet)
- **Bitcoin Core** (full node backend)

### Detailed Hands-On Exercise

#### Part 1: Design Your Privacy Wallet Architecture (90 minutes)

1. **Study Sparrow Wallet**
   - Download and run Sparrow Wallet
   - Create a test wallet (testnet)
   - Examine: How it displays UTXOs
   - Examine: Coin control interface
   - Examine: Change address handling
   - Document: What privacy features does Sparrow implement?

2. **Read the BDK Documentation**
   - https://docs.rs/bdk/latest/bdk/
   - Focus: Wallet struct, coin selection, transaction building
   - Understand: How BDK selects coins by default
   - Understand: How to override coin selection

3. **Design Your Privacy Wallet**
   - Create a requirements document:
     - Mandatory features: P2TR only, no address reuse, coin control UI
     - Privacy properties: No consolidation heuristics, no round amounts
     - UX: Simple for users, powerful for privacy-conscious users
   - Draw: Wallet architecture diagram (key management, change, UTXOs, transaction building)

4. **Privacy Requirements Checklist**
   - Address reuse: Never. Each payment = new address
   - Script types: Taproot (P2TR) only. No P2WPKH, no P2SH
   - Coin control: User must select which UTXOs to spend
   - Change: To a new address, never back to payment address
   - Amounts: No rounding. Exact amounts to preserve privacy
   - Fee selection: Avoid amounts that leak round values
   - Document: Why each requirement matters

#### Part 2: Implement a Privacy-First Wallet Skeleton in Rust with BDK (180 minutes)

1. **Set Up Your Rust Project**
   ```bash
   cargo new privacy_wallet
   cd privacy_wallet
   cargo add bdk bdk-sqlite bdk-electrum tokio serde
   ```

2. **Create the Core Wallet Structure**
   ```rust
   use bdk::{Wallet, blockchain::ElectrumBlockchain};
   use bdk::database::sqlite::SqliteDatabase;
   
   pub struct PrivacyWallet {
       // Private key management
       // UTXO tracking
       // Change address generation
       // Transaction builder
   }
   
   impl PrivacyWallet {
       pub fn new(extended_private_key: String, network: Network) -> Result<Self> {
           // Initialize wallet with Taproot descriptor
           // Set up SQLite database
           // Connect to blockchain
       }
       
       pub fn get_utxos(&self) -> Vec<UTXO> {
           // Return all available UTXOs with metadata
       }
       
       pub fn create_transaction(
           &self,
           recipient: Address,
           amount: u64,
           selected_utxos: Vec<UTXO>,
       ) -> Result<Transaction> {
           // Build transaction with selected UTXOs
           // Generate new change address
           // Validate privacy properties
       }
   }
   ```

3. **Implement Mandatory Privacy Features**
   
   a. **Address Derivation (No Reuse)**
   ```rust
   pub fn generate_payment_address(&mut self) -> Address {
       // Use BIP32 to derive next address
       // Store derivation index
       // Never reuse the same index
       // Return fresh Taproot address
   }
   ```
   
   b. **Taproot-Only Descriptors**
   ```rust
   // Force all descriptors to be P2TR (Taproot)
   let descriptor = "tr([...])"; // Taproot descriptor
   // Reject any non-Taproot descriptors at wallet creation
   ```
   
   c. **Coin Control Implementation**
   ```rust
   pub fn create_transaction_with_coin_control(
       &self,
       recipient: Address,
       amount: u64,
       selected_utxo_ids: Vec<OutPoint>, // User selects which UTXOs to spend
   ) -> Result<Transaction> {
       // Verify user selection
       // Build transaction with ONLY selected UTXOs
       // Don't add "better" UTXOs automatically
       // Return transaction with selected coins
   }
   ```
   
   d. **Change Address Management**
   ```rust
   pub fn get_change_address(&mut self) -> Address {
       // Generate a new, never-before-used address for change
       // Use BIP32 derivation (different path from payment addresses)
       // Store metadata: "this is change from tx_id"
       // Return address that won't leak user privacy
   }
   ```

4. **Build the Transaction Manager**
   ```rust
   pub struct TransactionBuilder {
       wallet: &PrivacyWallet,
   }
   
   impl TransactionBuilder {
       pub fn with_recipient(mut self, addr: Address, amount: u64) -> Self {
           self.recipient = Some(addr);
           self.amount = amount;
           self
       }
       
       pub fn with_utxos(mut self, utxos: Vec<UTXO>) -> Self {
           self.selected_utxos = utxos;
           self
       }
       
       pub fn with_fee_rate(mut self, sats_per_vb: f32) -> Self {
           self.fee_rate = sats_per_vb;
           self
       }
       
       pub fn build(self) -> Result<Transaction> {
           // 1. Validate all UTXOs are Taproot
           // 2. Calculate total input value
           // 3. Estimate transaction size
           // 4. Calculate fee
           // 5. Generate change address
           // 6. Build transaction
           // 7. Verify: inputs + change = outputs + fee
       }
   }
   ```

5. **Add Privacy Validation**
   ```rust
   pub fn validate_privacy(&self, tx: &Transaction) -> Result<()> {
       // Check 1: All outputs are P2TR or P2WSH
       // Check 2: Change address is fresh (never used)
       // Check 3: No obvious patterns in amounts
       // Check 4: Fee rate is reasonable (not suspiciously low or high)
       // Check 5: No address reuse detected
       return Ok(());
   }
   ```

6. **Write Tests**
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;
       
       #[test]
       fn test_address_never_reused() {
           // Generate 10 addresses
           // Verify all are unique
       }
       
       #[test]
       fn test_taproot_only() {
           // Create transaction
           // Verify all outputs are Taproot
       }
       
       #[test]
       fn test_coin_control_respected() {
           // Select specific UTXOs
           // Verify ONLY those UTXOs are spent
       }
       
       #[test]
       fn test_change_address_fresh() {
           // Create multiple transactions
           // Verify each uses a new change address
       }
   }
   ```

#### Part 3: Test on Testnet (90 minutes)

1. **Set Up a Testnet Environment**
   - Create a testnet wallet
   - Fund it with testnet Bitcoin (faucet)
   - Wait for confirmations

2. **Execute Privacy Transactions**
   - Create a transaction with coin control
   - Specify exact UTXOs to spend
   - Set custom fee rate
   - Broadcast to testnet
   - Monitor on blockchain explorer

3. **Analyze Your Transactions**
   - Open blockchair.com or mempool.space
   - Search your transaction
   - Verify: All outputs are Taproot (no visible script type)
   - Verify: Change address is fresh
   - Verify: No obvious consolidation pattern

4. **Document Your Implementation**
   - Write a README for your wallet
   - Include: Architecture diagram, privacy properties, coin control guide
   - Publish to GitHub

### Real-World Exercise: Contribute to BDK

1. **Fork the BDK Repository**
   - https://github.com/bitcoindevkit/bdk
   - Clone locally

2. **Choose a Contribution**
   - Option 1: Add a privacy-focused coin selection example
   - Option 2: Improve documentation for Taproot wallet setup
   - Option 3: Write a privacy best practices guide for wallet developers

3. **Create a Pull Request**
   - Reference your privacy wallet implementation
   - Explain the privacy improvements
   - Include tests and examples

### Open a PR This Week

**Choose one:**

1. **BDK Example: Privacy Wallet**
   - Repo: `bitcoindevkit/bdk`
   - Contribute: A complete example showing privacy-first wallet design
   - Target: `examples/privacy_wallet.rs` demonstrating all best practices

2. **Sparrow Wallet Documentation**
   - Repo: `sparrowwallet/sparrow`
   - Contribute: "Privacy Configuration Guide" for Sparrow users
   - Target: Help users understand and use coin control effectively

3. **Your Own Privacy Wallet**
   - Repo: Create `your-github/privacy-wallet`
   - Contribute: Full working wallet implementation
   - Target: Open-source reference for developers

### Daily Life Privacy Tip

**When choosing a wallet, ask: Does it support coin control?**

If yes: You can choose which UTXOs to spend. You have privacy power.
If no: The wallet chooses for you (often poorly). You have no privacy.

Action today:
1. Open Sparrow Wallet
2. Load a test wallet
3. Go to Transactions tab
4. Try selecting specific UTXOs to spend
5. Notice how coin control changes the transaction

### Reading List

1. **BDK Documentation**
   - https://docs.rs/bdk/
   - Focus: Wallet, blockchain, transaction building

2. **Sparrow Wallet Privacy Guide**
   - https://www.sparrowwallet.com/docs/
   - Study their coin control implementation

3. **Bitcoin Script Types**
   - "Taproot Guide" — https://bitcoinops.org/en/topics/taproot/
   - Why Taproot is better for privacy

4. **BIP32 Derivation**
   - "Hierarchical Deterministic Wallets" — BIP32
   - Understanding address generation

5. **Coin Selection Algorithms**
   - "Change Avoidance & Consolidation" — privacy trade-offs

---

## Session 22: Building a Privacy Testing Tool

### Real-World Scenario

You receive Bitcoin at 10 different addresses. How private is your transaction history? A privacy scoring tool can analyze your address and give you a score:

- Have you ever reused an address? (Privacy leak: -20 points)
- Do you consolidate UTXOs regularly? (Privacy leak: -15 points)
- Do you use round amounts (0.1, 1.0, 10.0)? (Heuristic leak: -10 points)
- Do you mix script types (P2WPKH + P2TR)? (Fingerprint leak: -5 points)
- Have you used more than 3 entities? (Cluster leak: -10 points)

Score: 40/100. Privacy: "Compromised. Improve by: Using CoinJoin, enabling coin control, avoiding consolidation."

**This is privacy feedback that drives behavior change.**

### Learning Objectives

- Design a privacy scoring algorithm (10+ metrics)
- Implement on-chain analysis to detect privacy leaks
- Build a web or CLI tool that scores Bitcoin addresses
- Understand the heuristics chain analysts use
- Create a user-friendly privacy report
- Contribute to the privacy tools ecosystem

### Privacy Tools You'll Use

- **Blockchain APIs** (Blockchair, blockchain.com, Mempool.space)
- **Python** (data analysis and tool building)
- **Flask or FastAPI** (web server, optional)
- **Matplotlib** (visualization)
- **GitHub** (open-source publishing)

### Detailed Hands-On Exercise

#### Part 1: Design a Privacy Scoring Framework (120 minutes)

1. **Define 10 Privacy Metrics**
   
   Metric 1: **Address Reuse Detection**
   - Score: -20 points if address has been reused
   - Implementation: Check if address appears in multiple transactions as a recipient
   - Privacy impact: High. Reuse is a major heuristic.
   
   Metric 2: **Consolidation Pattern**
   - Score: -15 points if address consolidates many small UTXOs into one
   - Implementation: Detect transactions with 5+ inputs and 1 output
   - Privacy impact: High. Screams "wallet consolidation"
   
   Metric 3: **Change Detection**
   - Score: -10 points if change address can be identified
   - Implementation: Detect outputs smaller than others (usually change)
   - Privacy impact: Medium. Leaks transaction flow.
   
   Metric 4: **Round Amounts**
   - Score: -8 points per transaction with round amounts (0.1, 1.0, 10.0)
   - Implementation: Detect outputs that are exact powers of 10 in satoshis
   - Privacy impact: Medium. Suggests merchant, not random spending
   
   Metric 5: **Script Type Mixing**
   - Score: -5 points if mixing P2PKH, P2WPKH, P2WSH, P2TR
   - Implementation: Analyze all outputs, detect heterogeneity
   - Privacy impact: Medium. Identifies wallet software
   
   Metric 6: **Timing Pattern**
   - Score: -5 points if transactions cluster at specific times (9am daily)
   - Implementation: Analyze transaction timestamps for periodicity
   - Privacy impact: Low-Medium. Suggests automated payments
   
   Metric 7: **Dust Attack Vulnerability**
   - Score: -3 points if address receives many tiny UTXOs (dust)
   - Implementation: Count UTXOs < 5000 satoshis
   - Privacy impact: Low. Indicates potential dust attack target
   
   Metric 8: **Entity Clustering**
   - Score: -10 points per identified entity
   - Implementation: Heuristic clustering (common inputs, change detection)
   - Privacy impact: High. Maps who you transact with
   
   Metric 9: **CoinJoin Participation**
   - Score: +20 points if address has been in a CoinJoin
   - Implementation: Detect CoinJoin patterns (51+ equal outputs)
   - Privacy impact: High positive. Shows privacy-conscious behavior
   
   Metric 10: **Age and Activity**
   - Score: +5 points if address is older than 1 year
   - Implementation: Analyze first transaction date
   - Privacy impact: Medium. Older addresses tend to be more obscure

2. **Design the Report Format**
   ```
   Privacy Score: 42/100
   
   Critical Issues (Fix First):
   - Address reused 3 times (-20 points)
   - Heavy consolidation detected (-15 points)
   
   Warnings (Improve):
   - Round amounts used in 2 transactions (-8 points)
   - Script type mixing (P2WPKH + P2TR) (-5 points)
   
   Positives:
   - Participated in CoinJoin (+20 points)
   - No dust attack vulnerability (+0 points)
   
   Recommendations:
   1. Stop reusing addresses immediately
   2. Use CoinJoin before spending to mix history
   3. Enable coin control to avoid consolidation
   4. Diversify script types to avoid fingerprinting
   ```

#### Part 2: Implement the Privacy Scorer (Python) (150 minutes)

1. **Set Up Your Python Project**
   ```bash
   mkdir privacy_scorer
   cd privacy_scorer
   python3 -m venv venv
   source venv/bin/activate
   pip install requests pandas matplotlib
   ```

2. **Create the Core Analyzer**
   ```python
   import requests
   from collections import defaultdict
   
   class PrivacyAnalyzer:
       def __init__(self, address):
           self.address = address
           self.api_key = "your_blockchair_key"
           self.transactions = []
           self.score = 0
           self.metrics = {}
       
       def fetch_transactions(self):
           # Fetch all transactions for this address
           # Use Blockchair API
           # Store in self.transactions
           pass
       
       def detect_address_reuse(self):
           # Check if address appears as recipient in multiple txs
           # Return count of reuses
           pass
       
       def detect_consolidation(self):
           # Find transactions with many inputs, few outputs
           # Return list of consolidation transactions
           pass
       
       def detect_change_address(self):
           # For each transaction, identify likely change output
           # Usually smallest output or sent to new address
           # Return probability of each output being change
           pass
       
       def detect_round_amounts(self):
           # Find outputs that are round amounts
           # 0.1 BTC, 1.0 BTC, 10.0 BTC, etc.
           # Return count and list
           pass
       
       def detect_script_mixing(self):
           # Analyze all outputs
           # Detect if using mixed script types
           # Return diversity score
           pass
       
       def detect_coinjoin_participation(self):
           # Look for transactions with 50+ equal outputs
           # Return list of CoinJoin transactions
           pass
       
       def analyze(self):
           # Run all analyses
           # Calculate total score
           # Generate report
           pass
   ```

3. **Calculate Privacy Score**
   ```python
   def calculate_score(self):
       total_score = 100
       
       # Metric 1: Address Reuse
       reuses = self.detect_address_reuse()
       if reuses > 0:
           total_score -= min(20, reuses * 5)
       self.metrics['address_reuse'] = reuses
       
       # Metric 2: Consolidation
       consolidations = self.detect_consolidation()
       if len(consolidations) > 0:
           total_score -= 15
       self.metrics['consolidation'] = len(consolidations)
       
       # Metric 3: Change Detection
       change_leaked = self.detect_change_address()
       if change_leaked > 0.7:  # High confidence change detection
           total_score -= 10
       self.metrics['change_leaked'] = change_leaked
       
       # ... continue for all 10 metrics
       
       self.score = max(0, total_score)
       return self.score
   ```

4. **Generate Privacy Report**
   ```python
   def generate_report(self):
       report = f"""
   Privacy Score: {self.score}/100
   
   Critical Issues:
   """
       if self.metrics['address_reuse'] > 0:
           report += f"- Address reused {self.metrics['address_reuse']} times\n"
       
       if self.metrics['consolidation'] > 0:
           report += f"- Heavy consolidation detected ({len(self.metrics['consolidation'])} instances)\n"
       
       report += "\nRecommendations:\n"
       report += "1. Use CoinJoin to mix your transaction history\n"
       report += "2. Enable coin control in your wallet\n"
       report += "3. Avoid consolidating UTXOs\n"
       report += "4. Use Taproot addresses (P2TR)\n"
       
       return report
   ```

#### Part 3: Build a Web Interface (Flask) (90 minutes)

1. **Create a Simple Web App**
   ```python
   from flask import Flask, render_template, request
   
   app = Flask(__name__)
   
   @app.route('/')
   def index():
       return render_template('index.html')
   
   @app.route('/analyze', methods=['POST'])
   def analyze():
       address = request.form['address']
       analyzer = PrivacyAnalyzer(address)
       analyzer.fetch_transactions()
       analyzer.analyze()
       
       return render_template('report.html', 
           score=analyzer.score,
           metrics=analyzer.metrics,
           report=analyzer.generate_report()
       )
   
   if __name__ == '__main__':
       app.run(debug=True)
   ```

2. **Create Simple HTML Templates**
   ```html
   <!-- index.html -->
   <form method="POST" action="/analyze">
       <label>Enter a Bitcoin address:</label>
       <input type="text" name="address" placeholder="1A1z7agoat...">
       <button type="submit">Analyze Privacy</button>
   </form>
   
   <!-- report.html -->
   <div class="score">Privacy Score: {{ score }}/100</div>
   <div class="metrics">
       {{ report|safe }}
   </div>
   <button>Download PDF Report</button>
   ```

#### Part 4: Test Your Tool (60 minutes)

1. **Test on Known Addresses**
   - Analyze a known merchant address (low privacy, high reuse)
   - Analyze a known CoinJoin output address (high privacy)
   - Analyze your own test address
   - Verify scores match expectations

2. **Validate Metrics**
   - Test address reuse detection
   - Test consolidation detection
   - Test CoinJoin pattern detection
   - Verify all calculations are correct

3. **Document Edge Cases**
   - What happens if address has no transactions?
   - What happens if address is very new?
   - What happens if address has 10,000+ transactions?

### Real-World Exercise: Analyze Real Bitcoin Addresses

1. **Find High-Privacy Addresses**
   - Search for CoinJoin outputs on OXT.me
   - Analyze the privacy score
   - Verify it's high

2. **Find Low-Privacy Addresses**
   - Search for merchant addresses (known address reuse)
   - Analyze the privacy score
   - Verify it's low

3. **Write Case Studies**
   - "Why Coinbase Deposit Addresses Score 10/100"
   - "Why CoinJoin Outputs Score 95/100"
   - "How to Improve Your Privacy Score from 20 to 80"

### Open a PR This Week

**Choose one:**

1. **Create a New GitHub Repository**
   - Repo: `your-github/bitcoin-privacy-scorer`
   - Contribute: Full working tool (Python + Flask)
   - Target: Open-source reference implementation, MIT license

2. **Contribute to Existing Privacy Tool**
   - Repo: Search "Bitcoin privacy" on GitHub
   - Contribute: Add a privacy scoring feature
   - Target: Help existing privacy tool communities

3. **Publish a Blog Post**
   - Title: "Privacy Scoring Framework for Bitcoin Addresses"
   - Explain: Your 10 metrics, how they work, what they mean
   - Include: Interactive examples, case studies
   - Target: Bitcoin Magazine, Nakamoto Institute, or personal blog

### Daily Life Privacy Tip

**Before spending Bitcoin, run it through a privacy scorer.**

Action:
1. Take one of your Bitcoin addresses
2. Use your privacy scorer tool (or my-balance.io if available)
3. Check your privacy score
4. If it's below 60, use CoinJoin before spending

### Reading List

1. **Privacy Heuristics**
   - "Chain Analysis 101" — Chainalysis blog
   - Understanding what analysts look for

2. **Consolidation and Change Detection**
   - https://oxt.me/
   - Real examples of privacy leaks

3. **CoinJoin Pattern Recognition**
   - "Identifying CoinJoin Transactions" — academic papers
   - How to detect mixing patterns

4. **Bitcoin Script Analysis**
   - "Address Types and Privacy" — bitcoinops.org

---

## Session 23: Contribution Sprint — Ship Code Together

### Real-World Scenario

You and 10 other developers are in a room. Eight Bitcoin privacy projects have open issues on the table:

- BDK: "Improve Taproot wallet examples"
- Core Lightning: "Improve BOLT12 documentation"
- Fedimint: "Add federation setup tutorial"
- Wasabi Wallet: "Improve UX for new CoinJoin users"
- JoinMarket: "Add configuration guide for privacy"
- Bitcoin Core: "Privacy review of transaction selection"
- LDK: "BOLT12 implementation examples"
- Cashu: "Improve blind signature documentation"

In 4 hours, your cohort will submit 5+ PRs. This is how open-source Bitcoin privacy gets built.

**This is the real work.**

### Learning Objectives

- Work collaboratively on real Bitcoin privacy repositories
- Merge-ready code in a production environment
- Experience code review and iteration
- Build relationships with Bitcoin privacy maintainers
- Ship impact in a single session
- Celebrate contributions with the cohort

### How This Session Works

1. **Morning (1 hour): Issue Selection & Pairing**
   - Facilitator presents 8+ open issues from privacy projects
   - Each participant picks an issue
   - Facilitator pairs people with expertise on mentorship

2. **Midday (2 hours): Deep Work**
   - Participants work heads-down
   - Facilitator and mentors available for questions
   - Goal: PR ready for submission

3. **Afternoon (1 hour): Live Code Review & Polish**
   - Each person presents their PR
   - Cohort gives feedback
   - Facilitator helps with final polish
   - Verify: Tests pass, documentation is clear, code is mergeable

4. **End of Session: Submit**
   - All PRs submitted to projects
   - Cohort celebrates together
   - Document the impact

### Open Issues to Target

**Pick one:**

1. **BDK: Taproot Wallet Example**
   - Repo: `bitcoindevkit/bdk`
   - Issue: Create a complete example showing privacy-first Taproot wallet
   - PR Target: `examples/privacy_taproot_wallet.rs`
   - Est. Time: 90-120 minutes
   - Impact: High. Teaches developers best practices

2. **Core Lightning: BOLT12 Tutorial**
   - Repo: `ElementsProject/lightning`
   - Issue: Write step-by-step BOLT12 guide for merchants
   - PR Target: `doc/BOLT12_GUIDE.md`
   - Est. Time: 60-90 minutes
   - Impact: High. Drives BOLT12 adoption

3. **Fedimint: Federation Setup Guide**
   - Repo: `fedimint/fedimint`
   - Issue: Create "Your First Federation" tutorial
   - PR Target: `docs/SETUP_GUIDE.md`
   - Est. Time: 90-120 minutes
   - Impact: High. Enables communities to self-host

4. **Wasabi Wallet: CoinJoin Onboarding**
   - Repo: `zkSNACKs/WalletWasabi`
   - Issue: Improve UX for first-time CoinJoin users
   - PR Target: UI improvements or documentation
   - Est. Time: 120-150 minutes
   - Impact: High. Better onboarding = more users

5. **JoinMarket: Privacy Configuration Guide**
   - Repo: `joinmarket-org/joinmarket-clientserver`
   - Issue: Create configuration guide for yield generators
   - PR Target: `docs/PRIVACY_CONFIG.md`
   - Est. Time: 60-90 minutes
   - Impact: Medium. Better market liquidity

6. **Bitcoin Core: Transaction Privacy**
   - Repo: `bitcoin/bitcoin`
   - Issue: Add privacy considerations to coin selection docs
   - PR Target: `doc/design/privacy.md`
   - Est. Time: 90 minutes
   - Impact: High. Influences Core development

7. **LDK: BOLT12 Implementation Examples**
   - Repo: `lightningdevkit/rust-lightning`
   - Issue: Create BOLT12 example for LDK users
   - PR Target: `lightning/examples/bolt12.rs`
   - Est. Time: 120 minutes
   - Impact: High. Enables developers to use BOLT12

8. **Cashu: Blind Signature Documentation**
   - Repo: `cashubtc/nutshell`
   - Issue: Improve blind signature protocol documentation
   - PR Target: `docs/BLIND_SIGNATURES.md`
   - Est. Time: 60 minutes
   - Impact: Medium. Teaches cryptography

### Working as a Cohort

**You're not alone. Here's how this works:**

- **Mentors available**: Real maintainers or experienced contributors
- **Code review loop**: Quick feedback, iterate, improve
- **Peer support**: Ask each other questions
- **Celebration**: Every PR counts. Every contribution matters.

### Success Criteria

- PR is submitted to the project's repository
- PR has clear description and rationale
- Code passes project's tests
- Documentation is clear and correct
- No obvious issues in code review

### Open a PR This Week

**You will submit a PR in this session.** No exceptions. The goal is 5+ PRs from your cohort.

### Daily Life Privacy Tip

**Contributing to Bitcoin privacy is how you level up faster than any tutorial.**

Real developers learn by shipping. Ship your first PR today.

### Reading List

1. **Bitcoin Open Source Contribution Workflow**
   - How to fork, branch, commit, and PR
   - Standard Git workflow

2. **Code Review Best Practices**
   - How to respond to feedback
   - How to iterate on PRs

3. **Bitcoin Development Standards**
   - Code style guides for major projects
   - Testing requirements

4. **License Compliance**
   - MIT, Apache, GPLv3 basics
   - How to respect copyright

---

## Session 24: Capstone — Present Your Work, Apply for Fellowship

### Real-World Scenario

You're standing in front of 20 Bitcoin developers, 5 privacy researchers, and OpenSats fellowship directors. You have 15 minutes.

"Here's what I built. Here are the 3 PRs I shipped. This is why Bitcoin privacy matters to me. This is how I'll contribute in the next 12 months."

If you nail this presentation, you walk out with:
- Recognition from the Bitcoin privacy community
- Connections to mentors and developers
- A fellowship offer (best-case scenario)
- A clear roadmap for the next year

**This is your moment.**

### Learning Objectives

- Communicate your work clearly and compellingly
- Tell the story of your privacy contributions
- Build relationships with Bitcoin privacy leaders
- Apply for advanced fellowships
- Plan your next 12 months of work
- Graduate as a Bitcoin privacy developer

### How the Session Works

1. **Morning (1 hour): Presentation Prep**
   - Each participant prepares a 15-minute talk
   - Topics: What you built, what you learned, what's next
   - Practice with feedback from facilitators

2. **Midday (1 hour): Guest Speakers**
   - Invited speakers from Bitcoin privacy community
   - Potential: josibake (protocol developer), Dan Gould (CoinJoin), 0xB10C (privacy researcher)
   - Topic: "Working in Bitcoin Privacy: Careers, Fellowship, Open Questions"

3. **Afternoon (2 hours): Cohort Presentations**
   - Each participant presents their work
   - 15 minutes talk + 5 minutes Q&A
   - Audience: Developers, researchers, fellowship directors
   - Recorded (with permission) for portfolio

4. **Evening: Fellowship Application Workshop**
   - Help participants apply for OpenSats fellowships
   - Review applications
   - Discuss next steps

### Your Capstone Presentation (15 minutes)

**Structure:**

1. **Opening (1 minute)**
   - "My name is X. I'm a Bitcoin privacy developer."
   - Why privacy matters to you

2. **What I Built (5 minutes)**
   - Phase 5-6 capstone project
   - Feature walkthrough
   - Live demo (if possible)

3. **Open Source Contributions (4 minutes)**
   - 3+ PRs you shipped
   - Links to repositories
   - What each PR achieved

4. **What I Learned (3 minutes)**
   - Top 3 insights from the Privacy Track
   - How thinking changed
   - What's still confusing

5. **Next 12 Months (2 minutes)**
   - Where you want to contribute
   - Specific projects in mind
   - How OpenSats fellowship would help

### Capstone Project Requirements

By Session 24, you must have:

1. **Built one complete project** (from Phase 5-6):
   - Privacy wallet with BDK
   - Privacy scoring tool
   - CoinJoin analysis tool
   - BOLT12 merchant setup
   - Fedimint federation setup
   - Or similar in scope and impact

2. **Shipped 3+ PRs** to major Bitcoin projects:
   - Wasabi, JoinMarket, Core Lightning, LDK, BDK, Bitcoin Core, Fedimint, Cashu
   - PRs must be real, merged (or actively in review)
   - Code you wrote, not just documentation

3. **Documented your work**:
   - GitHub repository with README
   - Blog post or write-up
   - Clear attribution to what you built

4. **Created a portfolio** showing:
   - Your capstone project
   - Links to your 3+ merged PRs
   - Your contributions to Bitcoin privacy
   - Your vision for the next 12 months

### Fellowship Application

**What you'll apply for:**

- **OpenSats Bitcoin Privacy Fellowship**
  - $40k/year (typical)
  - 12-month program
  - Mentorship from privacy experts
  - Access to Bitcoin Core, Lightning, privacy developer communities
  - Apply at: https://www.opensats.org/

**What reviewers look for:**

- Shipped code (PRs merged or in review)
- Clear communication about privacy problems
- Track record of contribution
- Passion and depth of knowledge
- Specific plans for 12 months
- Community endorsements (mentors, reviewers)

**Your application includes:**

- Capstone project (GitHub link)
- 3+ merged PRs (links)
- 500-word proposal: "My Work in Bitcoin Privacy"
- 3 references (facilitator, mentor, maintainer)
- 15-minute video presentation

### Guest Speakers

**Potential speakers from Bitcoin privacy community:**

- **josibake** (Protocol & CoinJoin)
  - Topic: "CoinJoin Protocol Design & Evolution"
- **Dan Gould** (CoinJoin + Markets)
  - Topic: "Building Market-Based Privacy Infrastructure"
- **0xB10C** (Privacy Analysis & Metrics)
  - Topic: "Measuring Privacy: Anonset, Metrics, and Heuristics"
- **Obi Nwosu** (Fedimint & eCash)
  - Topic: "Community Privacy: Fedimint for Self-Hosted Bitcoin"
- **Chris Belcher** (CoinSwap, JoinMarket)
  - Topic: "The Future of Bitcoin Privacy: CoinSwap and Beyond"

### Open a PR This Week

**No new PRs this week.** Focus on your presentation and application.

### Daily Life Privacy Tip

**Privacy is not a destination. It's a practice.**

As you graduate from this track:
1. Use CoinJoin on your Bitcoin every quarter
2. Enable coin control in your wallet
3. Never reuse addresses
4. Follow Bitcoin privacy research
5. Contribute back to the projects you use

### Reading List

1. **Bitcoin Privacy Philosophy**
   - "Bitcoin Privacy: Problems and Opportunities" — various authors
   - Why privacy matters

2. **OpenSats Fellowship Guidelines**
   - https://www.opensats.org/
   - What they look for

3. **Bitcoin Privacy Landscape**
   - Current state of privacy tools
   - Outstanding problems

4. **Career in Bitcoin Privacy**
   - Options: Protocol development, privacy tools, research, education
   - How to sustain yourself while contributing

---

## Phase 6 Capstone Presentation Checklist

Before you present, verify:

- Your capstone project works and is documented
- All 3+ PRs are real and verifiable
- Your presentation is under 15 minutes
- You have a live demo (or screenshots)
- Your slides are clear and professional
- You've practiced with feedback
- Your fellowship application is started
- You have 3 references lined up
- Your GitHub profile shows your work
- You're ready to answer tough questions

---

## Congratulations!

If you've completed Phases 1-6, you are now a Bitcoin privacy developer.

You understand:
- How chain analysis works (and how to resist it)
- Every major privacy technique (Silent Payments, PayJoin, CoinJoin, CoinSwap, eCash, Lightning)
- How to build privacy-preserving tools
- How to contribute to major Bitcoin projects
- How to think about privacy trade-offs

You've shipped code. You've contributed to open source. You've mastered the most important privacy techniques in Bitcoin.

The next step? Keep building. Keep contributing. Keep advancing Bitcoin privacy.

Welcome to the Bitcoin privacy developer community.

---

## Resources for Continued Learning

**After Phase 6:**

1. **Bitcoin Privacy Research Community**
   - Workshops at Bitcoin conferences
   - Privacy-focused hackathons
   - Academic papers and discussions

2. **Advanced Topics**
   - Multiparty computation (MPC)
   - Zero-knowledge proofs (ZKPs) for privacy
   - Advanced cryptography
   - Protocol design

3. **Maintainer Tracks**
   - After 12 months as a developer, consider becoming a maintainer
   - Maintain Wasabi, JoinMarket, or similar
   - Lead protocol development

4. **Teaching Track**
   - After 2 years, teach the next cohort
   - Become a Code Orange Faculty member
   - Expand Bitcoin privacy education

---

**The Bitcoin privacy movement needs you. Build great things.**
