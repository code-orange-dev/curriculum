# Decoding Bitcoin - 10-Week Developer Study Cohort

> **A guided study cohort through [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project: from how a transaction lives to building and spending your own Taproot output.**

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-orange.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Overview

Decoding Bitcoin is a 10-week study cohort for developers. Participants work through the free lessons, tools and coding exercises of [Decoding Bitcoin](https://bitcoindevs.xyz/decoding), made by [The Bitcoin Dev Project](https://bitcoindevs.xyz/), and meet once a week to discuss what they learned.

The lessons live on Decoding Bitcoin, and we link to them rather than copy them. This folder is the study guide around those lessons: for every week there are discussion questions, hands-on exercises, model answers, facilitator slides and notes. All of it is our own work and is released as CC0, so you can fork it and run your own cohort.

## Prerequisites

- Comfortable reading and writing code in at least one language (Python or JavaScript is enough for the exercises)
- Curiosity about how Bitcoin works under the hood. No prior Bitcoin development experience is needed
- Optional, for the hands-on labs: [Bitcoin Core](https://bitcoincore.org/en/download/) running on regtest (week 1 shows you how) and Python 3.8+

## Format

| Component | Details |
|-----------|---------|
| **Duration** | 10 weeks |
| **Time commitment** | 3-5 hours per week (lessons, exercises and the session) |
| **Weekly session** | One 90-minute group session, run as a Socratic seminar |
| **Group size** | 10-25 participants |
| **Each week** | Lessons on Decoding Bitcoin, one discussion question you own, 3 exercises |
| **Final project** | Build and spend a Taproot (P2TR) output (week 10) |

### How a week works

1. **Before the session:** read the week's lessons on Decoding Bitcoin, do the exercises and prepare the discussion question assigned to you.
2. **At the session:** the opening question, then everyone explains their own question and the group pushes back. One person shares their screen and walks through an exercise.
3. **After the session:** the Summariser posts the key takeaways and open questions in the cohort's Discord channel.

Week 1 is an intro week: participants just turn up, and homework starts in week 2.

### Seminar roles

Roles rotate through the group every week.

| Role | Job |
|---|---|
| **Facilitator** | Keeps time, asks the opening question and brings in quiet voices. Guides, doesn't lecture. |
| **Summariser** | Notes the key takeaways and open questions, and posts them on Discord within a day. |
| **Devil's advocate** | Steelmans the other side and asks "why not do it differently?" |
| **Exercise driver** | Shares their screen and walks the group through one of the hands-on exercises. |

---

## Schedule at a glance

Dates are for Code Orange's 2026-27 cohort (Mondays, 7pm UTC+8). Change them for your own cohort.

| Week | Date | Topic | Decoding Bitcoin lessons |
|---|---|---|---|
| [1](./week-01/) | 16 Nov | [Orientation and foundations](#week-1-orientation-and-foundations) | Welcome!, Bitcoin History, UTXO vs Account Models |
| [2](./week-02/) | 23 Nov | [How a transaction lives](#week-2-how-a-transaction-lives) | Transactions roadmap, Transaction Lifecycle, Transaction Structure (first read: the main parts) |
| [3](./week-03/) | 30 Nov | [Inside a transaction, byte by byte](#week-3-inside-a-transaction-byte-by-byte) | Technical Foundation, Transaction Structure (second read: every field) |
| [4](./week-04/) | 7 Dec | [Building a transaction and paying the fee](#week-4-building-a-transaction-and-paying-the-fee) | Creating a Transaction, Fee Calculation |
| [5](./week-05/) | 14 Dec | [Signing and the transaction exercises](#week-5-signing-and-the-transaction-exercises) | Signing Transactions, Exercises (GitHub Classroom) |
| [6](./week-06/) | 21 Dec | [Script basics](#week-6-script-basics) | Scripts overview, P2PK: Pay To Public Key, P2PKH: Pay To Public Key Hash |
| [7](./week-07/) | 28 Dec | [P2SH and multisig](#week-7-p2sh-and-multisig) | P2SH: Pay To Script Hash (BIP 16), P2MS: Pay To Multisig |
| [8](./week-08/) | 4 Jan | [Project: build your own Bitcoin stack](#week-8-project-build-your-own-bitcoin-stack) | Project: Build your own bitcoin Stack |
| [9](./week-09/) | 11 Jan | [Taproot: keys and Schnorr](#week-9-taproot-keys-and-schnorr) | Introduction to Taproot, Pay to Taproot, Schnorr & BIP340, Key-path Taproot |
| [10](./week-10/) | 18 Jan | [Taproot scripts and graduation](#week-10-taproot-scripts-and-graduation) | Script-path Taproot, Taproot Signatures, Capstone: Build & Spend a P2TR |

After week 10, graduates continue with [After the cohort](./after-the-cohort.md): Bitcoin Core architecture, reviewing pull requests and making a first open-source contribution.

## What's in each week folder

```
week-NN/
├── README.md        # The week at a glance: lessons, opening question, discussion questions, exercises
├── exercises/       # Hands-on exercises, plus bitcoin-cli labs on regtest (and Python labs in weeks 3-4)
├── solutions/       # Model answers to every question and exercise (try first!)
├── slides/          # Facilitator slides for the 90-minute session (Marp markdown)
└── notes/           # Key ideas, common mix-ups, a session plan, glossary and resources
```

### Presenting the slides

Each `slides/slides.md` is a [Marp](https://marp.app/) deck: plain markdown that reads fine on GitHub and turns into real slides.

- **VS Code:** install the "Marp for VS Code" extension, open `slides.md` and click the preview icon.
- **Command line:** `npx @marp-team/marp-cli@latest week-02/slides/slides.md --pdf` (or `--html`, `--pptx`).

Speaker notes are written as `<!-- comments -->` under each slide and show up in Marp's presenter view.

### Regtest labs

Every week's bitcoin-cli lab was run end to end on Bitcoin Core 29.0 (regtest) in November 2026, and the numbers in `solutions/` are measured, not estimated. Signatures can be 1 byte shorter now and then, so your sizes may differ by a byte. Running a newer version and something changed? Please open an issue or a pull request.

### Python labs

Weeks 3 and 4 have small Python labs graded against real mainnet transactions. Run them from this folder with plain Python 3.8+ (no installs):

```bash
python3 week-03/check.py              # parse a real transaction, compute its txid and wtxid
python3 week-04/check.py              # weight, vsize, fee and fee rate
python3 week-03/check.py --solution   # see the reference solution pass
```

---

## Week-by-Week Syllabus

### Week 1: Orientation and foundations

**Opening question:** If you had to explain Bitcoin to a friend in two sentences, what would you say, and what would you leave out?

Intro week. Meet the cohort, learn how the dashboard works and get comfortable on Decoding Bitcoin. The lessons below are a gentle start: the welcome, Bitcoin's history, and how Bitcoin keeps track of who owns what (coins, called UTXOs, not account balances). Read them after the session if you like. **Intro week: no homework before the session.**

**Lessons:**

- [Welcome!](https://bitcoindevs.xyz/decoding/welcome)
- [Bitcoin History](https://bitcoindevs.xyz/decoding/bitcoin-history)
- [UTXO vs Account Models](https://bitcoindevs.xyz/decoding/utxo)

**Discussion questions:**

1. What problem did Bitcoin solve that earlier digital cash attempts (DigiCash, b-money, Bit Gold) could not?
2. Pick one moment from the Bitcoin History lesson and explain why it mattered for how Bitcoin works today.
3. What is a hash function? Name three properties Bitcoin relies on and where each one shows up.
4. Explain the UTXO model in your own words. Why is there no account balance stored anywhere?
5. Give one advantage and one disadvantage of UTXOs compared with an account model.
6. Why do people say "don't trust, verify"? What can you verify yourself, and what do you usually take on trust?

**Week folder:** [`week-01/`](./week-01/) · [exercises](./week-01/exercises/README.md) · [slides](./week-01/slides/slides.md) · [notes](./week-01/notes/README.md) · [solutions](./week-01/solutions/README.md)

---

### Week 2: How a transaction lives

**Opening question:** When is a bitcoin payment actually final, and who gets to decide?

Follow a payment from the wallet that builds it, through the mempool, into a block. Then a first look at what a transaction is made of: version, inputs, outputs and locktime. Next week we go down to the bytes, so don't worry about the byte-level details yet.

**Lessons:**

- [Transactions roadmap](https://bitcoindevs.xyz/decoding/roadmap)
- [Transaction Lifecycle](https://bitcoindevs.xyz/decoding/transaction-lifecycle)
- [Transaction Structure (first read: the main parts)](https://bitcoindevs.xyz/decoding/transaction-structure)

**Discussion questions:**

1. Walk through the lifecycle of a payment: who builds it, who relays it, who checks it, and when is it confirmed?
2. What is the mempool? Why is there no single mempool that everyone shares?
3. What is a chain reorganisation, and why might a merchant wait for more than one confirmation?
4. Why does change go back to the sender as a new output instead of the old output being partly spent?
5. Name the main parts of a transaction in order and say in one line what each one is for.
6. What exactly does an input point to, and why is that enough to prove where the money came from?

**Week folder:** [`week-02/`](./week-02/) · [exercises](./week-02/exercises/README.md) · [slides](./week-02/slides/slides.md) · [notes](./week-02/notes/README.md) · [solutions](./week-02/solutions/README.md)

---

### Week 3: Inside a transaction, byte by byte

**Opening question:** A transaction is just bytes. What do those bytes have to say for everyone to agree it's valid?

A whole week on transaction structure. Learn the byte-level basics (hex, little-endian, compact size), then take a raw transaction apart field by field, including segwit's marker, flag and witness.

**Lessons:**

- [Technical Foundation](https://bitcoindevs.xyz/decoding/technical-foundation)
- [Transaction Structure (second read: every field)](https://bitcoindevs.xyz/decoding/transaction-structure)

**Discussion questions:**

1. What is little-endian, and where does it trip people up when reading a txid?
2. What is a compact size (varint) and why does Bitcoin use one instead of fixed-size counts?
3. What does segwit move into the witness, and why does that fix transaction malleability?
4. What is nLockTime for? Give a real situation where you would set it.
5. What are the segwit marker and flag bytes, and how does a parser know whether a transaction is segwit?
6. How is a txid calculated, and why is a wtxid different?

**Week folder:** [`week-03/`](./week-03/) · [exercises](./week-03/exercises/README.md) · [slides](./week-03/slides/slides.md) · [notes](./week-03/notes/README.md) · [solutions](./week-03/solutions/README.md)

---

### Week 4: Building a transaction and paying the fee

**Opening question:** Who should pay for block space, and how should they decide how much?

Pick inputs, create outputs and work out the fee in sats per virtual byte. See why weight units exist and how fee markets behave.

**Lessons:**

- [Creating a Transaction](https://bitcoindevs.xyz/decoding/transaction-creation)
- [Fee Calculation](https://bitcoindevs.xyz/decoding/fee-calculation)

**Discussion questions:**

1. Where is the fee written in a transaction? (Trick question: explain how it's actually found.)
2. What are weight units and virtual bytes, and why does a witness byte count less?
3. How does a wallet choose which UTXOs to spend? What can go wrong if it chooses badly?
4. What is dust, and why do nodes refuse to relay dust outputs?
5. Explain RBF and CPFP. When would you use each to speed up a stuck payment?
6. Fees were very high in some periods and very low in others. What drives the fee market?

**Week folder:** [`week-04/`](./week-04/) · [exercises](./week-04/exercises/README.md) · [slides](./week-04/slides/slides.md) · [notes](./week-04/notes/README.md) · [solutions](./week-04/solutions/README.md)

---

### Week 5: Signing and the transaction exercises

**Opening question:** A signature proves something very specific. What exactly does it prove, and what doesn't it?

How a transaction gets signed: the sighash, what each sighash flag commits to, and why the signature goes in the input. Then work through the GitHub Classroom exercises.

**Lessons:**

- [Signing Transactions](https://bitcoindevs.xyz/decoding/transaction-signing)
- [Exercises (GitHub Classroom)](https://bitcoindevs.xyz/decoding/transaction_exercises)

**Discussion questions:**

1. What is the sighash (the message that actually gets signed)? Why can't you just sign the whole raw transaction?
2. Compare SIGHASH_ALL, SIGHASH_NONE and SIGHASH_SINGLE. When would anyone use ANYONECANPAY?
3. Why does a segwit signature commit to the amount being spent, and what bug did that fix?
4. What happens if the same nonce is used to sign two different messages with the same key?
5. Where does the signature live in a legacy input versus a segwit input?
6. How can a hardware wallet sign a transaction without ever showing the private key to your computer?

**Week folder:** [`week-05/`](./week-05/) · [exercises](./week-05/exercises/README.md) · [slides](./week-05/slides/slides.md) · [notes](./week-05/notes/README.md) · [solutions](./week-05/solutions/README.md)

---

### Week 6: Script basics

**Opening question:** Why does Bitcoin use a tiny stack language instead of letting people write any program they like?

Bitcoin Script and the stack: how a locking script and an unlocking script run together, starting with the two oldest output types.

**Lessons:**

- [Scripts overview](https://bitcoindevs.xyz/decoding/overview)
- [P2PK: Pay To Public Key](https://bitcoindevs.xyz/decoding/p2pk)
- [P2PKH: Pay To Public Key Hash](https://bitcoindevs.xyz/decoding/p2pkh)

**Discussion questions:**

1. Explain how the stack works by running OP_2 OP_3 OP_ADD OP_5 OP_EQUAL step by step.
2. What is the difference between a scriptPubKey and a scriptSig, and in what order are they run?
3. Why did P2PKH replace P2PK for most payments? Give at least two reasons.
4. Run a P2PKH spend step by step: what is on the stack after each opcode?
5. Why is Script deliberately not Turing complete, and what does it gain from that?
6. Some opcodes were disabled early in Bitcoin's history. Why would you remove features from a running system?

**Week folder:** [`week-06/`](./week-06/) · [exercises](./week-06/exercises/README.md) · [slides](./week-06/slides/slides.md) · [notes](./week-06/notes/README.md) · [solutions](./week-06/solutions/README.md)

---

### Week 7: P2SH and multisig

**Opening question:** Why might you want more than one key to move your bitcoin, and what new risks does that bring?

Bare multisig and why P2SH wrapped it up behind a hash, moving the cost and complexity from the sender to the receiver.

**Lessons:**

- [P2SH: Pay To Script Hash (BIP 16)](https://bitcoindevs.xyz/decoding/p2sh)
- [P2MS: Pay To Multisig](https://bitcoindevs.xyz/decoding/p2ms)

**Discussion questions:**

1. How does P2SH move the cost and complexity of a script from the sender to the receiver?
2. Explain the OP_CHECKMULTISIG off-by-one bug. Why has it never been fixed?
3. Why is bare multisig (P2MS) rarely used today?
4. What is the redeem script, and when does it finally appear on the blockchain?
5. Compare 2-of-3 multisig with a single key plus a backup. Which risks does each protect against?
6. BIP 16 was a soft fork. What does that mean, and how could old nodes still accept P2SH spends?

**Week folder:** [`week-07/`](./week-07/) · [exercises](./week-07/exercises/README.md) · [slides](./week-07/slides/slides.md) · [notes](./week-07/notes/README.md) · [solutions](./week-07/solutions/README.md)

---

### Week 8: Project: build your own Bitcoin stack

**Opening question:** What did you only really understand once you had to build it yourself?

A bigger hands-on build that brings together everything so far: implement a Bitcoin Script stack machine. Work in pairs or small groups and demo it on Monday.

**Lessons:**

- [Project: Build your own bitcoin Stack](https://bitcoindevs.xyz/decoding/project)

**Discussion questions:**

1. How did you represent the stack and opcodes in your code? What would you change next time?
2. How does your stack treat true and false? Compare it with how Bitcoin Script does.
3. Which opcode was hardest to implement, and why?
4. How does your implementation handle a script that fails halfway through?
5. What limits (stack size, script size, opcode count) did you add, and why does Bitcoin have them?
6. Which test cases best convinced you that your stack is correct?

**Week folder:** [`week-08/`](./week-08/) · [exercises](./week-08/exercises/README.md) · [slides](./week-08/slides/slides.md) · [notes](./week-08/notes/README.md) · [solutions](./week-08/solutions/README.md)

---

### Week 9: Taproot: keys and Schnorr

**Opening question:** Taproot makes many different spending setups look the same on-chain. Why is that good for everyone?

Why Taproot happened, how a P2TR output is built, what Schnorr signatures add, and the simple case: spending with a single key.

**Lessons:**

- [Introduction to Taproot](https://bitcoindevs.xyz/decoding/introduction-taproot)
- [Pay to Taproot](https://bitcoindevs.xyz/decoding/p2tr)
- [Schnorr & BIP340](https://bitcoindevs.xyz/decoding/schnorr-bip340)
- [Key-path Taproot](https://bitcoindevs.xyz/decoding/key-path-taproot)

**Discussion questions:**

1. What problems was Taproot designed to solve for privacy, efficiency and flexibility?
2. What is a tweaked public key, and why does P2TR use x-only (32-byte) keys?
3. Compare Schnorr and ECDSA. What does linearity allow you to do?
4. What is key aggregation (MuSig), and why does it make multisig look like a single-key spend?
5. Walk through a key-path spend: what is in the witness, and what does a node check?
6. Why did Taproot addresses need bech32m instead of bech32?

**Week folder:** [`week-09/`](./week-09/) · [exercises](./week-09/exercises/README.md) · [slides](./week-09/slides/slides.md) · [notes](./week-09/notes/README.md) · [solutions](./week-09/solutions/README.md)

---

### Week 10: Taproot scripts and graduation

**Opening question:** Now that you can build and spend a Taproot output, what would you like to build next?

Script trees, control blocks and the Taproot sighash. Finish the capstone, share what you built, and plan your next step into Bitcoin open source.

**Lessons:**

- [Script-path Taproot](https://bitcoindevs.xyz/decoding/script-path-taproot)
- [Taproot Signatures](https://bitcoindevs.xyz/decoding/taproot-signatures)
- [Capstone: Build & Spend a P2TR](https://bitcoindevs.xyz/decoding/build-spend-p2tr)

**Discussion questions:**

1. What is a tapleaf and a tapbranch? How do they combine into the Merkle root?
2. What is in a control block, and what does it prove?
3. Why does a script-path spend only reveal the one script that was used?
4. What changed in the Taproot sighash (BIP341) compared with segwit v0?
5. Design a script tree for an inheritance wallet. What goes in the key path, and what goes in each leaf?
6. What's your next step after this cohort: a Code Orange program, a project to contribute to, or a review club?

**Week folder:** [`week-10/`](./week-10/) · [exercises](./week-10/exercises/README.md) · [slides](./week-10/slides/slides.md) · [notes](./week-10/notes/README.md) · [solutions](./week-10/solutions/README.md)

---

## After the Cohort

Graduates are encouraged to:

1. **Go deeper into Bitcoin Core** - work through [After the cohort](./after-the-cohort.md): the codebase, the test framework and reviewing real pull requests
2. **Make a first contribution** - documentation, tests, reviews and small fixes all count
3. **Join a review club** - [Bitcoin Core PR Review Club](https://bitcoincore.reviews/) meets weekly
4. **Keep studying** - the [Privacy Track](../privacy-track/) and [Bitcoin Dojo](../bitcoin-dojo/) in this repo
5. **Apply to fellowships and grants** - Chaincode Labs, Summer of Bitcoin, Btrust, Vinteum, Brink and other Bitcoin developer grant programs
6. **Mentor the next cohort** - become a facilitator for future Decoding Bitcoin cohorts

---

## Facilitator Guide

### Before the Cohort

- [ ] Pick a start date and a weekly session time; update the schedule table above
- [ ] Open sign-ups and set up a Discord channel with one thread per week
- [ ] Read week 1's [notes](./week-01/notes/README.md) and [slides](./week-01/slides/slides.md)
- [ ] Recruit 1-2 co-hosts (previous graduates are ideal)

### Every Week

- [ ] Assign one discussion question to each participant and rotate the seminar roles
- [ ] Post the week's lessons and exercises after the previous session
- [ ] Skim the week's `notes/` (session plan and common mix-ups) and present from `slides/`
- [ ] Record the session for people who can't make it
- [ ] Check the Summariser's post and answer open questions on Discord
- [ ] Nudge anyone who has gone quiet for two weeks

### After the Cohort

- [ ] Collect feedback (anonymous survey)
- [ ] Celebrate the capstones and share them (with permission)
- [ ] Track graduates' first contributions over the next 3-6 months
- [ ] Update this curriculum based on feedback and open a pull request

---

## Credits

The lessons, tools and coding exercises this cohort follows are [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by [The Bitcoin Dev Project](https://bitcoindevs.xyz/). Please support and credit them when you run this cohort. This study guide (questions, exercises, solutions, slides and notes) is Code Orange's own work.

## License

This study guide is dedicated to the public domain under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). Fork it, translate it, teach with it. No permission needed. The Decoding Bitcoin lessons themselves belong to their authors and are not covered by this license.
