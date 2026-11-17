# Week 02: How a transaction lives

[← Week 1](../week-01/) · [Syllabus](../README.md) · [Week 3 →](../week-03/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-2-how-a-transaction-lives). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** When is a bitcoin payment actually final, and who gets to decide?

Follow a payment from the wallet that builds it, through the mempool, into a block. Then a first look at what a transaction is made of: version, inputs, outputs and locktime. Next week we go down to the bytes, so don't worry about the byte-level details yet.

## Lessons (on Decoding Bitcoin)

- [Transactions roadmap](https://bitcoindevs.xyz/decoding/roadmap)
- [Transaction Lifecycle](https://bitcoindevs.xyz/decoding/transaction-lifecycle)
- [Transaction Structure (first read: the main parts)](https://bitcoindevs.xyz/decoding/transaction-structure)

**Tools and extras:**

- [Tool: Reorg Calculator](https://bitcoindevs.xyz/decoding/reorg-calculator)
- [Tool: Transaction Decoder](https://bitcoindevs.xyz/decoding/transaction-decoder)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. Walk through the lifecycle of a payment: who builds it, who relays it, who checks it, and when is it confirmed?
2. What is the mempool? Why is there no single mempool that everyone shares?
3. What is a chain reorganisation, and why might a merchant wait for more than one confirmation?
4. Why does change go back to the sender as a new output instead of the old output being partly spent?
5. Name the main parts of a transaction in order and say in one line what each one is for.
6. What exactly does an input point to, and why is that enough to prove where the money came from?

## Exercises

1. Watch a transaction you didn't create go from unconfirmed to 1 confirmation on mempool.space. How long did it take? ([mempool.space](https://mempool.space))
2. Use the Reorg Calculator: what's the chance an attacker with 10% of the hashrate reverses a payment after 1, 3 and 6 confirmations? ([Reorg Calculator](https://bitcoindevs.xyz/decoding/reorg-calculator))
3. Paste a raw transaction into the Transaction Decoder and find its version, inputs, outputs and locktime. What does each input point to? ([Transaction Decoder](https://bitcoindevs.xyz/decoding/transaction-decoder))

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
