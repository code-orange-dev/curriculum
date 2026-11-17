# Week 05: Signing and the transaction exercises

[← Week 4](../week-04/) · [Syllabus](../README.md) · [Week 6 →](../week-06/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-5-signing-and-the-transaction-exercises). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** A signature proves something very specific. What exactly does it prove, and what doesn't it?

How a transaction gets signed: the sighash, what each sighash flag commits to, and why the signature goes in the input. Then work through the GitHub Classroom exercises.

## Lessons (on Decoding Bitcoin)

- [Signing Transactions](https://bitcoindevs.xyz/decoding/transaction-signing)
- [Exercises (GitHub Classroom)](https://bitcoindevs.xyz/decoding/transaction_exercises)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. What is the sighash (the message that actually gets signed)? Why can't you just sign the whole raw transaction?
2. Compare SIGHASH_ALL, SIGHASH_NONE and SIGHASH_SINGLE. When would anyone use ANYONECANPAY?
3. Why does a segwit signature commit to the amount being spent, and what bug did that fix?
4. What happens if the same nonce is used to sign two different messages with the same key?
5. Where does the signature live in a legacy input versus a segwit input?
6. How can a hardware wallet sign a transaction without ever showing the private key to your computer?

## Exercises

1. Complete the Decoding Bitcoin transaction exercises on GitHub Classroom. ([Coding exercises](https://bitcoindevs.xyz/decoding/transaction_exercises))
2. Pair up with someone on Discord and review each other's exercise solutions. Note one thing you'd do differently. ([Discord](https://discord.gg/xd6dmPF9bA))
3. Find a transaction that uses a sighash flag other than ALL (hint: search online for examples) and explain what it allowed.

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
