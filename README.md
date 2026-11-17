# Code Orange Dev School - Curriculum

> **Free, open-source Bitcoin developer education for Southeast Asia and beyond.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## About This Repository

This is the master curriculum repository for [Code Orange Dev School](https://codeorange.dev), a Bitcoin-only developer education program. It contains everything an educator needs to fork this repo and run their own Bitcoin developer cohort, anywhere in the world, in any language.

All materials are released under **CC0 1.0 Universal (Public Domain)** - use them, adapt them, translate them, teach with them. No permission needed.

---

## Programs

### Recommended Learning Path

```
Bitcoin Dojo (7 weeks) ──> rawBit (10 weeks) ──> Decoding Bitcoin (10 weeks) ──> Open-source contribution
        │                                                                          ▲
        └── Sovereign Bitcoiner (5-10 weeks)       Privacy Track (drop-in, biweekly) ─┘
```

| Program | Duration | Level | Directory |
|---------|----------|-------|-----------|
| **Bitcoin Dojo** | 7 weeks | Beginner-Intermediate | [`/bitcoin-dojo/`](./bitcoin-dojo/) |
| **rawBit Study Cohort** | 10 weeks | Intermediate | [`/rawbit/`](./rawbit/) |
| **Decoding Bitcoin** | 10 weeks | Intermediate | [`/decoding-bitcoin/`](./decoding-bitcoin/) |
| **Sovereign Bitcoiner Crash Course** | 5-10 weeks | Beginner-Intermediate | [`/sovereign-bitcoiner/`](./sovereign-bitcoiner/) |
| **Privacy Track** | 12 biweekly sessions, drop-in | Intermediate | [`/privacy-track/`](./privacy-track/) |
| **Vibe Coding on Nostr** | Monthly workshops | All levels | [`/nostr-workshops/`](./nostr-workshops/) |
| **Workshop Modules** | Single session | Varies | [`/workshops/`](./workshops/) |

---

## How to Use This Curriculum

### For Educators

1. **Fork this repo** to your own GitHub account or organisation
2. **Pick a program** - start with Decoding Bitcoin if you have developers, or Sovereign Bitcoiner for general Bitcoiners
3. **Follow the week-by-week syllabus** - each week has readings, exercises, discussion questions, and assessments
4. **Adapt for your context** - translate materials, adjust pacing, add local examples
5. **Run your cohort** - use the Facilitator Guide in each program directory for logistics and best practices

### For Self-Learners

1. **Start with Week 1** of any program
2. **Complete the readings** before attempting exercises
3. **Try the exercises** - they're designed to be hands-on, not theoretical
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
│   ├── lib/, data/                    # Shared helpers and real mainnet transactions
│   └── week-01/ ... week-07/          # exercises/, solutions/ and a check.py grader per week
├── rawbit/                            # 10-week raw transaction building cohort
│   ├── README.md                      # Program overview, syllabus & facilitator guide
│   └── week-01/ ... week-10/          # Week page; exercises/ and solutions/ still to come
├── decoding-bitcoin/                  # 10-week study cohort on Decoding Bitcoin (bitcoindevs.xyz)
│   ├── README.md                      # Syllabus, schedule & facilitator guide
│   ├── after-the-cohort.md            # Bitcoin Core architecture & first contribution
│   ├── lib/, data/                    # Python lab helpers and real mainnet transactions
│   └── week-01/ ... week-10/          # README, exercises/, solutions/, slides/, notes/
├── privacy-track/                     # The Privacy Sessions: 12 drop-in sessions + labs
│   ├── README.md, SESSIONS.md         # Overview and session plans (starts with Silent Payments)
│   └── labs/                          # Offline Python labs (BIP352 vectors, chain analysis, ...)
├── sovereign-bitcoiner/               # 5-10 week crash course
│   ├── README.md                      # Syllabus
│   └── week-01/ ... week-05/          # One page per week (topics, hands-on, recaps)
├── nostr-workshops/                   # Monthly workshop modules
│   ├── README.md
│   └── modules/01-... 06-.../         # One self-contained workshop guide per module
├── workshops/                         # Standalone 2-3 hour workshops, one facilitator guide each
│   └── btcpay/ ecash/ mining/ multisig/ nodes/ nostr/ privacy/
├── resources/                         # Shared resources
│   ├── reading-list.md
│   └── tools-and-software.md
└── tools/
    └── check_links.py                 # CI check: every relative link and #heading resolves
```

---

## Upstream Resources

This curriculum builds on these open-source Bitcoin education resources:

- [Chaincode Labs Bitcoin Curriculum](https://github.com/chaincodelabs/bitcoin-curriculum) - Protocol development study groups
- [Bitcoin Dev Project](https://bitcoindevs.xyz/) - Developer onboarding and learning paths
- [Mastering Bitcoin](https://github.com/bitcoinbook/bitcoinbook) by Andreas Antonopoulos - Foundational textbook
- [Learn Bitcoin from the Command Line](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line) - Hands-on CLI tutorials
- [Bitcoin Optech](https://bitcoinops.org/) - Weekly technical newsletter

---

## Community

- **Website**: [codeorange.dev](https://codeorange.dev)
- **GitHub**: [github.com/code-orange-dev](https://github.com/code-orange-dev)
- **Discord**: [discord.gg/xd6dmPF9bA](https://discord.gg/xd6dmPF9bA)
- **X**: [@CodeOrangeDevs](https://x.com/CodeOrangeDevs)

---

## License

This work is dedicated to the public domain under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). No rights reserved. We build in the open because Bitcoin is built in the open.
