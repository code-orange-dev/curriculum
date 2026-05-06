# Phase 3: Payjoin (BIP77/78) — Sessions 9-12

**Objective:** Master Payjoin as a protocol that defeats Common Input Ownership Heuristic (CIOH) by design, understand the full stack from specification to production deployment, and contribute to the Payjoin ecosystem.

**Why This Matters:** Payjoin is the most elegant privacy tool ever specified in Bitcoin. A single transaction can make a payment while looking like a self-transfer to all external observers. By the end of Phase 3, you'll understand how it works, build a complete sender/receiver implementation, deploy it in production, and contribute upstream.

---

## Session 9: BIP77/78 Theory — How Payjoin Defeats Chain Analysis

### Real-World Scenario

**The Problem:**
A merchant runs a small coffee shop and uses BTCPay Server to accept Bitcoin payments. Alice walks in, pays 0.5 BTC, and the transaction lands on-chain with two inputs:
- Input A: BTCPay merchant's hot wallet
- Input B: Alice's wallet

A chain analyst sees both inputs and applies CIOH: "Both inputs came from the same transaction, so they must belong to the same person." They conclude Alice now controls the merchant's address.

In reality, Alice just bought a coffee.

**The Solution:**
With Payjoin enabled on BTCPay, Alice's wallet proposes a payment. Before the merchant broadcasts it, the merchant adds their own input and changes the output destinations. The final transaction looks like:
- Input 1: Merchant's address
- Input 2: Alice's address (change gets routed back to Alice, not visible)
- Output 1: Merchant's new address
- Output 2: Looks like the merchant's change

Now CIOH breaks. The analyst sees two inputs and can't tell who paid whom. The output structure is indistinguishable from a self-transfer.

**The Privacy Win:**
Every Payjoin transaction creates ambiguity at scale. If 10% of transactions are Payjoins, the analyst can no longer trust CIOH at all.

### Learning Objectives

- Understand the Common Input Ownership Heuristic and why it fails in Payjoin
- Learn the BIP77 (Payjoin sender) and BIP78 (Payjoin receiver) specifications
- Explain how input and output substitution breaks heuristics
- Identify which wallets support Payjoin and when to use each
- Calculate the privacy gain of Payjoin vs. standard CoinJoin

### Privacy Tools You'll Use

- **BTCPay Server** (BIP78 receiver) — production-grade merchant payments
- **Bull Bitcoin Wallet** (BIP77 sender) — mobile Payjoin creation
- **Sparrow Wallet** (BIP77 sender) — desktop Payjoin with full control
- **Wasabi Wallet** (planned BIP78 support) — receiver support coming
- **Payjoin Dev Kit** — reference implementation
- **bitcoin-cli** — transaction inspection and debugging

### Detailed Hands-On Exercise

**Part 1: Understand the Protocol Flow**

1. **Download and read BIP77 and BIP78** from github.com/bitcoin/bips:
   - BIP77: Payjoin Sender
   - BIP78: Payjoin Receiver
   - Focus on sections 2-4 (Request Format, Response Handling, Examples)

2. **Trace a real Payjoin transaction** on-chain:
   - Go to mempool.space
   - Search for a transaction with the Payjoin flag (marked with orange "P" icon)
   - Examine its inputs and outputs
   - Try to determine the payment direction using only the on-chain data
   - Note: You can't. That's the point.

3. **Study the protocol exchange:**
   - Sender creates PSBT (Partially Signed Bitcoin Transaction)
   - Sender sends to receiver's Payjoin endpoint
   - Receiver adds their input
   - Receiver modifies outputs (adds their own, adjusts change)
   - Receiver signs their input and returns modified PSBT
   - Sender verifies, signs their input, broadcasts

4. **Document each step** in a markdown file with annotated diagrams showing sender/receiver interaction

**Part 2: Set Up a Local Payjoin Test**

1. **Start a local Bitcoin Core node** (regtest):
   ```bash
   bitcoind -regtest -server -rpcuser=admin -rpcpassword=password
   ```

2. **Generate 101 blocks** to have spendable UTXOs:
   ```bash
   bitcoin-cli -regtest generatetoaddress 101 $(bitcoin-cli -regtest getnewaddress)
   ```

3. **Create test wallets:**
   ```bash
   bitcoin-cli -regtest createwallet sender
   bitcoin-cli -regtest createwallet receiver
   ```

