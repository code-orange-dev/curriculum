# Decoding Bitcoin — 8-Week Developer Study Cohort

> **An intensive, hands-on cohort taking developers from Bitcoin fundamentals to active open-source contribution.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Overview

Decoding Bitcoin is Code Orange Dev School's flagship developer program. Over 8 weeks, participants self-study Bitcoin protocol fundamentals — transactions, Script, Taproot, PSBTs — and learn how to contribute to Bitcoin open-source software through structured peer-learning sessions with experienced mentors.

**Our 2nd cohort produced 12 graduates who are now actively contributing to Bitcoin open-source projects** — with merged and approved PRs across Bitcoin Core, rust-bitcoin, BDK, rust-payjoin, peer-observer, LDK, and BlueWallet.

## Prerequisites

- Comfortable reading and writing code in at least one language (Python, Rust, C++, JavaScript, or Go preferred)
- Basic understanding of cryptography (hashing, public/private keys)
- A working Bitcoin Core node (we help you set this up in Week 1 if needed)
- Recommended: completion of Mastering Bitcoin Study Cohort or equivalent reading

## Format

| Component | Details |
|-----------|---------|
| **Duration** | 8 weeks |
| **Time commitment** | 8-12 hours per week (self-study + sessions) |
| **Weekly sessions** | 2x per week — group discussion + TA office hours |
| **Group size** | 10-20 participants, split into study groups of 4-5 |
| **Assessments** | 2 technical questions per week + final contribution project |
| **Mentors** | Experienced Bitcoin developers and Code Orange alumni |

## How It Works

1. **Monday**: Week's readings and exercises are assigned
2. **Self-study**: Participants study independently throughout the week
3. **Wednesday session**: Small group discussions — participants explain their answers to peers
4. **Friday session**: TA-led Q&A covering the week's technical questions
5. **Weekend**: Participants submit written answers to 2 technical assessment questions
6. **Week 8**: Final project — submit a real PR to a Bitcoin open-source project

---

## Week-by-Week Syllabus

### Week 1: Bitcoin Fundamentals & Environment Setup

**Learning Objectives:**
- Understand Bitcoin's architecture: blocks, transactions, UTXO model, consensus
- Set up a local Bitcoin Core development environment (regtest)
- Navigate the Bitcoin Core codebase and build from source

