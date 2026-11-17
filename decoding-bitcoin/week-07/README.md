# Week 07: P2SH and multisig

[← Week 6](../week-06/) · [Syllabus](../README.md) · [Week 8 →](../week-08/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-7-p2sh-and-multisig). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** Why might you want more than one key to move your bitcoin, and what new risks does that bring?

Bare multisig and why P2SH wrapped it up behind a hash, moving the cost and complexity from the sender to the receiver.

## Lessons (on Decoding Bitcoin)

- [P2SH: Pay To Script Hash (BIP 16)](https://bitcoindevs.xyz/decoding/p2sh)
- [P2MS: Pay To Multisig](https://bitcoindevs.xyz/decoding/p2ms)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. How does P2SH move the cost and complexity of a script from the sender to the receiver?
2. Explain the OP_CHECKMULTISIG off-by-one bug. Why has it never been fixed?
3. Why is bare multisig (P2MS) rarely used today?
4. What is the redeem script, and when does it finally appear on the blockchain?
5. Compare 2-of-3 multisig with a single key plus a backup. Which risks does each protect against?
6. BIP 16 was a soft fork. What does that mean, and how could old nodes still accept P2SH spends?

## Exercises

1. Do the P2MS exercises on Decoding Bitcoin, including the hard one. ([P2MS exercises](https://bitcoindevs.xyz/decoding/p2ms))
2. Find a real P2SH multisig spend and pull out the redeem script. What is M and what is N?
3. Draw a 2-of-3 setup for a small business: who holds each key, and where is it stored?

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