4. **Fund both wallets:**
   ```bash
   SENDER_ADDR=$(bitcoin-cli -regtest -rpcwallet=sender getnewaddress)
   RECEIVER_ADDR=$(bitcoin-cli -regtest -rpcwallet=receiver getnewaddress)

   bitcoin-cli -regtest generatetoaddress 1 $SENDER_ADDR
   bitcoin-cli -regtest generatetoaddress 1 $RECEIVER_ADDR
   ```

5. **Inspect a PSBT:**
   ```bash
   bitcoin-cli -regtest decodepsbt "$PSBT_HEX"
   ```
   - Identify inputs and outputs
   - Note the fee amount
   - Count required signatures

**Part 3: Compare Privacy Models**

Create a table showing:
- Standard payment: single input (sender), visible output (receiver)
- Coinjoin: many inputs, many outputs, extreme privacy, not practical for commerce
- Payjoin: two inputs (sender + receiver), outputs look like change, perfect for payments

Measure:
- Privacy per transaction
- User experience friction
- Real-world deployment status
- Network impact

### Open a PR This Week

**Target: payjoin/rust-payjoin**
- Repository: https://github.com/payjoin/rust-payjoin
- Difficulty: Start with documentation
  1. Read the README and examples
  2. Run the tests: `cargo test`
  3. Choose one: Add a detailed receiver example, improve error docs, or add a Getting Started guide
  4. Open a PR with the improvement

**OR Target: btcpayserver/btcpayserver**
- Look for Payjoin-related issues labeled "good-first-issue"
- Common contributions: Payjoin setup docs, test coverage, UI improvements

### Daily Life Privacy Tip

**Enable Payjoin on Your BTCPay Server Today**

If you run a BTCPay Server:
1. Go to Store Settings → Payment Methods → Bitcoin
2. Find "Enable Payjoin" and toggle it on
3. From now on, every customer payment is a Payjoin

Result: Your business becomes a privacy node in the Bitcoin network. Every payment you receive makes CIOH less reliable for everyone.

### Reading List

- **BIP77 (Payjoin Sender):** https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki
- **BIP78 (Payjoin Receiver):** https://github.com/bitcoin/bips/blob/master/bip-0078.mediawiki
- **Payjoin Spec (Human-Readable):** https://github.com/payjoin/payjoin/blob/master/README.md
- **Bull Bitcoin Wallet (BIP77):** https://www.bullbitcoin.com
- **Sparrow Wallet Payjoin Guide:** https://sparrowwallet.com
- **BTCPay Server Payjoin Docs:** https://docs.btcpayserver.org/Payjoin/
- **Mempool Payjoin Finder:** https://mempool.space

---

## Session 10: Building with Payjoin Dev Kit in Rust

### Real-World Scenario

**The Challenge:**
You're building a payment processor that should integrate with merchant wallets. You could integrate Payjoin one wallet at a time, but that's vendor-locked. Instead, you want to speak the standardized BIP77/78 protocol.

**Your Solution:**
The Payjoin Development Kit (PDK) is a Rust library that handles all protocol complexity. You implement sender logic once, and it works with any BIP78-compliant receiver.

This session, you'll build both sender and receiver implementations from scratch.

### Learning Objectives

- Understand the Payjoin Development Kit architecture
- Build a complete BIP78 receiver from scratch
- Build a complete BIP77 sender from scratch
- Debug PSBT construction and signing flows
- Test Payjoin transactions on regtest

### Privacy Tools You'll Use

- **Payjoin Development Kit (PDK)** — https://github.com/payjoin/rust-payjoin
- **Rust language** — stable edition 2021+
- **Cargo** — dependency management
- **bitcoin-cli** — transaction inspection
- **Bitcoin Core (regtest)** — local testing

### Detailed Hands-On Exercise

**Part 1: Environment Setup**

1. **Install Rust:**
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   rustup default stable
   ```

2. **Start Bitcoin Core on regtest:**
   ```bash
   bitcoind -regtest -server -rpcuser=admin -rpcpassword=password
   ```

3. **Create a new Rust project:**
   ```bash
   cargo new payjoin_implementation
   cd payjoin_implementation
   ```

**Part 2: Configure Dependencies**

Edit Cargo.toml with exact versions:
```toml
[package]
name = "payjoin_implementation"
version = "0.1.0"
edition = "2021"