**Readings:**
- Mastering Bitcoin, Chapters 1-2 (Antonopoulos)
- [Bitcoin Dev Project: How Bitcoin Works](https://bitcoindevs.xyz/)
- [Chaincode Curriculum: Bitcoin Protocol Overview](https://github.com/chaincodelabs/bitcoin-curriculum)

**Exercises:**
1. Build Bitcoin Core from source on your machine
2. Start a regtest network and mine 101 blocks
3. Create a wallet, generate addresses, and send transactions between two wallets using `bitcoin-cli`
4. Explore a block using `getblock` and `getrawtransaction` — decode and explain every field

**Assessment Questions:**
1. Explain the UTXO model. How does it differ from an account-based model? What are the trade-offs?
2. Walk through the lifecycle of a Bitcoin transaction from creation to confirmation. What happens at each stage?

**Facilitator Notes:**
- Ensure everyone has a working regtest environment before proceeding
- Common issues: build dependencies on different OSes, firewall rules, disk space
- Pair struggling participants with more experienced group members

---

### Week 2: Transactions Deep Dive

**Learning Objectives:**
- Understand raw transaction structure (version, inputs, outputs, locktime)
- Manually construct and sign a raw transaction
- Understand transaction serialisation and txid calculation

**Readings:**
- Mastering Bitcoin, Chapter 6 (Transactions)
- [Learn Bitcoin from the Command Line: Chapter 4](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line)
- [Bitcoin Optech: Transaction Structure](https://bitcoinops.org/en/topics/transaction-format/)

**Exercises:**
1. Create a raw transaction using `createrawtransaction`, sign it with `signrawtransactionwithwallet`, and broadcast with `sendrawtransaction`
2. Decode a raw transaction hex and label every field (version, vin count, txid, vout, scriptSig, sequence, vout count, value, scriptPubKey, locktime)
3. Calculate a txid by hand (double SHA256 of serialised transaction)
4. Create a transaction with multiple inputs and multiple outputs — explain the fee calculation

**Assessment Questions:**
1. What is transaction malleability? Why was it a problem, and how did SegWit fix it?
2. Explain the difference between `scriptPubKey` and `scriptSig`. How do they work together to validate a transaction?

---

### Week 3: Bitcoin Script

**Learning Objectives:**
- Understand Bitcoin's stack-based scripting language
- Analyse common script patterns (P2PKH, P2SH, P2WPKH)
- Debug scripts using the Script interpreter

**Readings:**
- Mastering Bitcoin, Chapter 7 (Advanced Transactions and Scripting)
- [Chaincode Curriculum: Script](https://github.com/chaincodelabs/bitcoin-curriculum)
- [Bitcoin Wiki: Script](https://en.bitcoin.it/wiki/Script)

**Exercises:**
1. Trace the execution of a P2PKH script step-by-step through the stack
2. Create a P2SH multisig transaction (2-of-3) on regtest
3. Write a custom script using `OP_IF`, `OP_ELSE`, and timelocks — test on regtest
4. Analyse a real mainnet transaction with an unusual script pattern

**Assessment Questions:**
1. Why is Bitcoin's Script language intentionally not Turing-complete? What are the security implications?
2. Explain how P2SH works. Why was it introduced, and what problem does it solve for the sender?

---

### Week 4: SegWit

**Learning Objectives:**
- Understand Segregated Witness (BIP141, BIP143, BIP144)
- Compare legacy, nested SegWit, and native SegWit transaction formats
- Understand the witness discount and its implications for fees

**Readings:**
- Mastering Bitcoin, Chapter 12 (SegWit)
- [BIP 141](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki), [BIP 143](https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki)
- [Bitcoin Optech: SegWit](https://bitcoinops.org/en/topics/segwit/)

**Exercises:**
1. Create and compare legacy (P2PKH) vs native SegWit (P2WPKH) transactions on regtest — compare sizes and fees
2. Decode a SegWit transaction and identify the witness data
3. Calculate the weight units and virtual size (vbytes) of a transaction
4. Create a P2WSH (Pay-to-Witness-Script-Hash) multisig transaction

**Assessment Questions:**
1. How does SegWit fix transaction malleability? Walk through the technical mechanism.
2. Explain the witness discount. Why does witness data get a 75% discount, and what behaviour does this incentivise?

---

### Week 5: Taproot

**Learning Objectives:**
- Understand Taproot (BIP340, BIP341, BIP342)
- Understand Schnorr signatures and their advantages over ECDSA
- Create Taproot transactions with key-path and script-path spends

**Readings:**
- [BIP 340](https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki) (Schnorr Signatures)
- [BIP 341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) (Taproot)
- [Bitcoin Optech: Taproot](https://bitcoinops.org/en/topics/taproot/)
- [Chaincode Curriculum: Taproot](https://github.com/chaincodelabs/bitcoin-curriculum)

**Exercises:**
1. Create a Taproot (P2TR) address and send a transaction to it on regtest
2. Spend from a Taproot output using the key-path (default)
3. Create a Taproot output with a script tree containing two spending conditions — spend using the script-path
4. Compare the on-chain footprint of a Taproot multisig vs a P2WSH multisig

**Assessment Questions:**
1. Explain how Taproot improves privacy. How does the key-path spend make complex scripts indistinguishable from simple payments?
2. What are Schnorr signatures and how do they enable key aggregation (MuSig2)? Why couldn't this be done with ECDSA?

---

### Week 6: PSBTs (Partially Signed Bitcoin Transactions)

**Learning Objectives:**
- Understand the PSBT format (BIP174, BIP370)
- Create, update, sign, and finalise PSBTs
- Use PSBTs for multisig coordination and hardware wallet workflows

**Readings:**
- [BIP 174](https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki) (PSBT)
- [BIP 370](https://github.com/bitcoin/bips/blob/master/bip-0370.mediawiki) (PSBT v2)
- [Bitcoin Optech: PSBTs](https://bitcoinops.org/en/topics/psbt/)

**Exercises:**
1. Create a PSBT using `walletcreatefundedpsbt`, inspect with `decodepsbt`
2. Implement a 2-of-3 multisig signing workflow using PSBTs — Creator, Updater, Signer(s), Finaliser, Extractor
3. Use `combinepsbt` to merge partial signatures from two signers
4. Build a PSBT workflow with a hardware wallet simulator (or HWI if available)

**Assessment Questions:**
1. Walk through the PSBT roles (Creator, Updater, Signer, Combiner, Finaliser, Extractor). Why are they separated?
2. How do PSBTs improve security for hardware wallets and air-gapped signing setups?

---

### Week 7: Bitcoin Core Architecture & Development

**Learning Objectives:**
- Navigate the Bitcoin Core codebase structure
- Understand the build system, testing framework, and CI pipeline
- Read and review real Bitcoin Core pull requests
- Understand the Bitcoin Core contribution workflow

**Readings:**
- [Bitcoin Core CONTRIBUTING.md](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md)
- [Bitcoin Core Developer Documentation](https://github.com/bitcoin/bitcoin/tree/master/doc)
- [Chaincode Curriculum: Bitcoin Core Architecture](https://github.com/chaincodelabs/bitcoin-curriculum)
- [Jon Atack's guide to reviewing Bitcoin Core PRs](https://jonatack.github.io/articles/how-to-review-pull-requests-in-bitcoin-core)

**Exercises:**
1. Clone Bitcoin Core, build from source, and run the functional test suite
2. Navigate the codebase: identify where transaction validation, block validation, and P2P networking code live
3. Pick a "good first issue" from Bitcoin Core (or another Bitcoin OSS project) and write up a plan for addressing it
4. Review an open Bitcoin Core PR — write review comments (even if you don't submit them)

**Assessment Questions:**
1. Describe the Bitcoin Core review process. Why is it considered one of the most rigorous in open source?
2. What is the role of the functional test suite? How would you write a test for a new feature?

---

### Week 8: Your First Open-Source Contribution

**Learning Objectives:**
- Submit a real pull request to a Bitcoin open-source project
- Understand git workflow for open-source contribution (fork, branch, PR, review, iterate)
- Navigate project-specific contribution guides and coding standards

**Readings:**
- Contribution guides for target projects:
  - [Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md)
  - [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin/blob/master/CONTRIBUTING.md)
  - [BDK](https://github.com/bitcoindevkit/bdk/blob/master/CONTRIBUTING.md)
  - [LDK](https://github.com/lightningdevkit/rust-lightning/blob/main/CONTRIBUTING.md)
- [How to contribute to Bitcoin (bitcoin-dev-project)](https://bitcoindevs.xyz/decoding)

**Final Project:**
Submit a real pull request to any Bitcoin open-source project. This can be:
- A bug fix
- A documentation improvement
- A test improvement
- A small feature
- A translation
- A code review (written review comments on an existing PR)

**Presentation:**
Each participant presents their contribution to the cohort:
1. What project did you contribute to, and why?
2. What does your PR do?
3. What did you learn from the review process?
4. What will you work on next?

---

## After the Cohort

Graduates are encouraged to:

1. **Continue contributing** — aim for 1 PR per month to any Bitcoin OSS project
2. **Apply to fellowships** — Chaincode Labs, base58, Btrust/Qala, Vinteum
3. **Apply for grants** — OpenSats, HRF Bitcoin Development Fund, Brink
4. **Mentor the next cohort** — become a TA or mentor for future Decoding Bitcoin cohorts
5. **Join the community** — stay active in our Discord, attend monthly reading clubs

---

## Facilitator Guide

### Before the Cohort

- [ ] Recruit 10-20 participants (screen for coding ability and commitment)
- [ ] Set up communication channels (Discord server or Telegram group)
- [ ] Assign study groups of 4-5 participants
- [ ] Ensure all participants have a working Bitcoin Core regtest environment
- [ ] Recruit 2-3 TAs (ideally previous cohort graduates)

### During the Cohort

- [ ] Post weekly readings and exercises every Monday
- [ ] Facilitate Wednesday group discussions (rotate discussion leaders)
- [ ] Host Friday TA Q&A sessions
- [ ] Collect and review assessment answers weekly
- [ ] Track participation and flag at-risk participants early
- [ ] Hold 1-on-1 check-ins at weeks 4 and 7

### After the Cohort

- [ ] Collect feedback (anonymous survey)
- [ ] Track graduate contributions (PRs, projects, fellowships)
- [ ] Update this curriculum based on feedback
- [ ] Invite top graduates to TA for the next cohort

---

## License

This curriculum is dedicated to the public domain under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). Fork it, translate it, teach with it. No permission needed.
