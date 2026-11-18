# Week 6: SegWit Transactions (P2WPKH)

[← Week 5](../week-05/) · [Syllabus](../README.md) · [Week 7 →](../week-07/)

> This week as it appears in the [rawBit Study Cohort syllabus](../README.md#week-6-segwit-transactions-p2wpkh).

**rawBit Lessons**: Lesson 10 (P2WPKH)

**Topics:**
- Segregated Witness: moving the witness outside the txid calculation
- P2WPKH (Pay-to-Witness-Public-Key-Hash): native SegWit
- Witness field structure
- Weight units vs virtual bytes
- The witness discount: why witness data is cheaper

**Exercises:**
1. Build a P2WPKH transaction in rawBit - compare structure to P2PKH
2. Calculate the weight and vbytes of your SegWit transaction
3. Build the same transaction as legacy P2PKH - compare sizes and fees
4. Verify that the witness data is excluded from the txid calculation

## Status

`exercises/` and `solutions/` are still empty for this week. Build the exercises in [rawBit](https://github.com/rawBit-io/rawbit) and share them, or pick up a [good first issue](https://github.com/code-orange-dev/curriculum/labels/good%20first%20issue) to add them here.