[dependencies]
payjoin = "0.13"
bitcoin = "0.31"
bitcoincore-rpc = "0.18"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1", features = ["full"] }
axum = "0.7"
anyhow = "1.0"
```

**Part 3: Build Components**

Implement `src/receiver.rs` for BIP78 receiver:
- Parse incoming PSBT from sender
- Add receiver's own UTXO as additional input
- Modify output destinations
- Sign receiver's input
- Return modified PSBT

Implement `src/sender.rs` for BIP77 sender:
- Create unsigned PSBT with receiver address
- Fund with sender's UTXO
- POST to receiver's Payjoin endpoint
- Receive modified PSBT from receiver
- Sign sender's input and broadcast

**Part 4: Integration Testing**

Write tests that:
- Create a Payjoin PSBT on regtest
- Verify receiver adds its input
- Verify outputs are modified
- Ensure transaction is valid before broadcast

### Open a PR This Week

**Target: payjoin/rust-payjoin**

1. **Review existing examples** at https://github.com/payjoin/rust-payjoin/tree/master/payjoin/examples

2. **Contribute:**
   - Write `examples/complete_payjoin.rs` showing full sender + receiver flow
   - Include comments explaining each protocol step
   - Ensure code compiles and runs

3. **PR checklist:**
   - Code compiles cleanly
   - Includes error handling
   - Follows existing code style
   - Has clear comments

### Daily Life Privacy Tip

**Use Payjoin for Every Payment You Receive**

If you're a merchant or service provider:
1. **BTCPay Server:** Enable Payjoin in store settings
2. **Sparrow Wallet:** Accept Payjoin requests when offered
3. **Bull Bitcoin:** Request Payjoin from merchants

Every Payjoin strengthens privacy for all Bitcoin users by degrading heuristic analysis.

### Reading List

- **Payjoin Dev Kit:** https://github.com/payjoin/rust-payjoin
- **Rust Book (chapters 1-10):** https://doc.rust-lang.org/book/
- **Bitcoincore RPC Docs:** https://github.com/rust-bitcoin/rust-bitcoincore-rpc
- **PSBT Spec (BIP174):** https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki
- **Cargo Book:** https://doc.rust-lang.org/cargo/

---

## Session 11: Payjoin in Production (BTCPay, Bull Bitcoin, Wallets)

### Real-World Scenario

**Your Business:**
You run a small coffee shop with Bitcoin payments via BTCPay Server. Every morning, customers pay with Bitcoin.

**The Problem (Before Payjoin):**
Every payment hits the blockchain with:
- Input 1: Your hot wallet address
- Output 1: Change back to you

Chain analysts see: "This person controls both the input and the output. All their payments are now linked."

**The Solution (With Payjoin):**
You enable Payjoin in BTCPay settings. Now:
- Alice sends 0.5 BTC
- Your wallet automatically adds its own input
- Outputs look scrambled to the analyst
- Result: Alice's payment is indistinguishable from your business consolidating change

After a month of Payjoin payments, analysts can't track your money in or out.

### Learning Objectives

- Deploy Payjoin in production using BTCPay Server
- Configure wallet integrations (Sparrow, Bull Bitcoin)
- Monitor Payjoin adoption and privacy metrics
- Debug production issues (timeout, rejection, fee negotiation)
- Understand operational implications of Payjoin

### Privacy Tools You'll Use

- **BTCPay Server** (BIP78 receiver) — production merchant platform
- **Sparrow Wallet** (BIP77 sender) — desktop wallet integration
- **Bull Bitcoin Wallet** (BIP77 sender) — mobile wallet
- **Bitcoin Core** — transaction validation
- **Mempool.space** — monitor transactions
- **docker** — containerized deployment

### Detailed Hands-On Exercise

**Part 1: Deploy BTCPay Server Locally**

1. **Clone and set up:**
   ```bash
   git clone https://github.com/btcpayserver/btcpayserver.git
   cd btcpayserver
   git checkout v1.13.0
   ```

2. **Configure with Docker Compose:**
   ```bash
   cp .env.example .env
   sed -i 's/NBITCOIN_NETWORK=.*/NBITCOIN_NETWORK=regtest/' .env
   docker compose up -d
   ```

3. **Access at http://127.0.0.1:3000:**
   - Create admin account
   - Set up test store

**Part 2: Enable Payjoin**

1. **In BTCPay Admin Settings:**
   - Go to Services → Bitcoin
   - Verify connection to Bitcoin Core

2. **Enable Payjoin on your store:**
   - Store Settings → Bitcoin → Payjoin (BIP78)
   - Toggle on
   - Configure: 30-minute expiration, 50bp max fee increase

3. **Verify endpoint is live:**
   ```bash
   curl http://localhost:3000/.well-known/payjoin
   ```

**Part 3: Create Invoice and Receive Payment**

1. **Create test invoice:**
   - Go to Invoices → Create Invoice
   - Enter amount: 0.5 BTC

2. **Send Payjoin payment from Sparrow:**
   - Open Sparrow Wallet
   - Send tab → Paste Payjoin address (with ?pj= parameter)
   - Sign and broadcast

3. **Inspect on-chain:**
   - Transaction now has 2 inputs (yours + sender's)
   - Outputs scrambled to analysts
   - CIOH is broken

**Part 4: Monitor and Test**

1. **Create 5-10 test invoices**
2. **Send Payjoin payments each time**
3. **Track metrics:**
   - Success rate
   - Average time to completion
   - Fee negotiation results

4. **Document failure cases:**
   - Insufficient fee
   - Small amounts
   - Timeout behavior

### Open a PR This Week

**Target: btcpayserver/btcpayserver**

1. **Find Payjoin issues:**
   - https://github.com/btcpayserver/btcpayserver/issues
   - Filter by "Payjoin" label

2. **Common contributions:**
   - Test case for Payjoin timeout handling
   - Documentation of Payjoin settings
   - UI improvements for Payjoin setup

3. **Example PR:**
   - Add test: "test_payjoin_timeout_broadcasts_unsigned"
   - Verify fallback behavior when receiver times out
   - File PR with detailed test steps

### Daily Life Privacy Tip

**If You Accept Bitcoin, Enable Payjoin Today**

Whether you're a merchant, freelancer, or donation recipient:

1. **BTCPay Server:**
   - Settings → Bitcoin → Payjoin (BIP78)
   - Toggle ON

2. **Wasabi Wallet:**
   - Enable Payjoin receiver mode (when available)

3. **The Ripple Effect:**
   - Every Payjoin transaction degrades heuristics globally
   - After 10% adoption, analysts can't rely on CIOH
   - You're making privacy the default

### Reading List

- **BTCPay Server Docs:** https://docs.btcpayserver.org
- **Payjoin Setup Guide:** https://docs.btcpayserver.org/Payjoin/
- **Sparrow Wallet Documentation:** https://sparrowwallet.com/docs
- **Bull Bitcoin Mobile Wallet:** https://www.bullbitcoin.com
- **BTCPay Server GitHub:** https://github.com/btcpayserver/btcpayserver
- **Docker Compose for Bitcoin:** https://docs.docker.com/compose
- **Bitcoin Core RPC Docs:** https://developer.bitcoin.org/reference/rpc/

---

## Session 12: Contributing to Payjoin — Ecosystem & Protocol

### Real-World Scenario

**The Opportunity:**
Payjoin is young but growing. Gaps exist:
- Wallet integration is inconsistent
- The specification needs clarification
- Production deployments need better tooling
- Privacy properties need academic validation

As a Bitcoin privacy developer, you can shape the protocol's future. This session, you'll find real issues and fix them.

### Learning Objectives

- Navigate the Payjoin ecosystem repositories
- Identify and prioritize contribution opportunities
- Write production-quality tests for Payjoin logic
- Improve protocol documentation and error handling
- Collaborate with the Payjoin working group

### Privacy Tools You'll Use

- **payjoin/rust-payjoin** — reference implementation
- **btcpayserver/btcpayserver** — production receiver
- **sparrowwallet/sparrow** — production sender
- **git** — version control
- **GitHub Issues & PRs** — collaboration
- **cargo test** — testing framework

### Detailed Hands-On Exercise

**Part 1: Understand the Ecosystem**

1. **Map the repositories:**
   ```bash
   git clone https://github.com/payjoin/rust-payjoin.git
   git clone https://github.com/btcpayserver/btcpayserver.git
   git clone https://github.com/sparrowwallet/sparrow.git
   ```

2. **Understand relationships:**
   - rust-payjoin: Specification + reference implementation
   - btcpayserver: Production receiver
   - Sparrow: Production sender

3. **Review open issues:**
   ```bash
   curl -s https://api.github.com/repos/payjoin/rust-payjoin/issues?state=open | jq '.[] | {number: .number, title: .title}'
   ```

**Part 2: Choose a Contribution**

**Option A: rust-payjoin — Protocol Robustness**

Improve error handling:
- Add context to PSBT validation errors
- Example: Instead of "Invalid PSBT", return "Invalid PSBT: input 0 has no previous_output"
- Write test showing improved error messages

**Option B: btcpayserver — Production Integration**

Add monitoring:
- Track Payjoin success rate
- Log attempt vs. success metrics
- Document failure modes

**Option C: Improve Error Messages**

User-friendly failures:
- Instead of: "Payjoin negotiation failed (500)"
- Show: "Merchant is processing your payment. Payment sent as standard transaction."

**Part 3: Fork and Set Up**

1. **Fork the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rust-payjoin.git
   cd rust-payjoin
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b improve/payjoin-error-context
   ```

