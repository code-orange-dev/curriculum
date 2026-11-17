# Week 5: Transaction Malleability & Payment Channels

[← Week 4](../week-04/) · [Syllabus](../README.md) · [Week 6 →](../week-06/)

> This week as it appears in the [rawBit Study Cohort syllabus](../README.md#week-5-transaction-malleability--payment-channels).

**rawBit Lesson**: Lesson 8 (Transaction malleability), Lesson 9 (Payment channels)

**Topics:**
- Transaction malleability: how it works, why it's dangerous
- How scriptSig manipulation changes the txid without invalidating the transaction
- Payment channels: the foundational concept behind Lightning
- Building a simple unidirectional payment channel
- Why malleability breaks payment channels (motivating SegWit)

**Exercises:**
1. Demonstrate transaction malleability: modify a scriptSig encoding and show the txid changes
2. Build a simple payment channel: funding tx + commitment txs + settlement tx
3. Show how malleability would break the commitment transaction chain

## Status

`exercises/` and `solutions/` are still empty for this week. Build the exercises in [rawBit](https://github.com/rawBit-io/rawbit) and share them, or pick up a [good first issue](https://github.com/code-orange-dev/curriculum/labels/good%20first%20issue) to add them here.
