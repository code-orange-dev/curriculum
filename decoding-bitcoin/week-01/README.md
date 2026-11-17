# Week 01: Orientation and foundations

[Syllabus](../README.md) · [Week 2 →](../week-02/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-1-orientation-and-foundations). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

> **Intro week.** Just come to the first session. We'll meet each other, show you how the cohort and your dashboard work, and go through this week's topics together. Homework starts in week 2: lessons, your own question and exercises before Monday 23 November.

**Opening question:** If you had to explain Bitcoin to a friend in two sentences, what would you say, and what would you leave out?

Intro week. Meet the cohort, learn how the dashboard works and get comfortable on Decoding Bitcoin. The lessons below are a gentle start: the welcome, Bitcoin's history, and how Bitcoin keeps track of who owns what (coins, called UTXOs, not account balances). Read them after the session if you like.

## Lessons (on Decoding Bitcoin)

- [Welcome!](https://bitcoindevs.xyz/decoding/welcome)
- [Bitcoin History](https://bitcoindevs.xyz/decoding/bitcoin-history)
- [UTXO vs Account Models](https://bitcoindevs.xyz/decoding/utxo)

**Tools and extras:**

- [Tool: Hash Functions](https://bitcoindevs.xyz/decoding/hash-functions)
- [Optional: Interactive Developer Roadmap](https://bitcoindevs.xyz/decoding/interactive-roadmap)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. What problem did Bitcoin solve that earlier digital cash attempts (DigiCash, b-money, Bit Gold) could not?
2. Pick one moment from the Bitcoin History lesson and explain why it mattered for how Bitcoin works today.
3. What is a hash function? Name three properties Bitcoin relies on and where each one shows up.
4. Explain the UTXO model in your own words. Why is there no account balance stored anywhere?
5. Give one advantage and one disadvantage of UTXOs compared with an account model.
6. Why do people say "don't trust, verify"? What can you verify yourself, and what do you usually take on trust?

## Exercises

1. Introduce yourself in the cohort channel on Discord: your background, why you joined, and what you'd like to build. ([Discord](https://discord.gg/xd6dmPF9bA))
2. Use the Hash Functions tool: hash your name, then change one letter. How much of the output changes? ([Hash Functions tool](https://bitcoindevs.xyz/decoding/hash-functions))
3. Open a recent block on mempool.space, pick one transaction, and note its inputs, outputs and fee. Which output do you think is the change, and why? ([mempool.space](https://mempool.space))

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