3. **Verify the build:**
   ```bash
   cargo test
   ```

**Part 4: Make Your Contribution**

Example: Improve Error Context

1. **Locate validation code:**
   ```bash
   grep -r "Invalid PSBT" src/
   ```

2. **Edit src/receive/mod.rs:**
   - Add input index to error messages
   - Write test showing improved error context
   - Run: `cargo test test_unsigned_receiver_input_error`

3. **Commit with clear message:**
   ```bash
   git add src/receive/mod.rs tests/validation.rs
   git commit -m "Improve error context for unsigned receiver inputs

   - Add input index to error messages
   - Add test case for unsigned input validation
   - Helps developers debug Payjoin flows"
   ```

**Part 5: Open Your PR**

1. **Push to fork:**
   ```bash
   git push origin improve/payjoin-error-context
   ```

2. **Open PR on GitHub:**
   - Clear description of problem and solution
   - Link to related issues
   - Show test results

3. **Respond to review feedback:**
   - Make requested changes
   - Push updates

### Open a PR This Week

Your PR should:
- Fix a real issue or improve documentation
- Include tests
- Follow existing code style
- Have clear commit messages
- Be mergeable (no conflicts)

### Daily Life Privacy Tip

**Join the Payjoin Community**

Payjoin is a movement to make privacy default for payments.

