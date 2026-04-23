# Bitcoin Dojo — 7-Week Developer Study Cohort

> **Build Bitcoin primitives from scratch. Understand the cryptography that makes Bitcoin work.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Overview

Bitcoin Dojo is a 7-week study cohort run in partnership with [Chaincode Labs](https://chaincode.com/) as part of the [BOSS Challenge](https://learning.chaincode.com/) (Building Open Source Software). Participants build Bitcoin's cryptographic primitives from scratch using Jimmy Song's [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin) — covering finite fields, elliptic curves, ECDSA, key generation, address encoding, and transaction construction.

This is not a lecture course. Participants study independently, then defend their understanding in weekly group calls where they explain answers to assigned questions. The goal: turn developers into Bitcoiners who are ready to contribute to open-source projects.

**Our first cohort had 49 registrants and produced 21 graduates**, many of whom are now pursuing Good First Issues across Bitcoin Core, rust-bitcoin, BDK, and other projects.

## Prerequisites

- Comfortable writing code in Python (the exercises use Python)
- Basic understanding of algebra (modular arithmetic is taught from scratch)
- No prior Bitcoin knowledge required — we build everything from first principles

## Format

| Component | Details |
|-----------|---------|
| **Duration** | 7 weeks |
| **Time commitment** | 6-10 hours per week (self-study + calls) |
| **Weekly calls** | Mondays 11:00 UTC via Discord |
| **Textbook** | [Programming Bitcoin](https://github.com/jimmysong/programmingbitcoin) by Jimmy Song |
| **Partner** | [Chaincode Labs](https://chaincode.com/) BOSS Challenge |
| **Registrants (Cohort 1)** | 49 |
| **Graduates (Cohort 1)** | 21 |

## How It Works

1. **Each week**: 2 chapters assigned from Programming Bitcoin
2. **Self-study**: Work through the chapters and solve the Python exercises
3. **Weekly questions**: 2-3 technical questions assigned per week — you must prepare written answers
4. **Monday call (11:00 UTC)**: Group discussion where participants explain their answers to peers
5. **Vibe coding homework**: Students vibe-code a website to visually explain one concept from the week's material
6. **Graduation**: Final call with personalised next-step plans for each developer

---

## Week-by-Week Syllabus

### Week 1: Finite Fields

**Chapters**: Programming Bitcoin, Chapters 1-2

**Topics:**
- What are finite fields and why Bitcoin needs them
- Modular arithmetic: addition, subtraction, multiplication, division, exponentiation
- Field properties: closure, associativity, commutativity, identity, inverse
- Why the modulus must be prime
- Python implementation: `FieldElement` class with operator overloading

**Discussion Questions:**
1. Explain the modulo operation. Why must the modulus be prime for the set of integers modulo p to form a field? What breaks if we use a composite modulus instead?
2. Implement and explain Fermat's Little Theorem. How does it enable division in a finite field?

**Exercises:**
- Implement `FieldElement.__add__`, `__sub__`, `__mul__`, `__pow__`, `__truediv__`
- Verify field closure: pick any two elements, show that every operation stays in the field
- Find all elements of order p-1 in a small field

---

### Week 2: Elliptic Curves

**Chapters**: Programming Bitcoin, Chapters 2-3

**Topics:**
- Elliptic curve equation: y^2 = x^3 + ax + b
- Point addition: geometric and algebraic
- The point at infinity (identity element)
- Elliptic curves over finite fields
- How point operations differ over real numbers vs finite fields
- Python implementation: `Point` class

**Discussion Questions:**
1. What is the point at infinity? Why do we need it? What algebraic properties would fail without it?
2. What are elliptic curves over finite fields, and how do they differ from elliptic curves over real numbers?
3. Explain point addition geometrically. What happens when both points are the same (point doubling)?

**Exercises:**
- Implement `Point.__add__` for all cases (different points, same point, identity)
- Verify that point addition is associative over a small curve
- Find the order of a generator point on a small curve

---

### Week 3: Keys, Addresses & Encoding

**Chapters**: Programming Bitcoin, Chapters 4-5

**Topics:**
- secp256k1: Bitcoin's specific elliptic curve parameters
- Private keys → public keys (scalar multiplication)
- Compressed vs uncompressed SEC (Standards for Efficient Cryptography) format
- SHA256 and RIPEMD160 hashing
- Base58Check encoding
- Bech32 encoding (SegWit addresses)
- How Bitcoin turns keys into addresses: the full pipeline

**Discussion Questions:**
1. Walk through the complete path from a private key (256-bit integer) to a Bitcoin address. What are all the steps and why does each exist?
2. What is the difference between compressed and uncompressed public keys? Why does Bitcoin prefer compressed keys?
3. Why does Bitcoin use both SHA256 and RIPEMD160 (Hash160) instead of just one?

**Exercises:**
- Generate a private key, compute the public key, and derive a P2PKH address by hand
- Implement Base58Check encoding and decoding
- Compare the address output for compressed vs uncompressed public keys from the same private key

---

### Week 4: Serialisation & Transactions

**Chapters**: Programming Bitcoin, Chapters 5-6

**Topics:**
- Transaction structure: version, inputs, outputs, locktime
- Input structure: previous txid, vout index, scriptSig, sequence
- Output structure: value, scriptPubKey
- Transaction serialisation (little-endian, varint encoding)
- Parsing a raw transaction from hex

**Discussion Questions:**
1. Explain each field in a raw Bitcoin transaction. Why is the txid little-endian?
2. What is the difference between scriptPubKey and scriptSig? How do they work together?

**Exercises:**
- Parse a real raw transaction hex, label every byte
- Implement `Tx.parse()` and `Tx.serialize()` in Python
- Calculate a transaction's fee given its inputs and outputs

---

### Week 5: Script & Transaction Validation

**Chapters**: Programming Bitcoin, Chapters 6-7

**Topics:**
- Bitcoin Script: stack-based execution
- Standard script patterns: P2PKH, P2SH
- Script evaluation: combining scriptSig + scriptPubKey
- OP_CHECKSIG: how signature verification works inside Script
- OP_CHECKMULTISIG and its off-by-one bug
- Transaction signing: creating the signature hash

**Discussion Questions:**
1. Trace the execution of a P2PKH script step by step. What is on the stack at each point?
2. Explain the OP_CHECKMULTISIG off-by-one bug. Why hasn't it been fixed?

**Exercises:**
- Implement a basic Script interpreter that can evaluate P2PKH
- Sign a transaction: generate the signature hash (sighash), sign with ECDSA, insert into scriptSig
- Create and validate a 2-of-3 multisig script

---

### Week 6: SegWit & Advanced Transactions

**Chapters**: Programming Bitcoin, Chapters 8-13

**Topics:**
- Transaction malleability problem
- Segregated Witness (BIP141): separating witness data
- SegWit transaction format: marker, flag, witness field
- P2WPKH and P2WSH
- Nested SegWit (P2SH-P2WPKH)
- Weight units and the witness discount
- Timelocks: nLockTime and nSequence (OP_CHECKLOCKTIMEVERIFY, OP_CHECKSEQUENCEVERIFY)

**Discussion Questions:**
1. How does SegWit fix transaction malleability? Walk through the technical mechanism.
2. Explain nLockTime vs nSequence. What is the difference between absolute and relative timelocks?

**Exercises:**
- Construct a SegWit (P2WPKH) transaction and compare its serialisation to a legacy transaction
- Calculate weight units and virtual bytes for both legacy and SegWit transactions
- Build a timelock transaction that can only be spent after a specific block height

---

### Week 7: Graduation & Next Steps

**Topics:**
- Review of the full cryptographic stack: fields → curves → keys → addresses → transactions → scripts → SegWit
- How to contribute to Bitcoin open-source software
- Finding your first Good First Issue
- Overview of Bitcoin OSS projects to contribute to
- Grant and fellowship opportunities

**Graduation Call:**
Each participant presents:
1. One concept from the course that changed how they understand Bitcoin
2. Their vibe-coded website explaining a Bitcoin concept
3. Their chosen next step: which project, which Good First Issue, which fellowship

**Next Steps for Graduates:**
- Join the [rawBit Study Cohort](../rawbit/) to build raw transactions with an interactive visual tool
- Start the [Decoding Bitcoin](../decoding-bitcoin/) cohort for deeper protocol work
- Pick a Good First Issue from Bitcoin Core, rust-bitcoin, BDK, or LDK
- Apply to Chaincode Labs BOSS Challenge or Summer of Bitcoin
- Continue in the Code Orange Discord community

---

## Facilitator Guide

### Before the Cohort

- [ ] Confirm partnership with Chaincode Labs / BOSS Challenge (if applicable)
- [ ] Open registration (target: 40-50 registrants, expect ~50% completion rate)
- [ ] Set up Discord channel with weekly topic threads
- [ ] Ensure all participants have Python 3 installed
- [ ] Clone Jimmy Song's [programmingbitcoin repo](https://github.com/jimmysong/programmingbitcoin)
- [ ] Recruit 2-3 TAs (previous Decoding Bitcoin or Dojo graduates)

### During the Cohort

- [ ] Post weekly readings and questions every Sunday
- [ ] Host Monday 11:00 UTC calls (record for those who miss)
- [ ] Assign vibe-coding homework: build a website explaining one concept
- [ ] Track participation — nudge quiet participants after week 2
- [ ] Highlight exceptional student work on social media (with permission)

### After the Cohort

- [ ] Host graduation call with individualised next-step plans
- [ ] Connect graduates to Good First Issues
- [ ] Track graduate contributions over 3-6 months
- [ ] Feed data into PR Tracking Dashboard
- [ ] Invite top graduates to TA for the next cohort

---

## Outcomes (Cohort 1: Feb-Apr 2026)

| Metric | Value |
|--------|-------|
| Registrants | 49 |
| Graduates | 21 |
| Completion rate | ~43% |
| Partner | Chaincode Labs (BOSS Challenge) |
| Graduates pursuing Good First Issues | Multiple |
| Graduates joining rawBit cohort | In progress |
| Graduates joining Code Orange workshops | In progress |

---

## License

CC0 1.0 Universal. Public domain. Fork it, translate it, teach with it.
