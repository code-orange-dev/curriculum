# Bitcoin Privacy Developer Track

> 12 sessions + capstone. From chain analysis fundamentals to contributing to Silent Payments, Payjoin, and privacy-preserving wallet development. The most comprehensive open-source Bitcoin privacy curriculum available.

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Why This Track Exists

Bitcoin's privacy infrastructure — Silent Payments, Payjoin, CoinSwap — is being built almost entirely by developers in North America and Europe. Southeast Asia has 700M+ people and growing Bitcoin adoption, but zero structured programs that train developers to contribute to privacy-focused open-source projects.

This track changes that. Graduates will understand how on-chain surveillance works, implement privacy protocols from scratch in both Python and Rust, and contribute code to the projects that make Bitcoin more private for everyone.

**Built by [Code Orange Dev School](https://codeorange.dev) in Bali, Indonesia.** Open-sourced under CC0 for any community to use.

---

## What's Included

```
privacy-track/
├── README.md                          ← You are here
├── FACILITATOR_GUIDE.md               ← Session-by-session plans with timing
├── CONTRIBUTING.md                    ← How to improve this curriculum
│
├── module-01-chain-analysis/
│   ├── README.md                      ← 2 sessions: surveillance heuristics + privacy philosophy
│   └── exercises/
│       └── chain_analysis_lab.py      ← 6 exercises: CIOH, change detection, wallet fingerprinting,
│                                         CoinJoin detection, full TX analysis, entity tracing
│
├── module-02-silent-payments/
│   ├── README.md                      ← 4 sessions: BIP352 theory → implementation → contribution
│   └── exercises/
│       ├── silent_payments_sender.py  ← 4 exercises: keypair generation, ECDH shared secret,
│       │                                 output key derivation, full SP simulation
│       └── silent_payments_scanner.py ← 3 exercises: scan transaction, scan block,
│                                         benchmark scanning performance
│
├── module-03-payjoin/
│   ├── README.md                      ← 3 sessions: BIP77/78 theory → PDK integration → contribution
│   └── exercises/
│       ├── payjoin_testnet.md         ← Step-by-step regtest Payjoin with bitcoin-cli
│       └── pdk_integration/           ← Rust project: full Payjoin with PDK
│           ├── Cargo.toml
│           └── src/main.rs            ← 5 exercises: environment setup, PSBT creation,
│                                         receiver modification, sender verification, analysis
│
├── module-04-wallet-privacy/
│   ├── README.md                      ← 3 sessions: coin selection, CBF, CoinJoin/CoinSwap/future
│   └── exercises/
│       ├── coin_selection_simulator.py  ← 6 exercises: 4 algorithms + privacy scoring + comparison
│       └── compact_block_filters.py     ← 5 exercises: Golomb-Rice coding, build filter,
│                                           query filter, measure properties, SP+CBF simulation
│
├── capstone/
│   └── README.md                      ← 4 project tracks with rubrics and proposal template
│
└── resources/
    ├── reading-list.md                ← 40+ papers, specs, and articles organized by module
    └── glossary.md                    ← 35+ technical terms with full definitions
```

**Total: 29 coding exercises across 7 exercise files, 12 session plans, 4 capstone tracks, 40+ readings.**

---

## Prerequisites

- Completed [Bitcoin Dojo](../bitcoin-dojo/) or [Decoding Bitcoin](../decoding-bitcoin/) (or equivalent foundational course)
- Comfortable reading Python and Rust
- Understanding of Bitcoin transactions, Script, ECDSA, and basic elliptic curve math
- A regtest/signet environment (Bitcoin Core installed)
- Rust toolchain installed (`rustup`)

---

## Track Structure

| Module | Sessions | Topic | Exercises |
|--------|----------|-------|-----------|
| [Module 1](module-01-chain-analysis/) | 2 | Chain Analysis & Why Privacy Matters | 6 (Python) |
| [Module 2](module-02-silent-payments/) | 4 | Silent Payments — BIP352 | 7 (Python) |
| [Module 3](module-03-payjoin/) | 3 | Payjoin — BIP77/78 | 8 (bash + Rust) |
| [Module 4](module-04-wallet-privacy/) | 3 | Privacy-Preserving Wallet Development | 11 (Python) |
| [Capstone](capstone/) | 3-4 weeks | Independent Project | 1 (your choice) |
| **Total** | **12 + capstone** | | **32+ exercises** |

---

## Learning Path

```
Module 1: Chain Analysis (2 sessions)
  │  Exercises: chain_analysis_lab.py (CIOH, change detection, wallet
  │  fingerprinting, CoinJoin detection, entity tracing)
  ↓  "I understand how Bitcoin surveillance works — and its weaknesses"

Module 2: Silent Payments (4 sessions)
  │  Exercises: silent_payments_sender.py, silent_payments_scanner.py
  │  (ECC from scratch, ECDH, BIP352 key derivation, scanning benchmarks)
  ↓  "I can implement BIP352 and contribute to real implementations"

Module 3: Payjoin (3 sessions)
  │  Exercises: payjoin_testnet.md, pdk_integration/ (Rust)
  │  (Manual PSBT construction, PDK API, sender verification, ambiguity analysis)
  ↓  "I can build with Payjoin Dev Kit and contribute to payjoin-rust"

Module 4: Wallet Privacy (3 sessions)
  │  Exercises: coin_selection_simulator.py, compact_block_filters.py
  │  (4 coin selection algorithms, Golomb-Rice coding, BIP158 filters,
  │   privacy scoring, Silent Payments + CBF integration)
  ↓  "I understand coin selection, compact block filters, and CoinJoin"

Capstone Project (3-4 weeks)
  │  Track A: Code contribution (PR to a privacy repo)
  │  Track B: Privacy analysis tool
  │  Track C: Research and documentation
  │  Track D: Education and curriculum extension
  ↓  "I've shipped real work to Bitcoin's privacy infrastructure"
```

---

## Target Outcomes

By the end of this track, each participant will:

1. **Analyze** real Bitcoin transactions using the same heuristics chain analysis firms use — and identify where those heuristics fail
2. **Implement** a complete Silent Payments sender and scanner from scratch in Python, including ECDH key exchange and BIP352 key derivation
3. **Build** a Payjoin transaction in both bash (manual PSBT) and Rust (Payjoin Dev Kit), understanding every verification step
4. **Evaluate** coin selection algorithms for privacy trade-offs and build/query compact block filters (BIP158) from scratch
5. **Contribute** at least 1 PR to a privacy-related Bitcoin open-source project
6. **Complete** a capstone project demonstrating professional-level understanding

---

## Target Contribution Repos

Graduates will be guided to contribute to these projects:

| Project | Language | What It Does | Contribution Areas |
|---------|----------|-------------|-------------------|
| [Bitcoin Core #28122](https://github.com/bitcoin/bitcoin/pull/28122) | C++ | Silent Payments implementation | Test vectors, review, documentation |
| [rust-silentpayments](https://github.com/cygnet3/rust-silentpayments) | Rust | Silent Payments library | API improvements, test coverage, label support |
| [payjoin-rust](https://github.com/payjoin/rust-payjoin) | Rust | Payjoin Dev Kit (BIP77/78) | Integration tests, V2 features, documentation |
| [rust-bitcoin](https://github.com/rust-bitcoin/rust-bitcoin) | Rust | Foundational Bitcoin library | Taproot utilities, PSBT improvements |
| [BDK](https://github.com/bitcoindevkit/bdk) | Rust | Bitcoin Development Kit | Coin selection, SP integration, privacy scoring |
| [Floresta](https://github.com/Davidson-Souza/Floresta) | Rust | Utreexo-based full node | CBF support, testing |
| [Kyoto](https://github.com/rustaceanrob/kyoto) | Rust | BIP157/158 light client | SP scanning integration, performance |
| [BTCPay Server](https://github.com/btcpayserver/btcpayserver) | C# | Merchant payments (Payjoin) | BIP77 V2, UX improvements |

---

## Key Resources

### Specifications

- [BIP352: Silent Payments](https://bips.dev/352/)
- [BIP78: Payjoin V1](https://bips.dev/78/)
- [BIP77: Payjoin V2](https://github.com/bitcoin/bips/blob/master/bip-0077.mediawiki)
- [BIP157: Client Side Block Filtering](https://bips.dev/157/)
- [BIP158: Compact Block Filters](https://bips.dev/158/)

### Reading

See the full [Reading List](resources/reading-list.md) (40+ resources organized by module).

### Reference

See the [Glossary](resources/glossary.md) (35+ technical terms with full definitions).

### Tools

- [OXT.me](https://oxt.me/) — On-chain transaction analysis
- [mempool.space](https://mempool.space/) — Block explorer with transaction visualization
- [Payjoin Dev Kit](https://payjoin.org/) — Rust library for Payjoin integration
- [rawBit](https://github.com/rawBit-io/rawbit) — Visual transaction builder and Script debugger

---

## Schedule

| Week (Intensive) | Week (Standard) | Session | Exercises Due |
|-------------------|-----------------|---------|---------------|
| Week 1 | Weeks 1-2 | Module 1: Sessions 1-2 | chain_analysis_lab.py + essay |
| Weeks 2-3 | Weeks 3-6 | Module 2: Sessions 1-4 | sender.py + scanner.py + 1st PR |
| Weeks 4-5 | Weeks 7-9 | Module 3: Sessions 1-3 | payjoin_testnet.md + pdk_integration + 2nd PR |
| Week 6 | Weeks 10-12 | Module 4: Sessions 1-3 | coin_selection.py + cbf.py + final report |
| Weeks 7-10 | Weeks 13-16 | Capstone Project | Capstone deliverable + presentation |

---

## For Facilitators

See the complete [Facilitator Guide](FACILITATOR_GUIDE.md) with:

- Minute-by-minute session plans for all 12 sessions
- Common problems and solutions
- Assessment framework with rubrics
- Guest speaker suggestions (Josie Baker, Dan Gould, Ruben Somsen, Murch, and more)
- Post-track contribution sprint guidance
- Success metrics for grant reporting

---

## For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to improve this curriculum. We especially welcome:

- Exercises in additional languages (Rust, Go, TypeScript)
- Translations (Indonesian, Thai, Vietnamese, Japanese)
- Reference implementations / solution keys
- Additional modules (Lightning privacy, eCash, Nostr)

---

## License

All materials in this track are released under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). Use them freely. No attribution required. Build Bitcoin privacy education everywhere.

---

*Code Orange Dev School | [codeorange.dev](https://codeorange.dev) | [github.com/code-orange-dev](https://github.com/code-orange-dev)*