1. **Follow the discussion:**
   - GitHub Discussions: https://github.com/payjoin/rust-payjoin/discussions
   - Bitcoin-dev mailing list: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/

2. **Test new features:**
   - Try every new release of rust-payjoin, Sparrow, BTCPay
   - Test with friends
   - Report bugs and UX issues

3. **Advocate for Payjoin:**
   - Tell merchants about BTCPay Payjoin
   - Recommend Sparrow to senders
   - Explain why CIOH is dead

Every time someone uses Payjoin, a heuristic dies.

### Reading List

- **GitHub Payjoin:** https://github.com/payjoin
- **Payjoin Spec:** https://github.com/payjoin/payjoin
- **rust-payjoin Documentation:** https://docs.rs/payjoin/latest/payjoin/
- **Open Source Contribution Guide:** https://opensource.guide/how-to-contribute/
- **Git Workflow for Contributors:** https://guides.github.com/introduction/flow/
- **Rust Testing Guide:** https://doc.rust-lang.org/book/ch11-00-testing.html

---

## Phase 3 Summary & Next Steps

**What You've Achieved:**
1. Understood BIP77/78 specification and privacy properties
2. Built complete Payjoin sender + receiver in Rust
3. Deployed production Payjoin with BTCPay Server
4. Contributed to open source Payjoin projects

**Privacy Impact:**
- Every Payjoin transaction breaks CIOH for that transaction
- Merchant Payjoins are 10x more effective than individual Coinjoins
- Active deployment in BTCPay, Sparrow, Bull Bitcoin

**Your Next Challenge (Phase 4):**
Payjoin solves transaction-level privacy (input ownership). Next:
- **Network privacy:** Who broadcasts transactions? (Dandelion++, Tor, I2P)
- **Address discovery privacy:** Which addresses are yours? (Compact Block Filters)
- **Scriptpubkey privacy:** What script type do you use? (Taproot)

In Phase 4, you'll learn network and protocol layers of Bitcoin privacy.
