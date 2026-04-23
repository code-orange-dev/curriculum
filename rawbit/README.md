# rawBit Study Cohort — 10-Week Program

> **Build raw Bitcoin transactions from scratch using a visual, interactive tool.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Overview

The rawBit Study Cohort is a 10-week hands-on program where participants build raw Bitcoin transactions from scratch using [rawBit](https://github.com/rawBit-io/rawbit) — an open-source visual Bitcoin transaction builder and Script debugger. Participants connect inputs, keys, and scripts on a visual canvas to construct transactions at the byte level, progressing from legacy P2PKH all the way to Taproot.

This cohort is the natural next step after [Bitcoin Dojo](../bitcoin-dojo/) — where you learned the cryptographic primitives, here you apply them to build real transactions.

**rawBit** is created by [@rawBit_io](https://x.com/rawBit_io) and ships with 12 built-in interactive lessons. Code Orange runs a structured study cohort around these lessons with weekly group calls, peer accountability, and mentor support.

## Prerequisites

- Completion of [Bitcoin Dojo](../bitcoin-dojo/) or equivalent knowledge of:
  - Elliptic curve cryptography and ECDSA
  - Bitcoin address formats (P2PKH, P2SH, P2WPKH)
  - Basic transaction structure (inputs, outputs, scripts)
- OR: Strong self-taught understanding of Bitcoin transaction fundamentals
- A laptop with a modern web browser (rawBit runs in-browser)

## Format

| Component | Details |
|-----------|---------|
| **Duration** | 10 weeks |
| **Time commitment** | 4-6 hours per week |
| **Weekly calls** | Via Discord (time TBD per cohort) |
| **Tool** | [rawBit](https://github.com/rawBit-io/rawbit) visual transaction builder |
| **Level** | Intermediate (post-Bitcoin Dojo) |

## How It Works

1. **Each week**: 1-2 rawBit lessons assigned + supplementary readings
2. **Self-study**: Work through the interactive lessons in rawBit — drag, connect, build, inspect
3. **Weekly call**: Group discussion and live debugging of transaction construction
4. **Challenge exercises**: Build increasingly complex transactions without the guided mode
5. **Final project**: Construct a complex multi-condition Taproot transaction from scratch

---

## Week-by-Week Syllabus

### Week 1: rawBit Setup & Legacy Transactions (P2PK, P2PKH)

**rawBit Lessons**: Lesson 1 (P2PK), Lesson 2 (P2PKH)

**Topics:**
- rawBit interface: canvas, nodes, connections, inspector
- Pay-to-Public-Key (P2PK): the simplest transaction type
- Pay-to-Public-Key-Hash (P2PKH): why hashing the public key matters
- Building a complete transaction: input → scriptSig → output → scriptPubKey
- Inspecting the raw hex output byte by byte

**Exercises:**
1. Build a P2PK transaction in rawBit — send coins to a public key and spend them
2. Build a P2PKH transaction — compare the script structure to P2PK
3. Export the raw hex and decode it manually, labelling every field

**Discussion:**
- Why did Bitcoin move from P2PK to P2PKH? What's the security improvement?

---

### Week 2: Multisig Transactions

**rawBit Lessons**: Lesson 3 (Multisig), Lesson 4 (P2SH fundamentals)

**Topics:**
- OP_CHECKMULTISIG: how multi-signature verification works in Script
- The off-by-one bug and OP_0 workaround
- 2-of-3 multisig: building and spending
- Pay-to-Script-Hash (P2SH): hiding complex scripts behind a hash
- Redeem scripts and their role in P2SH

**Exercises:**
1. Build a 2-of-3 bare multisig transaction in rawBit
2. Wrap the same multisig in P2SH — compare the output scripts
3. Spend from the P2SH output by providing the redeem script and signatures

---

### Week 3: Timelocks

**rawBit Lessons**: Lesson 5 (nLockTime/nSequence), Lesson 6 (OP_CHECKLOCKTIMEVERIFY)

**Topics:**
- Absolute timelocks: nLockTime (transaction-level)
- OP_CHECKLOCKTIMEVERIFY (CLTV): script-level absolute timelock
- Relative timelocks: nSequence and OP_CHECKSEQUENCEVERIFY (CSV)
- Use cases: payment channels, inheritance, escrow

**Exercises:**
1. Build a transaction with an nLockTime set to a future block height
2. Build a CLTV-locked output that can only be spent after block N
3. Build a CSV-locked output with a relative timelock of 144 blocks (~1 day)
4. Combine timelocks with multisig: "Alice can spend immediately with 2-of-3, OR Bob can spend alone after 1000 blocks"

---

### Week 4: OP_RETURN & Data Anchoring

**rawBit Lesson**: Lesson 7 (OP_RETURN anchors)

**Topics:**
- OP_RETURN: provably unspendable outputs
- Embedding data in the Bitcoin blockchain
- Size limits and relay policies
- Use cases: timestamping, commitments, coloured coins history
- Ethical and practical considerations of blockchain data

**Exercises:**
1. Build a transaction with an OP_RETURN output containing a message
2. Build a commitment scheme: hash a document, embed the hash in OP_RETURN
3. Explore a real mainnet transaction with OP_RETURN data

---

### Week 5: Transaction Malleability & Payment Channels

**rawBit Lesson**: Lesson 8 (Transaction malleability), Lesson 9 (Payment channels)

**Topics:**
- Transaction malleability: how it works, why it's dangerous
- How scriptSig manipulation changes the txid without invalidating the transaction
- Payment channels: the foundational concept behind Lightning
- Building a simple unidirectional payment channel
- Why malleability breaks payment channels (motivating SegWit)

**Exercises:**
1. Demonstrate transaction malleability: modify a scriptSig encoding and show the txid changes
2. Build a simple payment channel: funding tx + commitment txs + settlement tx
3. Show how malleability would break the commitment transaction chain

---

### Week 6: SegWit Transactions (P2WPKH)

**rawBit Lessons**: Lesson 10 (P2WPKH)

**Topics:**
- Segregated Witness: moving the witness outside the txid calculation
- P2WPKH (Pay-to-Witness-Public-Key-Hash): native SegWit
- Witness field structure
- Weight units vs virtual bytes
- The witness discount: why witness data is cheaper

**Exercises:**
1. Build a P2WPKH transaction in rawBit — compare structure to P2PKH
2. Calculate the weight and vbytes of your SegWit transaction
3. Build the same transaction as legacy P2PKH — compare sizes and fees
4. Verify that the witness data is excluded from the txid calculation

---

### Week 7: SegWit Scripts (P2WSH)

**rawBit Lessons**: Lesson 11 (P2WSH, nested SegWit)

**Topics:**
- P2WSH (Pay-to-Witness-Script-Hash): SegWit version of P2SH
- Witness scripts vs redeem scripts
- Nested SegWit (P2SH-P2WPKH): backward compatibility
- When to use P2WPKH vs P2WSH vs nested SegWit

**Exercises:**
1. Build a P2WSH 2-of-3 multisig in rawBit
2. Build the same multisig as P2SH — compare witness data vs scriptSig
3. Build a nested SegWit (P2SH-P2WPKH) transaction

---

### Week 8: Taproot Basics

**rawBit Lessons**: Lesson 12 (Taproot)

**Topics:**
- Schnorr signatures (BIP340): linearity and key aggregation
- Taproot (BIP341): key-path vs script-path spending
- The Taproot tweak: how a public key commits to a script tree
- P2TR (Pay-to-Taproot) output structure
- Why key-path spends look identical to regular payments (privacy)

**Exercises:**
1. Build a Taproot (P2TR) key-path spend in rawBit
2. Build a Taproot output with a script tree
3. Spend via the script-path — provide the script, control block, and Merkle proof
4. Compare the on-chain footprint of key-path vs script-path

---

### Week 9: Advanced Taproot & MuSig2

**Topics:**
- MuSig2: interactive multi-signature with a single public key
- Taproot script trees: building complex spending conditions
- MAST (Merkelized Abstract Syntax Tree) via Taproot
- Combining Taproot with timelocks for complex contracts
- Tapscript (BIP342): new opcodes for Taproot

**Exercises:**
1. Design a Taproot output with 3 spending conditions in the script tree
2. Build an escrow contract: "Alice+Bob key-path, OR Alice after 1000 blocks, OR Bob+mediator"
3. Calculate the Merkle root of a script tree with 4 leaves

---

### Week 10: Final Project & Graduation

**Final Project:**
Build a complex, real-world Bitcoin transaction entirely from scratch in rawBit. Choose from:

1. **Inheritance Vault**: Taproot output where spouse can spend with 2-of-3 multisig immediately, OR a single heir key after 52,560 blocks (~1 year)
2. **Atomic Swap**: Construct both sides of a cross-chain atomic swap using HTLCs (Hash Time-Locked Contracts)
3. **Lightning-style Channel**: Full funding → commitment → revocation → settlement flow
4. **Custom Design**: Propose your own complex transaction design

**Presentation:**
Each participant presents their final project:
1. What does the transaction do and why is it useful?
2. Walk through the script tree / spending conditions
3. What did building it teach you about Bitcoin?
4. What will you build or contribute to next?

---

## After the Cohort

Graduates are ready to:
- Start contributing to Bitcoin transaction-related projects (BDK, rust-bitcoin, Bitcoin Core wallet)
- Build wallet software that constructs transactions correctly
- Review PRs involving transaction format changes
- Teach others using rawBit as a visual aid
- Continue to the [Decoding Bitcoin](../decoding-bitcoin/) cohort for Bitcoin Core contribution

---

## Facilitator Guide

### Before the Cohort

- [ ] Ensure all participants have rawBit running in their browser
- [ ] Confirm participants have completed Bitcoin Dojo or equivalent
- [ ] Set up Discord channel with weekly threads
- [ ] Coordinate with [@rawBit_io](https://x.com/rawBit_io) for any tool updates or support

### During the Cohort

- [ ] Post weekly lesson assignments every Sunday
- [ ] Host weekly calls — screen-share rawBit for live transaction building
- [ ] Encourage participants to export and share their transaction hex
- [ ] Pair struggling participants with faster learners

### After the Cohort

- [ ] Host graduation presentations
- [ ] Connect graduates to relevant Good First Issues (especially BDK, rust-bitcoin transaction modules)
- [ ] Track graduate outcomes in PR Dashboard

---

## Credits

- **rawBit tool**: [rawBit.io](https://github.com/rawBit-io/rawbit) — Visual Bitcoin TX builder & Script debugger
- **Upstream textbook**: [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin) by Jimmy Song
- **Partner**: Code Orange Dev School in collaboration with rawBit

---

## License

CC0 1.0 Universal. Public domain. Fork it, translate it, teach with it.
