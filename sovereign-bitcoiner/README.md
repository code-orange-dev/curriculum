# Sovereign Bitcoiner Crash Course — 5-10 Week Program

> **A hands-on deep-dive for Bitcoiners who want to take full control of their Bitcoin stack.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Overview

The Sovereign Bitcoiner Crash Course takes curious Bitcoiners and transforms them into fully self-sovereign node operators, miners, and privacy advocates. Every graduate leaves with deployed, working systems — a running full node, a BTCPay server, a multisig inheritance plan, and the knowledge to defend their Bitcoin stack against both digital and physical threats.

## Prerequisites

- Basic Bitcoin knowledge (what it is, how to buy/send/receive)
- A laptop and willingness to work with command-line tools
- No coding experience required

## Format

| Component | Details |
|-----------|---------|
| **Duration** | 5-10 weeks (adjustable based on pacing) |
| **Time commitment** | 4-6 hours per week |
| **Sessions** | Weekly in-person workshops + self-study |
| **Group size** | 10-30 participants |
| **Hardware** | BitAxe (provided or BYOD), hardware signers recommended |

---

## Week-by-Week Syllabus

### Week 1: Bitcoin Philosophy & Why Sovereignty Matters

**Topics:**
- Why run a node? Why self-custody? Why privacy?
- Threat modelling: governments, exchanges, hackers, the $5 wrench attack
- Bitcoin as a tool for human rights and financial freedom
- History of financial censorship in Southeast Asia

**Readings:**
- The Bitcoin Standard, Chapters 1-3 (Ammous) — or selected excerpts
- [Why Run a Full Node](https://bitcoin.org/en/full-node)
- Alex Gladstein: "Check Your Financial Privilege"

**Activities:**
- Group discussion: What does financial sovereignty mean in your country?
- Threat modelling exercise: Identify your personal threat model

---

### Week 2: Running a Full Node

**Topics:**
- What a full node does and why it matters for the network
- Bitcoin Core vs Umbrel vs other node packages
- Setting up and syncing a full node
- Connecting your wallet to your own node

**Hands-On:**
1. Install Umbrel (or Bitcoin Core directly) on a Raspberry Pi or old laptop
2. Start the initial block download (IBD)
3. Explore the node dashboard — mempool, peers, block height
4. Connect a mobile wallet (e.g., BlueWallet) to your own node via Tor

**Hardware Needed:**
- Raspberry Pi 4 (4GB+) or old laptop, 1TB+ SSD, Ethernet cable

---

### Week 3: Bitcoin Mining

**Topics:**
- How mining works: proof-of-work, difficulty adjustment, block rewards
- Solo mining vs pool mining vs Stratum V2
- Open-source mining hardware: BitAxe
- Mining economics and why hash rate decentralisation matters

**Hands-On:**
1. Assemble and configure a BitAxe miner
2. Connect to a mining pool (or solo mine on regtest)
3. Configure Braiins OS (or equivalent open-source firmware)
4. Monitor hash rate and understand mining statistics

**Hardware Needed:**
- BitAxe (provided at in-person workshops)

---

### Week 4: Multisig & Key Management

**Topics:**
- Single-sig vs multisig: threat models and trade-offs
- 2-of-3 multisig setup for personal security
- Hardware signers: SeedSigner, Coldcard, Trezor
- Seed phrase security: metal backups, geographic distribution
- Inheritance planning: how your family recovers your Bitcoin

**Hands-On:**
1. Build a SeedSigner from a Raspberry Pi Zero
2. Create a 2-of-3 multisig wallet using Nunchuk (or Sparrow)
3. Practice a full recovery: wipe one signer, recover using the other two
4. Write an inheritance plan: letter to your family, key distribution strategy

**Hardware Needed:**
- 2-3 hardware signers (SeedSigner DIY, or Coldcard/Trezor)
- Metal seed backup plates

---

### Week 5: Privacy & Advanced Tools

**Topics:**
- Why Bitcoin privacy matters (fungibility, surveillance, censorship)
- CoinJoin and PayJoin
- eCash: Fedimint and Cashu — chaumian e-cash on Bitcoin
- Tor integration for node and wallet traffic
- BTCPay Server: accepting Bitcoin payments without a third party

**Hands-On:**
1. Set up Tor on your node
2. Deploy a BTCPay Server instance (self-hosted or cloud)
3. Create a Cashu mint or join a Fedimint federation (testnet)
4. Send a PayJoin transaction (testnet or regtest)

---

## After the Course

Graduates are equipped to:
- Run their own full node permanently
- Manage their Bitcoin with multisig self-custody
- Accept Bitcoin payments via BTCPay Server
- Understand and use privacy tools
- Teach others — become a local Bitcoin educator

---

## Facilitator Guide

### Materials Needed
- [ ] Raspberry Pi 4 + SSD (one per participant, or shared)
- [ ] BitAxe miners (one per 2-3 participants)
- [ ] SeedSigner kits (Raspberry Pi Zero + camera + screen)
- [ ] Seed phrase backup sheets (see `/resources/`)
- [ ] Printed facilitator notes for each week

### Tips
- Start with philosophy (Week 1) to establish motivation before diving into technical content
- Let participants struggle with setup — the debugging process is part of the learning
- Use regtest/testnet for all exercises to avoid financial risk
- Celebrate every working node, every successful multisig recovery

---

## License

CC0 1.0 Universal. Public domain. Use freely.
