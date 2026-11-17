# Week 10: Taproot scripts and graduation

[← Week 9](../week-09/) · [Syllabus](../README.md) · [After the cohort →](../after-the-cohort.md)

> Part of the [Decoding Bitcoin syllabus](../README.md#week-10-taproot-scripts-and-graduation). Lessons are on [Decoding Bitcoin](https://bitcoindevs.xyz/decoding) by The Bitcoin Dev Project; this folder is Code Orange's study guide for the week.

**Opening question:** Now that you can build and spend a Taproot output, what would you like to build next?

Script trees, control blocks and the Taproot sighash. Finish the capstone, share what you built, and plan your next step into Bitcoin open source.

## Lessons (on Decoding Bitcoin)

- [Script-path Taproot](https://bitcoindevs.xyz/decoding/script-path-taproot)
- [Taproot Signatures](https://bitcoindevs.xyz/decoding/taproot-signatures)
- [Capstone: Build & Spend a P2TR](https://bitcoindevs.xyz/decoding/build-spend-p2tr)

## Discussion questions

Each participant owns one question and comes ready to explain it. Model answers are in [`solutions/`](solutions/README.md), so try first.

1. What is a tapleaf and a tapbranch? How do they combine into the Merkle root?
2. What is in a control block, and what does it prove?
3. Why does a script-path spend only reveal the one script that was used?
4. What changed in the Taproot sighash (BIP341) compared with segwit v0?
5. Design a script tree for an inheritance wallet. What goes in the key path, and what goes in each leaf?
6. What's your next step after this cohort: a Code Orange program, a project to contribute to, or a review club?

## Exercises

1. Complete the capstone: build and spend a P2TR output on regtest or signet. ([Capstone](https://bitcoindevs.xyz/decoding/build-spend-p2tr))
2. Present your capstone (or one exercise you're proud of) in 3 minutes at the final session.
3. Share your feedback on the cohort so the next one is even better.

More hands-on work, including bitcoin-cli labs on regtest, is in [`exercises/`](exercises/README.md).

## What's in this folder

| Folder | What it holds |
|---|---|
| [`exercises/`](exercises/README.md) | Hands-on exercises for this week |
| [`solutions/`](solutions/README.md) | Model answers to the questions and exercises (try them first!) |
| [`slides/`](slides/slides.md) | Facilitator slides for the session ([how to present them](../README.md#presenting-the-slides)) |
| [`notes/`](notes/README.md) | Key ideas, common mix-ups, a session plan and extra resources |
