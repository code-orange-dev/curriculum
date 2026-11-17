# Week 04: Building a transaction and paying the fee

[← Week 3](../week-03/) · [Syllabus](../README.md) · [Week 5 →](../week-05/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-4-building-a-transaction-and-paying-the-fee). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** Who should pay for block space, and how should they decide how much?

Pick inputs, create outputs and work out the fee in sats per virtual byte. See why weight units exist and how fee markets behave.

## Lessons (on Decoding Bitcoin)

- [Creating a Transaction](https://bitcoindevs.xyz/decoding/transaction-creation)
- [Fee Calculation](https://bitcoindevs.xyz/decoding/fee-calculation)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. Where is the fee written in a transaction? (Trick question: explain how it's actually found.)
2. What are weight units and virtual bytes, and why does a witness byte count less?
3. How does a wallet choose which UTXOs to spend? What can go wrong if it chooses badly?
4. What is dust, and why do nodes refuse to relay dust outputs?
5. Explain RBF and CPFP. When would you use each to speed up a stuck payment?
6. Fees were very high in some periods and very low in others. What drives the fee market?

## Exercises

1. Work out the fee and the fee rate (sat/vB) of a real transaction from its inputs, outputs and vsize. Check your answer on mempool.space. ([mempool.space](https://mempool.space))
2. Estimate the vsize of a 1-input, 2-output P2WPKH transaction, then check it against a real one.
3. Look at mempool.space's fee estimates now and again at another time of day. What changed, and why might it have? ([mempool.space](https://mempool.space))

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
