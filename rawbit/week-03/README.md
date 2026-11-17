# Week 3: Timelocks

[← Week 2](../week-02/) · [Syllabus](../README.md) · [Week 4 →](../week-04/)

> This week as it appears in the [rawBit Study Cohort syllabus](../README.md#week-3-timelocks).

**rawBit Lessons**: Lesson 5 (nLockTime/nSequence), Lesson 6 (OP_CHECKLOCKTIMEVERIFY)

**Topics:**
- Absolute timelocks: nLockTime (transaction-level)
- OP_CHECKLOCKTIMEVERIFY (CLTV): script-level absolute timelock
- Relative timelocks: nSequence and OP_CHECKSEQUENCEVERIFY (CSV)
- Use cases: payment channels, inheritance, escrow

**Exercises:**
1. Build a transaction with an nLockTime set to a future block height
2. Build a CLTV-locked output that can only be spent after block N
3. Build a CSV-locked output with a relative timelock of 144 blocks (~1 day)
4. Combine timelocks with multisig: "Alice can spend immediately with 2-of-3, OR Bob can spend alone after 1000 blocks"

## Status

`exercises/` and `solutions/` are still empty for this week. Build the exercises in [rawBit](https://github.com/rawBit-io/rawbit) and share them, or pick up a [good first issue](https://github.com/code-orange-dev/curriculum/labels/good%20first%20issue) to add them here.
