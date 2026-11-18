# Code Orange Dev School - Curriculum

> **Free, open-source Bitcoin developer education for Southeast Asia and beyond.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Labs](https://github.com/code-orange-dev/curriculum/actions/workflows/labs.yml/badge.svg)](https://github.com/code-orange-dev/curriculum/actions/workflows/labs.yml)
[![Bitcoin Dojo](https://github.com/code-orange-dev/curriculum/actions/workflows/dojo.yml/badge.svg)](https://github.com/code-orange-dev/curriculum/actions/workflows/dojo.yml)
[![Good first issues](https://img.shields.io/github/issues/code-orange-dev/curriculum/good%20first%20issue?label=good%20first%20issues&color=7057ff)](https://github.com/code-orange-dev/curriculum/labels/good%20first%20issue)

**Start here:** [Decoding Bitcoin, week 1](./decoding-bitcoin/week-01/) · [All programs](#programs) · [Facilitator slides](https://code-orange-dev.github.io/curriculum/) · [Contribute](#contributing)

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

| Program | Duration | Level | What's inside |
|---------|----------|-------|---------------|
| **[Decoding Bitcoin](./decoding-bitcoin/)** | 10 weeks | Intermediate | Week guides, slides, notes, model answers, regtest labs tested on Bitcoin Core, Python labs |
| **[Bitcoin Dojo](./bitcoin-dojo/)** | 7 weeks | Beginner-Intermediate | Python exercises with self-grading checks against real mainnet transactions |
| **[Privacy Track](./privacy-track/)** | 12 biweekly sessions, drop-in | Intermediate | Session plans and offline labs (Silent Payments test vectors, chain analysis, coin selection) |
| **[rawBit Study Cohort](./rawbit/)** | 10 weeks | Intermediate | Syllabus and week pages (exercises wanted, see good first issues) |
| **[Sovereign Bitcoiner](./sovereign-bitcoiner/)** | 5-10 weeks | Beginner | Syllabus, week pages and recaps of past sessions |
| **[Workshops](./workshops/)** | 2-3 hours each | Beginner | Facilitator guides: multisig, nodes, mining, BTCPay, ecash, Nostr, privacy |
| **[Vibe Coding on Nostr](./nostr-workshops/)** | Monthly | All levels | 6 developer workshop modules with working code |

---------|----------|-------|-----------|
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

### Contributing

Found a mistake, or ran a lab and something didn't match? That is the most useful contribution there is.

- **Small fix:** open a pull request. The template has a short checklist.
- **Not sure how to fix it:** [open an issue](https://github.com/code-orange-dev/curriculum/issues/new/choose). There are forms for broken labs, unclear writing and new ideas.
- **Want something to work on:** pick a [good first issue](https://github.com/code-orange-dev/curriculum/labels/good%20first%20issue).

More in [`CONTRIBUTING.md`](./CONTRIBUTING.md). What changed recently is in the [changelog](./CHANGELOG.md).

### Thank you

Thanks to everyone who has tested labs, fixed mistakes and proposed workshops, including [Itokichi0000](https://github.com/Itokichi0000) and [RazorBest](https://github.com/RazorBest). See all [contributors](https://github.com/code-orange-dev/curriculum/graphs/contributors).

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
    ├── check_links.py                 # CI check: every relative link and #heading resolves
    └── build_slides_site.py           # Index page for the slides website (built by CI)
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
