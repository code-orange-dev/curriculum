# Week 03: Inside a transaction, byte by byte

[← Week 2](../week-02/) · [Syllabus](../README.md) · [Week 4 →](../week-04/)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-3-inside-a-transaction-byte-by-byte). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** A transaction is just bytes. What do those bytes have to say for everyone to agree it's valid?

A whole week on transaction structure. Learn the byte-level basics (hex, little-endian, compact size), then take a raw transaction apart field by field, including segwit's marker, flag and witness.

## Lessons (on Decoding Bitcoin)

- [Technical Foundation](https://bitcoindevs.xyz/decoding/technical-foundation)
- [Transaction Structure (second read: every field)](https://bitcoindevs.xyz/decoding/transaction-structure)

**Tools and extras:**

- [Tool: Transaction Decoder](https://bitcoindevs.xyz/decoding/transaction-decoder)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. What is little-endian, and where does it trip people up when reading a txid?
2. What is a compact size (varint) and why does Bitcoin use one instead of fixed-size counts?
3. What does segwit move into the witness, and why does that fix transaction malleability?
4. What is nLockTime for? Give a real situation where you would set it.
5. What are the segwit marker and flag bytes, and how does a parser know whether a transaction is segwit?
6. How is a txid calculated, and why is a wtxid different?

## Exercises

1. Paste a raw transaction into the Transaction Decoder and label every field by hand. ([Transaction Decoder](https://bitcoindevs.xyz/decoding/transaction-decoder))
2. Take a txid and reverse its byte order. Check on mempool.space that you've found the same transaction. ([mempool.space](https://mempool.space))
3. Find one legacy and one segwit transaction. Compare their sizes and weights, and explain the difference.

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
