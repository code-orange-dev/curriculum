# Week 06: Script basics

[← Week 5](../week-05/) · [Syllabus](../README.md) · [Week 7 →](../week-07/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-6-script-basics). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** Why does Bitcoin use a tiny stack language instead of letting people write any program they like?

Bitcoin Script and the stack: how a locking script and an unlocking script run together, starting with the two oldest output types.

## Lessons (on Decoding Bitcoin)

- [Scripts overview](https://bitcoindevs.xyz/decoding/overview)
- [P2PK: Pay To Public Key](https://bitcoindevs.xyz/decoding/p2pk)
- [P2PKH: Pay To Public Key Hash](https://bitcoindevs.xyz/decoding/p2pkh)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. Explain how the stack works by running OP_2 OP_3 OP_ADD OP_5 OP_EQUAL step by step.
2. What is the difference between a scriptPubKey and a scriptSig, and in what order are they run?
3. Why did P2PKH replace P2PK for most payments? Give at least two reasons.
4. Run a P2PKH spend step by step: what is on the stack after each opcode?
5. Why is Script deliberately not Turing complete, and what does it gain from that?
6. Some opcodes were disabled early in Bitcoin's history. Why would you remove features from a running system?

## Exercises

1. Find a P2PK output in an early block (block 9 or 170 are good starts) and decode its script.
2. Write out the full P2PKH stack execution for a real spend on paper, then post a photo or text version on Discord. ([Discord](https://discord.gg/xd6dmPF9bA))
3. Decode the output scripts of a recent transaction and identify each output type.

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
