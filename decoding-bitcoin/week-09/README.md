# Week 09: Taproot: keys and Schnorr

[← Week 8](../week-08/) · [Syllabus](../README.md) · [Week 10 →](../week-10/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-9-taproot-keys-and-schnorr). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** Taproot makes many different spending setups look the same on-chain. Why is that good for everyone?

Why Taproot happened, how a P2TR output is built, what Schnorr signatures add, and the simple case: spending with a single key.

## Lessons (on Decoding Bitcoin)

- [Introduction to Taproot](https://bitcoindevs.xyz/decoding/introduction-taproot)
- [Pay to Taproot](https://bitcoindevs.xyz/decoding/p2tr)
- [Schnorr & BIP340](https://bitcoindevs.xyz/decoding/schnorr-bip340)
- [Key-path Taproot](https://bitcoindevs.xyz/decoding/key-path-taproot)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. What problems was Taproot designed to solve for privacy, efficiency and flexibility?
2. What is a tweaked public key, and why does P2TR use x-only (32-byte) keys?
3. Compare Schnorr and ECDSA. What does linearity allow you to do?
4. What is key aggregation (MuSig), and why does it make multisig look like a single-key spend?
5. Walk through a key-path spend: what is in the witness, and what does a node check?
6. Why did Taproot addresses need bech32m instead of bech32?

## Exercises

1. Find a P2TR key-path spend on mempool.space and compare its witness with a P2WPKH spend. ([mempool.space](https://mempool.space))
2. Decode a bc1p address: what witness version and program does it contain?
3. Explain the taproot tweak to someone in the cohort without using any maths. Post your explanation on Discord. ([Discord](https://discord.gg/xd6dmPF9bA))

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
