# Code Orange Dev School — Curriculum

> **Free, open-source Bitcoin developer education for Southeast Asia and beyond.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## About This Repository

This is the master curriculum repository for [Code Orange Dev School](https://codeorange.dev) — Asia's Bitcoin Developer Pipeline. It contains everything an educator needs to fork this repo and run their own Bitcoin developer cohort, anywhere in the world, in any language.

All materials are released under **CC0 1.0 Universal (Public Domain)** — use them, adapt them, translate them, teach with them. No permission needed.

---

## Programs

### Recommended Learning Path

```
Bitcoin Dojo (7 weeks) ──> rawBit (10 weeks) ──> Decoding Bitcoin (8 weeks)
        │                                                │
        └── Sovereign Bitcoiner (5-10 weeks)             └── Open-source contribution
```

| Program | Duration | Level | Directory |
|---------|----------|-------|-----------|
| **Bitcoin Dojo** | 7 weeks | Beginner-Intermediate | [`/bitcoin-dojo/`](./bitcoin-dojo/) |
| **rawBit Study Cohort** | 10 weeks | Intermediate | [`/rawbit/`](./rawbit/) |
| **Decoding Bitcoin** | 8 weeks | Intermediate-Advanced | [`/decoding-bitcoin/`](./decoding-bitcoin/) |
| **Sovereign Bitcoiner Crash Course** | 5-10 weeks | Beginner-Intermediate | [`/sovereign-bitcoiner/`](./sovereign-bitcoiner/) |
| **Vibe Coding on Nostr** | Monthly workshops | All levels | [`/nostr-workshops/`](./nostr-workshops/) |
| **Workshop Modules** | Single session | Varies | [`/workshops/`](./workshops/) |

---

## How to Use This Curriculum

### For Educators

1. **Fork this repo** to your own GitHub account or organisation
2. **Pick a program** — start with Decoding Bitcoin if you have developers, or Sovereign Bitcoiner for general Bitcoiners
3. **Follow the week-by-week syllabus** — each week has readings, exercises, discussion questions, and assessments
4. **Adapt for your context** — translate materials, adjust pacing, add local examples
5. **Run your cohort** — use the Facilitator Guide in each program directory for logistics and best practices

### For Self-Learners

1. **Start with Week 1** of any program
2. **Complete the readings** before attempting exercises
3. **Try the exercises** — they're designed to be hands-on, not theoretical
4. **Join our Discord** for peer support: [discord.gg/xd6dmPF9bA](https://discord.gg/xd6dmPF9bA)

### For Contributors

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to submit improvements, translations, or new modules.

---

## Repository Structure

```
curriculum/
├── README.md                          # This file
├── LICENSE                            # CC0 1.0 Universal
├── CONTRIBUTING.md                    # How to contribute
├── bitcoin-dojo/                      # 7-week cryptography & primitives cohort
│   ├── README.md                      # Program overview, syllabus & facilitator guide
│   ├── week-01/                       # Finite Fields
│   ├── week-02/                       # Elliptic Curves
│   ├── week-03/                       # Keys, Addresses & Encoding
│   ├── week-04/                       # Serialisation & Transactions
│   ├── week-05/                       # Script & Transaction Validation
│   ├── week-06/                       # SegWit & Advanced Transactions
│   └── week-07/                       # Graduation & Next Steps
├── rawbit/                            # 10-week raw transaction building cohort
│   ├── README.md                      # Program overview, syllabus & facilitator guide
│   ├── week-01/                       # Legacy Transactions (P2PK, P2PKH)
│   ├── week-02/                       # Multisig Transactions
│   ├── week-03/                       # Timelocks
│   ├── week-04/                       # OP_RETURN & Data Anchoring
│   ├── week-05/                       # Transaction Malleability & Payment Channels
│   ├── week-06/                       # SegWit (P2WPKH)
│   ├── week-07/                       # SegWit Scripts (P2WSH)
│   ├── week-08/                       # Taproot Basics
│   ├── week-09/                       # Advanced Taproot & MuSig2
│   └── week-10/                       # Final Project & Graduation
├── decoding-bitcoin/                  # 8-week protocol contribution cohort
│   ├── README.md                      # Program overview & facilitator guide
│   ├── week-01-bitcoin-fundamentals/
│   ├── week-02-transactions/
│   ├── week-03-script/
│   ├── week-04-segwit/
│   ├── week-05-taproot/
│   ├── week-06-psbt/
│   ├── week-07-bitcoin-core/
│   └── week-08-contributing/
├── sovereign-bitcoiner/               # 5-10 week crash course
│   ├── README.md
│   ├── week-01-philosophy/
│   ├── week-02-nodes/
│   ├── week-03-mining/
│   ├── week-04-multisig/
│   └── week-05-privacy/
├── nostr-workshops/                   # Monthly workshop modules
│   ├── README.md
│   └── modules/
├── workshops/                         # Standalone workshop slides & guides
│   ├── mining/
│   ├── multisig/
│   ├── nodes/
│   ├── privacy/
│   ├── ecash/
│   ├── btcpay/
│   └── nostr/
└── resources/                         # Shared resources
    ├── seed-phrase-backup-sheet.pdf
    ├── reading-list.md
    └── tools-and-software.md
```

---

## Upstream Resources

This curriculum builds on world-class open-source Bitcoin education:

- [Chaincode Labs Bitcoin Curriculum](https://github.com/chaincodelabs/bitcoin-curriculum) — Protocol development study groups
- [Bitcoin Dev Project](https://bitcoindevs.xyz/) — Developer onboarding and learning paths
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook) by Andreas Antonopoulos — Foundational textbook
- [Learn Bitcoin from the Command Line](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line) — Hands-on CLI tutorials
- [Bitcoin Optech](https://bitcoinops.org/) — Weekly technical newsletter

---

## Community

- **Website**: [codeorange.dev](https://codeorange.dev)
- **GitHub**: [github.com/code-orange-dev](https://github.com/code-orange-dev)
- **Discord**: [discord.gg/xd6dmPF9bA](https://discord.gg/xd6dmPF9bA)
- **X**: [@CodeOrangeDevs](https://x.com/CodeOrangeDevs)

---

## License

This work is dedicated to the public domain under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). No rights reserved. We build in the open because Bitcoin is built in the open.
